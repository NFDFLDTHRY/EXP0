// BEHAVIOR: observe
// PURPOSE: prove the input side of the machine. Sees every admitted event,
//          proposes nothing. Use this as the ACTIVE behavior while running
//          the first admission tests that concern input, tracing and dedupe.
// INPUTS: every normalized EVENT.
// INTERNAL STATE: a count of events seen (in-memory only; not persisted).
// TRIGGERS: none.
// POSSIBLE ACTIONS: none.
// PROHIBITED ACTIONS: all external actions.
// STOP CONDITION: operator stops the machine or activates another behavior.

let seen = 0;

function onStart(ctx) {
  ctx.note('observe: started');
}

function onEvent(event, ctx) {
  seen += 1;
  if (seen === 1) ctx.note('observe: first event seen', event.event_id);
}
