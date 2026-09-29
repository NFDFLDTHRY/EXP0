```text
+====================================================================================================================+
|                                         EXP0 — CONTEXT PASS V1                                                    |
|                               USER + GEMMA 4  vs  BIGRIGJAY + TWITCH CHAT                                        |
|                                                                                                                    |
| V0 = original architecture map                                                                                    |
| V1 = this single-system update                                                                                    |
|                                                                                                                    |
| REPO:    https://github.com/NFDFLDTHRY/EXP0                                                                       |
| TWITCH:  bigrigjay                                                                                                |
| TARGET:  https://m.twitch.tv/bigrigjay                                                                            |
|                                                                                                                    |
| CORE QUESTION                                                                                                      |
|                                                                                                                    |
|   Can a small local Gemma model operate a coherent autonomous RTS civilization, cooperate with one human ally,    |
|   reason under fog of war, and fight a streamer-led civilization whose social intelligence comes from Twitch?     |
|                                                                                                                    |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                             HUMAN / AGENT FACTORY                                                  |
|                                                                                                                    |
|                                                   USER                                                             |
|                                    product + architecture authority                                                |
|                                                     |                                                              |
|                     +-------------------------------+-------------------------------+                              |
|                     |                               |                               |                              |
|                     v                               v                               v                              |
|               CHATGPT / SOL                    CLAUDE CHAT                        FABLE                            |
|               context integrator                  OPUS                           foundation                         |
|                     |                           advisor only                        builder                           |
|                     |                               |                               |                              |
|                     |                               |                               v                              |
|                     |                               |                    initial EXP0 repo/setup                    |
|                     |                               |                               |                              |
|                     |                               |                               v                              |
|                     |                               +----------------------> IMPLEMENTATION EVIDENCE               |
|                     |                                                               |                              |
|                     |                                                               v                              |
|                     +---------------------------------------------------------> CLAUDE CODE                        |
|                                                                                actual repo builder                  |
|                                                                                tests / fixes / proof                |
|                                                                                                                    |
|   SOL: preserve intent, reconcile findings, update map                                                             |
|   OPUS: attack assumptions, inspect architecture, find failure modes                                                |
|   FABLE: forge initial repo and setup surfaces                                                                     |
|   CLAUDE CODE: modify NFDFLDTHRY/EXP0 and prove physical links                                                     |
|                                                                                                                    |
|   NO AGENT PROSE COUNTS AS PROOF.                                                                                  |
|   REPOSITORY STATE + OBSERVED BEHAVIOR = PROOF.                                                                    |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                               PRODUCT INSTALLATION                                                 |
|                                                                                                                    |
|                                   ONE SUPPORTED ENTRYPOINT                                                         |
|                                                                                                                    |
|                                             ./setup.sh                                                             |
|                                                  |                                                                 |
|                           +----------------------+----------------------+                                          |
|                           |                                             |                                          |
|                           v                                             v                                          |
|                    DEBIAN 13 x86-64                                ANDROID / TERMUX                                 |
|                           |                                             |                                          |
|                    role selection                                 role selection                                   |
|                           |                                             |                                          |
|             +-------------+-------------+                               |                                          |
|             |                           |                               |                                          |
|             v                           v                               v                                          |
|        ALL-IN-ONE                     CORE                            EDGE                                          |
|        Debian runs all         Debian runs canonical         Twitch/network side                                  |
|             |                  state + Gemma                   only                                                |
|             |                           |                               |                                          |
|             +-------------+-------------+-------------------------------+                                          |
|                           |                                                                                        |
|                           v                                                                                        |
|                generated lifecycle interface                                                                      |
|                                                                                                                    |
|                  ./exp0 start                                                                                      |
|                  ./exp0 stop                                                                                       |
|                  ./exp0 restart                                                                                    |
|                  ./exp0 status                                                                                     |
|                  ./exp0 logs                                                                                       |
|                  ./exp0 doctor                                                                                     |
|                                                                                                                    |
|   DEBIAN ALONE MUST RUN THE WHOLE SYSTEM.                                                                          |
|   TERMUX MAY IMPROVE / OFFLOAD THE SYSTEM.                                                                         |
|   TERMUX MUST NEVER BE REQUIRED FOR EXP0 TO EXIST.                                                                 |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                           PHYSICAL DEPLOYMENT                                                      |
|                                                                                                                    |
|                                                                                                                    |
|   OPTIONAL PHONE / TERMUX EDGE                                      DEBIAN 13 CORE                                 |
|   ============================                                      ==============                                 |
|                                                                                                                    |
|   +-----------------------------+                    +---------------------------------------------------------+   |
|   | Twitch EventSub             |                    | CONTROLLER                                              |   |
|   | whispers                    |                    |                                                         |   |
|   | chat ingest                 |                    | command validation                                      |   |
|   | connection maintenance      |                    | authority checks                                        |   |
|   | ACK / retry                 |<------------------>| sequence/idempotency                                    |   |
|   | event normalization         |    paired link     | session management                                      |   |
|   | short event spool           |                    |                                                         |   |
|   | watchdog                    |                    +----------------------+----------------------------------+   |
|   +-----------------------------+                                           |                                      |
|                                                                              |                                      |
|                                                                              v                                      |
|                                                              +------------------------------+                       |
|                                                              |      CANONICAL WORLD ENGINE   |                       |
|                                                              |                              |                       |
|                                                              | resources                    |                       |
|                                                              | map                          |                       |
|                                                              | units                        |                       |
|                                                              | buildings                    |                       |
|                                                              | production                   |                       |
|                                                              | movement                     |                       |
|                                                              | combat                       |                       |
|                                                              | fog of war                   |                       |
|                                                              | detection                    |                       |
|                                                              | technology                   |                       |
|                                                              | victory conditions           |                       |
|                                                              | authoritative clock          |                       |
|                                                              +--------------+---------------+                       |
|                                                                             |                                       |
|                                  +------------------------------------------+----------------------------------+    |
|                                  |                                                                             |    |
|                                  v                                                                             v    |
|                     +---------------------------+                                                +------------------+ |
|                     | PERSISTENCE               |                                                | GEMMA PROJECTION | |
|                     |                           |                                                |                  | |
|                     | canonical snapshots       |                                                | ONLY information | |
|                     | append-only evidence      |                                                | Gemma legally    | |
|                     | event sequence            |                                                | knows            | |
|                     | crash recovery            |                                                +--------+---------+ |
|                     +---------------------------+                                                         |           |
|                                                                                                           v           |
|                                                                                                  +------------------+ |
|                                                                                                  | LM STUDIO        | |
|                                                                                                  | 127.0.0.1 only   | |
|                                                                                                  +--------+---------+ |
|                                                                                                           |           |
|                                                                                                           v           |
|                                                                                                  +------------------+ |
|                                                                                                  | GEMMA 4          | |
|                                                                                                  | enemy commander  | |
|                                                                                                  +--------+---------+ |
|                                                                                                           |           |
|                                                                                                     structured intent |
|                                                                                                           |           |
|                                                                                                           v           |
|                                                                                                  +------------------+ |
|                                                                                                  | ACTION VALIDATOR | |
|                                                                                                  +--------+---------+ |
|                                                                                                           |           |
|                                                                                                           +---------> |
|                                                                                                                   WORLD|
|                                                                                                                  ENGINE|
|                                                                                                                    |
|   IF TERMUX DIES:                                                                                                  |
|                                                                                                                    |
|       network edge may disappear                                                                                   |
|       canonical state survives                                                                                     |
|       Gemma survives                                                                                               |
|       game survives                                                                                                |
|       save survives                                                                                                |
|       Termux reconnects later                                                                                      |
|                                                                                                                    |
|   LM STUDIO / GEMMA ROLE CURRENTLY BELONGS ON DEBIAN.                                                              |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                                TWO GITHACK SURFACES                                                |
|                                                                                                                    |
|                                                                                                                    |
|                   USER / GEMMA SIDE                                         BIGRIGJAY SIDE                           |
|                   =================                                         ==============                           |
|                                                                                                                    |
|        GitHack: ally.html                                         GitHack: village.html                            |
|                 |                                                          |                                      |
|                 v                                                          v                                      |
|    +----------------------------+                              +------------------------------+                     |
|    | GEMMA WAR COUNCIL          |                              | PLAYER RTS INTERFACE         |                     |
|    |                            |                              |                              |                     |
|    | advise Gemma               |                              | resources                    |                     |
|    | share legal intelligence   |                              | known map                    |                     |
|    | coordinate strategy        |                              | build                        |                     |
|    | support actions            |                              | recruit                      |                     |
|    | respond to Gemma requests  |                              | scout                        |                     |
|    +-------------+--------------+                              | research                     |                     |
|                  |                                             | military orders              |                     |
|                  |                                             | diplomacy                    |                     |
|                  |                                             | chat council                 |                     |
|                  |                                             +---------------+--------------+                     |
|                  |                                                             |                                    |
|                  v                                                             v                                    |
|    +----------------------------+                                       Twitch OAuth                                |
|    | OPERATOR CONTROLS          |                                             |                                      |
|    |                            |                                             v                                      |
|    | Twitch setup wizard        |                                          TWITCH                                    |
|    | Twitch status              |                                             |                                      |
|    | LM Studio status           |                               private control / state transport                     |
|    | start / pause / save       |                                             |                                      |
|    | diagnostics                |                                             v                                      |
|    | emergency stop             |                                 TERMUX EDGE or DEBIAN EDGE                         |
|    +-------------+--------------+                                             |                                      |
|                  |                                                            v                                      |
|                  | loopback only                                      CONTROLLER                                    |
|                  | 127.0.0.1                                                |                                      |
|                  +----------------------------------------------------------+                                      |
|                                                                                                                    |
|   ally.html IS BOTH:                                                                                                |
|                                                                                                                    |
|       IN-GAME ALLY SURFACE                                                                                         |
|                 +                                                                                                  |
|       LOCAL OPERATOR SURFACE                                                                                       |
|                                                                                                                    |
|   THESE AUTHORITIES MUST NEVER BE CONFUSED.                                                                        |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                           TWITCH SETUP THROUGH ally.html                                            |
|                                                                                                                    |
|                                      USER OPENS ally.html                                                          |
|                                               |                                                                    |
|                                               v                                                                    |
|                                   +---------------------------+                                                    |
|                                   | TWITCH SETUP              |                                                    |
|                                   |                           |                                                    |
|                                   | show exact redirect URI   |                                                    |
|                                   | show required scopes      |                                                    |
|                                   | accept public Client ID   |                                                    |
|                                   | launch Twitch OAuth       |                                                    |
|                                   | verify account identity   |                                                    |
|                                   | resolve bigrigjay         |                                                    |
|                                   | resolve numeric user ID   |                                                    |
|                                   | test EventSub             |                                                    |
|                                   | test chat read            |                                                    |
|                                   | test chat send            |                                                    |
|                                   +-------------+-------------+                                                    |
|                                                 |                                                                  |
|                                                 v                                                                  |
|                                            TWITCH READY                                                             |
|                                                                                                                    |
|   USER SHOULD NOT HUNT SOURCE CODE FOR:                                                                            |
|                                                                                                                    |
|       redirect URI                                                                                                 |
|       scopes                                                                                                       |
|       channel target                                                                                               |
|       Client ID location                                                                                           |
|       setup order                                                                                                  |
|       service startup order                                                                                        |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                                GAME AUTHORITY                                                       |
|                                                                                                                    |
|                                                                                                                    |
|                                          CANONICAL WORLD ENGINE                                                     |
|                                                   |                                                                |
|                              +--------------------+--------------------+                                           |
|                              |                                         |                                           |
|                              v                                         v                                           |
|                     TEAM GEMMA VIEW                           TEAM JAY VIEW                                         |
|                              |                                         |                                           |
|                   +----------+----------+                     +--------+---------+                                  |
|                   |                     |                     |                  |                                  |
|                   v                     v                     v                  v                                  |
|                GEMMA 4               USER                BIGRIGJAY          TWITCH CHAT                             |
|           autonomous commander       ally                commander          council/population                     |
|                                                                                                                    |
|                                                                                                                    |
|   GEMMA KNOWS ONLY:                                                                                                 |
|                                                                                                                    |
|       own civilization                                                                                              |
|       own resources                                                                                                 |
|       legally discovered map                                                                                        |
|       observed enemy information                                                                                    |
|       user-shared legal intelligence                                                                                |
|       current legal action vocabulary                                                                               |
|                                                                                                                    |
|   BIGRIGJAY KNOWS ONLY:                                                                                             |
|                                                                                                                    |
|       his civilization                                                                                              |
|       his resources                                                                                                 |
|       legally discovered map                                                                                        |
|       observable enemy actions                                                                                      |
|                                                                                                                    |
|   WORLD ENGINE KNOWS EVERYTHING.                                                                                    |
|   PLAYERS DO NOT.                                                                                                   |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                               PRIME GAME LAW                                                        |
|                                                                                                                    |
|                                         NOBODY NARRATES REALITY                                                     |
|                                              INTO EXISTENCE                                                         |
|                                                                                                                    |
|                                                                                                                    |
|                          INTENT                                                                                    |
|                            |                                                                                       |
|                            v                                                                                       |
|                       VALIDATION                                                                                   |
|                            |                                                                                       |
|                            v                                                                                       |
|                     WORLD RESOLUTION                                                                               |
|                            |                                                                                       |
|                            v                                                                                       |
|                 CANONICAL STATE MUTATION                                                                           |
|                            |                                                                                       |
|                            v                                                                                       |
|                      OBSERVATION                                                                                   |
|                            |                                                                                       |
|                            v                                                                                       |
|                       NARRATION                                                                                    |
|                                                                                                                    |
|   GEMMA CANNOT DECLARE SUCCESS.                                                                                    |
|   BIGRIGJAY CANNOT DECLARE SUCCESS.                                                                                |
|   USER CANNOT DECLARE SUCCESS.                                                                                     |
|   TWITCH CHAT CANNOT DECLARE SUCCESS.                                                                              |
|   UI CANNOT DECLARE SUCCESS.                                                                                       |
|                                                                                                                    |
|   ONLY THE WORLD ENGINE MUTATES CANONICAL REALITY.                                                                 |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                             GEMMA COMMANDER CONTRACT                                                |
|                                                                                                                    |
|                              LEGAL GEMMA WORLD VIEW                                                                |
|                                         |                                                                          |
|                                         v                                                                          |
|                               +------------------+                                                                 |
|                               |     GEMMA 4      |                                                                 |
|                               | enemy commander  |                                                                 |
|                               +---------+--------+                                                                 |
|                                         |                                                                          |
|                              structured intent only                                                                |
|                                         |                                                                          |
|                                         v                                                                          |
|                               +------------------+                                                                 |
|                               | parse            |                                                                 |
|                               | schema validate  |                                                                 |
|                               | legality check   |                                                                 |
|                               +---------+--------+                                                                 |
|                                         |                                                                          |
|                                         v                                                                          |
|                                   WORLD ENGINE                                                                      |
|                                                                                                                    |
|   GEMMA IS:                                                                                                        |
|       autonomous enemy commander                                                                                   |
|                                                                                                                    |
|   GEMMA IS NOT:                                                                                                    |
|       referee                                                                                                      |
|       database                                                                                                     |
|       canonical state                                                                                              |
|       Twitch administrator                                                                                         |
|       transport                                                                                                    |
|       world engine                                                                                                 |
|                                                                                                                    |
|   RAW TWITCH CHAT MUST NEVER BECOME GEMMA SYSTEM INSTRUCTIONS.                                                     |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                               PUBLIC TWITCH VOICE                                                   |
|                                                                                                                    |
|                                            GEMMA PUBLIC MESSAGE                                                     |
|                                                     |                                                              |
|                                                     v                                                              |
|                                             ACTION VALIDATOR                                                       |
|                                                     |                                                              |
|                                                     v                                                              |
|                                        USER'S TWITCH ACCOUNT                                                       |
|                                                     |                                                              |
|                                                     v                                                              |
|                                          BIGRIGJAY'S TWITCH CHAT                                                   |
|                                                                                                                    |
|   FROM JAY'S PERSPECTIVE:                                                                                          |
|                                                                                                                    |
|       YOUR ACCOUNT = THE ENEMY CIVILIZATION'S VOICE                                                               |
|                                                                                                                    |
|   GEMMA MAY:                                                                                                       |
|       negotiate                                                                                                    |
|       threaten                                                                                                     |
|       bluff                                                                                                        |
|       answer diplomacy                                                                                             |
|       taunt                                                                                                        |
|       communicate battlefield consequences                                                                         |
|                                                                                                                    |
|   GEMMA NEVER RECEIVES TWITCH CREDENTIALS DIRECTLY.                                                               |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                             REMOTE CONTROL TRANSPORT                                                |
|                                                                                                                    |
|                                                                                                                    |
|                BIGRIGJAY'S BROWSER                                                                                |
|                        |                                                                                           |
|                  village.html                                                                                     |
|                        |                                                                                           |
|                   Twitch OAuth                                                                                    |
|                        |                                                                                           |
|                        v                                                                                           |
|                      TWITCH                                                                                        |
|                        |                                                                                           |
|               private command path                                                                                |
|                        |                                                                                           |
|                        v                                                                                           |
|                 EDGE / CONTROLLER                                                                                 |
|                        |                                                                                           |
|                        v                                                                                           |
|                   WORLD ENGINE                                                                                    |
|                                                                                                                    |
|   PREFERRED PRIVATE BUS UNDER TEST:                                                                                |
|                                                                                                                    |
|       Twitch whispers + EventSub                                                                                  |
|                                                                                                                    |
|   MESSAGE LAW:                                                                                                     |
|                                                                                                                    |
|       sender DISPLAY NAME != authority                                                                             |
|       authenticated numeric Twitch USER ID == authority                                                            |
|                                                                                                                    |
|   EACH COMMAND REQUIRES:                                                                                           |
|                                                                                                                    |
|       protocol version                                                                                             |
|       game session ID                                                                                              |
|       monotonic sequence ID                                                                                        |
|       action type                                                                                                  |
|       payload                                                                                                      |
|                                                                                                                    |
|   RETRY LAW:                                                                                                       |
|                                                                                                                    |
|       retry SAME sequence                                                                                          |
|       receiver idempotent                                                                                          |
|       duplicate command != duplicate action                                                                        |
|                                                                                                                    |
|   IF WHISPERS FAIL ADMISSION TESTING:                                                                              |
|                                                                                                                    |
|       temporary explicit Twitch chat commands may serve as fallback                                                |
|                                                                                                                    |
|   PUBLIC BACKEND / WEBHOOK IS NOT AUTOMATIC FALLBACK.                                                              |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                              SECURITY BOUNDARY                                                      |
|                                                                                                                    |
|   PUBLIC REPO + PUBLIC GITHACK MEANS:                                                                              |
|                                                                                                                    |
|       NEVER COMMIT:                                                                                                |
|           Twitch access token                                                                                      |
|           Twitch client secret                                                                                     |
|           OpenAI key                                                                                               |
|           LM Studio private credential                                                                             |
|           ephemeral local session secret                                                                           |
|                                                                                                                    |
|       PUBLIC CLIENT ID:                                                                                            |
|           acceptable                                                                                               |
|                                                                                                                    |
|       OAuth USER TOKENS:                                                                                           |
|           transient / memory where practical                                                                       |
|                                                                                                                    |
|                                                                                                                    |
|   ally.html -> LOCAL CONTROLLER                                                                                    |
|                                                                                                                    |
|       GitHack page                                                                                                 |
|           |                                                                                                        |
|           v                                                                                                        |
|       ephemeral boot/session token                                                                                 |
|           |                                                                                                        |
|           v                                                                                                        |
|       localhost controller                                                                                         |
|       127.0.0.1 only                                                                                               |
|                                                                                                                    |
|   CONTROLLER MUST NOT BIND INTERNET-FACING BY DEFAULT.                                                             |
|                                                                                                                    |
|   LM STUDIO MUST REMAIN LOCALHOST-ONLY.                                                                            |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                                GAMEPLAY MODEL                                                       |
|                                                                                                                    |
|                                                                                                                    |
|                                  TEAM GEMMA                        TEAM JAY                                          |
|                                  ==========                        ========                                          |
|                                                                                                                    |
|                                  GEMMA 4                           BIGRIGJAY                                         |
|                                  autonomous                        commander                                         |
|                                  commander                             +                                             |
|                                      +                             TWITCH CHAT                                       |
|                                   USER                             war council                                       |
|                                  human ally                                                                          |
|                                                                                                                    |
|                                       \                               /                                              |
|                                        \                             /                                               |
|                                         \                           /                                                |
|                                          v                         v                                                 |
|                                          CANONICAL WORLD ENGINE                                                     |
|                                                                                                                    |
|                                                                                                                    |
|   INITIAL RTS SCOPE MUST REMAIN SMALL:                                                                             |
|                                                                                                                    |
|       one settlement per side                                                                                      |
|       small map                                                                                                    |
|       few resources                                                                                                |
|       few buildings                                                                                                |
|       few unit types                                                                                               |
|       fog of war                                                                                                   |
|       scouting                                                                                                     |
|       economy                                                                                                      |
|       combat                                                                                                       |
|       diplomacy                                                                                                    |
|       one clear victory condition                                                                                  |
|                                                                                                                    |
|   DO NOT BUILD AGE OF EMPIRES.                                                                                     |
|   BUILD THE SMALLEST SYSTEM WHERE STRATEGY BECOMES REAL.                                                           |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                              BUILD ADMISSION GATES                                                  |
|                                                                                                                    |
|    G0     repo foundation                                                                                          |
|            |                                                                                                       |
|            v                                                                                                       |
|    G1     ./setup.sh works                                                                                         |
|            |                                                                                                       |
|            v                                                                                                       |
|    G2     ally.html from GitHack talks securely to localhost                                                       |
|            |                                                                                                       |
|            v                                                                                                       |
|    G3     Twitch OAuth + resolve numeric ID for bigrigjay                                                          |
|            |                                                                                                       |
|            v                                                                                                       |
|    G4     receive one real Twitch event                                                                            |
|            |                                                                                                       |
|            v                                                                                                       |
|    G5     send one deliberate TEST message as user's Twitch account                                                |
|            |                                                                                                       |
|            v                                                                                                       |
|    G6     village.html private remote command reaches controller                                                   |
|            |                                                                                                       |
|            v                                                                                                       |
|    G7     LM Studio reachable                                                                                      |
|            |                                                                                                       |
|            v                                                                                                       |
|    G8     Gemma returns one valid structured intent                                                                |
|            |                                                                                                       |
|            v                                                                                                       |
|    G9     invalid Gemma output cannot alter state                                                                  |
|            |                                                                                                       |
|            v                                                                                                       |
|    G10    minimum deterministic world works                                                                        |
|            |                                                                                                       |
|            v                                                                                                       |
|    G11    fog of war proven                                                                                       |
|            |                                                                                                       |
|            v                                                                                                       |
|    G12    user advises Gemma without puppeting it                                                                  |
|            |                                                                                                       |
|            v                                                                                                       |
|    G13    Jay + Twitch chat operate opposing civilization                                                         |
|            |                                                                                                       |
|            v                                                                                                       |
|    G14    failure/reconnect/restart tests                                                                          |
|            |                                                                                                       |
|            v                                                                                                       |
|    G15    freeze known-good GitHack demo revision                                                                  |
|                                                                                                                    |
|   DO NOT SKIP GATES BECAUSE LATER UI LOOKS IMPRESSIVE.                                                             |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                                FAILURE TESTS                                                        |
|                                                                                                                    |
|   MUST TEST:                                                                                                       |
|                                                                                                                    |
|       Termux killed                                                                                                |
|       Twitch disconnected                                                                                          |
|       Twitch reconnect                                                                                             |
|       wrong Twitch account                                                                                         |
|       duplicate event                                                                                              |
|       duplicate whisper                                                                                            |
|       stale sequence                                                                                               |
|       reordered sequence                                                                                           |
|       dropped ACK                                                                                                  |
|       browser refresh                                                                                              |
|       controller restart                                                                                           |
|       LM Studio unavailable                                                                                        |
|       malformed Gemma output                                                                                       |
|       illegal Gemma action                                                                                         |
|       Gemma references hidden information                                                                          |
|       prompt injection from Twitch chat                                                                            |
|       fake "bigrigjay" display name                                                                                |
|                                                                                                                    |
|   FAILURE MUST STOP UNCERTAIN ACTIONS.                                                                             |
|   FAILURE MUST NOT INVENT REALITY.                                                                                 |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                               ANTI-CATHEDRAL LAW                                                    |
|                                                                                                                    |
|   DO NOT ADD UNTIL REALITY REQUIRES IT:                                                                            |
|                                                                                                                    |
|       cloud database                                                                                                |
|       Redis                                                                                                        |
|       Kubernetes                                                                                                   |
|       Docker dependency                                                                                            |
|       microservices                                                                                                |
|       generalized game engine                                                                                      |
|       giant tech tree                                                                                              |
|       agent swarm                                                                                                  |
|       matchmaking                                                                                                  |
|       accounts system                                                                                              |
|       cloud LLM                                                                                                    |
|       voice system                                                                                                 |
|       3D renderer                                                                                                  |
|       public backend merely for convenience                                                                        |
|                                                                                                                    |
|   PREFER:                                                                                                          |
|                                                                                                                    |
|       one repo                                                                                                     |
|       one setup.sh                                                                                                 |
|       one controller                                                                                               |
|       two GitHack pages                                                                                            |
|       one canonical world                                                                                          |
|       one local Gemma                                                                                              |
|       optional Termux edge                                                                                         |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                               ANTI-DRIFT LAW                                                        |
|                                                                                                                    |
|   D&D bot                                              = DRIFT                                                      |
|   Gemma as referee                                     = DRIFT                                                      |
|   user directly puppets Gemma                          = DRIFT                                                      |
|   streamer merely watches                              = DRIFT                                                      |
|   Twitch chat directly prompts Gemma                   = DRIFT                                                      |
|   cloud AI replaces local Gemma                        = DRIFT                                                      |
|   GitHack replaced because another host is easier      = DRIFT                                                      |
|   Termux becomes mandatory                             = DRIFT                                                      |
|   phone becomes canonical truth holder                 = DRIFT                                                      |
|   operator powers become secret game powers            = DRIFT                                                      |
|   narration mutates state                              = FAILURE                                                    |
|   secrets committed publicly                           = FAILURE                                                    |
+====================================================================================================================+
                                                     |
                                                     v
+====================================================================================================================+
|                                                FINAL SYSTEM                                                         |
|                                                                                                                    |
|                                                                                                                    |
|                                  USER + GEMMA 4                                                                     |
|                                       |                                                                            |
|                                       |                                                                            |
|                                  ally.html                                                                          |
|                                       |                                                                            |
|                                       v                                                                            |
|                                  DEBIAN CORE                                                                        |
|                                       |                                                                            |
|                                 WORLD ENGINE                                                                        |
|                                       |                                                                            |
|                          +------------+------------+                                                               |
|                          |                         |                                                               |
|                          v                         v                                                               |
|                    GEMMA CIV                   JAY CIV                                                             |
|                          |                         |                                                               |
|                          |                         v                                                               |
|                          |                 village.html                                                            |
|                          |                         |                                                               |
|                          |                    BIGRIGJAY                                                            |
|                          |                         +                                                               |
|                          |                    TWITCH CHAT                                                          |
|                          |                                                                                         |
|                          v                                                                                         |
|                  USER TWITCH ACCOUNT                                                                               |
|                          |                                                                                         |
|                          v                                                                                         |
|                  BIGRIGJAY'S CHAT                                                                                  |
|                                                                                                                    |
|                                                                                                                    |
|                            ONE REPOSITORY                                                                           |
|                            ONE setup.sh                                                                             |
|                            TWO GITHACK LINKS                                                                        |
|                            ONE CANONICAL WORLD                                                                      |
|                            ONE LOCAL GEMMA                                                                          |
|                            OPTIONAL TERMUX EDGE                                                                     |
|                            TWO ACTUAL SIDES                                                                         |
|                                                                                                                    |
|                                                                                                                    |
|                         MAKE THE WIRING TRUE FIRST.                                                                 |
|                                                                                                                    |
|                           THEN MAKE WAR FUN.                                                                        |
|                                                                                                                    |
|                              REALITY WINS.                                                                          |
+====================================================================================================================+
```