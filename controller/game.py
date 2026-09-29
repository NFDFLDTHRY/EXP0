"""Small, deterministic EXP0 village war game.

The controller owns persistence and message deduplication. This module has no I/O,
network calls, clock, randomness, or model access. A model proposal selects only an
enemy move; every resource change and combat result is calculated here.

Public API:
    initial_state() -> canonical JSON-serializable state
    parse_command(text) -> commander intent, None, or ValueError for malformed !do
    legal_view(state) -> explicit allowlist of facts suitable for the model
    validate_proposal(obj) -> strict, sanitized enemy proposal or ValueError
    resolve_turn(state, intent, proposal) -> (new_state, authoritative outcome)
    status_text(state), help_text() -> bounded public Twitch messages

The caller must commit the returned state, processed Twitch message ID and evidence
before sending outcome['summary'] to Twitch. The proposal's 'narration' is a candidate
line, not an observed fact, and is deliberately not inserted into the outcome.

Rules for tonight's village:
    Each accepted command advances one day and consumes ceil(population / 6) food.
    Gather gives 8 food, 5 wood or 4 stone. A palisade costs 5 wood and 2 stone
    and grants 2 permanent defense. Two existing villagers can become defenders
    for 4 food. Negotiation costs 3 food and prevents a raid that same day.
    A scout can reveal the enemy front; an attack on that front reduces enemy
    strength. A defense order supplies temporary protection for one enemy move.
    The enemy begins with 10 supply. Raid costs 1, fortify costs 2 to add 1
    strength, and recruit costs 3 to add 2 strength. There is no enemy supply
    creation. Unaffordable proposals become a visible wait. Raids resolve
    against defenders, palisades and the temporary defense order.
    Starvation costs population and morale. Enemy strength 0 wins; population
    or morale 0 loses. All outcomes are computed here, including model moves.
"""

from __future__ import annotations

import copy
import re

WORLD_FIELDS = (
    "version", "day", "turn", "population", "food", "wood", "stone",
    "defenders", "enemy_strength", "enemy_supply", "village_defense", "morale",
    "known_enemy_pressure", "known_enemy_front", "current_event", "result",
)
DIRECTIONS = frozenset(("north", "east", "south", "west"))
ENEMY_ACTIONS = frozenset(("raid", "fortify", "recruit", "wait"))
GATHER_TYPES = frozenset(("food", "wood", "stone"))
_DO = re.compile(r"^!do(?:\s+(.+))?$", re.IGNORECASE)


def initial_state() -> dict:
    """Return a new world. Defenders are included in the population count."""
    return {
        "version": 1,
        "day": 1,
        "turn": 0,
        "population": 18,
        "food": 24,
        "wood": 10,
        "stone": 6,
        "defenders": 3,
        "enemy_strength": 8,
        "enemy_supply": 10,
        "village_defense": 2,
        "morale": 65,
        "known_enemy_pressure": 0,
        "known_enemy_front": None,
        "current_event": "A hostile force gathers beyond the village. Its approach is unknown.",
        "result": "ongoing",
        "_enemy_front": "east",
    }


def parse_command(text: str) -> dict | None:
    """Parse explicit commander !do syntax; ignore other messages.

    Reject an invalid !do with ValueError without creating an intent. No natural
    language or display name can acquire authority through this parser.
    """
    if not isinstance(text, str):
        raise ValueError("command must be text")
    line = text.strip()
    match = _DO.fullmatch(line)
    if not match:
        if re.match(r"^!do(?:\b|$)", line, re.IGNORECASE):
            raise ValueError("invalid !do syntax; type !help")
        return None
    words = (match.group(1) or "").lower().split()
    if not words:
        raise ValueError("choose an action; type !help")
    action, args = words[0], words[1:]
    if action in ("scout", "attack") and len(args) == 1 and args[0] in DIRECTIONS:
        return {"action": action, "target": args[0]}
    if action == "gather" and len(args) == 1 and args[0] in GATHER_TYPES:
        return {"action": action, "target": args[0]}
    if action == "build" and args == ["palisade"]:
        return {"action": action, "target": "palisade"}
    if action == "recruit" and args == ["defenders"]:
        return {"action": action, "target": "defenders"}
    if action == "defend" and (not args or len(args) == 1 and args[0] in DIRECTIONS):
        return {"action": action, "target": args[0] if args else None}
    if action == "negotiate" and not args:
        return {"action": action, "target": None}
    raise ValueError("unknown action or target; type !help")


def legal_view(state: dict) -> dict:
    """Make an explicit public/model projection, excluding all private state keys.

    The model receives this projection, never the canonical dict. Future private
    mechanics can be added without silently entering the model prompt.
    """
    _check_state(state)
    return {key: copy.deepcopy(state[key]) for key in WORLD_FIELDS}


def validate_proposal(obj: dict) -> dict:
    """Validate one strict model JSON proposal; no proposal may contain state edits.

    Required exact shape: {"enemy_action": "raid|fortify|recruit|wait",
    "enemy_target": "north|east|south|west" or null, "narration": "..."}.
    A raid needs a direction; every other enemy action needs a null target.
    Narration is untrusted pre-resolution flavor and never becomes a game fact.
    """
    if type(obj) is not dict or set(obj) != {"enemy_action", "enemy_target", "narration"}:
        raise ValueError("proposal requires exactly enemy_action, enemy_target, narration")
    action, target, narration = (obj[k] for k in ("enemy_action", "enemy_target", "narration"))
    if type(action) is not str or action not in ENEMY_ACTIONS:
        raise ValueError("unknown enemy action")
    if action == "raid":
        if type(target) is not str or target not in DIRECTIONS:
            raise ValueError("raid requires a cardinal enemy_target")
    elif target is not None:
        raise ValueError("non-raid enemy_target must be null")
    if type(narration) is not str or not 1 <= len(narration) <= 200 or not narration.strip():
        raise ValueError("narration must be 1-200 characters")
    if any(ord(c) < 32 or ord(c) == 127 for c in narration):
        raise ValueError("narration must be one printable line")
    return {"enemy_action": action, "enemy_target": target, "narration": narration.strip()}


def _check_state(state: dict) -> None:
    """Reject corrupt or incomplete persisted state before rule execution."""
    if type(state) is not dict or any(key not in state for key in WORLD_FIELDS + ("_enemy_front",)):
        raise ValueError("incomplete canonical world")
    numeric = (
        "version", "day", "turn", "population", "food", "wood", "stone",
        "defenders", "enemy_strength", "enemy_supply", "village_defense", "morale", "known_enemy_pressure",
    )
    if any(type(state[key]) is not int or state[key] < 0 for key in numeric):
        raise ValueError("invalid canonical world counters")
    if state["defenders"] > state["population"] or state["morale"] > 100:
        raise ValueError("invalid canonical world bounds")
    if state["_enemy_front"] not in DIRECTIONS:
        raise ValueError("invalid private enemy front")
    if state["known_enemy_front"] is not None and state["known_enemy_front"] not in DIRECTIONS:
        raise ValueError("invalid known enemy front")
    if type(state["current_event"]) is not str or state["result"] not in ("ongoing", "victory", "defeat"):
        raise ValueError("invalid canonical world event or result")


def _check_intent(intent: dict) -> tuple[str, str | None]:
    if type(intent) is not dict or set(intent) != {"action", "target"}:
        raise ValueError("invalid commander intent")
    action, target = intent["action"], intent["target"]
    if type(action) is not str or target is not None and type(target) is not str:
        raise ValueError("invalid commander intent")
    # Reuse the one grammar rather than maintaining a second policy.
    reconstructed = "!do " + action + (" " + target if target else "")
    if parse_command(reconstructed) != intent:
        raise ValueError("illegal commander intent")
    return action, target


def resolve_turn(state: dict, intent: dict, proposal: dict) -> tuple[dict, dict]:
    """Resolve exactly one legal commander turn and one model-selected enemy move.

    Inputs are never mutated. This is a total deterministic transition for legal
    inputs. Resource prerequisites raise ValueError before any state can change.
    Every legal action advances one day, charges food upkeep of ceil(population/6),
    and then applies the enemy move unless the village already won.
    """
    _check_state(state)
    action, target = _check_intent(intent)
    enemy = validate_proposal(proposal)
    if state["result"] != "ongoing":
        raise ValueError("the battle has ended; use !status")
    if action == "build" and (state["wood"] < 5 or state["stone"] < 2):
        raise ValueError("palisade needs 5 wood and 2 stone")
    if action == "recruit" and (state["food"] < 4 or state["population"] - state["defenders"] < 2):
        raise ValueError("recruiting needs 4 food and 2 available villagers")
    if action == "attack" and state["defenders"] < 1:
        raise ValueError("attacking needs at least 1 defender")
    if action == "negotiate" and state["food"] < 3:
        raise ValueError("a truce offer needs 3 food")

    world = copy.deepcopy(state)
    events = []
    guard = 0
    truce = False
    if action == "scout":
        if target == world["_enemy_front"]:
            world["known_enemy_front"] = target
            world["known_enemy_pressure"] = world["enemy_strength"]
            world["morale"] = min(100, world["morale"] + 2)
            events.append(f"Scouts find {world['enemy_strength']} enemy strength to the {target}.")
        else:
            events.append(f"Scouts find no enemy host to the {target}.")
    elif action == "gather":
        amount = {"food": 8, "wood": 5, "stone": 4}[target]
        world[target] += amount
        events.append(f"Villagers gather {amount} {target}.")
    elif action == "build":
        world["wood"] -= 5
        world["stone"] -= 2
        world["village_defense"] += 2
        events.append("A palisade rises: 5 wood and 2 stone spent; defense +2.")
    elif action == "recruit":
        world["food"] -= 4
        world["defenders"] += 2
        world["morale"] = min(100, world["morale"] + 2)
        events.append("Two villagers join the defenders; 4 food spent.")
    elif action == "defend":
        guard = 6 if target is None or target == world["_enemy_front"] else 1
        events.append("The village holds a defensive line" + (f" to the {target}." if target else "."))
    elif action == "attack":
        if target == world["_enemy_front"]:
            losses = min(world["enemy_strength"], max(1, (world["defenders"] * 2 + world["morale"] // 30) // 4))
            world["enemy_strength"] -= losses
            world["known_enemy_front"] = target
            world["known_enemy_pressure"] = world["enemy_strength"]
            events.append(f"The attack to the {target} defeats {losses} enemy strength.")
        else:
            lost_food = min(1, world["food"])
            world["food"] -= lost_food
            world["morale"] = max(0, world["morale"] - 4)
            events.append(f"The attack to the {target} finds no enemy; {lost_food} food is lost.")
    elif action == "negotiate":
        world["food"] -= 3
        world["morale"] = min(100, world["morale"] + 2)
        truce = True
        events.append("Envoys offer 3 food. A truce holds for this turn.")

    upkeep = (world["population"] + 5) // 6
    shortage = max(0, upkeep - world["food"])
    world["food"] = max(0, world["food"] - upkeep)
    if shortage:
        deaths = min(world["population"], (shortage + 1) // 2)
        world["population"] -= deaths
        world["defenders"] = min(world["defenders"], world["population"])
        world["morale"] = max(0, world["morale"] - shortage * 5)
        events.append(f"Food shortage costs {deaths} villager(s); morale falls.")
    else:
        events.append(f"The village consumes {upkeep} food.")

    if world["enemy_strength"] > 0 and world["population"] > 0 and world["morale"] > 0:
        enemy_action = enemy["enemy_action"]
        cost = {"raid": 1, "fortify": 2, "recruit": 3, "wait": 0}[enemy_action]
        if cost > world["enemy_supply"]:
            events.append("Enemy lines remain quiet; no fresh movement is seen.")
        elif enemy_action == "raid":
            world["enemy_supply"] -= cost
            raid_front = enemy["enemy_target"]
            world["_enemy_front"] = raid_front
            world["known_enemy_front"] = raid_front
            world["known_enemy_pressure"] = world["enemy_strength"]
            if truce:
                events.append(f"The enemy raid to the {raid_front} stops at the truce line.")
            else:
                protection = world["defenders"] + world["village_defense"] + guard
                danger = max(0, world["enemy_strength"] - protection)
                deaths = min(world["population"], danger // 3)
                world["population"] -= deaths
                world["defenders"] = min(world["defenders"], max(0, world["defenders"] - deaths))
                stolen = min(world["food"], (danger + 1) // 4)
                world["food"] -= stolen
                attrition = min(world["enemy_strength"], max(0, (protection - world["enemy_strength"]) // 3))
                world["enemy_strength"] -= attrition
                world["known_enemy_pressure"] = world["enemy_strength"]
                if deaths:
                    world["morale"] = max(0, world["morale"] - deaths * 5)
                events.append(f"Enemy raids from the {raid_front}: {deaths} villagers lost, {stolen} food taken, {attrition} enemy strength repelled.")
        elif enemy_action == "fortify":
            world["enemy_supply"] -= cost
            world["enemy_strength"] = min(20, world["enemy_strength"] + 1)
            events.append("Scouts report new enemy earthworks; strength rises by 1.")
        elif enemy_action == "recruit":
            world["enemy_supply"] -= cost
            world["enemy_strength"] = min(20, world["enemy_strength"] + 2)
            events.append("Scouts spot enemy reinforcements; strength rises by 2.")
        else:
            events.append("No enemy movement is seen.")

    world["turn"] += 1
    world["day"] += 1
    world["version"] += 1
    if world["enemy_strength"] == 0:
        world["result"] = "victory"
        events.append("Victory: the enemy force is broken.")
    elif world["population"] == 0 or world["morale"] == 0:
        world["result"] = "defeat"
        events.append("Defeat: the village can no longer hold.")
    world["current_event"] = events[-1]
    summary = f"Day {world['day']}: " + " ".join(events)
    outcome = {
        "action": action, "target": target, "enemy_action": enemy["enemy_action"],
        "events": events, "summary": summary, "result": world["result"],
        "version": world["version"],
    }
    return world, outcome


def status_text(state: dict) -> str:
    """Render only public facts, in a short Twitch-ready message."""
    view = legal_view(state)
    front = view["known_enemy_front"] or "unknown"
    return (
        f"Day {view['day']} | people {view['population']} | food {view['food']} "
        f"wood {view['wood']} stone {view['stone']} | defenders {view['defenders']} "
        f"defense {view['village_defense']} | morale {view['morale']} "
        f"| enemy {view['enemy_strength']} supply {view['enemy_supply']} | known front {front} "
        f"| {view['result']}. {view['current_event']}"
    )


def help_text() -> str:
    """Explicit Twitch grammar; the controller separately checks chatter numeric ID."""
    return (
        "Jay: !do scout north/east/south/west, !do gather food/wood/stone, "
        "!do build palisade, !do recruit defenders, !do defend [direction], "
        "!do attack direction, !do negotiate. Anyone: !status, !help. "
        "Viewers: !suggest your advice (council only)."
    )
