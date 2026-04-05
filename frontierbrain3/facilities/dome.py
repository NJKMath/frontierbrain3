"""
dome.py -- Battle Dome utilities.

Provides:
    calc_seed() - Calculate the seeding value for a team of 3.

Formula:
    seed = unique_types * (highest_level // 20) + sum(all stats)

Enemy bugs (is_enemy=True):
    - Stats are calculated as if the mon has 0 EVs.
    - Non-HP stats overflow to stat mod 256.
"""

from ..frontierutils import _norm, calc_stats, CustomSet, _default_species_map


def calc_seed(
    team: list,
    species_map: dict = None,
    *,
    level: int = 100,
    ivs: int = 31,
    is_enemy: bool = False,
) -> int:
    """
    Calculate the Battle Dome seeding value for a team of 3.

    Parameters
    ----------
    team : list
        List of 3 frontier set dicts, or CustomSets (CustomSet only if
        is_enemy is False).
    species_map : dict, optional
        Species data. Defaults to the built-in pokemon.json.
    level : int
        Level for frontier sets (ignored for CustomSets, which carry their own).
    ivs : int
        IVs for frontier sets (ignored for CustomSets).
    is_enemy : bool
        If True, applies the two enemy seeding bugs:
            1. Stats calculated with 0 EVs.
            2. Non-HP stats are taken mod 256.
        Only frontier set dicts are supported when is_enemy is True.

    Returns
    -------
    int
        The seeding value.
    """
    if species_map is None:
        species_map = _default_species_map()

    if len(team) != 3:
        raise ValueError(f"Team must have exactly 3 members, got {len(team)}")

    unique_types = set()
    highest_level = 0
    stat_total = 0

    for mon in team:
        if isinstance(mon, CustomSet):
            if is_enemy:
                raise ValueError(
                    "is_enemy=True only supports frontier set dicts, "
                    "not CustomSets"
                )
            # CustomSet: use its own level, stats, and type lookup
            dex_entry = next(
                (p for p in species_map.values()
                 if _norm(p["name"]) == _norm(mon.pokemon)),
                None,
            )
            if dex_entry:
                for t in dex_entry.get("types", []):
                    unique_types.add(_norm(t))
            stats = mon.get_stats()
            mon_level = mon.level
        else:
            # Frontier set dict
            dex = mon.get("DexNum")
            sp = species_map.get(dex, {})
            for t in sp.get("types", []):
                unique_types.add(_norm(t))

            if is_enemy:
                # Bug 1: stats calculated with 0 EVs
                zero_ev_set = dict(mon)
                zero_ev_set["EVs"] = [0, 0, 0, 0, 0, 0]
                stats = calc_stats(zero_ev_set, species_map, ivs=ivs, level=level)
            else:
                stats = calc_stats(mon, species_map, ivs=ivs, level=level)

            mon_level = level

        if mon_level > highest_level:
            highest_level = mon_level

        for stat_key, val in stats.items():
            if is_enemy and stat_key != "hp":
                # Bug 2: non-HP stats overflow (mod 256)
                val = val % 256
            stat_total += val

    seed = len(unique_types) * (highest_level // 20) + stat_total
    return seed