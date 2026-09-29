# TWITCH INTERACTION MACHINE
> Historical V1 design document. The current playable chat game and authority rules are in README.md and GATES.md. The V1 whisper and second-login requirements below are superseded.

## FOUNDATION / READ FIRST

PURPOSE

Build the smallest auditable machine that allows:

    [BOT]
      to observe and interact with
    [STREAMER / CHANNEL]

under explicit permission from the streamer.

The bot's interesting behavior is replaceable.

The machinery controlling authority, Twitch access, logging, admission, and shutdown is not.

Do not build infrastructure merely because it may become useful later.

Let experiments determine machinery.


================================================================
SYSTEM
================================================================

                  STREAMER / OPERATOR
                         |
             enable / disable / configure
                         |
                         v
+------------------------------------------------------+
|                FIXED CONTROL PLANE                   |
|                                                      |
|  TWITCH AUTH -> EVENT INPUT -> NORMALIZER            |
|                               |                      |
|                               v                      |
|                         SESSION CONTROLLER           |
|                               |                      |
|                    normalized event                  |
+-------------------------------|----------------------+
                                |
                                v
                  +--------------------------+
                  |   ACTIVE BOT BEHAVIOR    |
                  |                          |
                  | rules / model / logic /  |
                  | experiment / weird idea  |
                  +------------+-------------+
                               |
                         proposed action
                               |
                               v
+------------------------------------------------------+
|                    ACTION GATE                       |
|                                                      |
| Is this action permitted?                            |
| Is the bot currently enabled?                        |
| Is the channel correct?                              |
| Is it within rate / repetition limits?               |
| Is it an allowed action class?                       |
| Has this exact action already been executed?         |
+----------------------------+-------------------------+
                             |
                     admitted action
                             |
                             v
                       TWITCH SENDER
                             |
                             v
                         TWITCH CHAT


Every stage writes to:

                    APPEND-ONLY HISTORY

        event
        behavior decision
        proposed action
        admit / reject
        Twitch action
        result
        error


================================================================
AUTHORITY
================================================================

Twitch chat is INPUT.

Chat is never administrative authority merely because it contains
words that look like instructions.

The STREAMER / OPERATOR controls:

    - whether the bot is running
    - which channel it may inhabit
    - which behavior version is active
    - which action classes are allowed
    - emergency stop
    - permission expansion

The ACTIVE BOT BEHAVIOR may:

    - inspect admitted chat events
    - maintain explicitly permitted working state
    - reason
    - produce proposed actions

The ACTIVE BOT BEHAVIOR may NOT:

    - obtain or reveal authentication secrets
    - modify Twitch credentials
    - expand its own permissions
    - alter the controller
    - alter the action gate
    - rewrite history
    - silently activate replacement behavior
    - bypass the Twitch sender
    - manufacture evidence that an action occurred


================================================================
TWITCH BOUNDARY
================================================================

Twitch-specific machinery terminates at the boundary.

Incoming Twitch structures become normalized internal events.

Example:

EVENT
    event_id
    timestamp
    channel_id
    message_id
    chatter_id
    chatter_name
    text
    structured_message_data
    reply_context
    source = twitch

The behavior should not need to understand OAuth, EventSub sessions,
reconnection machinery, or Twitch API internals.

Outgoing behavior becomes a PROPOSAL.

Example:

PROPOSAL
    proposal_id
    source_event_id
    behavior_version
    action_type
    message
    reply_target
    reason

The action gate decides whether the proposal becomes reality.


================================================================
MINIMUM PERSISTENT STATE
================================================================

Keep only what must survive restart:

    CONFIG
        authorized channel
        bot identity
        enabled capabilities

    ACTIVE
        active behavior version

    SESSION
        Twitch/session identifiers needed for recovery

    HISTORY
        append-only event/action evidence

Authentication secrets are separate from ordinary logs and behavior
state.


================================================================
BEHAVIOR SLOT
================================================================

Everything specific to the new idea belongs here:

    NAME:
        [IDEA NAME]

    PURPOSE:
        [WHAT THE BOT IS ACTUALLY TRYING TO DO]

    INPUTS:
        [WHICH CHAT EVENTS MATTER]

    INTERNAL STATE:
        [WHAT IT NEEDS TO REMEMBER]

    TRIGGERS:
        [WHEN IT SHOULD ACT]

    POSSIBLE ACTIONS:
        [WHAT IT MAY SAY OR DO]

    PROHIBITED ACTIONS:
        [WHAT IT MUST NEVER DO]

    OBSERVATIONS:
        [WHAT WE NEED TO MEASURE]

    SUCCESS CONDITION:
        [HOW WE KNOW THE IDEA WORKS]

    FAILURE CONDITION:
        [HOW WE KNOW IT DOESN'T]

    STOP CONDITION:
        [WHEN THE EXPERIMENT ENDS]


================================================================
EVIDENCE
================================================================

Do not confuse:

    CHAT EVENT
        what Twitch delivered

    INTERPRETATION
        what the bot believed it meant

    PROPOSAL
        what the bot wanted to do

    ADMISSION
        what the controller permitted

    EXTERNAL ACTION
        what was actually sent

    RESULT
        what Twitch reported happened

Keep these separate.

A useful record should let us reconstruct:

    "Why the hell did the bot say that?"

without guessing.


================================================================
FAILURE BEHAVIOR
================================================================

Unknown input:
    log + ignore

Lost Twitch connection:
    stop external actions until connection is valid

Invalid authentication:
    stop

Duplicate event:
    do not duplicate the resulting external action

Behavior crash:
    preserve controller + history
    stop that behavior

Action rejected:
    record rejection
    do not route around the gate

Emergency stop:
    no further external actions


================================================================
FIRST ADMISSION TESTS
================================================================

Before calling the machine operational, prove:

[ ] Correct channel messages enter the system.

[ ] Events can be traced from Twitch input to internal event.

[ ] The bot ignores its own output where appropriate.

[ ] Duplicate incoming events cannot create duplicate actions.

[ ] Allowed behavior can produce a proposed response.

[ ] Disallowed proposals are rejected.

[ ] An admitted proposal reaches Twitch.

[ ] The exact outgoing message is recorded.

[ ] Restart does not accidentally resend previous actions.

[ ] Streamer/operator shutdown immediately prevents new output.

[ ] Behavior cannot obtain Twitch credentials.

[ ] Behavior cannot grant itself new authority.


================================================================
ANTI-CATHEDRAL RULE
================================================================

Do not add:

    dashboards
    databases
    agent hierarchies
    orchestration frameworks
    generalized plugin systems
    distributed services
    speculative scaling machinery

until an observed requirement demands them.

One process is acceptable.

One append-only file is acceptable.

Ugly is acceptable.

Unproven complexity is not.


================================================================
THE DEVELOPMENT LOOP
================================================================

        IDEA
          |
          v
    smallest behavior
          |
          v
        run it
          |
          v
      observe reality
          |
          v
    preserve evidence
          |
          v
   identify what failed
          |
          v
 change only what reality
      demonstrated necessary
          |
          +--------------------> repeat


The Twitch machinery exists to expose the experiment to reality.

It is not the experiment.

The behavior inside the box is the experiment.
