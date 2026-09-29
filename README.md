# EXP0: user + Gemma 4 vs bigrigjay + Twitch chat

Can a small local Gemma model run a coherent RTS civilization, cooperate with one human ally, reason under
fog of war, and fight a streamer-led civilization whose social intelligence comes from Twitch?
The full map is [`CONTEXT_PASS_V1.md`](CONTEXT_PASS_V1.md); the rules for the Twitch machinery are
[`FOUNDATION.md`](FOUNDATION.md); what is proven so far is in [`GATES.md`](GATES.md).

**Current state: the wiring (gates G0–G7).** Gemma, the world engine and the game itself are not built yet.
Wiring first, then war.

## The two links

| link | side | what it does now |
|---|---|---|
| **ally.html** — https://raw.githack.com/NFDFLDTHRY/EXP0/main/ally.html | you + Gemma (the enemy civilization, from Jay's point of view) | Twitch setup wizard to **TWITCH READY**, streamer-permission record, village invite, LM Studio check, E-STOP, evidence tail. Talks only to your controller on 127.0.0.1 |
| **village.html** — https://raw.githack.com/NFDFLDTHRY/EXP0/main/village.html | bigrigjay | signs in with Twitch, joins your game session, sends sequenced commands to your controller as whispers and waits for ACKs |

Open ally.html through the link that `./exp0 start` prints: its `#p=…&k=…` part carries the controller's
ephemeral key and never leaves your browser.

## Start (Debian 13 x86-64)

```sh
git clone https://github.com/NFDFLDTHRY/EXP0 && cd EXP0
./setup.sh            # the one supported entrypoint; checks the machine, writes var/, generates ./exp0
./exp0 start          # controller on 127.0.0.1:8787, prints your ally.html link
./exp0 doctor         # Twitch really answering, LM Studio, nothing listening on the network
```

Then in ally.html, top to bottom: register the Twitch app (the page shows the two exact redirect URLs,
the name, Category *Chat Bot*, Client Type *Public*) → Client ID → Authorize → confirm the account →
resolve bigrigjay → Test EventSub → Test chat read → Test chat send → **TWITCH READY**. Then *New game
session* and send the invite link to the streamer.

`./exp0 start | stop | restart | status | logs | doctor`. Python 3.11+ standard library only; nothing to install.
Termux is optional and not built yet: `setup.sh` says so and stops. Debian alone runs everything.

If you registered a Twitch app for the earlier V0 page, reuse it: add the two V1 redirect URLs to the same app.
V0 (browser-only machine) is frozen at commit `0899498`:
https://rawcdn.githack.com/NFDFLDTHRY/EXP0/0899498482f5311a4cc2788f4b223802798c83fd/setup.html

## Files

```
setup.sh              the one supported entrypoint (generates ./exp0)
controller/exp0d.py   the controller: loopback API, Twitch edge (EventSub WebSocket), action gate,
                      whisper command link, append-only history, LM Studio probe, lifecycle, doctor
ally.html             GitHack surface 1: operator + (later) war council
village.html          GitHack surface 2: bigrigjay's side
GATES.md              gate ledger: proven / simulated / pending / not built
CONTEXT_PASS_V1.md    the architecture map (V1)
FOUNDATION.md         authority, evidence and failure rules for the Twitch machinery
tests/                proof harness (dev only): fake Twitch + fake LM Studio + end-to-end run, and its evidence
var/                  created by setup.sh, never committed: config, state, history.ndjson, session key
```

## Security boundary

- Controller binds **127.0.0.1 only**; every call needs the ephemeral session key; foreign Origins and
  rebinding Host headers are refused. `./exp0 doctor` checks that nothing answers on the LAN.
- The Twitch user token lives **only in the controller's memory**; it is never written to disk, history or
  browser storage. Re-authorize once after each controller start.
- Never committed: tokens, client secrets, OpenAI keys, LM Studio credentials, the session key. The public
  Client ID is fine (Twitch treats it as public).
- LM Studio must stay localhost-only; the controller refuses a non-loopback LM Studio URL.
- Authority: the operator on 127.0.0.1; the opponent only by **numeric Twitch user id**. Chat is input,
  never authority. Posting in bigrigjay's chat is locked until his permission is recorded.

## Evidence

```sh
pip install aiohttp playwright && python3 tests/e2e_v1.py
```

Runs the real setup, lifecycle, controller and both pages against a fake Twitch on the real hostnames and
writes `tests/.run/`. Last run: [`tests/EVIDENCE-e2e.txt`](tests/EVIDENCE-e2e.txt), 81 checks, 0 failed.
Simulated Twitch proves EXP0's behavior, not Twitch's; the real gates are marked PENDING-REAL in GATES.md.
