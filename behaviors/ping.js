// BEHAVIOR: ping
// PURPOSE: the smallest behavior that exercises the whole path:
//          EVENT -> INTERPRETATION -> PROPOSAL -> ADMISSION -> EXTERNAL ACTION -> RESULT.
// INPUTS: chat messages whose text is exactly "!ping" (trimmed, case-insensitive).
// INTERNAL STATE: none.
// TRIGGERS: one matching message => one proposal.
// POSSIBLE ACTIONS: propose a threaded reply "pong" to the triggering message.
//                   (requires the operator to have enabled the "reply" capability)
// PROHIBITED ACTIONS: anything else. Never reacts to the bot's own messages.
// SUCCESS: a chatter types !ping and a "pong" reply appears, and history shows
//          event -> proposal -> admit -> action -> result(is_sent=true) for it.
// FAILURE: pong never appears, appears twice, or appears without a !ping.
// STOP CONDITION: one clean success recorded; then deactivate.

function onEvent(event, ctx) {
  if (event.is_self) return;
  if (String(event.text || '').trim().toLowerCase() !== '!ping') return;
  ctx.note('ping: trigger matched', event.event_id);
  ctx.propose({
    source_event_id: event.event_id,
    action_type: 'reply',
    reply_target: event.message_id,
    message: 'pong',
    reason: 'chat text was exactly !ping'
  });
}
