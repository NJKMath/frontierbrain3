from frontier_db import (
    Database, TrainerCollection,
    _norm, _trainer_has_pokemon_pred, _trainer_has_set_pred,
)
import random

# ── Tower trainer tier data ───────────────────────────────────────────────────
#
# Each entry: (index_range, ivs, rounds, last_in_round)
#   rounds:        list of round numbers this tier appears in (8 = round 8+)
#   last_in_round: None    — never the last trainer of a round
#                  int     — only last in that specific round
#                  "any"   — can be last in any of their rounds (round 8+ tier)
#
# Frontier Brains (index 300+) are not in this table; they're fixed battles.
# Brain IVs: Silver = 15, Gold = 31.

TIERS = [
    (range(  1,  81),  3,  [1],          None),
    (range( 81, 101),  6,  [1, 2],       None),
    (range(101, 121),  9,  [1, 2, 3],    1),
    (range(121, 141), 12,  [2, 3, 4],    2),
    (range(141, 161), 15,  [3, 4, 5],    3),
    (range(161, 181), 18,  [4, 5, 6],    4),
    (range(181, 201), 21,  [5, 6, 7],    5),
    (range(201, 221), 21,  [6, 7, 8],    6),
    (range(221, 241), 31,  [7, 8],       7),
    (range(241, 301), 31,  [8],          "any"),
]

BRAIN_IVS = {"silver": 15, "gold": 31}


def get_tier(index: int) -> dict | None:
    """Returns tier info for a trainer index, or None for Frontier Brains (300+)."""
    for rng, ivs, rounds, last_in in TIERS:
        if index in rng:
            return {"ivs": ivs, "rounds": rounds, "last_in_round": last_in}
    return None


def _appears_in_round(t: dict, round_num: int) -> bool:
    tier = get_tier(t["Index"])
    return tier is not None and round_num in tier["rounds"]


def _can_be_last_in_round(t: dict, round_num: int) -> bool:
    tier = get_tier(t["Index"])
    if tier is None:
        return False
    last = tier["last_in_round"]
    return last == "any" or last == round_num


# ── TowerTrainerCollection ────────────────────────────────────────────────────

class TowerTrainerCollection(TrainerCollection):

    def _filter(self, pred, negate=False):
        fn = (lambda t: not pred(t)) if negate else pred
        return TowerTrainerCollection([t for t in self._trainers if fn(t)], self._db)

    def appearsInRound(self, round_num: int) -> "TowerTrainerCollection":
        return self._filter(lambda t: _appears_in_round(t, round_num))

    def canBeLastInRound(self, round_num: int) -> "TowerTrainerCollection":
        """Filters to trainers that can appear as the last trainer of the given round."""
        return self._filter(lambda t: _can_be_last_in_round(t, round_num))

    @property
    def Not(self) -> "_NegatedTowerTrainerCollection":
        return _NegatedTowerTrainerCollection(self)


class _NegatedTowerTrainerCollection:
    def __init__(self, col: TowerTrainerCollection):
        self._col = col

    def hasPokemon(self, *species) -> TowerTrainerCollection:
        return self._col._filter(lambda t: _trainer_has_pokemon_pred(t, species), negate=True)

    def hasSet(self, *set_ids) -> TowerTrainerCollection:
        return self._col._filter(lambda t: _trainer_has_set_pred(t, set_ids), negate=True)

    def appearsInRound(self, round_num: int) -> TowerTrainerCollection:
        return self._col._filter(lambda t: _appears_in_round(t, round_num), negate=True)

    def canBeLastInRound(self, round_num: int) -> TowerTrainerCollection:
        return self._col._filter(lambda t: _can_be_last_in_round(t, round_num), negate=True)


# ── TowerDatabase ─────────────────────────────────────────────────────────────

class TowerDatabase(Database):

    def _make_trainer_collection(self, trainers: list) -> TowerTrainerCollection:
        return TowerTrainerCollection(trainers, self)

    def random_team(self,
                    round_num: int = None,
                    name: str = None,
                    trainer_class: str = None) -> str:
        """
        Randomly generate a 3-set team. Defaults to round 8 if no filters given,
        or all rounds if name/class is specified.
        """
        set_lookup = {f"{s['Pokemon']}-{s['SetNum']}": s for s in self._sets}

        if round_num is None and name is None and trainer_class is None:
            round_num = 8

        eligible = [
            t for t in self._trainers
            if (round_num is None or (
                _appears_in_round(t, round_num)
                and not _can_be_last_in_round(t, round_num)))
            and (name is None or _norm(t["Name"]) == _norm(name))
            and (trainer_class is None or _norm(t["Class"]) == _norm(trainer_class))
        ]

        if not eligible:
            filters = f"round={round_num}"
            if name:           filters += f", name='{name}'"
            if trainer_class:  filters += f", class='{trainer_class}'"
            return f"Error: no eligible trainers found for {filters}"

        trainer = random.choice(eligible)
        pool = [sid for sid in trainer["Sets"] if sid in set_lookup]
        random.shuffle(pool)

        chosen       = []
        used_species = set()
        used_items   = set()

        for sid in pool:
            s       = set_lookup[sid]
            species = _norm(s["Pokemon"])
            item    = _norm(s["Item"])
            if species in used_species or item in used_items:
                continue
            chosen.append(sid)
            used_species.add(species)
            used_items.add(item)
            if len(chosen) == 3:
                break

        if len(chosen) < 3:
            return (f"Error: could not find 3 valid sets for "
                    f"{trainer['Class']} {trainer['Name']} "
                    f"(species/item clause too restrictive)")

        random.shuffle(chosen)
        label = f"{trainer['Class']} {trainer['Name']}"
        return f"{label}: {', '.join(chosen)}"