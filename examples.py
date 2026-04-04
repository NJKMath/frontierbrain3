from frontierbrain3 import (
    Database, CustomSet, calc_stats, from_paste, from_clipboard,
    damage_rolls, ko_chance, calc_matchup, format_result, Field,
)
from frontierbrain3.facilities.tower import TowerDatabase
from frontierbrain3.facilities.factory import FactoryDatabase
from frontierbrain3.facilities.dome import calc_seed

db = Database()
tower = TowerDatabase()

def show(label, result):
    out = result.ids() if hasattr(result, "ids") else result.names()
    print(f"{label}:\n  {', '.join(out) if out else '(none)'}\n")


# Set filters
show("Water-types with Surf",          db.sets.hasType("Water").hasMove("surf"))
show("Pure Psychic-types",             db.sets.hasType("Psychic/"))
show("Pure OR part Water",             db.sets.hasType("Water"))
show("Fire/Flying sets",               db.sets.hasType("Fire/Flying"))
show("Adamant + Choice Band",          db.sets.hasNature("Adamant").hasItem("Choice Band"))
show("EQ users without Surf",          db.sets.hasMove("earthquake").Not.hasMove("surf"))
show("Calm Mind users with Surf or Thunder", db.sets.hasMove("calmmind").hasMove("surf", "thunder", match="any"))

# allSets
show("All Charizard sets", db.allSets("Charizard"))

# usedByTrainer / trainer filters
show("Trainers using a Water-type Surfer", db.sets.hasType("Water").hasMove("surf").usedByTrainer())
show("Trainers with Charizard but not Blastoise", db.trainers.hasPokemon("Charizard").Not.hasPokemon("Blastoise"))

# Stat calculations
print("\nStat calculations:")
alakazam = db.allSets("Alakazam")._sets[0]
print(f"  Alakazam set 1, 31 IVs lv100: {calc_stats(alakazam, db._species_map)}")
print(f"  Alakazam set 1, 15 IVs lv100: {calc_stats(alakazam, db._species_map, ivs=15)}")
snorlax = db.allSets("Snorlax")._sets[0]
print(f"  Snorlax set 1,  31 IVs lv50:  {calc_stats(snorlax,  db._species_map, level=50)}")

# Stat filtering
show("Sets with 300+ Atk (31 IVs, lv100)",        db.sets.statFilter("atk", min=300))
show("Sets with 150+ SpA at lv50, 15 IVs",         db.sets.statFilter("spa", min=150, level=50, ivs=15))

# Custom set speed comparisons
my_set = CustomSet("Flygon", nature="jolly", evs=[0, 0, 0, 0, 0, 252])
print(f"\nCustom set: {my_set}, speed = {my_set.speed()}")
show("Sets that outspeed it (31 IVs)",          db.sets.fasterThan(my_set))
show("Sets it outspeeds (31 IVs)",              db.sets.slowerThan(my_set))
show("Speed ties (31 IVs)",                     db.sets.speedTieWith(my_set))
show("Sets that outspeed it (enemy at 15 IVs)", db.sets.fasterThan(my_set, ivs=15))

# Pokepaste import
paste = """
BLEACH (Skarmory) (M) @ Chesto Berry
Ability: Sturdy
Level: 50
EVs: 252 HP / 140 Def / 116 SpD
Bold Nature
IVs: 0 Atk
- Protect
- Rest
- Whirlwind
- Torment

NO HALO (Latios) @ Lum Berry
Ability: Levitate
Level: 50
EVs: 172 HP / 108 Def / 4 SpA / 4 SpD / 220 Spe
Timid Nature
IVs: 0 Atk
- Substitute
- Calm Mind
- Recover
- Dragon Claw
"""
team = from_paste(paste)
print("\nPokepaste import:")
for name, cs in team.items():
    print(f"  {name}: {cs.pokemon}, speed={cs.speed()}, ability={cs.ability}, moves={cs.moves}")

# To import from clipboard instead:
# team = from_clipboard()

# Factory random teams (unconstrained)
fac = FactoryDatabase()
print("\nFactory random teams (unconstrained):")
for label, (level, rnd) in [("Open Lv Round 5+", ("open", 5)), ("Lv50 Round 1", ("lv50", 1))]:
    ids, typ, phrase = fac.random_team(level, rnd)
    print(f"  {label}: {', '.join(ids)} | {typ} | {phrase}")

# Factory random teams (Type/Phrase constrained)
print("\nFactory random teams (constrained):")
ids, typ, phrase = fac.random_team("open", 5, target_type="Water")
print(f"  Water / any phrase:    {', '.join(ids)} | {typ} | {phrase}")

ids, typ, phrase = fac.random_team("open", 5, target_phrase=4)
print(f"  Any type / phrase 4:   {', '.join(ids)} | {typ} | {phrase}")

ids, typ, phrase = fac.random_team("open", 5, target_type="Fire", target_phrase=1)
print(f"  Fire / phrase 1:       {', '.join(ids)} | {typ} | {phrase}")

ids, typ, phrase = fac.random_team("open", 5, target_type="None", target_phrase=8)
print(f"  No Type / Flex:        {', '.join(ids)} | {typ} | {phrase}")

# Random team generation
print("\nRandom round 8 teams:")
print(" ", tower.random_team(8))
print(" ", tower.random_team(8))
print(" ", tower.random_team(8, trainer_class="Dragon Tamer"))
print(" ", tower.random_team(name="Brady"))
print(" ", tower.random_team(8, trainer_class="Nobody Real"))  # invalid — shows error


# ══════════════════════════════════════════════════════════════════════════════
# Damage calculator examples
# ══════════════════════════════════════════════════════════════════════════════

# Move dicts — pass inline so examples work without Data/moves.json
EARTHQUAKE  = {"name": "Earthquake",   "type": "ground",   "power": 100}
METEOR_MASH = {"name": "Meteor Mash",  "type": "steel",    "power": 100}
SURF        = {"name": "Surf",         "type": "water",    "power": 95}
ICE_BEAM    = {"name": "Ice Beam",     "type": "ice",      "power": 95}
THUNDERBOLT = {"name": "Thunderbolt",  "type": "electric",  "power": 95}
ROCK_SLIDE  = {"name": "Rock Slide",   "type": "rock",     "power": 75}
SHADOW_BALL = {"name": "Shadow Ball",  "type": "ghost",    "power": 80}
MEGAHORN    = {"name": "Megahorn",     "type": "bug",      "power": 120}
SLUDGE_BOMB = {"name": "Sludge Bomb",  "type": "poison",   "power": 90}
FIRE_BLAST  = {"name": "Fire Blast",   "type": "fire",     "power": 120}
BODY_SLAM   = {"name": "Body Slam",    "type": "normal",   "power": 85}
PSYCHIC     = {"name": "Psychic",      "type": "psychic",  "power": 90}
HIDDEN_PWR_GRASS = {"name": "HP Grass", "type": "grass",   "power": 70}
DRAGON_RAGE = {"name": "Dragon Rage",  "type": "dragon",   "power": 0}
SEISMIC_TOSS= {"name": "Seismic Toss", "type": "fighting", "power": 0}
NIGHT_SHADE = {"name": "Night Shade",  "type": "ghost",    "power": 0}
SUPER_FANG  = {"name": "Super Fang",   "type": "normal",   "power": 0}
ENDEAVOR    = {"name": "Endeavor",     "type": "normal",   "power": 0}
ERUPTION    = {"name": "Eruption",     "type": "fire",     "power": 0}
WATER_SPOUT = {"name": "Water Spout",  "type": "water",    "power": 0}
SONIC_BOOM  = {"name": "SonicBoom",    "type": "normal",   "power": 0}
FLAIL       = {"name": "Flail",        "type": "normal",   "power": 0}
REVERSAL    = {"name": "Reversal",     "type": "fighting", "power": 0}
LOW_KICK    = {"name": "Low Kick",     "type": "fighting", "power": 0}
PSYWAVE     = {"name": "Psywave",      "type": "psychic",  "power": 0}

smap = db._species_map
print("\n" + "=" * 72)
print("DAMAGE CALCULATOR EXAMPLES")
print("=" * 72)

# ── Example 1: Frontier set vs frontier set — Metagross vs Tyranitar ──────
meta_sets = db.allSets("Metagross")._sets
ttar_sets = db.allSets("Tyranitar")._sets

print(f"\n--- Frontier set vs frontier set (31 IVs, lv100) ---")
if meta_sets and ttar_sets:
    meta = meta_sets[0]
    ttar = ttar_sets[0]
    print(f"Metagross-1 ({meta['Nature']}, {meta['Item']}) vs Tyranitar-1:")
    res = calc_matchup(meta, ttar, EARTHQUAKE, smap)
    print(format_result(res, "Earthquake"))
    res = calc_matchup(meta, ttar, METEOR_MASH, smap)
    print(format_result(res, "Meteor Mash"))

# ── Example 2: CustomSet vs frontier set — Starmie vs Snorlax ────────────
print(f"\n--- CustomSet vs frontier set ---")
starmie = CustomSet(
    "Starmie", nature="Timid",
    evs=[0, 0, 0, 252, 4, 252],
    item="None", ability="Natural Cure",
    moves=["Surf", "Thunderbolt", "Ice Beam", "Recover"],
)
lax_sets = db.allSets("Snorlax")._sets
if lax_sets:
    lax = lax_sets[0]
    print(f"Timid 252 SpA Starmie vs Snorlax-1 ({lax['Nature']}):")
    res = calc_matchup(starmie, lax, SURF, smap)
    print(format_result(res, "Surf"))
    res = calc_matchup(starmie, lax, THUNDERBOLT, smap)
    print(format_result(res, "Thunderbolt"))

# ── Example 3: SE matchup — Starmie vs Tyranitar (4× Water weakness) ─────
print(f"\n--- Super effective: Starmie vs Tyranitar ---")
if ttar_sets:
    ttar = ttar_sets[0]
    print(f"Timid 252 SpA Starmie vs Tyranitar-1:")
    res = calc_matchup(starmie, ttar, SURF, smap)
    print(format_result(res, "Surf (4x SE)"))

# ── Example 4: Weather — Rain-boosted Surf ────────────────────────────────
print(f"\n--- Weather modifier (Rain) ---")
rain = Field(weather="rain")
if ttar_sets:
    print(f"Timid 252 SpA Starmie vs Tyranitar-1 in rain:")
    res = calc_matchup(starmie, ttar, SURF, smap, field=rain)
    print(format_result(res, "Surf (Rain, 4x SE)"))

# ── Example 5: Choice Band physical attacker — Heracross vs Alakazam ─────
print(f"\n--- Choice Band attacker ---")
hera = CustomSet(
    "Heracross", nature="Adamant",
    evs=[4, 252, 0, 0, 0, 252],
    item="Choice Band", ability="Guts",
    moves=["Megahorn", "Rock Slide", "Earthquake", "Sleep Talk"],
)
zam_sets = db.allSets("Alakazam")._sets
if zam_sets:
    zam = zam_sets[0]
    print(f"Adamant CB Heracross vs Alakazam-1:")
    res = calc_matchup(hera, zam, MEGAHORN, smap)
    print(format_result(res, "Megahorn"))
    res = calc_matchup(hera, zam, EARTHQUAKE, smap)
    print(format_result(res, "Earthquake"))

# ── Example 6: Frontier sets at lv50, 15 IVs — Metagross vs Swampert ─────
print(f"\n--- Frontier set at lv50, 15 IVs ---")
swam_sets = db.allSets("Swampert")._sets
if meta_sets and swam_sets:
    meta = meta_sets[0]
    swam = swam_sets[0]
    print(f"Metagross-1 (15 IVs, lv50) vs Swampert-1 (15 IVs, lv50):")
    res = calc_matchup(meta, swam, METEOR_MASH, smap,
                       atk_ivs=15, def_ivs=15, atk_level=50, def_level=50)
    print(format_result(res, "Meteor Mash"))

# ── Example 7: Reflect — Metagross vs Steelix behind Reflect ─────────────
print(f"\n--- Reflect (physical screen) ---")
reflect_up = Field(reflect=True)
steelix_sets = db.allSets("Steelix")._sets
if meta_sets and steelix_sets:
    steelix = steelix_sets[0]
    print(f"Metagross-1 Earthquake vs Steelix-1, then with Reflect:")
    res_no = calc_matchup(meta, steelix, EARTHQUAKE, smap)
    print(format_result(res_no, "EQ (no Reflect)"))
    res_yes = calc_matchup(meta, steelix, EARTHQUAKE, smap, field=reflect_up)
    print(format_result(res_yes, "EQ (Reflect)"))

# ── Example 8: Critical hit — Alakazam Psychic vs Heracross ───────────────
print(f"\n--- Critical hit ---")
if zam_sets:
    zam = zam_sets[0]
    print(f"Alakazam-1 Psychic vs CB Heracross (normal vs crit):")
    res = calc_matchup(zam, hera, PSYCHIC, smap)
    print(format_result(res, "Psychic"))
    res = calc_matchup(zam, hera, PSYCHIC, smap, critical=True)
    print(format_result(res, "Psychic (crit)"))

# ── Example 9: KO calc with Leftovers — Metagross vs Snorlax ─────────────
print(f"\n--- KO chance with Leftovers recovery ---")
snorlax_custom = CustomSet(
    "Snorlax", nature="Careful",
    evs=[252, 0, 252, 0, 4, 0],
    item="Leftovers", ability="Thick Fat",
    moves=["Body Slam", "Rest", "Sleep Talk", "Earthquake"],
)
snorlax_hp = snorlax_custom.get_stats()["hp"]
leftovers_recovery = snorlax_hp // 16
if meta_sets:
    meta = meta_sets[0]
    print(f"Metagross-1 Meteor Mash vs Careful 252HP/252Def Snorlax (Leftovers):")
    res = calc_matchup(meta, snorlax_custom, METEOR_MASH, smap,
                       recovery=leftovers_recovery)
    print(format_result(res, "Meteor Mash"))

# ── Example 10: Immunity check — Earthquake vs Levitate ───────────────────
print(f"\n--- Ability immunity: Earthquake vs Levitate ---")
gengar_sets = db.allSets("Gengar")._sets
if meta_sets and gengar_sets:
    gengar = gengar_sets[0]
    print(f"Metagross-1 Earthquake vs Gengar-1 (Levitate):")
    res = calc_matchup(meta, gengar, EARTHQUAKE, smap)
    print(format_result(res, "Earthquake"))

# ── Example 11: Stat boosts — Dragon Dance Salamence ──────────────────────
print(f"\n--- Stat boosts: +1 Atk Dragon Dance ---")
sala_sets = db.allSets("Salamence")._sets
if sala_sets and ttar_sets:
    sala = sala_sets[0]
    ttar = ttar_sets[0]
    print(f"Salamence-1 Earthquake vs Tyranitar-1 (unboosted vs +1 Atk):")
    res = calc_matchup(sala, ttar, EARTHQUAKE, smap)
    print(format_result(res, "EQ (no boost)"))
    res = calc_matchup(sala, ttar, EARTHQUAKE, smap, atk_boosts={"atk": 1})
    print(format_result(res, "EQ (+1 Atk)"))

# ── Example 12: Intimidate + Calm Mind interaction ────────────────────────
print(f"\n--- Intimidate (Atk -1) vs Calm Mind (SpA +1, SpD +1) ---")
if zam_sets and meta_sets:
    zam = zam_sets[0]
    meta = meta_sets[0]
    print(f"Metagross-1 Meteor Mash vs Alakazam-1 at -1 Atk (Intimidate):")
    res = calc_matchup(meta, zam, METEOR_MASH, smap, atk_boosts={"atk": -1})
    print(format_result(res, "Meteor Mash (-1 Atk)"))
    print(f"Alakazam-1 Psychic vs Metagross-1 at +1 SpA (Calm Mind):")
    res = calc_matchup(zam, meta, PSYCHIC, smap, atk_boosts={"spa": 1})
    print(format_result(res, "Psychic (+1 SpA)"))

# ── Example 13: Crit ignoring boost/drop ──────────────────────────────────
print(f"\n--- Crit ignoring defensive boosts ---")
if sala_sets and lax_sets:
    sala = sala_sets[0]
    lax = lax_sets[0]
    print(f"Salamence-1 EQ vs Snorlax-1 at +2 Def (Curse), normal vs crit:")
    res = calc_matchup(sala, lax, EARTHQUAKE, smap, def_boosts={"def": 2})
    print(format_result(res, "EQ vs +2 Def"))
    res = calc_matchup(sala, lax, EARTHQUAKE, smap, def_boosts={"def": 2}, critical=True)
    print(format_result(res, "EQ vs +2 Def (crit, ignores +2)"))

# ── Example 14: Raw damage_rolls + ko_chance API ─────────────────────────
print(f"\n--- Raw API usage ---")
if meta_sets and ttar_sets:
    rolls = damage_rolls(meta_sets[0], ttar_sets[0], EARTHQUAKE, smap)
    ttar_hp = calc_stats(ttar_sets[0], smap)["hp"]
    print(f"Metagross-1 EQ vs Tyranitar-1:")
    print(f"  Rolls: {rolls}")
    print(f"  Tyranitar-1 HP: {ttar_hp}")
    kos = ko_chance(rolls, ttar_hp)
    for n, prob in sorted(kos.items()):
        print(f"  {n}HKO: {prob*100:.1f}%")

# ══════════════════════════════════════════════════════════════════════════════
# Fixed-damage and variable-power move examples
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("FIXED-DAMAGE & VARIABLE-POWER MOVE EXAMPLES")
print("=" * 72)

# Dragon Rage: always 40 (but 0 vs Normal-type immunity doesn't apply,
# Dragon has no immunities in Gen 3 — should be 40 vs anything)
if lax_sets:
    lax = lax_sets[0]
    print(f"\n--- Dragon Rage (fixed 40) ---")
    res = calc_matchup(lax, meta_sets[0], DRAGON_RAGE, smap)
    print(format_result(res, "Dragon Rage vs Metagross-1"))

# SonicBoom: always 20 (immune vs Ghost types)
print(f"\n--- SonicBoom (fixed 20, immune vs Ghost) ---")
if gengar_sets:
    res = calc_matchup(meta_sets[0], meta_sets[0], SONIC_BOOM, smap)
    print(format_result(res, "SonicBoom vs Metagross-1"))
    res = calc_matchup(meta_sets[0], gengar_sets[0], SONIC_BOOM, smap)
    print(format_result(res, "SonicBoom vs Gengar-1 (Ghost immune)"))

# Seismic Toss: damage = level (100 at lv100, 50 at lv50)
print(f"\n--- Seismic Toss (damage = level) ---")
if lax_sets:
    res = calc_matchup(lax_sets[0], meta_sets[0], SEISMIC_TOSS, smap)
    print(format_result(res, "Seismic Toss lv100 vs Metagross-1"))
    res = calc_matchup(lax_sets[0], meta_sets[0], SEISMIC_TOSS, smap,
                       atk_level=50, def_level=50, atk_ivs=15, def_ivs=15)
    print(format_result(res, "Seismic Toss lv50 vs Metagross-1"))

# Night Shade: damage = level (immune vs Normal types)
print(f"\n--- Night Shade (damage = level, immune vs Normal) ---")
if gengar_sets and lax_sets:
    res = calc_matchup(gengar_sets[0], meta_sets[0], NIGHT_SHADE, smap)
    print(format_result(res, "Night Shade vs Metagross-1"))
    res = calc_matchup(gengar_sets[0], lax_sets[0], NIGHT_SHADE, smap)
    print(format_result(res, "Night Shade vs Snorlax-1 (Normal immune)"))

# Super Fang: half of target's current HP
print(f"\n--- Super Fang (half current HP) ---")
if lax_sets:
    lax_hp = calc_stats(lax_sets[0], smap)["hp"]
    res = calc_matchup(meta_sets[0], lax_sets[0], SUPER_FANG, smap)
    print(format_result(res, f"Super Fang vs Snorlax-1 (full HP={lax_hp})"))
    res = calc_matchup(meta_sets[0], lax_sets[0], SUPER_FANG, smap,
                       def_current_hp=100)
    print(format_result(res, "Super Fang vs Snorlax-1 (100 HP remaining)"))

# Endeavor: damage = max(0, target HP - user HP)
print(f"\n--- Endeavor (target HP - user HP) ---")
if lax_sets and zam_sets:
    res = calc_matchup(zam_sets[0], lax_sets[0], ENDEAVOR, smap)
    print(format_result(res, "Endeavor (Alakazam full HP vs Snorlax full HP)"))
    res = calc_matchup(zam_sets[0], lax_sets[0], ENDEAVOR, smap,
                       atk_current_hp=1)
    print(format_result(res, "Endeavor (Alakazam 1 HP vs Snorlax full HP)"))

# Eruption at full HP (150 BP) vs reduced HP
print(f"\n--- Eruption (150 * currentHP / maxHP) ---")
groudon = CustomSet("Groudon", nature="Modest", evs=[0, 0, 0, 252, 4, 252],
                    item="None", moves=["Eruption"])
if meta_sets:
    print("Groudon Eruption vs Metagross-1:")
    res = calc_matchup(groudon, meta_sets[0], ERUPTION, smap)
    print(format_result(res, "Eruption (full HP = 150 BP)"))
    groudon_max = groudon.get_stats()["hp"]
    res = calc_matchup(groudon, meta_sets[0], ERUPTION, smap,
                       atk_current_hp=groudon_max // 2)
    print(format_result(res, f"Eruption (50% HP = ~75 BP)"))
    res = calc_matchup(groudon, meta_sets[0], ERUPTION, smap,
                       atk_current_hp=1)
    print(format_result(res, "Eruption (1 HP = 1 BP)"))

# Flail: power depends on attacker's HP percentage
print(f"\n--- Flail (HP-based power) ---")
if lax_sets and zam_sets:
    lax = lax_sets[0]
    zam = zam_sets[0]
    lax_max = calc_stats(lax, smap)["hp"]
    print(f"Snorlax-1 Flail vs Alakazam-1 at various HP:")
    res = calc_matchup(lax, zam, FLAIL, smap)
    print(format_result(res, "Flail (full HP = 20 BP)"))
    res = calc_matchup(lax, zam, FLAIL, smap, atk_current_hp=lax_max // 4)
    print(format_result(res, "Flail (25% HP = 80 BP)"))
    res = calc_matchup(lax, zam, FLAIL, smap, atk_current_hp=1)
    print(format_result(res, "Flail (1 HP = 200 BP)"))

# Reversal: same mechanic as Flail, Fighting-type (immune vs Ghost)
print(f"\n--- Reversal (like Flail, but Fighting-type) ---")
if gengar_sets and ttar_sets:
    print(f"Heracross Reversal vs Tyranitar-1 at 1 HP (200 BP, SE):")
    res = calc_matchup(hera, ttar_sets[0], REVERSAL, smap, atk_current_hp=1)
    print(format_result(res, "Reversal (1 HP vs Tyranitar)"))
    print(f"Heracross Reversal vs Gengar-1 (Fighting immune):")
    res = calc_matchup(hera, gengar_sets[0], REVERSAL, smap, atk_current_hp=1)
    print(format_result(res, "Reversal (vs Gengar, immune)"))

# Low Kick: power based on target's weight
print(f"\n--- Low Kick (weight-based power) ---")
if lax_sets and zam_sets:
    lax = lax_sets[0]
    zam = zam_sets[0]
    print(f"Heracross Low Kick vs Snorlax-1 (460 kg = 120 BP):")
    res = calc_matchup(hera, lax, LOW_KICK, smap)
    print(format_result(res, "Low Kick vs Snorlax"))
    print(f"Heracross Low Kick vs Alakazam-1 (48 kg = 60 BP):")
    res = calc_matchup(hera, zam, LOW_KICK, smap)
    print(format_result(res, "Low Kick vs Alakazam"))

# Psywave: damage = floor(level * (10r + 50) / 100), r = 0..10
# Returns 11 possible rolls instead of 16
print(f"\n--- Psywave (11 random rolls, level-based) ---")
if zam_sets and lax_sets:
    zam = zam_sets[0]
    lax = lax_sets[0]
    print(f"Alakazam-1 Psywave vs Snorlax-1 (lv100):")
    res = calc_matchup(zam, lax, PSYWAVE, smap)
    print(format_result(res, "Psywave lv100 (50–150 dmg)"))
    print(f"Alakazam-1 Psywave vs Snorlax-1 (lv50):")
    res = calc_matchup(zam, lax, PSYWAVE, smap, atk_level=50, def_level=50,
                       atk_ivs=15, def_ivs=15)
    print(format_result(res, "Psywave lv50 (25–75 dmg)"))

# ══════════════════════════════════════════════════════════════════════════════
# OHKO filter examples
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 72)
print("OHKO FILTER EXAMPLES")
print("=" * 72)

# willOHKO: sets that guaranteed OHKO Alakazam-1 (min roll kills)
if zam_sets:
    zam = zam_sets[0]
    show("Sets that guaranteed OHKO Alakazam-1", db.sets.willOHKO(zam))

# canOHKO: sets that can OHKO Snorlax-1 on the max roll
if lax_sets:
    lax = lax_sets[0]
    show("Sets that can OHKO Snorlax-1 (max roll)", db.sets.canOHKO(lax))

# diesTo: Water-types that Metagross-1 guaranteed OHKOs
if meta_sets:
    meta = meta_sets[0]
    show("Water-types that Metagross-1 guaranteed OHKOs",
         db.sets.hasType("Water").diesTo(meta))

# canDieTo: sets that Alakazam-1 can OHKO on a max roll
if zam_sets:
    zam = zam_sets[0]
    show("Sets Alakazam-1 can OHKO (max roll)", db.sets.canDieTo(zam))

# Negated: EQ users that DON'T guaranteed OHKO Tyranitar-1
if ttar_sets:
    ttar = ttar_sets[0]
    show("EQ users that don't guaranteed OHKO Tyranitar-1",
         db.sets.hasMove("earthquake").Not.willOHKO(ttar))

# Negated: sets that WON'T die to Heracross even on max roll
show("Sets that survive CB Heracross (even max roll)", db.sets.Not.canDieTo(hera))

# diesTo with stat boosts
if meta_sets and ttar_sets:
    meta = meta_sets[0]
    show("Sets Metagross-1 OHKOs at +1 Atk (Dragon Dance)",
         db.sets.diesTo(meta, atk_boosts={"atk": 1}))


# ======================================================================
# Battle Dome seeding examples
# ======================================================================
print("\n" + "=" * 72)
print("BATTLE DOME SEEDING EXAMPLES")
print("=" * 72)

if meta_sets and lax_sets and ttar_sets:
    meta = meta_sets[0]
    lax  = lax_sets[0]
    ttar = ttar_sets[0]
    team = [meta, lax, ttar]

    # Player team seeding at lv100 / 31 IVs
    seed = calc_seed(team, smap)
    print(f"\nMetagross-1 / Snorlax-1 / Tyranitar-1 (lv100, 31 IVs):")
    print(f"  Player seed: {seed}")

    # Enemy team seeding (0 EV bug + mod 256 overflow)
    enemy_seed = calc_seed(team, smap, is_enemy=True)
    print(f"  Enemy seed:  {enemy_seed}  (0 EV bug + mod 256 overflow)")
    print(f"  Difference:  {seed - enemy_seed}")

    # Lv50, 15 IVs (typical early Frontier)
    seed_50 = calc_seed(team, smap, level=50, ivs=15)
    enemy_50 = calc_seed(team, smap, level=50, ivs=15, is_enemy=True)
    print(f"\nSame team at lv50, 15 IVs:")
    print(f"  Player seed: {seed_50}")
    print(f"  Enemy seed:  {enemy_50}")

# Player team with a CustomSet
print(f"\nWith a CustomSet on the player's team:")
my_meta = CustomSet("Metagross", nature="Adamant",
                    evs=[252, 252, 0, 0, 4, 0], item="Choice Band")
if lax_sets and ttar_sets:
    mixed_team = [my_meta, lax_sets[0], ttar_sets[0]]
    seed = calc_seed(mixed_team, smap)
    print(f"  Custom Metagross / Snorlax-1 / Tyranitar-1: seed = {seed}")

# Monte Carlo: estimate highest enemy seed in a round 8 Tower run
print(f"\nMonte Carlo: highest enemy seed across 1000 random round 8 teams:")
set_lookup = {f"{s['Pokemon']}-{s['SetNum']}": s for s in db._sets}
best_seed = 0
best_team_str = ""
n_samples = 1000
for _ in range(n_samples):
    result = tower.random_team(8)
    if result.startswith("Error"):
        continue
    # Parse "CLASS Name: SetId1, SetId2, SetId3"
    label, ids_str = result.split(": ", 1)
    set_ids = [s.strip() for s in ids_str.split(", ")]
    team_sets = [set_lookup[sid] for sid in set_ids if sid in set_lookup]
    if len(team_sets) != 3:
        continue
    seed = calc_seed(team_sets, smap, is_enemy=True)
    if seed > best_seed:
        best_seed = seed
        best_team_str = result
print(f"  Highest seed: {best_seed}")
print(f"  Team: {best_team_str}")