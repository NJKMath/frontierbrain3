"""
frontierbrain3 -- Data analysis tools for Pokemon Emerald's Battle Frontier.

Quick start:
    from frontierbrain3 import Database, CustomSet, calc_matchup

Core:
    Database        - query/filter frontier sets and trainers
    CustomSet       - define your own Pokemon set
    calc_stats      - compute stats from a set dict
    from_paste      - import teams from Pokepaste format

Damage calculator:
    damage_rolls    - per-hit damage values
    calc_matchup    - full matchup summary with KO chances
    format_result   - pretty-print a matchup result
    Field           - field conditions (weather, screens, doubles)

Facilities:
    frontierbrain3.facilities.tower    - TowerDatabase
    frontierbrain3.facilities.factory  - FactoryDatabase
    frontierbrain3.facilities.dome     - calc_seed
    frontierbrain3.facilities.palace   - move selection probabilities
    frontierbrain3.facilities.pike     - events, status, wild encounters
    frontierbrain3.facilities.pyramid  - encounter & item tables
    frontierbrain3.facilities.arena    - (placeholder)
"""

from .frontierutils import (
    CustomSet,
    calc_stats,
    apply_stage,
    move_category,
    type_effectiveness,
    from_paste,
    STAT_KEYS,
)

from .frontier_db import Database, SetCollection, TrainerCollection

from .damagecalc import (
    damage_rolls,
    ko_chance,
    calc_matchup,
    format_result,
    get_move,
    get_hit_info,
    Field,
)

__version__ = "0.1.1"

__all__ = [
    # Core
    "Database", "SetCollection", "TrainerCollection",
    "CustomSet", "calc_stats", "apply_stage", "move_category",
    "type_effectiveness", "from_paste", "STAT_KEYS",
    # Damage calc
    "damage_rolls", "ko_chance", "calc_matchup", "format_result",
    "get_move", "get_hit_info", "Field",
]