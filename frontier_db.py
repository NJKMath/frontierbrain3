"""
frontier_db.py — Database and query/filter collections for Battle Frontier data.

Depends on:
    frontierutils  — shared data, stats, types, CustomSet
    damagecalc     — damage formula (for willOHKO filter)
"""

import json
from pathlib import Path

from frontierutils import (
    _norm, _set_id, calc_stats, CustomSet,
    SETS_FILE, TRAINERS_FILE, POKEMON_FILE,
    # Re-export for backward compatibility
    from_paste, from_clipboard, STAT_KEYS,
    apply_stage, move_category, type_effectiveness,
)


# ── Predicates ────────────────────────────────────────────────────────────────

def _move_pred(s, moves, match):
    set_moves  = set(s["Moves"])
    norm_moves = [_norm(m) for m in moves]
    fn = all if match == "all" else any
    return fn(m in set_moves for m in norm_moves)

def _ability_pred(s, abilities):
    set_abilities = {_norm(a) for a in s["Abilities"]}
    return any(_norm(a) in set_abilities for a in abilities)

def _item_pred(s, items):
    return _norm(s["Item"]) in {_norm(i) for i in items}

def _nature_pred(s, natures):
    return _norm(s["Nature"]) in {_norm(n) for n in natures}

def _type_pred(s, types, species_map):
    """Each arg is a type string:
      'Fire'        — has Fire (pure or dual)
      'Fire/Flying' — has both Fire and Flying
      'Fire/'       — pure Fire only (no second type)
    Multiple args are OR'd together.
    """
    dex = s.get("DexNum")
    if dex is None:
        return False
    pokemon_types = set(species_map.get(dex, {}).get("types", []))
    for t in types:
        if t.endswith("/"):
            if pokemon_types == {_norm(t[:-1])}:
                return True
        else:
            parts = {_norm(p) for p in t.split("/")}
            if parts <= pokemon_types:
                return True
    return False

def _trainer_has_pokemon_pred(t, species):
    norm_species = {_norm(sp) for sp in species}
    return any(_norm(sid.rsplit("-", 1)[0]) in norm_species for sid in t["Sets"])

def _trainer_has_set_pred(t, set_ids):
    norm_ids = {_norm(sid) for sid in set_ids}
    return any(_norm(sid) in norm_ids for sid in t["Sets"])


# ── OHKO filter helpers ───────────────────────────────────────────────────────

def _best_move_min_max(attacker, defender, species_map, **kwargs):
    """
    Returns (best_min_roll, best_max_roll) across all of the attacker's moves
    against the defender. 'Best' = highest min roll (the move most likely to KO).
    If no moves deal damage, returns (0, 0).
    """
    from damagecalc import damage_rolls, get_move

    if isinstance(attacker, CustomSet):
        move_names = attacker.moves or []
    else:
        move_names = attacker.get("Moves", [])

    best_min = 0
    best_max = 0

    for mname in move_names:
        try:
            mv = get_move(mname)
        except ValueError:
            continue
        if mv.get("power", 0) in (0, None):
            continue
        rolls = damage_rolls(attacker, defender, mv, species_map, **kwargs)
        roll_min = min(rolls)
        if roll_min > best_min:
            best_min = roll_min
            best_max = max(rolls)

    return best_min, best_max


def _get_defender_hp(defender, species_map, **kwargs):
    """Extract HP from a frontier set or CustomSet in the defender role.
    Respects def_current_hp if passed, otherwise uses max HP."""
    current = kwargs.get("def_current_hp")
    if current is not None:
        return current
    from damagecalc import _extract
    dfn = _extract(defender, species_map,
                   ivs=kwargs.get("def_ivs", 31),
                   level=kwargs.get("def_level", 100),
                   ability_override=kwargs.get("def_ability"))
    return dfn["stats"]["hp"]


# ── SetCollection ─────────────────────────────────────────────────────────────

class SetCollection:
    def __init__(self, sets: list, db: "Database"):
        self._sets = sets
        self._db   = db

    def _filter(self, pred, negate=False):
        fn = (lambda s: not pred(s)) if negate else pred
        return SetCollection([s for s in self._sets if fn(s)], self._db)

    def hasMove(self, *moves, match="any") -> "SetCollection":
        return self._filter(lambda s: _move_pred(s, moves, match))

    def hasAbility(self, *abilities) -> "SetCollection":
        return self._filter(lambda s: _ability_pred(s, abilities))

    def hasItem(self, *items) -> "SetCollection":
        return self._filter(lambda s: _item_pred(s, items))

    def hasNature(self, *natures) -> "SetCollection":
        return self._filter(lambda s: _nature_pred(s, natures))

    def hasType(self, *types) -> "SetCollection":
        return self._filter(lambda s: _type_pred(s, types, self._db._species_map))

    def statFilter(self, stat: str, *,
                   min: int = None, max: int = None,
                   ivs: int = 31, level: int = 100) -> "SetCollection":
        stat = _norm(stat)
        def pred(s):
            val = calc_stats(s, self._db._species_map, ivs=ivs, level=level).get(stat)
            if val is None:
                return False
            if min is not None and val < min:
                return False
            if max is not None and val > max:
                return False
            return True
        return self._filter(pred)

    def fasterThan(self, custom: CustomSet, *, ivs: int = 31, level: int = 100) -> "SetCollection":
        threshold = custom.speed()
        return self._filter(
            lambda s: calc_stats(s, self._db._species_map, ivs=ivs, level=level)["spe"] > threshold
        )

    def slowerThan(self, custom: CustomSet, *, ivs: int = 31, level: int = 100) -> "SetCollection":
        threshold = custom.speed()
        return self._filter(
            lambda s: calc_stats(s, self._db._species_map, ivs=ivs, level=level)["spe"] < threshold
        )

    def speedTieWith(self, custom: CustomSet, *, ivs: int = 31, level: int = 100) -> "SetCollection":
        threshold = custom.speed()
        return self._filter(
            lambda s: calc_stats(s, self._db._species_map, ivs=ivs, level=level)["spe"] == threshold
        )

    def willOHKO(self, defender, **kwargs) -> "SetCollection":
        """Filter to sets whose best move guarantees an OHKO (min roll KOs)."""
        smap = self._db._species_map
        hp = _get_defender_hp(defender, smap, **kwargs)
        return self._filter(
            lambda s: _best_move_min_max(s, defender, smap, **kwargs)[0] >= hp
        )

    def canOHKO(self, defender, **kwargs) -> "SetCollection":
        """Filter to sets whose best move can OHKO on the max roll."""
        smap = self._db._species_map
        hp = _get_defender_hp(defender, smap, **kwargs)
        return self._filter(
            lambda s: _best_move_min_max(s, defender, smap, **kwargs)[1] >= hp
        )

    def diesTo(self, attacker, **kwargs) -> "SetCollection":
        """Filter to sets that are guaranteed OHKO'd by the attacker's best move."""
        smap = self._db._species_map
        def pred(s):
            hp = _get_defender_hp(s, smap, **kwargs)
            return _best_move_min_max(attacker, s, smap, **kwargs)[0] >= hp
        return self._filter(pred)

    def canDieTo(self, attacker, **kwargs) -> "SetCollection":
        """Filter to sets that can be OHKO'd by the attacker's best move (max roll)."""
        smap = self._db._species_map
        def pred(s):
            hp = _get_defender_hp(s, smap, **kwargs)
            return _best_move_min_max(attacker, s, smap, **kwargs)[1] >= hp
        return self._filter(pred)

    def usedByTrainer(self) -> "TrainerCollection":
        ids = {_norm(_set_id(s)) for s in self._sets}
        matching = [t for t in self._db._trainers
                    if any(_norm(sid) in ids for sid in t["Sets"])]
        return self._db._make_trainer_collection(matching)

    @property
    def Not(self) -> "_NegatedSetCollection":
        return _NegatedSetCollection(self)

    def ids(self) -> list[str]:
        return [_set_id(s) for s in self._sets]

    def __iter__(self):
        return iter(self._sets)

    def __len__(self):
        return len(self._sets)

    def __repr__(self):
        return f"SetCollection({len(self._sets)} sets)"


class _NegatedSetCollection:
    def __init__(self, col: SetCollection):
        self._col = col

    def hasMove(self, *moves, match="any") -> SetCollection:
        return self._col._filter(lambda s: _move_pred(s, moves, match), negate=True)

    def hasAbility(self, *abilities) -> SetCollection:
        return self._col._filter(lambda s: _ability_pred(s, abilities), negate=True)

    def hasItem(self, *items) -> SetCollection:
        return self._col._filter(lambda s: _item_pred(s, items), negate=True)

    def hasNature(self, *natures) -> SetCollection:
        return self._col._filter(lambda s: _nature_pred(s, natures), negate=True)

    def hasType(self, *types) -> SetCollection:
        return self._col._filter(lambda s: _type_pred(s, types, self._col._db._species_map), negate=True)

    def statFilter(self, stat: str, *,
                   min: int = None, max: int = None,
                   ivs: int = 31, level: int = 100) -> SetCollection:
        stat = _norm(stat)
        def pred(s):
            val = calc_stats(s, self._col._db._species_map, ivs=ivs, level=level).get(stat)
            if val is None:
                return False
            if min is not None and val < min:
                return False
            if max is not None and val > max:
                return False
            return True
        return self._col._filter(pred, negate=True)

    def fasterThan(self, custom: CustomSet, *, ivs: int = 31, level: int = 100) -> SetCollection:
        threshold = custom.speed()
        return self._col._filter(
            lambda s: calc_stats(s, self._col._db._species_map, ivs=ivs, level=level)["spe"] > threshold,
            negate=True
        )

    def slowerThan(self, custom: CustomSet, *, ivs: int = 31, level: int = 100) -> SetCollection:
        threshold = custom.speed()
        return self._col._filter(
            lambda s: calc_stats(s, self._col._db._species_map, ivs=ivs, level=level)["spe"] < threshold,
            negate=True
        )

    def speedTieWith(self, custom: CustomSet, *, ivs: int = 31, level: int = 100) -> SetCollection:
        threshold = custom.speed()
        return self._col._filter(
            lambda s: calc_stats(s, self._col._db._species_map, ivs=ivs, level=level)["spe"] == threshold,
            negate=True
        )

    def willOHKO(self, defender, **kwargs) -> SetCollection:
        smap = self._col._db._species_map
        hp = _get_defender_hp(defender, smap, **kwargs)
        return self._col._filter(
            lambda s: _best_move_min_max(s, defender, smap, **kwargs)[0] >= hp,
            negate=True
        )

    def canOHKO(self, defender, **kwargs) -> SetCollection:
        smap = self._col._db._species_map
        hp = _get_defender_hp(defender, smap, **kwargs)
        return self._col._filter(
            lambda s: _best_move_min_max(s, defender, smap, **kwargs)[1] >= hp,
            negate=True
        )

    def diesTo(self, attacker, **kwargs) -> SetCollection:
        smap = self._col._db._species_map
        def pred(s):
            hp = _get_defender_hp(s, smap, **kwargs)
            return _best_move_min_max(attacker, s, smap, **kwargs)[0] >= hp
        return self._col._filter(pred, negate=True)

    def canDieTo(self, attacker, **kwargs) -> SetCollection:
        smap = self._col._db._species_map
        def pred(s):
            hp = _get_defender_hp(s, smap, **kwargs)
            return _best_move_min_max(attacker, s, smap, **kwargs)[1] >= hp
        return self._col._filter(pred, negate=True)


# ── TrainerCollection ─────────────────────────────────────────────────────────

class TrainerCollection:
    def __init__(self, trainers: list, db: "Database"):
        self._trainers = trainers
        self._db       = db

    def _filter(self, pred, negate=False):
        fn = (lambda t: not pred(t)) if negate else pred
        return TrainerCollection([t for t in self._trainers if fn(t)], self._db)

    def hasPokemon(self, *species) -> "TrainerCollection":
        return self._filter(lambda t: _trainer_has_pokemon_pred(t, species))

    def hasSet(self, *set_ids) -> "TrainerCollection":
        return self._filter(lambda t: _trainer_has_set_pred(t, set_ids))

    @property
    def Not(self) -> "_NegatedTrainerCollection":
        return _NegatedTrainerCollection(self)

    def names(self) -> list[str]:
        return [f"{t['Class'].upper()} {t['Name']}" for t in self._trainers]

    def __iter__(self):
        return iter(self._trainers)

    def __len__(self):
        return len(self._trainers)

    def __repr__(self):
        return f"TrainerCollection({len(self._trainers)} trainers)"


class _NegatedTrainerCollection:
    def __init__(self, col: TrainerCollection):
        self._col = col

    def hasPokemon(self, *species) -> TrainerCollection:
        return self._col._filter(lambda t: _trainer_has_pokemon_pred(t, species), negate=True)

    def hasSet(self, *set_ids) -> TrainerCollection:
        return self._col._filter(lambda t: _trainer_has_set_pred(t, set_ids), negate=True)


# ── Database ──────────────────────────────────────────────────────────────────

class Database:
    def __init__(self,
                 sets_file=SETS_FILE,
                 trainers_file=TRAINERS_FILE,
                 pokemon_file=POKEMON_FILE):
        with open(sets_file, encoding="utf-8") as f:
            self._sets = json.load(f)
        with open(trainers_file, encoding="utf-8") as f:
            self._trainers = json.load(f)
        with open(pokemon_file, encoding="utf-8") as f:
            self._species_map = {p["id"]: p for p in json.load(f)}

    def _make_trainer_collection(self, trainers: list) -> TrainerCollection:
        return TrainerCollection(trainers, self)

    @property
    def sets(self) -> SetCollection:
        return SetCollection(self._sets, self)

    @property
    def trainers(self) -> TrainerCollection:
        return TrainerCollection(self._trainers, self)

    def allSets(self, pokemon: str) -> SetCollection:
        norm = _norm(pokemon)
        return SetCollection(
            [s for s in self._sets if _norm(s["Pokemon"]) == norm], self
        )

    def usedByTrainer(self, set_id: str) -> TrainerCollection:
        norm = _norm(set_id)
        matching = [t for t in self._trainers
                    if any(_norm(sid) == norm for sid in t["Sets"])]
        return self._make_trainer_collection(matching)