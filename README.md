# frontierbrain3

A Python toolkit for analyzing Pokemon Emerald's Battle Frontier. Covers damage calculation, set/trainer querying, and facility-specific mechanics for the Tower, Factory, Dome, Palace, Pike, and Pyramid.

## Installation

```bash
pip install frontierbrain3
```

Alternatively, clone the repository and install locally:

```bash
git clone https://github.com/yourname/frontierbrain3.git
cd frontierbrain3
pip install -e .
```

## Quick Start

```python
from frontierbrain3 import Database, CustomSet, calc_matchup, format_result

db = Database()

# Find all Water-types with Surf
water_surfers = db.sets.hasType("Water").hasMove("surf")
print(f"{len(water_surfers)} sets")  # SetCollection with .ids(), iteration, etc.

# Damage calc: custom attacker vs frontier defender
starmie = CustomSet("Starmie", nature="Timid", evs=[0,0,0,252,4,252],
                    moves=["Surf", "Thunderbolt", "Ice Beam", "Psychic"])
ttar = db.allSets("Tyranitar")._sets[0]

result = calc_matchup(starmie, ttar, "Surf")
print(format_result(result, "Surf"))
```

## Package Structure

```
frontierbrain3/
├── __init__.py          # Re-exports core API
├── frontierutils.py     # CustomSet, stats, types, paste import
├── frontier_db.py       # Database, SetCollection, TrainerCollection
├── damagecalc.py        # Damage formula, KO probability
├── data/
│   ├── pokemon.json     # Species data (stats, types, weight, abilities)
│   ├── bf_pokemon.json  # All frontier sets (882 regular + 36 Frontier Brain)
│   ├── bf_trainers.json # All 300+ trainers (includes Frontier Brains)
│   ├── moves.json       # Move data (type, power, accuracy, etc.)
│   ├── items.json       # Item names/IDs
│   └── abilities.json   # Ability names/IDs
└── facilities/
    ├── tower.py         # Trainer tiers, TowerDatabase
    ├── factory.py       # Team type/phrase, FactoryDatabase
    ├── dome.py          # Seeding formula
    ├── palace.py        # Nature-based move selection
    ├── pike.py          # Events, status, wild Pokemon, hints
    ├── pyramid.py       # Wild encounters, items, round themes
    └── arena.py         # Placeholder (no mechanics to model)
```

---

## Core Concepts

### Frontier Sets

The package includes data for all 918 Battle Frontier Pokemon sets (882 regular sets plus 36 Frontier Brain sets). Each set is a dict with the following structure:

```json
{
    "Pokemon": "Sunkern",
    "SetNum": 1,
    "Nature": "Relaxed",
    "Item": "Lax Incense",
    "Abilities": ["Chlorophyll"],
    "Moves": ["megadrain", "helpinghand", "sunnyday", "lightscreen"],
    "EVs": [255, 0, 0, 255, 0, 0],
    "Index": 1,
    "DexNum": 191
}
```

EVs are ordered `[HP, Atk, Def, SpA, SpD, Spe]`. The `Index` field determines which facility tiers/groups the set belongs to (see Tower and Factory sections). Sets are referenced by ID strings like `"Sunkern-1"`, `"Metagross-4"`, etc.

You can access sets directly through the database:

```python
from frontierbrain3 import Database

db = Database()

db.allSets("Charizard")        # SetCollection of all Charizard sets
db.allSets("Charizard").ids()  # ["Charizard-1", "Charizard-2", ...]

# Access the raw set dict
meta = db.allSets("Metagross")._sets[0]
print(meta["Nature"], meta["Item"], meta["Moves"])
```

### CustomSet

Represents a player-defined Pokemon with full control over species, nature, EVs, IVs, level, item, ability, and moves. Used as attacker/defender in damage calcs and as a speed benchmark in queries.

```python
from frontierbrain3 import CustomSet

flygon = CustomSet(
    "Flygon",
    nature="Jolly",
    evs=[4, 252, 0, 0, 0, 252],
    ivs=31,            # int (all same) or list of 6
    level=100,
    item="Choice Band",
    ability="Levitate",
    moves=["Earthquake", "Rock Slide", "Fire Blast", "Return"],
)

flygon.get_stats()  # {'hp': ..., 'atk': ..., 'def': ..., 'spa': ..., 'spd': ..., 'spe': ...}
flygon.speed()      # shorthand for get_stats()["spe"]
```

The `stats` parameter lets you override calculated stats with exact values if needed:

```python
custom = CustomSet("Flygon", stats={"hp": 302, "atk": 299, "def": 196, "spa": 176, "spd": 196, "spe": 328})
```

### Pokepaste Import

Import teams from [Pokepaste](https://pokepast.es/) format:

```python
from frontierbrain3 import from_paste

# From a string
team = from_paste("""
Skarmory (M) @ Leftovers
Ability: Sturdy
EVs: 252 HP / 252 Def / 4 SpD
Bold Nature
- Spikes
- Whirlwind
- Protect
- Rest
""")

for name, cs in team.items():
    print(f"{name}: {cs.pokemon}, speed={cs.speed()}")
```

---

## Core Utilities (`frontierutils`)

### Stat Calculations

```python
from frontierbrain3 import calc_stats, Database

db = Database()
alakazam = db.allSets("Alakazam")._sets[0]

calc_stats(alakazam)                    # 31 IVs, lv100 (defaults)
calc_stats(alakazam, ivs=15)            # 15 IVs, lv100
calc_stats(alakazam, ivs=15, level=50)  # 15 IVs, lv50
calc_stats(alakazam, ivs=[31,31,31,0,31,31])  # per-stat IVs
```

---

## Database (`frontier_db`)

### Loading

```python
from frontierbrain3 import Database

db = Database()  # loads from default data/ paths

db.sets       # SetCollection of all 918 frontier sets (882 regular + 36 Frontier Brain)
db.trainers   # TrainerCollection of all trainers (300 regular + Frontier Brains)
```

### SetCollection

All filter methods return a new `SetCollection`, so they chain freely. Every `SetCollection` supports `len()`, iteration, `.ids()` (returns `["Pokemon-SetNum", ...]`), and `.Not` for negation.

#### Type Filters

```python
db.sets.hasType("Water")        # pure or part Water type
db.sets.hasType("Psychic/")     # pure Psychic only (trailing slash)
db.sets.hasType("Fire/Flying")  # must have both Fire and Flying
```

#### Move Filters

```python
db.sets.hasMove("surf")                        # has Surf
db.sets.hasMove("earthquake", "surf")           # has EQ OR Surf (default match="any")
db.sets.hasMove("calmmind", "surf", match="all")  # has BOTH Calm Mind AND Surf
```

#### Item, Nature, Ability Filters

```python
db.sets.hasItem("Choice Band")
db.sets.hasItem("Leftovers", "Shell Bell")  # has either item
db.sets.hasNature("Adamant")
db.sets.hasAbility("Intimidate")
```

#### Stat Filters

Filter by calculated stat value. Specify `ivs` and `level` to match the format you're analyzing.

```python
db.sets.statFilter("atk", min=300)                      # 300+ Atk at 31 IVs, lv100
db.sets.statFilter("spe", min=200, max=250)              # speed in range
db.sets.statFilter("spa", min=150, level=50, ivs=15)     # lv50, 15 IVs
```

#### Speed Comparisons

Compare frontier sets against a `CustomSet` benchmark:

```python
my_flygon = CustomSet("Flygon", nature="Jolly", evs=[4, 252, 0, 0, 0, 252])

db.sets.fasterThan(my_flygon)                # sets that outspeed it at 31 IVs
db.sets.slowerThan(my_flygon)                # sets it outspeeds
db.sets.speedTieWith(my_flygon)              # exact ties
db.sets.fasterThan(my_flygon, ivs=15)        # enemy sets at 15 IVs
```

#### OHKO Filters

These run the full damage calculator for every set in the collection. The attacker/defender can be a frontier set dict or a `CustomSet`.

```python
zam = db.allSets("Alakazam")._sets[0]
lax = db.allSets("Snorlax")._sets[0]

# Sets that GUARANTEED OHKO Alakazam-1 (min roll kills)
db.sets.willOHKO(zam)

# Sets that CAN OHKO Snorlax-1 (at least one roll kills)
db.sets.canOHKO(lax)

# Sets where at least 50% of rolls OHKO
db.sets.canOHKO(lax, min_chance=0.5)

# Normal-types that Metagross-1 guaranteed OHKOs (each set is the defender)
meta = db.allSets("Metagross")._sets[0]
db.sets.hasType("Normal").diesTo(meta)

# Sets that a custom Starmie can OHKO on at least one roll
starmie = CustomSet("Starmie", nature="Timid", evs=[0,0,0,252,4,252],
                    moves=["Surf", "Psychic", "Thunderbolt", "Ice Beam"])
db.sets.canDieTo(starmie)
```

Specify IVs for the attacker and defender independently, useful for analyzing player sets (31 IVs) against frontier enemies (3-31 IVs depending on tier):

```python
# Frontier sets at 3 IVs that a 31 IV Metagross-1 guaranteed OHKOs
db.sets.diesTo(meta, atk_ivs=31, def_ivs=3)

# Frontier sets at 31 IVs that can OHKO a 15 IV Alakazam-1
db.sets.canOHKO(zam, atk_ivs=31, def_ivs=15)
```

Other optional parameters are passed through to the damage calculator:

```python
from frontierbrain3 import Field

# With stat boosts
db.sets.diesTo(meta, atk_boosts={"atk": 1})

# With weather
ttar = db.allSets("Tyranitar")._sets[0]
db.sets.willOHKO(ttar, field=Field(weather="rain"))

# Include OHKO moves (Guillotine, Fissure, etc.)
db.sets.canOHKO(lax, include_ohko=True)

# Factor accuracy into guaranteed OHKOs (excludes imperfect-accuracy moves like Cross Chop)
db.sets.willOHKO(ttar, include_acc=True)
```

#### Negation

Every filter has a negated form via `.Not`:

```python
ttar = db.allSets("Tyranitar")._sets[0]
hera = CustomSet("Heracross", nature="Adamant", evs=[4,252,0,0,0,252],
                 item="Choice Band", moves=["Megahorn", "Earthquake", "Brick Break", "Rock Slide"])

db.sets.hasMove("earthquake").Not.hasMove("surf")     # has EQ but not Surf
db.sets.Not.canDieTo(hera)                             # survives Heracross even on max roll
db.sets.hasMove("earthquake").Not.willOHKO(ttar)       # EQ users that don't guaranteed OHKO Ttar
```

#### Trainer Lookup

```python
# Which trainers use Water-type Surfers?
db.sets.hasType("Water").hasMove("surf").usedByTrainer()
```

### TrainerCollection

Supports `len()`, iteration, `.names()` (returns `["CLASS Name", ...]`), and `.Not`.

```python
db.trainers.hasPokemon("Charizard")                           # trainers with any Charizard set
db.trainers.hasPokemon("Charizard").Not.hasPokemon("Blastoise")  # Charizard but no Blastoise
db.trainers.hasSet("Metagross-4")                              # trainers with a specific set
```

---

## Damage Calculator (`damagecalc`)

Implements the Gen 3 damage formula, referencing [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Damage) and [turskain's Frontier Calc](https://turskain.github.io/). Handles all Gen 3 mechanics including the physical/special split by type, ability immunities, item boosts, weather, screens, crits, stat stages, and special moves.

The examples below assume this setup:

```python
from frontierbrain3 import (
    Database, CustomSet, damage_rolls, calc_matchup,
    format_result, ko_chance, calc_stats, Field,
)

db = Database()

meta = db.allSets("Metagross")._sets[0]
ttar = db.allSets("Tyranitar")._sets[0]
lax  = db.allSets("Snorlax")._sets[0]
zam  = db.allSets("Alakazam")._sets[0]
sala = db.allSets("Salamence")._sets[0]

starmie = CustomSet("Starmie", nature="Timid", evs=[0,0,0,252,4,252],
                    moves=["Surf", "Psychic", "Thunderbolt", "Ice Beam"])
hera = CustomSet("Heracross", nature="Adamant", evs=[4,252,0,0,0,252],
                 item="Choice Band", ability="Guts",
                 moves=["Megahorn", "Earthquake", "Brick Break", "Rock Slide"])
```

### Specifying Moves

Moves can be passed as a string name (looked up from `data/moves.json`):

```python
result = calc_matchup(meta, ttar, "Earthquake")
result = calc_matchup(starmie, ttar, "Surf")
```

All move properties, including special behavior for fixed-damage moves, variable-power moves, multi-hit moves, etc., are handled automatically based on the move name.

Alternatively, pass a dict with `name`, `type`, and `power` keys. This is useful for Hidden Power (where type/power vary per Pokemon) or for ROM hacks with custom moves:

```python
hp_grass = {"name": "HP Grass", "type": "grass", "power": 70}
result = calc_matchup(starmie, ttar, hp_grass)
```

### Basic Usage

```python
# damage_rolls: returns 16 per-hit damage values (one per random roll 85-100)
rolls = damage_rolls(meta, ttar, "Earthquake")

# calc_matchup: full summary with KO chances
result = calc_matchup(meta, ttar, "Earthquake")
print(format_result(result, "Earthquake"))
#   Earthquake: 186-220 (54.7% - 64.7%) [HP: 340]
#   0.0% chance to 1HKO
#   guaranteed 2HKO

# result dict keys:
#   rolls          - per-hit damage values (list[int])
#   attack_rolls   - combined multi-hit totals (None for single-hit moves)
#   hit_info       - {"type": "single"/"fixed"/"variable"/"triple_kick", ...}
#   min, max       - min/max total damage
#   min_pct, max_pct - as percentage of defender's max HP
#   defender_hp    - defender's current HP used for KO calc
#   defender_max_hp
#   ko_chances     - {1: prob, 2: prob, ...} up to guaranteed KO
```

### Raw API

For fine-grained control, use `damage_rolls` + `ko_chance` directly:

```python
rolls = damage_rolls(meta, ttar, "Earthquake")
ttar_hp = calc_stats(ttar)["hp"]
kos = ko_chance(rolls, ttar_hp)
# kos = {1: 0.0, 2: 0.875, 3: 1.0}

# With Leftovers recovery between hits
kos = ko_chance(rolls, ttar_hp, recovery=ttar_hp // 16)
```

### Attacker and Defender

Both can be either a frontier set dict (from the database) or a `CustomSet`:

```python
# Frontier set vs frontier set
calc_matchup(meta, ttar, "Earthquake")

# CustomSet vs frontier set
calc_matchup(starmie, lax, "Surf")

# Frontier set at non-default IVs/level
swam = db.allSets("Swampert")._sets[0]
calc_matchup(meta, swam, "Earthquake", atk_ivs=15, def_ivs=15, atk_level=50, def_level=50)
```

### Field Conditions

```python
from frontierbrain3 import Field

# Weather
calc_matchup(starmie, ttar, "Surf", field=Field(weather="rain"))

# Screens
calc_matchup(meta, ttar, "Earthquake", field=Field(reflect=True))

# Doubles
calc_matchup(starmie, ttar, "Surf", field=Field(is_doubles=True))

# Combine freely
Field(weather="rain", reflect=True, is_doubles=True)

# Other fields: helping_hand (1.5x), cloud_nine (suppresses weather)
```

### Stat Boosts

```python
# Dragon Dance (+1 Atk, +1 Spe; only Atk affects damage)
calc_matchup(sala, ttar, "Earthquake", atk_boosts={"atk": 1})

# Calm Mind on defender (+1 SpD)
calc_matchup(starmie, lax, "Surf", def_boosts={"spd": 1})

# Intimidate on attacker
calc_matchup(meta, zam, "Meteor Mash", atk_boosts={"atk": -1})

# Critical hits ignore negative atk stages and positive def stages
calc_matchup(sala, lax, "Earthquake", def_boosts={"def": 2}, critical=True)
```

### Status Conditions

```python
# Burn halves physical damage (unless Guts)
calc_matchup(meta, ttar, "Earthquake", atk_status="burn")

# Guts: burn boosts Attack instead
calc_matchup(hera, ttar, "Megahorn", atk_status="burn")

# Facade doubles power when statused
calc_matchup(meta, lax, "Facade", atk_status="burn")  # 140 BP

# Marvel Scale: defender's status boosts their Defense
milotic = db.allSets("Milotic")._sets[0]
calc_matchup(meta, milotic, "Earthquake", def_status="burn")
```

### Special Parameters

| Parameter | Effect |
|---|---|
| `critical=True` | Critical hit (2x, ignores negative atk boosts and positive def boosts) |
| `atk_ivs=N` / `def_ivs=N` | IVs for attacker/defender (default 31) |
| `atk_level=N` / `def_level=N` | Level for attacker/defender (default 100) |
| `atk_current_hp=N` | Attacker's current HP (for Eruption, Flail, Reversal, Endeavor) |
| `def_current_hp=N` | Defender's current HP (for Super Fang, Endeavor, KO calc) |
| `flash_fire_active=True` | Flash Fire boost active (1.5x Fire moves) |
| `charge_active=True` | Charge boost active (2x Electric moves) |
| `stockpile_count=N` | Stockpile count for Spit Up (100/200/300 BP) |
| `double_dmg=True` | Doubled damage (Pursuit on switch, Stomp vs Minimize, etc.) |
| `recovery=N` | HP recovered between each attack in KO calc (e.g. Leftovers) |
| `max_hits=N` | Max attacks to simulate in KO calc (default 8) |

### Fixed-Damage Moves

| Move | Damage |
|---|---|
| Dragon Rage | Always 40 |
| SonicBoom | Always 20 |
| Seismic Toss / Night Shade | Equal to user's level |
| Super Fang | Half of target's current HP |
| Endeavor | target's current HP minus attacker's current HP |
| Psywave | Random: level x (50-150)% (11 rolls instead of 16) |

All respect type immunities (Night Shade vs Normal, SonicBoom vs Ghost, etc.).

### Variable-Power Moves

| Move | Mechanic |
|---|---|
| Eruption / Water Spout | 150 x currentHP / maxHP (use `atk_current_hp`) |
| Flail / Reversal | 20-200 BP based on HP% (use `atk_current_hp`) |
| Low Kick | 20-120 BP based on target weight |
| Facade | 140 BP when statused, 70 otherwise (use `atk_status`) |
| Smelling Salt | 120 BP vs paralysis, 60 otherwise (use `def_status`) |
| Weather Ball | Type/power changes with active weather |
| Magnitude | Weighted average across all magnitudes |

### Multi-Hit Moves

The calculator handles multi-hit moves automatically:

- **Fixed 2-hit** (Double Kick, Bonemerang, Twineedle): convolves 2 hits
- **Variable 2-5 hit** (Bullet Seed, Rock Blast, etc.): weighted by Gen 3 distribution (3/8, 3/8, 1/8, 1/8)
- **Triple Kick** (10+20+30 power): convolves 3 different-power kicks

```python
from frontierbrain3.damagecalc import get_hit_info

get_hit_info("Double Kick")   # {"type": "fixed", "hits": 2}
get_hit_info("Bullet Seed")   # {"type": "variable", "weights": {2:3, 3:3, 4:1, 5:1}}
get_hit_info("Triple Kick")   # {"type": "triple_kick", "powers": [10,20,30], "acc": 0.9}
get_hit_info("Earthquake")    # {"type": "single"}
```

`calc_matchup` and the OHKO filters handle multi-hit convolution automatically. For manual use:

```python
from frontierbrain3.damagecalc import combine_multi_hit_rolls, multi_hit_ohko_prob

blaziken = db.allSets("Blaziken")._sets[0]
per_hit = damage_rolls(blaziken, lax, "Double Kick")
hit_info = get_hit_info("Double Kick")
total_rolls = combine_multi_hit_rolls(per_hit, hit_info)
ohko_prob = multi_hit_ohko_prob(per_hit, calc_stats(lax)["hp"], hit_info)
```

### Recoil and Drain Reference

Not applied in the damage formula (they don't affect the hit), but provided as constants for external calculations:

```python
from frontierbrain3.damagecalc import RECOIL_MOVES, DRAIN_MOVES

RECOIL_MOVES  # {"doubleedge": 1/3, "volttackle": 1/3, "submission": 1/4, ...}
DRAIN_MOVES   # {"gigadrain": 1/2, "absorb": 1/2, "dreameater": 1/2, ...}
```

---

## Battle Tower (`facilities.tower`)

### Trainer Tiers

Tower trainers are grouped into tiers by index, each with fixed IVs and round eligibility. These are the same trainers used across all Battle Frontier facilities, though details like round eligibility and team size may differ slightly between facilities. The Ruby/Sapphire Battle Tower uses a different trainer list that is not currently supported.

```python
from frontierbrain3.facilities.tower import TowerDatabase, get_tier, TIERS, BRAIN_IVS

get_tier(250)  # {"ivs": 31, "rounds": [8], "last_in_round": "any"}
get_tier(150)  # {"ivs": 15, "rounds": [3, 4, 5], "last_in_round": 3}

BRAIN_IVS  # {"silver": 15, "gold": 31}
```

### TowerDatabase

Extends `Database` with tower-specific trainer filtering:

```python
tower = TowerDatabase()

# Trainers that appear in round 8
tower.trainers.appearsInRound(8)

# Trainers eligible to be the last battle of round 7
tower.trainers.canBeLastInRound(7)

# Combine with base filters
tower.trainers.appearsInRound(8).hasPokemon("Metagross")
tower.trainers.appearsInRound(8).Not.hasPokemon("Starmie")
```

### Random Team Generation

Generates a random trainer + 3-set team respecting species and item clause:

```python
tower.random_team(8)                              # random round 8 team
tower.random_team(8, trainer_class="Dragon Tamer") # filtered by class
tower.random_team(name="Brady")                    # filtered by name (any round)
# Returns: "CLASS Name: SetId1, SetId2, SetId3"
```

---

## Battle Factory (`facilities.factory`)

Unlike the Tower, Factory sets are not tied to specific trainers. Any trainer can use any set from the eligible pool. The relevant unit of generation is the team itself (3 sets respecting species/item clause), not a trainer-team pair.

### Groups and Pools

Factory sets are divided into 9 groups by index. Each round draws from specific groups:

```python
from frontierbrain3.facilities.factory import FactoryDatabase, get_group

get_group(500)  # 5 (set index 500 is in group 5)

fac = FactoryDatabase()
pool = fac.sets_in_groups([4, 5, 6, 7, 8])  # all sets in these groups
```

### Team Type and Phrase

Every Factory team gets a "type" (most common Pokemon type) and a "phrase" (battle style description):

```python
from frontierbrain3.facilities.factory import FactoryDatabase, team_type, team_phrase

fac = FactoryDatabase()
sample_team = fac.sets_in_groups([7, 8])[:3]  # grab 3 sets for demonstration

team_type(sample_team)   # "Water", "Fire", "No Type", etc.
team_phrase(sample_team)  # "appears to be one based on total preparation", etc.
```

### Random Team Generation

Generate teams with optional type/phrase constraints:

```python
fac = FactoryDatabase()

ids, typ, phrase = fac.random_team("open", 5)                           # unconstrained
ids, typ, phrase = fac.random_team("open", 5, target_type="Water")       # Water teams only
ids, typ, phrase = fac.random_team("open", 5, target_phrase=4)           # phrase 4 only
ids, typ, phrase = fac.random_team("lv50", 1, target_type="Fire", target_phrase=1)  # both

# Phrase numbers: 0=none, 1=preparation, 2=slow/steady, 3=endurance,
# 4=high-risk, 5=weaken foe, 6=unpredictable, 7=battle flow, 8=flex
```

---

## Battle Dome (`facilities.dome`)

### Seeding

The Dome ranks teams by a seeding value. Higher seed = higher bracket position. Notably, the higher seed wins in case of a tie, unlike every other facility where a tie counts as a loss for the player.

```python
from frontierbrain3 import Database, CustomSet
from frontierbrain3.facilities.dome import calc_seed

db = Database()

meta = db.allSets("Metagross")._sets[0]
lax  = db.allSets("Snorlax")._sets[0]
ttar = db.allSets("Tyranitar")._sets[0]
team = [meta, lax, ttar]  # exactly 3 sets

# Player seed (normal stat calculation)
calc_seed(team)

# Enemy seed (applies two bugs: 0 EVs + non-HP stats mod 256)
calc_seed(team, is_enemy=True)

# At specific level/IVs
calc_seed(team, level=50, ivs=15)
calc_seed(team, level=50, ivs=15, is_enemy=True)
```

`CustomSet` objects are supported for player teams (not with `is_enemy=True`).

**Seeding formula:** `unique_types x (highest_level // 20) + sum(all stats)`

**Enemy bugs:**
1. Stats calculated with 0 EVs regardless of the set's actual EVs
2. Non-HP stats taken mod 256 (overflow)

### Monte Carlo: estimating the score needed for seed #1

The enemy seeding bugs massively favor the player, but it's useful to know how high an enemy seed can actually get. Since the Dome draws from the same trainer/set pool as the Tower, we can use `TowerDatabase` to simulate round 8 enemy teams:

```python
from frontierbrain3.facilities.tower import TowerDatabase
from frontierbrain3.facilities.dome import calc_seed

tower = TowerDatabase()
set_lookup = {f"{s['Pokemon']}-{s['SetNum']}": s for s in tower._sets}

best_seed = 0
best_team = ""
for _ in range(1000):
    result = tower.random_team(8)
    if result.startswith("Error"):
        continue
    label, ids_str = result.split(": ", 1)
    set_ids = [s.strip() for s in ids_str.split(", ")]
    team_sets = [set_lookup[sid] for sid in set_ids if sid in set_lookup]
    if len(team_sets) == 3:
        seed = calc_seed(team_sets, is_enemy=True)
        if seed > best_seed:
            best_seed = seed
            best_team = result

print(f"Highest enemy seed: {best_seed}")
print(f"Team: {best_team}")
```

---

## Battle Palace (`facilities.palace`)

In the Palace, Pokemon choose moves autonomously. Each turn, the game first selects a move **category** (Attack, Defense, or Support) based on the Pokemon's nature. Then it picks one of the Pokemon's moves in that category uniformly at random (1/N chance if the category has N moves). If the selected category has no move in the set, there is a 50% chance the Pokemon picks a random move from all its moves and a 50% chance it wastes its turn.

### Move Categories

Palace classifies every move as attack, defense, or support:

```python
from frontierbrain3.facilities.palace import get_move_category, categorize_moveset

get_move_category("Earthquake")  # "attack"
get_move_category("Swords Dance") # "defense"
get_move_category("Thunder Wave") # "support"

categorize_moveset(["Earthquake", "Rock Slide", "Swords Dance", "Thunder Wave"])
# {"attack": ["Earthquake", "Rock Slide"], "defense": ["Swords Dance"], "support": ["Thunder Wave"]}
```

### Nature Ratios

Each nature has different category selection odds at high HP (>50%) and low HP (<=50%):

```python
from frontierbrain3.facilities.palace import get_nature_ratios

get_nature_ratios("Adamant")              # {"attack": 0.38, "defense": 0.31, "support": 0.31}
get_nature_ratios("Adamant", low_hp=True) # {"attack": 0.70, "defense": 0.15, "support": 0.15}
```

### Effective Action Probabilities

Accounts for empty categories and the random-move fallback:

```python
from frontierbrain3.facilities.palace import get_action_probabilities, get_move_probabilities

# Per-category probabilities (including "nothing")
get_action_probabilities("Adamant", ["Earthquake", "Rock Slide", "Swords Dance", "Protect"])
# {"attack": 0.5..., "defense": 0.3..., "support": 0.0..., "nothing": 0.1...}

# Per-move probabilities
get_move_probabilities("Adamant", ["Earthquake", "Rock Slide", "Protect"])
# {"Earthquake": 0.25, "Rock Slide": 0.25, "Protect": 0.38, "nothing": 0.12}
```

### Multi-Turn Analysis

Analyze probabilities over multiple turns, either by category or by specific move:

```python
from frontierbrain3.facilities.palace import (
    multi_turn_probabilities, move_turn_probabilities,
    cumulative_attack_prob, expected_attacks, multi_turn_mixed_hp,
)

moves = ["Earthquake", "Rock Slide", "Swords Dance", "Protect"]

# P(exactly k attacks in 5 turns)
multi_turn_probabilities("Adamant", moves, 5)  # {0: p, 1: p, ..., 5: p}

# P(exactly k uses of Earthquake specifically in 5 turns)
move_turn_probabilities("Adamant", moves, 5, "Earthquake")  # {0: p, 1: p, ..., 5: p}

# P(at least 3 attacks in 5 turns)
cumulative_attack_prob("Adamant", moves, 5, 3)  # float

# Expected attacks in 5 turns
expected_attacks("Adamant", moves, 5)  # float

# Mixed HP: 3 turns at high HP, then 2 turns at low HP
multi_turn_mixed_hp("Adamant", moves, 3, 2)  # {0: p, ..., 5: p}
```

### Nature Rankings and Utilities

```python
from frontierbrain3.facilities.palace import rank_natures, low_hp_message, DOUBLES_TARGETING

# Rank all 25 natures by attack probability for a moveset
rank_natures(["Earthquake", "Rock Slide", "Protect"])
# [("Sassy", 0.88), ("Brave", 0.70), ...]

# Low HP flavor text
low_hp_message("Adamant", "Metagross")  # "A glint appears in Metagross's eyes!"

# Doubles targeting preference by nature
DOUBLES_TARGETING["adamant"]  # "higher_hp"
DOUBLES_TARGETING["brave"]    # "lower_hp"
```

---

## Battle Pike (`facilities.pike`)

### Room Events

8 possible events per room, with some conditionally excluded:

```python
from frontierbrain3.facilities.pike import get_event_probabilities, EVENTS

# All events and descriptions
EVENTS  # {"single_battle": "A Trainer with 3 Pokemon...", ...}

# Default: all at full HP, none fainted/statused
get_event_probabilities()
# {"single_battle": 0.1667, "double_battle": 0.1667, ... "partial_heal": 0.0, "full_heal": 0.0}

# With party damage
get_event_probabilities(all_full_hp=False)  # healing rooms now possible

# With 2 fainted (double battle excluded)
get_event_probabilities(num_fainted=2, all_full_hp=False)
```

### Status Room

```python
from frontierbrain3.facilities.pike import get_status_chances, status_targets, STATUS_TABLE

# How many mons targeted per pass
status_targets(1)   # 1 (passes 1-5)
status_targets(6)   # 2 (passes 6-10)
status_targets(11)  # 3 (passes 11+)

# Status probabilities accounting for immunities
# Example team: Metagross / Tauros / Latios
get_status_chances(
    pokemon_types=[["steel", "psychic"], ["normal"], ["dragon", "psychic"]],
    pokemon_abilities=["clearbody", "intimidate", "levitate"],
    pass_num=1,
)
# {"bad_poison": 0.233, "freeze": 0.25, "paralysis": 0.2, "sleep": 0.1, "burn": 0.1}
```

### Wild Pokemon

```python
from frontierbrain3.facilities.pike import get_wild_pokemon

get_wild_pokemon(100, lv50=True)   # rooms 1-280: Seviper, Milotic, Dusclops
get_wild_pokemon(300, lv50=True)   # rooms 281-560: Seviper, Milotic, Electrode
get_wild_pokemon(900, lv50=False)  # rooms 841+: Seviper, Milotic, Wobbuffet
```

### Hints

```python
from frontierbrain3.facilities.pike import HINTS

HINTS["nostalgia"]   # {"text": "...wave of nostalgia...", "events": ["status", "partial_heal"]}
HINTS["people"]      # {"text": "...presence of people...", "events": ["single_battle", "full_heal"]}
HINTS["aroma"]       # {"text": "...aroma of Pokemon...", "events": ["wild_pokemon", "hard_battle_heal"]}
HINTS["whispering"]  # {"text": "...heard something...", "events": ["no_event", "double_battle"]}
HINTS["dreadful"]    # {"text": "...dreadful presence...", "events": ["pike_queen"]}
```

---

## Battle Pyramid (`facilities.pyramid`)

### Round Themes and Wild Pokemon

20 rounds, each with a theme and 8 wild Pokemon:

```python
from frontierbrain3.facilities.pyramid import (
    ROUNDS, ROUND_THEMES, get_round_pokemon, get_encounters,
)

ROUND_THEMES  # {1: "paralysis", 2: "poison", ..., 20: "normal"}

# All 8 Pokemon for a round
get_round_pokemon(1)  # [{"species": "Plusle", "moves": [...], ...}, ...]

# Encounters for a specific floor (1-7) with rates
get_encounters(1, 3)  # [{"pokemon": {...}, "rate": 30}, {"pokemon": {...}, "rate": 50}, ...]
```

Encounter data includes species, ability, level ranges, and moves. Rounds cycle after 20 (round 21 = round 1, etc.).

### Floor Mechanics

```python
from frontierbrain3.facilities.pyramid import FLOOR_TABLE, SLOT_RATES, get_floor_encounter_rate

# 12 encounter slots per floor, mapping to Pokemon IDs 1-8
FLOOR_TABLE[1]  # [1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 3, 4]

# Per-slot encounter rates (sum to 100%)
SLOT_RATES  # [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]

# Base encounter rate per step
get_floor_encounter_rate(7)  # 8 (floor 7 has doubled rate)
```

### Items

```python
from frontierbrain3.facilities.pyramid import get_items, get_pickup_items

# Floor items with per-floor rate weighting
get_items(1, 3)  # [{"item": "Hyper Potion", "rate": 31}, ...]

# Pickup ability items (same rates regardless of floor)
get_pickup_items(1)  # [{"item": "Hyper Potion", "rate": 30}, ...]
```

---

## Demo Script

Run the interactive demo to explore all features with guided examples:

```bash
python demo.py
```

Select a category from the menu, then step through examples one at a time.