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

---

## Database

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

### Frontier Trainers

The trainer list is shared across all Battle Frontier facilities, though details like round eligibility and team size may differ between facilities. Each trainer is a dict:

```json
{
    "Index": 1,
    "Name": "BRADY",
    "Class": "Youngster",
    "Sets": [
        "Sunkern-1", "Azurill-1", "Caterpie-1", "Weedle-1", "Wurmple-1",
        "Ralts-1", "Magikarp-1", "Feebas-1", "Pichu-1", "Igglybuff-1",
        "Wooper-1", "Tyrogue-1", "Sentret-1", "Cleffa-1", "Seedot-1",
        "Lotad-1", "Poochyena-1", "Shedinja-1", "Makuhita-1", "Whismur-1",
        "Zigzagoon-1", "Zubat-1", "Togepi-1", "Spinarak-1", "Marill-1",
        "Hoppip-1", "Slugma-1", "Swinub-1", "Smeargle-1", "Pidgey-1",
        "Rattata-1", "Wynaut-1", "Skitty-1", "Spearow-1", "Hoothoot-1",
        "Diglett-1", "Ledyba-1", "Nincada-1", "Surskit-1", "Jigglypuff-1",
        "Taillow-1", "Wingull-1", "NidoranM-1", "NidoranF-1", "Kirlia-1",
        "Mareep-1", "Meditite-1", "Slakoth-1", "Paras-1", "Ekans-1",
        "Ditto-1", "Barboach-1", "Meowth-1", "Pineco-1", "Trapinch-1",
        "Spheal-1", "Horsea-1", "Shroomish-1", "Shuppet-1", "Duskull-1",
        "Electrike-1", "Vulpix-1"
    ]
}
```

The `Sets` list contains all set IDs the trainer can draw from. In battle, they pick 3 (or fewer, depending on the facility) respecting species and item clause.

### Loading

```python
from frontierbrain3 import Database

db = Database()

db.sets       # SetCollection of all 918 frontier sets (882 regular + 36 Frontier Brain)
db.trainers   # TrainerCollection of all trainers (300 regular + Frontier Brains)

db.allSets("Charizard").ids()
```

---

## CustomSet

Represents a player-defined Pokemon with full control over species, nature, EVs, IVs, level, item, ability, and moves.

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

flygon.get_stats()
flygon.speed()
```

The `stats` parameter lets you directly declare stat values rather than calculating them from nature/EVs/IVs:

```python
custom = CustomSet("Flygon", stats={"hp": 302, "atk": 299, "def": 196, "spa": 176, "spd": 196, "spe": 328})
custom.get_stats()
```

### Pokepaste Import

Import teams from [Pokepaste](https://pokepast.es/) format:

```python
from frontierbrain3 import from_paste

from_paste("""
Skarmory (M) @ Leftovers
Ability: Sturdy
EVs: 252 HP / 252 Def / 4 SpD
Bold Nature
- Spikes
- Whirlwind
- Protect
- Rest
""")
```

### Stat Calculations

```python
from frontierbrain3 import calc_stats, Database

db = Database()
snorlax = db.allSets("Snorlax")._sets[0]

calc_stats(snorlax)
calc_stats(snorlax, ivs=15)
calc_stats(snorlax, ivs=15, level=50)
calc_stats(snorlax, ivs=[31,31,31,0,31,31])
```

---

## Filtering

### SetCollection

All filter methods return a new `SetCollection`, so they chain freely. Every `SetCollection` supports `len()`, iteration, `.ids()` (returns `["Pokemon-SetNum", ...]`), and `.Not` for negation.

#### Type Filters

```python
db.sets.hasType("Water")        # pure or part Water type
db.sets.hasType("Psychic/")     # pure Psychic only (trailing slash)
db.sets.hasType("Fire/Flying")  # must have both Fire and Flying
db.sets.hasType("Water", "Ice") # Water OR Ice type
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
from frontierbrain3 import CustomSet

my_flygon = CustomSet("Flygon", nature="Jolly", evs=[4, 252, 0, 0, 0, 252])

db.sets.fasterThan(my_flygon)                # sets that outspeed it at 31 IVs
db.sets.slowerThan(my_flygon)                # sets it outspeeds
db.sets.speedTieWith(my_flygon)              # exact ties
db.sets.fasterThan(my_flygon, ivs=15)        # enemy sets at 15 IVs
```

#### OHKO Filters

These run the full damage calculator for every set in the collection. The attacker/defender can be a frontier set dict or a `CustomSet`.

- `willOHKO(target)`: sets whose best move guarantees the KO (even the minimum damage roll kills)
- `canOHKO(target)`: sets whose best move has any chance to KO (the maximum damage roll kills)
- `willDieTo(attacker)`: sets that the attacker guarantees to KO (each set is the defender)
- `canDieTo(attacker)`: sets that the attacker can KO on at least one roll
- `min_chance=X`: minimum probability (0.0-1.0) that a random roll KOs. Only applies to `canOHKO` and `canDieTo`. Setting `min_chance=0` has no effect (equivalent to omitting it), and `min_chance=1.0` is equivalent to `willOHKO`/`willDieTo`.
- `include_acc=True`: factors move accuracy into all probability calcs, including Brightpowder/Lax Incense on the defender. When combined with `min_chance`, both accuracy and damage roll probability are multiplied together (e.g. a 50% OHKO chance on an 80% accuracy move gives 40% total).
- `include_ohko=True`: allows one-hit KO moves (Guillotine, Fissure, Horn Drill, Sheer Cold) to count

```python
lax = db.allSets("Snorlax")._sets[0]

db.sets.willOHKO(lax)
db.sets.canOHKO(lax)
db.sets.canOHKO(lax, min_chance=0.5)
```

Specify IVs for the attacker and defender independently, useful for analyzing player sets (31 IVs) against frontier enemies (3-31 IVs depending on tier):

```python
# Frontier sets at 3 IVs that guaranteed die to Snorlax-1 at 31 IVs
db.sets.willDieTo(lax, atk_ivs=31, def_ivs=3)

# Normal-types that Snorlax-1 can OHKO on max roll
db.sets.hasType("Normal").canDieTo(lax)
```

Other optional parameters are passed through to the damage calculator:

```python
from frontierbrain3 import Field

meta = db.allSets("Metagross")._sets[0]

db.sets.willDieTo(meta, atk_boosts={"atk": 1})
db.sets.willOHKO(meta, field=Field(weather="rain"))
db.sets.canOHKO(meta, include_ohko=True)

# include_acc excludes sets relying on imperfect-accuracy moves for the guaranteed KO
db.sets.willOHKO(meta)
db.sets.willOHKO(meta, include_acc=True)
```

#### Negation

Every filter has a negated form via `.Not`:

```python
db.sets.hasMove("earthquake").Not.hasMove("surf")     # has EQ but not Surf
db.sets.Not.willOHKO(meta).hasMove("earthquake")      # EQ users that don't guaranteed OHKO Meta
db.sets.Not.canDieTo(meta)                             # survives Metagross even on max roll
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

starmie = CustomSet("Starmie", nature="Timid", evs=[0,0,0,252,4,252],
                    moves=["Surf", "Psychic", "Thunderbolt", "Ice Beam"])
```

### Specifying Moves

Moves can be passed as a string name (looked up from `data/moves.json`):

```python
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
result = calc_matchup(meta, ttar, "Meteor Mash")
print(format_result(result, "Meteor Mash"))
```

The result dict contains: `rolls` (per-hit damage values), `attack_rolls` (combined multi-hit totals, None for single-hit), `hit_info`, `min`/`max` damage, `min_pct`/`max_pct` (as percentage of defender max HP), `defender_hp`, `defender_max_hp`, and `ko_chances` ({1: prob, 2: prob, ...}).

### Raw API

For fine-grained control, use `damage_rolls` + `ko_chance` directly:

```python
rolls = damage_rolls(meta, ttar, "Meteor Mash")
ttar_hp = calc_stats(ttar)["hp"]
kos = ko_chance(rolls, ttar_hp)
```

### Attacker and Defender

Both can be either a frontier set dict (from the database) or a `CustomSet`. Frontier sets at non-default IVs/level:

```python
calc_matchup(meta, ttar, "Meteor Mash", atk_ivs=15, def_ivs=15, atk_level=50, def_level=50)
```

### Field Conditions

```python
# Weather
calc_matchup(starmie, ttar, "Surf", field=Field(weather="rain"))

# Screens
calc_matchup(starmie, ttar, "Surf", field=Field(light_screen=True))

# Doubles (spread moves like Surf, Blizzard, Rock Slide are halved; screens use 2/3 instead of 1/2)
calc_matchup(starmie, ttar, "Surf", field=Field(is_doubles=True))
```

### Stat Boosts

```python
# Dragon Dance (+1 Atk)
calc_matchup(meta, ttar, "Meteor Mash", atk_boosts={"atk": 1})

# Intimidate on attacker (-1 Atk)
calc_matchup(meta, ttar, "Meteor Mash", atk_boosts={"atk": -1})

# Critical hits ignore negative atk stages and positive def stages
calc_matchup(meta, ttar, "Meteor Mash", def_boosts={"def": 2}, critical=True)
```

### Status Conditions

```python
# Burn halves physical damage (unless Guts)
calc_matchup(meta, ttar, "Meteor Mash", atk_status="burn")
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

get_hit_info("Double Kick")
get_hit_info("Bullet Seed")
get_hit_info("Triple Kick")
get_hit_info("Earthquake")
```

`calc_matchup` and the OHKO filters handle multi-hit convolution automatically. For manual use:

```python
from frontierbrain3.damagecalc import combine_multi_hit_rolls

blaziken = db.allSets("Blaziken")._sets[0]
lax = db.allSets("Snorlax")._sets[0]
per_hit = damage_rolls(blaziken, lax, "Double Kick")
hit_info = get_hit_info("Double Kick")
total_rolls = combine_multi_hit_rolls(per_hit, hit_info)
ko_chance(total_rolls, calc_stats(lax)["hp"])
```

### Recoil and Drain Reference

Not applied in the damage formula (they don't affect the hit), but provided as constants for external calculations:

```python
from frontierbrain3.damagecalc import RECOIL_MOVES, DRAIN_MOVES

RECOIL_MOVES
DRAIN_MOVES
```

---

## Battle Tower (`facilities.tower`)

### Trainer Tiers

Tower trainers are grouped into tiers by index, each with fixed IVs and round eligibility. Trainer data is based on the [Bulbapedia Battle Frontier trainer list](https://bulbapedia.bulbagarden.net/wiki/List_of_Battle_Frontier_Trainers_in_Generation_III). The Ruby/Sapphire Battle Tower uses a different trainer list that is not currently supported.

```python
from frontierbrain3.facilities.tower import TowerDatabase, get_tier, TIERS, BRAIN_IVS

get_tier(250)
get_tier(150)

BRAIN_IVS
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
tower.random_team(8)
tower.random_team(8, trainer_class="Dragon Tamer")
tower.random_team(name="Brady")
```

---

## Battle Factory (`facilities.factory`)

Unlike the Tower, Factory sets are not tied to specific trainers. Any trainer can use any set from the eligible pool. The relevant unit of generation is the team itself (3 sets respecting species/item clause), not a trainer-team pair.

### Groups and Pools

Factory sets are divided into 9 groups by index. Each round draws from specific groups:

```python
from frontierbrain3.facilities.factory import FactoryDatabase, get_group

get_group(500)

fac = FactoryDatabase()
pool = fac.sets_in_groups([4, 5, 6, 7, 8])
```

### Team Type and Phrase

Every Factory team gets a "type" (most common Pokemon type) and a "phrase" (battle style description):

```python
from frontierbrain3.facilities.factory import FactoryDatabase, team_type, team_phrase

fac = FactoryDatabase()
sample_team = fac.sets_in_groups([7, 8])[:3]

team_type(sample_team)
team_phrase(sample_team)
```

### Random Team Generation

Generate teams with optional type/phrase constraints:

```python
fac = FactoryDatabase()

ids, typ, phrase = fac.random_team("open", 5)
ids, typ, phrase = fac.random_team("open", 5, target_type="Water")
ids, typ, phrase = fac.random_team("open", 5, target_phrase=4)
ids, typ, phrase = fac.random_team("lv50", 1, target_type="Fire", target_phrase=1)
```

Phrase numbers: 0=none, 1=preparation, 2=slow/steady, 3=endurance, 4=high-risk, 5=weaken foe, 6=unpredictable, 7=battle flow, 8=flex.

---

## Battle Dome (`facilities.dome`)

### Seeding

The Dome gives each team a seed using a formula based on the Pokemon's stats, types, and levels. The seed affects where the players and opponents are placed in the bracket, and having the highest seed possible is advantageous to the player. The higher seed wins in case of a tie (except for Dome Ace Tucker, who will always win ties), unlike every other facility where a tie counts as a loss for the player.

```python
from frontierbrain3 import Database, CustomSet
from frontierbrain3.facilities.dome import calc_seed

db = Database()

meta = db.allSets("Metagross")._sets[0]
lax  = db.allSets("Snorlax")._sets[0]
ttar = db.allSets("Tyranitar")._sets[0]
team = [meta, lax, ttar]

# Player seed
calc_seed(team)

# Enemy seed (0 EV bug + mod 256 overflow)
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

After simulating 1000 random enemy teams, the highest seed found gives a rough upper bound on what the player needs to beat. This is an easy way to estimate how high your team's seed should be to guarantee the #1 position.

---

## Battle Palace (`facilities.palace`)

In the Palace, Pokemon choose their own moves. Each turn, the game first selects a move **category** (Attack, Defense, or Support) based on the Pokemon's nature. Then it picks one of the Pokemon's moves in that category uniformly at random (1/N chance if the category has N moves). If the Pokemon has no move in the selected category, it has a 50% chance to randomly use any move, and a 50% chance to do nothing for that turn.

### Move Categories

Palace classifies every move as attack, defense, or support:

```python
from frontierbrain3.facilities.palace import get_move_category, categorize_moveset

get_move_category("Earthquake"), get_move_category("Swords Dance"), get_move_category("Thunder Wave")

categorize_moveset(["Earthquake", "Rock Slide", "Swords Dance", "Thunder Wave"])
```

### Nature Ratios

Each nature has different category selection odds at high HP (>50%) and low HP (<=50%):

```python
from frontierbrain3.facilities.palace import get_nature_ratios

get_nature_ratios("Adamant")
get_nature_ratios("Adamant", low_hp=True)
```

### Effective Action Probabilities

Accounts for empty categories and the random-move fallback:

```python
from frontierbrain3.facilities.palace import get_action_probabilities, get_move_probabilities

moves = ["Earthquake", "Rock Slide", "Swords Dance", "Protect"]

# Per-category probabilities (including "nothing")
get_action_probabilities("Adamant", moves)

# Per-move probabilities
get_move_probabilities("Adamant", moves)
```

### Multi-Turn Analysis

Analyze probabilities over multiple turns, either by category or by specific move. Category defaults to "attack" but can be set to "defense" or "support":

```python
from frontierbrain3.facilities.palace import (
    multi_turn_probabilities, move_turn_probabilities,
    cumulative_attack_prob, expected_attacks, multi_turn_mixed_hp,
)

moves = ["Earthquake", "Rock Slide", "Swords Dance", "Protect"]

# P(exactly k attack-category moves in 5 turns)
multi_turn_probabilities("Adamant", moves, 5)

# P(exactly k uses of Earthquake specifically in 5 turns)
move_turn_probabilities("Adamant", moves, 5, "Earthquake")

# P(at least 3 attack-category moves in 5 turns)
cumulative_attack_prob("Adamant", moves, 5, 3)

# Expected number of attack-category moves in 5 turns
expected_attacks("Adamant", moves, 5)

# Mixed HP: 3 turns at high HP, then 2 turns at low HP
multi_turn_mixed_hp("Adamant", moves, 3, 2)
```

### Nature Rankings and Utilities

Rank all 25 natures by how likely they are to use a given category (defaults to "attack"):

```python
from frontierbrain3.facilities.palace import rank_natures, low_hp_message, DOUBLES_TARGETING

rank_natures(["Earthquake", "Rock Slide", "Swords Dance", "Protect"])

# Can also rank by other categories
rank_natures(["Earthquake", "Rock Slide", "Swords Dance", "Protect"], category="defense")

low_hp_message("Adamant", "Metagross")

DOUBLES_TARGETING["adamant"]
DOUBLES_TARGETING["brave"]
```

---

## Battle Pike (`facilities.pike`)

### Room Events

8 possible events per room, with some conditionally excluded:

```python
from frontierbrain3.facilities.pike import get_event_probabilities, EVENTS

EVENTS

get_event_probabilities()
get_event_probabilities(all_full_hp=False)
get_event_probabilities(num_fainted=2, all_full_hp=False)
```

### Status Room

```python
from frontierbrain3.facilities.pike import get_status_chances, status_targets

status_targets(1)
status_targets(6)
status_targets(11)
```

Status probabilities accounting for immunities (example team: Metagross / Tauros / Latios):

```python
get_status_chances(
    pokemon_types=[["steel", "psychic"], ["normal"], ["dragon", "psychic"]],
    pokemon_abilities=["clearbody", "intimidate", "levitate"],
    pass_num=1,
)
```

### Wild Pokemon

```python
from frontierbrain3.facilities.pike import pike_wild_pokemon

pike_wild_pokemon(100, lv50=True)
pike_wild_pokemon(300, lv50=True)
pike_wild_pokemon(900, lv50=False)
```

### Hints

```python
from frontierbrain3.facilities.pike import HINTS

HINTS
```

---

## Battle Pyramid (`facilities.pyramid`)

For more details, see the [Bulbapedia Battle Pyramid page](https://bulbapedia.bulbagarden.net/wiki/Battle_Pyramid).

### Round Themes and Wild Pokemon

20 rounds, each with a theme and 8 wild Pokemon:

```python
from frontierbrain3.facilities.pyramid import pyramid_wild_pokemon, ROUND_THEMES

ROUND_THEMES

# All 8 Pokemon for round 1
pyramid_wild_pokemon(1)

# Encounters with rates for round 1, floor 3
pyramid_wild_pokemon(1, floor=3)
```

Encounter data includes species, ability, level ranges, and moves. Rounds cycle after 20 (round 21 = round 1, etc.).

### Floor Mechanics

```python
from frontierbrain3.facilities.pyramid import FLOOR_TABLE, SLOT_RATES, get_floor_encounter_rate

FLOOR_TABLE[1]

SLOT_RATES

get_floor_encounter_rate(7)
```

### Items

```python
from frontierbrain3.facilities.pyramid import get_items, get_pickup_items

get_items(1, 3)

get_pickup_items(1)
```

---

## Demo Script

Run the interactive demo to explore all features with guided examples:

```bash
python demo.py
```

Select a category from the menu, then step through examples one at a time.