import json
import random
import re
from pathlib import Path

from frontier_db import Database, _norm

# ── Team Type/Phrase utilities ────────────────────────────────────────────────

_PHRASE_CATEGORIES = [
    (3, {
        "acidarmor","agility","amnesia","barrier","bellydrum","bulkup","calmmind",
        "charge","conversion","conversion2","cosmicpower","defensecurl","doubleteam",
        "dragondance","focusenergy","growth","harden","howl","irondefense","meditate",
        "minimize","psychup","sharpen","snatch","swordsdance","tailglow","withdraw",
    }),
    (3, {
        "attract","block","confuseray","disable","encore","flatter","glare",
        "grasswhistle","hypnosis","imprison","leechseed","lovelykiss","meanlook",
        "poisongas","poisonpowder","sing","sleeppowder","snatch","spiderweb","spikes",
        "spore","stunspore","supersonic","swagger","sweetkiss","taunt","teeterdance",
        "thunderwave","torment","toxic","yawn","willowisp",
    }),
    (3, {
        "aromatherapy","batonpass","detect","endure","haze","healbell","ingrain",
        "lightscreen","magiccoat","milkdrink","mist","moonlight","morningsun",
        "mudsport","protect","recover","reflect","rest","safeguard","slackoff",
        "softboiled","swallow","synthesis","recycle","refresh","watersport","wish",
    }),
    (2, {
        "bide","blastburn","counter","destinybond","doubleedge","explosion","facade",
        "fissure","flail","focuspunch","frenzyplant","grudge","guillotine","horndrill",
        "hydrocannon","hyperbeam","memento","mirrorcoat","overheat","painsplit",
        "perishsong","psychoboost","reversal","selfdestruct","skyattack","volttackle",
    }),
    (2, {
        "charm","cottonspore","faketears","featherdance","flash","growl","kinesis",
        "knockoff","leer","metalsound","sandattack","scaryface","screech","smokescreen",
        "spite","stringshot","sweetscent","tailwhip","tickle",
    }),
    (2, {
        "assist","camouflage","curse","followme","metronome","mimic","mirrormove",
        "present","rolepay","sketch","skillswap","substitute","transform","trick",
    }),
    (2, {
        "hail","raindance","sandstorm","sunnyday","weatherball",
    }),
]

_PHRASE_STYLES = {
    None:   "appears to be free-spirited and unrestrained",
    1:      "appears to be one based on total preparation",
    2:      "appears to be slow and steady",
    3:      "appears to be one of endurance",
    4:      "appears to be high risk, high return",
    5:      "appears to be weakening the foe to start",
    6:      "appears to be impossible to predict",
    7:      "appears to depend on the battle's flow",
    "flex": "appears to be flexibly adaptable to the situation",
}

# Maps user-facing phrase number (0-8) → _PHRASE_STYLES key
_PHRASE_NUM_MAP = {0: None, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: "flex"}


def team_type(sets: list[dict], species_map: dict) -> str:
    counts: dict[str, int] = {}
    for s in sets:
        dex = s.get("DexNum")
        for t in species_map.get(dex, {}).get("types", []):
            counts[t] = counts.get(t, 0) + 1
    if not counts:
        return "No Type"
    max_count = max(counts.values())
    winners   = [t for t, c in counts.items() if c == max_count]
    return winners[0].capitalize() if len(winners) == 1 else "No Type"


def team_phrase(sets: list[dict]) -> str:
    crossed = []
    for i, (threshold, move_set) in enumerate(_PHRASE_CATEGORIES, start=1):
        count = sum(1 for s in sets for m in s["Moves"] if m in move_set)
        if count >= threshold:
            crossed.append(i)
    if len(crossed) == 0:
        return _PHRASE_STYLES[None]
    elif len(crossed) >= 3:
        return _PHRASE_STYLES["flex"]
    else:
        return _PHRASE_STYLES[max(crossed)]


def _set_has_type(s: dict, type_name: str, species_map: dict) -> bool:
    """Check whether a set's species includes the given type."""
    dex = s.get("DexNum")
    if dex is None:
        return False
    types = species_map.get(dex, {}).get("types", [])
    return _norm(type_name) in types


_DATA = Path(__file__).parent / "Data"

# ── Group definitions ─────────────────────────────────────────────────────────
# Maps index range → group number. Indices 1-110 and Unown don't appear.

_GROUP_RANGES = [
    (range(111, 163), 1),
    (range(163, 269), 2),
    (range(269, 373), 3),
    (range(373, 470), 4),
    (range(470, 566), 5),
    (range(566, 662), 6),
    (range(662, 757), 7),
    (range(757, 851), 8),
    (range(851, 883), 9),
]

_UNOWN = "unown"


def get_group(index: int) -> int | None:
    """Returns the Factory group (1-9) for a set index, or None if not eligible."""
    for rng, grp in _GROUP_RANGES:
        if index in rng:
            return grp
    return None


# ── Round → group pool mappings ───────────────────────────────────────────────

_LV50_ROUNDS = {
    1: [1],
    2: [2],
    3: [3],
    4: [4],
    5: [5],
    6: [6],
    7: [7],
    8: [4, 5, 6, 7, 8],
}

_OPEN_ROUNDS = {
    1: [4],
    2: [5],
    3: [6],
    4: [7],
    5: [4, 5, 6, 7, 8, 9],
}

def _get_groups(level: str, round_num: int) -> list[int]:
    """
    Returns the list of eligible groups for a given level format and round.
    level: 'lv50' or 'open'. Round numbers beyond the defined max use the last entry.
    """
    level = _norm(level)
    if level in ("lv50", "50"):
        table = _LV50_ROUNDS
        max_round = 8
    else:
        table = _OPEN_ROUNDS
        max_round = 5

    r = min(round_num, max_round)
    return table[r]


# ── FactoryDatabase ───────────────────────────────────────────────────────────

class FactoryDatabase(Database):

    def sets_in_groups(self, groups: list[int]) -> list[dict]:
        """Returns all eligible sets belonging to the given group numbers."""
        return [
            s for s in self._sets
            if s.get("Index") is not None
            and get_group(s["Index"]) in groups
            and _norm(s["Pokemon"]) != _UNOWN
        ]

    def random_team(self, level: str = "open", round_num: int = 5,
                    target_type: str = None, target_phrase: int = None,
                    max_attempts: int = 200_000) -> tuple[list[str], str, str]:
        """
        Generate a random 3-set Factory team for the given level format and round.
        Respects species clause and item clause.

        Optional constraints:
            target_type:   Type string (e.g. "Water", "Fire") or "None" for No Type.
            target_phrase: Integer 0-8 (0 = no style, 1-7 = styles, 8 = flex).
            max_attempts:  Safety cap on rejection iterations.

        If a Type is given (and not "None"), sampling is biased: two of three sets
        are drawn from the type sub-pool, then the result is checked against the
        full Type/Phrase target. Without a type (or with "None"), teams are sampled
        uniformly and tested.

        Returns (list of 'Pokemon-SetNum' ids, type string, phrase string).
        Raises ValueError if no valid team is found within max_attempts.
        """
        groups = _get_groups(level, round_num)
        pool   = self.sets_in_groups(groups)

        if not pool:
            raise ValueError(f"No eligible sets for level='{level}', round={round_num}")

        # Resolve target strings for comparison
        want_type = None
        if target_type is not None:
            want_type = "No Type" if _norm(target_type) == "none" else target_type.capitalize()

        want_phrase = None
        if target_phrase is not None:
            if target_phrase not in _PHRASE_NUM_MAP:
                raise ValueError(f"target_phrase must be 0-8, got {target_phrase}")
            want_phrase = _PHRASE_STYLES[_PHRASE_NUM_MAP[target_phrase]]

        # Build type sub-pool for biased sampling (only for real types)
        use_type_bias = (want_type is not None and want_type != "No Type")
        if use_type_bias:
            type_pool = [s for s in pool if _set_has_type(s, want_type, self._species_map)]
            if len(type_pool) < 2:
                raise ValueError(
                    f"Fewer than 2 sets of type '{want_type}' in pool "
                    f"(level='{level}', round={round_num})"
                )

        for attempt in range(max_attempts):
            if use_type_bias:
                chosen = self._sample_type_biased(pool, type_pool)
            else:
                chosen = self._sample_uniform(pool)

            if chosen is None:
                continue

            typ    = team_type(chosen, self._species_map)
            phrase = team_phrase(chosen)

            if want_type is not None and typ != want_type:
                continue
            if want_phrase is not None and phrase != want_phrase:
                continue

            # Assign random slot order
            random.shuffle(chosen)
            ids = [f"{s['Pokemon']}-{s['SetNum']}" for s in chosen]
            return ids, typ, phrase

        filters = []
        if want_type is not None:
            filters.append(f"type='{want_type}'")
        if want_phrase is not None:
            filters.append(f"phrase='{want_phrase}'")
        raise ValueError(
            f"Could not generate a team matching {', '.join(filters)} "
            f"within {max_attempts:,} attempts "
            f"(level='{level}', round={round_num})"
        )

    # ── Internal sampling helpers ─────────────────────────────────────────────

    def _sample_uniform(self, pool: list[dict]) -> list[dict] | None:
        """Pick 3 random sets from pool respecting species/item clause."""
        random.shuffle(pool)

        chosen       = []
        used_species = set()
        used_items   = set()

        for s in pool:
            sp = _norm(s["Pokemon"])
            it = _norm(s["Item"])
            if sp in used_species or it in used_items:
                continue
            chosen.append(s)
            used_species.add(sp)
            used_items.add(it)
            if len(chosen) == 3:
                return chosen

        return None

    def _sample_type_biased(self, pool: list[dict],
                            type_pool: list[dict]) -> list[dict] | None:
        """
        Pick 2 sets from type_pool + 1 from full pool, respecting clauses.
        This biases sampling toward the target type so rejection rates stay
        manageable for rarer types.
        """
        # First typed set
        first = random.choice(type_pool)
        used_species = {_norm(first["Pokemon"])}
        used_items   = {_norm(first["Item"])}

        # Second typed set (clause-compatible with first)
        candidates = [
            s for s in type_pool
            if _norm(s["Pokemon"]) not in used_species
            and _norm(s["Item"]) not in used_items
        ]
        if not candidates:
            return None
        second = random.choice(candidates)
        used_species.add(_norm(second["Pokemon"]))
        used_items.add(_norm(second["Item"]))

        # Third set from full pool (clause-compatible with both)
        candidates = [
            s for s in pool
            if _norm(s["Pokemon"]) not in used_species
            and _norm(s["Item"]) not in used_items
        ]
        if not candidates:
            return None
        third = random.choice(candidates)

        return [first, second, third]