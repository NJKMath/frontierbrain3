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

## Quick Start


> ```python
> from frontierbrain3 import Database, CustomSet, calc_matchup, format_result
> ```


> ```python
> db = Database()
> ```


> ```python
> water_surfers = db.sets.hasType("Water").hasMove("surf")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> water_surfers = SetCollection(65 sets)
> [  # 65 items
>   'Wartortle-2',
>   'Sealeo-2',
>   'Pelipper-2',
>   'Sharpedo-2',
>   'Mantine-2',
>   'Huntail-2',
>   'Gorebyss-2',
>   'Politoed-2',
>   'Lanturn-1',
>   'Ludicolo-1',
>   'Slowbro-1',
>   'Wailord-1',
>   'Vaporeon-1',
>   'Feraligatr-1',
>   'Lapras-1',
>   ... (35 more) ...
>   'Lapras-4',
>   'Swampert-4',
>   'Milotic-4',
>   'Suicune-1',
>   'Suicune-3',
>   'Suicune-4',
>   'Starmie-5',
>   'Starmie-6',
>   'Starmie-8',
>   'Suicune-5',
>   'Suicune-6',
>   'Swampert-TuckerSilver',
>   'Swampert-TuckerGold',
>   'Suicune-SpenserGold',
>   'Milotic-LucySilver',
> ]
> ```
>
> </details>


> ```python
> print(f"{len(water_surfers)} sets")  # SetCollection with .ids(), iteration, etc.
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 65 sets
> ```
>
> </details>


> ```python
> starmie = CustomSet("Starmie", nature="Timid", evs=[0,0,0,252,4,252],
>                     moves=["Surf", "Thunderbolt", "Ice Beam", "Psychic"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> starmie = CustomSet(Starmie, nature=Timid, evs=[0, 0, 0, 252, 4, 252], ivs=[31, 31, 31, 31, 31, 31], level=100, ability=illuminate, moves=['surf', 'thunderbolt', 'icebeam', 'psychic'])
> ```
>
> </details>


> ```python
> ttar = db.allSets("Tyranitar")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ttar = {
>   'Pokemon': 'Tyranitar',
>   'SetNum': 1,
>   'Nature': 'Hardy',
>   'Item': 'BrightPowder',
>   'Abilities': ['Sand Stream'],
>   'Moves': ['earthquake', 'aerialace', 'thunderbolt', 'surf'],
>   'EVs': [0, 255, 0, 255, 0, 0],
>   'Index': 861,
>   'DexNum': 248,
> }
> ```
>
> </details>


> ```python
> result = calc_matchup(starmie, ttar, "Surf")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> result = {
>   'rolls': [261, 264, 267, 271, 274, 277, 280, 283, 286, 289, 292, 295, 298, 301, 304, 308],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 261,
>   'max': 308,
>   'min_pct': 76.50,
>   'max_pct': 90.30,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 1.0},
> }
> ```
>
> </details>


> ```python
> print(format_result(result, "Surf"))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> Surf: 261-308 (76.5% - 90.3%) [HP: 341]
>   Per-hit rolls: (261, 264, 267, 271, 274, 277, 280, 283, 286, 289, 292, 295, 298, 301, 304, 308)
>   guaranteed 2HKO
> ```
>
> </details>


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


> ```python
> from frontierbrain3 import Database
> ```


> ```python
> db = Database()
> ```


> ```python
> db.allSets("Charizard")        # SetCollection of all Charizard sets
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(5 sets)
> ['Charizard-1', 'Charizard-2', 'Charizard-3', 'Charizard-4', 'Charizard-TuckerSilver']
> ```
>
> </details>


> ```python
> db.allSets("Charizard").ids()  # ["Charizard-1", "Charizard-2", ...]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ['Charizard-1', 'Charizard-2', 'Charizard-3', 'Charizard-4', 'Charizard-TuckerSilver']
> ```
>
> </details>


> ```python
> meta = db.allSets("Metagross")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> meta = {
>   'Pokemon': 'Metagross',
>   'SetNum': 1,
>   'Nature': 'Adamant',
>   'Item': 'Leftovers',
>   'Abilities': ['Clear Body'],
>   'Moves': ['meteormash', 'aerialace', 'facade', 'lightscreen'],
>   'EVs': [0, 170, 0, 0, 170, 170],
>   'Index': 467,
>   'DexNum': 376,
> }
> ```
>
> </details>


> ```python
> print(meta["Nature"], meta["Item"], meta["Moves"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> Adamant Leftovers ['meteormash', 'aerialace', 'facade', 'lightscreen']
> ```
>
> </details>


### CustomSet

Represents a player-defined Pokemon with full control over species, nature, EVs, IVs, level, item, ability, and moves. Used as attacker/defender in damage calcs and as a speed benchmark in queries.


> ```python
> from frontierbrain3 import CustomSet
> ```


> ```python
> flygon = CustomSet(
>     "Flygon",
>     nature="Jolly",
>     evs=[4, 252, 0, 0, 0, 252],
>     ivs=31,            # int (all same) or list of 6
>     level=100,
>     item="Choice Band",
>     ability="Levitate",
>     moves=["Earthquake", "Rock Slide", "Fire Blast", "Return"],
> )
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> flygon = CustomSet(Flygon, nature=Jolly, evs=[4, 252, 0, 0, 0, 252], ivs=[31, 31, 31, 31, 31, 31], level=100, item=Choice Band, ability=Levitate, moves=['earthquake', 'rockslide', 'fireblast', 'return'])
> ```
>
> </details>


> ```python
> flygon.get_stats()  # {'hp': ..., 'atk': ..., 'def': ..., 'spa': ..., 'spd': ..., 'spe': ...}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'hp': 302,
>   'atk': 299,
>   'def': 196,
>   'spa': 176,
>   'spd': 196,
>   'spe': 328,
> }
> ```
>
> </details>


> ```python
> flygon.speed()      # shorthand for get_stats()["spe"]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 328
> ```
>
> </details>


The `stats` parameter lets you override calculated stats with exact values if needed:


> ```python
> custom = CustomSet("Flygon", stats={"hp": 302, "atk": 299, "def": 196, "spa": 176, "spd": 196, "spe": 328})
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> custom = CustomSet(Flygon, nature=hardy, evs=[0, 0, 0, 0, 0, 0], ivs=[31, 31, 31, 31, 31, 31], level=100, ability=levitate)
> ```
>
> </details>


### Pokepaste Import

Import teams from [Pokepaste](https://pokepast.es/) format:


> ```python
> from frontierbrain3 import from_paste
> ```


> ```python
> team = from_paste("""
> Skarmory (M) @ Leftovers
> Ability: Sturdy
> EVs: 252 HP / 252 Def / 4 SpD
> Bold Nature
> - Spikes
> - Whirlwind
> - Protect
> - Rest
> """)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> team = {
>   'CustomSkarmory': CustomSet(Skarmory, nature=Bold, evs=[252, 0, 252, 0, 4, 0], ivs=[31, 31, 31, 31, 31, 31], level=100, item=Leftovers, ability=Sturdy, moves=['spikes', 'whirlwind', 'protect', 'rest']),
> }
> ```
>
> </details>


> ```python
> for name, cs in team.items():
>     print(f"{name}: {cs.pokemon}, speed={cs.speed()}")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> CustomSkarmory: Skarmory, speed=176
> ```
>
> </details>


---

## Core Utilities (`frontierutils`)

### Stat Calculations


> ```python
> from frontierbrain3 import calc_stats, Database
> ```


> ```python
> db = Database()
> ```


> ```python
> alakazam = db.allSets("Alakazam")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> alakazam = {
>   'Pokemon': 'Alakazam',
>   'SetNum': 1,
>   'Nature': 'Modest',
>   'Item': 'Focus Band',
>   'Abilities': ['Synchronize', 'Inner Focus'],
>   'Moves': ['thunderpunch', 'firepunch', 'icepunch', 'thunderwave'],
>   'EVs': [0, 0, 255, 255, 0, 0],
>   'Index': 405,
>   'DexNum': 65,
> }
> ```
>
> </details>


> ```python
> calc_stats(alakazam)                    # 31 IVs, lv100 (defaults)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'hp': 251,
>   'atk': 122,
>   'def': 189,
>   'spa': 405,
>   'spd': 206,
>   'spe': 276,
> }
> ```
>
> </details>


> ```python
> calc_stats(alakazam, ivs=15)            # 15 IVs, lv100
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'hp': 235,
>   'atk': 108,
>   'def': 173,
>   'spa': 388,
>   'spd': 190,
>   'spe': 260,
> }
> ```
>
> </details>


> ```python
> calc_stats(alakazam, ivs=15, level=50)  # 15 IVs, lv50
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'hp': 122,
>   'atk': 55,
>   'def': 89,
>   'spa': 196,
>   'spd': 97,
>   'spe': 132,
> }
> ```
>
> </details>


> ```python
> calc_stats(alakazam, ivs=[31,31,31,0,31,31])  # per-stat IVs
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'hp': 251,
>   'atk': 122,
>   'def': 189,
>   'spa': 371,
>   'spd': 206,
>   'spe': 276,
> }
> ```
>
> </details>


---

## Database (`frontier_db`)

### Loading


> ```python
> from frontierbrain3 import Database
> ```


> ```python
> db = Database()  # loads from default data/ paths
> ```


> ```python
> db.sets       # SetCollection of all 918 frontier sets (882 regular + 36 Frontier Brain)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(918 sets)
> [  # 918 items
>   'Sunkern-1',
>   'Azurill-1',
>   'Caterpie-1',
>   'Weedle-1',
>   'Wurmple-1',
>   'Ralts-1',
>   'Magikarp-1',
>   'Feebas-1',
>   'Metapod-1',
>   'Kakuna-1',
>   'Pichu-1',
>   'Silcoon-1',
>   'Cascoon-1',
>   'Igglybuff-1',
>   'Wooper-1',
>   ... (888 more) ...
>   'Umbreon-GretaGold',
>   'Gengar-GretaGold',
>   'Breloom-GretaGold',
>   'Seviper-LucySilver',
>   'Shuckle-LucySilver',
>   'Milotic-LucySilver',
>   'Seviper-LucyGold',
>   'Steelix-LucyGold',
>   'Gyarados-LucyGold',
>   'Regirock-BrandonSilver',
>   'Registeel-BrandonSilver',
>   'Regice-BrandonSilver',
>   'Articuno-BrandonGold',
>   'Zapdos-BrandonGold',
>   'Moltres-BrandonGold',
> ]
> ```
>
> </details>


> ```python
> db.trainers   # TrainerCollection of all trainers (300 regular + Frontier Brains)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(312 trainers)
> [  # 312 items
>   'YOUNGSTER BRADY',
>   'YOUNGSTER CONNER',
>   'YOUNGSTER BRADLEY',
>   'LASS CYBIL',
>   'LASS RODETTE',
>   'LASS PEGGY',
>   'SCHOOL KID (M) KEITH',
>   'SCHOOL KID (M) GRAYSON',
>   'SCHOOL KID (M) GLENN',
>   'SCHOOL KID (F) LILIANA',
>   'SCHOOL KID (F) ELISE',
>   'SCHOOL KID (F) ZOEY',
>   'RICH BOY MANUEL',
>   'RICH BOY RUSS',
>   'RICH BOY DUSTIN',
>   ... (282 more) ...
>   'BEAUTY DAWN',
>   'AROMA LADY ABBY',
>   'AROMA LADY GRETEL',
>   'SALON MAIDEN ANABEL',
>   'SALON MAIDEN ANABEL',
>   'DOME ACE TUCKER',
>   'DOME ACE TUCKER',
>   'PALACE MAVEN SPENSER',
>   'PALACE MAVEN SPENSER',
>   'ARENA TYCOON GRETA',
>   'ARENA TYCOON GRETA',
>   'PIKE QUEEN LUCY',
>   'PIKE QUEEN LUCY',
>   'PYRAMID KING BRANDON',
>   'PYRAMID KING BRANDON',
> ]
> ```
>
> </details>


### SetCollection

All filter methods return a new `SetCollection`, so they chain freely. Every `SetCollection` supports `len()`, iteration, `.ids()` (returns `["Pokemon-SetNum", ...]`), and `.Not` for negation.

#### Type Filters


> ```python
> db.sets.hasType("Water")        # pure or part Water type
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(179 sets)
> [  # 179 items
>   'Magikarp-1',
>   'Feebas-1',
>   'Wooper-1',
>   'Lotad-1',
>   'Marill-1',
>   'Surskit-1',
>   'Wingull-1',
>   'Barboach-1',
>   'Spheal-1',
>   'Horsea-1',
>   'Poliwag-1',
>   'Remoraid-1',
>   'Shellder-1',
>   'Carvanha-1',
>   'Corphish-1',
>   ... (149 more) ...
>   'Starmie-6',
>   'Starmie-7',
>   'Starmie-8',
>   'Lapras-5',
>   'Lapras-6',
>   'Lapras-7',
>   'Lapras-8',
>   'Suicune-5',
>   'Suicune-6',
>   'Swampert-TuckerSilver',
>   'Swampert-TuckerGold',
>   'Lapras-SpenserSilver',
>   'Suicune-SpenserGold',
>   'Milotic-LucySilver',
>   'Gyarados-LucyGold',
> ]
> ```
>
> </details>


> ```python
> db.sets.hasType("Psychic/")     # pure Psychic only (trailing slash)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(40 sets)
> [  # 40 items
>   'Ralts-1',
>   'Wynaut-1',
>   'Kirlia-1',
>   'Abra-1',
>   'Drowzee-1',
>   'Spoink-1',
>   'Unown-1',
>   'Kadabra-1',
>   'Wobbuffet-1',
>   'Chimecho-1',
>   'Grumpig-1',
>   'Kadabra-2',
>   'Wobbuffet-2',
>   'Chimecho-2',
>   'Grumpig-2',
>   ... (10 more) ...
>   'Mr. Mime-3',
>   'Hypno-3',
>   'Alakazam-3',
>   'Gardevoir-3',
>   'Espeon-3',
>   'Mr. Mime-4',
>   'Hypno-4',
>   'Alakazam-4',
>   'Gardevoir-4',
>   'Espeon-4',
>   'Gardevoir-5',
>   'Gardevoir-6',
>   'Gardevoir-7',
>   'Gardevoir-8',
>   'Alakazam-AnabelSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.hasType("Fire/Flying")  # must have both Fire and Flying
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(12 sets)
> [
>   'Charizard-1',
>   'Charizard-2',
>   'Charizard-3',
>   'Charizard-4',
>   'Moltres-1',
>   'Moltres-2',
>   'Moltres-3',
>   'Moltres-4',
>   'Moltres-5',
>   'Moltres-6',
>   'Charizard-TuckerSilver',
>   'Moltres-BrandonGold',
> ]
> ```
>
> </details>


#### Move Filters


> ```python
> db.sets.hasMove("surf")                        # has Surf
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(72 sets)
> [  # 72 items
>   'Wartortle-2',
>   'Sealeo-2',
>   'Pelipper-2',
>   'Sharpedo-2',
>   'Mantine-2',
>   'Huntail-2',
>   'Gorebyss-2',
>   'Politoed-2',
>   'Lanturn-1',
>   'Ludicolo-1',
>   'Slowbro-1',
>   'Wailord-1',
>   'Vaporeon-1',
>   'Feraligatr-1',
>   'Lapras-1',
>   ... (42 more) ...
>   'Suicune-3',
>   'Suicune-4',
>   'Starmie-5',
>   'Starmie-6',
>   'Starmie-8',
>   'Dragonite-6',
>   'Dragonite-7',
>   'Dragonite-9',
>   'Tyranitar-1',
>   'Suicune-5',
>   'Suicune-6',
>   'Swampert-TuckerSilver',
>   'Swampert-TuckerGold',
>   'Suicune-SpenserGold',
>   'Milotic-LucySilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.hasMove("earthquake", "surf")           # has EQ OR Surf (default match="any")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(222 sets)
> [  # 222 items
>   'Lickitung-2',
>   'Graveler-2',
>   'Wailmer-2',
>   'Wartortle-2',
>   'Marshtomp-2',
>   'Sudowoodo-2',
>   'Magcargo-2',
>   'Pupitar-2',
>   'Sealeo-2',
>   'Gligar-2',
>   'Pelipper-2',
>   'Lairon-2',
>   'Arbok-2',
>   'Solrock-2',
>   'Sandslash-2',
>   ... (192 more) ...
>   'Tyranitar-10',
>   'Suicune-5',
>   'Suicune-6',
>   'Swampert-TuckerSilver',
>   'Salamence-TuckerSilver',
>   'Charizard-TuckerSilver',
>   'Swampert-TuckerGold',
>   'Metagross-TuckerGold',
>   'Slaking-SpenserSilver',
>   'Slaking-SpenserGold',
>   'Suicune-SpenserGold',
>   'Milotic-LucySilver',
>   'Steelix-LucyGold',
>   'Regirock-BrandonSilver',
>   'Registeel-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.hasMove("calmmind", "surf", match="all")  # has BOTH Calm Mind AND Surf
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(5 sets)
> ['Slowbro-2', 'Suicune-1', 'Suicune-5', 'Suicune-6', 'Suicune-SpenserGold']
> ```
>
> </details>


#### Item, Nature, Ability Filters


> ```python
> db.sets.hasItem("Choice Band")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(12 sets)
> [
>   'Beldum-1',
>   'Furret-2',
>   'Linoone-2',
>   'Kecleon-2',
>   'Absol-2',
>   'Aerodactyl-2',
>   'Mr. Mime-3',
>   'Alakazam-3',
>   'Slaking-3',
>   'Granbull-4',
>   'Armaldo-4',
>   'Ursaring-5',
> ]
> ```
>
> </details>


> ```python
> db.sets.hasItem("Leftovers", "Shell Bell")  # has either item
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(121 sets)
> [  # 121 items
>   'Slakoth-1',
>   'Carvanha-1',
>   'Staryu-1',
>   'Octillery-1',
>   'Omastar-1',
>   'Politoed-1',
>   'Wartortle-2',
>   'Parasect-2',
>   'Azumarill-2',
>   'Sunflora-2',
>   'Pelipper-2',
>   'Seadra-2',
>   'Chansey-2',
>   'Jumpluff-2',
>   'Piloswine-2',
>   ... (91 more) ...
>   'Metagross-7',
>   'Regice-5',
>   'Registeel-5',
>   'Latias-6',
>   'Latias-7',
>   'Latios-6',
>   'Dragonite-3',
>   'Dragonite-6',
>   'Dragonite-7',
>   'Dragonite-8',
>   'Swampert-TuckerGold',
>   'Umbreon-GretaSilver',
>   'Gengar-GretaGold',
>   'Milotic-LucySilver',
>   'Registeel-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.hasNature("Adamant")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(197 sets)
> [  # 197 items
>   'Machop-1',
>   'Graveler-1',
>   'Machoke-1',
>   'Linoone-1',
>   'Swellow-1',
>   'Arbok-1',
>   'Sandslash-1',
>   'Hitmonlee-1',
>   'Hitmonchan-1',
>   'Sharpedo-1',
>   'Absol-1',
>   'Crawdaunt-1',
>   'Kabutops-1',
>   'Poliwrath-1',
>   'Lickitung-2',
>   ... (167 more) ...
>   'Dragonite-4',
>   'Tyranitar-3',
>   'Tyranitar-5',
>   'Tyranitar-6',
>   'Tyranitar-7',
>   'Tyranitar-8',
>   'Tyranitar-10',
>   'Snorlax-AnabelSilver',
>   'Snorlax-AnabelGold',
>   'Salamence-TuckerSilver',
>   'Crobat-SpenserSilver',
>   'Shedinja-GretaSilver',
>   'Gyarados-LucyGold',
>   'Regirock-BrandonSilver',
>   'Registeel-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.hasAbility("Intimidate")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(41 sets)
> [  # 41 items
>   'Ekans-1',
>   'Snubbull-1',
>   'Growlithe-1',
>   'Mawile-1',
>   'Masquerain-1',
>   'Mightyena-1',
>   'Arbok-1',
>   'Hitmontop-1',
>   'Stantler-1',
>   'Masquerain-2',
>   'Mightyena-2',
>   'Arbok-2',
>   'Hitmontop-2',
>   'Stantler-2',
>   'Granbull-1',
>   ... (11 more) ...
>   'Gyarados-3',
>   'Arcanine-3',
>   'Salamence-3',
>   'Granbull-4',
>   'Tauros-4',
>   'Gyarados-4',
>   'Arcanine-4',
>   'Salamence-4',
>   'Salamence-5',
>   'Salamence-6',
>   'Salamence-7',
>   'Salamence-8',
>   'Swampert-TuckerSilver',
>   'Arcanine-SpenserGold',
>   'Gyarados-LucyGold',
> ]
> ```
>
> </details>


#### Stat Filters

Filter by calculated stat value. Specify `ivs` and `level` to match the format you're analyzing.


> ```python
> db.sets.statFilter("atk", min=300)                      # 300+ Atk at 31 IVs, lv100
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(172 sets)
> [  # 172 items
>   'Krabby-1',
>   'Hitmonlee-1',
>   'Zangoose-1',
>   'Sharpedo-1',
>   'Absol-1',
>   'Crawdaunt-1',
>   'Octillery-1',
>   'Huntail-1',
>   'Kabutops-1',
>   'Scyther-1',
>   'Pinsir-1',
>   'Machoke-2',
>   'Hitmonlee-2',
>   'Zangoose-2',
>   'Sharpedo-2',
>   ... (142 more) ...
>   'Entei-AnabelSilver',
>   'Snorlax-AnabelSilver',
>   'Snorlax-AnabelGold',
>   'Swampert-TuckerSilver',
>   'Salamence-TuckerSilver',
>   'Swampert-TuckerGold',
>   'Metagross-TuckerGold',
>   'Slaking-SpenserSilver',
>   'Arcanine-SpenserGold',
>   'Slaking-SpenserGold',
>   'Heracross-GretaSilver',
>   'Shedinja-GretaSilver',
>   'Breloom-GretaGold',
>   'Gyarados-LucyGold',
>   'Regirock-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.statFilter("spe", min=200, max=250)              # speed in range
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(138 sets)
> [  # 138 items
>   'Spearow-1',
>   'Taillow-1',
>   'Wingull-1',
>   'Meowth-1',
>   'Electrike-1',
>   'Vulpix-1',
>   'Remoraid-1',
>   'Doduo-1',
>   'Eevee-1',
>   'Voltorb-1',
>   'Luvdisc-1',
>   'Staryu-1',
>   'Elekid-1',
>   'Magby-1',
>   'Beedrill-1',
>   ... (108 more) ...
>   'Salamence-6',
>   'Metagross-5',
>   'Metagross-8',
>   'Articuno-5',
>   'Articuno-6',
>   'Zapdos-5',
>   'Moltres-6',
>   'Entei-5',
>   'Entei-6',
>   'Suicune-5',
>   'Suicune-6',
>   'Entei-AnabelSilver',
>   'Charizard-TuckerSilver',
>   'Arcanine-SpenserGold',
>   'Suicune-SpenserGold',
> ]
> ```
>
> </details>


> ```python
> db.sets.statFilter("spa", min=150, level=50, ivs=15)     # lv50, 15 IVs
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(116 sets)
> [  # 116 items
>   'Magneton-1',
>   'Gorebyss-1',
>   'Omastar-1',
>   'Jynx-1',
>   'Manectric-1',
>   'Alakazam-1',
>   'Golduck-1',
>   'Gengar-1',
>   'Ampharos-1',
>   'Exeggutor-1',
>   'Starmie-1',
>   'Venusaur-1',
>   'Vaporeon-1',
>   'Jolteon-1',
>   'Flareon-1',
>   ... (86 more) ...
>   'Latios-8',
>   'Dragonite-6',
>   'Dragonite-7',
>   'Dragonite-8',
>   'Tyranitar-4',
>   'Zapdos-5',
>   'Zapdos-6',
>   'Moltres-5',
>   'Moltres-6',
>   'Raikou-5',
>   'Alakazam-AnabelSilver',
>   'Latios-AnabelGold',
>   'Gengar-GretaGold',
>   'Zapdos-BrandonGold',
>   'Moltres-BrandonGold',
> ]
> ```
>
> </details>


#### Speed Comparisons

Compare frontier sets against a `CustomSet` benchmark:


> ```python
> my_flygon = CustomSet("Flygon", nature="Jolly", evs=[4, 252, 0, 0, 0, 252])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> my_flygon = CustomSet(Flygon, nature=Jolly, evs=[4, 252, 0, 0, 0, 252], ivs=[31, 31, 31, 31, 31, 31], level=100, ability=levitate)
> ```
>
> </details>


> ```python
> db.sets.fasterThan(my_flygon)                # sets that outspeed it at 31 IVs
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(27 sets)
> [
>   'Ninjask-1',
>   'Sneasel-2',
>   'Ninjask-2',
>   'Dugtrio-1',
>   'Aerodactyl-1',
>   'Jolteon-1',
>   'Sceptile-1',
>   'Dugtrio-2',
>   'Aerodactyl-2',
>   'Sceptile-2',
>   'Dugtrio-3',
>   'Starmie-3',
>   'Crobat-3',
>   'Dugtrio-4',
>   'Starmie-4',
>   'Jolteon-4',
>   'Sceptile-4',
>   'Crobat-4',
>   'Raikou-1',
>   'Raikou-2',
>   'Raikou-3',
>   'Raikou-4',
>   'Starmie-5',
>   'Starmie-7',
>   'Starmie-8',
>   'Raikou-5',
>   'Crobat-SpenserSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.slowerThan(my_flygon)                # sets it outspeeds
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(890 sets)
> [  # 890 items
>   'Sunkern-1',
>   'Azurill-1',
>   'Caterpie-1',
>   'Weedle-1',
>   'Wurmple-1',
>   'Ralts-1',
>   'Magikarp-1',
>   'Feebas-1',
>   'Metapod-1',
>   'Kakuna-1',
>   'Pichu-1',
>   'Silcoon-1',
>   'Cascoon-1',
>   'Igglybuff-1',
>   'Wooper-1',
>   ... (860 more) ...
>   'Umbreon-GretaGold',
>   'Gengar-GretaGold',
>   'Breloom-GretaGold',
>   'Seviper-LucySilver',
>   'Shuckle-LucySilver',
>   'Milotic-LucySilver',
>   'Seviper-LucyGold',
>   'Steelix-LucyGold',
>   'Gyarados-LucyGold',
>   'Regirock-BrandonSilver',
>   'Registeel-BrandonSilver',
>   'Regice-BrandonSilver',
>   'Articuno-BrandonGold',
>   'Zapdos-BrandonGold',
>   'Moltres-BrandonGold',
> ]
> ```
>
> </details>


> ```python
> db.sets.speedTieWith(my_flygon)              # exact ties
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(1 sets)
> ['Linoone-2']
> ```
>
> </details>


> ```python
> db.sets.fasterThan(my_flygon, ivs=15)        # enemy sets at 15 IVs
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(6 sets)
> ['Ninjask-1', 'Ninjask-2', 'Jolteon-1', 'Crobat-3', 'Jolteon-4', 'Crobat-4']
> ```
>
> </details>


#### OHKO Filters

These run the full damage calculator for every set in the collection. The attacker/defender can be a frontier set dict or a `CustomSet`.


> ```python
> zam = db.allSets("Alakazam")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> zam = {
>   'Pokemon': 'Alakazam',
>   'SetNum': 1,
>   'Nature': 'Modest',
>   'Item': 'Focus Band',
>   'Abilities': ['Synchronize', 'Inner Focus'],
>   'Moves': ['thunderpunch', 'firepunch', 'icepunch', 'thunderwave'],
>   'EVs': [0, 0, 255, 255, 0, 0],
>   'Index': 405,
>   'DexNum': 65,
> }
> ```
>
> </details>


> ```python
> lax = db.allSets("Snorlax")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> lax = {
>   'Pokemon': 'Snorlax',
>   'SetNum': 1,
>   'Nature': 'Adamant',
>   'Item': 'Leftovers',
>   'Abilities': ['Immunity', 'Thick Fat'],
>   'Moves': ['facade', 'shadowball', 'attract', 'doubleteam'],
>   'EVs': [0, 255, 255, 0, 0, 0],
>   'Index': 461,
>   'DexNum': 143,
> }
> ```
>
> </details>


> ```python
> db.sets.willOHKO(zam)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(65 sets)
> [  # 65 items
>   'Pineco-1',
>   'Sudowoodo-2',
>   'Furret-2',
>   'Banette-2',
>   'Absol-2',
>   'Granbull-1',
>   'Marowak-1',
>   'Heracross-1',
>   'Marowak-2',
>   'Glalie-2',
>   'Scizor-2',
>   'Heracross-2',
>   'Ursaring-2',
>   'Houndoom-2',
>   'Aerodactyl-2',
>   ... (35 more) ...
>   'Registeel-3',
>   'Moltres-4',
>   'Ursaring-5',
>   'Ursaring-6',
>   'Metagross-5',
>   'Metagross-8',
>   'Regirock-6',
>   'Tyranitar-4',
>   'Moltres-5',
>   'Moltres-6',
>   'Slaking-SpenserGold',
>   'Heracross-GretaSilver',
>   'Shedinja-GretaSilver',
>   'Steelix-LucyGold',
>   'Regirock-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.canOHKO(lax)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(25 sets)
> [
>   'Breloom-2',
>   'Glalie-2',
>   'Breloom-3',
>   'Forretress-3',
>   'Shiftry-3',
>   'Golem-3',
>   'Weezing-3',
>   'Steelix-3',
>   'Breloom-4',
>   'Forretress-4',
>   'Shiftry-4',
>   'Golem-4',
>   'Weezing-4',
>   'Muk-4',
>   'Claydol-4',
>   'Steelix-4',
>   'Exeggutor-4',
>   'Regirock-1',
>   'Regirock-2',
>   'Machamp-7',
>   'Metagross-5',
>   'Metagross-8',
>   'Regirock-6',
>   'Breloom-GretaGold',
>   'Regirock-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.canOHKO(lax, min_chance=0.5)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(20 sets)
> [
>   'Breloom-3',
>   'Shiftry-3',
>   'Golem-3',
>   'Weezing-3',
>   'Steelix-3',
>   'Breloom-4',
>   'Forretress-4',
>   'Shiftry-4',
>   'Golem-4',
>   'Weezing-4',
>   'Muk-4',
>   'Steelix-4',
>   'Exeggutor-4',
>   'Regirock-1',
>   'Regirock-2',
>   'Machamp-7',
>   'Metagross-5',
>   'Metagross-8',
>   'Breloom-GretaGold',
>   'Regirock-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> meta = db.allSets("Metagross")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> meta = {
>   'Pokemon': 'Metagross',
>   'SetNum': 1,
>   'Nature': 'Adamant',
>   'Item': 'Leftovers',
>   'Abilities': ['Clear Body'],
>   'Moves': ['meteormash', 'aerialace', 'facade', 'lightscreen'],
>   'EVs': [0, 170, 0, 0, 170, 170],
>   'Index': 467,
>   'DexNum': 376,
> }
> ```
>
> </details>


> ```python
> db.sets.hasType("Normal").diesTo(meta)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(18 sets)
> [
>   'Azurill-1',
>   'Igglybuff-1',
>   'Sentret-1',
>   'Cleffa-1',
>   'Whismur-1',
>   'Zigzagoon-1',
>   'Smeargle-1',
>   'Pidgey-1',
>   'Rattata-1',
>   'Skitty-1',
>   'Spearow-1',
>   'Hoothoot-1',
>   'Taillow-1',
>   'Meowth-1',
>   'Doduo-1',
>   'Swablu-1',
>   'Clefairy-1',
>   'Raticate-2',
> ]
> ```
>
> </details>


> ```python
> starmie = CustomSet("Starmie", nature="Timid", evs=[0,0,0,252,4,252],
>                     moves=["Surf", "Psychic", "Thunderbolt", "Ice Beam"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> starmie = CustomSet(Starmie, nature=Timid, evs=[0, 0, 0, 252, 4, 252], ivs=[31, 31, 31, 31, 31, 31], level=100, ability=illuminate, moves=['surf', 'psychic', 'thunderbolt', 'icebeam'])
> ```
>
> </details>


> ```python
> db.sets.canDieTo(starmie)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(325 sets)
> [  # 325 items
>   'Sunkern-1',
>   'Azurill-1',
>   'Caterpie-1',
>   'Weedle-1',
>   'Wurmple-1',
>   'Ralts-1',
>   'Magikarp-1',
>   'Feebas-1',
>   'Kakuna-1',
>   'Pichu-1',
>   'Igglybuff-1',
>   'Wooper-1',
>   'Tyrogue-1',
>   'Sentret-1',
>   'Seedot-1',
>   ... (295 more) ...
>   'Dragonite-6',
>   'Dragonite-7',
>   'Dragonite-8',
>   'Dragonite-9',
>   'Dragonite-10',
>   'Moltres-5',
>   'Moltres-6',
>   'Salamence-TuckerSilver',
>   'Charizard-TuckerSilver',
>   'Arcanine-SpenserGold',
>   'Gengar-GretaGold',
>   'Breloom-GretaGold',
>   'Seviper-LucySilver',
>   'Seviper-LucyGold',
>   'Moltres-BrandonGold',
> ]
> ```
>
> </details>


Specify IVs for the attacker and defender independently, useful for analyzing player sets (31 IVs) against frontier enemies (3-31 IVs depending on tier):


> ```python
> db.sets.diesTo(meta, atk_ivs=31, def_ivs=3)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(264 sets)
> [  # 264 items
>   'Sunkern-1',
>   'Azurill-1',
>   'Caterpie-1',
>   'Weedle-1',
>   'Wurmple-1',
>   'Ralts-1',
>   'Feebas-1',
>   'Metapod-1',
>   'Kakuna-1',
>   'Pichu-1',
>   'Silcoon-1',
>   'Cascoon-1',
>   'Igglybuff-1',
>   'Tyrogue-1',
>   'Sentret-1',
>   ... (234 more) ...
>   'Gengar-8',
>   'Gardevoir-8',
>   'Regice-5',
>   'Regice-6',
>   'Tyranitar-1',
>   'Tyranitar-2',
>   'Tyranitar-9',
>   'Articuno-5',
>   'Articuno-6',
>   'Alakazam-AnabelSilver',
>   'Heracross-GretaSilver',
>   'Shedinja-GretaSilver',
>   'Breloom-GretaGold',
>   'Regice-BrandonSilver',
>   'Articuno-BrandonGold',
> ]
> ```
>
> </details>


> ```python
> db.sets.canOHKO(zam, atk_ivs=31, def_ivs=15)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(173 sets)
> [  # 173 items
>   'Shedinja-1',
>   'Spinarak-1',
>   'Pineco-1',
>   'Geodude-1',
>   'Houndour-1',
>   'Rhyhorn-1',
>   'Ariados-1',
>   'Sableye-2',
>   'Plusle-2',
>   'Minun-2',
>   'Sudowoodo-2',
>   'Furret-2',
>   'Mightyena-2',
>   'Linoone-2',
>   'Kecleon-2',
>   ... (143 more) ...
>   'Moltres-6',
>   'Snorlax-AnabelSilver',
>   'Snorlax-AnabelGold',
>   'Swampert-TuckerSilver',
>   'Charizard-TuckerSilver',
>   'Swampert-TuckerGold',
>   'Metagross-TuckerGold',
>   'Slaking-SpenserSilver',
>   'Slaking-SpenserGold',
>   'Heracross-GretaSilver',
>   'Shedinja-GretaSilver',
>   'Steelix-LucyGold',
>   'Regirock-BrandonSilver',
>   'Zapdos-BrandonGold',
>   'Moltres-BrandonGold',
> ]
> ```
>
> </details>


Other optional parameters are passed through to the damage calculator:


> ```python
> from frontierbrain3 import Field
> ```


> ```python
> db.sets.diesTo(meta, atk_boosts={"atk": 1})
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(335 sets)
> [  # 335 items
>   'Sunkern-1',
>   'Azurill-1',
>   'Caterpie-1',
>   'Weedle-1',
>   'Wurmple-1',
>   'Ralts-1',
>   'Feebas-1',
>   'Metapod-1',
>   'Kakuna-1',
>   'Pichu-1',
>   'Silcoon-1',
>   'Cascoon-1',
>   'Igglybuff-1',
>   'Tyrogue-1',
>   'Sentret-1',
>   ... (305 more) ...
>   'Tyranitar-5',
>   'Tyranitar-6',
>   'Tyranitar-7',
>   'Tyranitar-8',
>   'Tyranitar-9',
>   'Tyranitar-10',
>   'Articuno-5',
>   'Articuno-6',
>   'Alakazam-AnabelSilver',
>   'Heracross-GretaSilver',
>   'Shedinja-GretaSilver',
>   'Breloom-GretaGold',
>   'Seviper-LucyGold',
>   'Regice-BrandonSilver',
>   'Articuno-BrandonGold',
> ]
> ```
>
> </details>


> ```python
> ttar = db.allSets("Tyranitar")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ttar = {
>   'Pokemon': 'Tyranitar',
>   'SetNum': 1,
>   'Nature': 'Hardy',
>   'Item': 'BrightPowder',
>   'Abilities': ['Sand Stream'],
>   'Moves': ['earthquake', 'aerialace', 'thunderbolt', 'surf'],
>   'EVs': [0, 255, 0, 255, 0, 0],
>   'Index': 861,
>   'DexNum': 248,
> }
> ```
>
> </details>


> ```python
> db.sets.willOHKO(ttar, field=Field(weather="rain"))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(103 sets)
> [  # 103 items
>   'Meditite-1',
>   'Hitmonlee-1',
>   'Hitmonchan-1',
>   'Poliwrath-1',
>   'Pinsir-1',
>   'Machoke-2',
>   'Combusken-2',
>   'Sealeo-2',
>   'Seadra-2',
>   'Primeape-2',
>   'Hitmonlee-2',
>   'Hitmonchan-2',
>   'Sharpedo-2',
>   'Gorebyss-2',
>   'Omastar-2',
>   ... (73 more) ...
>   'Machamp-5',
>   'Machamp-6',
>   'Machamp-7',
>   'Machamp-8',
>   'Starmie-5',
>   'Starmie-8',
>   'Lapras-6',
>   'Regirock-5',
>   'Registeel-5',
>   'Tyranitar-7',
>   'Suicune-5',
>   'Metagross-TuckerGold',
>   'Breloom-GretaGold',
>   'Milotic-LucySilver',
>   'Regirock-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.canOHKO(lax, include_ohko=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(50 sets)
> [  # 50 items
>   'Gligar-2',
>   'Seaking-2',
>   'Crawdaunt-2',
>   'Kingler-2',
>   'Pinsir-2',
>   'Nidoking-1',
>   'Breloom-2',
>   'Glalie-2',
>   'Rhydon-2',
>   'Dugtrio-3',
>   'Breloom-3',
>   'Forretress-3',
>   'Whiscash-3',
>   'Dewgong-3',
>   'Shiftry-3',
>   ... (20 more) ...
>   'Wailord-4',
>   'Steelix-4',
>   'Exeggutor-4',
>   'Walrein-4',
>   'Regirock-1',
>   'Regirock-2',
>   'Machamp-7',
>   'Lapras-7',
>   'Lapras-8',
>   'Metagross-5',
>   'Metagross-8',
>   'Regirock-6',
>   'Lapras-SpenserSilver',
>   'Breloom-GretaGold',
>   'Regirock-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.willOHKO(ttar, include_acc=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(0 sets)
> []
> ```
>
> </details>


#### Negation

Every filter has a negated form via `.Not`:


> ```python
> ttar = db.allSets("Tyranitar")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ttar = {
>   'Pokemon': 'Tyranitar',
>   'SetNum': 1,
>   'Nature': 'Hardy',
>   'Item': 'BrightPowder',
>   'Abilities': ['Sand Stream'],
>   'Moves': ['earthquake', 'aerialace', 'thunderbolt', 'surf'],
>   'EVs': [0, 255, 0, 255, 0, 0],
>   'Index': 861,
>   'DexNum': 248,
> }
> ```
>
> </details>


> ```python
> hera = CustomSet("Heracross", nature="Adamant", evs=[4,252,0,0,0,252],
>                  item="Choice Band", moves=["Megahorn", "Earthquake", "Brick Break", "Rock Slide"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> hera = CustomSet(Heracross, nature=Adamant, evs=[4, 252, 0, 0, 0, 252], ivs=[31, 31, 31, 31, 31, 31], level=100, item=Choice Band, ability=swarm, moves=['megahorn', 'earthquake', 'brickbreak', 'rockslide'])
> ```
>
> </details>


> ```python
> db.sets.hasMove("earthquake").Not.hasMove("surf")     # has EQ but not Surf
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(150 sets)
> [  # 150 items
>   'Lickitung-2',
>   'Graveler-2',
>   'Wailmer-2',
>   'Marshtomp-2',
>   'Sudowoodo-2',
>   'Magcargo-2',
>   'Pupitar-2',
>   'Gligar-2',
>   'Lairon-2',
>   'Arbok-2',
>   'Solrock-2',
>   'Sandslash-2',
>   'Piloswine-2',
>   'Seviper-2',
>   'Camerupt-2',
>   ... (120 more) ...
>   'Dragonite-10',
>   'Tyranitar-2',
>   'Tyranitar-3',
>   'Tyranitar-5',
>   'Tyranitar-6',
>   'Tyranitar-9',
>   'Tyranitar-10',
>   'Salamence-TuckerSilver',
>   'Charizard-TuckerSilver',
>   'Metagross-TuckerGold',
>   'Slaking-SpenserSilver',
>   'Slaking-SpenserGold',
>   'Steelix-LucyGold',
>   'Regirock-BrandonSilver',
>   'Registeel-BrandonSilver',
> ]
> ```
>
> </details>


> ```python
> db.sets.Not.canDieTo(hera)                             # survives Heracross even on max roll
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(173 sets)
> [  # 173 items
>   'Duskull-1',
>   'Koffing-1',
>   'Machoke-1',
>   'Haunter-1',
>   'Togetic-1',
>   'Azumarill-1',
>   'Gligar-1',
>   'Pelipper-1',
>   'Noctowl-1',
>   'Sandslash-1',
>   'Primeape-1',
>   'Hitmonlee-1',
>   'Hitmonchan-1',
>   'Hitmontop-1',
>   'Banette-1',
>   ... (143 more) ...
>   'Swampert-TuckerSilver',
>   'Salamence-TuckerSilver',
>   'Swampert-TuckerGold',
>   'Metagross-TuckerGold',
>   'Slaking-SpenserSilver',
>   'Lapras-SpenserSilver',
>   'Suicune-SpenserGold',
>   'Heracross-GretaSilver',
>   'Gengar-GretaGold',
>   'Shuckle-LucySilver',
>   'Steelix-LucyGold',
>   'Gyarados-LucyGold',
>   'Regirock-BrandonSilver',
>   'Registeel-BrandonSilver',
>   'Zapdos-BrandonGold',
> ]
> ```
>
> </details>


> ```python
> db.sets.hasMove("earthquake").Not.willOHKO(ttar)       # EQ users that don't guaranteed OHKO Ttar
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(151 sets)
> [  # 151 items
>   'Lickitung-2',
>   'Graveler-2',
>   'Wailmer-2',
>   'Marshtomp-2',
>   'Sudowoodo-2',
>   'Magcargo-2',
>   'Pupitar-2',
>   'Gligar-2',
>   'Lairon-2',
>   'Arbok-2',
>   'Solrock-2',
>   'Sandslash-2',
>   'Piloswine-2',
>   'Seviper-2',
>   'Camerupt-2',
>   ... (121 more) ...
>   'Tyranitar-1',
>   'Tyranitar-2',
>   'Tyranitar-3',
>   'Tyranitar-5',
>   'Tyranitar-6',
>   'Tyranitar-9',
>   'Tyranitar-10',
>   'Swampert-TuckerSilver',
>   'Salamence-TuckerSilver',
>   'Charizard-TuckerSilver',
>   'Swampert-TuckerGold',
>   'Slaking-SpenserSilver',
>   'Slaking-SpenserGold',
>   'Steelix-LucyGold',
>   'Registeel-BrandonSilver',
> ]
> ```
>
> </details>


#### Trainer Lookup


> ```python
> db.sets.hasType("Water").hasMove("surf").usedByTrainer()
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(158 trainers)
> [  # 158 items
>   'PSYCHIC (M) NORTON',
>   'PSYCHIC (M) LUKAS',
>   'PSYCHIC (M) ZACH',
>   'PSYCHIC (F) KAITLYN',
>   'PSYCHIC (F) BREANNA',
>   'PSYCHIC (F) KENDRA',
>   'HEX MANIAC MOLLY',
>   'HEX MANIAC JAZMIN',
>   'HEX MANIAC KELSEY',
>   'POKÉMANIAC JALEN',
>   'POKÉMANIAC GRIFFEN',
>   'POKÉMANIAC XANDER',
>   'GENTLEMAN MARVIN',
>   'GENTLEMAN BRENNAN',
>   'COLLECTOR GABRIEL',
>   ... (128 more) ...
>   'GUITARIST RAYMOND',
>   'BIRD KEEPER DIRK',
>   'BIRD KEEPER HAROLD',
>   'SAILOR OMAR',
>   'SAILOR PETER',
>   'PARASOL LADY ALIVIA',
>   'PARASOL LADY PAIGE',
>   'BEAUTY ANYA',
>   'BEAUTY DAWN',
>   'AROMA LADY ABBY',
>   'AROMA LADY GRETEL',
>   'DOME ACE TUCKER',
>   'DOME ACE TUCKER',
>   'PALACE MAVEN SPENSER',
>   'PIKE QUEEN LUCY',
> ]
> ```
>
> </details>


### TrainerCollection

Supports `len()`, iteration, `.names()` (returns `["CLASS Name", ...]`), and `.Not`.


> ```python
> db.trainers.hasPokemon("Charizard")                           # trainers with any Charizard set
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(50 trainers)
> [  # 50 items
>   'COOLTRAINER (M) COOPER',
>   'COOLTRAINER (F) LYNN',
>   'DRAGON TAMER ROBERTO',
>   'DRAGON TAMER DAMIAN',
>   'DRAGON TAMER BRODY',
>   'DRAGON TAMER GRAHAM',
>   'PKMN BREEDER (M) CORDELL',
>   'RICH BOY ISSAC',
>   'RICH BOY QUINTON',
>   'LADY SALMA',
>   'LADY ANSLEY',
>   'KINDLER KAMERON',
>   'KINDLER ALFREDO',
>   'GENTLEMAN RUBEN',
>   'GENTLEMAN LAMAR',
>   ... (20 more) ...
>   'TRIATHLETE (F RUNNER) DOROTHY',
>   'TRIATHLETE (F RUNNER) PIPER',
>   'TRIATHLETE (M BIKER) NICO',
>   'TRIATHLETE (M BIKER) JEREMY',
>   'TRIATHLETE (F BIKER) CAITLIN',
>   'TRIATHLETE (F BIKER) REENA',
>   'COLLECTOR GIDEON',
>   'COLLECTOR TRISTON',
>   'BIRD KEEPER DIRK',
>   'BIRD KEEPER HAROLD',
>   'KINDLER ANDRE',
>   'KINDLER FERRIS',
>   'PARASOL LADY ALIVIA',
>   'PARASOL LADY PAIGE',
>   'DOME ACE TUCKER',
> ]
> ```
>
> </details>


> ```python
> db.trainers.hasPokemon("Charizard").Not.hasPokemon("Blastoise")  # Charizard but no Blastoise
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(17 trainers)
> [
>   'DRAGON TAMER ROBERTO',
>   'DRAGON TAMER DAMIAN',
>   'DRAGON TAMER BRODY',
>   'DRAGON TAMER GRAHAM',
>   'KINDLER KAMERON',
>   'KINDLER ALFREDO',
>   'DRAGON TAMER MADDOX',
>   'DRAGON TAMER DAVIN',
>   'DRAGON TAMER TREVON',
>   'BLACK BELT BRET',
>   'BATTLE GIRL ELENA',
>   'POKÉMANIAC LAYTON',
>   'BIRD KEEPER DIRK',
>   'BIRD KEEPER HAROLD',
>   'KINDLER ANDRE',
>   'KINDLER FERRIS',
>   'DOME ACE TUCKER',
> ]
> ```
>
> </details>


> ```python
> db.trainers.hasSet("Metagross-4")                              # trainers with a specific set
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(28 trainers)
> [
>   'PKMN BREEDER (M) OSCAR',
>   'PKMN BREEDER (M) WILSON',
>   'PKMN BREEDER (F) CLARE',
>   'PKMN BREEDER (F) TESS',
>   'COOLTRAINER (M) ALONZO',
>   'COOLTRAINER (M) VINCE',
>   'COOLTRAINER (F) CARRIE',
>   'PKMN RANGER (M) TYLER',
>   'BLACK BELT RAUL',
>   'BATTLE GIRL ALANA',
>   'EXPERT (M) ALEXAS',
>   'EXPERT (F) NADIA',
>   'PSYCHIC (M) ROLANDO',
>   'PSYCHIC (M) STANLY',
>   'PSYCHIC (M) DARIO',
>   'PSYCHIC (F) KARLEE',
>   'PSYCHIC (F) JAYLIN',
>   'PSYCHIC (F) INGRID',
>   'POKÉMANIAC MARV',
>   'POKÉMANIAC LAYTON',
>   'GENTLEMAN BROOKS',
>   'GENTLEMAN GREGORY',
>   'TRIATHLETE (M RUNNER) MASON',
>   'TRIATHLETE (M BIKER) NICO',
>   'RUIN MANIAC HUGO',
>   'RUIN MANIAC BRYCE',
>   'HIKER DEV',
>   'HIKER COREY',
> ]
> ```
>
> </details>


---

## Damage Calculator (`damagecalc`)

Implements the Gen 3 damage formula, referencing [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Damage) and [turskain's Frontier Calc](https://turskain.github.io/). Handles all Gen 3 mechanics including the physical/special split by type, ability immunities, item boosts, weather, screens, crits, stat stages, and special moves.

The examples below assume this setup:


> ```python
> from frontierbrain3 import (
>     Database, CustomSet, damage_rolls, calc_matchup,
>     format_result, ko_chance, calc_stats, Field,
> )
> ```


> ```python
> db = Database()
> ```


> ```python
> meta = db.allSets("Metagross")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> meta = {
>   'Pokemon': 'Metagross',
>   'SetNum': 1,
>   'Nature': 'Adamant',
>   'Item': 'Leftovers',
>   'Abilities': ['Clear Body'],
>   'Moves': ['meteormash', 'aerialace', 'facade', 'lightscreen'],
>   'EVs': [0, 170, 0, 0, 170, 170],
>   'Index': 467,
>   'DexNum': 376,
> }
> ```
>
> </details>


> ```python
> ttar = db.allSets("Tyranitar")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ttar = {
>   'Pokemon': 'Tyranitar',
>   'SetNum': 1,
>   'Nature': 'Hardy',
>   'Item': 'BrightPowder',
>   'Abilities': ['Sand Stream'],
>   'Moves': ['earthquake', 'aerialace', 'thunderbolt', 'surf'],
>   'EVs': [0, 255, 0, 255, 0, 0],
>   'Index': 861,
>   'DexNum': 248,
> }
> ```
>
> </details>


> ```python
> lax  = db.allSets("Snorlax")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> lax = {
>   'Pokemon': 'Snorlax',
>   'SetNum': 1,
>   'Nature': 'Adamant',
>   'Item': 'Leftovers',
>   'Abilities': ['Immunity', 'Thick Fat'],
>   'Moves': ['facade', 'shadowball', 'attract', 'doubleteam'],
>   'EVs': [0, 255, 255, 0, 0, 0],
>   'Index': 461,
>   'DexNum': 143,
> }
> ```
>
> </details>


> ```python
> zam  = db.allSets("Alakazam")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> zam = {
>   'Pokemon': 'Alakazam',
>   'SetNum': 1,
>   'Nature': 'Modest',
>   'Item': 'Focus Band',
>   'Abilities': ['Synchronize', 'Inner Focus'],
>   'Moves': ['thunderpunch', 'firepunch', 'icepunch', 'thunderwave'],
>   'EVs': [0, 0, 255, 255, 0, 0],
>   'Index': 405,
>   'DexNum': 65,
> }
> ```
>
> </details>


> ```python
> sala = db.allSets("Salamence")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> sala = {
>   'Pokemon': 'Salamence',
>   'SetNum': 1,
>   'Nature': 'Hardy',
>   'Item': "King's Rock",
>   'Abilities': ['Intimidate'],
>   'Moves': ['dragonclaw', 'aerialace', 'headbutt', 'rockslide'],
>   'EVs': [0, 255, 0, 0, 0, 255],
>   'Index': 466,
>   'DexNum': 373,
> }
> ```
>
> </details>


> ```python
> starmie = CustomSet("Starmie", nature="Timid", evs=[0,0,0,252,4,252],
>                     moves=["Surf", "Psychic", "Thunderbolt", "Ice Beam"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> starmie = CustomSet(Starmie, nature=Timid, evs=[0, 0, 0, 252, 4, 252], ivs=[31, 31, 31, 31, 31, 31], level=100, ability=illuminate, moves=['surf', 'psychic', 'thunderbolt', 'icebeam'])
> ```
>
> </details>


> ```python
> hera = CustomSet("Heracross", nature="Adamant", evs=[4,252,0,0,0,252],
>                  item="Choice Band", ability="Guts",
>                  moves=["Megahorn", "Earthquake", "Brick Break", "Rock Slide"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> hera = CustomSet(Heracross, nature=Adamant, evs=[4, 252, 0, 0, 0, 252], ivs=[31, 31, 31, 31, 31, 31], level=100, item=Choice Band, ability=Guts, moves=['megahorn', 'earthquake', 'brickbreak', 'rockslide'])
> ```
>
> </details>


### Specifying Moves

Moves can be passed as a string name (looked up from `data/moves.json`):


> ```python
> result = calc_matchup(meta, ttar, "Earthquake")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> result = {
>   'rolls': [215, 218, 220, 223, 226, 228, 231, 233, 236, 238, 241, 243, 246, 248, 251, 254],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 215,
>   'max': 254,
>   'min_pct': 63.00,
>   'max_pct': 74.50,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 1.0},
> }
> ```
>
> </details>


> ```python
> result = calc_matchup(starmie, ttar, "Surf")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> result = {
>   'rolls': [261, 264, 267, 271, 274, 277, 280, 283, 286, 289, 292, 295, 298, 301, 304, 308],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 261,
>   'max': 308,
>   'min_pct': 76.50,
>   'max_pct': 90.30,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 1.0},
> }
> ```
>
> </details>


All move properties, including special behavior for fixed-damage moves, variable-power moves, multi-hit moves, etc., are handled automatically based on the move name.

Alternatively, pass a dict with `name`, `type`, and `power` keys. This is useful for Hidden Power (where type/power vary per Pokemon) or for ROM hacks with custom moves:


> ```python
> hp_grass = {"name": "HP Grass", "type": "grass", "power": 70}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> hp_grass = {
>   'name': 'HP Grass',
>   'type': 'grass',
>   'power': 70,
> }
> ```
>
> </details>


> ```python
> result = calc_matchup(starmie, ttar, hp_grass)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> result = {
>   'rolls': [129, 130, 132, 133, 135, 136, 138, 139, 141, 142, 144, 145, 147, 148, 150, 152],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 129,
>   'max': 152,
>   'min_pct': 37.80,
>   'max_pct': 44.60,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 1.0},
> }
> ```
>
> </details>


### Basic Usage


> ```python
> rolls = damage_rolls(meta, ttar, "Earthquake")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> rolls = [215, 218, 220, 223, 226, 228, 231, 233, 236, 238, 241, 243, 246, 248, 251, 254]
> ```
>
> </details>


> ```python
> result = calc_matchup(meta, ttar, "Earthquake")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> result = {
>   'rolls': [215, 218, 220, 223, 226, 228, 231, 233, 236, 238, 241, 243, 246, 248, 251, 254],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 215,
>   'max': 254,
>   'min_pct': 63.00,
>   'max_pct': 74.50,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 1.0},
> }
> ```
>
> </details>


> ```python
> print(format_result(result, "Earthquake"))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> Earthquake: 215-254 (63.0% - 74.5%) [HP: 341]
>   Per-hit rolls: (215, 218, 220, 223, 226, 228, 231, 233, 236, 238, 241, 243, 246, 248, 251, 254)
>   guaranteed 2HKO
> ```
>
> </details>


### Raw API

For fine-grained control, use `damage_rolls` + `ko_chance` directly:


> ```python
> rolls = damage_rolls(meta, ttar, "Earthquake")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> rolls = [215, 218, 220, 223, 226, 228, 231, 233, 236, 238, 241, 243, 246, 248, 251, 254]
> ```
>
> </details>


> ```python
> ttar_hp = calc_stats(ttar)["hp"]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ttar_hp = 341
> ```
>
> </details>


> ```python
> kos = ko_chance(rolls, ttar_hp)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> kos = {
>   1: 0.00,
>   2: 1.00,
> }
> ```
>
> </details>


> ```python
> kos = ko_chance(rolls, ttar_hp, recovery=ttar_hp // 16)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> kos = {
>   1: 0.00,
>   2: 1.00,
> }
> ```
>
> </details>


### Attacker and Defender

Both can be either a frontier set dict (from the database) or a `CustomSet`:


> ```python
> calc_matchup(meta, ttar, "Earthquake")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [215, 218, 220, 223, 226, 228, 231, 233, 236, 238, 241, 243, 246, 248, 251, 254],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 215,
>   'max': 254,
>   'min_pct': 63.00,
>   'max_pct': 74.50,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 1.0},
> }
> ```
>
> </details>


> ```python
> calc_matchup(starmie, lax, "Surf")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [120, 122, 123, 124, 126, 127, 129, 130, 132, 133, 134, 136, 137, 139, 140, 142],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 120,
>   'max': 142,
>   'min_pct': 26.00,
>   'max_pct': 30.80,
>   'defender_hp': 461,
>   'defender_max_hp': 461,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 0.0, 4: 1.0},
> }
> ```
>
> </details>


> ```python
> swam = db.allSets("Swampert")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> swam = {
>   'Pokemon': 'Swampert',
>   'SetNum': 1,
>   'Nature': 'Adamant',
>   'Item': 'Lum Berry',
>   'Abilities': ['Torrent'],
>   'Moves': ['earthquake', 'counter', 'rest', 'curse'],
>   'EVs': [170, 0, 170, 0, 170, 0],
>   'Index': 459,
>   'DexNum': 260,
> }
> ```
>
> </details>


> ```python
> calc_matchup(meta, swam, "Earthquake", atk_ivs=15, def_ivs=15, atk_level=50, def_level=50)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [56, 57, 58, 58, 59, 60, 60, 61, 62, 62, 63, 64, 64, 65, 66, 67],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 56,
>   'max': 67,
>   'min_pct': 29.80,
>   'max_pct': 35.60,
>   'defender_hp': 188,
>   'defender_max_hp': 188,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 0.27, 4: 1.0},
> }
> ```
>
> </details>


### Field Conditions


> ```python
> from frontierbrain3 import Field
> ```


> ```python
> calc_matchup(starmie, ttar, "Surf", field=Field(weather="rain"))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [389, 393, 398, 403, 407, 412, 416, 421, 425, 430, 435, 439, 444, 448, 453, 458],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 389,
>   'max': 458,
>   'min_pct': 114.10,
>   'max_pct': 134.30,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 1.0},
> }
> ```
>
> </details>


> ```python
> calc_matchup(meta, ttar, "Earthquake", field=Field(reflect=True))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [108, 110, 111, 112, 113, 115, 116, 117, 119, 120, 121, 122, 124, 125, 126, 128],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 108,
>   'max': 128,
>   'min_pct': 31.70,
>   'max_pct': 37.50,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 0.89, 4: 1.0},
> }
> ```
>
> </details>


> ```python
> calc_matchup(starmie, ttar, "Surf", field=Field(is_doubles=True))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [261, 264, 267, 271, 274, 277, 280, 283, 286, 289, 292, 295, 298, 301, 304, 308],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 261,
>   'max': 308,
>   'min_pct': 76.50,
>   'max_pct': 90.30,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 1.0},
> }
> ```
>
> </details>


> ```python
> Field(weather="rain", reflect=True, is_doubles=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> Field(weather='rain', reflect=True, light_screen=False, is_doubles=True, helping_hand=False, cloud_nine=False)
> ```
>
> </details>


### Stat Boosts


> ```python
> calc_matchup(sala, ttar, "Earthquake", atk_boosts={"atk": 1})
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [311, 314, 318, 322, 325, 329, 333, 336, 340, 344, 347, 351, 355, 358, 362, 366],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 311,
>   'max': 366,
>   'min_pct': 91.20,
>   'max_pct': 107.30,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.43, 2: 1.0},
> }
> ```
>
> </details>


> ```python
> calc_matchup(starmie, lax, "Surf", def_boosts={"spd": 1})
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 81,
>   'max': 96,
>   'min_pct': 17.60,
>   'max_pct': 20.80,
>   'defender_hp': 461,
>   'defender_max_hp': 461,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.04, 6: 1.0},
> }
> ```
>
> </details>


> ```python
> calc_matchup(meta, zam, "Meteor Mash", atk_boosts={"atk": -1})
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [145, 147, 148, 150, 152, 153, 155, 157, 159, 160, 162, 164, 165, 167, 169, 171],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 145,
>   'max': 171,
>   'min_pct': 57.80,
>   'max_pct': 68.10,
>   'defender_hp': 251,
>   'defender_max_hp': 251,
>   'ko_chances': {1: 0.0, 2: 1.0},
> }
> ```
>
> </details>


> ```python
> calc_matchup(sala, lax, "Earthquake", def_boosts={"def": 2}, critical=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [232, 235, 238, 241, 243, 246, 249, 252, 254, 257, 260, 263, 265, 268, 271, 274],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 232,
>   'max': 274,
>   'min_pct': 50.30,
>   'max_pct': 59.40,
>   'defender_hp': 461,
>   'defender_max_hp': 461,
>   'ko_chances': {1: 0.0, 2: 1.0},
> }
> ```
>
> </details>


### Status Conditions


> ```python
> calc_matchup(meta, ttar, "Earthquake", atk_status="burn")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [108, 110, 111, 112, 113, 115, 116, 117, 119, 120, 121, 122, 124, 125, 126, 128],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 108,
>   'max': 128,
>   'min_pct': 31.70,
>   'max_pct': 37.50,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 0.89, 4: 1.0},
> }
> ```
>
> </details>


> ```python
> calc_matchup(hera, ttar, "Megahorn", atk_status="burn")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [868, 878, 889, 899, 909, 919, 930, 940, 950, 960, 970, 981, 991, 1001, 1011, 1022],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 868,
>   'max': 1022,
>   'min_pct': 254.50,
>   'max_pct': 299.70,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 1.0},
> }
> ```
>
> </details>


> ```python
> calc_matchup(meta, lax, "Facade", atk_status="burn")  # 140 BP
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 85,
>   'max': 100,
>   'min_pct': 18.40,
>   'max_pct': 21.70,
>   'defender_hp': 461,
>   'defender_max_hp': 461,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.57, 6: 1.0},
> }
> ```
>
> </details>


> ```python
> milotic = db.allSets("Milotic")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> milotic = {
>   'Pokemon': 'Milotic',
>   'SetNum': 1,
>   'Nature': 'Modest',
>   'Item': 'Lum Berry',
>   'Abilities': ['Marvel Scale'],
>   'Moves': ['hydropump', 'icywind', 'recover', 'mirrorcoat'],
>   'EVs': [170, 0, 170, 170, 0, 0],
>   'Index': 464,
>   'DexNum': 350,
> }
> ```
>
> </details>


> ```python
> calc_matchup(meta, milotic, "Earthquake", def_status="burn")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [78, 79, 80, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 78,
>   'max': 92,
>   'min_pct': 20.90,
>   'max_pct': 24.70,
>   'defender_hp': 373,
>   'defender_max_hp': 373,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 1.0},
> }
> ```
>
> </details>


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


> ```python
> from frontierbrain3.damagecalc import get_hit_info
> ```


> ```python
> get_hit_info("Double Kick")   # {"type": "fixed", "hits": 2}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'type': 'fixed',
>   'hits': 2,
> }
> ```
>
> </details>


> ```python
> get_hit_info("Bullet Seed")   # {"type": "variable", "weights": {2:3, 3:3, 4:1, 5:1}}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'type': 'variable',
>   'weights': {2: 3, 3: 3, 4: 1, 5: 1},
> }
> ```
>
> </details>


> ```python
> get_hit_info("Triple Kick")   # {"type": "triple_kick", "powers": [10,20,30], "acc": 0.9}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'type': 'triple_kick',
>   'powers': [10, 20, 30],
>   'acc': 0.90,
> }
> ```
>
> </details>


> ```python
> get_hit_info("Earthquake")    # {"type": "single"}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'type': 'single',
> }
> ```
>
> </details>


`calc_matchup` and the OHKO filters handle multi-hit convolution automatically. For manual use:


> ```python
> from frontierbrain3.damagecalc import combine_multi_hit_rolls, multi_hit_ohko_prob
> ```


> ```python
> blaziken = db.allSets("Blaziken")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> blaziken = {
>   'Pokemon': 'Blaziken',
>   'SetNum': 1,
>   'Nature': 'Docile',
>   'Item': 'Quick Claw',
>   'Abilities': ['Blaze'],
>   'Moves': ['flamethrower', 'sunnyday', 'doublekick', 'roar'],
>   'EVs': [0, 255, 0, 255, 0, 0],
>   'Index': 452,
>   'DexNum': 257,
> }
> ```
>
> </details>


> ```python
> per_hit = damage_rolls(blaziken, lax, "Double Kick")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> per_hit = [98, 99, 100, 102, 103, 104, 105, 106, 107, 109, 110, 111, 112, 113, 114, 116]
> ```
>
> </details>


> ```python
> hit_info = get_hit_info("Double Kick")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> hit_info = {
>   'type': 'fixed',
>   'hits': 2,
> }
> ```
>
> </details>


> ```python
> total_rolls = combine_multi_hit_rolls(per_hit, hit_info)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> total_rolls = [  # 256 items
>   196,
>   197,
>   197,
>   198,
>   198,
>   198,
>   199,
>   199,
>   200,
>   200,
>   200,
>   201,
>   201,
>   201,
>   201,
>   ... (226 more) ...
>   226,
>   226,
>   226,
>   227,
>   227,
>   227,
>   227,
>   228,
>   228,
>   228,
>   229,
>   229,
>   230,
>   230,
>   232,
> ]
> ```
>
> </details>


> ```python
> ohko_prob = multi_hit_ohko_prob(per_hit, calc_stats(lax)["hp"], hit_info)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ohko_prob = 0.00
> ```
>
> </details>


### Recoil and Drain Reference

Not applied in the damage formula (they don't affect the hit), but provided as constants for external calculations:


> ```python
> from frontierbrain3.damagecalc import RECOIL_MOVES, DRAIN_MOVES
> ```


> ```python
> RECOIL_MOVES  # {"doubleedge": 1/3, "volttackle": 1/3, "submission": 1/4, ...}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'doubleedge': 0.33,
>   'struggle': 0.25,
>   'submission': 0.25,
>   'takedown': 0.25,
>   'volttackle': 0.33,
> }
> ```
>
> </details>


> ```python
> DRAIN_MOVES   # {"gigadrain": 1/2, "absorb": 1/2, "dreameater": 1/2, ...}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'absorb': 0.50,
>   'megadrain': 0.50,
>   'gigadrain': 0.50,
>   'leechlife': 0.50,
>   'dreameater': 0.50,
> }
> ```
>
> </details>


---

## Battle Tower (`facilities.tower`)

### Trainer Tiers

Tower trainers are grouped into tiers by index, each with fixed IVs and round eligibility. These are the same trainers used across all Battle Frontier facilities, though details like round eligibility and team size may differ slightly between facilities. The Ruby/Sapphire Battle Tower uses a different trainer list that is not currently supported.


> ```python
> from frontierbrain3.facilities.tower import TowerDatabase, get_tier, TIERS, BRAIN_IVS
> ```


> ```python
> get_tier(250)  # {"ivs": 31, "rounds": [8], "last_in_round": "any"}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'ivs': 31,
>   'rounds': [8],
>   'last_in_round': 'any',
> }
> ```
>
> </details>


> ```python
> get_tier(150)  # {"ivs": 15, "rounds": [3, 4, 5], "last_in_round": 3}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'ivs': 15,
>   'rounds': [3, 4, 5],
>   'last_in_round': 3,
> }
> ```
>
> </details>


> ```python
> BRAIN_IVS  # {"silver": 15, "gold": 31}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'silver': 15,
>   'gold': 31,
> }
> ```
>
> </details>


### TowerDatabase

Extends `Database` with tower-specific trainer filtering:


> ```python
> tower = TowerDatabase()
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> tower = <frontierbrain3.facilities.tower.TowerDatabase object at 0x000001D25A0417F0>
> ```
>
> </details>


> ```python
> tower.trainers.appearsInRound(8)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(100 trainers)
> [  # 100 items
>   'YOUNGSTER JAXON',
>   'YOUNGSTER LOGAN',
>   'LASS EMILEE',
>   'LASS JOSIE',
>   'CAMPER ARMANDO',
>   'CAMPER SKYLER',
>   'PICNICKER RUTH',
>   'PICNICKER MELODY',
>   'SWIMMER? PEDRO',
>   'SWIMMER? ERICK',
>   'SWIMMER? ELAINE',
>   'SWIMMER? JOYCE',
>   'POKÉFAN (M) TODD',
>   'POKÉFAN (M) GAVIN',
>   'POKÉFAN (F) MALORY',
>   ... (70 more) ...
>   'GUITARIST RAYMOND',
>   'BIRD KEEPER DIRK',
>   'BIRD KEEPER HAROLD',
>   'SAILOR OMAR',
>   'SAILOR PETER',
>   'HIKER DEV',
>   'HIKER COREY',
>   'KINDLER ANDRE',
>   'KINDLER FERRIS',
>   'PARASOL LADY ALIVIA',
>   'PARASOL LADY PAIGE',
>   'BEAUTY ANYA',
>   'BEAUTY DAWN',
>   'AROMA LADY ABBY',
>   'AROMA LADY GRETEL',
> ]
> ```
>
> </details>


> ```python
> tower.trainers.canBeLastInRound(7)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(80 trainers)
> [  # 80 items
>   'COOLTRAINER (M) LEON',
>   'COOLTRAINER (M) ALONZO',
>   'COOLTRAINER (M) VINCE',
>   'COOLTRAINER (M) BRYON',
>   'COOLTRAINER (F) AVA',
>   'COOLTRAINER (F) MIRIAM',
>   'COOLTRAINER (F) CARRIE',
>   'COOLTRAINER (F) GILLIAN',
>   'PKMN RANGER (M) TYLER',
>   'PKMN RANGER (M) CHAZ',
>   'PKMN RANGER (M) NELSON',
>   'PKMN RANGER (F) SHANIA',
>   'PKMN RANGER (F) STELLA',
>   'PKMN RANGER (F) DORINE',
>   'DRAGON TAMER MADDOX',
>   ... (50 more) ...
>   'GUITARIST RAYMOND',
>   'BIRD KEEPER DIRK',
>   'BIRD KEEPER HAROLD',
>   'SAILOR OMAR',
>   'SAILOR PETER',
>   'HIKER DEV',
>   'HIKER COREY',
>   'KINDLER ANDRE',
>   'KINDLER FERRIS',
>   'PARASOL LADY ALIVIA',
>   'PARASOL LADY PAIGE',
>   'BEAUTY ANYA',
>   'BEAUTY DAWN',
>   'AROMA LADY ABBY',
>   'AROMA LADY GRETEL',
> ]
> ```
>
> </details>


> ```python
> tower.trainers.appearsInRound(8).hasPokemon("Metagross")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(38 trainers)
> [  # 38 items
>   'PKMN BREEDER (M) OSCAR',
>   'PKMN BREEDER (M) WILSON',
>   'PKMN BREEDER (F) CLARE',
>   'PKMN BREEDER (F) TESS',
>   'COOLTRAINER (M) ALONZO',
>   'COOLTRAINER (M) VINCE',
>   'COOLTRAINER (F) CARRIE',
>   'PKMN RANGER (M) TYLER',
>   'PKMN RANGER (M) CHAZ',
>   'PKMN RANGER (F) SHANIA',
>   'PKMN RANGER (F) STELLA',
>   'BLACK BELT RAUL',
>   'BATTLE GIRL ALANA',
>   'EXPERT (M) ALEXAS',
>   'EXPERT (F) NADIA',
>   ... (8 more) ...
>   'POKÉMANIAC LAYTON',
>   'GENTLEMAN BROOKS',
>   'GENTLEMAN GREGORY',
>   'TRIATHLETE (M RUNNER) MASON',
>   'TRIATHLETE (M RUNNER) TOBY',
>   'TRIATHLETE (F RUNNER) DOROTHY',
>   'TRIATHLETE (F RUNNER) PIPER',
>   'TRIATHLETE (M BIKER) NICO',
>   'TRIATHLETE (M BIKER) JEREMY',
>   'TRIATHLETE (F BIKER) CAITLIN',
>   'TRIATHLETE (F BIKER) REENA',
>   'RUIN MANIAC HUGO',
>   'RUIN MANIAC BRYCE',
>   'HIKER DEV',
>   'HIKER COREY',
> ]
> ```
>
> </details>


> ```python
> tower.trainers.appearsInRound(8).Not.hasPokemon("Starmie")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(56 trainers)
> [  # 56 items
>   'YOUNGSTER JAXON',
>   'YOUNGSTER LOGAN',
>   'LASS EMILEE',
>   'LASS JOSIE',
>   'CAMPER ARMANDO',
>   'CAMPER SKYLER',
>   'PICNICKER RUTH',
>   'PICNICKER MELODY',
>   'POKÉFAN (M) TODD',
>   'POKÉFAN (M) GAVIN',
>   'POKÉFAN (F) MALORY',
>   'POKÉFAN (F) ESTHER',
>   'COOLTRAINER (M) ALONZO',
>   'COOLTRAINER (M) BRYON',
>   'COOLTRAINER (F) AVA',
>   ... (26 more) ...
>   'RUIN MANIAC HUGO',
>   'RUIN MANIAC BRYCE',
>   'COLLECTOR GIDEON',
>   'COLLECTOR TRISTON',
>   'GUITARIST CHARLES',
>   'BIRD KEEPER DIRK',
>   'BIRD KEEPER HAROLD',
>   'SAILOR OMAR',
>   'SAILOR PETER',
>   'HIKER DEV',
>   'HIKER COREY',
>   'KINDLER ANDRE',
>   'KINDLER FERRIS',
>   'BEAUTY ANYA',
>   'BEAUTY DAWN',
> ]
> ```
>
> </details>


### Random Team Generation

Generates a random trainer + 3-set team respecting species and item clause:


> ```python
> tower.random_team(8)                              # random round 8 team
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'PKMN Breeder (M) OSCAR: Starmie-4, Milotic-4, Arcanine-4'
> ```
>
> </details>


> ```python
> tower.random_team(8, trainer_class="Dragon Tamer") # filtered by class
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'Dragon Tamer TREVON: Latias-7, Tyranitar-9, Milotic-1'
> ```
>
> </details>


> ```python
> tower.random_team(name="Brady")                    # filtered by name (any round)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'Youngster BRADY: Shroomish-1, Shuppet-1, Makuhita-1'
> ```
>
> </details>


---

## Battle Factory (`facilities.factory`)

Unlike the Tower, Factory sets are not tied to specific trainers. Any trainer can use any set from the eligible pool. The relevant unit of generation is the team itself (3 sets respecting species/item clause), not a trainer-team pair.

### Groups and Pools

Factory sets are divided into 9 groups by index. Each round draws from specific groups:


> ```python
> from frontierbrain3.facilities.factory import FactoryDatabase, get_group
> ```


> ```python
> get_group(500)  # 5 (set index 500 is in group 5)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 5
> ```
>
> </details>


> ```python
> fac = FactoryDatabase()
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> fac = <frontierbrain3.facilities.factory.FactoryDatabase object at 0x000001D25A042A50>
> ```
>
> </details>


> ```python
> pool = fac.sets_in_groups([4, 5, 6, 7, 8])  # all sets in these groups
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> pool = [  # 478 items
>   {'Pokemon': 'Dugtrio', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Soft Sand', 'Abilities': ['Sand Veil', 'Arena Trap'], 'Moves': ['earthquake', 'triattack', 'slash', 'sandtomb'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 373, 'DexNum': 51},
>   {'Pokemon': 'Medicham', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Focus Band', 'Abilities': ['Pure Power'], 'Moves': ['psychic', 'hijumpkick', 'calmmind', 'batonpass'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 374, 'DexNum': 308},
>   {'Pokemon': 'Misdreavus', 'SetNum': 1, 'Nature': 'Impish', 'Item': 'Focus Band', 'Abilities': ['Levitate'], 'Moves': ['painsplit', 'shadowball', 'confuseray', 'thunderwave'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 375, 'DexNum': 200},
>   {'Pokemon': 'Fearow', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Sharp Beak', 'Abilities': ['Keen Eye'], 'Moves': ['drillpeck', 'triattack', 'facade', 'mudslap'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 376, 'DexNum': 22},
>   {'Pokemon': 'Granbull', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Cheri Berry', 'Abilities': ['Intimidate'], 'Moves': ['megakick', 'smellingsalt', 'thunderwave', 'roar'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 377, 'DexNum': 210},
>   {'Pokemon': 'Jynx', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Oblivious'], 'Moves': ['icebeam', 'fakeout', 'lovelykiss', 'attract'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 378, 'DexNum': 124},
>   {'Pokemon': 'Dusclops', 'SetNum': 1, 'Nature': 'Impish', 'Item': 'Leftovers', 'Abilities': ['Pressure'], 'Moves': ['willowisp', 'seismictoss', 'painsplit', 'confuseray'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 379, 'DexNum': 356},
>   {'Pokemon': 'Dodrio', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Run Away', 'Early Bird'], 'Moves': ['drillpeck', 'triattack', 'sleeptalk', 'rest'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 380, 'DexNum': 85},
>   {'Pokemon': 'Mr. Mime', 'SetNum': 1, 'Nature': 'Relaxed', 'Item': 'Leftovers', 'Abilities': ['Soundproof'], 'Moves': ['psychic', 'magicalleaf', 'fakeout', 'reflect'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 381, 'DexNum': 122},
>   {'Pokemon': 'Lanturn', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Cheri Berry', 'Abilities': ['Volt Absorb', 'Illuminate'], 'Moves': ['surf', 'confuseray', 'attract', 'thunderwave'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 382, 'DexNum': 171},
>   {'Pokemon': 'Breloom', 'SetNum': 1, 'Nature': 'Jolly', 'Item': "King's Rock", 'Abilities': ['Effect Spore'], 'Moves': ['skyuppercut', 'machpunch', 'headbutt', 'counter'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 383, 'DexNum': 286},
>   {'Pokemon': 'Forretress', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Sturdy'], 'Moves': ['doubleedge', 'rockslide', 'lightscreen', 'spikes'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 384, 'DexNum': 205},
>   {'Pokemon': 'Whiscash', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Oblivious'], 'Moves': ['earthquake', 'rockslide', 'amnesia', 'rest'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 385, 'DexNum': 340},
>   {'Pokemon': 'Xatu', 'SetNum': 1, 'Nature': 'Hardy', 'Item': 'Sharp Beak', 'Abilities': ['Synchronize', 'Early Bird'], 'Moves': ['drillpeck', 'nightshade', 'wish', 'futuresight'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 386, 'DexNum': 178},
>   {'Pokemon': 'Skarmory', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Scope Lens', 'Abilities': ['Keen Eye', 'Sturdy'], 'Moves': ['steelwing', 'aircutter', 'counter', 'agility'], 'EVs': [170, 170, 0, 0, 170, 0], 'Index': 387, 'DexNum': 227},
>   ... (448 more) ...
>   {'Pokemon': 'Metagross', 'SetNum': 8, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Clear Body'], 'Moves': ['meteormash', 'earthquake', 'brickbreak', 'explosion'], 'EVs': [170, 170, 0, 0, 0, 170], 'Index': 836, 'DexNum': 376},
>   {'Pokemon': 'Regirock', 'SetNum': 5, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Clear Body'], 'Moves': ['hyperbeam', 'focuspunch', 'rockslide', 'doubleteam'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 837, 'DexNum': 377},
>   {'Pokemon': 'Regirock', 'SetNum': 6, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Clear Body'], 'Moves': ['swagger', 'psychup', 'rockslide', 'explosion'], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 838, 'DexNum': 377},
>   {'Pokemon': 'Regice', 'SetNum': 5, 'Nature': 'Brave', 'Item': 'Leftovers', 'Abilities': ['Clear Body'], 'Moves': ['earthquake', 'icebeam', 'curse', 'counter'], 'EVs': [170, 0, 170, 170, 0, 0], 'Index': 839, 'DexNum': 378},
>   {'Pokemon': 'Regice', 'SetNum': 6, 'Nature': 'Modest', 'Item': 'Chesto Berry', 'Abilities': ['Clear Body'], 'Moves': ['icebeam', 'thunderbolt', 'sleeptalk', 'rest'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 840, 'DexNum': 378},
>   {'Pokemon': 'Registeel', 'SetNum': 5, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Clear Body'], 'Moves': ['focuspunch', 'substitute', 'toxic', 'doubleteam'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 841, 'DexNum': 379},
>   {'Pokemon': 'Registeel', 'SetNum': 6, 'Nature': 'Adamant', 'Item': 'White Herb', 'Abilities': ['Clear Body'], 'Moves': ['superpower', 'aerialace', 'swagger', 'psychup'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 842, 'DexNum': 379},
>   {'Pokemon': 'Latias', 'SetNum': 5, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Levitate'], 'Moves': ['dragonclaw', 'thunderwave', 'calmmind', 'recover'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 843, 'DexNum': 380},
>   {'Pokemon': 'Latias', 'SetNum': 6, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Levitate'], 'Moves': ['mistball', 'dragonclaw', 'attract', 'thunderwave'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 844, 'DexNum': 380},
>   {'Pokemon': 'Latias', 'SetNum': 7, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Levitate'], 'Moves': ['earthquake', 'shadowball', 'swagger', 'psychup'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 845, 'DexNum': 380},
>   {'Pokemon': 'Latias', 'SetNum': 8, 'Nature': 'Docile', 'Item': "King's Rock", 'Abilities': ['Levitate'], 'Moves': ['psychic', 'shadowball', 'earthquake', 'aerialace'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 846, 'DexNum': 380},
>   {'Pokemon': 'Latios', 'SetNum': 5, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Levitate'], 'Moves': ['dragonclaw', 'thunderwave', 'calmmind', 'recover'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 847, 'DexNum': 381},
>   {'Pokemon': 'Latios', 'SetNum': 6, 'Nature': 'Docile', 'Item': 'Shell Bell', 'Abilities': ['Levitate'], 'Moves': ['lusterpurge', 'shadowball', 'dragonclaw', 'thunderwave'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 848, 'DexNum': 381},
>   {'Pokemon': 'Latios', 'SetNum': 7, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Levitate'], 'Moves': ['earthquake', 'shadowball', 'dragondance', 'recover'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 849, 'DexNum': 381},
>   {'Pokemon': 'Latios', 'SetNum': 8, 'Nature': 'Docile', 'Item': "King's Rock", 'Abilities': ['Levitate'], 'Moves': ['psychic', 'shadowball', 'earthquake', 'aerialace'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 850, 'DexNum': 381},
> ]
> ```
>
> </details>


### Team Type and Phrase

Every Factory team gets a "type" (most common Pokemon type) and a "phrase" (battle style description):


> ```python
> from frontierbrain3.facilities.factory import FactoryDatabase, team_type, team_phrase
> ```


> ```python
> fac = FactoryDatabase()
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> fac = <frontierbrain3.facilities.factory.FactoryDatabase object at 0x000001D25A9E3250>
> ```
>
> </details>


> ```python
> sample_team = fac.sets_in_groups([7, 8])[:3]  # grab 3 sets for demonstration
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> sample_team = [
>   {'Pokemon': 'Medicham', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Lum Berry', 'Abilities': ['Pure Power'], 'Moves': ['megakick', 'psychic', 'shadowball', 'rockslide'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 662, 'DexNum': 308},
>   {'Pokemon': 'Misdreavus', 'SetNum': 4, 'Nature': 'Timid', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['destinybond', 'psychic', 'shadowball', 'thunderbolt'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 663, 'DexNum': 200},
>   {'Pokemon': 'Fearow', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Lum Berry', 'Abilities': ['Keen Eye'], 'Moves': ['drillpeck', 'doubleedge', 'steelwing', 'skyattack'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 664, 'DexNum': 22},
> ]
> ```
>
> </details>


> ```python
> team_type(sample_team)   # "Water", "Fire", "No Type", etc.
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'No Type'
> ```
>
> </details>


> ```python
> team_phrase(sample_team)  # "appears to be one based on total preparation", etc.
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'appears to be high risk, high return'
> ```
>
> </details>


### Random Team Generation

Generate teams with optional type/phrase constraints:


> ```python
> fac = FactoryDatabase()
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> fac = <frontierbrain3.facilities.factory.FactoryDatabase object at 0x000001D25A61D1D0>
> ```
>
> </details>


> ```python
> ids, typ, phrase = fac.random_team("open", 5)                           # unconstrained
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ids = ['Miltank-3', 'Walrein-2', 'Vileplume-4']
> typ = 'No Type'
> phrase = 'appears to be free-spirited and unrestrained'
> ```
>
> </details>


> ```python
> ids, typ, phrase = fac.random_team("open", 5, target_type="Water")       # Water teams only
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ids = ['Dragonite-6', 'Feraligatr-2', 'Lanturn-3']
> typ = 'Water'
> phrase = 'appears to be free-spirited and unrestrained'
> ```
>
> </details>


> ```python
> ids, typ, phrase = fac.random_team("open", 5, target_phrase=4)           # phrase 4 only
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ids = ['Dragonite-6', 'Aggron-4', 'Gengar-7']
> typ = 'No Type'
> phrase = 'appears to be high risk, high return'
> ```
>
> </details>


> ```python
> ids, typ, phrase = fac.random_team("lv50", 1, target_type="Fire", target_phrase=1)  # both
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ids = ["Farfetch'd-1", 'Houndour-1', 'Growlithe-1']
> typ = 'Fire'
> phrase = 'appears to be one based on total preparation'
> ```
>
> </details>


---

## Battle Dome (`facilities.dome`)

### Seeding

The Dome ranks teams by a seeding value. Higher seed = higher bracket position. Notably, the higher seed wins in case of a tie, unlike every other facility where a tie counts as a loss for the player.


> ```python
> from frontierbrain3 import Database, CustomSet
> from frontierbrain3.facilities.dome import calc_seed
> ```


> ```python
> db = Database()
> ```


> ```python
> meta = db.allSets("Metagross")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> meta = {
>   'Pokemon': 'Metagross',
>   'SetNum': 1,
>   'Nature': 'Adamant',
>   'Item': 'Leftovers',
>   'Abilities': ['Clear Body'],
>   'Moves': ['meteormash', 'aerialace', 'facade', 'lightscreen'],
>   'EVs': [0, 170, 0, 0, 170, 170],
>   'Index': 467,
>   'DexNum': 376,
> }
> ```
>
> </details>


> ```python
> lax  = db.allSets("Snorlax")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> lax = {
>   'Pokemon': 'Snorlax',
>   'SetNum': 1,
>   'Nature': 'Adamant',
>   'Item': 'Leftovers',
>   'Abilities': ['Immunity', 'Thick Fat'],
>   'Moves': ['facade', 'shadowball', 'attract', 'doubleteam'],
>   'EVs': [0, 255, 255, 0, 0, 0],
>   'Index': 461,
>   'DexNum': 143,
> }
> ```
>
> </details>


> ```python
> ttar = db.allSets("Tyranitar")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ttar = {
>   'Pokemon': 'Tyranitar',
>   'SetNum': 1,
>   'Nature': 'Hardy',
>   'Item': 'BrightPowder',
>   'Abilities': ['Sand Stream'],
>   'Moves': ['earthquake', 'aerialace', 'thunderbolt', 'surf'],
>   'EVs': [0, 255, 0, 255, 0, 0],
>   'Index': 861,
>   'DexNum': 248,
> }
> ```
>
> </details>


> ```python
> team = [meta, lax, ttar]  # exactly 3 sets
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> team = [
>   {'Pokemon': 'Metagross', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Clear Body'], 'Moves': ['meteormash', 'aerialace', 'facade', 'lightscreen'], 'EVs': [0, 170, 0, 0, 170, 170], 'Index': 467, 'DexNum': 376},
>   {'Pokemon': 'Snorlax', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Immunity', 'Thick Fat'], 'Moves': ['facade', 'shadowball', 'attract', 'doubleteam'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 461, 'DexNum': 143},
>   {'Pokemon': 'Tyranitar', 'SetNum': 1, 'Nature': 'Hardy', 'Item': 'BrightPowder', 'Abilities': ['Sand Stream'], 'Moves': ['earthquake', 'aerialace', 'thunderbolt', 'surf'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 861, 'DexNum': 248},
> ]
> ```
>
> </details>


> ```python
> calc_seed(team)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 4871
> ```
>
> </details>


> ```python
> calc_seed(team, is_enemy=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 2947
> ```
>
> </details>


> ```python
> calc_seed(team, level=50, ivs=15)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 2334
> ```
>
> </details>


> ```python
> calc_seed(team, level=50, ivs=15, is_enemy=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 2138
> ```
>
> </details>


`CustomSet` objects are supported for player teams (not with `is_enemy=True`).

**Seeding formula:** `unique_types x (highest_level // 20) + sum(all stats)`

**Enemy bugs:**
1. Stats calculated with 0 EVs regardless of the set's actual EVs
2. Non-HP stats taken mod 256 (overflow)

### Monte Carlo: estimating the score needed for seed #1

The enemy seeding bugs massively favor the player, but it's useful to know how high an enemy seed can actually get. Since the Dome draws from the same trainer/set pool as the Tower, we can use `TowerDatabase` to simulate round 8 enemy teams:


> ```python
> from frontierbrain3.facilities.tower import TowerDatabase
> from frontierbrain3.facilities.dome import calc_seed
> ```


> ```python
> tower = TowerDatabase()
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> tower = <frontierbrain3.facilities.tower.TowerDatabase object at 0x000001D25A4F6D50>
> ```
>
> </details>


> ```python
> set_lookup = {f"{s['Pokemon']}-{s['SetNum']}": s for s in tower._sets}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> set_lookup = {  # 918 entries
>   'Sunkern-1': {'Pokemon': 'Sunkern', 'SetNum': 1, 'Nature': 'Relaxed', 'Item': 'Lax Incense', 'Abilities': ['Chlorophyll'], 'Moves': ['megadrain', 'helpinghand', 'sunnyday', 'lightscreen'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 1, 'DexNum': 191},
>   'Azurill-1': {'Pokemon': 'Azurill', 'SetNum': 1, 'Nature': 'Rash', 'Item': 'Cheri Berry', 'Abilities': ['Thick Fat', 'Huge Power'], 'Moves': ['waterpulse', 'attract', 'sing', 'charm'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 2, 'DexNum': 298},
>   'Caterpie-1': {'Pokemon': 'Caterpie', 'SetNum': 1, 'Nature': 'Quirky', 'Item': 'Focus Band', 'Abilities': ['Shield Dust'], 'Moves': ['tackle', 'stringshot', '', ''], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 3, 'DexNum': 10},
>   'Weedle-1': {'Pokemon': 'Weedle', 'SetNum': 1, 'Nature': 'Quirky', 'Item': 'Focus Band', 'Abilities': ['Shield Dust'], 'Moves': ['poisonsting', 'stringshot', '', ''], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 4, 'DexNum': 13},
>   'Wurmple-1': {'Pokemon': 'Wurmple', 'SetNum': 1, 'Nature': 'Quirky', 'Item': 'Lax Incense', 'Abilities': ['Shield Dust'], 'Moves': ['tackle', 'stringshot', 'poisonsting', ''], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 5, 'DexNum': 265},
>   'Ralts-1': {'Pokemon': 'Ralts', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'TwistedSpoon', 'Abilities': ['Synchronize', 'Trace'], 'Moves': ['confusion', 'imprison', 'doubleteam', 'lightscreen'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 6, 'DexNum': 280},
>   'Magikarp-1': {'Pokemon': 'Magikarp', 'SetNum': 1, 'Nature': 'Hardy', 'Item': 'Focus Band', 'Abilities': ['Swift Swim'], 'Moves': ['flail', '', '', ''], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 7, 'DexNum': 129},
>   'Feebas-1': {'Pokemon': 'Feebas', 'SetNum': 1, 'Nature': 'Lonely', 'Item': 'Focus Band', 'Abilities': ['Swift Swim'], 'Moves': ['flail', 'mirrorcoat', '', ''], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 8, 'DexNum': 349},
>   'Metapod-1': {'Pokemon': 'Metapod', 'SetNum': 1, 'Nature': 'Bashful', 'Item': 'Lax Incense', 'Abilities': ['Shed Skin'], 'Moves': ['harden', '', '', ''], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 9, 'DexNum': 11},
>   'Kakuna-1': {'Pokemon': 'Kakuna', 'SetNum': 1, 'Nature': 'Bashful', 'Item': 'Lax Incense', 'Abilities': ['Shed Skin'], 'Moves': ['harden', '', '', ''], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 10, 'DexNum': 14},
>   'Pichu-1': {'Pokemon': 'Pichu', 'SetNum': 1, 'Nature': 'Rash', 'Item': 'Sitrus Berry', 'Abilities': ['Static'], 'Moves': ['sweetkiss', 'thunderwave', 'attract', 'shockwave'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 11, 'DexNum': 172},
>   'Silcoon-1': {'Pokemon': 'Silcoon', 'SetNum': 1, 'Nature': 'Bashful', 'Item': 'Lax Incense', 'Abilities': ['Shed Skin'], 'Moves': ['harden', '', '', ''], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 12, 'DexNum': 266},
>   'Cascoon-1': {'Pokemon': 'Cascoon', 'SetNum': 1, 'Nature': 'Bashful', 'Item': 'Lax Incense', 'Abilities': ['Shed Skin'], 'Moves': ['harden', '', '', ''], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 13, 'DexNum': 268},
>   'Igglybuff-1': {'Pokemon': 'Igglybuff', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Focus Band', 'Abilities': ['Cute Charm'], 'Moves': ['sweetkiss', 'sing', 'attract', 'seismictoss'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 14, 'DexNum': 174},
>   'Wooper-1': {'Pokemon': 'Wooper', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Sitrus Berry', 'Abilities': ['Damp', 'Water Absorb'], 'Moves': ['yawn', 'dig', 'waterpulse', 'raindance'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 15, 'DexNum': 194},
>   'Tyrogue-1': {'Pokemon': 'Tyrogue', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Focus Band', 'Abilities': ['Guts'], 'Moves': ['machpunch', 'protect', 'doubleteam', 'facade'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 16, 'DexNum': 236},
>   'Sentret-1': {'Pokemon': 'Sentret', 'SetNum': 1, 'Nature': 'Docile', 'Item': "King's Rock", 'Abilities': ['Run Away', 'Keen Eye'], 'Moves': ['quickattack', 'followme', 'helpinghand', 'assist'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 17, 'DexNum': 161},
>   'Cleffa-1': {'Pokemon': 'Cleffa', 'SetNum': 1, 'Nature': 'Serious', 'Item': 'Lax Incense', 'Abilities': ['Cute Charm'], 'Moves': ['sweetkiss', 'sing', 'attract', 'metronome'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 18, 'DexNum': 173},
>   'Seedot-1': {'Pokemon': 'Seedot', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Focus Band', 'Abilities': ['Chlorophyll', 'Early Bird'], 'Moves': ['bulletseed', 'bide', 'defensecurl', 'rollout'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 19, 'DexNum': 273},
>   'Lotad-1': {'Pokemon': 'Lotad', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Lax Incense', 'Abilities': ['Swift Swim', 'Rain Dish'], 'Moves': ['raindance', 'waterpulse', 'sunnyday', 'megadrain'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 20, 'DexNum': 270},
>   ... (898 more) ...
> }
> ```
>
> </details>


> ```python
> best_seed = 0
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> best_seed = 0
> ```
>
> </details>


> ```python
> best_team = ""
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> best_team = ''
> ```
>
> </details>


> ```python
> for _ in range(1000):
>     result = tower.random_team(8)
>     if result.startswith("Error"):
>         continue
>     label, ids_str = result.split(": ", 1)
>     set_ids = [s.strip() for s in ids_str.split(", ")]
>     team_sets = [set_lookup[sid] for sid in set_ids if sid in set_lookup]
>     if len(team_sets) == 3:
>         seed = calc_seed(team_sets, is_enemy=True)
>         if seed > best_seed:
>             best_seed = seed
>             best_team = result
> ```


> ```python
> print(f"Highest enemy seed: {best_seed}")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> Highest enemy seed: 4205
> ```
>
> </details>


> ```python
> print(f"Team: {best_team}")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> Team: PKMN Breeder (F) CLARE: Lapras-4, Charizard-4, Kingdra-4
> ```
>
> </details>


---

## Battle Palace (`facilities.palace`)

In the Palace, Pokemon choose moves autonomously. Each turn, the game first selects a move **category** (Attack, Defense, or Support) based on the Pokemon's nature. Then it picks one of the Pokemon's moves in that category uniformly at random (1/N chance if the category has N moves). If the selected category has no move in the set, there is a 50% chance the Pokemon picks a random move from all its moves and a 50% chance it wastes its turn.

### Move Categories

Palace classifies every move as attack, defense, or support:


> ```python
> from frontierbrain3.facilities.palace import get_move_category, categorize_moveset
> ```


> ```python
> get_move_category("Earthquake")  # "attack"
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'attack'
> ```
>
> </details>


> ```python
> get_move_category("Swords Dance") # "defense"
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'defense'
> ```
>
> </details>


> ```python
> get_move_category("Thunder Wave") # "support"
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'support'
> ```
>
> </details>


> ```python
> categorize_moveset(["Earthquake", "Rock Slide", "Swords Dance", "Thunder Wave"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'attack': ['Earthquake', 'Rock Slide'],
>   'defense': ['Swords Dance'],
>   'support': ['Thunder Wave'],
> }
> ```
>
> </details>


### Nature Ratios

Each nature has different category selection odds at high HP (>50%) and low HP (<=50%):


> ```python
> from frontierbrain3.facilities.palace import get_nature_ratios
> ```


> ```python
> get_nature_ratios("Adamant")              # {"attack": 0.38, "defense": 0.31, "support": 0.31}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'attack': 0.38,
>   'defense': 0.31,
>   'support': 0.31,
> }
> ```
>
> </details>


> ```python
> get_nature_ratios("Adamant", low_hp=True) # {"attack": 0.70, "defense": 0.15, "support": 0.15}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'attack': 0.70,
>   'defense': 0.15,
>   'support': 0.15,
> }
> ```
>
> </details>


### Effective Action Probabilities

Accounts for empty categories and the random-move fallback:


> ```python
> from frontierbrain3.facilities.palace import get_action_probabilities, get_move_probabilities
> ```


> ```python
> get_action_probabilities("Adamant", ["Earthquake", "Rock Slide", "Swords Dance", "Protect"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'attack': 0.46,
>   'defense': 0.39,
>   'support': 0.00,
>   'nothing': 0.15,
> }
> ```
>
> </details>


> ```python
> get_move_probabilities("Adamant", ["Earthquake", "Rock Slide", "Protect"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'Earthquake': 0.24,
>   'Rock Slide': 0.24,
>   'Protect': 0.36,
>   'nothing': 0.15,
> }
> ```
>
> </details>


### Multi-Turn Analysis

Analyze probabilities over multiple turns, either by category or by specific move:


> ```python
> from frontierbrain3.facilities.palace import (
>     multi_turn_probabilities, move_turn_probabilities,
>     cumulative_attack_prob, expected_attacks, multi_turn_mixed_hp,
> )
> ```


> ```python
> moves = ["Earthquake", "Rock Slide", "Swords Dance", "Protect"]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> moves = ['Earthquake', 'Rock Slide', 'Swords Dance', 'Protect']
> ```
>
> </details>


> ```python
> multi_turn_probabilities("Adamant", moves, 5)  # {0: p, 1: p, ..., 5: p}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   0: 0.05,
>   1: 0.20,
>   2: 0.33,
>   3: 0.28,
>   4: 0.12,
>   5: 0.02,
> }
> ```
>
> </details>


> ```python
> move_turn_probabilities("Adamant", moves, 5, "Earthquake")  # {0: p, 1: p, ..., 5: p}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   0: 0.27,
>   1: 0.40,
>   2: 0.24,
>   3: 0.07,
>   4: 0.01,
>   5: 0.0006,
> }
> ```
>
> </details>


> ```python
> cumulative_attack_prob("Adamant", moves, 5, 3)  # float
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 0.42
> ```
>
> </details>


> ```python
> expected_attacks("Adamant", moves, 5)  # float
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 2.29
> ```
>
> </details>


> ```python
> multi_turn_mixed_hp("Adamant", moves, 3, 2)  # {0: p, ..., 5: p}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   0: 0.01,
>   1: 0.09,
>   2: 0.27,
>   3: 0.36,
>   4: 0.22,
>   5: 0.05,
> }
> ```
>
> </details>


### Nature Rankings and Utilities


> ```python
> from frontierbrain3.facilities.palace import rank_natures, low_hp_message, DOUBLES_TARGETING
> ```


> ```python
> rank_natures(["Earthquake", "Rock Slide", "Protect"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   ('Sassy', 0.9),
>   ('Impish', 0.77),
>   ('Brave', 0.75),
>   ('Hardy', 0.71),
>   ('Timid', 0.71),
>   ('Docile', 0.63),
>   ('Naive', 0.63),
>   ('Quiet', 0.63),
>   ('Quirky', 0.63),
>   ('Hasty', 0.59),
>   ('Jolly', 0.54),
>   ('Lax', 0.53),
>   ('Serious', 0.52),
>   ('Rash', 0.49),
>   ('Adamant', 0.48),
>   ('Bold', 0.46),
>   ('Mild', 0.46),
>   ('Relaxed', 0.44),
>   ('Careful', 0.44),
>   ('Calm', 0.43),
>   ('Modest', 0.41),
>   ('Lonely', 0.38),
>   ('Bashful', 0.33),
>   ('Naughty', 0.23),
>   ('Gentle', 0.21),
> ]
> ```
>
> </details>


> ```python
> low_hp_message("Adamant", "Metagross")  # "A glint appears in Metagross's eyes!"
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> "A glint appears in Metagross's eyes!"
> ```
>
> </details>


> ```python
> DOUBLES_TARGETING["adamant"]  # "higher_hp"
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'higher_hp'
> ```
>
> </details>


> ```python
> DOUBLES_TARGETING["brave"]    # "lower_hp"
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'lower_hp'
> ```
>
> </details>


---

## Battle Pike (`facilities.pike`)

### Room Events

8 possible events per room, with some conditionally excluded:


> ```python
> from frontierbrain3.facilities.pike import get_event_probabilities, EVENTS
> ```


> ```python
> EVENTS  # {"single_battle": "A Trainer with 3 Pokemon...", ...}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'single_battle': 'A Trainer with 3 Pokemon walks up and battles.',
>   'double_battle': 'Two Trainers with 1 Pokemon each team up and battle.',
>   'hard_battle_heal': 'A tough Trainer battle; full party heal if you win.',
>   'wild_pokemon': 'Wild Pokemon appear as you cross a long corridor.',
>   'no_event': 'An NPC stands to the side and does nothing.',
>   'status': "A Gentleman's Pokemon inflicts a status condition.",
>   'partial_heal': 'A Gentleman fully heals one or two of your Pokemon.',
>   'full_heal': 'A receptionist fully heals all three of your Pokemon.',
> }
> ```
>
> </details>


> ```python
> get_event_probabilities()
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'single_battle': 0.17,
>   'double_battle': 0.17,
>   'hard_battle_heal': 0.17,
>   'wild_pokemon': 0.17,
>   'no_event': 0.17,
>   'status': 0.17,
>   'partial_heal': 0.00,
>   'full_heal': 0.00,
> }
> ```
>
> </details>


> ```python
> get_event_probabilities(all_full_hp=False)  # healing rooms now possible
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'single_battle': 0.12,
>   'double_battle': 0.12,
>   'hard_battle_heal': 0.12,
>   'wild_pokemon': 0.12,
>   'no_event': 0.12,
>   'status': 0.12,
>   'partial_heal': 0.12,
>   'full_heal': 0.12,
> }
> ```
>
> </details>


> ```python
> get_event_probabilities(num_fainted=2, all_full_hp=False)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'single_battle': 0.14,
>   'double_battle': 0.00,
>   'hard_battle_heal': 0.14,
>   'wild_pokemon': 0.14,
>   'no_event': 0.14,
>   'status': 0.14,
>   'partial_heal': 0.14,
>   'full_heal': 0.14,
> }
> ```
>
> </details>


### Status Room


> ```python
> from frontierbrain3.facilities.pike import get_status_chances, status_targets, STATUS_TABLE
> ```


> ```python
> status_targets(1)   # 1 (passes 1-5)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 1
> ```
>
> </details>


> ```python
> status_targets(6)   # 2 (passes 6-10)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 2
> ```
>
> </details>


> ```python
> status_targets(11)  # 3 (passes 11+)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 3
> ```
>
> </details>


> ```python
> get_status_chances(
>     pokemon_types=[["steel", "psychic"], ["normal"], ["dragon", "psychic"]],
>     pokemon_abilities=["clearbody", "intimidate", "levitate"],
>     pass_num=1,
> )
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'bad_poison': 0.23,
>   'freeze': 0.25,
>   'paralysis': 0.20,
>   'sleep': 0.10,
>   'burn': 0.10,
> }
> ```
>
> </details>


### Wild Pokemon


> ```python
> from frontierbrain3.facilities.pike import get_wild_pokemon
> ```


> ```python
> get_wild_pokemon(100, lv50=True)   # rooms 1-280: Seviper, Milotic, Dusclops
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'species': 'Seviper', 'ability': 'Shed Skin', 'level': 46, 'rate': 26, 'moves': ['Toxic', 'Glare', 'Sludge Bomb', 'Body Slam']},
>   {'species': 'Milotic', 'ability': 'Marvel Scale', 'level': 46, 'rate': 26, 'moves': ['Toxic', 'Hypnosis', 'Body Slam', 'Surf']},
>   {'species': 'Dusclops', 'ability': 'Pressure', 'level': 45, 'rate': 48, 'moves': ['Will-O-Wisp', 'Mean Look', 'Toxic', 'Shadow Punch']},
> ]
> ```
>
> </details>


> ```python
> get_wild_pokemon(300, lv50=True)   # rooms 281-560: Seviper, Milotic, Electrode
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'species': 'Seviper', 'ability': 'Shed Skin', 'level': 46, 'rate': 26, 'moves': ['Toxic', 'Glare', 'Sludge Bomb', 'Body Slam']},
>   {'species': 'Milotic', 'ability': 'Marvel Scale', 'level': 46, 'rate': 26, 'moves': ['Toxic', 'Hypnosis', 'Body Slam', 'Surf']},
>   {'species': 'Electrode', 'ability': 'Soundproof', 'level': 45, 'rate': 48, 'moves': ['Explosion', 'Selfdestruct', 'Thunder', 'Toxic']},
> ]
> ```
>
> </details>


> ```python
> get_wild_pokemon(900, lv50=False)  # rooms 841+: Seviper, Milotic, Wobbuffet
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'species': 'Seviper', 'ability': 'Shed Skin', 'level': [60, 96], 'rate': 26, 'moves': ['Toxic', 'Glare', 'Sludge Bomb', 'Poison Fang']},
>   {'species': 'Milotic', 'ability': 'Marvel Scale', 'level': [60, 96], 'rate': 26, 'moves': ['Toxic', 'Hypnosis', 'Body Slam', 'Ice Beam']},
>   {'species': 'Wobbuffet', 'ability': 'Shadow Tag', 'level': [60, 95], 'rate': 48, 'moves': ['Counter', 'Mirror Coat', 'Safeguard', 'Encore']},
> ]
> ```
>
> </details>


### Hints


> ```python
> from frontierbrain3.facilities.pike import HINTS
> ```


> ```python
> HINTS["nostalgia"]   # {"text": "...wave of nostalgia...", "events": ["status", "partial_heal"]}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'text': 'For some odd reason, I felt a wave of nostalgia coming from it...',
>   'events': ['status', 'partial_heal'],
> }
> ```
>
> </details>


> ```python
> HINTS["people"]      # {"text": "...presence of people...", "events": ["single_battle", "full_heal"]}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'text': 'Is it...A Trainer? I sense the presence of people...',
>   'events': ['single_battle', 'full_heal'],
> }
> ```
>
> </details>


> ```python
> HINTS["aroma"]       # {"text": "...aroma of Pokemon...", "events": ["wild_pokemon", "hard_battle_heal"]}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'text': 'It seems to have the distinct aroma of Pokemon wafting around it...',
>   'events': ['wild_pokemon', 'hard_battle_heal'],
> }
> ```
>
> </details>


> ```python
> HINTS["whispering"]  # {"text": "...heard something...", "events": ["no_event", "double_battle"]}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'text': 'I seem to have heard something... It may have been whispering...',
>   'events': ['no_event', 'double_battle'],
> }
> ```
>
> </details>


> ```python
> HINTS["dreadful"]    # {"text": "...dreadful presence...", "events": ["pike_queen"]}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'text': 'From every path I sense a dreadful presence...',
>   'events': ['pike_queen'],
> }
> ```
>
> </details>


---

## Battle Pyramid (`facilities.pyramid`)

### Round Themes and Wild Pokemon

20 rounds, each with a theme and 8 wild Pokemon:


> ```python
> from frontierbrain3.facilities.pyramid import (
>     ROUNDS, ROUND_THEMES, get_round_pokemon, get_encounters,
> )
> ```


> ```python
> ROUND_THEMES  # {1: "paralysis", 2: "poison", ..., 20: "normal"}
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   1: 'paralysis',
>   2: 'poison',
>   3: 'burn',
>   4: 'pp_drain',
>   5: 'levitate',
>   6: 'trapping',
>   7: 'ice',
>   8: 'selfdestruct',
>   9: 'psychic',
>   10: 'rock',
>   11: 'fighting',
>   12: 'weather',
>   13: 'bug',
>   14: 'dark',
>   15: 'water',
>   16: 'ghost',
>   17: 'steel',
>   18: 'dragon',
>   19: 'stone_evo',
>   20: 'normal',
> }
> ```
>
> </details>


> ```python
> get_round_pokemon(1)  # [{"species": "Plusle", "moves": [...], ...}, ...]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'species': 'Plusle', 'ability': None, 'lv50': [30, 40], 'open_offset': [-20, -10], 'moves': ['Thunder Wave', 'Spark', 'Encore']},
>   {'species': 'Minun', 'ability': None, 'lv50': [30, 40], 'open_offset': [-20, -10], 'moves': ['Thunder Wave', 'Thunderbolt', 'Quick Attack']},
>   {'species': 'Pikachu', 'ability': None, 'lv50': [32, 42], 'open_offset': [-18, -8], 'moves': ['Thunder Wave', 'Thunderbolt', 'Slam']},
>   {'species': 'Electabuzz', 'ability': None, 'lv50': [32, 42], 'open_offset': [-18, -8], 'moves': ['ThunderPunch', 'Swift', 'Screech']},
>   {'species': 'Vileplume', 'ability': None, 'lv50': [34, 44], 'open_offset': [-13, -3], 'moves': ['Stun Spore', 'Giga Drain', 'Protect']},
>   {'species': 'Manectric', 'ability': None, 'lv50': [34, 44], 'open_offset': [-13, -3], 'moves': ['Thunder Wave', 'Thunder', 'Quick Attack']},
>   {'species': 'Breloom', 'ability': None, 'lv50': [35, 45], 'open_offset': [-11, -1], 'moves': ['Stun Spore', 'Focus Punch', 'Giga Drain', 'Mach Punch']},
>   {'species': 'Jolteon', 'ability': None, 'lv50': [35, 45], 'open_offset': [-11, -1], 'moves': ['Thunder Wave', 'Thunder', 'Pin Missile', 'Quick Attack']},
> ]
> ```
>
> </details>


> ```python
> get_encounters(1, 3)  # [{"pokemon": {...}, "rate": 30}, {"pokemon": {...}, "rate": 50}, ...]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'pokemon': {'species': 'Pikachu', 'ability': None, 'lv50': [32, 42], 'open_offset': [-18, -8], 'moves': ['Thunder Wave', 'Thunderbolt', 'Slam']}, 'rate': 60},
>   {'pokemon': {'species': 'Electabuzz', 'ability': None, 'lv50': [32, 42], 'open_offset': [-18, -8], 'moves': ['ThunderPunch', 'Swift', 'Screech']}, 'rate': 20},
>   {'pokemon': {'species': 'Vileplume', 'ability': None, 'lv50': [34, 44], 'open_offset': [-13, -3], 'moves': ['Stun Spore', 'Giga Drain', 'Protect']}, 'rate': 15},
>   {'pokemon': {'species': 'Manectric', 'ability': None, 'lv50': [34, 44], 'open_offset': [-13, -3], 'moves': ['Thunder Wave', 'Thunder', 'Quick Attack']}, 'rate': 5},
> ]
> ```
>
> </details>


Encounter data includes species, ability, level ranges, and moves. Rounds cycle after 20 (round 21 = round 1, etc.).

### Floor Mechanics


> ```python
> from frontierbrain3.facilities.pyramid import FLOOR_TABLE, SLOT_RATES, get_floor_encounter_rate
> ```


> ```python
> FLOOR_TABLE[1]  # [1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 3, 4]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 3, 4]
> ```
>
> </details>


> ```python
> SLOT_RATES  # [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
> ```
>
> </details>


> ```python
> get_floor_encounter_rate(7)  # 8 (floor 7 has doubled rate)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 8
> ```
>
> </details>


### Items


> ```python
> from frontierbrain3.facilities.pyramid import get_items, get_pickup_items
> ```


> ```python
> get_items(1, 3)  # [{"item": "Hyper Potion", "rate": 31}, ...]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'item': 'Hyper Potion', 'rate': 15},
>   {'item': 'Fluffy Tail', 'rate': 15},
>   {'item': 'Cheri Berry', 'rate': 31},
>   {'item': 'Ether', 'rate': 10},
>   {'item': 'Lum Berry', 'rate': 10},
>   {'item': 'Revive', 'rate': 10},
>   {'item': 'Bright Powder', 'rate': 3},
>   {'item': 'Shell Bell', 'rate': 3},
>   {'item': 'Max Revive', 'rate': 3},
> ]
> ```
>
> </details>


> ```python
> get_pickup_items(1)  # [{"item": "Hyper Potion", "rate": 30}, ...]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'item': 'Hyper Potion', 'rate': 30},
>   {'item': 'Fluffy Tail', 'rate': 10},
>   {'item': 'Cheri Berry', 'rate': 10},
>   {'item': 'Ether', 'rate': 10},
>   {'item': 'Lum Berry', 'rate': 10},
>   {'item': 'Revive', 'rate': 10},
>   {'item': 'Bright Powder', 'rate': 5},
>   {'item': 'Shell Bell', 'rate': 5},
>   {'item': 'Max Revive', 'rate': 5},
>   {'item': 'Sacred Ash', 'rate': 5},
> ]
> ```
>
> </details>


---

## Demo Script

Run the interactive demo to explore all features with guided examples:

```bash
python demo.py
```

Select a category from the menu, then step through examples one at a time.