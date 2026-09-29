#!/usr/bin/env python3
"""EXP0 V2 local integration proof; fake Twitch and fake LM Studio, NEVER live proof.

Runs a copied ./setup.sh, ./exp0 process, loopback HTTP API, EventSub WebSocket,
chat send/echo, strict fake model, and disk persistence. No browser is required.
The public/ally pages are statically inspected; the actual browser OAuth flow and
live Twitch behavior remain PENDING-REAL.

    python3 -m pip install aiohttp
    python3 tests/e2e_v2.py

Returns 1 on any failed check. The active product never imports tests/.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path

from fake_twitch import CLIENT_ID, FakeTwitch

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RUN = HERE / ".run"
APP = RUN / "EXP0"
PLAIN, TLS, LM, PORT = 9780, 9443, 1234, 8788
GH = "https://raw.githack.com/NFDFLDTHRY/EXP0/main/"
RESULTS: list[tuple[str, bool]] = []
LOG: list[str] = []
ENV = dict(os.environ, EXP0_TWITCH_ID_URL=f"http://127.0.0.1:{PLAIN}",
           EXP0_TWITCH_HELIX_URL=f"http://127.0.0.1:{PLAIN}/helix",
           EXP0_TWITCH_EVENTSUB_URL=f"ws://127.0.0.1:{PLAIN}/ws")
ENV.pop("TERMUX_VERSION", None)
ENV.pop("PREFIX", None)
DIRECT = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def check(name: str, ok, detail="") -> bool:
    ok = bool(ok)
    RESULTS.append((name, ok))
    line = ("PASS " if ok else "FAIL ") + name + ((" -- " + str(detail)[:500]) if detail != "" else "")
    print(line, flush=True)
    LOG.append(line)
    return ok


def sh(*args: str, timeout: int = 60):
    p = subprocess.run(args, cwd=APP, env=ENV, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr


def key() -> str:
    return (APP / "var" / "session.key").read_text().strip()


def ctl(method: str, path: str, body=None, auth=True, headers=None):
    h = {"Authorization": "Bearer " + key()} if auth else {}
    h.update(headers or {})
    data = json.dumps(body).encode() if body is not None else None
    if data is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=data, method=method, headers=h)
    try:
        with DIRECT.open(req, timeout=10) as r:
            return r.status, dict(r.headers), json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, dict(e.headers), json.loads(e.read() or b"{}")
        except ValueError:
            return e.code, dict(e.headers), {}


def status() -> dict:
    code, _, obj = ctl("GET", "/v1/status")
    assert code == 200, (code, obj)
    return obj


def hist() -> list[dict]:
    p = APP / "var" / "history.ndjson"
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def records(kind: str, **fields) -> list[dict]:
    return [r for r in hist() if r.get("kind") == kind and all(r.get("data", {}).get(k) == v for k, v in fields.items())]


def until(predicate, timeout: float = 8.0) -> bool:
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        try:
            if predicate():
                return True
        except (AssertionError, KeyError, IndexError, OSError):
            pass
        time.sleep(.08)
    return False


def world() -> dict:
    return status()["game"]["world"]


def send(tw: FakeTwitch, chatter: str, message: str, msg_id: str):
    deliveries = tw.call(tw.deliver_chat, "123456", chatter, message, msg_id)
    assert deliveries, "EventSub subscription not active"
    return deliveries[0]


def require(ok: bool, message: str):
    if not ok:
        raise AssertionError(message)


def main() -> int:
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    shutil.copytree(REPO, APP, ignore=shutil.ignore_patterns(".git", "tests", "var", "exp0", "__pycache__"))
    subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                    "-keyout", str(RUN / "key.pem"), "-out", str(RUN / "cert.pem"),
                    "-days", "2", "-subj", "/CN=exp0-fake"], check=True, capture_output=True)
    tw = FakeTwitch(APP, PLAIN, TLS, LM, RUN / "cert.pem", RUN / "key.pem")
    tw.start()
    try:
        run_checks(tw)
    except Exception:
        traceback.print_exc()
        check("harness completed without an uncaught exception", False)
    finally:
        if (APP / "exp0").exists():
            rc, out = sh("./exp0", "stop")
            check("./exp0 stop", rc == 0 and ("stopped" in out or "not running" in out), out.strip())
        check("ephemeral controller key removed after stop", not (APP / "var" / "session.key").exists())
        for p in (APP / "var").glob("**/*"):
            if p.is_file():
                content = p.read_bytes()
                check("token absent from var/" + p.name,
                      all(t.encode() not in content for t in ("tokenemy0001", "tokother0001")))
        if (APP / "var" / "history.ndjson").exists():
            seqs = [r["seq"] for r in hist()]
            check("append-only evidence sequence is gapless", seqs == list(range(1, len(seqs) + 1)), len(seqs))
    failures = [n for n, ok in RESULTS if not ok]
    summary = f"{len(RESULTS)} checks, {len(failures)} failed; FAKE TWITCH / FAKE GEMMA ONLY"
    print("\n" + summary)
    (RUN / "e2e-v2.log").write_text("\n".join(LOG) + "\n" + summary + "\n")
    return int(bool(failures))


def run_checks(tw: FakeTwitch) -> None:
    # Static product law: the public page has zero authority, only ally OAuth exists.
    ally = (APP / "ally.html").read_text()
    village = (APP / "village.html").read_text()
    check("village.html has no OAuth, token or whisper JavaScript", not re.search(
        r"oauth2/authorize|access_token|sessionStorage|localStorage|whisper|verified.phone|fetch\s*\(|user:manage:whispers",
        village, re.I))
    check("public page explains !do, !suggest and BigRigJay channel", all(s in village.lower() for s in
          ("!do", "!suggest", "bigrigjay")))
    check("ally presents only chat read/write and derives OAuth scopes from controller",
          "user:read:chat" in ally and "user:write:chat" in ally and
          "scope: ST.required_scopes.join(' ')" in ally and "user:manage:whispers" not in ally)

    rc, out = sh("./setup.sh", "--role", "all-in-one", "--port", str(PORT))
    require(check("fresh ./setup.sh --role all-in-one", rc == 0, out[-350:]), "setup failed")
    check("./exp0 generated executable", os.access(APP / "exp0", os.X_OK))
    check("var/ mode 700", (APP / "var").stat().st_mode & 0o777 == 0o700)
    rc, out = sh("./setup.sh", "--yes")
    check("setup rerun keeps config", rc == 0 and json.loads((APP / "var" / "config.json").read_text())["port"] == PORT)
    rc, out = sh("./setup.sh", "--role", "core")
    check("unbuilt split role honestly refused", rc == 3 and "not built" in out)
    # Tight local test rate limits without imposing a real Twitch behavior on production config.
    cfg_path = APP / "var" / "config.json"
    cfg = json.loads(cfg_path.read_text())
    cfg["limits"].update(chat_min_interval_s=.01, chat_max_per_min=100, repeat_window_s=.01)
    cfg_path.write_text(json.dumps(cfg))
    rc, out = sh("./exp0", "start")
    require(check("./exp0 start prints local ally link", rc == 0 and re.search(r"ally\.html#p=8788&k=", out), out[-300:]),
            "start failed")
    rc, out = sh("./exp0", "status")
    check("./exp0 status RUNNING", rc == 0 and "RUNNING" in out)
    code, _, health = ctl("GET", "/v1/health", auth=False)
    check("unprivileged health contains no secret", code == 200 and set(health) == {"ok", "exp0", "role"})
    code, _, body = ctl("GET", "/v1/status", auth=False)
    check("status requires ephemeral local key", code == 401, body)
    code, _, body = ctl("GET", "/v1/status", headers={"Origin": "https://evil.example"})
    check("foreign origin refused despite valid key", code == 403, body)

    code, _, body = ctl("POST", "/v1/op/client_id", {"client_id": CLIENT_ID})
    require(check("client ID accepted", code == 200, body), "client ID failed")
    code, _, body = ctl("POST", "/v1/op/twitch/token", {"access_token": "tokenemy0001"})
    require(check("only USER account token accepted", code == 200 and body.get("user_id") == "700001" and
                  body.get("missing_scopes") == [], body), "token failed")
    check("controller requires only chat scopes", status().get("required_scopes") ==
          ["user:read:chat", "user:write:chat"], status().get("required_scopes"))
    ctl("POST", "/v1/op/identity/confirm", {})
    code, _, body = ctl("POST", "/v1/op/opponent", {"login": "bigrigjay"})
    require(check("BigRigJay numeric ID resolved", code == 200 and body.get("id") == "123456", body), "resolve failed")
    code, _, new_game = ctl("POST", "/v1/op/game/new", {})
    require(check("canonical village initialized with a versioned world", code == 200 and
                  isinstance(new_game.get("world"), dict) and new_game["world"].get("turn") == 0, new_game),
            "new game failed")
    code, _, probe = ctl("POST", "/v1/op/lmstudio/probe", {})
    check("localhost model discovery reports actual fake model ID", code == 200 and
          "gemma-4-e4b-it" in probe.get("models", []), probe)
    code, _, body = ctl("POST", "/v1/op/edge/start", {})
    require(check("single user EventSub edge starts", code == 200, body), "edge failed")
    require(until(lambda: status()["edge"]["connected"] and len(tw.sub_posts) >= 1), "subscription did not connect")
    want = {"broadcaster_user_id": "123456", "user_id": "700001"}
    check("only BigRigJay chat subscribed; no whispers or second account",
          len(tw.sub_posts) == 1 and tw.sub_posts[0]["type"] == "channel.chat.message"
          and tw.sub_posts[0]["condition"] == want and tw.sub_posts[0]["user_id"] == "700001", tw.sub_posts)
    rc, doctor = sh("./exp0", "doctor", timeout=35)
    check("./exp0 doctor checks loopback controller, Twitch and discovered model",
          rc == 0 and "controller running" in doctor
          and "sent session_welcome" in doctor and "models: gemma-4-e4b-it" in doctor,
          " | ".join(line.strip() for line in doctor.splitlines() if "FAIL" in line or "WARN" in line))

    # Both roles may ask for help and status, but neither status command mutates world.
    initial = world().copy()
    send(tw, "123456", "!help", "v2-help-jay")
    require(until(lambda: any("!do" in d["message"] for d in tw.chat_sent)), "help not sent")
    check("!help answered in Jay's chat from user's account", tw.chat_sent[-1]["broadcaster_id"] == "123456"
          and tw.chat_sent[-1]["sender_id"] == "700001")
    send(tw, "555", "!status", "v2-status-viewer")
    require(until(lambda: any(r["data"].get("message_id") == "v2-status-viewer" for r in records("command"))),
            "viewer status not seen")
    check("!status view did not change world", world() == initial)
    send(tw, "555", "!suggest fortify west", "v2-council")
    require(until(lambda: records("council", message_id="v2-council")), "council not recorded")
    check("viewer suggestion has no direct world authority", world() == initial)
    code, _, advice = ctl("POST", "/v1/op/advice", {"text": "Watch the western ridge."})
    check("private user advice saved without direct mutation", code == 200 and world() == initial, advice)
    code, _, tainted = ctl("POST", "/v1/op/advice", {"text": "Do not repeat tokenemy0001 in game output."})
    check("accidentally pasted OAuth token in ally advice is redacted before disk evidence",
          code == 200 and "tokenemy0001" not in json.dumps(tainted) and
          all(b"tokenemy0001" not in (APP / "var" / name).read_bytes()
              for name in ("state.json", "history.ndjson")))
    check("token-bearing advice alone cannot mutate world", world() == initial)

    # Action via real WebSocket, fake JSON model, deterministic engine and durable commit.
    first_sent = len(tw.chat_sent)
    send(tw, "123456", "!do scout north", "v2-scout")
    require(until(lambda: records("applied", message_id="v2-scout") and len(tw.chat_sent) > first_sent, 12),
            "scout turn did not commit and narrate")
    after_scout = world().copy()
    check("!do produced exactly one committed commander action", len(records("applied", message_id="v2-scout")) == 1
          and after_scout["turn"] == initial["turn"] + 1, after_scout)
    check("fake Gemma called with discovered loaded ID", bool(tw.lm_requests) and
          tw.lm_requests[0].get("model") == "gemma-4-e4b-it", tw.lm_requests[:1])
    context = json.loads(tw.lm_requests[0]["messages"][1]["content"]) if tw.lm_requests else {}
    context_text = json.dumps(context)
    check("Gemma receives legal state, council and ally advice but no private engine fields",
          all(s in context_text for s in ("scout", "fortify west", "Watch the western ridge."))
          and not any(k.startswith("_") for k in context.get("world", {}))
          and "tokenemy0001" not in context_text)
    commitment = records("applied", message_id="v2-scout")[-1]["seq"]
    narrations = [r for r in hist() if r.get("kind") == "action" and
                  r.get("data", {}).get("body", {}).get("broadcaster_id") == "123456"]
    check("narration is attempted only after durable applied record", any(r["seq"] > commitment for r in narrations),
          [(r["seq"], r["kind"]) for r in hist()[-12:]])
    check("narration reached BigRigJay chat from user's account",
          tw.chat_sent[-1]["broadcaster_id"] == "123456" and tw.chat_sent[-1]["sender_id"] == "700001")
    check("valid Gemma observation narration accepted after the authoritative summary",
          bool(records("model", op="narration_accepted", message_id="v2-scout")) and
          any(m["message"].startswith("Day 2:") and m["message"].endswith("The air holds its breath.")
              for m in tw.chat_sent))

    # EventSub replay + same Twitch chat message in a new EventSub envelope.
    previous = next(d for d in reversed(tw.delivered) if d["msg"]["payload"]["event"].get("message_id") == "v2-scout")
    sent_before = len(tw.chat_sent)
    tw.call(tw.replay, previous)
    tw.call(tw.deliver_chat, "123456", "123456", "!do scout north", "v2-scout")
    time.sleep(.3)
    check("duplicate Twitch message cannot replay action or narration", len(records("applied", message_id="v2-scout")) == 1
          and world() == after_scout and len(tw.chat_sent) == sent_before)

    # Same display name, other numeric ID: council input at most, never commander.
    send(tw, "666", "!do attack west", "v2-impostor")
    time.sleep(.3)
    check("impostor display name cannot become commander", world() == after_scout
          and not records("applied", message_id="v2-impostor"))
    model_before_illegal_command = len(tw.lm_requests)
    send(tw, "123456", "!do build spaceship", "v2-illegal-command")
    require(until(lambda: records("admission", message_id="v2-illegal-command")), "illegal command not examined")
    check("illegal commander action creates no model turn or state mutation",
          world() == after_scout and len(tw.lm_requests) == model_before_illegal_command
          and not records("applied", message_id="v2-illegal-command"))

    # Two invalid model replies: initial and one repair attempt. Both must skip.
    tw.lm_responses.extend(["{invalid json", "{still invalid"])
    before_invalid = world().copy()
    send(tw, "123456", "!do gather food", "v2-invalid-json")
    require(until(lambda: records("model", op="turn_skipped", message_id="v2-invalid-json"), 10),
            "malformed model did not skip")
    check("malformed Gemma JSON does not mutate world", world() == before_invalid
          and not records("applied", message_id="v2-invalid-json")
          and len(records("model", op="proposal_rejected", message_id="v2-invalid-json")) == 2)
    invalid_proposal = {"enemy_action": "mint_gold", "enemy_target": None, "narration": "Surprise gold."}
    tw.lm_responses.extend([invalid_proposal, invalid_proposal])
    send(tw, "123456", "!do recruit defenders", "v2-illegal-json")
    require(until(lambda: records("model", op="turn_skipped", message_id="v2-illegal-json"), 10),
            "illegal model did not skip")
    check("illegal Gemma action cannot mutate world", world() == before_invalid
          and not records("applied", message_id="v2-illegal-json")
          and len(records("model", op="proposal_rejected", message_id="v2-illegal-json")) == 2)

    # Many suggestions remain advisory and only a bounded tail is persisted.
    for n in range(16):
        send(tw, "555", f"!suggest council {n}", f"v2-council-{n}")
    require(until(lambda: len(records("council")) >= 17, 10), "council burst not delivered")
    recent = status()["recent_council"]
    check("recent council stays bounded and ordered, without changing world",
          len(recent) == 12 and recent[-1]["text"] == "council 15"
          and not any(r["text"] == "fortify west" for r in recent) and world() == before_invalid)

    # E-STOP is a hard state and external-action brake.
    code, _, body = ctl("POST", "/v1/op/estop", {})
    require(check("E-STOP set", code == 200 and body.get("estop") is True, body), "estop failed")
    stopped_sent, stopped_model, stopped_world = len(tw.chat_sent), len(tw.lm_requests), world().copy()
    send(tw, "123456", "!do attack east", "v2-estop")
    time.sleep(.5)
    check("E-STOP stops model turn, mutation and Twitch output", world() == stopped_world
          and len(tw.chat_sent) == stopped_sent and len(tw.lm_requests) == stopped_model)
    ctl("POST", "/v1/op/estop/clear", {})

    # Process restart preserves world, dedupe and council; token is memory-only.
    before_restart = world().copy()
    sent_before_restart = len(tw.chat_sent)
    rc, out = sh("./exp0", "restart")
    require(check("./exp0 restart gives a new ephemeral key", rc == 0 and "ally.html#" in out, out[-300:]),
            "restart failed")
    check("world survived restart unchanged", world() == before_restart)
    check("token is absent after restart", status()["twitch"]["token"] is False)
    check("recent council survives restart", "council 15" in json.dumps(status().get("recent_council", [])))
    ctl("POST", "/v1/op/twitch/token", {"access_token": "tokenemy0001"})
    ctl("POST", "/v1/op/identity/confirm", {})
    ctl("POST", "/v1/op/edge/start", {})
    require(until(lambda: status()["edge"]["connected"] and len(tw.sub_posts) >= 2), "edge restart failed")
    tw.call(tw.deliver_chat, "123456", "123456", "!do scout north", "v2-scout")
    time.sleep(.3)
    check("dedupe survives restart; old narration not resent", world() == before_restart
          and len(tw.chat_sent) == sent_before_restart and len(records("applied", message_id="v2-scout")) == 1)
    send(tw, "123456", "!status", "v2-status-after-restart")
    require(until(lambda: any("Day " in m["message"] for m in tw.chat_sent[sent_before_restart:]), 8),
            "status after restart not sent")
    check("!status after restart describes persisted world", f"Day {before_restart['day']}" in tw.chat_sent[-1]["message"])
    for n in (1, 2):
        send(tw, "123456", "!do build palisade", f"v2-build-{n}")
        require(until(lambda: records("applied", message_id=f"v2-build-{n}"), 10), f"build {n} not applied")
    no_wood = world().copy()
    check("two affordable palisades exhaust wood by audited rules", no_wood["wood"] == 0 and
          no_wood["village_defense"] == before_restart["village_defense"] + 4)
    model_before_unaffordable = len(tw.lm_requests)
    send(tw, "123456", "!do build palisade", "v2-unaffordable")
    require(until(lambda: records("command_rejected", message_id="v2-unaffordable"), 8),
            "unaffordable command not rejected")
    check("unaffordable legal command does not call model or mutate world",
          world() == no_wood and len(tw.lm_requests) == model_before_unaffordable
          and not records("applied", message_id="v2-unaffordable"))
    check("unaffordable command gives Jay concrete feedback",
          until(lambda: any("Order refused: palisade needs 5 wood and 2 stone" in m["message"]
                            for m in tw.chat_sent), 8))
    require(until(lambda: records("model", op="narration_accepted", message_id="v2-build-2"), 5),
            "prior narration still in flight")
    # Pause a real in-flight HTTP model response, then sever EventSub before it returns.
    model_before_disconnect, before_disconnect = len(tw.lm_requests), world().copy()
    tw.lm_delay_s = 2.0
    send(tw, "123456", "!do defend", "v2-disconnect-race")
    require(until(lambda: len(tw.lm_requests) > model_before_disconnect, 5), "paused model call not started")
    code, _, stopped = ctl("POST", "/v1/op/edge/stop", {})
    require(check("EventSub disconnected while model call was in flight", code == 200 and
                  until(lambda: not status()["edge"]["connected"], 5), stopped), "edge stop failed")
    time.sleep(2.2)
    check("lost EventSub prevents in-flight model result from committing",
          world() == before_disconnect and not records("applied", message_id="v2-disconnect-race")
          and status()["game"]["pending_count"] == 1)
    tw.lm_delay_s = 0.0
    ctl("POST", "/v1/op/edge/start", {})
    require(until(lambda: records("applied", message_id="v2-disconnect-race"), 12),
            "pending command did not resume after reconnect")
    check("reconnected pending intent commits exactly once",
          world()["version"] == before_disconnect["version"] + 1
          and len(records("applied", message_id="v2-disconnect-race")) == 1)


if __name__ == "__main__":
    sys.exit(main())
