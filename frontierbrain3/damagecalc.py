"""
damagecalc.py -- Gen 3 (ADV) damage calculator for Battle Frontier analysis.

Provides:
    damage_rolls()        - per-hit damage values for a given attack
    get_hit_info()        - multi-hit info for a move
    ko_chance()           - probability of n-HKO (single-hit moves)
    multi_hit_ohko_prob() - exact OHKO probability (multi-hit aware)
    calc_matchup()        - convenience wrapper returning a full summary dict
    format_result()       - pretty-print a matchup result

Dependencies: frontierutils only (no frontier_db).
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from .frontierutils import (
    _norm, calc_stats, apply_stage, move_category,
    type_effectiveness, _TYPE_CHART,
    CustomSet, POKEMON_FILE,
)

# -- Move property lists (kept here so we don't need flags in moves.json) ------

_SOUND_MOVES = frozenset({
    "grasswhistle", "growl", "healbell", "hypervoice", "metalsound",
    "perishsong", "roar", "screech", "sing", "snore", "supersonic", "uproar",
})

# Gen 3 spread: moves that hit both foes (NOT all-field like EQ/Explosion).
# Damage halved in doubles if more than one target.
_SPREAD_MOVES = frozenset({
    "acid", "aircutter", "blizzard", "bubble", "eruption", "heatwave",
    "hypervoice", "icywind", "muddywater", "powdersnow", "razorleaf",
    "razorwind", "rockslide", "swift", "twister", "waterspout",
})

# Multi-hit moves
_FIXED_2_HIT = frozenset({"doublekick", "bonemerang", "twineedle"})
_VARIABLE_2_5_HIT = frozenset({
    "armthrust", "barrage", "bonerush", "bulletseed", "cometpunch",
    "doubleslap", "furyattack", "furyswipes", "iciclespear", "pinmissile",
    "rockblast", "spikecannon",
})
# Gen 3: 2-5 hit distribution: 2=3/8, 3=3/8, 4=1/8, 5=1/8
_MULTI_HIT_WEIGHTS = {2: 3, 3: 3, 4: 1, 5: 1}  # out of 8

# Triple Kick: 3 kicks at 10/20/30 power, each 90% acc, stops on miss
_TRIPLE_KICK_POWERS = [10, 20, 30]
_TRIPLE_KICK_ACC = 0.9

# Recoil moves: fraction of damage dealt taken as recoil
RECOIL_MOVES: dict[str, float] = {
    "doubleedge": 1/3,
    "struggle": 1/4,
    "submission": 1/4,
    "takedown": 1/4,
    "volttackle": 1/3,
}

# Drain moves: fraction of damage dealt healed
DRAIN_MOVES: dict[str, float] = {
    "absorb": 1/2,
    "megadrain": 1/2,
    "gigadrain": 1/2,
    "leechlife": 1/2,
    "dreameater": 1/2,
}


# -- Item / ability lookups ----------------------------------------------------

# Gen 3 type-boosting held items -> boosted type
# In Gen 3, these boost the ATTACK STAT by 1.1x (not base power like Gen 4+)
_TYPE_BOOST_ITEMS: dict[str, str] = {
    "silkscarf": "normal", "blackbelt": "fighting", "poisonbarb": "poison",
    "softsand": "ground", "sharpbeak": "flying", "silverpowder": "bug",
    "hardstone": "rock", "spelltag": "ghost", "metalcoat": "steel",
    "charcoal": "fire", "mysticwater": "water", "magnet": "electric",
    "miracleseed": "grass", "nevermeltice": "ice", "twistedspoon": "psychic",
    "dragonfang": "dragon", "blackglasses": "dark",
}

# Pinch abilities -> boosted type (activate at <=1/3 HP, 1.5x base power)
_PINCH_ABILITIES: dict[str, str] = {
    "overgrow": "grass", "blaze": "fire", "torrent": "water", "swarm": "bug",
}

_MAGNITUDE_TABLE = [
    (10, 1), (30, 2), (50, 4), (70, 6), (90, 4), (110, 2), (150, 1),
]


# -- Move data loading ---------------------------------------------------------

_MOVES_FILE = Path(__file__).parent / "data" / "moves.json"
_moves_cache: dict | None = None


def _load_moves() -> dict:
    global _moves_cache
    if _moves_cache is not None:
        return _moves_cache
    if _MOVES_FILE.exists():
        with open(_MOVES_FILE, encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, list):
            _moves_cache = {_norm(m["name"]): m for m in raw}
        else:
            _moves_cache = {_norm(k): v for k, v in raw.items()}
        return _moves_cache
    return {}


def get_move(move: Union[str, dict]) -> dict:
    if isinstance(move, dict):
        m = dict(move)
        m.setdefault("category", move_category(m["type"]))
        m.setdefault("name", "Unknown")
        return m
    name = _norm(move)
    moves_db = _load_moves()
    if name not in moves_db:
        raise ValueError(
            f"Move '{move}' not found. Pass a dict with 'type' and 'power', "
            f"or ensure data/moves.json exists and contains it."
        )
    m = dict(moves_db[name])
    m.setdefault("category", move_category(m["type"]))
    return m


# -- Multi-hit helpers ---------------------------------------------------------

def get_hit_info(move) -> dict:
    """
    Returns hit info for a move:
        {"type": "single"}
        {"type": "fixed", "hits": 2}
        {"type": "variable", "weights": {2:3, 3:3, 4:1, 5:1}}
        {"type": "triple_kick", "powers": [10, 20, 30], "acc": 0.9}
    """
    mv = get_move(move)
    name = _norm(mv.get("name", ""))
    if name in _FIXED_2_HIT:
        return {"type": "fixed", "hits": 2}
    if name in _VARIABLE_2_5_HIT:
        return {"type": "variable", "weights": dict(_MULTI_HIT_WEIGHTS)}
    if name == "triplekick":
        return {"type": "triple_kick", "powers": list(_TRIPLE_KICK_POWERS), "acc": _TRIPLE_KICK_ACC}
    return {"type": "single"}


def _convolve_once(dist: dict[int, int], rolls: list[int]) -> dict[int, int]:
    """Add one round of rolls to an existing damage distribution."""
    new = {}
    for total, count in dist.items():
        for r in rolls:
            t = total + r
            new[t] = new.get(t, 0) + count
    return new


def _ko_prob_from_dist(dist: dict[int, int], total_combos: int, hp: int) -> float:
    """Fraction of outcomes in dist that deal >= hp damage."""
    return sum(c for t, c in dist.items() if t >= hp) / total_combos


def _expand_dist(dist: dict[int, int], total: int) -> list[int]:
    """Expand a {damage: count} distribution into a flat list."""
    result = []
    for dmg, count in sorted(dist.items()):
        result.extend([dmg] * count)
    return result


def combine_multi_hit_rolls(per_hit_rolls: list[int], hit_info: dict) -> list[int]:
    """
    Combine per-hit rolls into a single-attack total distribution.
    Returns a flat list of all possible totals (length varies by hit type).
    Suitable for feeding into ko_chance().
    """
    h = hit_info["type"]
    if h == "single":
        return list(per_hit_rolls)
    if h == "fixed":
        dist = {0: 1}
        for _ in range(hit_info["hits"]):
            dist = _convolve_once(dist, per_hit_rolls)
        return _expand_dist(dist, len(per_hit_rolls) ** hit_info["hits"])
    if h == "variable":
        weights = hit_info["weights"]
        n = len(per_hit_rolls)
        all_rolls = []
        for hits, w in weights.items():
            dist = {0: 1}
            for _ in range(hits):
                dist = _convolve_once(dist, per_hit_rolls)
            combos = n ** hits
            expanded = _expand_dist(dist, combos)
            all_rolls.extend(expanded * w)
        return all_rolls
    return list(per_hit_rolls)


def multi_hit_ohko_prob(per_hit_rolls: list[int], hp: int, hit_info: dict) -> float:
    """
    Exact OHKO probability for a single attack (possibly multi-hit).
    Returns 0.0-1.0.
    """
    h = hit_info["type"]
    n = len(per_hit_rolls)

    if h == "single":
        return sum(1 for r in per_hit_rolls if r >= hp) / n

    if h == "fixed":
        dist = {0: 1}
        for _ in range(hit_info["hits"]):
            dist = _convolve_once(dist, per_hit_rolls)
        return _ko_prob_from_dist(dist, n ** hit_info["hits"], hp)

    if h == "variable":
        weights = hit_info["weights"]
        total_weight = sum(weights.values())
        prob = 0.0
        for hits, w in weights.items():
            dist = {0: 1}
            for _ in range(hits):
                dist = _convolve_once(dist, per_hit_rolls)
            p = _ko_prob_from_dist(dist, n ** hits, hp)
            prob += (w / total_weight) * p
        return prob

    if h == "triple_kick":
        # Caller should handle Triple Kick separately with per-kick rolls
        return sum(1 for r in per_hit_rolls if r >= hp) / n

    return sum(1 for r in per_hit_rolls if r >= hp) / n


# -- Field conditions ----------------------------------------------------------

@dataclass
class Field:
    weather: str = "none"
    reflect: bool = False
    light_screen: bool = False
    is_doubles: bool = False
    helping_hand: bool = False
    cloud_nine: bool = False


# -- Combatant extraction ------------------------------------------------------

def _extract(s, species_map: dict, *,
             ivs: int = 31, level: int = 100,
             ability_override: str = None) -> dict:
    if isinstance(s, CustomSet):
        dex_entry = next(
            (p for p in species_map.values() if _norm(p["name"]) == _norm(s.pokemon)),
            None,
        )
        return {
            "stats": s.get_stats(),
            "types": dex_entry.get("types", []) if dex_entry else [],
            "ability": _norm(ability_override or s.ability or ""),
            "item": _norm(s.item or "none"),
            "species": _norm(s.pokemon),
            "level": s.level,
            "weight": dex_entry.get("weight", 0) if dex_entry else 0,
        }
    stats = calc_stats(s, species_map, ivs=ivs, level=level)
    dex = s.get("DexNum")
    sp = species_map.get(dex, {})
    abilities = s.get("Abilities", [])
    return {
        "stats": stats,
        "types": sp.get("types", []),
        "ability": _norm(ability_override or (abilities[0] if abilities else "")),
        "item": _norm(s.get("Item", "None")),
        "species": _norm(s.get("Pokemon", "")),
        "level": level,
        "weight": sp.get("weight", 0),
    }


def _get_weight_kg(defender, species_map) -> float:
    if isinstance(defender, CustomSet):
        dex_entry = next(
            (p for p in species_map.values() if _norm(p["name"]) == _norm(defender.pokemon)),
            None,
        )
        return (dex_entry.get("weight", 0) if dex_entry else 0) / 10
    dex = defender.get("DexNum")
    return species_map.get(dex, {}).get("weight", 0) / 10


# -- Core damage formula -------------------------------------------------------

def damage_rolls(
    attacker, defender, move,
    species_map: dict,
    *,
    atk_ivs: int = 31,
    def_ivs: int = 31,
    atk_level: int = 100,
    def_level: int = 100,
    atk_ability: str = None,
    def_ability: str = None,
    field: Field = None,
    critical: bool = False,
    atk_status: str = None,
    def_status: str = None,
    flash_fire_active: bool = False,
    stockpile_count: int = 0,
    charge_active: bool = False,
    double_dmg: bool = False,
    atk_boosts: dict = None,
    def_boosts: dict = None,
    atk_current_hp: int = None,
    def_current_hp: int = None,
) -> list[int]:
    """
    Calculate PER-HIT damage rolls. For multi-hit moves, these are the rolls
    for a single hit. Use get_hit_info() + combine_multi_hit_rolls() or
    calc_matchup() for total damage from a full attack.
    """
    if field is None:
        field = Field()

    mv = get_move(move)
    move_type = _norm(mv["type"])
    power = mv.get("power", 0) or 0
    category = mv.get("category", move_category(mv["type"]))
    move_name = _norm(mv.get("name", ""))

    _kwargs = dict(
        atk_ivs=atk_ivs, def_ivs=def_ivs, atk_level=atk_level,
        def_level=def_level, atk_ability=atk_ability, def_ability=def_ability,
        field=field, critical=critical, atk_status=atk_status,
        def_status=def_status, flash_fire_active=flash_fire_active,
        stockpile_count=stockpile_count, charge_active=charge_active,
        double_dmg=double_dmg, atk_boosts=atk_boosts, def_boosts=def_boosts,
        atk_current_hp=atk_current_hp, def_current_hp=def_current_hp,
    )

    atk = _extract(attacker, species_map, ivs=atk_ivs, level=atk_level,
                   ability_override=atk_ability)
    dfn = _extract(defender, species_map, ivs=def_ivs, level=def_level,
                   ability_override=def_ability)

    level = atk["level"]

    atk_max_hp = atk["stats"]["hp"]
    def_max_hp = dfn["stats"]["hp"]
    atk_hp = atk_current_hp if atk_current_hp is not None else atk_max_hp
    def_hp = def_current_hp if def_current_hp is not None else def_max_hp

    # -- Type effectiveness ----------------------------------------------------
    typeEffect1 = _TYPE_CHART.get(
        (move_type, _norm(dfn["types"][0])), 1.0) if dfn["types"] else 1.0
    typeEffect2 = _TYPE_CHART.get(
        (move_type, _norm(dfn["types"][1])), 1.0) if len(dfn["types"]) > 1 else 1.0
    type_eff = typeEffect1 * typeEffect2

    # -- Fixed-damage moves ----------------------------------------------------

    if move_name == "dragonrage":
        return [0] * 16 if type_eff == 0 else [40] * 16
    if move_name == "sonicboom":
        return [0] * 16 if type_eff == 0 else [20] * 16
    if move_name in ("seismictoss", "nightshade"):
        return [0] * 16 if type_eff == 0 else [level] * 16
    if move_name == "superfang":
        return [0] * 16 if type_eff == 0 else [max(1, def_hp // 2)] * 16
    if move_name == "endeavor":
        return [0] * 16 if type_eff == 0 else [max(0, def_hp - atk_hp)] * 16
    if move_name == "psywave":
        if type_eff == 0:
            return [0] * 11
        return [max(1, level * (i * 10 + 50) // 100) for i in range(11)]

    # -- Magnitude -------------------------------------------------------------
    if move_name == "magnitude" and power == 0:
        all_rolls = []
        for bp_val, weight in _MAGNITUDE_TABLE:
            mag_mv = dict(mv)
            mag_mv["power"] = bp_val
            sub_rolls = damage_rolls(
                attacker, defender, mag_mv, species_map, **_kwargs)
            all_rolls.extend(sub_rolls * weight)
        return all_rolls

    if move_name == "hiddenpower" and power == 0:
        return [0] * 16

    # -- Spit Up ---------------------------------------------------------------
    is_spit_up = (move_name == "spitup")
    if is_spit_up:
        if stockpile_count <= 0:
            return [0] * 16
        power = 100 * stockpile_count

    if power == 0 and not is_spit_up:
        return [0] * 16

    # -- Variable base power ---------------------------------------------------

    if move_name in ("flail", "reversal"):
        p = 48 * atk_hp // atk_max_hp
        power = (200 if p <= 1 else 150 if p <= 4 else 100 if p <= 9
                 else 80 if p <= 16 else 40 if p <= 32 else 20)

    if move_name in ("eruption", "waterspout"):
        power = max(1, 150 * atk_hp // atk_max_hp)

    if move_name in ("lowkick", "grassknot"):
        w = _get_weight_kg(defender, species_map)
        power = (120 if w >= 200 else 100 if w >= 100 else 80 if w >= 50
                 else 60 if w >= 25 else 40 if w >= 10 else 20)

    if move_name == "facade":
        power = 140 if atk_status in ("burn", "poison", "paralysis") else 70

    if move_name == "smellingsalt":
        power = 120 if def_status == "paralysis" else 60

    # -- Weather Ball type change ----------------------------------------------
    weather = "none" if field.cloud_nine else _norm(field.weather)
    is_weather_ball = (move_name == "weatherball")
    if is_weather_ball:
        move_type = {
            "sun": "fire", "rain": "water", "sand": "rock", "hail": "ice",
        }.get(weather, "normal")
        category = move_category(move_type)
        typeEffect1 = _TYPE_CHART.get(
            (move_type, _norm(dfn["types"][0])), 1.0) if dfn["types"] else 1.0
        typeEffect2 = _TYPE_CHART.get(
            (move_type, _norm(dfn["types"][1])), 1.0
        ) if len(dfn["types"]) > 1 else 1.0
        type_eff = typeEffect1 * typeEffect2

    # -- Ability immunities ----------------------------------------------------
    def_ab = dfn["ability"]
    if def_ab == "flashfire" and move_type == "fire":
        return [0] * 16
    if def_ab == "levitate" and move_type == "ground":
        return [0] * 16
    if def_ab == "voltabsorb" and move_type == "electric":
        return [0] * 16
    if def_ab == "waterabsorb" and move_type == "water":
        return [0] * 16
    if def_ab == "wonderguard" and type_eff <= 1.0:
        return [0] * 16
    if def_ab == "soundproof" and move_name in _SOUND_MOVES:
        return [0] * 16
    if type_eff == 0:
        return [0] * 16

    # -- A and D stats (turskain ordering) -------------------------------------
    is_physical = (category == "physical")
    at = atk["stats"]["atk"] if is_physical else atk["stats"]["spa"]
    df = dfn["stats"]["def"] if is_physical else dfn["stats"]["spd"]

    atk_ab = atk["ability"]
    atk_item = atk["item"]
    def_item = dfn["item"]

    # Huge Power / Pure Power
    if is_physical and atk_ab in ("hugepower", "purepower"):
        at *= 2

    # Item boosts on attack stat (mutually exclusive)
    boosted_type = _TYPE_BOOST_ITEMS.get(atk_item)
    if (atk_item != "seaincense" and boosted_type
            and _norm(boosted_type) == move_type):
        at = at * 110 // 100
    elif atk_item == "seaincense" and move_type == "water":
        at = at * 105 // 100
    elif ((is_physical and atk_item == "choiceband")
          or (not is_physical and atk_item == "souldew"
              and atk["species"] in ("latios", "latias"))):
        at = at * 3 // 2
    elif ((not is_physical and atk_item == "deepseatooth"
           and atk["species"] == "clamperl")
          or (not is_physical and atk_item == "lightball"
              and atk["species"] == "pikachu")
          or (is_physical and atk_item == "thickclub"
              and atk["species"] in ("cubone", "marowak"))):
        at *= 2

    # Item boosts on defense stat
    if (not is_physical and def_item == "souldew"
            and dfn["species"] in ("latios", "latias")):
        df = df * 3 // 2
    elif ((not is_physical and def_item == "deepseascale"
           and dfn["species"] == "clamperl")
          or (is_physical and def_item == "metalpowder"
              and dfn["species"] == "ditto")):
        df *= 2

    # Thick Fat / Marvel Scale
    if def_ab == "thickfat" and move_type in ("fire", "ice"):
        at = at // 2
    elif is_physical and def_ab == "marvelscale" and def_status is not None:
        df = df * 3 // 2

    # Hustle / Guts / Plus / Minus -- OR pinch abilities (mutually exclusive)
    if ((is_physical and (atk_ab == "hustle"
                          or (atk_ab == "guts" and atk_status is not None)))
            or (not is_physical and atk_ab in ("plus", "minus"))):
        at = at * 3 // 2
    elif atk_hp * 3 <= atk_max_hp:
        pinch_type = _PINCH_ABILITIES.get(atk_ab)
        if pinch_type and _norm(pinch_type) == move_type:
            power = power * 3 // 2

    # Explosion / Self-Destruct: halve defense
    is_explosion = move_name in ("explosion", "selfdestruct")
    if is_explosion:
        df = df // 2

    # Stat boosts (applied AFTER ability/item mods, matching turskain)
    is_critical = critical and def_ab not in ("battlearmor", "shellarmor")

    atk_stage = (atk_boosts or {}).get("atk" if is_physical else "spa", 0)
    def_stage = (def_boosts or {}).get("def" if is_physical else "spd", 0)

    if atk_stage > 0 or (not is_critical and atk_stage < 0):
        at = apply_stage(at, atk_stage)
    if def_stage < 0 or (not is_critical and def_stage > 0):
        df = apply_stage(df, def_stage)

    # -- Base damage -----------------------------------------------------------
    if df == 0:
        df = 1
    base = ((2 * level // 5 + 2) * at * power // df) // 50

    # -- Modifier chain (strict turskain order) --------------------------------

    # Burn
    if atk_status == "burn" and is_physical and atk_ab != "guts":
        base = base // 2

    # Screen (Reflect / Light Screen)
    has_screen = ((is_physical and field.reflect)
                  or (not is_physical and field.light_screen))
    if has_screen and not is_critical:
        if field.is_doubles:
            base = base * 2 // 3
        else:
            base = base // 2

    # Spread (auto-detect from move name in doubles)
    if field.is_doubles and move_name in _SPREAD_MOVES:
        base = base // 2

    # Weather
    if weather == "rain":
        if move_type == "water":
            base = base * 3 // 2
        elif move_type == "fire":
            base = base // 2
    elif weather == "sun":
        if move_type == "fire":
            base = base * 3 // 2
        elif move_type == "water":
            base = base // 2

    # SolarBeam halved in non-sun non-clear weather
    if move_name == "solarbeam" and weather in ("rain", "sand", "hail"):
        base = base // 2

    # Flash Fire
    if flash_fire_active and move_type == "fire" and atk_ab == "flashfire":
        base = base * 3 // 2

    # +2 (with safety floor)
    base = max(1, base) + 2

    # Critical
    if is_critical:
        base *= 2

    # Weather Ball x2 in non-clear weather
    if is_weather_ball and weather != "none":
        base *= 2

    # DoubleDmg (Pursuit switch, Stomp+Minimize, etc.)
    if double_dmg:
        base *= 2

    # Charge
    if charge_active and move_type == "electric":
        base *= 2

    # Helping Hand
    if field.helping_hand:
        base = base * 3 // 2

    # STAB
    if move_type in [_norm(t) for t in atk["types"]]:
        base = base * 3 // 2

    # Type effectiveness (per type for correct truncation)
    for dt in dfn["types"]:
        mult = _TYPE_CHART.get((move_type, _norm(dt)), 1.0)
        if mult == 2.0:
            base *= 2
        elif mult == 0.5:
            base = base // 2
        elif mult == 0.0:
            return [0] * 16

    # Random: x(85..100) // 100  (Spit Up: always 100, no randomness)
    if is_spit_up:
        return [max(1, base)] * 16

    rolls = []
    for r in range(85, 101):
        dmg = (base * r) // 100
        rolls.append(max(1, dmg) if base > 0 else 0)
    return rolls


# -- KO probability ------------------------------------------------------------

def ko_chance(
    rolls: list[int],
    hp: int,
    *,
    max_hp: int = None,
    max_hits: int = 8,
    recovery: int = 0,
) -> dict[int, float]:
    """
    Compute probability of KOing in n attacks (1..max_hits).
    Each "attack" uses the full rolls list (which may already be combined
    multi-hit rolls from combine_multi_hit_rolls()).
    """
    if max_hp is None:
        max_hp = hp

    if all(r == 0 for r in rolls):
        return {i: 0.0 for i in range(1, max_hits + 1)}

    n_rolls = len(rolls)
    dist: dict[int, float] = {hp: 1.0}
    result: dict[int, float] = {}

    for hit in range(1, max_hits + 1):
        new_dist: dict[int, float] = {}

        for current_hp, prob in dist.items():
            if current_hp <= 0:
                new_dist[0] = new_dist.get(0, 0.0) + prob
                continue
            for roll in rolls:
                new_hp = max(0, current_hp - roll)
                p = prob / n_rolls
                new_dist[new_hp] = new_dist.get(new_hp, 0.0) + p

        ko_prob = new_dist.get(0, 0.0)
        result[hit] = ko_prob

        if ko_prob >= 1.0 - 1e-12:
            result[hit] = 1.0
            break

        if recovery != 0 and hit < max_hits:
            recovered: dict[int, float] = {}
            for rem_hp, prob in new_dist.items():
                if rem_hp <= 0:
                    recovered[0] = recovered.get(0, 0.0) + prob
                else:
                    new_hp = max(1, min(max_hp, rem_hp + recovery))
                    recovered[new_hp] = recovered.get(new_hp, 0.0) + prob
            new_dist = recovered

        dist = new_dist

    return result


# -- HP-dependent moves (skip KO calc) ----------------------------------------

_HP_DEPENDENT_MOVES = frozenset({"superfang", "endeavor"})


# -- calc_matchup --------------------------------------------------------------

def calc_matchup(
    attacker, defender, move,
    species_map: dict,
    **kwargs,
) -> dict:
    """
    Full matchup summary with multi-hit support.

    For multi-hit moves, per_hit_rolls are per-hit values, and ko_chances
    use properly combined attack totals.
    """
    recovery = kwargs.pop("recovery", 0)
    max_hits = kwargs.pop("max_hits", 8)

    per_hit_rolls = damage_rolls(
        attacker, defender, move, species_map, **kwargs)

    mv = get_move(move)
    move_name = _norm(mv.get("name", ""))
    hit_info = get_hit_info(move)

    dfn = _extract(
        defender, species_map,
        ivs=kwargs.get("def_ivs", 31),
        level=kwargs.get("def_level", 100),
        ability_override=kwargs.get("def_ability"),
    )
    max_hp = dfn["stats"]["hp"]
    hp = kwargs.get("def_current_hp") or max_hp

    # Combine rolls for multi-hit
    if hit_info["type"] == "single":
        attack_rolls = per_hit_rolls
    elif hit_info["type"] == "triple_kick":
        # Special: compute per-kick rolls at each power, then convolve
        kick_rolls_list = []
        for kick_power in _TRIPLE_KICK_POWERS:
            kick_mv = dict(mv)
            kick_mv["power"] = kick_power
            kick_rolls_list.append(
                damage_rolls(attacker, defender, kick_mv, species_map, **kwargs)
            )
        dist = {0: 1}
        for kr in kick_rolls_list:
            dist = _convolve_once(dist, kr)
        n = 1
        for kr in kick_rolls_list:
            n *= len(kr)
        attack_rolls = _expand_dist(dist, n)
    else:
        attack_rolls = combine_multi_hit_rolls(per_hit_rolls, hit_info)

    min_dmg, max_dmg = min(attack_rolls), max(attack_rolls)
    min_pct = round(min_dmg / max_hp * 100, 1) if max_hp else 0
    max_pct = round(max_dmg / max_hp * 100, 1) if max_hp else 0

    if move_name in _HP_DEPENDENT_MOVES:
        ko = {}
    else:
        ko = ko_chance(attack_rolls, hp, max_hp=max_hp,
                       max_hits=max_hits, recovery=recovery)

    return {
        "rolls": per_hit_rolls,
        "attack_rolls": attack_rolls if hit_info["type"] != "single" else None,
        "hit_info": hit_info,
        "min": min_dmg,
        "max": max_dmg,
        "min_pct": min_pct,
        "max_pct": max_pct,
        "defender_hp": hp,
        "defender_max_hp": max_hp,
        "ko_chances": ko,
    }


def format_result(result: dict, move_name: str = "Move") -> str:
    r = result
    hi = r.get("hit_info", {"type": "single"})

    per_hit = r["rolls"]
    n = len(per_hit)
    if n <= 16:
        rolls_str = ", ".join(str(d) for d in per_hit)
    else:
        rolls_str = (f"{len(set(per_hit))} unique values, "
                     f"{min(per_hit)}-{max(per_hit)}")

    if hi["type"] == "fixed":
        hit_label = f" (x{hi['hits']} hits)"
    elif hi["type"] == "variable":
        hit_label = " (2-5 hits)"
    elif hi["type"] == "triple_kick":
        hit_label = " (Triple Kick: 10+20+30)"
    else:
        hit_label = ""

    lines = [
        f"  {move_name}{hit_label}: {r['min']}-{r['max']} "
        f"({r['min_pct']}% - {r['max_pct']}%) "
        f"[HP: {r['defender_hp']}]",
        f"  Per-hit rolls: ({rolls_str})",
    ]

    for n_hit, prob in sorted(r["ko_chances"].items()):
        pct = prob * 100
        if pct >= 100 - 1e-9:
            lines.append(f"  guaranteed {n_hit}HKO")
            break
        elif pct > 0:
            lines.append(f"  {pct:.1f}% chance to {n_hit}HKO")
    if not r["ko_chances"]:
        lines.append("  (KO calc N/A -- damage depends on current HP)")
    return "\n".join(lines)