"""
damagecalc.py — Gen 3 (ADV) damage calculator for Battle Frontier analysis.

Provides:
    damage_rolls()   — possible damage values for a given attack
    ko_chance()      — probability of n-HKO given rolls and defender HP
    calc_matchup()   — convenience wrapper returning a full summary dict
    format_result()  — pretty-print a matchup result

Ordering and mechanics matched against turskain's CALCULATE_DAMAGE_ADV.
Move data can be supplied as dicts or loaded from Data/moves.json.

Dependencies: frontierutils only (no frontier_db).
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from frontierutils import (
    _norm, calc_stats, apply_stage, move_category,
    type_effectiveness, _TYPE_CHART,
    CustomSet, POKEMON_FILE,
)

# ── Item and ability lookups ──────────────────────────────────────────────────

# Gen 3 type-boosting held items → boosted type
# In Gen 3, these boost the ATTACK STAT by 1.1× (not base power like Gen 4+)
_TYPE_BOOST_ITEMS: dict[str, str] = {
    "silkscarf": "normal", "blackbelt": "fighting", "poisonbarb": "poison",
    "softsand": "ground", "sharpbeak": "flying", "silverpowder": "bug",
    "hardstone": "rock", "spelltag": "ghost", "metalcoat": "steel",
    "charcoal": "fire", "mysticwater": "water", "magnet": "electric",
    "miracleseed": "grass", "nevermeltice": "ice", "twistedspoon": "psychic",
    "dragonfang": "dragon", "blackglasses": "dark",
}

# Pinch abilities → boosted type (activate at ≤1/3 HP, 1.5× base power)
_PINCH_ABILITIES: dict[str, str] = {
    "overgrow": "grass", "blaze": "fire", "torrent": "water", "swarm": "bug",
}

# Magnitude: (base_power, weight) — weights sum to 20 for clean probability
_MAGNITUDE_TABLE = [
    (10, 1), (30, 2), (50, 4), (70, 6), (90, 4), (110, 2), (150, 1),
]


# ── Move data loading ─────────────────────────────────────────────────────────

_MOVES_FILE = Path(__file__).parent / "Data" / "moves.json"
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
            f"or ensure Data/moves.json exists and contains it."
        )
    m = dict(moves_db[name])
    m.setdefault("category", move_category(m["type"]))
    return m


# ── Field conditions ──────────────────────────────────────────────────────────

@dataclass
class Field:
    weather: str = "none"       # "sun", "rain", "sand", "hail", "none"
    reflect: bool = False       # on defender's side
    light_screen: bool = False  # on defender's side
    is_doubles: bool = False
    is_multi_target: bool = False
    helping_hand: bool = False
    cloud_nine: bool = False


# ── Combatant extraction ──────────────────────────────────────────────────────

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
    """Get defender's weight in kg from hectograms in data."""
    if isinstance(defender, CustomSet):
        dex_entry = next(
            (p for p in species_map.values() if _norm(p["name"]) == _norm(defender.pokemon)),
            None,
        )
        return (dex_entry.get("weight", 0) if dex_entry else 0) / 10
    dex = defender.get("DexNum")
    return species_map.get(dex, {}).get("weight", 0) / 10


# ── Core damage formula ──────────────────────────────────────────────────────

def _fl(val):
    """int floor — identity for ints, floor for floats."""
    return int(val) if isinstance(val, float) and val >= 0 else val


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
    atk_status: str = None,       # "burn", "poison", "paralysis"
    def_status: str = None,
    flash_fire_active: bool = False,
    stockpile_count: int = 0,
    charge_active: bool = False,
    double_dmg: bool = False,     # Pursuit switch, Stomp+Minimize, etc.
    atk_boosts: dict = None,
    def_boosts: dict = None,
    atk_current_hp: int = None,
    def_current_hp: int = None,
) -> list[int]:
    """
    Calculate possible damage rolls for a Gen 3 attack.
    Returns 16 values for normal moves, 11 for Psywave, 320 for Magnitude.
    """
    if field is None:
        field = Field()

    mv = get_move(move)
    move_type = _norm(mv["type"])
    power = mv.get("power", 0) or 0
    category = mv.get("category", move_category(mv["type"]))
    move_name = _norm(mv.get("name", ""))

    # Shared kwargs for recursive calls (Magnitude)
    _kwargs = dict(
        atk_ivs=atk_ivs, def_ivs=def_ivs, atk_level=atk_level,
        def_level=def_level, atk_ability=atk_ability, def_ability=def_ability,
        field=field, critical=critical, atk_status=atk_status,
        def_status=def_status, flash_fire_active=flash_fire_active,
        stockpile_count=stockpile_count, charge_active=charge_active,
        double_dmg=double_dmg, atk_boosts=atk_boosts, def_boosts=def_boosts,
        atk_current_hp=atk_current_hp, def_current_hp=def_current_hp,
    )

    # ── Extract combatants ────────────────────────────────────────────────
    atk = _extract(attacker, species_map, ivs=atk_ivs, level=atk_level,
                   ability_override=atk_ability)
    dfn = _extract(defender, species_map, ivs=def_ivs, level=def_level,
                   ability_override=def_ability)

    level = atk["level"]

    # ── Resolve current/max HP ────────────────────────────────────────────
    atk_max_hp = atk["stats"]["hp"]
    def_max_hp = dfn["stats"]["hp"]
    atk_hp = atk_current_hp if atk_current_hp is not None else atk_max_hp
    def_hp = def_current_hp if def_current_hp is not None else def_max_hp

    # ── Type effectiveness (needed for immunity checks) ───────────────────
    typeEffect1 = _TYPE_CHART.get((move_type, _norm(dfn["types"][0])), 1.0) if dfn["types"] else 1.0
    typeEffect2 = _TYPE_CHART.get((move_type, _norm(dfn["types"][1])), 1.0) if len(dfn["types"]) > 1 else 1.0
    type_eff = typeEffect1 * typeEffect2

    # ── Fixed-damage moves (bypass formula) ───────────────────────────────

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

    # ── Magnitude: 7 BPs × 16 rolls = 320 weighted rolls ─────────────────
    if move_name == "magnitude" and power == 0:
        all_rolls = []
        for bp_val, weight in _MAGNITUDE_TABLE:
            mag_mv = dict(mv)
            mag_mv["power"] = bp_val
            sub_rolls = damage_rolls(attacker, defender, mag_mv, species_map, **_kwargs)
            all_rolls.extend(sub_rolls * weight)
        return all_rolls

    # ── Hidden Power: user must set type/power in move dict ───────────────
    # Default power 0 → returns [0]*16 unless overridden
    if move_name == "hiddenpower" and power == 0:
        return [0] * 16

    # ── Zero BP catchall (status moves, etc.) ─────────────────────────────
    if power == 0 and move_name not in ("spitup",):
        return [0] * 16

    # ── Variable base power moves ─────────────────────────────────────────

    # Spit Up: BP = 100 × stockpile count, random roll fixed at 100
    is_spit_up = (move_name == "spitup")
    if is_spit_up:
        if stockpile_count <= 0:
            return [0] * 16
        power = 100 * stockpile_count

    # Flail / Reversal: Gen 3 uses floor(48 * curHP / maxHP)
    if move_name in ("flail", "reversal"):
        p = 48 * atk_hp // atk_max_hp
        power = 200 if p <= 1 else 150 if p <= 4 else 100 if p <= 9 else 80 if p <= 16 else 40 if p <= 32 else 20

    # Eruption / Water Spout
    if move_name in ("eruption", "waterspout"):
        power = max(1, 150 * atk_hp // atk_max_hp)

    # Low Kick / Grass Knot: weight-based
    if move_name in ("lowkick", "grassknot"):
        w = _get_weight_kg(defender, species_map)
        power = 120 if w >= 200 else 100 if w >= 100 else 80 if w >= 50 else 60 if w >= 25 else 40 if w >= 10 else 20

    # Facade: doubles BP if user is poisoned, burned, or paralyzed
    if move_name == "facade" and atk_status in ("burn", "poison", "paralysis"):
        power = 140
    elif move_name == "facade":
        power = 70

    # SmellingSalt: doubles BP if target is paralyzed
    if move_name == "smellingsalt":
        power = 120 if def_status == "paralysis" else 60

    # Weather Ball: type changes based on weather, ×2 applied later as DoubleDmg
    weather = "none" if field.cloud_nine else _norm(field.weather)
    is_weather_ball = (move_name == "weatherball")
    if is_weather_ball:
        if weather == "sun":
            move_type = "fire"
        elif weather == "rain":
            move_type = "water"
        elif weather == "sand":
            move_type = "rock"
        elif weather == "hail":
            move_type = "ice"
        else:
            move_type = "normal"
        category = move_category(move_type)
        # Recalculate type effectiveness with new type
        typeEffect1 = _TYPE_CHART.get((move_type, _norm(dfn["types"][0])), 1.0) if dfn["types"] else 1.0
        typeEffect2 = _TYPE_CHART.get((move_type, _norm(dfn["types"][1])), 1.0) if len(dfn["types"]) > 1 else 1.0
        type_eff = typeEffect1 * typeEffect2

    # ── Ability immunities ────────────────────────────────────────────────
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
    if def_ab == "soundproof" and mv.get("isSound", False):
        return [0] * 16

    if type_eff == 0:
        return [0] * 16

    # ── Determine A (attack) and D (defense) ──────────────────────────────
    # Matches turskain ordering exactly
    is_physical = (category == "physical")
    at = atk["stats"]["atk"] if is_physical else atk["stats"]["spa"]
    df = dfn["stats"]["def"] if is_physical else dfn["stats"]["spd"]

    atk_ab = atk["ability"]
    atk_item = atk["item"]
    def_item = dfn["item"]

    # 1. Huge Power / Pure Power
    if is_physical and atk_ab in ("hugepower", "purepower"):
        at *= 2

    # 2. Item boosts on attack stat (mutually exclusive)
    # Gen 3: type-boosting items boost the STAT by 1.1× (not base power)
    boosted_type = _TYPE_BOOST_ITEMS.get(atk_item)
    if atk_item != "seaincense" and boosted_type and _norm(boosted_type) == move_type:
        at = at * 110 // 100
    elif atk_item == "seaincense" and move_type == "water":
        at = at * 105 // 100
    elif (is_physical and atk_item == "choiceband") or \
         (not is_physical and atk_item == "souldew" and atk["species"] in ("latios", "latias")):
        at = at * 3 // 2
    elif (not is_physical and atk_item == "deepseatooth" and atk["species"] == "clamperl") or \
         (not is_physical and atk_item == "lightball" and atk["species"] == "pikachu") or \
         (is_physical and atk_item == "thickclub" and atk["species"] in ("cubone", "marowak")):
        at *= 2

    # 3. Item boosts on defense stat (mutually exclusive)
    if not is_physical and def_item == "souldew" and dfn["species"] in ("latios", "latias"):
        df = df * 3 // 2
    elif (not is_physical and def_item == "deepseascale" and dfn["species"] == "clamperl") or \
         (is_physical and def_item == "metalpowder" and dfn["species"] == "ditto"):
        df *= 2

    # 4. Thick Fat / Marvel Scale
    if def_ab == "thickfat" and move_type in ("fire", "ice"):
        at = at // 2
    elif is_physical and def_ab == "marvelscale" and def_status is not None:
        df = df * 3 // 2

    # 5. Hustle / Guts / Plus / Minus — OR pinch abilities (mutually exclusive)
    if (is_physical and (atk_ab == "hustle" or (atk_ab == "guts" and atk_status is not None))) or \
       (not is_physical and atk_ab in ("plus", "minus")):
        at = at * 3 // 2
    elif atk_hp * 3 <= atk_max_hp:
        pinch_type = _PINCH_ABILITIES.get(atk_ab)
        if pinch_type and _norm(pinch_type) == move_type:
            power = power * 3 // 2

    # 6. Explosion / Self-Destruct: halve defense
    is_explosion = move_name in ("explosion", "selfdestruct")
    if is_explosion:
        df = df // 2

    # 7. Stat boosts (after all ability/item mods, matching turskain)
    is_critical = critical and def_ab not in ("battlearmor", "shellarmor")

    atk_stage = (atk_boosts or {}).get("atk" if is_physical else "spa", 0)
    def_stage = (def_boosts or {}).get("def" if is_physical else "spd", 0)

    if atk_stage > 0 or (not is_critical and atk_stage < 0):
        at = apply_stage(at, atk_stage)
    if def_stage < 0 or (not is_critical and def_stage > 0):
        df = apply_stage(df, def_stage)

    # ── Base damage ───────────────────────────────────────────────────────
    if df == 0:
        df = 1
    base = ((2 * level // 5 + 2) * at * power // df) // 50

    # ── Modifier chain (strict order from turskain) ───────────────────────

    # 1. Burn
    if atk_status == "burn" and is_physical and atk_ab != "guts":
        base = base // 2

    # 2. Screen (Reflect / Light Screen)
    has_screen = (is_physical and field.reflect) or (not is_physical and field.light_screen)
    if has_screen and not is_critical:
        if field.is_doubles:
            base = base * 2 // 3
        else:
            base = base // 2

    # 3. Targets (spread in doubles)
    if field.is_doubles and field.is_multi_target and not is_explosion:
        base = base // 2

    # 4. Weather
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

    # SolarBeam halved in non-sun, non-clear weather
    if move_name == "solarbeam" and weather in ("rain", "sand", "hail"):
        base = base // 2

    # 5. Flash Fire
    if flash_fire_active and move_type == "fire" and atk_ab == "flashfire":
        base = base * 3 // 2

    # +2 (with safety floor)
    base = max(1, base) + 2

    # 6. Stockpile (Spit Up multiplier already applied to power)
    # (no-op here since we set power = 100 * count above)

    # 7. Critical
    if is_critical:
        base *= 2

    # 8. DoubleDmg (Pursuit switch, Stomp+Minimize, Weather Ball in weather, etc.)
    if is_weather_ball and weather != "none":
        base *= 2
    if double_dmg:
        base *= 2

    # 9. Charge
    if charge_active and move_type == "electric":
        base *= 2

    # 10. Helping Hand
    if field.helping_hand:
        base = base * 3 // 2

    # 11. STAB
    if move_type in [_norm(t) for t in atk["types"]]:
        base = base * 3 // 2

    # 12–13. Type effectiveness (applied per type for correct truncation)
    for dt in dfn["types"]:
        mult = _TYPE_CHART.get((move_type, _norm(dt)), 1.0)
        if mult == 2.0:
            base *= 2
        elif mult == 0.5:
            base = base // 2
        elif mult == 0.0:
            return [0] * 16

    # 14. Random: ×(85..100) // 100  (Spit Up: always 100, no randomness)
    if is_spit_up:
        return [max(1, base)] * 16

    rolls = []
    for r in range(85, 101):
        dmg = (base * r) // 100
        rolls.append(max(1, dmg) if base > 0 else 0)

    return rolls


# ── KO probability calculation ────────────────────────────────────────────────

def ko_chance(
    rolls: list[int],
    hp: int,
    *,
    max_hp: int = None,
    max_hits: int = 8,
    recovery: int = 0,
) -> dict[int, float]:
    """
    Compute the probability of KOing in n hits (1..max_hits).
    Uses exact convolution over the damage rolls.
    Handles variable-length roll lists (16 for normal, 11 for Psywave, 320 for Magnitude).
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


# ── Moves whose damage depends on current HP ─────────────────────────────────

_HP_DEPENDENT_MOVES = frozenset({"superfang", "endeavor"})


# ── High-level convenience ────────────────────────────────────────────────────

def calc_matchup(
    attacker, defender, move,
    species_map: dict,
    **kwargs,
) -> dict:
    """Full matchup summary."""
    recovery = kwargs.pop("recovery", 0)
    max_hits = kwargs.pop("max_hits", 8)

    rolls = damage_rolls(attacker, defender, move, species_map, **kwargs)

    mv = get_move(move)
    move_name = _norm(mv.get("name", ""))

    dfn = _extract(
        defender, species_map,
        ivs=kwargs.get("def_ivs", 31),
        level=kwargs.get("def_level", 100),
        ability_override=kwargs.get("def_ability"),
    )
    max_hp = dfn["stats"]["hp"]
    hp = kwargs.get("def_current_hp") or max_hp

    min_dmg, max_dmg = min(rolls), max(rolls)
    min_pct = round(min_dmg / max_hp * 100, 1) if max_hp else 0
    max_pct = round(max_dmg / max_hp * 100, 1) if max_hp else 0

    if move_name in _HP_DEPENDENT_MOVES:
        ko = {}
    else:
        ko = ko_chance(rolls, hp, max_hp=max_hp, max_hits=max_hits, recovery=recovery)

    return {
        "rolls": rolls,
        "min": min_dmg,
        "max": max_dmg,
        "min_pct": min_pct,
        "max_pct": max_pct,
        "defender_hp": hp,
        "defender_max_hp": max_hp,
        "ko_chances": ko,
    }


def format_result(result: dict, move_name: str = "Move") -> str:
    """Pretty-print a calc_matchup() result dict."""
    r = result
    n_rolls = len(r["rolls"])
    if n_rolls <= 16:
        rolls_str = ", ".join(str(d) for d in r["rolls"])
    else:
        # Magnitude etc: show min–max and unique sorted values
        unique = sorted(set(r["rolls"]))
        rolls_str = f"{len(unique)} unique values, {r['min']}-{r['max']}"
    lines = [
        f"  {move_name}: {r['min']}-{r['max']} "
        f"({r['min_pct']}% - {r['max_pct']}%) "
        f"[HP: {r['defender_hp']}]",
        f"  Rolls: ({rolls_str})",
    ]
    for n, prob in sorted(r["ko_chances"].items()):
        pct = prob * 100
        if pct >= 100 - 1e-9:
            lines.append(f"  guaranteed {n}HKO")
            break
        elif pct > 0:
            lines.append(f"  {pct:.1f}% chance to {n}HKO")
    if not r["ko_chances"]:
        lines.append("  (KO calc N/A — damage depends on current HP)")
    return "\n".join(lines)