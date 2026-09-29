# EXP0 V2 gate ledger

A passing local harness proves EXP0's behavior against **fake Twitch and a fake LiteRT-LM endpoint**, never a real Twitch delivery or a real Gemma decision. The current [test record](tests/EVIDENCE-v2.txt) reports **68 checks passed, 0 failed** and 186 gapless history records on 2026-09-29 UTC. Run it with:

```sh
python3 -m venv /tmp/exp0-test-venv
/tmp/exp0-test-venv/bin/pip install aiohttp
/tmp/exp0-test-venv/bin/python tests/e2e_v2.py
```

The controller needs only Python 3.11+ standard library; the local model runtime is [Google LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM) in a separate environment. The test harness needs `aiohttp`; no browser was available in this work environment, so page behavior is checked statically and the actual browser flow remains pending.

| gate | status here | observed evidence | remaining real proof |
|---|---|---|---|
| Fresh setup and lifecycle | **PROVEN-HERE** on Ubuntu 24.04; **PENDING-REAL** on Debian 13 | harness clones the working tree, runs `./setup.sh`, re-runs it, starts/restarts/stops `./exp0` | run on the Debian 13 x86-64 laptop |
| Loopback controller security | **SIMULATED** | 127.0.0.1 process, ephemeral key, unauthorized and foreign-Origin refusals, token redaction in `var/` | open printed GitHack ally link in the laptop browser and allow local access |
| One user OAuth; no Jay/viewer auth | **SIMULATED** token validation and **STATIC** page check | only `user:read:chat` and `user:write:chat`; public page contains no auth script/token store; fake token from the user's account | complete ally.html OAuth in a real browser with the user's Twitch account |
| BigRigJay chat read and send | **SIMULATED** | one `channel.chat.message` subscription with broadcaster=Jay numeric ID and user=authorized numeric ID; fake Helix send/echo | receive Jay's real chat event and observe a send from the user's account in Jay's chat |
| Commander, council and language | **SIMULATED** | numeric ID routing, `!help`, `!status`, `!do`, bounded `!suggest`, private advice, display-name impostor and duplicate IDs | Jay and a viewer exercise these in real chat |
| Local Gemma game-master loop | **SIMULATED** | `/v1/models` ID discovery, successful and broken fake completion probes, `max_completion_tokens`, JSON object response format, bounded legal projection, strict JSON validation, one repair, post-commit narration; fake model responses | import actual Gemma 4 E4B into LiteRT-LM at 127.0.0.1:1234, test a short completion, and observe a turn on the Debian laptop |
| Canonical world and legality | **PROVEN-HERE** pure engine plus **SIMULATED** integration | resource costs, food upkeep, enemy supplies, fog projection, illegal commander/model moves, malformed JSON, versioned state | observe the same rules during real play |
| Commit before narration; reconnect and restart | **SIMULATED** | state and append-only evidence precede fake Twitch action; duplicate chat cannot repeat a turn; delayed Gemma call during disconnect leaves the pending turn unchanged until reconnect; world and council persist; token drops at restart | restart the Debian controller, reauthorize/reconnect, and request `!status` |
| E-STOP | **SIMULATED** | incoming commands logged, model and mutation halted, fake Twitch output blocked | press it during real play and verify silence |
| Termux/core split | **NOT BUILT** | setup honestly refuses unsupported split roles | not needed for tonight's Debian all-in-one game |

## Shortest real proof tonight

1. On the Debian machine, follow [README.md](README.md) to install LiteRT-LM, import Gemma 4 E4B and run `litert-lm serve --host 127.0.0.1 --port 1234`. Run `./setup.sh`, `./exp0 start`, and `./exp0 doctor`. Use the printed commit-pinned GitHack links; the mutable `/main/` cache may lag.
2. Open the printed ally.html link **on that machine**. Register its exact redirect URL in the public Twitch app if needed. Save the Client ID, authorize only your Twitch account, confirm the numeric ID, resolve `bigrigjay`, connect EventSub, and use the local model probe to confirm `gemma4-e4b` can produce a completion.
3. In BigRigJay's chat, have Jay type `!help`; verify the response is from your account. Use ally.html to send a TEST to BigRigJay's chat and wait for its EventSub echo. Have Jay type `!do scout north`; verify one intent, one Gemma proposal, one committed world version, and a later narration in `var/history.ndjson`.
4. Have a viewer type `!suggest fortify west`. On the next Jay `!do`, verify it appears in the bounded model context and does not itself advance the turn. Run `./exp0 restart`, open its **new** ally link, reauthorize your account, reconnect EventSub, and have Jay type `!status`. The same world must appear.

A Twitch chat subscription can fail for channel/account restrictions, and EventSub does not replay messages missed during a disconnected interval. The harness cannot prove those account-specific conditions or the speed and memory of E4B on this 8 GB Debian laptop. A committed narration send that Twitch rejects is logged with `is_sent`/`drop_reason`; old narration is never resent automatically after restart.

Google's [Gemma 4 LiteRT-LM model list](https://developers.google.com/edge/litert-lm/models/gemma-4) currently supports E2B and E4B. The 26B A4B model is **not supported by this runtime route yet** and is not part of tonight's gate.
