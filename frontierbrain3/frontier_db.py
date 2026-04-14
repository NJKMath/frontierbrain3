"""
frontier_db.py — Database and query/filter collections for Battle Frontier data.

Depends on:
    frontierutils  — shared data, stats, types, CustomSet
    damagecalc     — damage formula (for OHKO filters)
"""

import json
from pathlib import Path

from .frontierutils import (
    _norm, _set_id, calc_stats, CustomSet, type_effectiveness,
    SETS_FILE, TRAINERS_FILE, POKEMON_FILE,
    # Re-exported for backward compatibility
    from_paste, STAT_KEYS,
    apply_stage, move_category,
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

# One-hit KO moves: normalized name → move type
_OHKO_MOVES = {
    "guillotine": "normal",
    "horndrill":  "normal",
    "fissure":    "ground",
    "sheercold":  "ice",
}


def _ohko_move_accuracy(atk_level: int, def_level: int) -> int:
    """Gen 3 OHKO move accuracy: fails if attacker level < defender level."""
    if atk_level < def_level:
        return 0
    return min(100, 30 + atk_level - def_level)


def _best_ohko_chance(attacker, defender, species_map, *,
                      include_ohko=False, include_acc=False, **kwargs):
    """
    Returns the highest OHKO probability (0.0–1.0) across all of the
    attacker's moves against the defender, including multi-hit support.
    """
    from .damagecalc import (
        damage_rolls, get_move, get_hit_info, _extract,
        multi_hit_ohko_prob, _convolve_once, _ko_prob_from_dist,
        _TRIPLE_KICK_POWERS,
    )

    dfn = _extract(defender, species_map,
                   ivs=kwargs.get("def_ivs", 31),
                   level=kwargs.get("def_level", 100),
                   ability_override=kwargs.get("def_ability"))
    hp = kwargs.get("def_current_hp") or dfn["stats"]["hp"]
    def_types = dfn["types"]
    def_ability = dfn["ability"]
    def_level = dfn["level"]

    atk_info = _extract(attacker, species_map,
                        ivs=kwargs.get("atk_ivs", 31),
                        level=kwargs.get("atk_level", 100),
                        ability_override=kwargs.get("atk_ability"))
    atk_level = atk_info["level"]

    if isinstance(attacker, CustomSet):
        move_names = attacker.moves or []
    else:
        move_names = attacker.get("Moves", [])

    best = 0.0

    for mname in move_names:
        norm = _norm(mname)

        # ── OHKO moves ────────────────────────────────────────────────
        if norm in _OHKO_MOVES and include_ohko:
            if def_ability == "sturdy":
                continue
            ohko_type = _OHKO_MOVES[norm]
            eff = type_effectiveness(ohko_type, def_types)
            if eff == 0:
                continue
            if include_acc:
                acc = _ohko_move_accuracy(atk_level, def_level)
                chance = acc / 100
            else:
                chance = 1.0
            best = max(best, chance)
            if best >= 1.0:
                return 1.0
            continue

        # ── Regular damaging moves ────────────────────────────────────
        try:
            mv = get_move(mname)
        except ValueError:
            continue
        if mv.get("power", 0) in (0, None):
            continue

        per_hit_rolls = damage_rolls(attacker, defender, mv, species_map, **kwargs)
        hit_info = get_hit_info(mv)

        # Compute OHKO probability based on hit type
        if hit_info["type"] == "triple_kick":
            # Convolve 3 different-power kicks
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
            total_combos = 1
            for kr in kick_rolls_list:
                total_combos *= len(kr)
            roll_chance = _ko_prob_from_dist(dist, total_combos, hp)
        else:
            roll_chance = multi_hit_ohko_prob(per_hit_rolls, hp, hit_info)

        if roll_chance <= 0:
            continue

        if include_acc:
            acc = mv.get("accuracy", 100)
            if not acc or acc <= 0:
                acc = 100
            else:
                # Defender evasion items (not applied to never-miss moves)
                if dfn["item"] == "brightpowder":
                    acc = acc * 9 // 10
                elif dfn["item"] == "laxincense":
                    acc = acc * 95 // 100
            chance = (acc / 100) * roll_chance
        else:
            chance = roll_chance

        best = max(best, chance)
        if best >= 1.0:
            return 1.0

    return best


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

    # ── OHKO filters ──────────────────────────────────────────────────────

    def willOHKO(self, defender, *,
                 include_ohko=False, include_acc=False, **kwargs) -> "SetCollection":
        """
        Filter to sets that GUARANTEE an OHKO on the defender.

        include_ohko: Allow OHKO moves (Guillotine, etc.) to count.
        include_acc:  Only count moves with 100% accuracy as guaranteed.
                      (A move with <100% accuracy cannot be a guaranteed OHKO.)
        **kwargs:     Passed to damage_rolls (field, atk_boosts, critical, etc.)
        """
        smap = self._db._species_map
        return self._filter(
            lambda s: _best_ohko_chance(
                s, defender, smap,
                include_ohko=include_ohko, include_acc=include_acc, **kwargs
            ) >= 1.0
        )

    def canOHKO(self, defender, *,
                include_ohko=False, include_acc=False,
                min_chance=None, **kwargs) -> "SetCollection":
        """
        Filter to sets that CAN OHKO the defender (at least one roll KOs).

        include_ohko: Allow OHKO moves to count.
        include_acc:  Factor accuracy into the probability.
        min_chance:   Minimum OHKO probability threshold (0.0–1.0).
                      None (default) = any non-zero chance.
                      E.g. min_chance=0.5 for "at least 50% to OHKO".
        **kwargs:     Passed to damage_rolls.
        """
        smap = self._db._species_map
        if min_chance is None:
            return self._filter(
                lambda s: _best_ohko_chance(
                    s, defender, smap,
                    include_ohko=include_ohko, include_acc=include_acc, **kwargs
                ) > 0
            )
        return self._filter(
            lambda s: _best_ohko_chance(
                s, defender, smap,
                include_ohko=include_ohko, include_acc=include_acc, **kwargs
            ) >= min_chance
        )

    def willDieTo(self, attacker, *,
               include_ohko=False, include_acc=False, **kwargs) -> "SetCollection":
        """
        Filter to sets that the attacker GUARANTEES to OHKO.
        (Reverse of willOHKO; each set in the collection is the defender.)
        """
        smap = self._db._species_map
        return self._filter(
            lambda s: _best_ohko_chance(
                attacker, s, smap,
                include_ohko=include_ohko, include_acc=include_acc, **kwargs
            ) >= 1.0
        )

    def canDieTo(self, attacker, *,
                 include_ohko=False, include_acc=False,
                 min_chance=None, **kwargs) -> "SetCollection":
        """
        Filter to sets that the attacker CAN OHKO.
        (Reverse of canOHKO — each set in the collection is the defender.)
        """
        smap = self._db._species_map
        if min_chance is None:
            return self._filter(
                lambda s: _best_ohko_chance(
                    attacker, s, smap,
                    include_ohko=include_ohko, include_acc=include_acc, **kwargs
                ) > 0
            )
        return self._filter(
            lambda s: _best_ohko_chance(
                attacker, s, smap,
                include_ohko=include_ohko, include_acc=include_acc, **kwargs
            ) >= min_chance
        )

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

    # ── Negated OHKO filters ──────────────────────────────────────────────

    def willOHKO(self, defender, *,
                 include_ohko=False, include_acc=False, **kwargs) -> SetCollection:
        smap = self._col._db._species_map
        return self._col._filter(
            lambda s: _best_ohko_chance(
                s, defender, smap,
                include_ohko=include_ohko, include_acc=include_acc, **kwargs
            ) >= 1.0,
            negate=True
        )

    def canOHKO(self, defender, *,
                include_ohko=False, include_acc=False,
                min_chance=None, **kwargs) -> SetCollection:
        smap = self._col._db._species_map
        if min_chance is None:
            return self._col._filter(
                lambda s: _best_ohko_chance(
                    s, defender, smap,
                    include_ohko=include_ohko, include_acc=include_acc, **kwargs
                ) > 0,
                negate=True
            )
        return self._col._filter(
            lambda s: _best_ohko_chance(
                s, defender, smap,
                include_ohko=include_ohko, include_acc=include_acc, **kwargs
            ) >= min_chance,
            negate=True
        )

    def willDieTo(self, attacker, *,
               include_ohko=False, include_acc=False, **kwargs) -> SetCollection:
        smap = self._col._db._species_map
        return self._col._filter(
            lambda s: _best_ohko_chance(
                attacker, s, smap,
                include_ohko=include_ohko, include_acc=include_acc, **kwargs
            ) >= 1.0,
            negate=True
        )

    def canDieTo(self, attacker, *,
                 include_ohko=False, include_acc=False,
                 min_chance=None, **kwargs) -> SetCollection:
        smap = self._col._db._species_map
        if min_chance is None:
            return self._col._filter(
                lambda s: _best_ohko_chance(
                    attacker, s, smap,
                    include_ohko=include_ohko, include_acc=include_acc, **kwargs
                ) > 0,
                negate=True
            )
        return self._col._filter(
            lambda s: _best_ohko_chance(
                attacker, s, smap,
                include_ohko=include_ohko, include_acc=include_acc, **kwargs
            ) >= min_chance,
            negate=True
        )


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
        return self._make_trainer_collection(self._trainers)

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