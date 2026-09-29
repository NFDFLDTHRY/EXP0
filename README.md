# EXP0 — BigRigJay and chat versus Gemma

EXP0 is a small persistent village war game played in [BigRigJay's Twitch chat](https://www.twitch.tv/bigrigjay). Jay commands the village with `!do`; viewers advise with `!suggest`. A local Gemma model chooses the enemy move. The rule engine resolves the turn and persists the result before EXP0 narrates through **your** Twitch account.

Exactly one Twitch account authorizes EXP0: yours. Jay and viewers use ordinary chat. Their numeric Twitch chatter IDs determine their roles; a display name grants no authority. `./exp0 start` prints both immutable GitHack links: the private ally setup link and the public `village.html` guide. The public page never authenticates anyone.

## Play on Debian 13

1. Clone the project, install [Google LiteRT-LM](https://developers.google.com/edge/litert-lm/cli/installation) in a Python virtual environment, and [import](https://developers.google.com/edge/litert-lm/cli/model_management) the Gemma 4 E4B bundle:

   ```sh
   git clone https://github.com/NFDFLDTHRY/EXP0.git
   cd EXP0
   python3 -m venv .venv
   .venv/bin/python -m pip install 'litert-lm==0.17.1'
   .venv/bin/litert-lm import --from-huggingface-repo=litert-community/gemma-4-E4B-it-litert-lm gemma-4-E4B-it.litertlm gemma4-e4b
   ```

   On Debian, install `python3-venv` if `python3 -m venv` is missing. The model download requires internet access. LiteRT-LM's E4B inference speed and peak memory on this particular 8 GB Debian machine still need a real check. [Google's current Gemma 4 LiteRT-LM list](https://developers.google.com/edge/litert-lm/models/gemma-4) supports E2B and E4B; it lists larger variants as coming later. **The 26B A4B model is not supported by this route yet.**

2. [Serve](https://developers.google.com/edge/litert-lm/cli/openai_server) the imported model on loopback in a separate terminal, then set up EXP0 in the project directory:

   ```sh
   .venv/bin/litert-lm serve --host 127.0.0.1 --port 1234
   ```

   ```sh
   ./setup.sh
   ./exp0 start
   ```

3. Open the **ally.html link printed by `./exp0 start` on that same machine**. It is pinned to the cloned commit so GitHack cannot mix cached branch revisions. Its `#p=…&k=…` fragment carries an ephemeral local controller key. Follow the page's wizard: create a public Twitch app if needed, save its Client ID, authorize **your** account for `user:read:chat` and `user:write:chat`, confirm the account, resolve `bigrigjay`, connect EventSub, and test reading and sending chat. The app's OAuth redirect URL must exactly match the ally URL displayed by the page, without the fragment.
4. Check the local Gemma service in the ally page. Its probe must show the imported E4B model and a successful short completion. The world is seeded when your identity and Jay's numeric ID are resolved. Jay types `!help`, then `!do scout north` in his own Twitch chat. A viewer can type `!suggest fortify west`; advice enters the next bounded council context and has no direct authority. Your private advice box on ally.html also enters Gemma's next context.
5. Use `./exp0 status`, `./exp0 logs`, and `./exp0 doctor` to inspect the system. **E-STOP** on ally.html prevents game mutation and Twitch output.

After `./exp0 restart`, open the new ally link, authorize your account again, and reconnect EventSub. Twitch tokens exist only in controller memory. The world and processed message IDs remain in `var/`; `!status` should show the same world.

If Chrome asks whether raw.githack.com may access apps on this device, allow local network access so ally.html can reach `127.0.0.1`. The public village page needs no local access.

## Chat language

| speaker | command | effect |
|---|---|---|
| Jay, by numeric Twitch ID | `!do scout north` | discover the enemy front if scouts find it |
| Jay | `!do gather food` / `wood` / `stone` | collect one resource |
| Jay | `!do build palisade` | spend wood and stone for defense |
| Jay | `!do recruit defenders` | spend food and assign villagers to defense |
| Jay | `!do defend` or `!do defend west` | protect the village this turn |
| Jay | `!do attack east` | attack that front |
| Jay | `!do negotiate` | offer food for a one-turn truce |
| anyone | `!help`, `!status` | read instructions or the persisted world |
| viewers | `!suggest gather food` | advise Gemma; does not execute a move |

Each accepted commander move advances a day and consumes food. Gemma proposes an enemy action using only a legal projection; the rule engine validates and resolves it. Bad JSON or an illegal move cannot change canonical state. The explicit command language works without natural-language interpretation.

## Boundaries and files

The controller binds to `127.0.0.1` only. ally.html calls it with a tab-scoped session key; `village.html` is static and public. The controller alone calls Twitch and the local LiteRT-LM service. A Twitch access token is never stored in browser storage, `var/`, or history. `var/state.json` holds canonical state and dedupe IDs, and `var/history.ndjson` is append-only evidence. `var/` is gitignored. No database, cloud inference service, second login, whisper scope, or Termux role is required. `setup.sh` reports the unfinished split roles honestly.

| path | role |
|---|---|
| `controller/exp0d.py` | loopback API, Twitch EventSub/send, Gemma calls, persistence and lifecycle |
| `controller/game.py` | deterministic grammar, legal model view, proposal validator and world rules |
| `ally.html` | private operator setup and Gemma war council |
| `village.html` | public how-to-play page |
| `tests/` | simulated Twitch and local Gemma service integration harness |
| `GATES.md` | observed proof and pending real-world checks |

The controller uses Python 3.11+ standard library only; LiteRT-LM runs in its own environment. This Google Gemma route does not invoke LM Studio, Ollama, or llama.cpp, and EXP0 selects only Gemma 4 model IDs. LiteRT-LM also offers optional Llama-family model support elsewhere in its codebase; a complete binary provenance audit has not been performed. `./exp0 start | stop | restart | status | logs | doctor` is generated by `./setup.sh`. The historical V1 design remains in git history; [GATES.md](GATES.md) is the current evidence ledger.

## Verify

Run the harness as described in [GATES.md](GATES.md). It exercises the real controller against fake Twitch and fake local model responses, then labels live Twitch, browser OAuth, Debian 13 and actual Gemma checks **PENDING-REAL**. A simulated pass is never a claim that Jay's real chat or your laptop was tested here.
