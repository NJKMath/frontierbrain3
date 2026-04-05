#!/usr/bin/env python3
"""
Interactive demo for frontierbrain3.

Run with: python demo.py

Navigate by category, step through examples with Enter.
Shows code and full output in REPL style.
"""

import random
import sys

from frontierbrain3 import (
    Database, CustomSet, calc_stats, from_paste,
    damage_rolls, ko_chance, calc_matchup, format_result, Field,
)
from frontierbrain3.damagecalc import get_hit_info, RECOIL_MOVES, DRAIN_MOVES
from frontierbrain3.facilities.tower import TowerDatabase, get_tier, BRAIN_IVS
from frontierbrain3.facilities.factory import FactoryDatabase, team_type, team_phrase, get_group
from frontierbrain3.facilities.dome import calc_seed
from frontierbrain3.facilities.palace import (
    get_move_category, categorize_moveset, get_nature_ratios,
    get_action_probabilities, get_move_probabilities,
    multi_turn_probabilities, move_turn_probabilities,
    cumulative_attack_prob, expected_attacks,
    rank_natures, low_hp_message, DOUBLES_TARGETING,
)
from frontierbrain3.facilities.pike import (
    get_event_probabilities, get_status_chances, status_targets,
    get_wild_pokemon, HINTS, EVENTS, STATUS_TABLE,
)
from frontierbrain3.facilities.pyramid import (
    ROUNDS, ROUND_THEMES, get_round_pokemon, get_encounters,
    get_floor_encounter_rate, get_items, get_pickup_items,
    FLOOR_TABLE, SLOT_RATES,
)
from frontierbrain3.frontier_db import SetCollection, TrainerCollection

# -- Setup ---------------------------------------------------------------------

print("Loading databases...", end=" ", flush=True)
db = Database()
tower = TowerDatabase()
fac = FactoryDatabase()
print("done.\n")

def _first(pokemon):
    sets = db.allSets(pokemon)._sets
    return sets[0] if sets else None

META = _first("Metagross")
TTAR = _first("Tyranitar")
LAX  = _first("Snorlax")
ZAM  = _first("Alakazam")
SALA = _first("Salamence")
GENGAR = _first("Gengar")
STEELIX = _first("Steelix")
SWAM = _first("Swampert")

STARMIE = CustomSet("Starmie", nature="Timid", evs=[0,0,0,252,4,252],
                    ability="Natural Cure",
                    moves=["Surf", "Thunderbolt", "Ice Beam", "Psychic"])
HERA = CustomSet("Heracross", nature="Adamant", evs=[4,252,0,0,0,252],
                 item="Choice Band", ability="Guts",
                 moves=["Megahorn", "Earthquake", "Brick Break", "Rock Slide"])
FLYGON_CUSTOM = CustomSet("Flygon", nature="Jolly", evs=[4,252,0,0,0,252])

DRAGON_RAGE = {"name": "Dragon Rage", "type": "dragon",   "power": 0}
SONIC_BOOM  = {"name": "SonicBoom",   "type": "normal",   "power": 0}
SEISMIC_TOSS= {"name": "Seismic Toss","type": "fighting",  "power": 0}
NIGHT_SHADE = {"name": "Night Shade", "type": "ghost",    "power": 0}
SUPER_FANG  = {"name": "Super Fang",  "type": "normal",   "power": 0}
ENDEAVOR    = {"name": "Endeavor",    "type": "normal",   "power": 0}
ERUPTION    = {"name": "Eruption",    "type": "fire",     "power": 0}
FLAIL       = {"name": "Flail",       "type": "normal",   "power": 0}
REVERSAL    = {"name": "Reversal",    "type": "fighting",  "power": 0}
LOW_KICK    = {"name": "Low Kick",    "type": "fighting",  "power": 0}
PSYWAVE     = {"name": "Psywave",     "type": "psychic",  "power": 0}
DOUBLE_KICK = {"name": "Double Kick", "type": "fighting",  "power": 30}
BULLET_SEED = {"name": "Bullet Seed", "type": "grass",    "power": 25}


# -- Display helpers -----------------------------------------------------------

WIDTH = 70

def pause():
    input("\n[Enter to continue, 'q' to go back] ")

def _fmt(val):
    """Format a value for display, rounding floats."""
    if isinstance(val, float):
        return f"{val:.2f}"
    return repr(val)

def show(code, result):
    """Display a code line and its result in REPL style."""
    print(f">>> {code}")
    if isinstance(result, SetCollection):
        ids = result.ids()
        print(f"{repr(result)}")
        print(f"  {ids}")
    elif isinstance(result, TrainerCollection):
        names = result.names()
        print(f"{repr(result)}")
        print(f"  {names}")
    elif isinstance(result, str):
        if "\n" in result:
            for line in result.splitlines():
                print(f"  {line}")
        else:
            print(f"  {result}")
    elif isinstance(result, dict):
        print("  {")
        for k, v in result.items():
            print(f"    {repr(k)}: {_fmt(v)},")
        print("  }")
    elif isinstance(result, list):
        print(f"  {result}")
    else:
        print(f"  {_fmt(result)}")
    print()

def show_matchup(attacker_label, defender_label, move_name, result):
    """Display a damage calc result with context."""
    print(f">>> calc_matchup({attacker_label}, {defender_label}, \"{move_name}\")")
    print(format_result(result, move_name))
    print()

def header(title):
    print(f"\n{'~' * WIDTH}")
    print(f"  {title}")
    print(f"{'~' * WIDTH}\n")


# -- Category 1: Database & Set Filters ----------------------------------------

def cat_database():
    def ex_type_filters():
        print("# Type filters: hasType\n")
        show('db.sets.hasType("Water")',
             db.sets.hasType("Water"))
        show('db.sets.hasType("Psychic/")',
             db.sets.hasType("Psychic/"))
        show('db.sets.hasType("Fire/Flying")',
             db.sets.hasType("Fire/Flying"))

    def ex_move_filters():
        print("# Move filters: hasMove\n")
        show('db.sets.hasMove("earthquake")',
             db.sets.hasMove("earthquake"))
        show('db.sets.hasMove("earthquake", "surf")',
             db.sets.hasMove("earthquake", "surf"))
        show('db.sets.hasMove("calmmind", "surf", match="all")',
             db.sets.hasMove("calmmind", "surf", match="all"))

    def ex_item_nature_ability():
        print("# Item, Nature, Ability filters\n")
        show('db.sets.hasNature("Adamant").hasItem("Choice Band")',
             db.sets.hasNature("Adamant").hasItem("Choice Band"))
        show('db.sets.hasAbility("Intimidate")',
             db.sets.hasAbility("Intimidate"))

    def ex_negation():
        print("# Negated filters with .Not\n")
        show('db.sets.hasMove("earthquake").Not.hasMove("surf")',
             db.sets.hasMove("earthquake").Not.hasMove("surf"))
        show('db.sets.Not.hasType("Water").hasMove("surf")',
             db.sets.Not.hasType("Water").hasMove("surf"))

    def ex_all_sets():
        print("# All sets for a species\n")
        show('db.allSets("Charizard").ids()',
             db.allSets("Charizard").ids())
        show('db.allSets("Metagross").ids()',
             db.allSets("Metagross").ids())

    def ex_trainers():
        print("# Trainer queries\n")
        show('db.sets.hasType("Water").hasMove("surf").usedByTrainer()',
             db.sets.hasType("Water").hasMove("surf").usedByTrainer())
        show('db.trainers.hasPokemon("Charizard").Not.hasPokemon("Blastoise")',
             db.trainers.hasPokemon("Charizard").Not.hasPokemon("Blastoise"))

    return [ex_type_filters, ex_move_filters, ex_item_nature_ability,
            ex_negation, ex_all_sets, ex_trainers]


# -- Category 2: Stats & Speed ------------------------------------------------

def cat_stats():
    def ex_calc_stats():
        print("# Stat calculations at different IVs/levels\n")
        show('calc_stats(ZAM)',
             calc_stats(ZAM))
        show('calc_stats(ZAM, ivs=15)',
             calc_stats(ZAM, ivs=15))
        show('calc_stats(LAX, level=50)',
             calc_stats(LAX, level=50))

    def ex_stat_filter():
        print("# Filter sets by calculated stat value\n")
        show('db.sets.statFilter("atk", min=300)',
             db.sets.statFilter("atk", min=300))
        show('db.sets.statFilter("spa", min=150, level=50, ivs=15)',
             db.sets.statFilter("spa", min=150, level=50, ivs=15))

    def ex_custom_set():
        print("# CustomSet: player-defined Pokemon\n")
        show('FLYGON_CUSTOM', FLYGON_CUSTOM)
        show('FLYGON_CUSTOM.get_stats()', FLYGON_CUSTOM.get_stats())
        show('FLYGON_CUSTOM.speed()', FLYGON_CUSTOM.speed())

    def ex_speed_compare():
        print(f"# Speed comparisons against Jolly Flygon (speed={FLYGON_CUSTOM.speed()})\n")
        show('db.sets.fasterThan(FLYGON_CUSTOM)',
             db.sets.fasterThan(FLYGON_CUSTOM))
        show('db.sets.slowerThan(FLYGON_CUSTOM)',
             db.sets.slowerThan(FLYGON_CUSTOM))
        show('db.sets.speedTieWith(FLYGON_CUSTOM)',
             db.sets.speedTieWith(FLYGON_CUSTOM))
        show('db.sets.fasterThan(FLYGON_CUSTOM, ivs=15)',
             db.sets.fasterThan(FLYGON_CUSTOM, ivs=15))

    def ex_paste():
        print("# Pokepaste import\n")
        paste = (
            "BLEACH (Skarmory) (M) @ Chesto Berry\n"
            "Ability: Sturdy\nLevel: 50\n"
            "EVs: 252 HP / 140 Def / 116 SpD\nBold Nature\n"
            "IVs: 0 Atk\n- Protect\n- Rest\n- Whirlwind\n- Torment\n\n"
            "NO HALO (Latios) @ Lum Berry\n"
            "Ability: Levitate\nLevel: 50\n"
            "EVs: 172 HP / 108 Def / 4 SpA / 4 SpD / 220 Spe\nTimid Nature\n"
            "IVs: 0 Atk\n- Substitute\n- Calm Mind\n- Recover\n- Dragon Claw"
        )
        team = from_paste(paste)
        print('>>> team = from_paste(paste)')
        for name, cs in team.items():
            print(f"  {name}: {cs}")
        print()

    return [ex_calc_stats, ex_stat_filter, ex_custom_set, ex_speed_compare, ex_paste]


# -- Category 3: Damage Calculator: Basics ------------------------------------

def cat_dmg_basics():
    def ex_frontier_vs_frontier():
        print("# Frontier set vs frontier set: Metagross-1 vs Tyranitar-1\n")
        for move in ["Earthquake", "Meteor Mash"]:
            res = calc_matchup(META, TTAR, move)
            show_matchup("META", "TTAR", move, res)

    def ex_custom_vs_frontier():
        print("# CustomSet vs frontier set: Timid 252 SpA Starmie vs Snorlax-1\n")
        for move in ["Surf", "Thunderbolt"]:
            res = calc_matchup(STARMIE, LAX, move)
            show_matchup("STARMIE", "LAX", move, res)

    def ex_super_effective():
        print("# Super effective: Starmie Surf vs Tyranitar (4x SE)\n")
        res = calc_matchup(STARMIE, TTAR, "Surf")
        show_matchup("STARMIE", "TTAR", "Surf", res)

    def ex_lvl50():
        print("# Level 50, 15 IVs: Metagross-1 vs Swampert-1\n")
        print('>>> calc_matchup(META, SWAM, "Meteor Mash", atk_ivs=15, def_ivs=15, atk_level=50, def_level=50)')
        res = calc_matchup(META, SWAM, "Meteor Mash",
                           atk_ivs=15, def_ivs=15, atk_level=50, def_level=50)
        print(format_result(res, "Meteor Mash"))
        print()

    def ex_raw_api():
        print("# Raw API: damage_rolls + ko_chance\n")
        rolls = damage_rolls(META, TTAR, "Earthquake")
        show('damage_rolls(META, TTAR, "Earthquake")', rolls)
        hp = calc_stats(TTAR)["hp"]
        show('calc_stats(TTAR)["hp"]', hp)
        kos = ko_chance(rolls, hp)
        show('ko_chance(rolls, hp)', kos)

    return [ex_frontier_vs_frontier, ex_custom_vs_frontier,
            ex_super_effective, ex_lvl50, ex_raw_api]


# -- Category 4: Damage Calculator: Advanced ----------------------------------

def cat_dmg_advanced():
    def ex_weather():
        print("# Weather: Rain-boosted Surf vs Tyranitar\n")
        res = calc_matchup(STARMIE, TTAR, "Surf")
        show_matchup("STARMIE", "TTAR", "Surf", res)
        print('>>> calc_matchup(STARMIE, TTAR, "Surf", field=Field(weather="rain"))')
        res = calc_matchup(STARMIE, TTAR, "Surf", field=Field(weather="rain"))
        print(format_result(res, "Surf (Rain)"))
        print()

    def ex_screens():
        print("# Reflect: Metagross-1 EQ vs Steelix-1\n")
        res = calc_matchup(META, STEELIX, "Earthquake")
        show_matchup("META", "STEELIX", "Earthquake", res)
        print('>>> calc_matchup(META, STEELIX, "Earthquake", field=Field(reflect=True))')
        res = calc_matchup(META, STEELIX, "Earthquake", field=Field(reflect=True))
        print(format_result(res, "Earthquake (Reflect)"))
        print()

    def ex_choice_band():
        print("# Choice Band: Adamant CB Heracross Megahorn vs Alakazam-1\n")
        res = calc_matchup(HERA, ZAM, "Megahorn")
        show_matchup("HERA", "ZAM", "Megahorn", res)

    def ex_stat_boosts():
        print("# Stat boosts: Salamence-1 EQ vs Tyranitar-1\n")
        res = calc_matchup(SALA, TTAR, "Earthquake")
        show_matchup("SALA", "TTAR", "Earthquake", res)
        print('>>> calc_matchup(SALA, TTAR, "Earthquake", atk_boosts={"atk": 1})')
        res = calc_matchup(SALA, TTAR, "Earthquake", atk_boosts={"atk": 1})
        print(format_result(res, "Earthquake (+1 Atk)"))
        print()

    def ex_crit():
        print("# Critical hits: Alakazam-1 Psychic vs Heracross\n")
        res = calc_matchup(ZAM, HERA, "Psychic")
        show_matchup("ZAM", "HERA", "Psychic", res)
        print('>>> calc_matchup(ZAM, HERA, "Psychic", critical=True)')
        res = calc_matchup(ZAM, HERA, "Psychic", critical=True)
        print(format_result(res, "Psychic (crit)"))
        print()

    def ex_crit_ignores_boosts():
        print("# Crit ignoring +2 Def: Salamence-1 EQ vs Snorlax-1\n")
        print('>>> calc_matchup(SALA, LAX, "Earthquake", def_boosts={"def": 2})')
        res = calc_matchup(SALA, LAX, "Earthquake", def_boosts={"def": 2})
        print(format_result(res, "Earthquake vs +2 Def"))
        print()
        print('>>> calc_matchup(SALA, LAX, "Earthquake", def_boosts={"def": 2}, critical=True)')
        res = calc_matchup(SALA, LAX, "Earthquake", def_boosts={"def": 2}, critical=True)
        print(format_result(res, "Earthquake vs +2 Def (crit ignores)"))
        print()

    def ex_leftovers():
        print("# KO calc with Leftovers: Metagross-1 vs Careful Snorlax\n")
        lax_c = CustomSet("Snorlax", nature="Careful", evs=[252,0,252,0,4,0],
                          item="Leftovers", ability="Thick Fat")
        hp = lax_c.get_stats()["hp"]
        recovery = hp // 16
        show('lax_c.get_stats()["hp"]', hp)
        show('recovery = hp // 16', recovery)
        print(f'>>> calc_matchup(META, lax_c, "Meteor Mash", recovery={recovery})')
        res = calc_matchup(META, lax_c, "Meteor Mash", recovery=recovery)
        print(format_result(res, "Meteor Mash"))
        print()

    def ex_immunity():
        print("# Ability immunities: EQ vs Levitate\n")
        res = calc_matchup(META, GENGAR, "Earthquake")
        show_matchup("META", "GENGAR", "Earthquake", res)

    return [ex_weather, ex_screens, ex_choice_band, ex_stat_boosts,
            ex_crit, ex_crit_ignores_boosts, ex_leftovers, ex_immunity]


# -- Category 5: Special Moves ------------------------------------------------

def cat_special_moves():
    def ex_fixed_damage():
        print("# Fixed-damage moves\n")
        show_matchup("LAX", "META", "Dragon Rage",
                     calc_matchup(LAX, META, DRAGON_RAGE))
        show_matchup("META", "GENGAR", "SonicBoom",
                     calc_matchup(META, GENGAR, SONIC_BOOM))
        show_matchup("LAX", "META", "Seismic Toss",
                     calc_matchup(LAX, META, SEISMIC_TOSS))
        show_matchup("GENGAR", "LAX", "Night Shade",
                     calc_matchup(GENGAR, LAX, NIGHT_SHADE))

    def ex_super_fang():
        print("# Super Fang: half of target's current HP\n")
        lax_hp = calc_stats(LAX)["hp"]
        show('calc_stats(LAX)["hp"]', lax_hp)
        show_matchup("META", "LAX", "Super Fang",
                     calc_matchup(META, LAX, SUPER_FANG))
        print('>>> calc_matchup(META, LAX, SUPER_FANG, def_current_hp=100)')
        res = calc_matchup(META, LAX, SUPER_FANG, def_current_hp=100)
        print(format_result(res, "Super Fang (100 HP left)"))
        print()

    def ex_endeavor():
        print("# Endeavor: target HP minus attacker HP\n")
        print('>>> calc_matchup(ZAM, LAX, ENDEAVOR, atk_current_hp=1)')
        res = calc_matchup(ZAM, LAX, ENDEAVOR, atk_current_hp=1)
        print(format_result(res, "Endeavor (Alakazam at 1 HP)"))
        print()

    def ex_eruption():
        print("# Eruption: 150 x currentHP/maxHP\n")
        groudon = CustomSet("Groudon", nature="Modest", evs=[0,0,0,252,4,252],
                            moves=["Eruption"])
        g_hp = groudon.get_stats()["hp"]
        show('groudon.get_stats()["hp"]', g_hp)
        show_matchup("groudon", "META", "Eruption",
                     calc_matchup(groudon, META, ERUPTION))
        print(f'>>> calc_matchup(groudon, META, ERUPTION, atk_current_hp={g_hp // 2})')
        res = calc_matchup(groudon, META, ERUPTION, atk_current_hp=g_hp // 2)
        print(format_result(res, "Eruption (50% HP)"))
        print()
        print('>>> calc_matchup(groudon, META, ERUPTION, atk_current_hp=1)')
        res = calc_matchup(groudon, META, ERUPTION, atk_current_hp=1)
        print(format_result(res, "Eruption (1 HP)"))
        print()

    def ex_flail():
        print("# Flail: power scales inversely with HP\n")
        show_matchup("LAX", "ZAM", "Flail",
                     calc_matchup(LAX, ZAM, FLAIL))
        print('>>> calc_matchup(LAX, ZAM, FLAIL, atk_current_hp=1)')
        res = calc_matchup(LAX, ZAM, FLAIL, atk_current_hp=1)
        print(format_result(res, "Flail (1 HP, 200 BP)"))
        print()

    def ex_low_kick():
        print("# Low Kick: power based on target weight\n")
        show_matchup("HERA", "LAX", "Low Kick",
                     calc_matchup(HERA, LAX, LOW_KICK))
        show_matchup("HERA", "ZAM", "Low Kick",
                     calc_matchup(HERA, ZAM, LOW_KICK))

    def ex_psywave():
        print("# Psywave: random level-based damage (11 rolls)\n")
        show_matchup("ZAM", "LAX", "Psywave",
                     calc_matchup(ZAM, LAX, PSYWAVE))

    def ex_multi_hit():
        print("# Multi-hit moves\n")
        show('get_hit_info(DOUBLE_KICK)', get_hit_info(DOUBLE_KICK))
        show('get_hit_info(BULLET_SEED)', get_hit_info(BULLET_SEED))
        show_matchup("HERA", "TTAR", "Double Kick",
                     calc_matchup(HERA, TTAR, DOUBLE_KICK))

    return [ex_fixed_damage, ex_super_fang, ex_endeavor, ex_eruption,
            ex_flail, ex_low_kick, ex_psywave, ex_multi_hit]


# -- Category 6: OHKO Filters -------------------------------------------------

def cat_ohko():
    def ex_will_ohko():
        print("# willOHKO: guaranteed OHKO (min roll kills)\n")
        show('db.sets.willOHKO(ZAM)', db.sets.willOHKO(ZAM))

    def ex_can_ohko():
        print("# canOHKO: can OHKO (at least one roll kills)\n")
        show('db.sets.canOHKO(LAX)', db.sets.canOHKO(LAX))

    def ex_dies_to():
        print("# diesTo: Normal-types that Metagross-1 guaranteed OHKOs\n")
        show('db.sets.hasType("Normal").diesTo(META)',
             db.sets.hasType("Normal").diesTo(META))

    def ex_can_die_to():
        print("# canDieTo: sets Alakazam-1 can OHKO on max roll\n")
        show('db.sets.canDieTo(ZAM)', db.sets.canDieTo(ZAM))

    def ex_negated():
        print("# Negated OHKO filters\n")
        show('db.sets.hasMove("earthquake").Not.willOHKO(TTAR)',
             db.sets.hasMove("earthquake").Not.willOHKO(TTAR))
        show('db.sets.Not.canDieTo(HERA)',
             db.sets.Not.canDieTo(HERA))

    def ex_with_boosts():
        print("# OHKO with stat boosts: Metagross-1 at +1 Atk\n")
        show('db.sets.diesTo(META, atk_boosts={"atk": 1})',
             db.sets.diesTo(META, atk_boosts={"atk": 1}))

    def ex_with_ivs():
        print("# OHKO with different IVs for attacker/defender\n")
        show('db.sets.diesTo(META, atk_ivs=31, def_ivs=3)',
             db.sets.diesTo(META, atk_ivs=31, def_ivs=3))
        show('db.sets.willOHKO(TTAR, include_acc=True)',
             db.sets.willOHKO(TTAR, include_acc=True))

    return [ex_will_ohko, ex_can_ohko, ex_dies_to,
            ex_can_die_to, ex_negated, ex_with_boosts, ex_with_ivs]


# -- Category 7: Battle Tower -------------------------------------------------

def cat_tower():
    def ex_tiers():
        print("# Trainer tiers: index -> IVs, rounds, last-in-round\n")
        for idx in [50, 130, 200, 250]:
            show(f'get_tier({idx})', get_tier(idx))
        show('BRAIN_IVS', BRAIN_IVS)

    def ex_round_filter():
        print("# Round filtering\n")
        show('tower.trainers.appearsInRound(8)',
             tower.trainers.appearsInRound(8))
        show('tower.trainers.canBeLastInRound(7)',
             tower.trainers.canBeLastInRound(7))
        show('tower.trainers.appearsInRound(8).hasPokemon("Metagross")',
             tower.trainers.appearsInRound(8).hasPokemon("Metagross"))
        show('tower.trainers.appearsInRound(8).Not.hasPokemon("Starmie")',
             tower.trainers.appearsInRound(8).Not.hasPokemon("Starmie"))

    def ex_random_team():
        print("# Random team generation\n")
        for _ in range(3):
            show('tower.random_team(8)', tower.random_team(8))
        show('tower.random_team(8, trainer_class="Dragon Tamer")',
             tower.random_team(8, trainer_class="Dragon Tamer"))
        show('tower.random_team(name="Brady")',
             tower.random_team(name="Brady"))
        show('tower.random_team(8, trainer_class="Nobody Real")',
             tower.random_team(8, trainer_class="Nobody Real"))

    return [ex_tiers, ex_round_filter, ex_random_team]


# -- Category 8: Battle Factory -----------------------------------------------

def cat_factory():
    def ex_groups():
        print("# Set groups: index -> group number\n")
        for idx in [150, 300, 500, 700, 860]:
            show(f'get_group({idx})', get_group(idx))
        show('len(fac.sets_in_groups([7, 8, 9]))',
             len(fac.sets_in_groups([7, 8, 9])))

    def ex_type_phrase():
        print("# Team type and phrase\n")
        ids, typ, phrase = fac.random_team("open", 5)
        print(f'>>> ids, typ, phrase = fac.random_team("open", 5)')
        print(f'  ids = {ids}')
        print(f'  typ = {typ!r}')
        print(f'  phrase = {phrase!r}')
        print()

    def ex_random_unconstrained():
        print("# Random teams (unconstrained)\n")
        for label, (level, rnd) in [("open, 5", ("open", 5)), ("lv50, 1", ("lv50", 1))]:
            ids, typ, phrase = fac.random_team(level, rnd)
            print(f'>>> fac.random_team("{level}", {rnd})')
            print(f'  ({ids}, {typ!r}, {phrase!r})')
            print()

    def ex_random_constrained():
        print("# Random teams (constrained)\n")
        ids, typ, phrase = fac.random_team("open", 5, target_type="Water")
        print('>>> fac.random_team("open", 5, target_type="Water")')
        print(f'  ({ids}, {typ!r}, {phrase!r})')
        print()
        ids, typ, phrase = fac.random_team("open", 5, target_phrase=4)
        print('>>> fac.random_team("open", 5, target_phrase=4)')
        print(f'  ({ids}, {typ!r}, {phrase!r})')
        print()
        ids, typ, phrase = fac.random_team("open", 5, target_type="Fire", target_phrase=1)
        print('>>> fac.random_team("open", 5, target_type="Fire", target_phrase=1)')
        print(f'  ({ids}, {typ!r}, {phrase!r})')
        print()

    return [ex_groups, ex_type_phrase, ex_random_unconstrained, ex_random_constrained]


# -- Category 9: Battle Dome --------------------------------------------------

def cat_dome():
    def ex_basic_seed():
        print("# Basic seeding\n")
        team = [META, LAX, TTAR]
        show('calc_seed([META, LAX, TTAR])', calc_seed(team))

    def ex_enemy_bugs():
        print("# Enemy seeding bugs: 0 EVs + non-HP stats mod 256\n")
        team = [META, LAX, TTAR]
        show('calc_seed([META, LAX, TTAR])', calc_seed(team))
        show('calc_seed([META, LAX, TTAR], is_enemy=True)',
             calc_seed(team, is_enemy=True))

    def ex_lv50():
        print("# Level 50, 15 IVs\n")
        team = [META, LAX, TTAR]
        show('calc_seed(team, level=50, ivs=15)',
             calc_seed(team, level=50, ivs=15))
        show('calc_seed(team, level=50, ivs=15, is_enemy=True)',
             calc_seed(team, level=50, ivs=15, is_enemy=True))

    def ex_custom_set():
        print("# CustomSet in player teams\n")
        my_meta = CustomSet("Metagross", nature="Adamant",
                            evs=[252, 252, 0, 0, 4, 0], item="Choice Band")
        show('my_meta', my_meta)
        show('calc_seed([my_meta, LAX, TTAR])',
             calc_seed([my_meta, LAX, TTAR]))

    def ex_monte_carlo():
        print("# Monte Carlo: highest enemy seed across 1000 random round 8 teams\n")
        set_lookup = {f"{s['Pokemon']}-{s['SetNum']}": s for s in db._sets}
        best_seed = 0
        best_team_str = ""
        n_samples = 1000
        for _ in range(n_samples):
            result = tower.random_team(8)
            if result.startswith("Error"):
                continue
            label, ids_str = result.split(": ", 1)
            set_ids = [s.strip() for s in ids_str.split(", ")]
            team_sets = [set_lookup[sid] for sid in set_ids if sid in set_lookup]
            if len(team_sets) != 3:
                continue
            seed = calc_seed(team_sets, is_enemy=True)
            if seed > best_seed:
                best_seed = seed
                best_team_str = result
        print(f"  Sampled {n_samples} random round 8 enemy teams")
        print(f"  Highest enemy seed: {best_seed}")
        print(f"  Team: {best_team_str}")
        print()

    return [ex_basic_seed, ex_enemy_bugs, ex_lv50, ex_custom_set, ex_monte_carlo]


# -- Category 10: Battle Palace ------------------------------------------------

def cat_palace():
    def ex_move_cats():
        print("# Move categories: attack, defense, support\n")
        for m in ["Earthquake", "Swords Dance", "Thunder Wave", "Surf", "Protect", "Toxic"]:
            show(f'get_move_category("{m}")', get_move_category(m))
        show('categorize_moveset(["Earthquake", "Rock Slide", "Swords Dance", "Thunder Wave"])',
             categorize_moveset(["Earthquake", "Rock Slide", "Swords Dance", "Thunder Wave"]))

    def ex_nature_ratios():
        print("# Nature ratios: category selection odds at high/low HP\n")
        for nature in ["Adamant", "Brave", "Jolly", "Sassy"]:
            show(f'get_nature_ratios("{nature}")',
                 get_nature_ratios(nature))
            show(f'get_nature_ratios("{nature}", low_hp=True)',
                 get_nature_ratios(nature, low_hp=True))

    def ex_action_probs():
        print("# Effective action probabilities\n")
        print("# Nature picks category, then 1/N within that category.")
        print("# Empty category: 50% random move, 50% nothing.\n")
        moves = ["Earthquake", "Rock Slide", "Swords Dance", "Protect"]
        show(f'get_action_probabilities("Adamant", {moves})',
             get_action_probabilities("Adamant", moves))

    def ex_move_probs():
        print("# Per-move probabilities\n")
        moves = ["Earthquake", "Rock Slide", "Protect"]
        show(f'get_move_probabilities("Adamant", {moves})',
             get_move_probabilities("Adamant", moves))

    def ex_multi_turn():
        print("# Multi-turn analysis by category\n")
        moves = ["Earthquake", "Rock Slide", "Swords Dance", "Protect"]
        show(f'multi_turn_probabilities("Adamant", moves, 5)',
             multi_turn_probabilities("Adamant", moves, 5))
        show(f'cumulative_attack_prob("Adamant", moves, 5, 3)',
             cumulative_attack_prob("Adamant", moves, 5, 3))
        show(f'expected_attacks("Adamant", moves, 5)',
             expected_attacks("Adamant", moves, 5))

    def ex_move_multi_turn():
        print("# Multi-turn analysis by specific move\n")
        moves = ["Earthquake", "Rock Slide", "Swords Dance", "Protect"]
        show(f'move_turn_probabilities("Adamant", moves, 5, "Earthquake")',
             move_turn_probabilities("Adamant", moves, 5, "Earthquake"))

    def ex_rank_natures():
        print("# Rank all 25 natures by attack probability\n")
        moves = ["Earthquake", "Rock Slide", "Protect"]
        ranking = rank_natures(moves)
        show(f'rank_natures({moves})', ranking)

    def ex_low_hp_msg():
        print("# Low HP messages and doubles targeting\n")
        for nature in ["Adamant", "Brave", "Timid", "Hardy"]:
            show(f'low_hp_message("{nature}", "Metagross")',
                 low_hp_message(nature, "Metagross"))
            show(f'DOUBLES_TARGETING["{nature.lower()}"]',
                 DOUBLES_TARGETING[nature.lower()])

    return [ex_move_cats, ex_nature_ratios, ex_action_probs, ex_move_probs,
            ex_multi_turn, ex_move_multi_turn, ex_rank_natures, ex_low_hp_msg]


# -- Category 11: Battle Pike -------------------------------------------------

def cat_pike():
    def ex_events():
        print("# Room events\n")
        show('EVENTS', EVENTS)

    def ex_event_probs():
        print("# Event probabilities\n")
        show('get_event_probabilities()',
             get_event_probabilities())
        show('get_event_probabilities(all_full_hp=False)',
             get_event_probabilities(all_full_hp=False))
        show('get_event_probabilities(num_fainted=2, all_full_hp=False)',
             get_event_probabilities(num_fainted=2, all_full_hp=False))
        show('get_event_probabilities(all_living_statused=True)',
             get_event_probabilities(all_living_statused=True))

    def ex_status():
        print("# Status room: chances accounting for immunities\n")
        for p in [1, 6, 11]:
            show(f'status_targets({p})', status_targets(p))
        print()
        types = [["steel", "psychic"], ["normal"], ["dragon", "psychic"]]
        abilities = ["clearbody", "intimidate", "levitate"]
        print(f"# Example team: Metagross / Tauros / Latios")
        show(f'get_status_chances({types}, {abilities}, pass_num=1)',
             get_status_chances(types, abilities, pass_num=1))

    def ex_wild():
        print("# Wild Pokemon encounters\n")
        for room in [100, 300, 600, 900]:
            show(f'get_wild_pokemon({room}, lv50=True)',
                 get_wild_pokemon(room, lv50=True))

    def ex_hints():
        print("# Path hints\n")
        show('HINTS', HINTS)

    return [ex_events, ex_event_probs, ex_status, ex_wild, ex_hints]


# -- Category 12: Battle Pyramid ----------------------------------------------

def cat_pyramid():
    def ex_themes():
        print("# Round themes\n")
        show('ROUND_THEMES', ROUND_THEMES)

    def ex_encounters():
        print("# Floor encounters: round 1, floors 1 and 7\n")
        show('get_encounters(1, 1)', get_encounters(1, 1))
        show('get_encounters(1, 7)', get_encounters(1, 7))

    def ex_floor_rates():
        print("# Floor encounter rates (per step)\n")
        for floor in range(1, 8):
            show(f'get_floor_encounter_rate({floor})',
                 get_floor_encounter_rate(floor))

    def ex_slot_table():
        print("# Encounter slot table\n")
        show('SLOT_RATES', SLOT_RATES)
        for floor in [1, 4, 7]:
            show(f'FLOOR_TABLE[{floor}]', FLOOR_TABLE[floor])

    def ex_items():
        print("# Floor items\n")
        show('get_items(1, 1)', get_items(1, 1))
        show('get_pickup_items(1)', get_pickup_items(1))

    return [ex_themes, ex_encounters, ex_floor_rates, ex_slot_table, ex_items]


# -- Menu system ---------------------------------------------------------------

CATEGORIES = [
    ("Database & Set Filters",        cat_database),
    ("Stats, Speed & Paste Import",   cat_stats),
    ("Damage Calculator: Basics",     cat_dmg_basics),
    ("Damage Calculator: Advanced",   cat_dmg_advanced),
    ("Special & Variable-Power Moves", cat_special_moves),
    ("OHKO Filters",                  cat_ohko),
    ("Battle Tower",                  cat_tower),
    ("Battle Factory",                cat_factory),
    ("Battle Dome",                   cat_dome),
    ("Battle Palace",                 cat_palace),
    ("Battle Pike",                   cat_pike),
    ("Battle Pyramid",               cat_pyramid),
]


def run_category(name, examples):
    header(name)
    for i, ex_fn in enumerate(examples, 1):
        ex_fn()
        if i < len(examples):
            try:
                pause()
            except (EOFError, KeyboardInterrupt):
                return


def show_menu():
    print(f"\n{'=' * WIDTH}")
    print(f"  frontierbrain3: Interactive Demo")
    print(f"{'=' * WIDTH}")
    for i, (name, _) in enumerate(CATEGORIES, 1):
        print(f"  {i:2d}. {name}")
    print()
    print(f"   a. Run all")
    print(f"   q. Quit")
    print(f"{'=' * WIDTH}")


def main():
    while True:
        show_menu()
        choice = input("\n  Select: ").strip().lower()

        if choice == "q":
            print("  Bye!")
            break

        if choice == "a":
            for name, builder in CATEGORIES:
                examples = builder()
                run_category(name, examples)
                try:
                    pause()
                except (EOFError, KeyboardInterrupt):
                    break
            continue

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(CATEGORIES):
                name, builder = CATEGORIES[idx]
                examples = builder()
                run_category(name, examples)
            else:
                print("  Invalid selection.")
        except ValueError:
            print("  Invalid selection.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  Bye!")
        sys.exit(0)