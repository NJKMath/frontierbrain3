"""
frontierutils.py — Shared utilities for Battle Frontier analysis.

Contains:
    - String normalization
    - Nature data and stat calculations
    - Type chart and effectiveness
    - CustomSet class
    - Pokepaste import/export
"""

import json
import re
import tkinter as tk
from pathlib import Path

# ── File paths ────────────────────────────────────────────────────────────────

_DATA         = Path(__file__).parent / "Data"
SETS_FILE     = _DATA / "bf_pokemon.json"
TRAINERS_FILE = _DATA / "bf_trainers.json"
POKEMON_FILE  = _DATA / "pokemon.json"


# ── Normalization ─────────────────────────────────────────────────────────────

def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())

def _set_id(s: dict) -> str:
    return f"{s['Pokemon']}-{s['SetNum']}"


# ── Nature modifiers ──────────────────────────────────────────────────────────

_NATURE_MODS = {
    "hardy":   None, "lonely":  ("atk", "def"), "brave":   ("atk", "spe"),
    "adamant": ("atk", "spa"), "naughty": ("atk", "spd"), "bold":    ("def", "atk"),
    "docile":  None, "relaxed": ("def", "spe"), "impish":  ("def", "spa"),
    "lax":     ("def", "spd"), "timid":   ("spe", "atk"), "hasty":   ("spe", "def"),
    "serious": None, "jolly":   ("spe", "spa"), "naive":   ("spe", "spd"),
    "modest":  ("spa", "atk"), "mild":    ("spa", "def"), "quiet":   ("spa", "spe"),
    "bashful": None, "rash":    ("spa", "spd"), "calm":    ("spd", "atk"),
    "gentle":  ("spd", "def"), "sassy":   ("spd", "spe"), "careful": ("spd", "spa"),
    "quirky":  None,
}

STAT_KEYS = ["hp", "atk", "def", "spa", "spd", "spe"]


# ── Stat stage multipliers ────────────────────────────────────────────────────
# Gen 3: stage +N → multiply by (2+N)/2, stage -N → multiply by 2/(2+N).

_STAGE_NUMERATORS   = {-6:2, -5:2, -4:2, -3:2, -2:2, -1:2, 0:2, 1:3, 2:4, 3:5, 4:6, 5:7, 6:8}
_STAGE_DENOMINATORS = {-6:8, -5:7, -4:6, -3:5, -2:4, -1:3, 0:2, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2}


def apply_stage(stat: int, stage: int) -> int:
    """Apply a stat stage modifier (-6..+6) to a stat value."""
    stage = max(-6, min(6, stage))
    return stat * _STAGE_NUMERATORS[stage] // _STAGE_DENOMINATORS[stage]


# ── Stat calculation ──────────────────────────────────────────────────────────

def calc_stats(s: dict, species_map: dict,
               ivs: int | list[int] = 31, level: int = 100) -> dict:
    """
    Calculate a set's stats given IVs and level.
    ivs can be a single int (all stats equal) or a list of 6 ints [hp,atk,def,spa,spd,spe].
    """
    dex     = s.get("DexNum")
    bases   = species_map.get(dex, {}).get("stats", {})
    evs     = s["EVs"]
    iv_list = ivs if isinstance(ivs, list) else [ivs] * 6
    mods    = _NATURE_MODS.get(_norm(s["Nature"]))
    boosted = mods[0] if mods else None
    reduced = mods[1] if mods else None

    result = {}
    for i, stat in enumerate(STAT_KEYS):
        base = bases.get(stat, 0)
        ev   = evs[i]
        iv   = iv_list[i]
        core = (2 * base + iv + ev // 4) * level // 100
        if stat == "hp":
            result[stat] = core + level + 10
        else:
            nature = 1.1 if stat == boosted else 0.9 if stat == reduced else 1.0
            result[stat] = int((core + 5) * nature)
    return result


# ── Gen 3 physical/special split (by type) ────────────────────────────────────

_PHYSICAL_TYPES = frozenset({
    "normal", "fighting", "poison", "ground",
    "flying", "bug", "rock", "ghost", "steel",
})
_SPECIAL_TYPES = frozenset({
    "fire", "water", "electric", "grass",
    "ice", "psychic", "dragon", "dark",
})


def move_category(move_type: str) -> str:
    t = _norm(move_type)
    if t in _PHYSICAL_TYPES:
        return "physical"
    if t in _SPECIAL_TYPES:
        return "special"
    raise ValueError(f"Unknown type for category lookup: {move_type}")


# ── Gen 3 type effectiveness chart ────────────────────────────────────────────

_TYPE_CHART: dict[tuple[str, str], float] = {}

_RAW_CHART = {
    "normal":   {"rock": .5, "ghost": 0, "steel": .5},
    "fire":     {"fire": .5, "water": .5, "grass": 2, "ice": 2, "bug": 2,
                 "rock": .5, "dragon": .5, "steel": 2},
    "water":    {"fire": 2, "water": .5, "grass": .5, "ground": 2,
                 "rock": 2, "dragon": .5},
    "electric": {"water": 2, "electric": .5, "grass": .5, "ground": 0,
                 "flying": 2, "dragon": .5},
    "grass":    {"fire": .5, "water": 2, "grass": .5, "poison": .5,
                 "ground": 2, "flying": .5, "bug": .5, "rock": 2,
                 "dragon": .5, "steel": .5},
    "ice":      {"fire": .5, "water": .5, "grass": 2, "ice": .5,
                 "ground": 2, "flying": 2, "dragon": 2, "steel": .5},
    "fighting": {"normal": 2, "ice": 2, "poison": .5, "flying": .5,
                 "psychic": .5, "bug": .5, "rock": 2, "ghost": 0,
                 "dark": 2, "steel": 2},
    "poison":   {"grass": 2, "poison": .5, "ground": .5, "rock": .5,
                 "ghost": .5, "steel": 0},
    "ground":   {"fire": 2, "electric": 2, "grass": .5, "poison": 2,
                 "flying": 0, "bug": .5, "rock": 2, "steel": 2},
    "flying":   {"electric": .5, "grass": 2, "fighting": 2, "bug": 2,
                 "rock": .5, "steel": .5},
    "psychic":  {"fighting": 2, "poison": 2, "psychic": .5, "dark": 0,
                 "steel": .5},
    "bug":      {"fire": .5, "grass": 2, "fighting": .5, "poison": .5,
                 "flying": .5, "psychic": 2, "ghost": .5, "dark": 2,
                 "steel": .5},
    "rock":     {"fire": 2, "ice": 2, "fighting": .5, "ground": .5,
                 "flying": 2, "bug": 2, "steel": .5},
    "ghost":    {"normal": 0, "psychic": 2, "ghost": 2, "dark": .5,
                 "steel": .5},
    "dragon":   {"dragon": 2, "steel": .5},
    "dark":     {"fighting": .5, "psychic": 2, "ghost": 2, "dark": .5,
                 "steel": .5},
    "steel":    {"fire": .5, "water": .5, "electric": .5, "ice": 2,
                 "rock": 2, "steel": .5},
}

for atk_t, matchups in _RAW_CHART.items():
    for def_t, mult in matchups.items():
        _TYPE_CHART[(_norm(atk_t), _norm(def_t))] = mult


def type_effectiveness(move_type: str, defender_types: list[str]) -> float:
    """Combined type effectiveness multiplier against a (possibly dual-typed) defender."""
    mt = _norm(move_type)
    eff = 1.0
    for dt in defender_types:
        eff *= _TYPE_CHART.get((mt, _norm(dt)), 1.0)
    return eff


# ── CustomSet ─────────────────────────────────────────────────────────────────

class CustomSet:
    def __init__(self,
                 pokemon:  str,
                 nature:   str             = "hardy",
                 evs:      list[int]       = None,
                 ivs:      int | list[int] = 31,
                 level:    int             = 100,
                 item:     str             = "None",
                 ability:  str             = None,
                 moves:    list[str]       = None,
                 stats:    dict            = None):
        self.pokemon    = pokemon
        self.nature     = nature
        self.evs        = evs or [0] * 6
        self.ivs        = ivs if isinstance(ivs, list) else [ivs] * 6
        self.level      = level
        self.item       = item
        self.moves      = [_norm(m) for m in (moves or [])][:4]
        self._raw_stats = stats

        with open(POKEMON_FILE, encoding="utf-8") as f:
            species_map = {p["id"]: p for p in json.load(f)}

        dex_entry = next(
            (p for p in species_map.values() if _norm(p["name"]) == _norm(pokemon)),
            None
        )
        if dex_entry is None:
            raise ValueError(f"Species '{pokemon}' not found in pokemon data")
        self._dex_id      = dex_entry["id"]
        self._species_map = species_map
        self.ability      = ability if ability else (dex_entry.get("abilities") or [None])[0]

    def get_stats(self) -> dict:
        if self._raw_stats:
            return self._raw_stats
        fake_set = {"DexNum": self._dex_id, "Nature": self.nature, "EVs": self.evs}
        return calc_stats(fake_set, self._species_map, ivs=self.ivs, level=self.level)

    def speed(self) -> int:
        return self.get_stats()["spe"]

    def __repr__(self):
        return f"CustomSet({self.pokemon}, nature={self.nature}, ivs={self.ivs}, level={self.level})"


# ── Pokepaste import ──────────────────────────────────────────────────────────

_PASTE_STAT = {"HP": 0, "Atk": 1, "Def": 2, "SpA": 3, "SpD": 4, "Spe": 5}


def _parse_paste_block(block: str) -> tuple[str, CustomSet]:
    lines = [l.strip() for l in block.strip().splitlines() if l.strip()]

    header = lines[0]
    item   = "None"
    if " @ " in header:
        header, item = header.rsplit(" @ ", 1)
    header  = re.sub(r"\s*\([MF]\)\s*$", "", header).strip()
    m       = re.search(r"\(([^)]+)\)\s*$", header)
    species  = m.group(1) if m else header
    nickname = re.sub(r"\s*\([^)]+\)\s*$", "", header).strip() if m else None

    ability = None
    level   = 100
    nature  = "hardy"
    evs     = [0] * 6
    ivs     = [31] * 6
    moves   = []

    for line in lines[1:]:
        if line.startswith("Ability:"):
            ability = line.split(":", 1)[1].strip()
        elif line.startswith("Level:"):
            level = int(line.split(":", 1)[1].strip())
        elif line.endswith(" Nature"):
            nature = line.replace(" Nature", "").strip()
        elif line.startswith("EVs:"):
            for seg in line.split(":", 1)[1].split("/"):
                seg = seg.strip()
                m2  = re.match(r"(\d+)\s+(\S+)", seg)
                if m2 and m2.group(2) in _PASTE_STAT:
                    evs[_PASTE_STAT[m2.group(2)]] = int(m2.group(1))
        elif line.startswith("IVs:"):
            for seg in line.split(":", 1)[1].split("/"):
                seg = seg.strip()
                m2  = re.match(r"(\d+)\s+(\S+)", seg)
                if m2 and m2.group(2) in _PASTE_STAT:
                    ivs[_PASTE_STAT[m2.group(2)]] = int(m2.group(1))
        elif line.startswith("- "):
            moves.append(line[2:].strip())

    name = nickname if nickname else f"Custom{species}"
    return name, CustomSet(pokemon=species, nature=nature, evs=evs, ivs=ivs,
                           level=level, item=item, ability=ability, moves=moves)


def from_paste(text: str) -> dict[str, CustomSet]:
    blocks = re.split(r"\n{2,}", text.strip())
    result = {}
    for block in blocks:
        if not block.strip():
            continue
        name, cs = _parse_paste_block(block)
        base, n  = name, 1
        while name in result:
            name = f"{base}_{n}"
            n   += 1
        result[name] = cs
    return result


def from_clipboard() -> dict[str, CustomSet]:
    root = tk.Tk()
    root.withdraw()
    text = root.clipboard_get()
    root.destroy()
    return from_paste(text)