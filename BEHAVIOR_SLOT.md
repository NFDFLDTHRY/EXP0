# BEHAVIOR SLOT

Copy this file per experiment (e.g. `behaviors/<idea>.md`) and fill every line
before writing `behaviors/<idea>.js`. The machine does not read this file; you do.

    NAME:
        [IDEA NAME]

    PURPOSE:
        [WHAT THE BOT IS ACTUALLY TRYING TO DO]

    INPUTS:
        [WHICH CHAT EVENTS MATTER]

    INTERNAL STATE:
        [WHAT IT NEEDS TO REMEMBER]
        (in-memory: plain variables; across restarts: ctx.state = {...})

    TRIGGERS:
        [WHEN IT SHOULD ACT]

    POSSIBLE ACTIONS:
        [WHAT IT MAY SAY OR DO]
        (say | reply — the operator must have enabled the class in machine.html)

    PROHIBITED ACTIONS:
        [WHAT IT MUST NEVER DO]

    OBSERVATIONS:
        [WHAT WE NEED TO MEASURE]
        (name the history kinds/fields you will read: event, interpretation,
         proposal, admission, action, result)

    SUCCESS CONDITION:
        [HOW WE KNOW THE IDEA WORKS]

    FAILURE CONDITION:
        [HOW WE KNOW IT DOESN'T]

    STOP CONDITION:
        [WHEN THE EXPERIMENT ENDS]

## Contract the source must satisfy

```js
// required
function onEvent(event, ctx) { /* ... */ }
// optional
function onStart(ctx) { /* runs once when the behavior starts; ctx.state holds persisted state or null */ }
```

`event` is the normalized EVENT from FOUNDATION.md plus `is_self` (true when the
chatter is the bot account), `chatter_login`, `channel_login`, and `raw`
(EventSub ids, for tracing only).

`ctx.propose({ source_event_id, action_type: 'say' | 'reply', message, reply_target, reason })`
— a PROPOSAL. The gate decides. `reply_target` must be a `message_id` the machine has observed.

`ctx.note(text, source_event_id)` — an INTERPRETATION line in history ("what the bot believed").

`ctx.state = value` — explicitly persisted working state (JSON), keyed by behavior version.

The behavior runs inside a Web Worker built from the source text: no DOM, no
`localStorage`, no token, no access to the controller or the gate. Anything it
posts other than `note`, `proposal`, `state` is logged as unauthorized and ignored.
More than 50 messages per incoming event stops the behavior as a flood.
