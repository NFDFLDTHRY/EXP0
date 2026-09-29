# EXP0 — Twitch Interaction Machine

The smallest auditable machine that lets a bot observe and interact with a Twitch
channel under explicit permission from the streamer. Read `FOUNDATION.md` first;
everything here exists to serve it.

Two single-file HTML apps, distributed as githack links (no server, no build):

| link | role |
|---|---|
| **entry** — https://raw.githack.com/NFDFLDTHRY/EXP0/main/setup.html | Walks through the Twitch developer-account integration, obtains the token (implicit grant), resolves the target channel, records streamer permission, runs pre-flight. |
| **machine** — https://raw.githack.com/NFDFLDTHRY/EXP0/main/machine.html | The fixed control plane: EventSub input → normalizer → session controller → behavior worker → action gate → Twitch sender, with append-only history and the first-admission-tests checklist. |

Both pages are served from the same origin (`raw.githack.com`) and share that
origin's `localStorage` (keys `tim.*`). The token never enters history.

Target channel for this experiment: `bigrigjay` (https://m.twitch.tv/bigrigjay).

## Files

```
FOUNDATION.md       the design; read first
setup.html          entry link (Twitch dev-account integration + OAuth + pre-flight)
machine.html        the machine (control plane, gate, sender, history, self-tests)
behaviors/observe.js   v0 behavior: proposes nothing (input-side proof)
behaviors/ping.js      smallest full-path behavior: "!ping" -> reply "pong"
BEHAVIOR_SLOT.md    template + the source contract for new behaviors
```

## Bring-up

1. Open the **entry** link on the phone (Chrome). Step 0 shows the exact redirect URL.
2. Twitch: enable 2FA on the account that will own the app, then register the app
   at https://dev.twitch.tv/console/apps/create — Name (unique), OAuth Redirect URL
   = the URL from step 0 (press *Add*), Category *Chat Bot*, Client Type **Public**.
   Copy the Client ID. (Client type cannot be changed later.)
3. Entry step 3: paste the Client ID. Step 4: *Authorize* — log in as the account
   that should speak in chat (that account becomes the bot identity). Scopes:
   `user:read:chat`, `user:write:chat`.
4. Step 5: resolve `bigrigjay` → broadcaster id. Step 6: record how/when the
   streamer permitted the bot (the machine refuses to enable `send` without it).
5. Step 7: pre-flight → *Open the machine*.
6. Machine: **run offline self-test** (proves t4, t6, t9, t10, t11, t12 against the
   real gate/dedupe/worker code, no Twitch). Load `behaviors/observe.js`, ACTIVATE,
   START. Watch chat events arrive in history (t1, t2).
7. Load `behaviors/ping.js`, ACTIVATE, enable `send` + `reply`, have someone type
   `!ping` in chat (not the bot account). History should show
   event → interpretation → proposal → ADMIT → action → result(is_sent=true) →
   CONFIRMED in chat (t3, t5, t7, t8). Type `!ping` again within the repeat window
   to watch a rejection (t6 live).
8. Reload the page mid-run: it comes back STOPPED, nothing is resent (t9), and
   executed keys are preserved.

Every step writes to the append-only history; export it as `.ndjson` from the
machine page. "Why the hell did the bot say that?" is answered by following
`proposal_id` / `event_id` through the lines.

## Operator controls (machine page)

- **START / STOP** — whether the bot is running. Every page load starts STOPPED.
- **E-STOP** — persistent; no external actions until explicitly cleared.
- **observe / send / reply** — allowed action classes (`send` and `reply` lock
  without a recorded streamer permission).
- **ACTIVATE** — activates the source in the editor as `name@sha256[0:12]`;
  a changed source is a new version. Nothing activates silently.
- **limits** — min interval between sends, max sends per minute, repeat window.
- **export / archive** — archive downloads the whole log and starts a new one;
  `seq` numbering continues, nothing is edited.

## Twitch surface used

- Implicit grant: `https://id.twitch.tv/oauth2/authorize?response_type=token…`
  ([docs](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/))
- Validate (start, hourly, before reconnect): `GET https://id.twitch.tv/oauth2/validate`
- Channel lookup: `GET https://api.twitch.tv/helix/users?login=…`
- Chat input: EventSub WebSocket `wss://eventsub.wss.twitch.tv/ws`, subscription
  `channel.chat.message` v1, condition `{broadcaster_user_id, user_id}`, user token
  ([docs](https://dev.twitch.tv/docs/eventsub/handling-websocket-events/))
- Chat output: `POST https://api.twitch.tv/helix/chat/messages`
  `{broadcaster_id, sender_id, message, reply_parent_message_id?}` → `{message_id, is_sent, drop_reason}`
  ([docs](https://dev.twitch.tv/docs/api/reference/#send-chat-message))
- Revoke: `POST https://id.twitch.tv/oauth2/revoke`

## Distribution notes

- `raw.githack.com/…/main/…` serves the latest commit on `main` (changes appear
  within minutes; heavy traffic extends cache). For a frozen build use
  `rawcdn.githack.com/NFDFLDTHRY/EXP0/<commit-sha>/machine.html` (cached forever
  per URL). The OAuth redirect URL must be the `setup.html` URL you actually open.
- Everything served from `raw.githack.com` shares one browser origin: any other
  githack page opened in the same browser profile can read `tim.*`, including the
  token. Use a dedicated browser profile for the machine, and revoke the token
  from the entry page when done.
- Keep the machine tab in the foreground on the phone (or split-screen); Android
  Chrome throttles background tabs. The keepalive watchdog reconnects after drops
  and external actions stay refused until the connection is valid again.

## Anti-cathedral

One process (a browser tab). One append-only log (chunked `localStorage`, NDJSON).
No server, no database, no framework. Add machinery only when reality demands it.
