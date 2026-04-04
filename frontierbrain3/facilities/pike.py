"""
pike.py -- Battle Pike event probabilities, wild Pokemon, and hints.

Provides:
    get_event_probabilities() - adjusted event odds given party state
    get_status_chances()      - status infliction odds with immunities
    get_wild_pokemon()        - wild Pokemon pool for a given room number
    HINTS                     - hint text -> possible event pairs
"""

# -- Events --------------------------------------------------------------------
# 8 possible events, each with equal base chance (1/8).
# Some are conditionally excluded based on party state.

EVENTS = {
    "single_battle":    "A Trainer with 3 Pokemon walks up and battles.",
    "double_battle":    "Two Trainers with 1 Pokemon each team up and battle.",
    "hard_battle_heal": "A tough Trainer battle; full party heal if you win.",
    "wild_pokemon":     "Wild Pokemon appear as you cross a long corridor.",
    "no_event":         "An NPC stands to the side and does nothing.",
    "status":           "A Gentleman's Pokemon inflicts a status condition.",
    "partial_heal":     "A Gentleman fully heals one or two of your Pokemon.",
    "full_heal":        "A receptionist fully heals all three of your Pokemon.",
}

# Which events are excluded under which conditions
# double_battle: excluded if 2+ fainted
# status: excluded if all living mons already have a status
# partial_heal: excluded if all mons at full HP
# full_heal: excluded if all mons at full HP


def get_event_probabilities(
    *,
    num_fainted: int = 0,
    all_full_hp: bool = True,
    all_living_statused: bool = False,
) -> dict[str, float]:
    """
    Return the probability of each event occurring in a room.

    Parameters
    ----------
    num_fainted : int
        Number of fainted Pokemon (0-2).
    all_full_hp : bool
        True if all Pokemon are at full HP (no damage/status).
    all_living_statused : bool
        True if every non-fainted Pokemon already has a status condition.

    Returns
    -------
    dict[str, float]
        Event name -> probability (0.0-1.0). Excluded events have 0.0.
    """
    available = list(EVENTS.keys())

    # Double battle excluded if 2+ fainted
    if num_fainted >= 2 and "double_battle" in available:
        available.remove("double_battle")

    # Status excluded if all living mons already statused
    if all_living_statused and "status" in available:
        available.remove("status")

    # Healing rooms excluded if all at full HP
    if all_full_hp:
        if "partial_heal" in available:
            available.remove("partial_heal")
        if "full_heal" in available:
            available.remove("full_heal")

    n = len(available)
    result = {}
    for event in EVENTS:
        result[event] = (1.0 / n) if event in available else 0.0
    return result


# -- Status conditions ---------------------------------------------------------

STATUS_TABLE = [
    {
        "status": "bad_poison",
        "probability": 0.35,
        "move": "Toxic",
        "user": "Kirlia",
        "immune_types": ["poison", "steel"],
        "immune_abilities": ["immunity"],
    },
    {
        "status": "freeze",
        "probability": 0.25,
        "move": "Ice Beam",
        "user": "Dusclops",
        "immune_types": ["ice"],
        "immune_abilities": ["magmaarmor"],
    },
    {
        "status": "paralysis",
        "probability": 0.20,
        "move": "Thunder Wave",
        "user": "Kirlia",
        "immune_types": ["ground", "electric"],
        "immune_abilities": ["limber"],
    },
    {
        "status": "sleep",
        "probability": 0.10,
        "move": "Hypnosis",
        "user": "Kirlia",
        "immune_types": [],
        "immune_abilities": ["insomnia", "vitalspirit"],
    },
    {
        "status": "burn",
        "probability": 0.10,
        "move": "Will-O-Wisp",
        "user": "Dusclops",
        "immune_types": ["fire"],
        "immune_abilities": ["waterveil"],
    },
]

# Number of Pokemon targeted by the status room, by pass number
def status_targets(pass_num: int) -> int:
    """How many non-fainted, non-statused Pokemon are targeted."""
    if pass_num <= 5:
        return 1
    elif pass_num <= 10:
        return 2
    else:
        return 3


def get_status_chances(
    pokemon_types: list[list[str]],
    pokemon_abilities: list[str],
    *,
    pass_num: int = 1,
) -> dict[str, float]:
    """
    Calculate effective status infliction probabilities for each status,
    accounting for type/ability immunities on your team.

    Parameters
    ----------
    pokemon_types : list[list[str]]
        Types for each non-fainted, non-statused Pokemon on the team.
        E.g. [["steel","psychic"], ["water"], ["normal","flying"]]
    pokemon_abilities : list[str]
        Abilities for each corresponding Pokemon.
        E.g. ["clearbody", "intimidate", "keeneye"]

    pass_num : int
        Current pass number (affects how many mons are targeted).

    Returns
    -------
    dict[str, float]
        For each status: probability that at least one team member
        gets afflicted with it (considering immunities).
    """
    from ..frontierutils import _norm

    n_mons = len(pokemon_types)
    n_targets = min(status_targets(pass_num), n_mons)

    result = {}
    for entry in STATUS_TABLE:
        status = entry["status"]
        base_prob = entry["probability"]
        immune_types = {_norm(t) for t in entry["immune_types"]}
        immune_abs = {_norm(a) for a in entry["immune_abilities"]}

        # Count how many mons are immune
        n_immune = 0
        for i in range(n_mons):
            types = {_norm(t) for t in pokemon_types[i]}
            ab = _norm(pokemon_abilities[i])
            if types & immune_types or ab in immune_abs:
                n_immune += 1

        n_vulnerable = n_mons - n_immune

        # Probability that at least one targeted mon is vulnerable
        # Targeting is random among the eligible mons
        if n_vulnerable == 0 or n_targets == 0:
            result[status] = 0.0
        elif n_vulnerable >= n_mons:
            # All vulnerable, status always lands
            result[status] = base_prob
        else:
            # Probability that all targeted mons are immune
            # = C(n_immune, n_targets) / C(n_mons, n_targets)
            from math import comb
            p_all_immune = comb(n_immune, n_targets) / comb(n_mons, n_targets)
            result[status] = base_prob * (1.0 - p_all_immune)

    return result


# -- Hints ---------------------------------------------------------------------
# The receptionist hints at what one of the three paths contains.
# Each hint maps to two possible events. The other two paths will NOT
# contain either of the hinted events.

HINTS = {
    "nostalgia": {
        "text": "For some odd reason, I felt a wave of nostalgia coming from it...",
        "events": ["status", "partial_heal"],
    },
    "people": {
        "text": "Is it...A Trainer? I sense the presence of people...",
        "events": ["single_battle", "full_heal"],
    },
    "aroma": {
        "text": "It seems to have the distinct aroma of Pokemon wafting around it...",
        "events": ["wild_pokemon", "hard_battle_heal"],
    },
    "whispering": {
        "text": "I seem to have heard something... It may have been whispering...",
        "events": ["no_event", "double_battle"],
    },
    "dreadful": {
        "text": "From every path I sense a dreadful presence...",
        "events": ["pike_queen"],
    },
}


# -- Wild Pokemon --------------------------------------------------------------
# Wild Pokemon appear in the "wild_pokemon" event room.
# Seviper and Milotic always appear (26% each).
# The 48% slot rotates based on cumulative room number.

WILD_POKEMON_LV50 = {
    "seviper": {
        "species": "Seviper", "ability": "Shed Skin", "level": 46, "rate": 26,
        "moves": ["Toxic", "Glare", "Sludge Bomb", "Body Slam"],
    },
    "milotic": {
        "species": "Milotic", "ability": "Marvel Scale", "level": 46, "rate": 26,
        "moves": ["Toxic", "Hypnosis", "Body Slam", "Surf"],
    },
    "dusclops": {
        "species": "Dusclops", "ability": "Pressure", "level": 45, "rate": 48,
        "moves": ["Will-O-Wisp", "Mean Look", "Toxic", "Shadow Punch"],
        "rooms": [1, 280],
    },
    "electrode": {
        "species": "Electrode", "ability": "Soundproof", "level": 45, "rate": 48,
        "moves": ["Explosion", "Selfdestruct", "Thunder", "Toxic"],
        "rooms": [281, 560],
    },
    "breloom": {
        "species": "Breloom", "ability": "Effect Spore", "level": 45, "rate": 48,
        "moves": ["Spore", "Stun Spore", "PoisonPowder", "Hidden Power"],
        "rooms": [561, 840],
    },
    "wobbuffet": {
        "species": "Wobbuffet", "ability": "Shadow Tag", "level": 45, "rate": 48,
        "moves": ["Counter", "Mirror Coat", "Safeguard", "Destiny Bond"],
        "rooms": [841, None],  # 841+
    },
}

WILD_POKEMON_OPEN = {
    "seviper": {
        "species": "Seviper", "ability": "Shed Skin", "level": [60, 96], "rate": 26,
        "moves": ["Toxic", "Glare", "Sludge Bomb", "Poison Fang"],
    },
    "milotic": {
        "species": "Milotic", "ability": "Marvel Scale", "level": [60, 96], "rate": 26,
        "moves": ["Toxic", "Hypnosis", "Body Slam", "Ice Beam"],
    },
    "dusclops": {
        "species": "Dusclops", "ability": "Pressure", "level": [60, 95], "rate": 48,
        "moves": ["Will-O-Wisp", "Mean Look", "Toxic", "Ice Beam"],
        "rooms": [1, 280],
    },
    "electrode": {
        "species": "Electrode", "ability": "Soundproof", "level": [60, 95], "rate": 48,
        "moves": ["Explosion", "Selfdestruct", "Thunder", "Toxic"],
        "rooms": [281, 560],
    },
    "breloom": {
        "species": "Breloom", "ability": "Effect Spore", "level": [60, 95], "rate": 48,
        "moves": ["Spore", "Stun Spore", "PoisonPowder", "Hidden Power"],
        "rooms": [561, 840],
    },
    "wobbuffet": {
        "species": "Wobbuffet", "ability": "Shadow Tag", "level": [60, 95], "rate": 48,
        "moves": ["Counter", "Mirror Coat", "Safeguard", "Encore"],
        "rooms": [841, None],
    },
}


def get_wild_pokemon(cumulative_room: int, *, lv50: bool = True) -> list[dict]:
    """
    Return the wild Pokemon pool for a given cumulative room number.

    Parameters
    ----------
    cumulative_room : int
        Total rooms entered across all challenges (1-based).
    lv50 : bool
        True for Lv50 format, False for Open Level.

    Returns
    -------
    list[dict]
        List of {species, ability, level, rate, moves} dicts.
        Always 3 Pokemon: Seviper (26%), Milotic (26%), and
        one rotating 48% encounter.
    """
    pool = WILD_POKEMON_LV50 if lv50 else WILD_POKEMON_OPEN

    result = [dict(pool["seviper"]), dict(pool["milotic"])]

    # Determine the 48% slot based on room number
    for key in ("dusclops", "electrode", "breloom", "wobbuffet"):
        entry = pool[key]
        low, high = entry["rooms"]
        if high is None:
            if cumulative_room >= low:
                result.append({k: v for k, v in entry.items() if k != "rooms"})
                break
        elif low <= cumulative_room <= high:
            result.append({k: v for k, v in entry.items() if k != "rooms"})
            break

    return result


# -- Difficulty ----------------------------------------------------------------
# From round 9 onwards, Hard Single Battle uses the same difficulty as
# regular Single Battle (no tier difference).
HARD_BATTLE_SAME_DIFFICULTY_FROM = 9