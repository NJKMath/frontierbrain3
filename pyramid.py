"""
pyramid.py -- Battle Pyramid wild Pokemon and encounter data.

Data sourced from Smogon's Emerald Battle Pyramid Wild Pokemon Guide.

Provides:
    ROUNDS          - dict of all 20 rounds of wild Pokemon data
    FLOOR_TABLE     - which Pokemon IDs (1-8) appear on each floor
    SLOT_RATES      - encounter rate per slot (12 slots per floor)
    FLOOR_RATES     - base encounter rate per floor
    get_encounters()  - Pokemon + rates for a given round and floor
    get_round_pokemon() - all 8 Pokemon for a given round
"""

# -- Floor encounter tables ----------------------------------------------------
# Each floor has 12 encounter slots mapping to Pokemon IDs 1-8 for that round.
# Slots correspond to SLOT_RATES below.

FLOOR_TABLE = {
    1: [1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 3, 4],
    2: [2, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 4],
    3: [3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 5, 6],
    4: [5, 5, 5, 5, 6, 6, 7, 7, 7, 8, 7, 8],
    5: [5, 5, 5, 5, 6, 6, 7, 7, 7, 8, 7, 8],
    6: [6, 6, 6, 5, 7, 7, 8, 8, 8, 8, 8, 8],
    7: [8, 8, 7, 7, 7, 6, 6, 6, 5, 5, 5, 5],
}

# Encounter rate per slot (12 slots, sums to 100%)
SLOT_RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]

# Base encounter rate per step on each floor
FLOOR_RATES = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 8}

ROUND_THEMES = {
    1: "paralysis", 2: "poison", 3: "burn", 4: "pp_drain",
    5: "levitate", 6: "trapping", 7: "ice", 8: "selfdestruct",
    9: "psychic", 10: "rock", 11: "fighting", 12: "weather",
    13: "bug", 14: "dark", 15: "water", 16: "ghost",
    17: "steel", 18: "dragon", 19: "stone_evo", 20: "normal",
}


# -- Round data ----------------------------------------------------------------
# Each round has 8 Pokemon entries. Fields:
#   species  - Pokemon name
#   ability  - specific ability if noted, else None
#   lv50     - [min_level, max_level] for Lv50 format
#   open_offset - [min_offset, max_offset] from player's highest level
#   moves    - list of moves

ROUNDS = {
    1: {
        "theme": "paralysis",
        "warning": "I see a shower of sparks...",
        "pokemon": [
            {"species": "Plusle",     "ability": None, "lv50": [30,40], "open_offset": [-20,-10], "moves": ["Thunder Wave","Spark","Encore"]},
            {"species": "Minun",      "ability": None, "lv50": [30,40], "open_offset": [-20,-10], "moves": ["Thunder Wave","Thunderbolt","Quick Attack"]},
            {"species": "Pikachu",    "ability": None, "lv50": [32,42], "open_offset": [-18,-8],  "moves": ["Thunder Wave","Thunderbolt","Slam"]},
            {"species": "Electabuzz", "ability": None, "lv50": [32,42], "open_offset": [-18,-8],  "moves": ["ThunderPunch","Swift","Screech"]},
            {"species": "Vileplume",  "ability": None, "lv50": [34,44], "open_offset": [-13,-3],  "moves": ["Stun Spore","Giga Drain","Protect"]},
            {"species": "Manectric",  "ability": None, "lv50": [34,44], "open_offset": [-13,-3],  "moves": ["Thunder Wave","Thunder","Quick Attack"]},
            {"species": "Breloom",    "ability": None, "lv50": [35,45], "open_offset": [-11,-1],  "moves": ["Stun Spore","Focus Punch","Giga Drain","Mach Punch"]},
            {"species": "Jolteon",    "ability": None, "lv50": [35,45], "open_offset": [-11,-1],  "moves": ["Thunder Wave","Thunder","Pin Missile","Quick Attack"]},
        ],
    },
    2: {
        "theme": "poison",
        "warning": "I see poison...",
        "pokemon": [
            {"species": "Gulpin",    "ability": None,       "lv50": [31,41], "open_offset": [-19,-9],  "moves": ["Toxic","Sludge","Protect"]},
            {"species": "Roselia",   "ability": None,       "lv50": [31,41], "open_offset": [-19,-9],  "moves": ["Toxic","Giga Drain","Magical Leaf","Petal Dance"]},
            {"species": "Butterfree","ability": None,       "lv50": [33,43], "open_offset": [-17,-7],  "moves": ["Poisonpowder","Gust","Psybeam"]},
            {"species": "Seviper",   "ability": None,       "lv50": [33,43], "open_offset": [-17,-7],  "moves": ["Poison Fang","Swagger","Crunch","Poison Tail"]},
            {"species": "Skarmory",  "ability": None,       "lv50": [35,45], "open_offset": [-12,-2],  "moves": ["Toxic","Fly","Steel Wing"]},
            {"species": "Ludicolo",  "ability": "Rain Dish","lv50": [35,45], "open_offset": [-12,-2],  "moves": ["Toxic","Protect","Dive","Rain Dance"]},
            {"species": "Crobat",    "ability": None,       "lv50": [36,46], "open_offset": [-10,0],   "moves": ["Toxic","Confuse Ray","Mean Look","Bite"]},
            {"species": "Gengar",    "ability": None,       "lv50": [36,46], "open_offset": [-10,0],   "moves": ["Toxic","Shadow Punch","Night Shade"]},
        ],
    },
    3: {
        "theme": "burn",
        "warning": "I see bright red flames...",
        "pokemon": [
            {"species": "Growlithe","ability": None,         "lv50": [32,42], "open_offset": [-18,-8],  "moves": ["Flame Wheel","Take Down"]},
            {"species": "Vulpix",   "ability": None,         "lv50": [32,42], "open_offset": [-18,-8],  "moves": ["Will-O-Wisp","Flamethrower"]},
            {"species": "Magcargo", "ability": "Flame Body", "lv50": [34,44], "open_offset": [-16,-6],  "moves": ["Flamethrower","Rock Slide","Protect"]},
            {"species": "Ninetales","ability": None,         "lv50": [34,44], "open_offset": [-16,-6],  "moves": ["Will-O-Wisp","Quick Attack","Flamethrower"]},
            {"species": "Medicham", "ability": None,         "lv50": [36,46], "open_offset": [-11,-1],  "moves": ["Fire Punch","Hi Jump Kick"]},
            {"species": "Weezing",  "ability": None,         "lv50": [36,46], "open_offset": [-11,-1],  "moves": ["Will-O-Wisp","Flamethrower","Protect"]},
            {"species": "Dusclops", "ability": None,         "lv50": [37,47], "open_offset": [-10,0],   "moves": ["Will-O-Wisp","Confuse Ray","Mean Look","Shadow Punch"]},
            {"species": "Houndoom", "ability": None,         "lv50": [37,47], "open_offset": [-10,0],   "moves": ["Flamethrower","Bite","SolarBeam","Overheat"]},
        ],
    },
    4: {
        "theme": "pp_drain",
        "warning": "I sense the tremendous pressure of unrequited anger...",
        "pokemon": [
            {"species": "Dunsparce", "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Spite","Toxic","Protect"]},
            {"species": "Banette",   "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Grudge","Will-O-Wisp","Night Shade"]},
            {"species": "Misdreavus","ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Grudge","Spite","Shadow Ball"]},
            {"species": "Ninetales", "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Grudge","Will-O-Wisp","Overheat"]},
            {"species": "Absol",     "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Bite","Aerial Ace","Shadow Ball","Protect"]},
            {"species": "Dusclops",  "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Will-O-Wisp","Protect","Toxic","Shadow Ball"]},
            {"species": "Shedinja",  "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Grudge","Toxic","Spite"]},
            {"species": "Gengar",    "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Grudge","Spite","Night Shade"]},
        ],
    },
    5: {
        "theme": "levitate",
        "warning": "I see Pokemon loftily airborne...",
        "pokemon": [
            {"species": "Haunter",   "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Night Shade","Thunderbolt","Sludge Bomb"]},
            {"species": "Chimecho",  "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Double-Edge","Toxic","Psychic","Protect"]},
            {"species": "Solrock",   "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Earthquake","Rock Slide","Fire Blast","Toxic"]},
            {"species": "Misdreavus","ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Psychic","Spite","Shadow Ball","Pain Split"]},
            {"species": "Claydol",   "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Earthquake","AncientPower","Selfdestruct","Psychic"]},
            {"species": "Weezing",   "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Sludge Bomb","Selfdestruct","Protect"]},
            {"species": "Flygon",    "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Earthquake","Crunch","Dragon Claw","Dragonbreath"]},
            {"species": "Gengar",    "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Thunderbolt","Psychic","Giga Drain","Night Shade"]},
        ],
    },
    6: {
        "theme": "trapping",
        "warning": "I sense terrific energy rising from the ground below...",
        "pokemon": [
            {"species": "Diglett",   "ability": None,         "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Rock Slide","Slash","Dig"]},
            {"species": "Trapinch",  "ability": None,         "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Rock Slide","Earthquake","Giga Drain"]},
            {"species": "Wynaut",    "ability": "Shadow Tag",  "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Destiny Bond","Splash","Counter","Mirror Coat"]},
            {"species": "Diglett",   "ability": None,         "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Earthquake","Rock Slide","Magnitude","Toxic"]},
            {"species": "Trapinch",  "ability": None,         "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Rock Slide","Earthquake","Giga Drain","Protect"]},
            {"species": "Wynaut",    "ability": "Shadow Tag",  "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Counter","Mirror Coat","Destiny Bond"]},
            {"species": "Wobbuffet", "ability": "Shadow Tag",  "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Counter","Mirror Coat","Destiny Bond"]},
            {"species": "Dugtrio",   "ability": "Arena Trap",  "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Rock Slide","Sludge Bomb","Earthquake","Protect"]},
        ],
    },
    7: {
        "theme": "ice",
        "warning": "I see ICE-type Pokemon...",
        "pokemon": [
            {"species": "Glalie",   "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Ice Beam","Crunch","Protect"]},
            {"species": "Sneasel",  "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Ice Beam","Crush Claw","Spite"]},
            {"species": "Dewgong",  "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Blizzard","Double-Edge","Surf"]},
            {"species": "Piloswine","ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Ice Beam","Earthquake","Toxic"]},
            {"species": "Jynx",     "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Blizzard","Lovely Kiss","Psychic"]},
            {"species": "Cloyster", "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Ice Beam","Surf","Protect"]},
            {"species": "Walrein",  "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Blizzard","Body Slam","Surf"]},
            {"species": "Lapras",   "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Sing","Body Slam","Ice Beam","Psychic"]},
        ],
    },
    8: {
        "theme": "selfdestruct",
        "warning": "I see a flurry of moves that imperil the user...",
        "pokemon": [
            {"species": "Weezing",   "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Selfdestruct","Sludge Bomb","Fire Blast"]},
            {"species": "Electrode",  "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Selfdestruct","Thunderbolt","Rollout"]},
            {"species": "Gengar",    "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Destiny Bond","Lick","Shadow Ball"]},
            {"species": "Golem",     "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Selfdestruct","Protect","Earthquake"]},
            {"species": "Pineco",    "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Explosion","Double-Edge","Giga Drain"]},
            {"species": "Solrock",   "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Explosion","Fire Spin","Psywave"]},
            {"species": "Forretress","ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Explosion","Toxic","Rock Slide"]},
            {"species": "Shiftry",   "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Explosion","Giga Drain","SolarBeam","Protect"]},
        ],
    },
    9: {
        "theme": "psychic",
        "warning": "I see PSYCHIC-type Pokemon...",
        "pokemon": [
            {"species": "Wobbuffet","ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Counter","Mirror Coat","Safeguard","Destiny Bond"]},
            {"species": "Metang",   "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Earthquake","Toxic","Sludge Bomb","Psychic"]},
            {"species": "Exeggutor","ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Egg Bomb","Psychic","Hypnosis"]},
            {"species": "Slowking", "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Shadow Ball","Surf","Ice Beam","Flamethrower"]},
            {"species": "Xatu",     "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Confuse Ray","Shadow Ball","Psychic","Steel Wing"]},
            {"species": "Alakazam", "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Psychic","Fire Punch","Ice Punch","Toxic"]},
            {"species": "Starmie",  "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Psychic","Thunderbolt","Surf","Ice Beam"]},
            {"species": "Espeon",   "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Psychic","Dig","Shadow Ball"]},
        ],
    },
    10: {
        "theme": "rock",
        "warning": "I see ROCK-type Pokemon...",
        "pokemon": [
            {"species": "Golem",     "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Selfdestruct","Earthquake","Protect"]},
            {"species": "Steelix",   "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Iron Tail","Crunch","Earthquake"]},
            {"species": "Omastar",   "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Surf","Mud Shot","AncientPower"]},
            {"species": "Lunatone",  "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Hypnosis","Psywave","Explosion"]},
            {"species": "Shuckle",   "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Toxic","Protect","Wrap"]},
            {"species": "Armaldo",   "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["AncientPower","Protect","Aerial Ace"]},
            {"species": "Cradily",   "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Sludge Bomb","Giga Drain","Confuse Ray"]},
            {"species": "Aerodactyl","ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Hyper Beam","Rock Slide","Bite"]},
        ],
    },
    11: {
        "theme": "fighting",
        "warning": "I see FIGHTING-type Pokemon...",
        "pokemon": [
            {"species": "Poliwrath","ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Submission","Focus Punch","Surf"]},
            {"species": "Hariyama", "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Fake Out","Surf","Focus Punch"]},
            {"species": "Breloom",  "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Spore","Focus Punch","Protect"]},
            {"species": "Medicham", "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["ThunderPunch","Fire Punch","Ice Punch","Focus Punch"]},
            {"species": "Hitmonchan","ability": None,"lv50": [39,49], "open_offset": [-11,-1],  "moves": ["ThunderPunch","Fire Punch","Ice Punch","Focus Punch"]},
            {"species": "Hitmonlee","ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Mega Kick","Focus Punch"]},
            {"species": "Heracross","ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Megahorn","Earthquake","Focus Punch","Rock Slide"]},
            {"species": "Machamp",  "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Rock Slide","Earthquake","Focus Punch","Seismic Toss"]},
        ],
    },
    12: {
        "theme": "weather",
        "warning": "RAIN DANCE... SUNNY DAY... SANDSTORM... HAIL...",
        "pokemon": [
            {"species": "Quagsire","ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Rain Dance","Surf","Protect"]},
            {"species": "Tropius", "ability": None, "lv50": [36,46], "open_offset": [-15,-5],  "moves": ["Sunny Day","SolarBeam"]},
            {"species": "Pupitar", "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Sandstorm","Earthquake","Rock Slide"]},
            {"species": "Lapras",  "ability": None, "lv50": [37,47], "open_offset": [-13,-3],  "moves": ["Hail","Ice Beam"]},
            {"species": "Cacturne","ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Sandstorm","Giga Drain","SolarBeam"]},
            {"species": "Flareon", "ability": None, "lv50": [39,49], "open_offset": [-11,-1],  "moves": ["Sunny Day","Flamethrower","Protect"]},
            {"species": "Walrein", "ability": None, "lv50": [40,50], "open_offset": [-10,0],   "moves": ["Hail","Ice Beam"]},
            {"species": "Gyarados","ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Rain Dance","Thunder","Hydro Pump"]},
        ],
    },
    13: {
        "theme": "bug",
        "warning": "I see BUG-type Pokemon...",
        "pokemon": [
            {"species": "Pineco",     "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Explosion","Take Down"]},
            {"species": "Shuckle",    "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Toxic","Earthquake","Protect"]},
            {"species": "Venomoth",   "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Silver Wind","Poisonpowder","Sleep Powder","Psychic"]},
            {"species": "Scizor",     "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Quick Attack","Metal Claw","Fury Cutter","Pursuit"]},
            {"species": "Heracross",  "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Megahorn","Brick Break","Earthquake","Rock Slide"]},
            {"species": "Forretress", "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Explosion","Earthquake","Protect"]},
            {"species": "Armaldo",    "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Water Pulse","Protect","Rock Slide"]},
            {"species": "Shedinja",   "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Shadow Ball","Toxic","Spite","Grudge"]},
        ],
    },
    14: {
        "theme": "dark",
        "warning": "I see DARK-type Pokemon...",
        "pokemon": [
            {"species": "Sableye",  "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Night Shade","Psychic","Aerial Ace"]},
            {"species": "Sneasel",  "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Ice Beam","Taunt","Faint Attack","Quick Attack"]},
            {"species": "Crawdaunt","ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Crabhammer","Ice Beam","Surf"]},
            {"species": "Shiftry",  "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Explosion","Shadow Ball","Aerial Ace","Giga Drain"]},
            {"species": "Cacturne", "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Toxic","Giga Drain","Needle Arm"]},
            {"species": "Absol",    "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Bite","Protect","Slash"]},
            {"species": "Houndoom", "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Overheat","Crunch","Shadow Ball","Protect"]},
            {"species": "Umbreon",  "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Psychic","Shadow Ball","Iron Tail","Quick Attack"]},
        ],
    },
    15: {
        "theme": "water",
        "warning": "I see WATER-type Pokemon...",
        "pokemon": [
            {"species": "Octillery","ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Octazooka","Ice Beam","Fire Blast"]},
            {"species": "Dewgong",  "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Water Pulse","Ice Beam","Headbutt"]},
            {"species": "Pelipper", "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Protect","Supersonic","Surf"]},
            {"species": "Quagsire", "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Earthquake","Rock Tomb","Surf"]},
            {"species": "Ludicolo", "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Protect","SolarBeam","Toxic","Ice Beam"]},
            {"species": "Slowking", "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Psychic","Headbutt","Swagger"]},
            {"species": "Starmie",  "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Water Pulse","Thunderbolt","Confuse Ray","Blizzard"]},
            {"species": "Blastoise","ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Hydro Pump","Bite","Ice Beam"]},
        ],
    },
    16: {
        "theme": "ghost",
        "warning": "I see GHOST-type Pokemon...",
        "pokemon": [
            {"species": "Duskull",   "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Night Shade","Will-O-Wisp","Shadow Ball","Protect"]},
            {"species": "Haunter",   "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Toxic","Spite","Hypnosis","Shadow Ball"]},
            {"species": "Banette",   "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Shadow Ball","Spite","Will-O-Wisp"]},
            {"species": "Misdreavus","ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Perish Song","Spite","Mean Look"]},
            {"species": "Sableye",   "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Shadow Ball","Mean Look","Dig","Night Shade"]},
            {"species": "Dusclops",  "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Will-O-Wisp","Toxic","Shadow Ball"]},
            {"species": "Shedinja",  "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Shadow Ball","Spite","Grudge","Protect"]},
            {"species": "Gengar",    "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Psychic","Destiny Bond","Spite","Night Shade"]},
        ],
    },
    17: {
        "theme": "steel",
        "warning": "I see STEEL-type Pokemon...",
        "pokemon": [
            {"species": "Mawile",    "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Crunch","Toxic","Ice Beam"]},
            {"species": "Magneton",  "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Thunderbolt","Thunder Wave"]},
            {"species": "Steelix",   "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Rock Throw","Double-Edge","Earthquake"]},
            {"species": "Scizor",    "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Metal Claw","Slash"]},
            {"species": "Forretress","ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Explosion","Toxic"]},
            {"species": "Skarmory",  "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Steel Wing","Toxic","Fly","Protect"]},
            {"species": "Aggron",    "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Earthquake","Take Down","Surf","Ice Beam"]},
            {"species": "Metagross", "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Earthquake","Psychic","Shadow Ball","Brick Break"]},
        ],
    },
    18: {
        "theme": "dragon",
        "warning": "I see flying Pokemon...",
        "pokemon": [
            {"species": "Dragonair",  "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Thunder Wave","Toxic","Ice Beam"]},
            {"species": "Vibrava",    "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Earthquake","Dragonbreath","Crunch","Steel Wing"]},
            {"species": "Altaria",    "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Earthquake","Dragon Claw","Sing","Protect"]},
            {"species": "Flygon",     "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Earthquake","Dragon Claw","Fire Blast"]},
            {"species": "Aerodactyl", "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Earthquake","Rock Slide","Dragon Claw"]},
            {"species": "Gyarados",   "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Earthquake","Surf","Thrash","Bite"]},
            {"species": "Kingdra",    "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Hydro Pump","Ice Beam","Protect"]},
            {"species": "Charizard",  "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Flamethrower","Focus Punch","Fire Blast","Iron Tail"]},
        ],
    },
    19: {
        "theme": "stone_evo",
        "warning": "I see those that have evolved from the power of stones...",
        "pokemon": [
            {"species": "Arcanine", "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Fire Blast","Take Down"]},
            {"species": "Poliwrath","ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Hydro Pump","Ice Beam"]},
            {"species": "Raichu",   "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Thunder","Thunder Wave","Slam"]},
            {"species": "Vaporeon", "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Surf","Ice Beam"]},
            {"species": "Jolteon",  "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Thunderbolt","Pin Missile"]},
            {"species": "Flareon",  "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Flamethrower","Bite"]},
            {"species": "Ninetales","ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Flamethrower","Will-O-Wisp","Protect"]},
            {"species": "Starmie",  "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Ice Beam","Surf","Thunderbolt","Psychic"]},
        ],
    },
    20: {
        "theme": "normal",
        "warning": "I see NORMAL-type Pokemon...",
        "pokemon": [
            {"species": "Kangaskhan","ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Hyper Beam","Flamethrower","Surf","Dizzy Punch"]},
            {"species": "Swellow",   "ability": None, "lv50": [37,47], "open_offset": [-15,-5],  "moves": ["Aerial Ace","Hyper Beam","Toxic"]},
            {"species": "Ursaring",  "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Hyper Beam","Earthquake","Focus Punch","Protect"]},
            {"species": "Porygon2",  "ability": None, "lv50": [41,51], "open_offset": [-13,-3],  "moves": ["Psybeam","Hyper Beam","Shadow Ball","Ice Beam"]},
            {"species": "Tauros",    "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Earthquake","Hyper Beam","Surf","Thunderbolt"]},
            {"species": "Fearow",    "ability": None, "lv50": [43,53], "open_offset": [-11,-1],  "moves": ["Hyper Beam","Fly","Mirror Move","Protect"]},
            {"species": "Snorlax",   "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Hyper Beam","Body Slam","Shadow Ball","Earthquake"]},
            {"species": "Slaking",   "ability": None, "lv50": [45,55], "open_offset": [-10,0],   "moves": ["Hyper Beam","Earthquake","Shadow Ball","Ice Beam"]},
        ],
    },
}


# -- Item data -----------------------------------------------------------------
# Probability of each item slot (1-10) appearing, by floor.
# Each list is 10 values summing to 100.

ITEM_FLOOR_RATES = {
    1: [31, 15, 15, 10, 10, 10, 3, 3, 3, 0],
    2: [15, 31, 15, 10, 10, 10, 3, 0, 3, 3],
    3: [15, 15, 31, 10, 10, 10, 3, 3, 3, 0],
    4: [28, 15, 15, 10, 10, 10, 0, 4, 4, 4],
    5: [15, 28, 15, 10, 10, 10, 4, 4, 0, 4],
    6: [15, 15, 28, 10, 10, 10, 4, 4, 4, 0],
    7: [28, 15, 15, 10, 10, 10, 4, 0, 4, 4],
}

ITEM_PICKUP_RATES = [30, 10, 10, 10, 10, 10, 5, 5, 5, 5]

# Item pool per round (1-20, cycles after 20). Each list has 10 items
# corresponding to item slots 1-10.
ITEM_POOLS = {
    1:  ["Hyper Potion","Fluffy Tail", "Cheri Berry", "Ether","Lum Berry",  "Revive","Bright Powder","Shell Bell",  "Max Revive",   "Sacred Ash"],
    2:  ["Hyper Potion","Dire Hit",    "Pecha Berry", "Ether","Leppa Berry", "Revive","Leftovers",    "Choice Band", "Full Restore", "Max Elixir"],
    3:  ["Hyper Potion","X Attack",    "Rawst Berry", "Ether","Lum Berry",  "Revive","Scope Lens",   "Focus Band",  "Max Revive",   "Sacred Ash"],
    4:  ["Hyper Potion","X Defense",   "Lum Berry",   "Ether","Leppa Berry", "Revive","Quick Claw",   "King's Rock", "Full Restore", "Max Elixir"],
    5:  ["Hyper Potion","X Speed",     "Chesto Berry","Ether","Lum Berry",  "Revive","Bright Powder","Shell Bell",  "Max Revive",   "Sacred Ash"],
    6:  ["Hyper Potion","X Accuracy",  "Lum Berry",   "Ether","Leppa Berry", "Revive","Leftovers",    "Choice Band", "Full Restore", "Max Elixir"],
    7:  ["Hyper Potion","X Sp. Atk",   "Lum Berry",   "Ether","Lum Berry",  "Revive","Scope Lens",   "Focus Band",  "Max Revive",   "Sacred Ash"],
    8:  ["Hyper Potion","Guard Spec.",  "Lum Berry",   "Ether","Leppa Berry", "Revive","Quick Claw",   "King's Rock", "Full Restore", "Max Elixir"],
    9:  ["Hyper Potion","Fluffy Tail", "Lum Berry",   "Ether","Lum Berry",  "Revive","Bright Powder","Shell Bell",  "Max Revive",   "Sacred Ash"],
    10: ["Hyper Potion","Dire Hit",    "Lum Berry",   "Ether","Leppa Berry", "Revive","Leftovers",    "Choice Band", "Full Restore", "Max Elixir"],
    11: ["Hyper Potion","X Attack",    "Lum Berry",   "Ether","Lum Berry",  "Revive","Scope Lens",   "Focus Band",  "Max Revive",   "Sacred Ash"],
    12: ["Hyper Potion","X Defense",   "Lum Berry",   "Ether","Leppa Berry", "Revive","Quick Claw",   "King's Rock", "Full Restore", "Max Elixir"],
    13: ["Hyper Potion","X Speed",     "Lum Berry",   "Ether","Lum Berry",  "Revive","Bright Powder","Shell Bell",  "Max Revive",   "Sacred Ash"],
    14: ["Hyper Potion","X Accuracy",  "Lum Berry",   "Ether","Leppa Berry", "Revive","Leftovers",    "Choice Band", "Full Restore", "Max Elixir"],
    15: ["Hyper Potion","X Sp. Atk",   "Lum Berry",   "Ether","Lum Berry",  "Revive","Scope Lens",   "Focus Band",  "Max Revive",   "Sacred Ash"],
    16: ["Hyper Potion","Guard Spec.",  "Lum Berry",   "Ether","Leppa Berry", "Revive","Quick Claw",   "King's Rock", "Full Restore", "Max Elixir"],
    17: ["Hyper Potion","Fluffy Tail", "Lum Berry",   "Ether","Lum Berry",  "Revive","Bright Powder","Shell Bell",  "Max Revive",   "Sacred Ash"],
    18: ["Hyper Potion","Dire Hit",    "Lum Berry",   "Ether","Leppa Berry", "Revive","Leftovers",    "Choice Band", "Full Restore", "Max Elixir"],
    19: ["Hyper Potion","X Attack",    "Lum Berry",   "Ether","Lum Berry",  "Revive","Scope Lens",   "Focus Band",  "Max Revive",   "Sacred Ash"],
    20: ["Hyper Potion","X Defense",   "Lum Berry",   "Ether","Leppa Berry", "Revive","Quick Claw",   "King's Rock", "Full Restore", "Max Elixir"],
}


# -- Helper functions ----------------------------------------------------------

def get_round_pokemon(round_num: int) -> list[dict]:
    """Return the list of 8 Pokemon entries for a given round (1-20)."""
    rnd = round_num
    # Rounds cycle: 21 -> 1, 22 -> 2, etc.
    if rnd > 20:
        rnd = ((rnd - 1) % 20) + 1
    if rnd not in ROUNDS:
        raise ValueError(f"Round must be 1-20 (or higher to cycle), got {round_num}")
    return ROUNDS[rnd]["pokemon"]


def get_encounters(round_num: int, floor: int) -> list[dict]:
    """
    Return a list of {pokemon, rate} dicts for a given round and floor.

    Each entry has:
        pokemon - the Pokemon data dict from ROUNDS
        rate    - encounter probability (0-100, sums to 100)

    Floor must be 1-7.
    """
    if floor not in FLOOR_TABLE:
        raise ValueError(f"Floor must be 1-7, got {floor}")

    pokemon_list = get_round_pokemon(round_num)
    slots = FLOOR_TABLE[floor]

    # Aggregate rates by Pokemon ID (1-indexed)
    rate_by_id: dict[int, int] = {}
    for slot_idx, poke_id in enumerate(slots):
        rate_by_id[poke_id] = rate_by_id.get(poke_id, 0) + SLOT_RATES[slot_idx]

    result = []
    for poke_id, rate in sorted(rate_by_id.items()):
        result.append({
            "pokemon": pokemon_list[poke_id - 1],  # 0-indexed
            "rate": rate,
        })
    return result


def get_floor_encounter_rate(floor: int) -> int:
    """Return the base encounter rate (percent per step) for a floor."""
    if floor not in FLOOR_RATES:
        raise ValueError(f"Floor must be 1-7, got {floor}")
    return FLOOR_RATES[floor]


def get_items(round_num: int, floor: int) -> list[dict]:
    """
    Return a list of {item, rate} dicts for a given round and floor.

    Each entry has:
        item - item name string
        rate - probability (0-100)

    Items with 0% rate on that floor are excluded.
    """
    if floor not in ITEM_FLOOR_RATES:
        raise ValueError(f"Floor must be 1-7, got {floor}")

    rnd = round_num
    if rnd > 20:
        rnd = ((rnd - 1) % 20) + 1
    if rnd not in ITEM_POOLS:
        raise ValueError(f"Round must be 1-20 (or higher to cycle), got {round_num}")

    items = ITEM_POOLS[rnd]
    rates = ITEM_FLOOR_RATES[floor]

    return [
        {"item": items[i], "rate": rates[i]}
        for i in range(10)
        if rates[i] > 0
    ]


def get_pickup_items(round_num: int) -> list[dict]:
    """
    Return a list of {item, rate} dicts for Pickup on a given round.
    Pickup rates are the same regardless of floor.
    """
    rnd = round_num
    if rnd > 20:
        rnd = ((rnd - 1) % 20) + 1
    if rnd not in ITEM_POOLS:
        raise ValueError(f"Round must be 1-20 (or higher to cycle), got {round_num}")

    items = ITEM_POOLS[rnd]
    return [
        {"item": items[i], "rate": ITEM_PICKUP_RATES[i]}
        for i in range(10)
        if ITEM_PICKUP_RATES[i] > 0
    ]