# EXP0 gate ledger

REPOSITORY STATE + OBSERVED BEHAVIOR = PROOF. Agent prose is not proof. This file records, per gate,
what was observed, where, and what is still unproven. Update it when a gate moves.

| mark | meaning |
|---|---|
| **PROVEN-HERE** | observed on the builder's machine against the real component |
| **SIMULATED** | observed against `tests/fake_twitch.py` (fake Twitch, fake LM Studio): proves EXP0's code paths, **not** Twitch |
| **PENDING-REAL** | needs your accounts or your Debian machine; the steps are listed |
| **NOT BUILT** | deliberately not started (gate order: do not skip gates) |

Evidence: [`tests/EVIDENCE-e2e.txt`](tests/EVIDENCE-e2e.txt), 81 checks, 0 failed, 2026-09-29.
Re-run anywhere: `pip install aiohttp playwright && python3 tests/e2e_v1.py`.
The harness runs the real `./setup.sh`, the real `./exp0` lifecycle, the real controller process on
127.0.0.1, and both pages in Chromium under the real `https://raw.githack.com` origin (the fake host answers
for raw.githack.com, id.twitch.tv, api.twitch.tv and eventsub.wss.twitch.tv; the page code is unmodified).

## Gates

| gate | status | evidence | to prove for real |
|---|---|---|---|
| G0 repo foundation | **PROVEN-HERE** | this repo: one `setup.sh`, one controller, two pages, `CONTEXT_PASS_V1.md`, `FOUNDATION.md` | nothing |
| G1 `./setup.sh` works | **PROVEN-HERE** on Ubuntu 24.04 (Debian family). **PENDING-REAL** on Debian 13 | `G1` lines | `./setup.sh` on the Debian 13 box: expect `PASS platform: Debian 13 x86_64 (reference platform)` |
| G2 ally.html from GitHack talks securely to localhost | **SIMULATED** origin (real Chromium, real controller) | `G2` lines: key only in the fragment → tab sessionStorage, wrong key 401, foreign Origin 403, rebinding Host 403, CORS + Private-Network preflight, nothing listening on the LAN | open the `./exp0 start` link in Chrome on the Debian box. Chrome 142+ asks to let raw.githack.com reach apps on this device: **Allow** |
| G3 Twitch OAuth + numeric id for bigrigjay | **SIMULATED** | `G3` lines: exact implicit-grant request, token never left in URL or storage, identity bound, `m.twitch.tv/bigrigjay` → numeric id | ally.html steps 1–5 with your real app and account |
| G4 receive one real Twitch event | **SIMULATED** | `G4` lines: 3 subscriptions with exact conditions, one opponent-chat event normalized | ally.html steps 6–7: type in your own chat |
| G5 send one deliberate TEST message | **SIMULATED** | `G5` lines: own channel only; opponent chat refused without a permission record; evidence chain proposal → admission → action → result → echo | ally.html step 8 → **TWITCH READY** |
| G6 village.html command reaches controller | **SIMULATED** | `G6` + `F` lines | needs two accounts **with verified phone numbers** (Twitch requires it to send whispers). Rehearse with a second account of yours: resolve it as the opponent in step 5, New game session, open the invite in another browser profile signed in as that account. Then resolve bigrigjay again (this voids the rehearsal session, by design) and send him the new invite |
| G7 LM Studio reachable | **SIMULATED** | `G7` lines, `./exp0 doctor` | install LM Studio on the Debian box, load a Gemma 4 model, start the server (`lms server start`), keep "Serve on Local Network" off, run `./exp0 doctor` |
| G8 Gemma returns one valid structured intent | **NOT BUILT** | | known risk: an 8 GB CPU-only box runs only small Gemma variants; LM Studio's own docs warn structured output is unreliable below ~7B. Grammar-constrained decoding keeps the JSON parseable, so G9 has to catch everything that is legal-looking but wrong |
| G9 invalid Gemma output cannot alter state | **NOT BUILT** | | |
| G10 minimum deterministic world | **NOT BUILT** | | |
| G11 fog of war proven | **NOT BUILT** | | |
| G12 user advises Gemma without puppeting it | **NOT BUILT** | ally.html WAR COUNCIL zone reserved | |
| G13 Jay + chat operate the opposing civilization | **NOT BUILT** | village.html YOUR CIVILIZATION zone reserved | |
| G14 failure / reconnect / restart tests | **SIMULATED** for the wiring (below) | | re-run the failure list on real Twitch after G6 |
| G15 freeze a known-good GitHack revision | **NOT BUILT** | | pin `rawcdn.githack.com/NFDFLDTHRY/EXP0/<commit>/…`, register those redirect URLs too, set `ally_url`/`village_url` in `var/config.json` |

## Failure tests (CONTEXT_PASS_V1 list)

| failure | status | what was observed |
|---|---|---|
| Termux killed | **NOT BUILT** | the Termux edge role does not exist yet; `setup.sh` refuses it honestly (exit 3) |
| Twitch disconnected | **SIMULATED** | sends refused with `connection_invalid` while down; backoff reconnect; resubscribed |
| Twitch reconnect | **SIMULATED** | `session_reconnect` followed; old socket kept until welcome; subscriptions not recreated; commands kept flowing |
| wrong Twitch account | **SIMULATED** | token for another account refused while a game is bound to the enemy account |
| duplicate event | **SIMULATED** | replayed chat notification dropped |
| duplicate whisper | **SIMULATED** | replayed whisper notification dropped, nothing re-applied |
| stale sequence | **SIMULATED** | cached ACK re-sent with `dup`, not re-applied |
| reordered sequence | **SIMULATED** | `sequence_gap`, `expect` returned, not applied |
| dropped ACK | **SIMULATED** | Twitch "silently dropped" the ACK; village retried the same seq; controller re-ACKed from cache; applied once |
| browser refresh | **SIMULATED** | ally keeps its link (tab sessionStorage); village re-joins and keeps its sequence |
| controller restart | **SIMULATED** | new key; old tab told; config, game and sequence kept; token dropped (memory-only); nothing resent; history seq gapless |
| LM Studio unavailable | **SIMULATED** | reported by ally.html and `./exp0 doctor` as FAIL; nothing else affected |
| malformed / illegal Gemma output, hidden-information references | **NOT BUILT** | G8–G11 |
| prompt injection from Twitch chat | **SIMULATED** (wiring only) | instruction-shaped text in chat and whispers is logged as input and refused; no authority gained. Gemma does not exist yet, so "raw chat never becomes Gemma instructions" is proven only at G8 |
| fake "bigrigjay" display name | **SIMULATED** | whisper from another numeric id displaying "bigrigjay" rejected, no reply, nothing applied |
| E-STOP | **SIMULATED** | incoming commands logged, not applied, not answered; after clearing, the village's retry applied once |

## Real-world constraints found while building (not in the map)

- **Chrome Local Network Access** (Chrome 142, Oct 2025): a public page calling `http://127.0.0.1` needs a one-time Allow. ally.html explains this when the controller is unreachable.
- **Whispers**: the sender needs a verified phone number; the first whisper to someone is limited to 500 characters; 3/s, 100/min, 40 new recipients per day; Twitch may drop a whisper silently and still answer 204. The command link is stop-and-wait with ACKs because of that last rule.
- **Filtering networks**: a proxy can complete TLS to twitch.tv and still block every request. `./exp0 doctor` therefore requires Twitch's own 401 JSON and a real EventSub `session_welcome`, not just a TLS handshake (see the last block of the evidence file: the builder's sandbox is such a network).
- **Twitch token is memory-only** in the controller: after every `./exp0 start`, press Authorize once in ally.html. Twitch remembers the consent, so it is one click.
