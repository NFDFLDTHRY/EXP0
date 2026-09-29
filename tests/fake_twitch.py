"""TEST-ONLY fake Twitch (id + Helix + EventSub WebSocket), fake GitHack host and LM Studio.

Never used by the product. One aiohttp app served twice:
  http://127.0.0.1:<plain>   for the controller (EXP0_TWITCH_* environment overrides)
  https://127.0.0.1:<tls>    for Chromium, which maps raw.githack.com, id.twitch.tv, api.twitch.tv and
                             eventsub.wss.twitch.tv onto it (--host-resolver-rules), so the pages run unmodified.
Behaviour copied from Twitch where it matters: implicit grant redirect with #fragment, validate,
users, EventSub WebSocket welcome/keepalive/reconnect/close codes, subscriptions bound to a session,
chat echo and CORS on the API hosts. This fake cannot prove live Twitch delivery.
"""
from __future__ import annotations

import asyncio
import json
import threading
import time
import uuid
from pathlib import Path
from urllib.parse import urlencode

from aiohttp import WSMsgType, web

CLIENT_ID = "abcdefghijklmnopqrstuvwxyz0123"
USERS = {
    "700001": {"id": "700001", "login": "enemy_acct", "display_name": "Enemy_Acct"},
    "123456": {"id": "123456", "login": "bigrigjay", "display_name": "BigRigJay"},
    "666": {"id": "666", "login": "totally_not_jay", "display_name": "bigrigjay"},
    "700002": {"id": "700002", "login": "other_acct", "display_name": "Other_Acct"},
    "555": {"id": "555", "login": "viewer1", "display_name": "Viewer1"},
}
TOKENS = {
    "tokenemy0001": {"user_id": "700001", "scopes": ["user:read:chat", "user:write:chat"]},
    "tokother0001": {"user_id": "700002", "scopes": ["user:read:chat", "user:write:chat"]},
}
CTYPES = {".html": "text/html; charset=utf-8", ".js": "application/javascript", ".md": "text/plain; charset=utf-8"}


def iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class FakeTwitch:
    def __init__(self, static_root: Path, plain_port: int, tls_port: int, lm_port: int, cert: Path, key: Path):
        self.static_root, self.plain_port, self.tls_port, self.lm_port = static_root, plain_port, tls_port, lm_port
        self.cert, self.key = cert, key
        self.tokens = {k: dict(v, valid=True) for k, v in TOKENS.items()}
        # There is exactly one OAuth surface in the V2 product: ally.html.
        self.login_as = {"ally.html": "tokenemy0001"}
        self.sessions: dict = {}
        self.subs: dict = {}
        self.sub_posts: list = []
        self.chat_sent: list = []
        self.delivered: list = []
        self.authorize_requests: list = []
        self.lm_models = ["gemma-4-e4b-it"]
        self.lm_requests: list = []
        self.lm_responses: list = []
        self.lm_delay_s = 0.0
        self.lm_runner = None
        self.loop = None
        self.ready = threading.Event()

    # ---------------------------------------------------------------- plumbing
    def start(self) -> None:
        threading.Thread(target=self._thread, daemon=True).start()
        if not self.ready.wait(15):
            raise RuntimeError("fake twitch did not start")

    def _thread(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._serve())
        self.ready.set()
        self.loop.run_forever()

    async def _serve(self) -> None:
        import ssl
        app = web.Application(middlewares=[self._cors])
        app.router.add_get("/oauth2/authorize", self.authorize)
        app.router.add_get("/oauth2/validate", self.validate)
        app.router.add_post("/oauth2/revoke", self.revoke)
        app.router.add_get("/helix/users", self.users)
        app.router.add_post("/helix/eventsub/subscriptions", self.subscribe)
        app.router.add_delete("/helix/eventsub/subscriptions", self.unsubscribe)
        app.router.add_post("/helix/chat/messages", self.chat_send)
        app.router.add_get("/ws", self.ws_handler)
        app.router.add_get("/NFDFLDTHRY/EXP0/main/{name}", self.static)
        app.router.add_route("OPTIONS", "/{tail:.*}", self.options)
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, "127.0.0.1", self.plain_port).start()
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.load_cert_chain(str(self.cert), str(self.key))
        await web.TCPSite(runner, "127.0.0.1", self.tls_port, ssl_context=ctx).start()
        await self._lm_start()

    def call(self, coro_or_fn, *args):
        async def run():
            r = coro_or_fn(*args)
            return await r if asyncio.iscoroutine(r) else r
        return asyncio.run_coroutine_threadsafe(run(), self.loop).result(15)

    @web.middleware
    async def _cors(self, request, handler):
        resp = await handler(request)
        if request.path.startswith(("/helix", "/oauth2/validate", "/oauth2/revoke")):
            resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp

    async def options(self, request):
        return web.Response(status=204, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, DELETE, PATCH, PUT, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Client-Id, Content-Type",
            "Access-Control-Max-Age": "600"})

    async def static(self, request):
        name = request.match_info["name"]
        p = (self.static_root / name).resolve()
        if p.parent != self.static_root.resolve() or not p.is_file():
            return web.Response(status=404, text="404")
        return web.Response(body=p.read_bytes(), headers={"Content-Type": CTYPES.get(p.suffix, "application/octet-stream"),
                                                           "Cache-Control": "no-store"})

    # ---------------------------------------------------------------- id.twitch.tv
    async def authorize(self, request):
        q = dict(request.query)
        self.authorize_requests.append(q)
        if q.get("client_id") != CLIENT_ID:
            return web.Response(status=400, text="invalid client")
        page = q.get("redirect_uri", "").rsplit("/", 1)[-1]
        tok = self.login_as.get(page)
        if tok is None:
            return web.Response(status=403, text="this page has no OAuth flow")
        frag = urlencode({"access_token": tok, "scope": " ".join(self.tokens[tok]["scopes"]),
                          "state": q.get("state", ""), "token_type": "bearer"})
        raise web.HTTPFound(q["redirect_uri"] + "#" + frag)

    def _token(self, request, prefixes=("Bearer ", "OAuth ")):
        auth = request.headers.get("Authorization", "")
        for p in prefixes:
            if auth.startswith(p):
                t = self.tokens.get(auth[len(p):])
                if t and t["valid"]:
                    return t
        return None

    async def validate(self, request):
        t = self._token(request)
        if not t:
            return web.json_response({"status": 401, "message": "invalid access token"}, status=401)
        u = USERS[t["user_id"]]
        return web.json_response({"client_id": CLIENT_ID, "login": u["login"], "scopes": t["scopes"],
                                  "user_id": u["id"], "expires_in": 5011234})

    async def revoke(self, request):
        form = await request.post()
        t = self.tokens.get(form.get("token", ""))
        if t:
            t["valid"] = False
        return web.Response(status=200)

    # ---------------------------------------------------------------- api.twitch.tv/helix
    def _helix_auth(self, request):
        t = self._token(request, ("Bearer ",))
        if not t or request.headers.get("Client-Id") != CLIENT_ID:
            return None
        return t

    async def users(self, request):
        if not self._helix_auth(request):
            return web.json_response({"error": "Unauthorized", "status": 401, "message": "Invalid OAuth token"}, status=401)
        login, uid = request.query.get("login", "").lower(), request.query.get("id")
        data = [dict(u, created_at="2015-01-01T00:00:00Z", description="", type="", broadcaster_type="")
                for u in USERS.values() if (login and u["login"] == login) or (uid and u["id"] == uid)]
        return web.json_response({"data": data})

    async def subscribe(self, request):
        t = self._helix_auth(request)
        if not t:
            return web.json_response({"error": "Unauthorized", "status": 401, "message": "Invalid OAuth token"}, status=401)
        body = await request.json()
        typ, cond, tr = body.get("type"), body.get("condition") or {}, body.get("transport") or {}
        self.sub_posts.append({"user_id": t["user_id"], "type": typ, "condition": cond, "session_id": tr.get("session_id")})
        sess = self.sessions.get(tr.get("session_id"))
        if tr.get("method") != "websocket" or not sess or sess.get("closed"):
            return web.json_response({"error": "Bad Request", "status": 400, "message": "websocket transport session does not exist or has already disconnected"}, status=400)
        if typ == "channel.chat.message":
            if cond.get("user_id") != t["user_id"] or "user:read:chat" not in t["scopes"]:
                return web.json_response({"error": "Forbidden", "status": 403, "message": "subscription missing proper authorization"}, status=403)
        else:
            return web.json_response({"error": "Bad Request", "status": 400, "message": "unsupported type"}, status=400)
        sub_id = str(uuid.uuid4())
        sub = {"id": sub_id, "status": "enabled", "type": typ, "version": "1", "condition": cond,
               "created_at": iso(), "transport": {"method": "websocket", "session_id": sess["id"]}, "cost": 0}
        self.subs[sub_id] = sub
        sess["subs"].add(sub_id)
        return web.json_response({"data": [sub], "total": len(self.subs), "total_cost": 0, "max_total_cost": 10}, status=202)

    async def unsubscribe(self, request):
        self.subs.pop(request.query.get("id", ""), None)
        return web.Response(status=204)

    async def chat_send(self, request):
        t = self._helix_auth(request)
        if not t:
            return web.json_response({"error": "Unauthorized", "status": 401, "message": "Invalid OAuth token"}, status=401)
        body = await request.json()
        if body.get("sender_id") != t["user_id"] or "user:write:chat" not in t["scopes"]:
            return web.json_response({"error": "Forbidden", "status": 403, "message": "sender mismatch or missing scope"}, status=403)
        mid = str(uuid.uuid4())
        self.chat_sent.append({"broadcaster_id": body.get("broadcaster_id"), "sender_id": body.get("sender_id"),
                               "message": body.get("message"), "message_id": mid, "t": time.time()})
        asyncio.get_running_loop().call_later(0.05, lambda: asyncio.ensure_future(
            self.deliver_chat(body["broadcaster_id"], t["user_id"], body["message"], mid)))
        return web.json_response({"data": [{"message_id": mid, "is_sent": True, "drop_reason": None}]})

    # ---------------------------------------------------------------- EventSub websocket
    async def ws_handler(self, request):
        ws = web.WebSocketResponse(autoping=True, heartbeat=None)
        await ws.prepare(request)
        sid = "sess_" + uuid.uuid4().hex[:12]
        ka = int(request.query.get("keepalive_timeout_seconds", "10"))
        sess = {"id": sid, "ws": ws, "subs": set(), "host": request.host, "secure": request.secure, "keepalive": ka,
                "last": time.time(), "closed": False, "reconnect_of": request.query.get("reconnect_from")}
        self.sessions[sid] = sess
        old = self.sessions.get(sess["reconnect_of"] or "")
        if old:
            for sub_id in list(old["subs"]):
                self.subs[sub_id]["transport"]["session_id"] = sid
                sess["subs"].add(sub_id)
            old["subs"] = set()
        await self._send(sess, {"metadata": {"message_id": str(uuid.uuid4()), "message_type": "session_welcome", "message_timestamp": iso()},
                                "payload": {"session": {"id": sid, "status": "connected", "connected_at": iso(),
                                                        "keepalive_timeout_seconds": ka, "reconnect_url": None}}})
        task = asyncio.create_task(self._keepalive(sess))
        try:
            async for msg in ws:
                if msg.type in (WSMsgType.TEXT, WSMsgType.BINARY):
                    await ws.close(code=4001, message=b"client sent inbound traffic")
                    break
        finally:
            task.cancel()
            sess["closed"] = True
            for sub_id in sess["subs"]:
                if sub_id in self.subs:
                    self.subs[sub_id]["status"] = "websocket_disconnected"
        return ws

    async def _send(self, sess, obj) -> None:
        if sess["closed"] or sess["ws"].closed:
            return
        await sess["ws"].send_str(json.dumps(obj))
        sess["last"] = time.time()

    async def _keepalive(self, sess) -> None:
        while True:
            await asyncio.sleep(0.5)
            if time.time() - sess["last"] >= sess["keepalive"]:
                await self._send(sess, {"metadata": {"message_id": str(uuid.uuid4()), "message_type": "session_keepalive",
                                                     "message_timestamp": iso()}, "payload": {}})

    async def notify(self, typ: str, match, event: dict, message_id: str | None = None) -> list:
        sent = []
        for sub in list(self.subs.values()):
            if sub["type"] != typ or sub["status"] != "enabled" or not match(sub["condition"]):
                continue
            sess = self.sessions.get(sub["transport"]["session_id"])
            if not sess or sess["closed"]:
                continue
            msg = {"metadata": {"message_id": message_id or str(uuid.uuid4()), "message_type": "notification",
                                "message_timestamp": iso(), "subscription_type": typ, "subscription_version": "1"},
                   "payload": {"subscription": sub, "event": event}}
            await self._send(sess, msg)
            self.delivered.append({"session_id": sess["id"], "msg": msg})
            sent.append(msg)
        return sent

    async def deliver_chat(self, broadcaster_id: str, chatter_id: str, text: str, message_id: str | None = None):
        b, u = USERS[broadcaster_id], USERS[chatter_id]
        ev = {"broadcaster_user_id": b["id"], "broadcaster_user_login": b["login"], "broadcaster_user_name": b["display_name"],
              "chatter_user_id": u["id"], "chatter_user_login": u["login"], "chatter_user_name": u["display_name"],
              "message_id": message_id or str(uuid.uuid4()),
              "message": {"text": text, "fragments": [{"type": "text", "text": text, "cheermote": None, "emote": None, "mention": None}]},
              "color": "", "badges": [], "message_type": "text", "cheer": None, "reply": None, "channel_points_custom_reward_id": None,
              "source_broadcaster_user_id": None, "source_broadcaster_user_login": None, "source_broadcaster_user_name": None,
              "source_message_id": None, "source_badges": None}
        return await self.notify("channel.chat.message", lambda c: c.get("broadcaster_user_id") == broadcaster_id, ev)

    # ---------------------------------------------------------------- test controls
    def session_of(self, user_id: str, typ: str = "channel.chat.message"):
        for sub in self.subs.values():
            if sub["type"] == typ and sub["status"] == "enabled" and sub["condition"].get("user_id") == user_id:
                return sub["transport"]["session_id"]
        return None

    async def send_reconnect(self, session_id: str) -> None:
        sess = self.sessions[session_id]
        scheme = "wss" if sess["secure"] else "ws"
        url = f"{scheme}://{sess['host']}/ws?keepalive_timeout_seconds={sess['keepalive']}&reconnect_from={session_id}"
        await self._send(sess, {"metadata": {"message_id": str(uuid.uuid4()), "message_type": "session_reconnect", "message_timestamp": iso()},
                                "payload": {"session": {"id": session_id, "status": "reconnecting", "keepalive_timeout_seconds": None,
                                                        "reconnect_url": url, "connected_at": iso()}}})

    async def drop(self, session_id: str, code: int = 4006) -> None:
        sess = self.sessions[session_id]
        await sess["ws"].close(code=code, message=b"network error")

    async def replay(self, entry: dict) -> None:
        sess = self.sessions.get(entry["session_id"])
        if sess:
            await self._send(sess, entry["msg"])

    # ---------------------------------------------------------------- fake LM Studio (127.0.0.1 only)
    async def _lm_start(self) -> None:
        app = web.Application()

        async def models(_request):
            return web.json_response({"object": "list", "data": [{"id": m, "object": "model", "owned_by": "organization_owner"} for m in self.lm_models]})
        async def completions(request):
            body = await request.json()
            self.lm_requests.append(body)
            delay = self.lm_delay_s
            if delay:
                await asyncio.sleep(delay)
            if self.lm_responses:
                proposed = self.lm_responses.pop(0)
            elif (body.get("messages") or [{}])[0].get("content", "").startswith("You narrate"):
                observation = json.loads(body["messages"][1]["content"])
                proposed = {"narration": observation["summary"] + " The air holds its breath."}
            else:
                proposed = {"enemy_action": "wait", "enemy_target": None, "narration": "The enemy watches from the ridge."}
            if isinstance(proposed, dict):
                proposed = json.dumps(proposed, separators=(",", ":"))
            return web.json_response({"id": "fake-gemma-" + uuid.uuid4().hex,
                                      "object": "chat.completion", "created": int(time.time()),
                                      "model": body.get("model", "gemma-4-e4b-it"),
                                      "choices": [{"index": 0, "message": {"role": "assistant", "content": proposed},
                                                   "finish_reason": "stop"}],
                                      "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70}})
        app.router.add_get("/v1/models", models)
        app.router.add_post("/v1/chat/completions", completions)
        self.lm_runner = web.AppRunner(app)
        await self.lm_runner.setup()
        await web.TCPSite(self.lm_runner, "127.0.0.1", self.lm_port).start()

    async def lm_stop(self) -> None:
        if self.lm_runner:
            await self.lm_runner.cleanup()
            self.lm_runner = None

    async def lm_restart(self) -> None:
        if not self.lm_runner:
            await self._lm_start()
