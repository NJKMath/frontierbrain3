"""
palace.py -- Battle Palace move selection logic and probability analysis.

In the Battle Palace, Pokémon act autonomously based on their Nature.
Each turn, a move *category* (Attack / Defense / Support) is selected
according to nature-dependent ratios, and one of the Pokémon's moves in
that category is used.  If no move exists in the chosen category, there
is a 50 % chance the Pokémon picks a random move and a 50 % chance it
wastes its turn.

Provides:
    get_move_category()        - classify a move as attack/defense/support
    categorize_moveset()       - break a moveset into its three categories
    get_nature_ratios()        - raw per-nature category ratios
    get_action_probabilities() - effective per-turn odds given a moveset
    multi_turn_probabilities() - P(exactly k attacks in n turns), etc.
    cumulative_attack_prob()   - P(at least k attacks in n turns)
    expected_attacks()         - E[attacks] in n turns
    DOUBLES_TARGETING          - which foe each Nature targets
"""

from __future__ import annotations

from math import comb
from frontierutils import _norm


# ══════════════════════════════════════════════════════════════════════════════
# Move categories
# ══════════════════════════════════════════════════════════════════════════════
# Attack  = any move NOT listed under Defense or Support.
# Defense = self-/side-/field-targeting moves (no move-calling moves).
# Support = non-damaging moves not in Defense, plus Counter & Mirror Coat.

_DEFENSE_MOVES = frozenset({
    "acidarmor", "agility", "amnesia", "aromatherapy", "barrier",
    "batonpass", "bellydrum", "bide", "bulkup", "calmmind",
    "camouflage", "charge", "conversion2", "conversion", "cosmicpower",
    "defensecurl", "destinybond", "detect", "doubleteam", "dragondance",
    "endure", "focusenergy", "followme", "growth", "grudge",
    "hail", "harden", "haze", "healbell", "helpinghand",
    "howl", "imprison", "ingrain", "irondefense", "lightscreen",
    "meditate", "milkdrink", "minimize", "mist", "moonlight",
    "morningsun", "mudsport", "perishsong", "protect", "raindance",
    "recover", "recycle", "reflect", "refresh", "rest",
    "safeguard", "sandstorm", "sharpen", "slackoff", "softboiled",
    "splash", "stockpile", "substitute", "sunnyday", "swallow",
    "swordsdance", "synthesis", "tailglow", "teleport", "watersport",
    "wish", "withdraw",
})

_SUPPORT_MOVES = frozenset({
    "assist", "attract", "block", "charm", "confuseray",
    "cottonspore", "counter", "curse", "disable", "encore",
    "faketears", "featherdance", "flash", "flatter", "foresight",
    "glare", "grasswhistle", "growl", "hypnosis", "kinesis",
    "leechseed", "leer", "lockon", "lovelykiss", "magiccoat",
    "meanlook", "memento", "metalsound", "metronome", "mimic",
    "mindreader", "mirrorcoat", "mirrormove", "naturepower",
    "nightmare", "odorsleuth", "painsplit", "poisongas", "poisonpowder",
    "psychup", "roar", "roleplay", "sandattack", "scaryface",
    "screech", "sing", "sketch", "skillswap", "sleeppowder",
    "sleeptalk", "smokescreen", "snatch", "spiderweb", "spikes",
    "spite", "spore", "stringshot", "stunspore", "supersonic",
    "swagger", "sweetkiss", "sweetscent", "tailwhip", "taunt",
    "teeterdance", "thunderwave", "tickle", "torment", "toxic",
    "transform", "trick", "whirlwind", "willowisp", "yawn",
})


def get_move_category(move: str) -> str:
    """
    Classify a move as 'attack', 'defense', or 'support' under
    Battle Palace rules.

    Parameters
    ----------
    move : str
        Move name (case/punctuation insensitive).

    Returns
    -------
    str
        One of 'attack', 'defense', 'support'.
    """
    n = _norm(move)
    if n in _DEFENSE_MOVES:
        return "defense"
    if n in _SUPPORT_MOVES:
        return "support"
    return "attack"


def categorize_moveset(moves: list[str]) -> dict[str, list[str]]:
    """
    Split a moveset into Palace categories.

    Parameters
    ----------
    moves : list[str]
        Up to 4 move names.

    Returns
    -------
    dict with keys 'attack', 'defense', 'support', each mapping to a
    list of the original move names in that category.
    """
    cats: dict[str, list[str]] = {"attack": [], "defense": [], "support": []}
    for m in moves:
        cats[get_move_category(m)].append(m)
    return cats


# ══════════════════════════════════════════════════════════════════════════════
# Nature data
# ══════════════════════════════════════════════════════════════════════════════
# (attack%, defense%, support%) at >50 % HP, then at ≤50 % HP.

_NATURE_RATIOS: dict[str, dict] = {
    "hardy":   {"high": (61,  7, 32), "low": (61,  7, 32)},
    "lonely":  {"high": (20, 25, 55), "low": (84,  8,  8)},
    "brave":   {"high": (70, 15, 15), "low": (32, 60,  8)},
    "adamant": {"high": (38, 31, 31), "low": (70, 15, 15)},
    "naughty": {"high": (20, 70, 10), "low": (70, 22,  8)},
    "bold":    {"high": (30, 20, 50), "low": (32, 58, 10)},
    "docile":  {"high": (56, 22, 22), "low": (56, 22, 22)},
    "relaxed": {"high": (25, 15, 60), "low": (75, 15, 10)},
    "impish":  {"high": (69,  6, 25), "low": (28, 55, 17)},
    "lax":     {"high": (35, 10, 55), "low": (29,  6, 65)},
    "timid":   {"high": (62, 10, 28), "low": (30, 20, 50)},
    "hasty":   {"high": (58, 37,  5), "low": (88,  6,  6)},
    "serious": {"high": (34, 11, 55), "low": (29, 11, 60)},
    "jolly":   {"high": (35,  5, 60), "low": (35, 60,  5)},
    "naive":   {"high": (56, 22, 22), "low": (56, 22, 22)},
    "modest":  {"high": (35, 45, 20), "low": (34, 60,  6)},
    "mild":    {"high": (44, 50,  6), "low": (34,  6, 60)},
    "quiet":   {"high": (56, 22, 22), "low": (56, 22, 22)},
    "bashful": {"high": (30, 58, 12), "low": (30, 58, 12)},
    "rash":    {"high": (30, 13, 57), "low": (27,  6, 67)},
    "calm":    {"high": (40, 50, 10), "low": (25, 62, 13)},
    "gentle":  {"high": (18, 70, 12), "low": (90,  5,  5)},
    "sassy":   {"high": (88,  6,  6), "low": (22, 20, 58)},
    "careful": {"high": (42, 50,  8), "low": (42,  5, 53)},
    "quirky":  {"high": (56, 22, 22), "low": (56, 22, 22)},
}


def get_nature_ratios(nature: str, *, low_hp: bool = False) -> dict[str, float]:
    """
    Raw category selection ratios for a Nature.

    Parameters
    ----------
    nature : str
        Pokemon nature name.
    low_hp : bool
        If True, use the ≤50 % HP ratios.

    Returns
    -------
    dict
        {'attack': float, 'defense': float, 'support': float}
        Values are 0-1 probabilities summing to 1.0.
    """
    n = _norm(nature)
    if n not in _NATURE_RATIOS:
        raise ValueError(f"Unknown nature '{nature}'")
    key = "low" if low_hp else "high"
    a, d, s = _NATURE_RATIOS[n][key]
    return {"attack": a / 100, "defense": d / 100, "support": s / 100}


# ══════════════════════════════════════════════════════════════════════════════
# Effective action probabilities
# ══════════════════════════════════════════════════════════════════════════════

def get_action_probabilities(
    nature: str,
    moves: list[str],
    *,
    low_hp: bool = False,
) -> dict[str, float]:
    """
    Effective per-turn probability of each outcome, accounting for the
    moveset's category coverage.

    If the selected category has no move in the set:
        - 50 % chance: pick one of the Pokémon's moves at random
          (distributed across whichever categories the mon *does* have).
        - 50 % chance: the Pokémon wastes its turn (does nothing).

    Parameters
    ----------
    nature : str
        Pokemon nature.
    moves : list[str]
        The moveset (up to 4 moves).
    low_hp : bool
        Use ≤50 % HP ratios.

    Returns
    -------
    dict with keys 'attack', 'defense', 'support', 'nothing'.
        Probabilities sum to 1.0.
        'nothing' is the chance of wasting the turn entirely.
    """
    ratios = get_nature_ratios(nature, low_hp=low_hp)
    cats = categorize_moveset(moves)
    n_total = len(moves)
    if n_total == 0:
        return {"attack": 0.0, "defense": 0.0, "support": 0.0, "nothing": 1.0}

    n = {c: len(cats[c]) for c in ("attack", "defense", "support")}

    # Probability mass landing on empty categories
    p_empty = sum(ratios[c] for c in ("attack", "defense", "support") if n[c] == 0)

    # Of that mass, half is wasted, half is redistributed by random move pick
    p_nothing = p_empty * 0.5
    p_redirect = p_empty * 0.5

    result = {}
    for c in ("attack", "defense", "support"):
        # Direct selection (category has moves)
        direct = ratios[c] if n[c] > 0 else 0.0
        # Redirected from empty-category random pick
        redirected = p_redirect * (n[c] / n_total)
        result[c] = direct + redirected

    result["nothing"] = p_nothing
    return result


def get_move_probabilities(
    nature: str,
    moves: list[str],
    *,
    low_hp: bool = False,
) -> dict[str, float]:
    """
    Per-move usage probability on a single turn.

    Within a selected category, each move is equally likely (uniform AI
    approximation). When a random move is forced (empty category), each
    of the Pokémon's moves is equally likely.

    Parameters
    ----------
    nature : str
    moves : list[str]
    low_hp : bool

    Returns
    -------
    dict  {move_name: probability}
        Plus a 'nothing' key for the skip probability.
        Move names are returned as-given (not normalized).
    """
    ratios = get_nature_ratios(nature, low_hp=low_hp)
    cats = categorize_moveset(moves)
    n_total = len(moves)
    if n_total == 0:
        return {"nothing": 1.0}

    n_cat = {c: len(cats[c]) for c in ("attack", "defense", "support")}

    p_empty = sum(ratios[c] for c in ("attack", "defense", "support") if n_cat[c] == 0)
    p_nothing = p_empty * 0.5
    p_redirect = p_empty * 0.5

    # Per-move probability from redirect: each move gets equal share
    p_redirect_per_move = p_redirect / n_total

    result: dict[str, float] = {}
    for c in ("attack", "defense", "support"):
        if n_cat[c] == 0:
            continue
        # Direct selection: ratio * (1 / number of moves in category)
        direct_per_move = ratios[c] / n_cat[c]
        for m in cats[c]:
            result[m] = direct_per_move + p_redirect_per_move

    result["nothing"] = p_nothing
    return result


# ══════════════════════════════════════════════════════════════════════════════
# Multi-turn probability distributions
# ══════════════════════════════════════════════════════════════════════════════

def multi_turn_probabilities(
    nature: str,
    moves: list[str],
    n_turns: int,
    *,
    low_hp: bool = False,
    category: str = "attack",
) -> dict[int, float]:
    """
    Probability of using a given category exactly k times in n turns.

    Each turn is independent (i.i.d. Bernoulli trial).

    Parameters
    ----------
    nature : str
    moves : list[str]
    n_turns : int
    low_hp : bool
    category : str
        'attack', 'defense', or 'support'.

    Returns
    -------
    dict  {k: P(exactly k times in n_turns)}, k = 0 .. n_turns.
    """
    probs = get_action_probabilities(nature, moves, low_hp=low_hp)
    p = probs.get(category, 0.0)
    q = 1.0 - p

    return {
        k: comb(n_turns, k) * (p ** k) * (q ** (n_turns - k))
        for k in range(n_turns + 1)
    }


def cumulative_attack_prob(
    nature: str,
    moves: list[str],
    n_turns: int,
    min_attacks: int,
    *,
    low_hp: bool = False,
) -> float:
    """
    P(at least `min_attacks` Attack-category moves in `n_turns` turns).

    Parameters
    ----------
    nature, moves, n_turns, low_hp : as above.
    min_attacks : int
        Minimum number of attacking turns desired.

    Returns
    -------
    float   0.0 – 1.0
    """
    dist = multi_turn_probabilities(nature, moves, n_turns, low_hp=low_hp,
                                    category="attack")
    return sum(p for k, p in dist.items() if k >= min_attacks)


def expected_attacks(
    nature: str,
    moves: list[str],
    n_turns: int,
    *,
    low_hp: bool = False,
) -> float:
    """Expected number of Attack-category moves used over n turns."""
    probs = get_action_probabilities(nature, moves, low_hp=low_hp)
    return probs["attack"] * n_turns


# ══════════════════════════════════════════════════════════════════════════════
# Mixed HP-state probability (transition mid-fight)
# ══════════════════════════════════════════════════════════════════════════════

def multi_turn_mixed_hp(
    nature: str,
    moves: list[str],
    high_hp_turns: int,
    low_hp_turns: int,
    *,
    category: str = "attack",
) -> dict[int, float]:
    """
    Probability of using a category exactly k times across a fight where
    the Pokémon spends some turns above 50 % HP and some at or below.

    The two phases are independent sequences with different per-turn odds.

    Parameters
    ----------
    nature : str
    moves : list[str]
    high_hp_turns : int
        Turns spent above 50 % HP.
    low_hp_turns : int
        Turns spent at or below 50 % HP.
    category : str

    Returns
    -------
    dict  {k: probability}, k = 0 .. (high_hp_turns + low_hp_turns).
    """
    d_high = multi_turn_probabilities(nature, moves, high_hp_turns,
                                      low_hp=False, category=category)
    d_low = multi_turn_probabilities(nature, moves, low_hp_turns,
                                     low_hp=True, category=category)

    total_turns = high_hp_turns + low_hp_turns
    result: dict[int, float] = {k: 0.0 for k in range(total_turns + 1)}
    for k1, p1 in d_high.items():
        for k2, p2 in d_low.items():
            result[k1 + k2] += p1 * p2
    return result


# ══════════════════════════════════════════════════════════════════════════════
# Doubles targeting
# ══════════════════════════════════════════════════════════════════════════════

# "higher_hp"  → targets the foe with more HP
# "lower_hp"   → targets the foe with less HP
# "random"     → random foe (also used when both foes have equal HP)

DOUBLES_TARGETING: dict[str, str] = {
    "hardy":   "higher_hp",
    "lonely":  "higher_hp",
    "brave":   "lower_hp",
    "adamant": "higher_hp",
    "naughty": "lower_hp",
    "bold":    "lower_hp",
    "docile":  "random",
    "relaxed": "higher_hp",
    "impish":  "higher_hp",
    "lax":     "higher_hp",
    "timid":   "lower_hp",
    "hasty":   "lower_hp",
    "serious": "lower_hp",
    "jolly":   "higher_hp",
    "naive":   "random",
    "modest":  "lower_hp",
    "mild":    "higher_hp",
    "quiet":   "lower_hp",
    "bashful": "lower_hp",
    "rash":    "higher_hp",
    "calm":    "higher_hp",
    "gentle":  "higher_hp",
    "sassy":   "lower_hp",
    "careful": "lower_hp",
    "quirky":  "higher_hp",
}


# ══════════════════════════════════════════════════════════════════════════════
# Low-HP style change messages
# ══════════════════════════════════════════════════════════════════════════════

_LOW_HP_MESSAGES = {
    "glint":    {"lonely", "adamant", "naughty", "relaxed", "hasty", "gentle"},
    "position": {"brave", "bold", "impish", "jolly", "modest", "calm"},
    "growling": {"lax", "timid", "mild", "rash", "sassy", "careful"},
    "eager":    {"hardy", "docile", "serious", "naive", "quiet", "bashful", "quirky"},
}

_MSG_TEXT = {
    "glint":    "A glint appears in {name}'s eyes!",
    "position": "{name} is getting into position!",
    "growling": "{name} began growling deeply!",
    "eager":    "{name} is eager for more!",
}


def low_hp_message(nature: str, pokemon_name: str = "Pokémon") -> str:
    """Return the flavour text shown when a Pokémon drops to ≤50 % HP."""
    n = _norm(nature)
    for key, natures in _LOW_HP_MESSAGES.items():
        if n in natures:
            return _MSG_TEXT[key].format(name=pokemon_name)
    raise ValueError(f"Unknown nature '{nature}'")


# ══════════════════════════════════════════════════════════════════════════════
# Convenience: rank natures for a moveset
# ══════════════════════════════════════════════════════════════════════════════

def rank_natures(
    moves: list[str],
    *,
    low_hp: bool = False,
    category: str = "attack",
    descending: bool = True,
) -> list[tuple[str, float]]:
    """
    Rank all 25 natures by effective probability of using a category
    given a specific moveset.

    Returns a sorted list of (nature_name, probability) tuples.
    """
    results = []
    for nature in _NATURE_RATIOS:
        probs = get_action_probabilities(nature, moves, low_hp=low_hp)
        results.append((nature.capitalize(), probs[category]))
    results.sort(key=lambda x: x[1], reverse=descending)
    return results