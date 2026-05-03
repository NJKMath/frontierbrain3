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


> ```python
> from frontierbrain3 import Database
> db = Database()
> db.sets       # SetCollection of all 918 frontier sets (882 regular + 36 Frontier Brain)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(918 sets)
> [
>   'Sunkern-1', 'Azurill-1', 'Caterpie-1', 'Weedle-1', 'Wurmple-1', 'Ralts-1', 'Magikarp-1', 'Feebas-1', 'Metapod-1',
>   'Kakuna-1', 'Pichu-1', 'Silcoon-1', 'Cascoon-1', 'Igglybuff-1', 'Wooper-1', 'Tyrogue-1', 'Sentret-1', 'Cleffa-1',
>   'Seedot-1', 'Lotad-1', 'Poochyena-1', 'Shedinja-1', 'Makuhita-1', 'Whismur-1', 'Zigzagoon-1', 'Zubat-1', 'Togepi-1',
>   'Spinarak-1', 'Marill-1', 'Hoppip-1', 'Slugma-1', 'Swinub-1', 'Smeargle-1', 'Pidgey-1', 'Rattata-1', 'Wynaut-1',
>   'Skitty-1', 'Spearow-1', 'Hoothoot-1', 'Diglett-1', 'Ledyba-1', 'Nincada-1', 'Surskit-1', 'Jigglypuff-1', 'Taillow-1',
>   'Wingull-1', 'NidoranM-1', 'NidoranF-1', 'Kirlia-1', 'Mareep-1', 'Meditite-1', 'Slakoth-1', 'Paras-1', 'Ekans-1',
>   'Ditto-1', 'Barboach-1', 'Meowth-1', 'Pineco-1', 'Trapinch-1', 'Spheal-1', 'Horsea-1', 'Shroomish-1', 'Shuppet-1',
>   'Duskull-1', 'Electrike-1', 'Vulpix-1', 'Pikachu-1', 'Sandshrew-1', 'Poliwag-1', 'Bellsprout-1', 'Geodude-1',
>   'Dratini-1', 'Snubbull-1', 'Remoraid-1', 'Larvitar-1', 'Baltoy-1', 'Snorunt-1', 'Bagon-1', 'Beldum-1', 'Gulpin-1',
>   'Venonat-1', 'Mankey-1', 'Machop-1', 'Shellder-1', 'Smoochum-1', 'Numel-1', 'Carvanha-1', 'Corphish-1',
>   'Charmander-1', 'Cyndaquil-1', 'Abra-1', 'Doduo-1', 'Gastly-1', 'Swablu-1', 'Treecko-1', 'Torchic-1', 'Mudkip-1',
>   'Squirtle-1', 'Totodile-1', 'Slowpoke-1', 'Bulbasaur-1', 'Chikorita-1', 'Oddish-1', 'Psyduck-1', 'Cubone-1',
>   'Goldeen-1', 'Natu-1', 'Clefairy-1', 'Magnemite-1', 'Seel-1', 'Grimer-1', 'Krabby-1', 'Exeggcute-1', 'Eevee-1',
>   'Drowzee-1', 'Voltorb-1', 'Chinchou-1', 'Teddiursa-1', 'Delibird-1', 'Houndour-1', 'Phanpy-1', 'Spoink-1', 'Aron-1',
>   'Luvdisc-1', 'Tentacool-1', 'Cacnea-1', 'Unown-1', 'Koffing-1', 'Staryu-1', 'Skiploom-1', 'Nuzleaf-1', 'Lombre-1',
>   'Vibrava-1', 'Rhyhorn-1', 'Clamperl-1', 'Pidgeotto-1', 'Growlithe-1', "Farfetch'd-1", 'Omanyte-1', 'Kabuto-1',
>   'Lileep-1', 'Anorith-1', 'Aipom-1', 'Elekid-1', 'Loudred-1', 'Spinda-1', 'Nidorina-1', 'Nidorino-1', 'Flaaffy-1',
>   'Magby-1', 'Nosepass-1', 'Corsola-1', 'Mawile-1', 'Butterfree-1', 'Beedrill-1', 'Poliwhirl-1', 'Onix-1',
>   'Beautifly-1', 'Dustox-1', 'Ledian-1', 'Ariados-1', 'Yanma-1', 'Delcatty-1', 'Sableye-1', 'Lickitung-1',
>   'Weepinbell-1', 'Graveler-1', 'Gloom-1', 'Porygon-1', 'Kadabra-1', 'Wailmer-1', 'Roselia-1', 'Volbeat-1',
>   'Illumise-1', 'Ivysaur-1', 'Charmeleon-1', 'Wartortle-1', 'Parasect-1', 'Machoke-1', 'Haunter-1', 'Bayleef-1',
>   'Quilava-1', 'Croconaw-1', 'Togetic-1', 'Murkrow-1', 'Wobbuffet-1', 'Plusle-1', 'Minun-1', 'Grovyle-1', 'Combusken-1',
>   'Marshtomp-1', 'Ponyta-1', 'Azumarill-1', 'Sudowoodo-1', 'Magcargo-1', 'Pupitar-1', 'Sealeo-1', 'Raticate-1',
>   'Masquerain-1', 'Furret-1', 'Dunsparce-1', 'Dragonair-1', 'Mightyena-1', 'Linoone-1', 'Castform-1', 'Shelgon-1',
>   'Metang-1', 'Wigglytuff-1', 'Sunflora-1', 'Chimecho-1', 'Gligar-1', 'Qwilfish-1', 'Sneasel-1', 'Pelipper-1',
>   'Swellow-1', 'Lairon-1', 'Tangela-1', 'Arbok-1', 'Persian-1', 'Seadra-1', 'Kecleon-1', 'Vigoroth-1', 'Lunatone-1',
>   'Solrock-1', 'Noctowl-1', 'Sandslash-1', 'Venomoth-1', 'Chansey-1', 'Seaking-1', 'Jumpluff-1', 'Piloswine-1',
>   'Golbat-1', 'Primeape-1', 'Hitmonlee-1', 'Hitmonchan-1', 'Girafarig-1', 'Hitmontop-1', 'Banette-1', 'Ninjask-1',
>   'Seviper-1', 'Zangoose-1', 'Camerupt-1', 'Sharpedo-1', 'Tropius-1', 'Magneton-1', 'Mantine-1', 'Stantler-1',
>   'Absol-1', 'Swalot-1', 'Crawdaunt-1', 'Pidgeot-1', 'Grumpig-1', 'Torkoal-1', 'Kingler-1', 'Cacturne-1', 'Bellossom-1',
>   'Octillery-1', 'Huntail-1', 'Gorebyss-1', 'Relicanth-1', 'Omastar-1', 'Kabutops-1', 'Poliwrath-1', 'Scyther-1',
>   'Pinsir-1', 'Politoed-1', 'Cloyster-1', 'Delcatty-2', 'Sableye-2', 'Lickitung-2', 'Weepinbell-2', 'Graveler-2',
>   'Gloom-2', 'Porygon-2', 'Kadabra-2', 'Wailmer-2', 'Roselia-2', 'Volbeat-2', 'Illumise-2', 'Ivysaur-2', 'Charmeleon-2',
>   'Wartortle-2', 'Parasect-2', 'Machoke-2', 'Haunter-2', 'Bayleef-2', 'Quilava-2', 'Croconaw-2', 'Togetic-2',
>   'Murkrow-2', 'Wobbuffet-2', 'Plusle-2', 'Minun-2', 'Grovyle-2', 'Combusken-2', 'Marshtomp-2', 'Ponyta-2',
>   'Azumarill-2', 'Sudowoodo-2', 'Magcargo-2', 'Pupitar-2', 'Sealeo-2', 'Raticate-2', 'Masquerain-2', 'Furret-2',
>   'Dunsparce-2', 'Dragonair-2', 'Mightyena-2', 'Linoone-2', 'Castform-2', 'Shelgon-2', 'Metang-2', 'Wigglytuff-2',
>   'Sunflora-2', 'Chimecho-2', 'Gligar-2', 'Qwilfish-2', 'Sneasel-2', 'Pelipper-2', 'Swellow-2', 'Lairon-2', 'Tangela-2',
>   'Arbok-2', 'Persian-2', 'Seadra-2', 'Kecleon-2', 'Vigoroth-2', 'Lunatone-2', 'Solrock-2', 'Noctowl-2', 'Sandslash-2',
>   'Venomoth-2', 'Chansey-2', 'Seaking-2', 'Jumpluff-2', 'Piloswine-2', 'Golbat-2', 'Primeape-2', 'Hitmonlee-2',
>   'Hitmonchan-2', 'Girafarig-2', 'Hitmontop-2', 'Banette-2', 'Ninjask-2', 'Seviper-2', 'Zangoose-2', 'Camerupt-2',
>   'Sharpedo-2', 'Tropius-2', 'Magneton-2', 'Mantine-2', 'Stantler-2', 'Absol-2', 'Swalot-2', 'Crawdaunt-2', 'Pidgeot-2',
>   'Grumpig-2', 'Torkoal-2', 'Kingler-2', 'Cacturne-2', 'Bellossom-2', 'Octillery-2', 'Huntail-2', 'Gorebyss-2',
>   'Relicanth-2', 'Omastar-2', 'Kabutops-2', 'Poliwrath-2', 'Scyther-2', 'Pinsir-2', 'Politoed-2', 'Cloyster-2',
>   'Dugtrio-1', 'Medicham-1', 'Misdreavus-1', 'Fearow-1', 'Granbull-1', 'Jynx-1', 'Dusclops-1', 'Dodrio-1', 'Mr. Mime-1',
>   'Lanturn-1', 'Breloom-1', 'Forretress-1', 'Whiscash-1', 'Xatu-1', 'Skarmory-1', 'Marowak-1', 'Quagsire-1',
>   'Clefable-1', 'Hariyama-1', 'Raichu-1', 'Dewgong-1', 'Manectric-1', 'Vileplume-1', 'Victreebel-1', 'Electrode-1',
>   'Exploud-1', 'Shiftry-1', 'Glalie-1', 'Ludicolo-1', 'Hypno-1', 'Golem-1', 'Rhydon-1', 'Alakazam-1', 'Weezing-1',
>   'Kangaskhan-1', 'Electabuzz-1', 'Tauros-1', 'Slowbro-1', 'Slowking-1', 'Miltank-1', 'Altaria-1', 'Nidoqueen-1',
>   'Nidoking-1', 'Magmar-1', 'Cradily-1', 'Armaldo-1', 'Golduck-1', 'Rapidash-1', 'Muk-1', 'Gengar-1', 'Ampharos-1',
>   'Scizor-1', 'Heracross-1', 'Ursaring-1', 'Houndoom-1', 'Donphan-1', 'Claydol-1', 'Wailord-1', 'Ninetales-1',
>   'Machamp-1', 'Shuckle-1', 'Steelix-1', 'Tentacruel-1', 'Aerodactyl-1', 'Porygon2-1', 'Gardevoir-1', 'Exeggutor-1',
>   'Starmie-1', 'Flygon-1', 'Venusaur-1', 'Vaporeon-1', 'Jolteon-1', 'Flareon-1', 'Meganium-1', 'Espeon-1', 'Umbreon-1',
>   'Blastoise-1', 'Feraligatr-1', 'Aggron-1', 'Blaziken-1', 'Walrein-1', 'Sceptile-1', 'Charizard-1', 'Typhlosion-1',
>   'Lapras-1', 'Crobat-1', 'Swampert-1', 'Gyarados-1', 'Snorlax-1', 'Kingdra-1', 'Blissey-1', 'Milotic-1', 'Arcanine-1',
>   'Salamence-1', 'Metagross-1', 'Slaking-1', 'Dugtrio-2', 'Medicham-2', 'Marowak-2', 'Quagsire-2', 'Misdreavus-2',
>   'Fearow-2', 'Granbull-2', 'Jynx-2', 'Dusclops-2', 'Dodrio-2', 'Mr. Mime-2', 'Lanturn-2', 'Breloom-2', 'Forretress-2',
>   'Skarmory-2', 'Whiscash-2', 'Xatu-2', 'Clefable-2', 'Hariyama-2', 'Raichu-2', 'Dewgong-2', 'Manectric-2',
>   'Vileplume-2', 'Victreebel-2', 'Electrode-2', 'Exploud-2', 'Shiftry-2', 'Glalie-2', 'Ludicolo-2', 'Hypno-2',
>   'Golem-2', 'Rhydon-2', 'Alakazam-2', 'Weezing-2', 'Kangaskhan-2', 'Electabuzz-2', 'Tauros-2', 'Slowbro-2',
>   'Slowking-2', 'Miltank-2', 'Altaria-2', 'Nidoqueen-2', 'Nidoking-2', 'Magmar-2', 'Cradily-2', 'Armaldo-2',
>   'Golduck-2', 'Rapidash-2', 'Muk-2', 'Gengar-2', 'Ampharos-2', 'Scizor-2', 'Heracross-2', 'Ursaring-2', 'Houndoom-2',
>   'Donphan-2', 'Claydol-2', 'Wailord-2', 'Ninetales-2', 'Machamp-2', 'Shuckle-2', 'Steelix-2', 'Tentacruel-2',
>   'Aerodactyl-2', 'Porygon2-2', 'Gardevoir-2', 'Exeggutor-2', 'Starmie-2', 'Flygon-2', 'Venusaur-2', 'Vaporeon-2',
>   'Jolteon-2', 'Flareon-2', 'Meganium-2', 'Espeon-2', 'Umbreon-2', 'Blastoise-2', 'Feraligatr-2', 'Aggron-2',
>   'Blaziken-2', 'Walrein-2', 'Sceptile-2', 'Charizard-2', 'Typhlosion-2', 'Lapras-2', 'Crobat-2', 'Swampert-2',
>   'Gyarados-2', 'Snorlax-2', 'Kingdra-2', 'Blissey-2', 'Milotic-2', 'Arcanine-2', 'Salamence-2', 'Metagross-2',
>   'Slaking-2', 'Dugtrio-3', 'Medicham-3', 'Misdreavus-3', 'Fearow-3', 'Granbull-3', 'Jynx-3', 'Dusclops-3', 'Dodrio-3',
>   'Mr. Mime-3', 'Lanturn-3', 'Breloom-3', 'Forretress-3', 'Whiscash-3', 'Xatu-3', 'Skarmory-3', 'Marowak-3',
>   'Quagsire-3', 'Clefable-3', 'Hariyama-3', 'Raichu-3', 'Dewgong-3', 'Manectric-3', 'Vileplume-3', 'Victreebel-3',
>   'Electrode-3', 'Exploud-3', 'Shiftry-3', 'Glalie-3', 'Ludicolo-3', 'Hypno-3', 'Golem-3', 'Rhydon-3', 'Alakazam-3',
>   'Weezing-3', 'Kangaskhan-3', 'Electabuzz-3', 'Tauros-3', 'Slowbro-3', 'Slowking-3', 'Miltank-3', 'Altaria-3',
>   'Nidoqueen-3', 'Nidoking-3', 'Magmar-3', 'Cradily-3', 'Armaldo-3', 'Golduck-3', 'Rapidash-3', 'Muk-3', 'Gengar-3',
>   'Ampharos-3', 'Scizor-3', 'Heracross-3', 'Ursaring-3', 'Houndoom-3', 'Donphan-3', 'Claydol-3', 'Wailord-3',
>   'Ninetales-3', 'Machamp-3', 'Shuckle-3', 'Steelix-3', 'Tentacruel-3', 'Aerodactyl-3', 'Porygon2-3', 'Gardevoir-3',
>   'Exeggutor-3', 'Starmie-3', 'Flygon-3', 'Venusaur-3', 'Vaporeon-3', 'Jolteon-3', 'Flareon-3', 'Meganium-3',
>   'Espeon-3', 'Umbreon-3', 'Blastoise-3', 'Feraligatr-3', 'Aggron-3', 'Blaziken-3', 'Walrein-3', 'Sceptile-3',
>   'Charizard-3', 'Typhlosion-3', 'Lapras-3', 'Crobat-3', 'Swampert-3', 'Gyarados-3', 'Snorlax-3', 'Kingdra-3',
>   'Blissey-3', 'Milotic-3', 'Arcanine-3', 'Salamence-3', 'Metagross-3', 'Slaking-3', 'Dugtrio-4', 'Medicham-4',
>   'Misdreavus-4', 'Fearow-4', 'Granbull-4', 'Jynx-4', 'Dusclops-4', 'Dodrio-4', 'Mr. Mime-4', 'Lanturn-4', 'Breloom-4',
>   'Forretress-4', 'Whiscash-4', 'Xatu-4', 'Skarmory-4', 'Marowak-4', 'Quagsire-4', 'Clefable-4', 'Hariyama-4',
>   'Raichu-4', 'Dewgong-4', 'Manectric-4', 'Vileplume-4', 'Victreebel-4', 'Electrode-4', 'Exploud-4', 'Shiftry-4',
>   'Glalie-4', 'Ludicolo-4', 'Hypno-4', 'Golem-4', 'Rhydon-4', 'Alakazam-4', 'Weezing-4', 'Kangaskhan-4', 'Electabuzz-4',
>   'Tauros-4', 'Slowbro-4', 'Slowking-4', 'Miltank-4', 'Altaria-4', 'Nidoqueen-4', 'Nidoking-4', 'Magmar-4', 'Cradily-4',
>   'Armaldo-4', 'Golduck-4', 'Rapidash-4', 'Muk-4', 'Gengar-4', 'Ampharos-4', 'Scizor-4', 'Heracross-4', 'Ursaring-4',
>   'Houndoom-4', 'Donphan-4', 'Claydol-4', 'Wailord-4', 'Ninetales-4', 'Machamp-4', 'Shuckle-4', 'Steelix-4',
>   'Tentacruel-4', 'Aerodactyl-4', 'Porygon2-4', 'Gardevoir-4', 'Exeggutor-4', 'Starmie-4', 'Flygon-4', 'Venusaur-4',
>   'Vaporeon-4', 'Jolteon-4', 'Flareon-4', 'Meganium-4', 'Espeon-4', 'Umbreon-4', 'Blastoise-4', 'Feraligatr-4',
>   'Aggron-4', 'Blaziken-4', 'Walrein-4', 'Sceptile-4', 'Charizard-4', 'Typhlosion-4', 'Lapras-4', 'Crobat-4',
>   'Swampert-4', 'Gyarados-4', 'Snorlax-4', 'Kingdra-4', 'Blissey-4', 'Milotic-4', 'Arcanine-4', 'Salamence-4',
>   'Metagross-4', 'Slaking-4', 'Articuno-1', 'Zapdos-1', 'Moltres-1', 'Raikou-1', 'Entei-1', 'Suicune-1', 'Regirock-1',
>   'Regice-1', 'Registeel-1', 'Latias-1', 'Latios-1', 'Articuno-2', 'Zapdos-2', 'Moltres-2', 'Raikou-2', 'Entei-2',
>   'Suicune-2', 'Regirock-2', 'Regice-2', 'Registeel-2', 'Latias-2', 'Latios-2', 'Articuno-3', 'Zapdos-3', 'Moltres-3',
>   'Raikou-3', 'Entei-3', 'Suicune-3', 'Regirock-3', 'Regice-3', 'Registeel-3', 'Latias-3', 'Latios-3', 'Articuno-4',
>   'Zapdos-4', 'Moltres-4', 'Raikou-4', 'Entei-4', 'Suicune-4', 'Regirock-4', 'Regice-4', 'Registeel-4', 'Latias-4',
>   'Latios-4', 'Gengar-5', 'Gengar-6', 'Gengar-7', 'Gengar-8', 'Ursaring-5', 'Ursaring-6', 'Ursaring-7', 'Ursaring-8',
>   'Machamp-5', 'Machamp-6', 'Machamp-7', 'Machamp-8', 'Gardevoir-5', 'Gardevoir-6', 'Gardevoir-7', 'Gardevoir-8',
>   'Starmie-5', 'Starmie-6', 'Starmie-7', 'Starmie-8', 'Lapras-5', 'Lapras-6', 'Lapras-7', 'Lapras-8', 'Snorlax-5',
>   'Snorlax-6', 'Snorlax-7', 'Snorlax-8', 'Salamence-5', 'Salamence-6', 'Salamence-7', 'Salamence-8', 'Metagross-5',
>   'Metagross-6', 'Metagross-7', 'Metagross-8', 'Regirock-5', 'Regirock-6', 'Regice-5', 'Regice-6', 'Registeel-5',
>   'Registeel-6', 'Latias-5', 'Latias-6', 'Latias-7', 'Latias-8', 'Latios-5', 'Latios-6', 'Latios-7', 'Latios-8',
>   'Dragonite-1', 'Dragonite-2', 'Dragonite-3', 'Dragonite-4', 'Dragonite-5', 'Dragonite-6', 'Dragonite-7',
>   'Dragonite-8', 'Dragonite-9', 'Dragonite-10', 'Tyranitar-1', 'Tyranitar-2', 'Tyranitar-3', 'Tyranitar-4',
>   'Tyranitar-5', 'Tyranitar-6', 'Tyranitar-7', 'Tyranitar-8', 'Tyranitar-9', 'Tyranitar-10', 'Articuno-5', 'Articuno-6',
>   'Zapdos-5', 'Zapdos-6', 'Moltres-5', 'Moltres-6', 'Raikou-5', 'Raikou-6', 'Entei-5', 'Entei-6', 'Suicune-5',
>   'Suicune-6', 'Alakazam-AnabelSilver', 'Entei-AnabelSilver', 'Snorlax-AnabelSilver', 'Raikou-AnabelGold',
>   'Latios-AnabelGold', 'Snorlax-AnabelGold', 'Swampert-TuckerSilver', 'Salamence-TuckerSilver',
>   'Charizard-TuckerSilver', 'Swampert-TuckerGold', 'Metagross-TuckerGold', 'Latias-TuckerGold', 'Crobat-SpenserSilver',
>   'Slaking-SpenserSilver', 'Lapras-SpenserSilver', 'Arcanine-SpenserGold', 'Slaking-SpenserGold', 'Suicune-SpenserGold',
>   'Heracross-GretaSilver', 'Umbreon-GretaSilver', 'Shedinja-GretaSilver', 'Umbreon-GretaGold', 'Gengar-GretaGold',
>   'Breloom-GretaGold', 'Seviper-LucySilver', 'Shuckle-LucySilver', 'Milotic-LucySilver', 'Seviper-LucyGold',
>   'Steelix-LucyGold', 'Gyarados-LucyGold', 'Regirock-BrandonSilver', 'Registeel-BrandonSilver', 'Regice-BrandonSilver',
>   'Articuno-BrandonGold', 'Zapdos-BrandonGold', 'Moltres-BrandonGold'
> ]
> ```
>
> </details>


<br>

> ```python
> db.trainers   # TrainerCollection of all trainers (300 regular + Frontier Brains)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(312 trainers)
> [
>   'YOUNGSTER BRADY', 'YOUNGSTER CONNER', 'YOUNGSTER BRADLEY', 'LASS CYBIL', 'LASS RODETTE', 'LASS PEGGY',
>   'SCHOOL KID (M) KEITH', 'SCHOOL KID (M) GRAYSON', 'SCHOOL KID (M) GLENN', 'SCHOOL KID (F) LILIANA',
>   'SCHOOL KID (F) ELISE', 'SCHOOL KID (F) ZOEY', 'RICH BOY MANUEL', 'RICH BOY RUSS', 'RICH BOY DUSTIN', 'LADY TINA',
>   'LADY GILLIAN', 'LADY ZOE', 'CAMPER CHEN', 'CAMPER AL', 'CAMPER MITCH', 'PICNICKER ANNE', 'PICNICKER ALIZE',
>   'PICNICKER LAUREN', 'TUBER (M) KIPP', 'TUBER (M) JASON', 'TUBER (M) JOHN', 'TUBER (F) ANN', 'TUBER (F) EILEEN',
>   'TUBER (F) CARLIE', 'SWIMMER (M) GORDON', 'SWIMMER (M) AYDEN', 'SWIMMER (M) MARCO', 'SWIMMER (F) CIERRA',
>   'SWIMMER (F) MARCY', 'SWIMMER (F) KATHY', 'POKÉFAN (M) PEYTON', 'POKÉFAN (M) JULIAN', 'POKÉFAN (M) QUINN',
>   'POKÉFAN (F) HAYLEE', 'POKÉFAN (F) AMANDA', 'POKÉFAN (F) STACY', 'PKMN BREEDER (M) RAFAEL', 'PKMN BREEDER (M) OLIVER',
>   'PKMN BREEDER (M) PAYTON', 'PKMN BREEDER (F) PAMELA', 'PKMN BREEDER (F) ELIZA', 'PKMN BREEDER (F) MARISA',
>   'BUG CATCHER LEWIS', 'BUG CATCHER YOSHI', 'BUG CATCHER DESTIN', 'NINJA BOY KEON', 'NINJA BOY STUART',
>   'NINJA BOY NESTOR', 'BUG MANIAC DERRICK', 'BUG MANIAC BRYSON', 'BUG MANIAC CLAYTON', 'FISHERMAN TRENTON',
>   'FISHERMAN JENSON', 'FISHERMAN WESLEY', 'RUIN MANIAC ANTON', 'RUIN MANIAC LAWSON', 'RUIN MANIAC SAMMY',
>   'COLLECTOR ARNIE', 'COLLECTOR ADRIAN', 'COLLECTOR TRISTAN', 'PARASOL LADY JULIANA', 'PARASOL LADY RYLEE',
>   'PARASOL LADY CHELSEA', 'BEAUTY DANELA', 'BEAUTY LIZBETH', 'BEAUTY AMELIA', 'AROMA LADY JILLIAN', 'AROMA LADY ABBIE',
>   'AROMA LADY BRIANA', 'GUITARIST ANTONIO', 'GUITARIST JADEN', 'GUITARIST DAKOTA', 'BIRD KEEPER BRAYDEN',
>   'BIRD KEEPER CORSON', 'BIRD KEEPER TREVIN', 'SAILOR PATRICK', 'SAILOR KADEN', 'SAILOR MAXWELL', 'HIKER DARYL',
>   'HIKER KENNETH', 'HIKER RICH', 'KINDLER CADEN', 'KINDLER MARLON', 'KINDLER NASH', 'TRIATHLETE (M RUNNER) ROBBY',
>   'TRIATHLETE (M RUNNER) REECE', 'TRIATHLETE (F RUNNER) KATHRYN', 'TRIATHLETE (F RUNNER) ELLEN',
>   'TRIATHLETE (M SWIMMER) RAMON', 'TRIATHLETE (M SWIMMER) ARTHUR', 'TRIATHLETE (F SWIMMER) ALONDRA',
>   'TRIATHLETE (F SWIMMER) ADRIANA', 'TRIATHLETE (M BIKER) MALIK', 'TRIATHLETE (F BIKER) JILL',
>   'TRIATHLETE (M RUNNER) ERIK', 'TRIATHLETE (F RUNNER) YAZMIN', 'TRIATHLETE (M SWIMMER) JAMAL',
>   'TRIATHLETE (F SWIMMER) LESLIE', 'TRIATHLETE (M BIKER) DAVE', 'TRIATHLETE (M BIKER) CARLO',
>   'TRIATHLETE (F BIKER) EMILIA', 'TRIATHLETE (F BIKER) DALIA', 'BLACK BELT HITOMI', 'BLACK BELT RICARDO',
>   'BLACK BELT SHIZUKA', 'BATTLE GIRL JOANA', 'BATTLE GIRL KELLY', 'BATTLE GIRL RAYNA', 'EXPERT (M) EVAN',
>   'EXPERT (M) JORDAN', 'EXPERT (M) JOEL', 'EXPERT (F) KRISTEN', 'EXPERT (F) SELPHY', 'EXPERT (F) CHLOE',
>   'PSYCHIC (M) NORTON', 'PSYCHIC (M) LUKAS', 'PSYCHIC (M) ZACH', 'PSYCHIC (F) KAITLYN', 'PSYCHIC (F) BREANNA',
>   'PSYCHIC (F) KENDRA', 'HEX MANIAC MOLLY', 'HEX MANIAC JAZMIN', 'HEX MANIAC KELSEY', 'POKÉMANIAC JALEN',
>   'POKÉMANIAC GRIFFEN', 'POKÉMANIAC XANDER', 'GENTLEMAN MARVIN', 'GENTLEMAN BRENNAN', 'BUG MANIAC BALEY',
>   'RUIN MANIAC ZACKARY', 'COLLECTOR GABRIEL', 'PARASOL LADY EMILY', 'BEAUTY JORDYN', 'AROMA LADY SOFIA',
>   'COOLTRAINER (M) BRADEN', 'COOLTRAINER (M) KAYDEN', 'COOLTRAINER (M) COOPER', 'COOLTRAINER (F) JULIA',
>   'COOLTRAINER (F) AMARA', 'COOLTRAINER (F) LYNN', 'PKMN RANGER (M) JOVAN', 'PKMN RANGER (M) DOMINIC',
>   'PKMN RANGER (M) NIKOLAS', 'PKMN RANGER (F) VALERIA', 'PKMN RANGER (F) DELANEY', 'PKMN RANGER (F) MEGHAN',
>   'DRAGON TAMER ROBERTO', 'DRAGON TAMER DAMIAN', 'DRAGON TAMER BRODY', 'DRAGON TAMER GRAHAM', 'POKÉFAN (M) TYLOR',
>   'POKÉFAN (F) JAREN', 'PKMN BREEDER (M) CORDELL', 'PKMN BREEDER (F) JAZLYN', 'YOUNGSTER ZACHERY', 'YOUNGSTER JOHAN',
>   'LASS SHEA', 'LASS KAILA', 'SCHOOL KID (M) ISIAH', 'SCHOOL KID (M) GARRETT', 'SCHOOL KID (F) HAYLIE',
>   'SCHOOL KID (F) MEGAN', 'RICH BOY ISSAC', 'RICH BOY QUINTON', 'LADY SALMA', 'LADY ANSLEY', 'BUG CATCHER HOLDEN',
>   'BUG CATCHER LUCA', 'NINJA BOY JAMISON', 'NINJA BOY GUNNAR', 'TUBER (M) CRAIG', 'TUBER (M) PIERCE',
>   'TUBER (F) REGINA', 'TUBER (F) ALISON', 'BUG MANIAC HANK', 'BUG MANIAC EARL', 'FISHERMAN RAMIRO', 'FISHERMAN HUNTER',
>   'RUIN MANIAC AIDEN', 'RUIN MANIAC XAVIER', 'COLLECTOR CLINTON', 'COLLECTOR JESSE', 'GUITARIST EDUARDO',
>   'GUITARIST HAL', 'BIRD KEEPER GAGE', 'BIRD KEEPER ARNOLD', 'SAILOR JARRETT', 'SAILOR GARETT', 'HIKER EMANUEL',
>   'HIKER GUSTAVO', 'KINDLER KAMERON', 'KINDLER ALFREDO', 'GENTLEMAN RUBEN', 'GENTLEMAN LAMAR', 'YOUNGSTER JAXON',
>   'YOUNGSTER LOGAN', 'LASS EMILEE', 'LASS JOSIE', 'CAMPER ARMANDO', 'CAMPER SKYLER', 'PICNICKER RUTH',
>   'PICNICKER MELODY', 'SWIMMER (M) PEDRO', 'SWIMMER (M) ERICK', 'SWIMMER (F) ELAINE', 'SWIMMER (F) JOYCE',
>   'POKÉFAN (M) TODD', 'POKÉFAN (M) GAVIN', 'POKÉFAN (F) MALORY', 'POKÉFAN (F) ESTHER', 'PKMN BREEDER (M) OSCAR',
>   'PKMN BREEDER (M) WILSON', 'PKMN BREEDER (F) CLARE', 'PKMN BREEDER (F) TESS', 'COOLTRAINER (M) LEON',
>   'COOLTRAINER (M) ALONZO', 'COOLTRAINER (M) VINCE', 'COOLTRAINER (M) BRYON', 'COOLTRAINER (F) AVA',
>   'COOLTRAINER (F) MIRIAM', 'COOLTRAINER (F) CARRIE', 'COOLTRAINER (F) GILLIAN', 'PKMN RANGER (M) TYLER',
>   'PKMN RANGER (M) CHAZ', 'PKMN RANGER (M) NELSON', 'PKMN RANGER (F) SHANIA', 'PKMN RANGER (F) STELLA',
>   'PKMN RANGER (F) DORINE', 'DRAGON TAMER MADDOX', 'DRAGON TAMER DAVIN', 'DRAGON TAMER TREVON', 'BLACK BELT MATEO',
>   'BLACK BELT BRET', 'BLACK BELT RAUL', 'BATTLE GIRL KAY', 'BATTLE GIRL ELENA', 'BATTLE GIRL ALANA',
>   'EXPERT (M) ALEXAS', 'EXPERT (M) WESTON', 'EXPERT (M) JASPER', 'EXPERT (F) NADIA', 'EXPERT (F) MIRANDA',
>   'EXPERT (F) EMMA', 'PSYCHIC (M) ROLANDO', 'PSYCHIC (M) STANLY', 'PSYCHIC (M) DARIO', 'PSYCHIC (F) KARLEE',
>   'PSYCHIC (F) JAYLIN', 'PSYCHIC (F) INGRID', 'HEX MANIAC DELILAH', 'HEX MANIAC CARLY', 'HEX MANIAC LEXIE',
>   'POKÉMANIAC MILLER', 'POKÉMANIAC MARV', 'POKÉMANIAC LAYTON', 'GENTLEMAN BROOKS', 'GENTLEMAN GREGORY',
>   'GENTLEMAN REESE', 'TRIATHLETE (M RUNNER) MASON', 'TRIATHLETE (M RUNNER) TOBY', 'TRIATHLETE (F RUNNER) DOROTHY',
>   'TRIATHLETE (F RUNNER) PIPER', 'TRIATHLETE (M SWIMMER) FINN', 'TRIATHLETE (M SWIMMER) SAMIR',
>   'TRIATHLETE (F SWIMMER) FIONA', 'TRIATHLETE (F SWIMMER) GLORIA', 'TRIATHLETE (M BIKER) NICO',
>   'TRIATHLETE (M BIKER) JEREMY', 'TRIATHLETE (F BIKER) CAITLIN', 'TRIATHLETE (F BIKER) REENA', 'BUG MANIAC AVERY',
>   'BUG MANIAC LIAM', 'FISHERMAN THEO', 'FISHERMAN BAILEY', 'RUIN MANIAC HUGO', 'RUIN MANIAC BRYCE', 'COLLECTOR GIDEON',
>   'COLLECTOR TRISTON', 'GUITARIST CHARLES', 'GUITARIST RAYMOND', 'BIRD KEEPER DIRK', 'BIRD KEEPER HAROLD',
>   'SAILOR OMAR', 'SAILOR PETER', 'HIKER DEV', 'HIKER COREY', 'KINDLER ANDRE', 'KINDLER FERRIS', 'PARASOL LADY ALIVIA',
>   'PARASOL LADY PAIGE', 'BEAUTY ANYA', 'BEAUTY DAWN', 'AROMA LADY ABBY', 'AROMA LADY GRETEL', 'SALON MAIDEN ANABEL',
>   'SALON MAIDEN ANABEL', 'DOME ACE TUCKER', 'DOME ACE TUCKER', 'PALACE MAVEN SPENSER', 'PALACE MAVEN SPENSER',
>   'ARENA TYCOON GRETA', 'ARENA TYCOON GRETA', 'PIKE QUEEN LUCY', 'PIKE QUEEN LUCY', 'PYRAMID KING BRANDON',
>   'PYRAMID KING BRANDON'
> ]
> ```
>
> </details>


<br>

> ```python
> db.allSets("Charizard").ids()
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


---

## CustomSet

Represents a player-defined Pokemon with full control over species, nature, EVs, IVs, level, item, ability, and moves.


> ```python
> from frontierbrain3 import CustomSet
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


<br>

> ```python
> flygon.get_stats()
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


<br>

> ```python
> flygon.speed()
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


The `stats` parameter lets you directly declare stat values rather than calculating them from nature/EVs/IVs:


> ```python
> custom = CustomSet("Flygon", stats={"hp": 302, "atk": 299, "def": 196, "spa": 176, "spd": 196, "spe": 328})
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> custom = CustomSet(Flygon, stats={'hp': 302, 'atk': 299, 'def': 196, 'spa': 176, 'spd': 196, 'spe': 328}, level=100, ability=levitate)
> ```
>
> </details>


<br>

> ```python
> custom.get_stats()
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


### Pokepaste Import

Import teams from [Pokepaste](https://pokepast.es/) format:


> ```python
> from frontierbrain3 import from_paste
> from_paste("""
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
> {
>   'CustomSkarmory': CustomSet(Skarmory, nature=Bold, evs=[252, 0, 252, 0, 4, 0], ivs=[31, 31, 31, 31, 31, 31], level=100, item=Leftovers, ability=Sturdy, moves=['spikes', 'whirlwind', 'protect', 'rest']),
> }
> ```
>
> </details>


### Stat Calculations


> ```python
> from frontierbrain3 import calc_stats, Database
> db = Database()
> snorlax = db.allSets("Snorlax")._sets[0]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> snorlax = {
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


<br>

> ```python
> calc_stats(snorlax)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'hp': 461,
>   'atk': 350,
>   'def': 229,
>   'spa': 149,
>   'spd': 256,
>   'spe': 96,
> }
> ```
>
> </details>


<br>

> ```python
> calc_stats(snorlax, ivs=15)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'hp': 445,
>   'atk': 333,
>   'def': 213,
>   'spa': 135,
>   'spd': 240,
>   'spe': 80,
> }
> ```
>
> </details>


<br>

> ```python
> calc_stats(snorlax, ivs=15, level=50)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'hp': 227,
>   'atk': 169,
>   'def': 109,
>   'spa': 69,
>   'spd': 122,
>   'spe': 42,
> }
> ```
>
> </details>


<br>

> ```python
> calc_stats(snorlax, ivs=[31,31,31,0,31,31])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'hp': 461,
>   'atk': 350,
>   'def': 229,
>   'spa': 121,
>   'spd': 256,
>   'spe': 96,
> }
> ```
>
> </details>


---

## Filtering

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
> [
>   'Magikarp-1', 'Feebas-1', 'Wooper-1', 'Lotad-1', 'Marill-1', 'Surskit-1', 'Wingull-1', 'Barboach-1', 'Spheal-1',
>   'Horsea-1', 'Poliwag-1', 'Remoraid-1', 'Shellder-1', 'Carvanha-1', 'Corphish-1', 'Mudkip-1', 'Squirtle-1',
>   'Totodile-1', 'Slowpoke-1', 'Psyduck-1', 'Goldeen-1', 'Seel-1', 'Krabby-1', 'Chinchou-1', 'Luvdisc-1', 'Tentacool-1',
>   'Staryu-1', 'Lombre-1', 'Clamperl-1', 'Omanyte-1', 'Kabuto-1', 'Corsola-1', 'Poliwhirl-1', 'Wailmer-1', 'Wartortle-1',
>   'Croconaw-1', 'Marshtomp-1', 'Azumarill-1', 'Sealeo-1', 'Qwilfish-1', 'Pelipper-1', 'Seadra-1', 'Seaking-1',
>   'Sharpedo-1', 'Mantine-1', 'Crawdaunt-1', 'Kingler-1', 'Octillery-1', 'Huntail-1', 'Gorebyss-1', 'Relicanth-1',
>   'Omastar-1', 'Kabutops-1', 'Poliwrath-1', 'Politoed-1', 'Cloyster-1', 'Wailmer-2', 'Wartortle-2', 'Croconaw-2',
>   'Marshtomp-2', 'Azumarill-2', 'Sealeo-2', 'Qwilfish-2', 'Pelipper-2', 'Seadra-2', 'Seaking-2', 'Sharpedo-2',
>   'Mantine-2', 'Crawdaunt-2', 'Kingler-2', 'Octillery-2', 'Huntail-2', 'Gorebyss-2', 'Relicanth-2', 'Omastar-2',
>   'Kabutops-2', 'Poliwrath-2', 'Politoed-2', 'Cloyster-2', 'Lanturn-1', 'Whiscash-1', 'Quagsire-1', 'Dewgong-1',
>   'Ludicolo-1', 'Slowbro-1', 'Slowking-1', 'Golduck-1', 'Wailord-1', 'Tentacruel-1', 'Starmie-1', 'Vaporeon-1',
>   'Blastoise-1', 'Feraligatr-1', 'Walrein-1', 'Lapras-1', 'Swampert-1', 'Gyarados-1', 'Kingdra-1', 'Milotic-1',
>   'Quagsire-2', 'Lanturn-2', 'Whiscash-2', 'Dewgong-2', 'Ludicolo-2', 'Slowbro-2', 'Slowking-2', 'Golduck-2',
>   'Wailord-2', 'Tentacruel-2', 'Starmie-2', 'Vaporeon-2', 'Blastoise-2', 'Feraligatr-2', 'Walrein-2', 'Lapras-2',
>   'Swampert-2', 'Gyarados-2', 'Kingdra-2', 'Milotic-2', 'Lanturn-3', 'Whiscash-3', 'Quagsire-3', 'Dewgong-3',
>   'Ludicolo-3', 'Slowbro-3', 'Slowking-3', 'Golduck-3', 'Wailord-3', 'Tentacruel-3', 'Starmie-3', 'Vaporeon-3',
>   'Blastoise-3', 'Feraligatr-3', 'Walrein-3', 'Lapras-3', 'Swampert-3', 'Gyarados-3', 'Kingdra-3', 'Milotic-3',
>   'Lanturn-4', 'Whiscash-4', 'Quagsire-4', 'Dewgong-4', 'Ludicolo-4', 'Slowbro-4', 'Slowking-4', 'Golduck-4',
>   'Wailord-4', 'Tentacruel-4', 'Starmie-4', 'Vaporeon-4', 'Blastoise-4', 'Feraligatr-4', 'Walrein-4', 'Lapras-4',
>   'Swampert-4', 'Gyarados-4', 'Kingdra-4', 'Milotic-4', 'Suicune-1', 'Suicune-2', 'Suicune-3', 'Suicune-4', 'Starmie-5',
>   'Starmie-6', 'Starmie-7', 'Starmie-8', 'Lapras-5', 'Lapras-6', 'Lapras-7', 'Lapras-8', 'Suicune-5', 'Suicune-6',
>   'Swampert-TuckerSilver', 'Swampert-TuckerGold', 'Lapras-SpenserSilver', 'Suicune-SpenserGold', 'Milotic-LucySilver',
>   'Gyarados-LucyGold'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.hasType("Psychic/")     # pure Psychic only (trailing slash)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(40 sets)
> [
>   'Ralts-1', 'Wynaut-1', 'Kirlia-1', 'Abra-1', 'Drowzee-1', 'Spoink-1', 'Unown-1', 'Kadabra-1', 'Wobbuffet-1',
>   'Chimecho-1', 'Grumpig-1', 'Kadabra-2', 'Wobbuffet-2', 'Chimecho-2', 'Grumpig-2', 'Mr. Mime-1', 'Hypno-1',
>   'Alakazam-1', 'Gardevoir-1', 'Espeon-1', 'Mr. Mime-2', 'Hypno-2', 'Alakazam-2', 'Gardevoir-2', 'Espeon-2',
>   'Mr. Mime-3', 'Hypno-3', 'Alakazam-3', 'Gardevoir-3', 'Espeon-3', 'Mr. Mime-4', 'Hypno-4', 'Alakazam-4',
>   'Gardevoir-4', 'Espeon-4', 'Gardevoir-5', 'Gardevoir-6', 'Gardevoir-7', 'Gardevoir-8', 'Alakazam-AnabelSilver'
> ]
> ```
>
> </details>


<br>

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
>   'Charizard-1', 'Charizard-2', 'Charizard-3', 'Charizard-4', 'Moltres-1', 'Moltres-2', 'Moltres-3', 'Moltres-4',
>   'Moltres-5', 'Moltres-6', 'Charizard-TuckerSilver', 'Moltres-BrandonGold'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.hasType("Water", "Ice") # Water OR Ice type
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(209 sets)
> [
>   'Magikarp-1', 'Feebas-1', 'Wooper-1', 'Lotad-1', 'Marill-1', 'Swinub-1', 'Surskit-1', 'Wingull-1', 'Barboach-1',
>   'Spheal-1', 'Horsea-1', 'Poliwag-1', 'Remoraid-1', 'Snorunt-1', 'Shellder-1', 'Smoochum-1', 'Carvanha-1',
>   'Corphish-1', 'Mudkip-1', 'Squirtle-1', 'Totodile-1', 'Slowpoke-1', 'Psyduck-1', 'Goldeen-1', 'Seel-1', 'Krabby-1',
>   'Chinchou-1', 'Delibird-1', 'Luvdisc-1', 'Tentacool-1', 'Staryu-1', 'Lombre-1', 'Clamperl-1', 'Omanyte-1', 'Kabuto-1',
>   'Corsola-1', 'Poliwhirl-1', 'Wailmer-1', 'Wartortle-1', 'Croconaw-1', 'Marshtomp-1', 'Azumarill-1', 'Sealeo-1',
>   'Qwilfish-1', 'Sneasel-1', 'Pelipper-1', 'Seadra-1', 'Seaking-1', 'Piloswine-1', 'Sharpedo-1', 'Mantine-1',
>   'Crawdaunt-1', 'Kingler-1', 'Octillery-1', 'Huntail-1', 'Gorebyss-1', 'Relicanth-1', 'Omastar-1', 'Kabutops-1',
>   'Poliwrath-1', 'Politoed-1', 'Cloyster-1', 'Wailmer-2', 'Wartortle-2', 'Croconaw-2', 'Marshtomp-2', 'Azumarill-2',
>   'Sealeo-2', 'Qwilfish-2', 'Sneasel-2', 'Pelipper-2', 'Seadra-2', 'Seaking-2', 'Piloswine-2', 'Sharpedo-2',
>   'Mantine-2', 'Crawdaunt-2', 'Kingler-2', 'Octillery-2', 'Huntail-2', 'Gorebyss-2', 'Relicanth-2', 'Omastar-2',
>   'Kabutops-2', 'Poliwrath-2', 'Politoed-2', 'Cloyster-2', 'Jynx-1', 'Lanturn-1', 'Whiscash-1', 'Quagsire-1',
>   'Dewgong-1', 'Glalie-1', 'Ludicolo-1', 'Slowbro-1', 'Slowking-1', 'Golduck-1', 'Wailord-1', 'Tentacruel-1',
>   'Starmie-1', 'Vaporeon-1', 'Blastoise-1', 'Feraligatr-1', 'Walrein-1', 'Lapras-1', 'Swampert-1', 'Gyarados-1',
>   'Kingdra-1', 'Milotic-1', 'Quagsire-2', 'Jynx-2', 'Lanturn-2', 'Whiscash-2', 'Dewgong-2', 'Glalie-2', 'Ludicolo-2',
>   'Slowbro-2', 'Slowking-2', 'Golduck-2', 'Wailord-2', 'Tentacruel-2', 'Starmie-2', 'Vaporeon-2', 'Blastoise-2',
>   'Feraligatr-2', 'Walrein-2', 'Lapras-2', 'Swampert-2', 'Gyarados-2', 'Kingdra-2', 'Milotic-2', 'Jynx-3', 'Lanturn-3',
>   'Whiscash-3', 'Quagsire-3', 'Dewgong-3', 'Glalie-3', 'Ludicolo-3', 'Slowbro-3', 'Slowking-3', 'Golduck-3',
>   'Wailord-3', 'Tentacruel-3', 'Starmie-3', 'Vaporeon-3', 'Blastoise-3', 'Feraligatr-3', 'Walrein-3', 'Lapras-3',
>   'Swampert-3', 'Gyarados-3', 'Kingdra-3', 'Milotic-3', 'Jynx-4', 'Lanturn-4', 'Whiscash-4', 'Quagsire-4', 'Dewgong-4',
>   'Glalie-4', 'Ludicolo-4', 'Slowbro-4', 'Slowking-4', 'Golduck-4', 'Wailord-4', 'Tentacruel-4', 'Starmie-4',
>   'Vaporeon-4', 'Blastoise-4', 'Feraligatr-4', 'Walrein-4', 'Lapras-4', 'Swampert-4', 'Gyarados-4', 'Kingdra-4',
>   'Milotic-4', 'Articuno-1', 'Suicune-1', 'Regice-1', 'Articuno-2', 'Suicune-2', 'Regice-2', 'Articuno-3', 'Suicune-3',
>   'Regice-3', 'Articuno-4', 'Suicune-4', 'Regice-4', 'Starmie-5', 'Starmie-6', 'Starmie-7', 'Starmie-8', 'Lapras-5',
>   'Lapras-6', 'Lapras-7', 'Lapras-8', 'Regice-5', 'Regice-6', 'Articuno-5', 'Articuno-6', 'Suicune-5', 'Suicune-6',
>   'Swampert-TuckerSilver', 'Swampert-TuckerGold', 'Lapras-SpenserSilver', 'Suicune-SpenserGold', 'Milotic-LucySilver',
>   'Gyarados-LucyGold', 'Regice-BrandonSilver', 'Articuno-BrandonGold'
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
> [
>   'Wartortle-2', 'Sealeo-2', 'Pelipper-2', 'Sharpedo-2', 'Mantine-2', 'Huntail-2', 'Gorebyss-2', 'Politoed-2',
>   'Lanturn-1', 'Ludicolo-1', 'Slowbro-1', 'Wailord-1', 'Vaporeon-1', 'Feraligatr-1', 'Lapras-1', 'Lanturn-2',
>   'Whiscash-2', 'Ludicolo-2', 'Slowbro-2', 'Slowking-2', 'Golduck-2', 'Tentacruel-2', 'Vaporeon-2', 'Feraligatr-2',
>   'Lapras-2', 'Swampert-2', 'Kingdra-2', 'Milotic-2', 'Whiscash-3', 'Slowbro-3', 'Slowking-3', 'Nidoking-3',
>   'Tentacruel-3', 'Starmie-3', 'Vaporeon-3', 'Blastoise-3', 'Aggron-3', 'Walrein-3', 'Swampert-3', 'Gyarados-3',
>   'Milotic-3', 'Lanturn-4', 'Whiscash-4', 'Quagsire-4', 'Dewgong-4', 'Tauros-4', 'Slowbro-4', 'Slowking-4', 'Golduck-4',
>   'Wailord-4', 'Vaporeon-4', 'Blastoise-4', 'Walrein-4', 'Lapras-4', 'Swampert-4', 'Milotic-4', 'Suicune-1',
>   'Suicune-3', 'Suicune-4', 'Starmie-5', 'Starmie-6', 'Starmie-8', 'Dragonite-6', 'Dragonite-7', 'Dragonite-9',
>   'Tyranitar-1', 'Suicune-5', 'Suicune-6', 'Swampert-TuckerSilver', 'Swampert-TuckerGold', 'Suicune-SpenserGold',
>   'Milotic-LucySilver'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.hasMove("earthquake", "surf")           # has EQ OR Surf (default match="any")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(222 sets)
> [
>   'Lickitung-2', 'Graveler-2', 'Wailmer-2', 'Wartortle-2', 'Marshtomp-2', 'Sudowoodo-2', 'Magcargo-2', 'Pupitar-2',
>   'Sealeo-2', 'Gligar-2', 'Pelipper-2', 'Lairon-2', 'Arbok-2', 'Solrock-2', 'Sandslash-2', 'Piloswine-2', 'Seviper-2',
>   'Camerupt-2', 'Sharpedo-2', 'Mantine-2', 'Huntail-2', 'Gorebyss-2', 'Relicanth-2', 'Politoed-2', 'Dugtrio-1',
>   'Lanturn-1', 'Whiscash-1', 'Quagsire-1', 'Ludicolo-1', 'Golem-1', 'Rhydon-1', 'Tauros-1', 'Slowbro-1', 'Donphan-1',
>   'Claydol-1', 'Wailord-1', 'Steelix-1', 'Flygon-1', 'Vaporeon-1', 'Feraligatr-1', 'Aggron-1', 'Lapras-1', 'Swampert-1',
>   'Dugtrio-2', 'Marowak-2', 'Lanturn-2', 'Forretress-2', 'Whiscash-2', 'Exploud-2', 'Ludicolo-2', 'Rhydon-2',
>   'Tauros-2', 'Slowbro-2', 'Slowking-2', 'Nidoqueen-2', 'Nidoking-2', 'Cradily-2', 'Golduck-2', 'Heracross-2',
>   'Ursaring-2', 'Donphan-2', 'Claydol-2', 'Machamp-2', 'Steelix-2', 'Tentacruel-2', 'Aerodactyl-2', 'Vaporeon-2',
>   'Feraligatr-2', 'Aggron-2', 'Walrein-2', 'Charizard-2', 'Lapras-2', 'Swampert-2', 'Snorlax-2', 'Kingdra-2',
>   'Milotic-2', 'Metagross-2', 'Dugtrio-3', 'Granbull-3', 'Dusclops-3', 'Forretress-3', 'Whiscash-3', 'Marowak-3',
>   'Quagsire-3', 'Hariyama-3', 'Glalie-3', 'Golem-3', 'Rhydon-3', 'Kangaskhan-3', 'Tauros-3', 'Slowbro-3', 'Slowking-3',
>   'Miltank-3', 'Altaria-3', 'Nidoking-3', 'Armaldo-3', 'Heracross-3', 'Donphan-3', 'Steelix-3', 'Tentacruel-3',
>   'Starmie-3', 'Flygon-3', 'Venusaur-3', 'Vaporeon-3', 'Meganium-3', 'Blastoise-3', 'Feraligatr-3', 'Aggron-3',
>   'Blaziken-3', 'Walrein-3', 'Sceptile-3', 'Typhlosion-3', 'Swampert-3', 'Gyarados-3', 'Milotic-3', 'Salamence-3',
>   'Metagross-3', 'Slaking-3', 'Dugtrio-4', 'Granbull-4', 'Lanturn-4', 'Forretress-4', 'Whiscash-4', 'Marowak-4',
>   'Quagsire-4', 'Hariyama-4', 'Dewgong-4', 'Exploud-4', 'Glalie-4', 'Golem-4', 'Rhydon-4', 'Kangaskhan-4', 'Tauros-4',
>   'Slowbro-4', 'Slowking-4', 'Altaria-4', 'Nidoqueen-4', 'Nidoking-4', 'Armaldo-4', 'Golduck-4', 'Heracross-4',
>   'Ursaring-4', 'Donphan-4', 'Claydol-4', 'Wailord-4', 'Machamp-4', 'Steelix-4', 'Aerodactyl-4', 'Flygon-4',
>   'Venusaur-4', 'Vaporeon-4', 'Meganium-4', 'Blastoise-4', 'Feraligatr-4', 'Aggron-4', 'Blaziken-4', 'Walrein-4',
>   'Charizard-4', 'Typhlosion-4', 'Lapras-4', 'Swampert-4', 'Gyarados-4', 'Milotic-4', 'Salamence-4', 'Metagross-4',
>   'Suicune-1', 'Regirock-1', 'Regirock-2', 'Registeel-2', 'Latias-2', 'Latios-2', 'Suicune-3', 'Regirock-3', 'Latias-3',
>   'Latios-3', 'Suicune-4', 'Registeel-4', 'Ursaring-7', 'Ursaring-8', 'Machamp-5', 'Machamp-6', 'Starmie-5',
>   'Starmie-6', 'Starmie-8', 'Snorlax-6', 'Snorlax-7', 'Salamence-5', 'Metagross-5', 'Metagross-7', 'Metagross-8',
>   'Regice-5', 'Latias-7', 'Latias-8', 'Latios-7', 'Latios-8', 'Dragonite-1', 'Dragonite-2', 'Dragonite-6',
>   'Dragonite-7', 'Dragonite-9', 'Dragonite-10', 'Tyranitar-1', 'Tyranitar-2', 'Tyranitar-3', 'Tyranitar-5',
>   'Tyranitar-6', 'Tyranitar-9', 'Tyranitar-10', 'Suicune-5', 'Suicune-6', 'Swampert-TuckerSilver',
>   'Salamence-TuckerSilver', 'Charizard-TuckerSilver', 'Swampert-TuckerGold', 'Metagross-TuckerGold',
>   'Slaking-SpenserSilver', 'Slaking-SpenserGold', 'Suicune-SpenserGold', 'Milotic-LucySilver', 'Steelix-LucyGold',
>   'Regirock-BrandonSilver', 'Registeel-BrandonSilver'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.hasMove("calmmind", "surf", match="all")  # has BOTH Calm Mind AND Surf
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(5 sets)
> [
>   'Slowbro-2', 'Suicune-1', 'Suicune-5', 'Suicune-6', 'Suicune-SpenserGold'
> ]
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
>   'Beldum-1', 'Furret-2', 'Linoone-2', 'Kecleon-2', 'Absol-2', 'Aerodactyl-2', 'Mr. Mime-3', 'Alakazam-3', 'Slaking-3',
>   'Granbull-4', 'Armaldo-4', 'Ursaring-5'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.hasItem("Leftovers", "Shell Bell")  # has either item
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(121 sets)
> [
>   'Slakoth-1', 'Carvanha-1', 'Staryu-1', 'Octillery-1', 'Omastar-1', 'Politoed-1', 'Wartortle-2', 'Parasect-2',
>   'Azumarill-2', 'Sunflora-2', 'Pelipper-2', 'Seadra-2', 'Chansey-2', 'Jumpluff-2', 'Piloswine-2', 'Mantine-2',
>   'Swalot-2', 'Huntail-2', 'Gorebyss-2', 'Cloyster-2', 'Jynx-1', 'Dusclops-1', 'Mr. Mime-1', 'Clefable-1', 'Ludicolo-1',
>   'Slowbro-1', 'Slowking-1', 'Cradily-1', 'Golduck-1', 'Gengar-1', 'Wailord-1', 'Porygon2-1', 'Gardevoir-1',
>   'Starmie-1', 'Blastoise-1', 'Walrein-1', 'Sceptile-1', 'Lapras-1', 'Snorlax-1', 'Metagross-1', 'Quagsire-2',
>   'Misdreavus-2', 'Dusclops-2', 'Whiscash-2', 'Xatu-2', 'Dewgong-2', 'Victreebel-2', 'Ludicolo-2', 'Electabuzz-2',
>   'Slowbro-2', 'Slowking-2', 'Miltank-2', 'Altaria-2', 'Nidoqueen-2', 'Nidoking-2', 'Rapidash-2', 'Gengar-2',
>   'Claydol-2', 'Shuckle-2', 'Steelix-2', 'Tentacruel-2', 'Starmie-2', 'Vaporeon-2', 'Meganium-2', 'Umbreon-2',
>   'Blastoise-2', 'Crobat-2', 'Gyarados-2', 'Blissey-2', 'Salamence-2', 'Slaking-2', 'Dusclops-3', 'Breloom-3',
>   'Vileplume-3', 'Glalie-3', 'Ludicolo-3', 'Tauros-3', 'Cradily-3', 'Golduck-3', 'Claydol-3', 'Shuckle-3',
>   'Tentacruel-3', 'Exeggutor-3', 'Swampert-3', 'Milotic-3', 'Quagsire-4', 'Glalie-4', 'Ludicolo-4', 'Altaria-4',
>   'Cradily-4', 'Tentacruel-4', 'Umbreon-4', 'Swampert-4', 'Milotic-4', 'Articuno-2', 'Suicune-2', 'Zapdos-3',
>   'Zapdos-4', 'Regirock-4', 'Regice-4', 'Registeel-4', 'Latias-4', 'Starmie-6', 'Lapras-5', 'Snorlax-6', 'Salamence-8',
>   'Metagross-7', 'Regice-5', 'Registeel-5', 'Latias-6', 'Latias-7', 'Latios-6', 'Dragonite-3', 'Dragonite-6',
>   'Dragonite-7', 'Dragonite-8', 'Swampert-TuckerGold', 'Umbreon-GretaSilver', 'Gengar-GretaGold', 'Milotic-LucySilver',
>   'Registeel-BrandonSilver'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.hasNature("Adamant")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(197 sets)
> [
>   'Machop-1', 'Graveler-1', 'Machoke-1', 'Linoone-1', 'Swellow-1', 'Arbok-1', 'Sandslash-1', 'Hitmonlee-1',
>   'Hitmonchan-1', 'Sharpedo-1', 'Absol-1', 'Crawdaunt-1', 'Kabutops-1', 'Poliwrath-1', 'Lickitung-2', 'Graveler-2',
>   'Machoke-2', 'Croconaw-2', 'Azumarill-2', 'Raticate-2', 'Furret-2', 'Dragonair-2', 'Gligar-2', 'Qwilfish-2',
>   'Swellow-2', 'Arbok-2', 'Vigoroth-2', 'Sandslash-2', 'Piloswine-2', 'Golbat-2', 'Hitmonlee-2', 'Hitmonchan-2',
>   'Hitmontop-2', 'Banette-2', 'Zangoose-2', 'Stantler-2', 'Absol-2', 'Swalot-2', 'Crawdaunt-2', 'Pidgeot-2',
>   'Kingler-2', 'Kabutops-2', 'Poliwrath-2', 'Scyther-2', 'Dugtrio-1', 'Fearow-1', 'Granbull-1', 'Dodrio-1',
>   'Forretress-1', 'Whiscash-1', 'Skarmory-1', 'Marowak-1', 'Quagsire-1', 'Hariyama-1', 'Golem-1', 'Rhydon-1',
>   'Weezing-1', 'Kangaskhan-1', 'Tauros-1', 'Nidoqueen-1', 'Nidoking-1', 'Armaldo-1', 'Muk-1', 'Scizor-1', 'Heracross-1',
>   'Donphan-1', 'Claydol-1', 'Machamp-1', 'Steelix-1', 'Aerodactyl-1', 'Porygon2-1', 'Flygon-1', 'Aggron-1',
>   'Swampert-1', 'Snorlax-1', 'Arcanine-1', 'Metagross-1', 'Slaking-1', 'Dugtrio-2', 'Marowak-2', 'Fearow-2', 'Dodrio-2',
>   'Mr. Mime-2', 'Forretress-2', 'Clefable-2', 'Raichu-2', 'Golem-2', 'Rhydon-2', 'Weezing-2', 'Kangaskhan-2',
>   'Tauros-2', 'Nidoqueen-2', 'Nidoking-2', 'Cradily-2', 'Armaldo-2', 'Gengar-2', 'Scizor-2', 'Ursaring-2', 'Wailord-2',
>   'Machamp-2', 'Aerodactyl-2', 'Umbreon-2', 'Aggron-2', 'Charizard-2', 'Snorlax-2', 'Metagross-2', 'Slaking-2',
>   'Dugtrio-3', 'Granbull-3', 'Dusclops-3', 'Dodrio-3', 'Breloom-3', 'Marowak-3', 'Quagsire-3', 'Hariyama-3', 'Hypno-3',
>   'Golem-3', 'Rhydon-3', 'Miltank-3', 'Altaria-3', 'Armaldo-3', 'Heracross-3', 'Donphan-3', 'Steelix-3', 'Venusaur-3',
>   'Typhlosion-3', 'Crobat-3', 'Snorlax-3', 'Kingdra-3', 'Metagross-3', 'Slaking-3', 'Dugtrio-4', 'Dusclops-4',
>   'Dodrio-4', 'Breloom-4', 'Forretress-4', 'Skarmory-4', 'Marowak-4', 'Hariyama-4', 'Golem-4', 'Rhydon-4', 'Weezing-4',
>   'Kangaskhan-4', 'Miltank-4', 'Nidoqueen-4', 'Armaldo-4', 'Heracross-4', 'Ursaring-4', 'Donphan-4', 'Claydol-4',
>   'Steelix-4', 'Aggron-4', 'Crobat-4', 'Gyarados-4', 'Snorlax-4', 'Salamence-4', 'Regirock-1', 'Registeel-1',
>   'Regirock-2', 'Regirock-3', 'Registeel-3', 'Ursaring-5', 'Ursaring-6', 'Machamp-5', 'Machamp-6', 'Machamp-7',
>   'Machamp-8', 'Snorlax-5', 'Snorlax-6', 'Snorlax-7', 'Snorlax-8', 'Salamence-5', 'Metagross-8', 'Regirock-5',
>   'Regirock-6', 'Registeel-5', 'Registeel-6', 'Latias-7', 'Latios-7', 'Dragonite-1', 'Dragonite-2', 'Dragonite-3',
>   'Dragonite-4', 'Tyranitar-3', 'Tyranitar-5', 'Tyranitar-6', 'Tyranitar-7', 'Tyranitar-8', 'Tyranitar-10',
>   'Snorlax-AnabelSilver', 'Snorlax-AnabelGold', 'Salamence-TuckerSilver', 'Crobat-SpenserSilver',
>   'Shedinja-GretaSilver', 'Gyarados-LucyGold', 'Regirock-BrandonSilver', 'Registeel-BrandonSilver'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.hasAbility("Intimidate")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(41 sets)
> [
>   'Ekans-1', 'Snubbull-1', 'Growlithe-1', 'Mawile-1', 'Masquerain-1', 'Mightyena-1', 'Arbok-1', 'Hitmontop-1',
>   'Stantler-1', 'Masquerain-2', 'Mightyena-2', 'Arbok-2', 'Hitmontop-2', 'Stantler-2', 'Granbull-1', 'Tauros-1',
>   'Gyarados-1', 'Arcanine-1', 'Salamence-1', 'Granbull-2', 'Tauros-2', 'Gyarados-2', 'Arcanine-2', 'Salamence-2',
>   'Granbull-3', 'Tauros-3', 'Gyarados-3', 'Arcanine-3', 'Salamence-3', 'Granbull-4', 'Tauros-4', 'Gyarados-4',
>   'Arcanine-4', 'Salamence-4', 'Salamence-5', 'Salamence-6', 'Salamence-7', 'Salamence-8', 'Swampert-TuckerSilver',
>   'Arcanine-SpenserGold', 'Gyarados-LucyGold'
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
> [
>   'Krabby-1', 'Hitmonlee-1', 'Zangoose-1', 'Sharpedo-1', 'Absol-1', 'Crawdaunt-1', 'Octillery-1', 'Huntail-1',
>   'Kabutops-1', 'Scyther-1', 'Pinsir-1', 'Machoke-2', 'Hitmonlee-2', 'Zangoose-2', 'Sharpedo-2', 'Stantler-2',
>   'Absol-2', 'Crawdaunt-2', 'Kingler-2', 'Kabutops-2', 'Scyther-2', 'Fearow-1', 'Granbull-1', 'Dodrio-1', 'Breloom-1',
>   'Forretress-1', 'Hariyama-1', 'Golem-1', 'Rhydon-1', 'Weezing-1', 'Kangaskhan-1', 'Tauros-1', 'Nidoking-1',
>   'Armaldo-1', 'Muk-1', 'Scizor-1', 'Heracross-1', 'Ursaring-1', 'Donphan-1', 'Machamp-1', 'Aerodactyl-1', 'Flygon-1',
>   'Aggron-1', 'Blaziken-1', 'Snorlax-1', 'Arcanine-1', 'Salamence-1', 'Metagross-1', 'Slaking-1', 'Fearow-2',
>   'Dodrio-2', 'Forretress-2', 'Hariyama-2', 'Raichu-2', 'Victreebel-2', 'Golem-2', 'Rhydon-2', 'Weezing-2',
>   'Kangaskhan-2', 'Tauros-2', 'Nidoking-2', 'Armaldo-2', 'Muk-2', 'Scizor-2', 'Ursaring-2', 'Donphan-2', 'Machamp-2',
>   'Aerodactyl-2', 'Aggron-2', 'Blaziken-2', 'Salamence-2', 'Metagross-2', 'Slaking-2', 'Granbull-3', 'Dodrio-3',
>   'Breloom-3', 'Hariyama-3', 'Victreebel-3', 'Golem-3', 'Rhydon-3', 'Armaldo-3', 'Scizor-3', 'Heracross-3', 'Donphan-3',
>   'Machamp-3', 'Aerodactyl-3', 'Flareon-3', 'Blaziken-3', 'Crobat-3', 'Swampert-3', 'Gyarados-3', 'Salamence-3',
>   'Metagross-3', 'Slaking-3', 'Granbull-4', 'Dodrio-4', 'Breloom-4', 'Forretress-4', 'Hariyama-4', 'Victreebel-4',
>   'Golem-4', 'Rhydon-4', 'Weezing-4', 'Kangaskhan-4', 'Armaldo-4', 'Muk-4', 'Heracross-4', 'Ursaring-4', 'Donphan-4',
>   'Machamp-4', 'Aerodactyl-4', 'Flareon-4', 'Aggron-4', 'Blaziken-4', 'Crobat-4', 'Swampert-4', 'Gyarados-4',
>   'Snorlax-4', 'Salamence-4', 'Metagross-4', 'Slaking-4', 'Regirock-1', 'Regirock-2', 'Entei-3', 'Ursaring-5',
>   'Ursaring-6', 'Ursaring-7', 'Ursaring-8', 'Machamp-5', 'Machamp-6', 'Machamp-7', 'Machamp-8', 'Snorlax-5',
>   'Snorlax-6', 'Salamence-5', 'Salamence-6', 'Metagross-5', 'Metagross-6', 'Metagross-7', 'Metagross-8', 'Regirock-5',
>   'Dragonite-1', 'Dragonite-2', 'Dragonite-3', 'Dragonite-4', 'Dragonite-5', 'Dragonite-9', 'Dragonite-10',
>   'Tyranitar-1', 'Tyranitar-2', 'Tyranitar-3', 'Tyranitar-5', 'Tyranitar-6', 'Tyranitar-7', 'Tyranitar-8',
>   'Tyranitar-9', 'Tyranitar-10', 'Entei-AnabelSilver', 'Snorlax-AnabelSilver', 'Snorlax-AnabelGold',
>   'Swampert-TuckerSilver', 'Salamence-TuckerSilver', 'Swampert-TuckerGold', 'Metagross-TuckerGold',
>   'Slaking-SpenserSilver', 'Arcanine-SpenserGold', 'Slaking-SpenserGold', 'Heracross-GretaSilver',
>   'Shedinja-GretaSilver', 'Breloom-GretaGold', 'Gyarados-LucyGold', 'Regirock-BrandonSilver'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.statFilter("spe", min=200, max=250)              # speed in range
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(138 sets)
> [
>   'Spearow-1', 'Taillow-1', 'Wingull-1', 'Meowth-1', 'Electrike-1', 'Vulpix-1', 'Remoraid-1', 'Doduo-1', 'Eevee-1',
>   'Voltorb-1', 'Luvdisc-1', 'Staryu-1', 'Elekid-1', 'Magby-1', 'Beedrill-1', 'Poliwhirl-1', 'Beautifly-1', 'Dustox-1',
>   'Yanma-1', 'Kadabra-1', 'Illumise-1', 'Haunter-1', 'Murkrow-1', 'Plusle-1', 'Minun-1', 'Grovyle-1', 'Ponyta-1',
>   'Pupitar-1', 'Furret-1', 'Linoone-1', 'Gligar-1', 'Qwilfish-1', 'Sneasel-1', 'Vigoroth-1', 'Primeape-1',
>   'Hitmonlee-1', 'Zangoose-1', 'Sharpedo-1', 'Magneton-1', 'Stantler-1', 'Pidgeot-1', 'Cacturne-1', 'Scyther-1',
>   'Pinsir-1', 'Delcatty-2', 'Kadabra-2', 'Haunter-2', 'Murkrow-2', 'Gligar-2', 'Qwilfish-2', 'Seadra-2', 'Vigoroth-2',
>   'Golbat-2', 'Primeape-2', 'Hitmonlee-2', 'Girafarig-2', 'Absol-2', 'Misdreavus-1', 'Jynx-1', 'Xatu-1', 'Kangaskhan-1',
>   'Electabuzz-1', 'Miltank-1', 'Nidoking-1', 'Heracross-1', 'Tentacruel-1', 'Kingdra-1', 'Metagross-1', 'Slaking-1',
>   'Misdreavus-2', 'Jynx-2', 'Mr. Mime-2', 'Breloom-2', 'Xatu-2', 'Kangaskhan-2', 'Miltank-2', 'Nidoking-2', 'Golduck-2',
>   'Donphan-2', 'Tentacruel-2', 'Lapras-2', 'Kingdra-2', 'Metagross-2', 'Slaking-2', 'Misdreavus-3', 'Jynx-3',
>   'Mr. Mime-3', 'Lanturn-3', 'Breloom-3', 'Exploud-3', 'Glalie-3', 'Miltank-3', 'Nidoking-3', 'Magmar-3', 'Golduck-3',
>   'Kingdra-3', 'Salamence-3', 'Metagross-3', 'Slaking-3', 'Fearow-4', 'Jynx-4', 'Mr. Mime-4', 'Lanturn-4', 'Breloom-4',
>   'Xatu-4', 'Raichu-4', 'Electabuzz-4', 'Miltank-4', 'Nidoking-4', 'Magmar-4', 'Tentacruel-4', 'Kingdra-4',
>   'Salamence-4', 'Slaking-4', 'Moltres-1', 'Articuno-2', 'Moltres-2', 'Suicune-2', 'Articuno-3', 'Articuno-4',
>   'Zapdos-4', 'Gardevoir-5', 'Salamence-5', 'Salamence-6', 'Metagross-5', 'Metagross-8', 'Articuno-5', 'Articuno-6',
>   'Zapdos-5', 'Moltres-6', 'Entei-5', 'Entei-6', 'Suicune-5', 'Suicune-6', 'Entei-AnabelSilver',
>   'Charizard-TuckerSilver', 'Arcanine-SpenserGold', 'Suicune-SpenserGold'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.statFilter("spa", min=150, level=50, ivs=15)     # lv50, 15 IVs
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(116 sets)
> [
>   'Magneton-1', 'Gorebyss-1', 'Omastar-1', 'Jynx-1', 'Manectric-1', 'Alakazam-1', 'Golduck-1', 'Gengar-1', 'Ampharos-1',
>   'Exeggutor-1', 'Starmie-1', 'Venusaur-1', 'Vaporeon-1', 'Jolteon-1', 'Flareon-1', 'Espeon-1', 'Blaziken-1',
>   'Sceptile-1', 'Charizard-1', 'Typhlosion-1', 'Kingdra-1', 'Manectric-2', 'Alakazam-2', 'Slowking-2', 'Magmar-2',
>   'Ampharos-2', 'Houndoom-2', 'Porygon2-2', 'Gardevoir-2', 'Jolteon-2', 'Blaziken-2', 'Sceptile-2', 'Milotic-2',
>   'Mr. Mime-3', 'Alakazam-3', 'Slowbro-3', 'Gengar-3', 'Ampharos-3', 'Porygon2-3', 'Gardevoir-3', 'Starmie-3',
>   'Espeon-3', 'Charizard-3', 'Arcanine-3', 'Salamence-3', 'Jynx-4', 'Mr. Mime-4', 'Manectric-4', 'Vileplume-4',
>   'Alakazam-4', 'Slowking-4', 'Gengar-4', 'Ampharos-4', 'Houndoom-4', 'Porygon2-4', 'Gardevoir-4', 'Exeggutor-4',
>   'Starmie-4', 'Jolteon-4', 'Flareon-4', 'Espeon-4', 'Blaziken-4', 'Walrein-4', 'Sceptile-4', 'Slaking-4', 'Articuno-1',
>   'Zapdos-1', 'Moltres-1', 'Raikou-1', 'Regice-1', 'Latias-1', 'Latios-1', 'Moltres-2', 'Raikou-2', 'Regice-2',
>   'Latias-2', 'Latios-2', 'Zapdos-3', 'Moltres-3', 'Raikou-3', 'Regice-3', 'Latias-3', 'Latios-3', 'Zapdos-4',
>   'Moltres-4', 'Raikou-4', 'Latios-4', 'Gengar-5', 'Gengar-6', 'Gengar-7', 'Gengar-8', 'Gardevoir-8', 'Starmie-5',
>   'Starmie-7', 'Starmie-8', 'Salamence-7', 'Salamence-8', 'Regice-6', 'Latias-6', 'Latios-5', 'Latios-6', 'Latios-8',
>   'Dragonite-6', 'Dragonite-7', 'Dragonite-8', 'Tyranitar-4', 'Zapdos-5', 'Zapdos-6', 'Moltres-5', 'Moltres-6',
>   'Raikou-5', 'Alakazam-AnabelSilver', 'Latios-AnabelGold', 'Gengar-GretaGold', 'Zapdos-BrandonGold',
>   'Moltres-BrandonGold'
> ]
> ```
>
> </details>


#### Speed Comparisons

Compare frontier sets against a `CustomSet` benchmark:


> ```python
> from frontierbrain3 import CustomSet
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


<br>

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
>   'Ninjask-1', 'Sneasel-2', 'Ninjask-2', 'Dugtrio-1', 'Aerodactyl-1', 'Jolteon-1', 'Sceptile-1', 'Dugtrio-2',
>   'Aerodactyl-2', 'Sceptile-2', 'Dugtrio-3', 'Starmie-3', 'Crobat-3', 'Dugtrio-4', 'Starmie-4', 'Jolteon-4',
>   'Sceptile-4', 'Crobat-4', 'Raikou-1', 'Raikou-2', 'Raikou-3', 'Raikou-4', 'Starmie-5', 'Starmie-7', 'Starmie-8',
>   'Raikou-5', 'Crobat-SpenserSilver'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.slowerThan(my_flygon)                # sets it outspeeds
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(890 sets)
> [
>   'Sunkern-1', 'Azurill-1', 'Caterpie-1', 'Weedle-1', 'Wurmple-1', 'Ralts-1', 'Magikarp-1', 'Feebas-1', 'Metapod-1',
>   'Kakuna-1', 'Pichu-1', 'Silcoon-1', 'Cascoon-1', 'Igglybuff-1', 'Wooper-1', 'Tyrogue-1', 'Sentret-1', 'Cleffa-1',
>   'Seedot-1', 'Lotad-1', 'Poochyena-1', 'Shedinja-1', 'Makuhita-1', 'Whismur-1', 'Zigzagoon-1', 'Zubat-1', 'Togepi-1',
>   'Spinarak-1', 'Marill-1', 'Hoppip-1', 'Slugma-1', 'Swinub-1', 'Smeargle-1', 'Pidgey-1', 'Rattata-1', 'Wynaut-1',
>   'Skitty-1', 'Spearow-1', 'Hoothoot-1', 'Diglett-1', 'Ledyba-1', 'Nincada-1', 'Surskit-1', 'Jigglypuff-1', 'Taillow-1',
>   'Wingull-1', 'NidoranM-1', 'NidoranF-1', 'Kirlia-1', 'Mareep-1', 'Meditite-1', 'Slakoth-1', 'Paras-1', 'Ekans-1',
>   'Ditto-1', 'Barboach-1', 'Meowth-1', 'Pineco-1', 'Trapinch-1', 'Spheal-1', 'Horsea-1', 'Shroomish-1', 'Shuppet-1',
>   'Duskull-1', 'Electrike-1', 'Vulpix-1', 'Pikachu-1', 'Sandshrew-1', 'Poliwag-1', 'Bellsprout-1', 'Geodude-1',
>   'Dratini-1', 'Snubbull-1', 'Remoraid-1', 'Larvitar-1', 'Baltoy-1', 'Snorunt-1', 'Bagon-1', 'Beldum-1', 'Gulpin-1',
>   'Venonat-1', 'Mankey-1', 'Machop-1', 'Shellder-1', 'Smoochum-1', 'Numel-1', 'Carvanha-1', 'Corphish-1',
>   'Charmander-1', 'Cyndaquil-1', 'Abra-1', 'Doduo-1', 'Gastly-1', 'Swablu-1', 'Treecko-1', 'Torchic-1', 'Mudkip-1',
>   'Squirtle-1', 'Totodile-1', 'Slowpoke-1', 'Bulbasaur-1', 'Chikorita-1', 'Oddish-1', 'Psyduck-1', 'Cubone-1',
>   'Goldeen-1', 'Natu-1', 'Clefairy-1', 'Magnemite-1', 'Seel-1', 'Grimer-1', 'Krabby-1', 'Exeggcute-1', 'Eevee-1',
>   'Drowzee-1', 'Voltorb-1', 'Chinchou-1', 'Teddiursa-1', 'Delibird-1', 'Houndour-1', 'Phanpy-1', 'Spoink-1', 'Aron-1',
>   'Luvdisc-1', 'Tentacool-1', 'Cacnea-1', 'Unown-1', 'Koffing-1', 'Staryu-1', 'Skiploom-1', 'Nuzleaf-1', 'Lombre-1',
>   'Vibrava-1', 'Rhyhorn-1', 'Clamperl-1', 'Pidgeotto-1', 'Growlithe-1', "Farfetch'd-1", 'Omanyte-1', 'Kabuto-1',
>   'Lileep-1', 'Anorith-1', 'Aipom-1', 'Elekid-1', 'Loudred-1', 'Spinda-1', 'Nidorina-1', 'Nidorino-1', 'Flaaffy-1',
>   'Magby-1', 'Nosepass-1', 'Corsola-1', 'Mawile-1', 'Butterfree-1', 'Beedrill-1', 'Poliwhirl-1', 'Onix-1',
>   'Beautifly-1', 'Dustox-1', 'Ledian-1', 'Ariados-1', 'Yanma-1', 'Delcatty-1', 'Sableye-1', 'Lickitung-1',
>   'Weepinbell-1', 'Graveler-1', 'Gloom-1', 'Porygon-1', 'Kadabra-1', 'Wailmer-1', 'Roselia-1', 'Volbeat-1',
>   'Illumise-1', 'Ivysaur-1', 'Charmeleon-1', 'Wartortle-1', 'Parasect-1', 'Machoke-1', 'Haunter-1', 'Bayleef-1',
>   'Quilava-1', 'Croconaw-1', 'Togetic-1', 'Murkrow-1', 'Wobbuffet-1', 'Plusle-1', 'Minun-1', 'Grovyle-1', 'Combusken-1',
>   'Marshtomp-1', 'Ponyta-1', 'Azumarill-1', 'Sudowoodo-1', 'Magcargo-1', 'Pupitar-1', 'Sealeo-1', 'Raticate-1',
>   'Masquerain-1', 'Furret-1', 'Dunsparce-1', 'Dragonair-1', 'Mightyena-1', 'Linoone-1', 'Castform-1', 'Shelgon-1',
>   'Metang-1', 'Wigglytuff-1', 'Sunflora-1', 'Chimecho-1', 'Gligar-1', 'Qwilfish-1', 'Sneasel-1', 'Pelipper-1',
>   'Swellow-1', 'Lairon-1', 'Tangela-1', 'Arbok-1', 'Persian-1', 'Seadra-1', 'Kecleon-1', 'Vigoroth-1', 'Lunatone-1',
>   'Solrock-1', 'Noctowl-1', 'Sandslash-1', 'Venomoth-1', 'Chansey-1', 'Seaking-1', 'Jumpluff-1', 'Piloswine-1',
>   'Golbat-1', 'Primeape-1', 'Hitmonlee-1', 'Hitmonchan-1', 'Girafarig-1', 'Hitmontop-1', 'Banette-1', 'Seviper-1',
>   'Zangoose-1', 'Camerupt-1', 'Sharpedo-1', 'Tropius-1', 'Magneton-1', 'Mantine-1', 'Stantler-1', 'Absol-1', 'Swalot-1',
>   'Crawdaunt-1', 'Pidgeot-1', 'Grumpig-1', 'Torkoal-1', 'Kingler-1', 'Cacturne-1', 'Bellossom-1', 'Octillery-1',
>   'Huntail-1', 'Gorebyss-1', 'Relicanth-1', 'Omastar-1', 'Kabutops-1', 'Poliwrath-1', 'Scyther-1', 'Pinsir-1',
>   'Politoed-1', 'Cloyster-1', 'Delcatty-2', 'Sableye-2', 'Lickitung-2', 'Weepinbell-2', 'Graveler-2', 'Gloom-2',
>   'Porygon-2', 'Kadabra-2', 'Wailmer-2', 'Roselia-2', 'Volbeat-2', 'Illumise-2', 'Ivysaur-2', 'Charmeleon-2',
>   'Wartortle-2', 'Parasect-2', 'Machoke-2', 'Haunter-2', 'Bayleef-2', 'Quilava-2', 'Croconaw-2', 'Togetic-2',
>   'Murkrow-2', 'Wobbuffet-2', 'Plusle-2', 'Minun-2', 'Grovyle-2', 'Combusken-2', 'Marshtomp-2', 'Ponyta-2',
>   'Azumarill-2', 'Sudowoodo-2', 'Magcargo-2', 'Pupitar-2', 'Sealeo-2', 'Raticate-2', 'Masquerain-2', 'Furret-2',
>   'Dunsparce-2', 'Dragonair-2', 'Mightyena-2', 'Castform-2', 'Shelgon-2', 'Metang-2', 'Wigglytuff-2', 'Sunflora-2',
>   'Chimecho-2', 'Gligar-2', 'Qwilfish-2', 'Pelipper-2', 'Swellow-2', 'Lairon-2', 'Tangela-2', 'Arbok-2', 'Persian-2',
>   'Seadra-2', 'Kecleon-2', 'Vigoroth-2', 'Lunatone-2', 'Solrock-2', 'Noctowl-2', 'Sandslash-2', 'Venomoth-2',
>   'Chansey-2', 'Seaking-2', 'Jumpluff-2', 'Piloswine-2', 'Golbat-2', 'Primeape-2', 'Hitmonlee-2', 'Hitmonchan-2',
>   'Girafarig-2', 'Hitmontop-2', 'Banette-2', 'Seviper-2', 'Zangoose-2', 'Camerupt-2', 'Sharpedo-2', 'Tropius-2',
>   'Magneton-2', 'Mantine-2', 'Stantler-2', 'Absol-2', 'Swalot-2', 'Crawdaunt-2', 'Pidgeot-2', 'Grumpig-2', 'Torkoal-2',
>   'Kingler-2', 'Cacturne-2', 'Bellossom-2', 'Octillery-2', 'Huntail-2', 'Gorebyss-2', 'Relicanth-2', 'Omastar-2',
>   'Kabutops-2', 'Poliwrath-2', 'Scyther-2', 'Pinsir-2', 'Politoed-2', 'Cloyster-2', 'Medicham-1', 'Misdreavus-1',
>   'Fearow-1', 'Granbull-1', 'Jynx-1', 'Dusclops-1', 'Dodrio-1', 'Mr. Mime-1', 'Lanturn-1', 'Breloom-1', 'Forretress-1',
>   'Whiscash-1', 'Xatu-1', 'Skarmory-1', 'Marowak-1', 'Quagsire-1', 'Clefable-1', 'Hariyama-1', 'Raichu-1', 'Dewgong-1',
>   'Manectric-1', 'Vileplume-1', 'Victreebel-1', 'Electrode-1', 'Exploud-1', 'Shiftry-1', 'Glalie-1', 'Ludicolo-1',
>   'Hypno-1', 'Golem-1', 'Rhydon-1', 'Alakazam-1', 'Weezing-1', 'Kangaskhan-1', 'Electabuzz-1', 'Tauros-1', 'Slowbro-1',
>   'Slowking-1', 'Miltank-1', 'Altaria-1', 'Nidoqueen-1', 'Nidoking-1', 'Magmar-1', 'Cradily-1', 'Armaldo-1',
>   'Golduck-1', 'Rapidash-1', 'Muk-1', 'Gengar-1', 'Ampharos-1', 'Scizor-1', 'Heracross-1', 'Ursaring-1', 'Houndoom-1',
>   'Donphan-1', 'Claydol-1', 'Wailord-1', 'Ninetales-1', 'Machamp-1', 'Shuckle-1', 'Steelix-1', 'Tentacruel-1',
>   'Porygon2-1', 'Gardevoir-1', 'Exeggutor-1', 'Starmie-1', 'Flygon-1', 'Venusaur-1', 'Vaporeon-1', 'Flareon-1',
>   'Meganium-1', 'Espeon-1', 'Umbreon-1', 'Blastoise-1', 'Feraligatr-1', 'Aggron-1', 'Blaziken-1', 'Walrein-1',
>   'Charizard-1', 'Typhlosion-1', 'Lapras-1', 'Crobat-1', 'Swampert-1', 'Gyarados-1', 'Snorlax-1', 'Kingdra-1',
>   'Blissey-1', 'Milotic-1', 'Arcanine-1', 'Salamence-1', 'Metagross-1', 'Slaking-1', 'Medicham-2', 'Marowak-2',
>   'Quagsire-2', 'Misdreavus-2', 'Fearow-2', 'Granbull-2', 'Jynx-2', 'Dusclops-2', 'Dodrio-2', 'Mr. Mime-2', 'Lanturn-2',
>   'Breloom-2', 'Forretress-2', 'Skarmory-2', 'Whiscash-2', 'Xatu-2', 'Clefable-2', 'Hariyama-2', 'Raichu-2',
>   'Dewgong-2', 'Manectric-2', 'Vileplume-2', 'Victreebel-2', 'Electrode-2', 'Exploud-2', 'Shiftry-2', 'Glalie-2',
>   'Ludicolo-2', 'Hypno-2', 'Golem-2', 'Rhydon-2', 'Alakazam-2', 'Weezing-2', 'Kangaskhan-2', 'Electabuzz-2', 'Tauros-2',
>   'Slowbro-2', 'Slowking-2', 'Miltank-2', 'Altaria-2', 'Nidoqueen-2', 'Nidoking-2', 'Magmar-2', 'Cradily-2',
>   'Armaldo-2', 'Golduck-2', 'Rapidash-2', 'Muk-2', 'Gengar-2', 'Ampharos-2', 'Scizor-2', 'Heracross-2', 'Ursaring-2',
>   'Houndoom-2', 'Donphan-2', 'Claydol-2', 'Wailord-2', 'Ninetales-2', 'Machamp-2', 'Shuckle-2', 'Steelix-2',
>   'Tentacruel-2', 'Porygon2-2', 'Gardevoir-2', 'Exeggutor-2', 'Starmie-2', 'Flygon-2', 'Venusaur-2', 'Vaporeon-2',
>   'Jolteon-2', 'Flareon-2', 'Meganium-2', 'Espeon-2', 'Umbreon-2', 'Blastoise-2', 'Feraligatr-2', 'Aggron-2',
>   'Blaziken-2', 'Walrein-2', 'Charizard-2', 'Typhlosion-2', 'Lapras-2', 'Crobat-2', 'Swampert-2', 'Gyarados-2',
>   'Snorlax-2', 'Kingdra-2', 'Blissey-2', 'Milotic-2', 'Arcanine-2', 'Salamence-2', 'Metagross-2', 'Slaking-2',
>   'Medicham-3', 'Misdreavus-3', 'Fearow-3', 'Granbull-3', 'Jynx-3', 'Dusclops-3', 'Dodrio-3', 'Mr. Mime-3', 'Lanturn-3',
>   'Breloom-3', 'Forretress-3', 'Whiscash-3', 'Xatu-3', 'Skarmory-3', 'Marowak-3', 'Quagsire-3', 'Clefable-3',
>   'Hariyama-3', 'Raichu-3', 'Dewgong-3', 'Manectric-3', 'Vileplume-3', 'Victreebel-3', 'Electrode-3', 'Exploud-3',
>   'Shiftry-3', 'Glalie-3', 'Ludicolo-3', 'Hypno-3', 'Golem-3', 'Rhydon-3', 'Alakazam-3', 'Weezing-3', 'Kangaskhan-3',
>   'Electabuzz-3', 'Tauros-3', 'Slowbro-3', 'Slowking-3', 'Miltank-3', 'Altaria-3', 'Nidoqueen-3', 'Nidoking-3',
>   'Magmar-3', 'Cradily-3', 'Armaldo-3', 'Golduck-3', 'Rapidash-3', 'Muk-3', 'Gengar-3', 'Ampharos-3', 'Scizor-3',
>   'Heracross-3', 'Ursaring-3', 'Houndoom-3', 'Donphan-3', 'Claydol-3', 'Wailord-3', 'Ninetales-3', 'Machamp-3',
>   'Shuckle-3', 'Steelix-3', 'Tentacruel-3', 'Aerodactyl-3', 'Porygon2-3', 'Gardevoir-3', 'Exeggutor-3', 'Flygon-3',
>   'Venusaur-3', 'Vaporeon-3', 'Jolteon-3', 'Flareon-3', 'Meganium-3', 'Espeon-3', 'Umbreon-3', 'Blastoise-3',
>   'Feraligatr-3', 'Aggron-3', 'Blaziken-3', 'Walrein-3', 'Sceptile-3', 'Charizard-3', 'Typhlosion-3', 'Lapras-3',
>   'Swampert-3', 'Gyarados-3', 'Snorlax-3', 'Kingdra-3', 'Blissey-3', 'Milotic-3', 'Arcanine-3', 'Salamence-3',
>   'Metagross-3', 'Slaking-3', 'Medicham-4', 'Misdreavus-4', 'Fearow-4', 'Granbull-4', 'Jynx-4', 'Dusclops-4',
>   'Dodrio-4', 'Mr. Mime-4', 'Lanturn-4', 'Breloom-4', 'Forretress-4', 'Whiscash-4', 'Xatu-4', 'Skarmory-4', 'Marowak-4',
>   'Quagsire-4', 'Clefable-4', 'Hariyama-4', 'Raichu-4', 'Dewgong-4', 'Manectric-4', 'Vileplume-4', 'Victreebel-4',
>   'Electrode-4', 'Exploud-4', 'Shiftry-4', 'Glalie-4', 'Ludicolo-4', 'Hypno-4', 'Golem-4', 'Rhydon-4', 'Alakazam-4',
>   'Weezing-4', 'Kangaskhan-4', 'Electabuzz-4', 'Tauros-4', 'Slowbro-4', 'Slowking-4', 'Miltank-4', 'Altaria-4',
>   'Nidoqueen-4', 'Nidoking-4', 'Magmar-4', 'Cradily-4', 'Armaldo-4', 'Golduck-4', 'Rapidash-4', 'Muk-4', 'Gengar-4',
>   'Ampharos-4', 'Scizor-4', 'Heracross-4', 'Ursaring-4', 'Houndoom-4', 'Donphan-4', 'Claydol-4', 'Wailord-4',
>   'Ninetales-4', 'Machamp-4', 'Shuckle-4', 'Steelix-4', 'Tentacruel-4', 'Aerodactyl-4', 'Porygon2-4', 'Gardevoir-4',
>   'Exeggutor-4', 'Flygon-4', 'Venusaur-4', 'Vaporeon-4', 'Flareon-4', 'Meganium-4', 'Espeon-4', 'Umbreon-4',
>   'Blastoise-4', 'Feraligatr-4', 'Aggron-4', 'Blaziken-4', 'Walrein-4', 'Charizard-4', 'Typhlosion-4', 'Lapras-4',
>   'Swampert-4', 'Gyarados-4', 'Snorlax-4', 'Kingdra-4', 'Blissey-4', 'Milotic-4', 'Arcanine-4', 'Salamence-4',
>   'Metagross-4', 'Slaking-4', 'Articuno-1', 'Zapdos-1', 'Moltres-1', 'Entei-1', 'Suicune-1', 'Regirock-1', 'Regice-1',
>   'Registeel-1', 'Latias-1', 'Latios-1', 'Articuno-2', 'Zapdos-2', 'Moltres-2', 'Entei-2', 'Suicune-2', 'Regirock-2',
>   'Regice-2', 'Registeel-2', 'Latias-2', 'Latios-2', 'Articuno-3', 'Zapdos-3', 'Moltres-3', 'Entei-3', 'Suicune-3',
>   'Regirock-3', 'Regice-3', 'Registeel-3', 'Latias-3', 'Latios-3', 'Articuno-4', 'Zapdos-4', 'Moltres-4', 'Entei-4',
>   'Suicune-4', 'Regirock-4', 'Regice-4', 'Registeel-4', 'Latias-4', 'Latios-4', 'Gengar-5', 'Gengar-6', 'Gengar-7',
>   'Gengar-8', 'Ursaring-5', 'Ursaring-6', 'Ursaring-7', 'Ursaring-8', 'Machamp-5', 'Machamp-6', 'Machamp-7',
>   'Machamp-8', 'Gardevoir-5', 'Gardevoir-6', 'Gardevoir-7', 'Gardevoir-8', 'Starmie-6', 'Lapras-5', 'Lapras-6',
>   'Lapras-7', 'Lapras-8', 'Snorlax-5', 'Snorlax-6', 'Snorlax-7', 'Snorlax-8', 'Salamence-5', 'Salamence-6',
>   'Salamence-7', 'Salamence-8', 'Metagross-5', 'Metagross-6', 'Metagross-7', 'Metagross-8', 'Regirock-5', 'Regirock-6',
>   'Regice-5', 'Regice-6', 'Registeel-5', 'Registeel-6', 'Latias-5', 'Latias-6', 'Latias-7', 'Latias-8', 'Latios-5',
>   'Latios-6', 'Latios-7', 'Latios-8', 'Dragonite-1', 'Dragonite-2', 'Dragonite-3', 'Dragonite-4', 'Dragonite-5',
>   'Dragonite-6', 'Dragonite-7', 'Dragonite-8', 'Dragonite-9', 'Dragonite-10', 'Tyranitar-1', 'Tyranitar-2',
>   'Tyranitar-3', 'Tyranitar-4', 'Tyranitar-5', 'Tyranitar-6', 'Tyranitar-7', 'Tyranitar-8', 'Tyranitar-9',
>   'Tyranitar-10', 'Articuno-5', 'Articuno-6', 'Zapdos-5', 'Zapdos-6', 'Moltres-5', 'Moltres-6', 'Raikou-6', 'Entei-5',
>   'Entei-6', 'Suicune-5', 'Suicune-6', 'Alakazam-AnabelSilver', 'Entei-AnabelSilver', 'Snorlax-AnabelSilver',
>   'Raikou-AnabelGold', 'Latios-AnabelGold', 'Snorlax-AnabelGold', 'Swampert-TuckerSilver', 'Salamence-TuckerSilver',
>   'Charizard-TuckerSilver', 'Swampert-TuckerGold', 'Metagross-TuckerGold', 'Latias-TuckerGold', 'Slaking-SpenserSilver',
>   'Lapras-SpenserSilver', 'Arcanine-SpenserGold', 'Slaking-SpenserGold', 'Suicune-SpenserGold', 'Heracross-GretaSilver',
>   'Umbreon-GretaSilver', 'Shedinja-GretaSilver', 'Umbreon-GretaGold', 'Gengar-GretaGold', 'Breloom-GretaGold',
>   'Seviper-LucySilver', 'Shuckle-LucySilver', 'Milotic-LucySilver', 'Seviper-LucyGold', 'Steelix-LucyGold',
>   'Gyarados-LucyGold', 'Regirock-BrandonSilver', 'Registeel-BrandonSilver', 'Regice-BrandonSilver',
>   'Articuno-BrandonGold', 'Zapdos-BrandonGold', 'Moltres-BrandonGold'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.speedTieWith(my_flygon)              # exact ties
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(1 sets)
> [
>   'Linoone-2'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.fasterThan(my_flygon, ivs=15)        # enemy sets at 15 IVs
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(6 sets)
> [
>   'Ninjask-1', 'Ninjask-2', 'Jolteon-1', 'Crobat-3', 'Jolteon-4', 'Crobat-4'
> ]
> ```
>
> </details>


#### OHKO Filters

These run the full damage calculator for every set in the collection. The attacker/defender can be a frontier set dict or a `CustomSet`.

- `willOHKO(target)`: sets whose best move guarantees the KO (even the minimum damage roll kills)
- `canOHKO(target)`: sets whose best move has any chance to KO (the maximum damage roll kills)
- `willDieTo(attacker)`: sets that the attacker guarantees to KO (each set is the defender)
- `canDieTo(attacker)`: sets that the attacker can KO on at least one roll
- `min_chance=X`: minimum probability (0.0-1.0) that a random roll KOs. Only applies to `canOHKO` and `canDieTo`. Setting `min_chance=0` has no effect (equivalent to omitting it), and `min_chance=1.0` is equivalent to `willOHKO`/`willDieTo`.
- `include_acc=True`: factors move accuracy into all probability calcs, including Brightpowder/Lax Incense on the defender. When combined with `min_chance`, both accuracy and damage roll probability are multiplied together (e.g. a 50% OHKO chance on an 80% accuracy move gives 40% total).
- `include_ohko=True`: allows one-hit KO moves (Guillotine, Fissure, Horn Drill, Sheer Cold) to count


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


<br>

> ```python
> db.sets.willOHKO(lax)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(18 sets)
> [
>   'Breloom-3', 'Shiftry-3', 'Golem-3', 'Steelix-3', 'Breloom-4', 'Forretress-4', 'Shiftry-4', 'Golem-4', 'Weezing-4',
>   'Muk-4', 'Steelix-4', 'Regirock-1', 'Regirock-2', 'Machamp-7', 'Metagross-5', 'Metagross-8', 'Breloom-GretaGold',
>   'Regirock-BrandonSilver'
> ]
> ```
>
> </details>


<br>

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
>   'Breloom-2', 'Glalie-2', 'Breloom-3', 'Forretress-3', 'Shiftry-3', 'Golem-3', 'Weezing-3', 'Steelix-3', 'Breloom-4',
>   'Forretress-4', 'Shiftry-4', 'Golem-4', 'Weezing-4', 'Muk-4', 'Claydol-4', 'Steelix-4', 'Exeggutor-4', 'Regirock-1',
>   'Regirock-2', 'Machamp-7', 'Metagross-5', 'Metagross-8', 'Regirock-6', 'Breloom-GretaGold', 'Regirock-BrandonSilver'
> ]
> ```
>
> </details>


<br>

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
>   'Breloom-3', 'Shiftry-3', 'Golem-3', 'Weezing-3', 'Steelix-3', 'Breloom-4', 'Forretress-4', 'Shiftry-4', 'Golem-4',
>   'Weezing-4', 'Muk-4', 'Steelix-4', 'Exeggutor-4', 'Regirock-1', 'Regirock-2', 'Machamp-7', 'Metagross-5',
>   'Metagross-8', 'Breloom-GretaGold', 'Regirock-BrandonSilver'
> ]
> ```
>
> </details>


Specify IVs for the attacker and defender independently, useful for analyzing player sets (31 IVs) against frontier enemies (3-31 IVs depending on tier):


> ```python
> db.sets.willDieTo(lax, atk_ivs=31, def_ivs=3)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(117 sets)
> [
>   'Sunkern-1', 'Azurill-1', 'Caterpie-1', 'Weedle-1', 'Wurmple-1', 'Ralts-1', 'Magikarp-1', 'Feebas-1', 'Pichu-1',
>   'Igglybuff-1', 'Tyrogue-1', 'Sentret-1', 'Cleffa-1', 'Lotad-1', 'Poochyena-1', 'Shedinja-1', 'Makuhita-1',
>   'Whismur-1', 'Zigzagoon-1', 'Zubat-1', 'Spinarak-1', 'Swinub-1', 'Smeargle-1', 'Pidgey-1', 'Rattata-1', 'Spearow-1',
>   'Hoothoot-1', 'Diglett-1', 'Ledyba-1', 'Surskit-1', 'Taillow-1', 'Wingull-1', 'NidoranM-1', 'Kirlia-1', 'Meditite-1',
>   'Ekans-1', 'Barboach-1', 'Meowth-1', 'Trapinch-1', 'Shuppet-1', 'Electrike-1', 'Vulpix-1', 'Pikachu-1', 'Poliwag-1',
>   'Dratini-1', 'Remoraid-1', 'Baltoy-1', 'Mankey-1', 'Smoochum-1', 'Numel-1', 'Carvanha-1', 'Charmander-1',
>   'Cyndaquil-1', 'Abra-1', 'Doduo-1', 'Gastly-1', 'Treecko-1', 'Torchic-1', 'Psyduck-1', 'Natu-1', 'Drowzee-1',
>   'Chinchou-1', 'Delibird-1', 'Houndour-1', 'Spoink-1', 'Tentacool-1', 'Cacnea-1', 'Unown-1', 'Elekid-1', 'Magby-1',
>   'Beedrill-1', 'Ledian-1', 'Kadabra-1', 'Haunter-1', 'Sharpedo-1', 'Kadabra-2', 'Haunter-2', 'Plusle-2', 'Minun-2',
>   'Grovyle-2', 'Ponyta-2', 'Sharpedo-2', 'Dugtrio-1', 'Medicham-1', 'Jynx-1', 'Alakazam-1', 'Gengar-1', 'Dugtrio-2',
>   'Medicham-2', 'Alakazam-2', 'Gengar-2', 'Espeon-2', 'Dugtrio-3', 'Medicham-3', 'Mr. Mime-3', 'Xatu-3', 'Alakazam-3',
>   'Gengar-3', 'Gardevoir-3', 'Espeon-3', 'Dugtrio-4', 'Medicham-4', 'Misdreavus-4', 'Jynx-4', 'Mr. Mime-4', 'Xatu-4',
>   'Alakazam-4', 'Gengar-4', 'Gardevoir-4', 'Espeon-4', 'Gengar-5', 'Gengar-6', 'Gengar-7', 'Gengar-8', 'Gardevoir-8',
>   'Alakazam-AnabelSilver', 'Shedinja-GretaSilver'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.hasType("Normal").canDieTo(lax)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(11 sets)
> [
>   'Igglybuff-1', 'Sentret-1', 'Cleffa-1', 'Whismur-1', 'Pidgey-1', 'Rattata-1', 'Spearow-1', 'Hoothoot-1', 'Taillow-1',
>   'Meowth-1', 'Doduo-1'
> ]
> ```
>
> </details>


Other optional parameters are passed through to the damage calculator:


> ```python
> from frontierbrain3 import Field
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


<br>

> ```python
> db.sets.willDieTo(meta, atk_boosts={"atk": 1})
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(335 sets)
> [
>   'Sunkern-1', 'Azurill-1', 'Caterpie-1', 'Weedle-1', 'Wurmple-1', 'Ralts-1', 'Feebas-1', 'Metapod-1', 'Kakuna-1',
>   'Pichu-1', 'Silcoon-1', 'Cascoon-1', 'Igglybuff-1', 'Tyrogue-1', 'Sentret-1', 'Cleffa-1', 'Seedot-1', 'Lotad-1',
>   'Poochyena-1', 'Shedinja-1', 'Makuhita-1', 'Whismur-1', 'Zigzagoon-1', 'Zubat-1', 'Togepi-1', 'Spinarak-1',
>   'Hoppip-1', 'Swinub-1', 'Smeargle-1', 'Pidgey-1', 'Rattata-1', 'Skitty-1', 'Spearow-1', 'Hoothoot-1', 'Diglett-1',
>   'Ledyba-1', 'Nincada-1', 'Surskit-1', 'Jigglypuff-1', 'Taillow-1', 'Wingull-1', 'NidoranM-1', 'NidoranF-1',
>   'Kirlia-1', 'Meditite-1', 'Slakoth-1', 'Paras-1', 'Ekans-1', 'Barboach-1', 'Meowth-1', 'Trapinch-1', 'Spheal-1',
>   'Shroomish-1', 'Shuppet-1', 'Duskull-1', 'Pikachu-1', 'Bellsprout-1', 'Geodude-1', 'Dratini-1', 'Snubbull-1',
>   'Remoraid-1', 'Larvitar-1', 'Baltoy-1', 'Snorunt-1', 'Bagon-1', 'Gulpin-1', 'Venonat-1', 'Mankey-1', 'Machop-1',
>   'Smoochum-1', 'Carvanha-1', 'Abra-1', 'Doduo-1', 'Gastly-1', 'Swablu-1', 'Treecko-1', 'Torchic-1', 'Bulbasaur-1',
>   'Chikorita-1', 'Oddish-1', 'Psyduck-1', 'Natu-1', 'Clefairy-1', 'Grimer-1', 'Eevee-1', 'Drowzee-1', 'Teddiursa-1',
>   'Delibird-1', 'Houndour-1', 'Phanpy-1', 'Spoink-1', 'Tentacool-1', 'Cacnea-1', 'Unown-1', 'Skiploom-1', 'Nuzleaf-1',
>   'Lombre-1', 'Vibrava-1', 'Rhyhorn-1', 'Pidgeotto-1', "Farfetch'd-1", 'Omanyte-1', 'Kabuto-1', 'Lileep-1', 'Anorith-1',
>   'Aipom-1', 'Loudred-1', 'Spinda-1', 'Nidorina-1', 'Nidorino-1', 'Nosepass-1', 'Butterfree-1', 'Beedrill-1', 'Onix-1',
>   'Beautifly-1', 'Dustox-1', 'Ledian-1', 'Ariados-1', 'Yanma-1', 'Delcatty-1', 'Sableye-1', 'Weepinbell-1',
>   'Graveler-1', 'Gloom-1', 'Kadabra-1', 'Roselia-1', 'Volbeat-1', 'Illumise-1', 'Ivysaur-1', 'Parasect-1', 'Haunter-1',
>   'Murkrow-1', 'Grovyle-1', 'Combusken-1', 'Sudowoodo-1', 'Pupitar-1', 'Raticate-1', 'Dragonair-1', 'Mightyena-1',
>   'Linoone-1', 'Castform-1', 'Chimecho-1', 'Sneasel-1', 'Swellow-1', 'Arbok-1', 'Lunatone-1', 'Solrock-1', 'Venomoth-1',
>   'Piloswine-1', 'Girafarig-1', 'Ninjask-1', 'Seviper-1', 'Zangoose-1', 'Stantler-1', 'Absol-1', 'Cacturne-1',
>   'Delcatty-2', 'Sableye-2', 'Weepinbell-2', 'Graveler-2', 'Gloom-2', 'Porygon-2', 'Kadabra-2', 'Roselia-2',
>   'Volbeat-2', 'Illumise-2', 'Ivysaur-2', 'Parasect-2', 'Haunter-2', 'Murkrow-2', 'Plusle-2', 'Grovyle-2',
>   'Combusken-2', 'Sudowoodo-2', 'Pupitar-2', 'Raticate-2', 'Furret-2', 'Dragonair-2', 'Linoone-2', 'Castform-2',
>   'Sneasel-2', 'Swellow-2', 'Vigoroth-2', 'Lunatone-2', 'Solrock-2', 'Venomoth-2', 'Piloswine-2', 'Banette-2',
>   'Ninjask-2', 'Zangoose-2', 'Stantler-2', 'Absol-2', 'Pidgeot-2', 'Cacturne-2', 'Scyther-2', 'Dugtrio-1', 'Medicham-1',
>   'Fearow-1', 'Jynx-1', 'Dodrio-1', 'Breloom-1', 'Xatu-1', 'Glalie-1', 'Golem-1', 'Rhydon-1', 'Alakazam-1', 'Cradily-1',
>   'Armaldo-1', 'Gengar-1', 'Heracross-1', 'Shuckle-1', 'Aerodactyl-1', 'Flygon-1', 'Espeon-1', 'Sceptile-1',
>   'Dugtrio-2', 'Medicham-2', 'Fearow-2', 'Granbull-2', 'Jynx-2', 'Dodrio-2', 'Mr. Mime-2', 'Breloom-2', 'Victreebel-2',
>   'Exploud-2', 'Glalie-2', 'Golem-2', 'Rhydon-2', 'Alakazam-2', 'Cradily-2', 'Armaldo-2', 'Gengar-2', 'Heracross-2',
>   'Shuckle-2', 'Aerodactyl-2', 'Flygon-2', 'Espeon-2', 'Sceptile-2', 'Dugtrio-3', 'Medicham-3', 'Fearow-3', 'Jynx-3',
>   'Dodrio-3', 'Mr. Mime-3', 'Breloom-3', 'Xatu-3', 'Vileplume-3', 'Victreebel-3', 'Exploud-3', 'Shiftry-3', 'Glalie-3',
>   'Golem-3', 'Rhydon-3', 'Alakazam-3', 'Cradily-3', 'Armaldo-3', 'Gengar-3', 'Heracross-3', 'Shuckle-3', 'Aerodactyl-3',
>   'Gardevoir-3', 'Flygon-3', 'Espeon-3', 'Sceptile-3', 'Crobat-3', 'Dugtrio-4', 'Medicham-4', 'Misdreavus-4',
>   'Fearow-4', 'Granbull-4', 'Jynx-4', 'Dodrio-4', 'Mr. Mime-4', 'Breloom-4', 'Xatu-4', 'Vileplume-4', 'Victreebel-4',
>   'Exploud-4', 'Shiftry-4', 'Glalie-4', 'Golem-4', 'Rhydon-4', 'Alakazam-4', 'Nidoking-4', 'Cradily-4', 'Armaldo-4',
>   'Gengar-4', 'Heracross-4', 'Shuckle-4', 'Aerodactyl-4', 'Gardevoir-4', 'Flygon-4', 'Venusaur-4', 'Espeon-4',
>   'Sceptile-4', 'Crobat-4', 'Articuno-1', 'Regice-1', 'Articuno-2', 'Regice-2', 'Latios-2', 'Articuno-3', 'Regice-3',
>   'Latios-3', 'Articuno-4', 'Regice-4', 'Gengar-5', 'Gengar-6', 'Gengar-7', 'Gengar-8', 'Gardevoir-6', 'Gardevoir-8',
>   'Regice-5', 'Regice-6', 'Latios-6', 'Latios-8', 'Tyranitar-1', 'Tyranitar-2', 'Tyranitar-3', 'Tyranitar-4',
>   'Tyranitar-5', 'Tyranitar-6', 'Tyranitar-7', 'Tyranitar-8', 'Tyranitar-9', 'Tyranitar-10', 'Articuno-5', 'Articuno-6',
>   'Alakazam-AnabelSilver', 'Heracross-GretaSilver', 'Shedinja-GretaSilver', 'Breloom-GretaGold', 'Seviper-LucyGold',
>   'Regice-BrandonSilver', 'Articuno-BrandonGold'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.willOHKO(meta, field=Field(weather="rain"))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(4 sets)
> [
>   'Marowak-1', 'Marowak-2', 'Marowak-3', 'Marowak-4'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.canOHKO(meta, include_ohko=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(69 sets)
> [
>   'Gligar-2', 'Seaking-2', 'Crawdaunt-2', 'Kingler-2', 'Pinsir-2', 'Marowak-1', 'Golem-1', 'Rhydon-1', 'Nidoking-1',
>   'Donphan-1', 'Charizard-1', 'Typhlosion-1', 'Marowak-2', 'Rhydon-2', 'Magmar-2', 'Houndoom-2', 'Arcanine-2',
>   'Dugtrio-3', 'Whiscash-3', 'Marowak-3', 'Dewgong-3', 'Golem-3', 'Rhydon-3', 'Nidoking-3', 'Rapidash-3', 'Houndoom-3',
>   'Donphan-3', 'Wailord-3', 'Ninetales-3', 'Blaziken-3', 'Walrein-3', 'Charizard-3', 'Typhlosion-3', 'Swampert-3',
>   'Arcanine-3', 'Slaking-3', 'Dugtrio-4', 'Granbull-4', 'Whiscash-4', 'Marowak-4', 'Dewgong-4', 'Golem-4', 'Rhydon-4',
>   'Armaldo-4', 'Rapidash-4', 'Houndoom-4', 'Donphan-4', 'Wailord-4', 'Ninetales-4', 'Flareon-4', 'Blaziken-4',
>   'Walrein-4', 'Charizard-4', 'Typhlosion-4', 'Arcanine-4', 'Moltres-1', 'Moltres-2', 'Entei-2', 'Moltres-3',
>   'Moltres-4', 'Lapras-7', 'Lapras-8', 'Moltres-5', 'Moltres-6', 'Charizard-TuckerSilver', 'Swampert-TuckerGold',
>   'Lapras-SpenserSilver', 'Arcanine-SpenserGold', 'Moltres-BrandonGold'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.willOHKO(meta)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(25 sets)
> [
>   'Marowak-1', 'Charizard-1', 'Typhlosion-1', 'Marowak-2', 'Magmar-2', 'Houndoom-2', 'Marowak-3', 'Rapidash-3',
>   'Arcanine-3', 'Marowak-4', 'Houndoom-4', 'Ninetales-4', 'Flareon-4', 'Blaziken-4', 'Charizard-4', 'Typhlosion-4',
>   'Arcanine-4', 'Moltres-2', 'Entei-2', 'Moltres-3', 'Moltres-4', 'Moltres-5', 'Moltres-6', 'Charizard-TuckerSilver',
>   'Moltres-BrandonGold'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.willOHKO(meta, include_acc=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(3 sets)
> [
>   'Marowak-2', 'Marowak-3', 'Marowak-4'
> ]
> ```
>
> </details>


#### Negation

Every filter has a negated form via `.Not`:


> ```python
> db.sets.hasMove("earthquake").Not.hasMove("surf")     # has EQ but not Surf
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(150 sets)
> [
>   'Lickitung-2', 'Graveler-2', 'Wailmer-2', 'Marshtomp-2', 'Sudowoodo-2', 'Magcargo-2', 'Pupitar-2', 'Gligar-2',
>   'Lairon-2', 'Arbok-2', 'Solrock-2', 'Sandslash-2', 'Piloswine-2', 'Seviper-2', 'Camerupt-2', 'Relicanth-2',
>   'Dugtrio-1', 'Whiscash-1', 'Quagsire-1', 'Golem-1', 'Rhydon-1', 'Tauros-1', 'Donphan-1', 'Claydol-1', 'Steelix-1',
>   'Flygon-1', 'Aggron-1', 'Swampert-1', 'Dugtrio-2', 'Marowak-2', 'Forretress-2', 'Exploud-2', 'Rhydon-2', 'Tauros-2',
>   'Nidoqueen-2', 'Nidoking-2', 'Cradily-2', 'Heracross-2', 'Ursaring-2', 'Donphan-2', 'Claydol-2', 'Machamp-2',
>   'Steelix-2', 'Aerodactyl-2', 'Aggron-2', 'Walrein-2', 'Charizard-2', 'Snorlax-2', 'Metagross-2', 'Dugtrio-3',
>   'Granbull-3', 'Dusclops-3', 'Forretress-3', 'Marowak-3', 'Quagsire-3', 'Hariyama-3', 'Glalie-3', 'Golem-3',
>   'Rhydon-3', 'Kangaskhan-3', 'Tauros-3', 'Miltank-3', 'Altaria-3', 'Armaldo-3', 'Heracross-3', 'Donphan-3',
>   'Steelix-3', 'Flygon-3', 'Venusaur-3', 'Meganium-3', 'Feraligatr-3', 'Blaziken-3', 'Sceptile-3', 'Typhlosion-3',
>   'Salamence-3', 'Metagross-3', 'Slaking-3', 'Dugtrio-4', 'Granbull-4', 'Forretress-4', 'Marowak-4', 'Hariyama-4',
>   'Exploud-4', 'Glalie-4', 'Golem-4', 'Rhydon-4', 'Kangaskhan-4', 'Altaria-4', 'Nidoqueen-4', 'Nidoking-4', 'Armaldo-4',
>   'Heracross-4', 'Ursaring-4', 'Donphan-4', 'Claydol-4', 'Machamp-4', 'Steelix-4', 'Aerodactyl-4', 'Flygon-4',
>   'Venusaur-4', 'Meganium-4', 'Feraligatr-4', 'Aggron-4', 'Blaziken-4', 'Charizard-4', 'Typhlosion-4', 'Gyarados-4',
>   'Salamence-4', 'Metagross-4', 'Regirock-1', 'Regirock-2', 'Registeel-2', 'Latias-2', 'Latios-2', 'Regirock-3',
>   'Latias-3', 'Latios-3', 'Registeel-4', 'Ursaring-7', 'Ursaring-8', 'Machamp-5', 'Machamp-6', 'Snorlax-6', 'Snorlax-7',
>   'Salamence-5', 'Metagross-5', 'Metagross-7', 'Metagross-8', 'Regice-5', 'Latias-7', 'Latias-8', 'Latios-7',
>   'Latios-8', 'Dragonite-1', 'Dragonite-2', 'Dragonite-10', 'Tyranitar-2', 'Tyranitar-3', 'Tyranitar-5', 'Tyranitar-6',
>   'Tyranitar-9', 'Tyranitar-10', 'Salamence-TuckerSilver', 'Charizard-TuckerSilver', 'Metagross-TuckerGold',
>   'Slaking-SpenserSilver', 'Slaking-SpenserGold', 'Steelix-LucyGold', 'Regirock-BrandonSilver',
>   'Registeel-BrandonSilver'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.Not.willOHKO(meta).hasMove("earthquake")      # EQ users that don't guaranteed OHKO Meta
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(161 sets)
> [
>   'Lickitung-2', 'Graveler-2', 'Wailmer-2', 'Marshtomp-2', 'Sudowoodo-2', 'Magcargo-2', 'Pupitar-2', 'Gligar-2',
>   'Lairon-2', 'Arbok-2', 'Solrock-2', 'Sandslash-2', 'Piloswine-2', 'Seviper-2', 'Camerupt-2', 'Sharpedo-2',
>   'Relicanth-2', 'Dugtrio-1', 'Whiscash-1', 'Quagsire-1', 'Golem-1', 'Rhydon-1', 'Tauros-1', 'Donphan-1', 'Claydol-1',
>   'Steelix-1', 'Flygon-1', 'Aggron-1', 'Swampert-1', 'Dugtrio-2', 'Forretress-2', 'Whiscash-2', 'Exploud-2', 'Rhydon-2',
>   'Tauros-2', 'Nidoqueen-2', 'Nidoking-2', 'Cradily-2', 'Heracross-2', 'Ursaring-2', 'Donphan-2', 'Claydol-2',
>   'Machamp-2', 'Steelix-2', 'Aerodactyl-2', 'Aggron-2', 'Walrein-2', 'Charizard-2', 'Swampert-2', 'Snorlax-2',
>   'Metagross-2', 'Dugtrio-3', 'Granbull-3', 'Dusclops-3', 'Forretress-3', 'Quagsire-3', 'Hariyama-3', 'Glalie-3',
>   'Golem-3', 'Rhydon-3', 'Kangaskhan-3', 'Tauros-3', 'Slowking-3', 'Miltank-3', 'Altaria-3', 'Armaldo-3', 'Heracross-3',
>   'Donphan-3', 'Steelix-3', 'Flygon-3', 'Venusaur-3', 'Meganium-3', 'Blastoise-3', 'Feraligatr-3', 'Blaziken-3',
>   'Sceptile-3', 'Typhlosion-3', 'Swampert-3', 'Gyarados-3', 'Salamence-3', 'Metagross-3', 'Slaking-3', 'Dugtrio-4',
>   'Granbull-4', 'Forretress-4', 'Whiscash-4', 'Quagsire-4', 'Hariyama-4', 'Exploud-4', 'Glalie-4', 'Golem-4',
>   'Rhydon-4', 'Kangaskhan-4', 'Slowbro-4', 'Altaria-4', 'Nidoqueen-4', 'Nidoking-4', 'Armaldo-4', 'Heracross-4',
>   'Ursaring-4', 'Donphan-4', 'Claydol-4', 'Wailord-4', 'Machamp-4', 'Steelix-4', 'Aerodactyl-4', 'Flygon-4',
>   'Venusaur-4', 'Meganium-4', 'Blastoise-4', 'Feraligatr-4', 'Aggron-4', 'Walrein-4', 'Swampert-4', 'Gyarados-4',
>   'Salamence-4', 'Metagross-4', 'Regirock-1', 'Regirock-2', 'Registeel-2', 'Latias-2', 'Latios-2', 'Regirock-3',
>   'Latias-3', 'Latios-3', 'Registeel-4', 'Ursaring-7', 'Ursaring-8', 'Machamp-5', 'Machamp-6', 'Snorlax-6', 'Snorlax-7',
>   'Salamence-5', 'Metagross-5', 'Metagross-7', 'Metagross-8', 'Regice-5', 'Latias-7', 'Latias-8', 'Latios-7',
>   'Latios-8', 'Dragonite-1', 'Dragonite-2', 'Dragonite-9', 'Dragonite-10', 'Tyranitar-1', 'Tyranitar-2', 'Tyranitar-3',
>   'Tyranitar-5', 'Tyranitar-6', 'Tyranitar-9', 'Tyranitar-10', 'Swampert-TuckerSilver', 'Salamence-TuckerSilver',
>   'Swampert-TuckerGold', 'Metagross-TuckerGold', 'Slaking-SpenserSilver', 'Slaking-SpenserGold', 'Steelix-LucyGold',
>   'Regirock-BrandonSilver', 'Registeel-BrandonSilver'
> ]
> ```
>
> </details>


<br>

> ```python
> db.sets.Not.canDieTo(meta)                             # survives Metagross even on max roll
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> SetCollection(699 sets)
> [
>   'Magikarp-1', 'Wooper-1', 'Togepi-1', 'Marill-1', 'Slugma-1', 'Wynaut-1', 'Nincada-1', 'Jigglypuff-1', 'Wingull-1',
>   'Mareep-1', 'Slakoth-1', 'Ditto-1', 'Barboach-1', 'Pineco-1', 'Horsea-1', 'Shroomish-1', 'Duskull-1', 'Electrike-1',
>   'Vulpix-1', 'Pikachu-1', 'Sandshrew-1', 'Poliwag-1', 'Beldum-1', 'Gulpin-1', 'Shellder-1', 'Numel-1', 'Corphish-1',
>   'Charmander-1', 'Cyndaquil-1', 'Torchic-1', 'Mudkip-1', 'Squirtle-1', 'Totodile-1', 'Slowpoke-1', 'Chikorita-1',
>   'Psyduck-1', 'Cubone-1', 'Goldeen-1', 'Magnemite-1', 'Seel-1', 'Grimer-1', 'Krabby-1', 'Exeggcute-1', 'Voltorb-1',
>   'Chinchou-1', 'Houndour-1', 'Phanpy-1', 'Aron-1', 'Luvdisc-1', 'Tentacool-1', 'Koffing-1', 'Staryu-1', 'Lombre-1',
>   'Clamperl-1', 'Growlithe-1', "Farfetch'd-1", 'Omanyte-1', 'Aipom-1', 'Elekid-1', 'Loudred-1', 'Spinda-1',
>   'Nidorina-1', 'Nidorino-1', 'Flaaffy-1', 'Magby-1', 'Corsola-1', 'Mawile-1', 'Poliwhirl-1', 'Onix-1', 'Dustox-1',
>   'Ariados-1', 'Yanma-1', 'Delcatty-1', 'Sableye-1', 'Lickitung-1', 'Gloom-1', 'Porygon-1', 'Kadabra-1', 'Wailmer-1',
>   'Roselia-1', 'Illumise-1', 'Charmeleon-1', 'Wartortle-1', 'Machoke-1', 'Bayleef-1', 'Quilava-1', 'Croconaw-1',
>   'Togetic-1', 'Murkrow-1', 'Wobbuffet-1', 'Plusle-1', 'Minun-1', 'Combusken-1', 'Marshtomp-1', 'Ponyta-1',
>   'Azumarill-1', 'Magcargo-1', 'Sealeo-1', 'Masquerain-1', 'Furret-1', 'Dunsparce-1', 'Dragonair-1', 'Mightyena-1',
>   'Linoone-1', 'Castform-1', 'Shelgon-1', 'Metang-1', 'Wigglytuff-1', 'Sunflora-1', 'Chimecho-1', 'Gligar-1',
>   'Qwilfish-1', 'Pelipper-1', 'Swellow-1', 'Lairon-1', 'Tangela-1', 'Arbok-1', 'Persian-1', 'Seadra-1', 'Kecleon-1',
>   'Vigoroth-1', 'Noctowl-1', 'Sandslash-1', 'Venomoth-1', 'Chansey-1', 'Seaking-1', 'Jumpluff-1', 'Golbat-1',
>   'Primeape-1', 'Hitmonlee-1', 'Hitmonchan-1', 'Girafarig-1', 'Hitmontop-1', 'Banette-1', 'Seviper-1', 'Zangoose-1',
>   'Camerupt-1', 'Sharpedo-1', 'Tropius-1', 'Magneton-1', 'Mantine-1', 'Stantler-1', 'Absol-1', 'Swalot-1',
>   'Crawdaunt-1', 'Pidgeot-1', 'Grumpig-1', 'Torkoal-1', 'Kingler-1', 'Bellossom-1', 'Octillery-1', 'Huntail-1',
>   'Gorebyss-1', 'Relicanth-1', 'Omastar-1', 'Kabutops-1', 'Poliwrath-1', 'Scyther-1', 'Pinsir-1', 'Politoed-1',
>   'Cloyster-1', 'Sableye-2', 'Lickitung-2', 'Weepinbell-2', 'Wailmer-2', 'Roselia-2', 'Charmeleon-2', 'Wartortle-2',
>   'Machoke-2', 'Haunter-2', 'Bayleef-2', 'Quilava-2', 'Croconaw-2', 'Togetic-2', 'Murkrow-2', 'Wobbuffet-2', 'Plusle-2',
>   'Minun-2', 'Combusken-2', 'Marshtomp-2', 'Ponyta-2', 'Azumarill-2', 'Magcargo-2', 'Sealeo-2', 'Masquerain-2',
>   'Furret-2', 'Dunsparce-2', 'Dragonair-2', 'Mightyena-2', 'Castform-2', 'Shelgon-2', 'Metang-2', 'Wigglytuff-2',
>   'Sunflora-2', 'Chimecho-2', 'Gligar-2', 'Qwilfish-2', 'Pelipper-2', 'Swellow-2', 'Lairon-2', 'Tangela-2', 'Arbok-2',
>   'Persian-2', 'Seadra-2', 'Kecleon-2', 'Vigoroth-2', 'Noctowl-2', 'Sandslash-2', 'Venomoth-2', 'Chansey-2',
>   'Seaking-2', 'Jumpluff-2', 'Golbat-2', 'Primeape-2', 'Hitmonlee-2', 'Hitmonchan-2', 'Girafarig-2', 'Hitmontop-2',
>   'Banette-2', 'Ninjask-2', 'Seviper-2', 'Camerupt-2', 'Sharpedo-2', 'Tropius-2', 'Magneton-2', 'Mantine-2', 'Swalot-2',
>   'Crawdaunt-2', 'Pidgeot-2', 'Grumpig-2', 'Torkoal-2', 'Kingler-2', 'Cacturne-2', 'Bellossom-2', 'Octillery-2',
>   'Huntail-2', 'Gorebyss-2', 'Relicanth-2', 'Omastar-2', 'Kabutops-2', 'Poliwrath-2', 'Scyther-2', 'Pinsir-2',
>   'Politoed-2', 'Cloyster-2', 'Misdreavus-1', 'Granbull-1', 'Dusclops-1', 'Mr. Mime-1', 'Lanturn-1', 'Forretress-1',
>   'Whiscash-1', 'Xatu-1', 'Skarmory-1', 'Marowak-1', 'Quagsire-1', 'Clefable-1', 'Hariyama-1', 'Raichu-1', 'Dewgong-1',
>   'Manectric-1', 'Vileplume-1', 'Victreebel-1', 'Electrode-1', 'Exploud-1', 'Shiftry-1', 'Ludicolo-1', 'Hypno-1',
>   'Rhydon-1', 'Weezing-1', 'Kangaskhan-1', 'Electabuzz-1', 'Tauros-1', 'Slowbro-1', 'Slowking-1', 'Miltank-1',
>   'Altaria-1', 'Nidoqueen-1', 'Nidoking-1', 'Magmar-1', 'Cradily-1', 'Golduck-1', 'Rapidash-1', 'Muk-1', 'Ampharos-1',
>   'Scizor-1', 'Ursaring-1', 'Houndoom-1', 'Donphan-1', 'Claydol-1', 'Wailord-1', 'Ninetales-1', 'Machamp-1',
>   'Shuckle-1', 'Steelix-1', 'Tentacruel-1', 'Porygon2-1', 'Gardevoir-1', 'Exeggutor-1', 'Starmie-1', 'Flygon-1',
>   'Venusaur-1', 'Vaporeon-1', 'Jolteon-1', 'Flareon-1', 'Meganium-1', 'Espeon-1', 'Umbreon-1', 'Blastoise-1',
>   'Feraligatr-1', 'Aggron-1', 'Blaziken-1', 'Walrein-1', 'Charizard-1', 'Typhlosion-1', 'Lapras-1', 'Crobat-1',
>   'Swampert-1', 'Gyarados-1', 'Snorlax-1', 'Kingdra-1', 'Blissey-1', 'Milotic-1', 'Arcanine-1', 'Salamence-1',
>   'Metagross-1', 'Slaking-1', 'Marowak-2', 'Quagsire-2', 'Misdreavus-2', 'Granbull-2', 'Dusclops-2', 'Mr. Mime-2',
>   'Lanturn-2', 'Forretress-2', 'Skarmory-2', 'Whiscash-2', 'Xatu-2', 'Clefable-2', 'Hariyama-2', 'Raichu-2',
>   'Dewgong-2', 'Manectric-2', 'Vileplume-2', 'Victreebel-2', 'Electrode-2', 'Exploud-2', 'Shiftry-2', 'Ludicolo-2',
>   'Hypno-2', 'Golem-2', 'Weezing-2', 'Kangaskhan-2', 'Electabuzz-2', 'Tauros-2', 'Slowbro-2', 'Slowking-2', 'Miltank-2',
>   'Altaria-2', 'Nidoqueen-2', 'Nidoking-2', 'Magmar-2', 'Golduck-2', 'Rapidash-2', 'Muk-2', 'Ampharos-2', 'Scizor-2',
>   'Ursaring-2', 'Houndoom-2', 'Donphan-2', 'Claydol-2', 'Wailord-2', 'Ninetales-2', 'Machamp-2', 'Shuckle-2',
>   'Steelix-2', 'Tentacruel-2', 'Porygon2-2', 'Gardevoir-2', 'Exeggutor-2', 'Starmie-2', 'Flygon-2', 'Venusaur-2',
>   'Vaporeon-2', 'Jolteon-2', 'Flareon-2', 'Meganium-2', 'Umbreon-2', 'Blastoise-2', 'Feraligatr-2', 'Aggron-2',
>   'Blaziken-2', 'Walrein-2', 'Charizard-2', 'Typhlosion-2', 'Lapras-2', 'Crobat-2', 'Swampert-2', 'Gyarados-2',
>   'Snorlax-2', 'Kingdra-2', 'Blissey-2', 'Milotic-2', 'Arcanine-2', 'Salamence-2', 'Metagross-2', 'Slaking-2',
>   'Misdreavus-3', 'Granbull-3', 'Dusclops-3', 'Lanturn-3', 'Forretress-3', 'Whiscash-3', 'Skarmory-3', 'Marowak-3',
>   'Quagsire-3', 'Clefable-3', 'Hariyama-3', 'Raichu-3', 'Dewgong-3', 'Manectric-3', 'Vileplume-3', 'Victreebel-3',
>   'Electrode-3', 'Exploud-3', 'Shiftry-3', 'Ludicolo-3', 'Hypno-3', 'Rhydon-3', 'Weezing-3', 'Kangaskhan-3',
>   'Electabuzz-3', 'Tauros-3', 'Slowbro-3', 'Slowking-3', 'Miltank-3', 'Altaria-3', 'Nidoqueen-3', 'Nidoking-3',
>   'Magmar-3', 'Golduck-3', 'Rapidash-3', 'Muk-3', 'Ampharos-3', 'Scizor-3', 'Ursaring-3', 'Houndoom-3', 'Donphan-3',
>   'Claydol-3', 'Wailord-3', 'Ninetales-3', 'Machamp-3', 'Shuckle-3', 'Steelix-3', 'Tentacruel-3', 'Porygon2-3',
>   'Exeggutor-3', 'Starmie-3', 'Flygon-3', 'Venusaur-3', 'Vaporeon-3', 'Jolteon-3', 'Flareon-3', 'Meganium-3',
>   'Umbreon-3', 'Blastoise-3', 'Feraligatr-3', 'Aggron-3', 'Blaziken-3', 'Walrein-3', 'Charizard-3', 'Typhlosion-3',
>   'Lapras-3', 'Crobat-3', 'Swampert-3', 'Gyarados-3', 'Snorlax-3', 'Kingdra-3', 'Blissey-3', 'Milotic-3', 'Arcanine-3',
>   'Salamence-3', 'Metagross-3', 'Slaking-3', 'Granbull-4', 'Dusclops-4', 'Lanturn-4', 'Forretress-4', 'Whiscash-4',
>   'Skarmory-4', 'Marowak-4', 'Quagsire-4', 'Clefable-4', 'Hariyama-4', 'Raichu-4', 'Dewgong-4', 'Manectric-4',
>   'Vileplume-4', 'Victreebel-4', 'Electrode-4', 'Exploud-4', 'Shiftry-4', 'Ludicolo-4', 'Hypno-4', 'Rhydon-4',
>   'Weezing-4', 'Kangaskhan-4', 'Electabuzz-4', 'Tauros-4', 'Slowbro-4', 'Slowking-4', 'Miltank-4', 'Altaria-4',
>   'Nidoqueen-4', 'Nidoking-4', 'Magmar-4', 'Cradily-4', 'Golduck-4', 'Rapidash-4', 'Muk-4', 'Ampharos-4', 'Scizor-4',
>   'Ursaring-4', 'Houndoom-4', 'Donphan-4', 'Claydol-4', 'Wailord-4', 'Ninetales-4', 'Machamp-4', 'Shuckle-4',
>   'Steelix-4', 'Tentacruel-4', 'Porygon2-4', 'Exeggutor-4', 'Starmie-4', 'Flygon-4', 'Venusaur-4', 'Vaporeon-4',
>   'Jolteon-4', 'Flareon-4', 'Meganium-4', 'Umbreon-4', 'Blastoise-4', 'Feraligatr-4', 'Aggron-4', 'Blaziken-4',
>   'Walrein-4', 'Charizard-4', 'Typhlosion-4', 'Lapras-4', 'Crobat-4', 'Swampert-4', 'Gyarados-4', 'Snorlax-4',
>   'Kingdra-4', 'Blissey-4', 'Milotic-4', 'Arcanine-4', 'Salamence-4', 'Metagross-4', 'Slaking-4', 'Zapdos-1',
>   'Moltres-1', 'Raikou-1', 'Entei-1', 'Suicune-1', 'Regirock-1', 'Registeel-1', 'Latias-1', 'Latios-1', 'Articuno-2',
>   'Zapdos-2', 'Moltres-2', 'Raikou-2', 'Entei-2', 'Suicune-2', 'Regirock-2', 'Registeel-2', 'Latias-2', 'Latios-2',
>   'Zapdos-3', 'Moltres-3', 'Raikou-3', 'Entei-3', 'Suicune-3', 'Regirock-3', 'Registeel-3', 'Latias-3', 'Latios-3',
>   'Zapdos-4', 'Moltres-4', 'Raikou-4', 'Entei-4', 'Suicune-4', 'Regirock-4', 'Regice-4', 'Registeel-4', 'Latias-4',
>   'Latios-4', 'Ursaring-5', 'Ursaring-6', 'Ursaring-7', 'Ursaring-8', 'Machamp-5', 'Machamp-6', 'Machamp-7',
>   'Machamp-8', 'Gardevoir-5', 'Gardevoir-6', 'Gardevoir-7', 'Starmie-5', 'Starmie-6', 'Starmie-7', 'Starmie-8',
>   'Lapras-5', 'Lapras-6', 'Lapras-7', 'Lapras-8', 'Snorlax-5', 'Snorlax-6', 'Snorlax-7', 'Snorlax-8', 'Salamence-5',
>   'Salamence-6', 'Salamence-7', 'Salamence-8', 'Metagross-5', 'Metagross-6', 'Metagross-7', 'Metagross-8', 'Regirock-5',
>   'Regirock-6', 'Registeel-5', 'Registeel-6', 'Latias-5', 'Latias-6', 'Latias-7', 'Latias-8', 'Latios-5', 'Latios-6',
>   'Latios-7', 'Latios-8', 'Dragonite-1', 'Dragonite-2', 'Dragonite-3', 'Dragonite-4', 'Dragonite-5', 'Dragonite-6',
>   'Dragonite-7', 'Dragonite-8', 'Dragonite-9', 'Dragonite-10', 'Tyranitar-3', 'Tyranitar-4', 'Tyranitar-5',
>   'Tyranitar-6', 'Tyranitar-7', 'Tyranitar-8', 'Tyranitar-10', 'Zapdos-5', 'Zapdos-6', 'Moltres-5', 'Moltres-6',
>   'Raikou-5', 'Raikou-6', 'Entei-5', 'Entei-6', 'Suicune-5', 'Suicune-6', 'Entei-AnabelSilver', 'Snorlax-AnabelSilver',
>   'Raikou-AnabelGold', 'Latios-AnabelGold', 'Snorlax-AnabelGold', 'Swampert-TuckerSilver', 'Salamence-TuckerSilver',
>   'Charizard-TuckerSilver', 'Swampert-TuckerGold', 'Metagross-TuckerGold', 'Latias-TuckerGold', 'Crobat-SpenserSilver',
>   'Slaking-SpenserSilver', 'Lapras-SpenserSilver', 'Arcanine-SpenserGold', 'Slaking-SpenserGold', 'Suicune-SpenserGold',
>   'Umbreon-GretaSilver', 'Umbreon-GretaGold', 'Gengar-GretaGold', 'Seviper-LucySilver', 'Shuckle-LucySilver',
>   'Milotic-LucySilver', 'Seviper-LucyGold', 'Steelix-LucyGold', 'Gyarados-LucyGold', 'Regirock-BrandonSilver',
>   'Registeel-BrandonSilver', 'Zapdos-BrandonGold', 'Moltres-BrandonGold'
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
> [
>   'PSYCHIC (M) NORTON', 'PSYCHIC (M) LUKAS', 'PSYCHIC (M) ZACH', 'PSYCHIC (F) KAITLYN', 'PSYCHIC (F) BREANNA',
>   'PSYCHIC (F) KENDRA', 'HEX MANIAC MOLLY', 'HEX MANIAC JAZMIN', 'HEX MANIAC KELSEY', 'POKÉMANIAC JALEN',
>   'POKÉMANIAC GRIFFEN', 'POKÉMANIAC XANDER', 'GENTLEMAN MARVIN', 'GENTLEMAN BRENNAN', 'COLLECTOR GABRIEL',
>   'PARASOL LADY EMILY', 'COOLTRAINER (M) BRADEN', 'COOLTRAINER (M) KAYDEN', 'COOLTRAINER (M) COOPER',
>   'COOLTRAINER (F) JULIA', 'COOLTRAINER (F) AMARA', 'COOLTRAINER (F) LYNN', 'PKMN RANGER (M) JOVAN',
>   'PKMN RANGER (M) DOMINIC', 'PKMN RANGER (M) NIKOLAS', 'PKMN RANGER (F) VALERIA', 'PKMN RANGER (F) DELANEY',
>   'PKMN RANGER (F) MEGHAN', 'DRAGON TAMER ROBERTO', 'DRAGON TAMER DAMIAN', 'DRAGON TAMER BRODY', 'DRAGON TAMER GRAHAM',
>   'POKÉFAN (M) TYLOR', 'POKÉFAN (F) JAREN', 'PKMN BREEDER (M) CORDELL', 'PKMN BREEDER (F) JAZLYN', 'YOUNGSTER ZACHERY',
>   'YOUNGSTER JOHAN', 'LASS SHEA', 'LASS KAILA', 'SCHOOL KID (M) ISIAH', 'SCHOOL KID (M) GARRETT',
>   'SCHOOL KID (F) HAYLIE', 'SCHOOL KID (F) MEGAN', 'RICH BOY ISSAC', 'RICH BOY QUINTON', 'LADY SALMA', 'LADY ANSLEY',
>   'BUG CATCHER HOLDEN', 'BUG CATCHER LUCA', 'NINJA BOY JAMISON', 'NINJA BOY GUNNAR', 'TUBER (M) CRAIG',
>   'TUBER (M) PIERCE', 'TUBER (F) REGINA', 'TUBER (F) ALISON', 'FISHERMAN RAMIRO', 'FISHERMAN HUNTER',
>   'RUIN MANIAC AIDEN', 'RUIN MANIAC XAVIER', 'COLLECTOR CLINTON', 'COLLECTOR JESSE', 'BIRD KEEPER GAGE',
>   'BIRD KEEPER ARNOLD', 'SAILOR JARRETT', 'SAILOR GARETT', 'GENTLEMAN RUBEN', 'GENTLEMAN LAMAR', 'YOUNGSTER JAXON',
>   'YOUNGSTER LOGAN', 'LASS EMILEE', 'LASS JOSIE', 'CAMPER ARMANDO', 'CAMPER SKYLER', 'PICNICKER RUTH',
>   'PICNICKER MELODY', 'SWIMMER (M) PEDRO', 'SWIMMER (M) ERICK', 'SWIMMER (F) ELAINE', 'SWIMMER (F) JOYCE',
>   'POKÉFAN (M) TODD', 'POKÉFAN (M) GAVIN', 'POKÉFAN (F) MALORY', 'POKÉFAN (F) ESTHER', 'PKMN BREEDER (M) OSCAR',
>   'PKMN BREEDER (M) WILSON', 'PKMN BREEDER (F) CLARE', 'PKMN BREEDER (F) TESS', 'COOLTRAINER (M) LEON',
>   'COOLTRAINER (M) ALONZO', 'COOLTRAINER (M) VINCE', 'COOLTRAINER (M) BRYON', 'COOLTRAINER (F) AVA',
>   'COOLTRAINER (F) MIRIAM', 'COOLTRAINER (F) CARRIE', 'COOLTRAINER (F) GILLIAN', 'PKMN RANGER (M) TYLER',
>   'PKMN RANGER (M) CHAZ', 'PKMN RANGER (M) NELSON', 'PKMN RANGER (F) SHANIA', 'PKMN RANGER (F) STELLA',
>   'PKMN RANGER (F) DORINE', 'DRAGON TAMER MADDOX', 'DRAGON TAMER DAVIN', 'DRAGON TAMER TREVON', 'EXPERT (M) ALEXAS',
>   'EXPERT (M) WESTON', 'EXPERT (M) JASPER', 'EXPERT (F) NADIA', 'EXPERT (F) MIRANDA', 'EXPERT (F) EMMA',
>   'PSYCHIC (M) ROLANDO', 'PSYCHIC (M) STANLY', 'PSYCHIC (M) DARIO', 'PSYCHIC (F) KARLEE', 'PSYCHIC (F) JAYLIN',
>   'PSYCHIC (F) INGRID', 'HEX MANIAC DELILAH', 'HEX MANIAC CARLY', 'HEX MANIAC LEXIE', 'POKÉMANIAC MILLER',
>   'POKÉMANIAC MARV', 'POKÉMANIAC LAYTON', 'GENTLEMAN BROOKS', 'GENTLEMAN GREGORY', 'GENTLEMAN REESE',
>   'TRIATHLETE (M RUNNER) MASON', 'TRIATHLETE (M RUNNER) TOBY', 'TRIATHLETE (F RUNNER) DOROTHY',
>   'TRIATHLETE (F RUNNER) PIPER', 'TRIATHLETE (M SWIMMER) FINN', 'TRIATHLETE (M SWIMMER) SAMIR',
>   'TRIATHLETE (F SWIMMER) FIONA', 'TRIATHLETE (F SWIMMER) GLORIA', 'TRIATHLETE (M BIKER) NICO',
>   'TRIATHLETE (M BIKER) JEREMY', 'TRIATHLETE (F BIKER) CAITLIN', 'TRIATHLETE (F BIKER) REENA', 'FISHERMAN THEO',
>   'FISHERMAN BAILEY', 'COLLECTOR GIDEON', 'COLLECTOR TRISTON', 'GUITARIST CHARLES', 'GUITARIST RAYMOND',
>   'BIRD KEEPER DIRK', 'BIRD KEEPER HAROLD', 'SAILOR OMAR', 'SAILOR PETER', 'PARASOL LADY ALIVIA', 'PARASOL LADY PAIGE',
>   'BEAUTY ANYA', 'BEAUTY DAWN', 'AROMA LADY ABBY', 'AROMA LADY GRETEL', 'DOME ACE TUCKER', 'DOME ACE TUCKER',
>   'PALACE MAVEN SPENSER', 'PIKE QUEEN LUCY'
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
> [
>   'COOLTRAINER (M) COOPER', 'COOLTRAINER (F) LYNN', 'DRAGON TAMER ROBERTO', 'DRAGON TAMER DAMIAN', 'DRAGON TAMER BRODY',
>   'DRAGON TAMER GRAHAM', 'PKMN BREEDER (M) CORDELL', 'RICH BOY ISSAC', 'RICH BOY QUINTON', 'LADY SALMA', 'LADY ANSLEY',
>   'KINDLER KAMERON', 'KINDLER ALFREDO', 'GENTLEMAN RUBEN', 'GENTLEMAN LAMAR', 'PKMN BREEDER (M) OSCAR',
>   'PKMN BREEDER (M) WILSON', 'PKMN BREEDER (F) CLARE', 'PKMN BREEDER (F) TESS', 'COOLTRAINER (M) ALONZO',
>   'PKMN RANGER (M) TYLER', 'PKMN RANGER (M) CHAZ', 'PKMN RANGER (F) SHANIA', 'PKMN RANGER (F) STELLA',
>   'DRAGON TAMER MADDOX', 'DRAGON TAMER DAVIN', 'DRAGON TAMER TREVON', 'BLACK BELT BRET', 'BATTLE GIRL ELENA',
>   'POKÉMANIAC MILLER', 'POKÉMANIAC MARV', 'POKÉMANIAC LAYTON', 'GENTLEMAN BROOKS', 'TRIATHLETE (M RUNNER) MASON',
>   'TRIATHLETE (M RUNNER) TOBY', 'TRIATHLETE (F RUNNER) DOROTHY', 'TRIATHLETE (F RUNNER) PIPER',
>   'TRIATHLETE (M BIKER) NICO', 'TRIATHLETE (M BIKER) JEREMY', 'TRIATHLETE (F BIKER) CAITLIN',
>   'TRIATHLETE (F BIKER) REENA', 'COLLECTOR GIDEON', 'COLLECTOR TRISTON', 'BIRD KEEPER DIRK', 'BIRD KEEPER HAROLD',
>   'KINDLER ANDRE', 'KINDLER FERRIS', 'PARASOL LADY ALIVIA', 'PARASOL LADY PAIGE', 'DOME ACE TUCKER'
> ]
> ```
>
> </details>


<br>

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
>   'DRAGON TAMER ROBERTO', 'DRAGON TAMER DAMIAN', 'DRAGON TAMER BRODY', 'DRAGON TAMER GRAHAM', 'KINDLER KAMERON',
>   'KINDLER ALFREDO', 'DRAGON TAMER MADDOX', 'DRAGON TAMER DAVIN', 'DRAGON TAMER TREVON', 'BLACK BELT BRET',
>   'BATTLE GIRL ELENA', 'POKÉMANIAC LAYTON', 'BIRD KEEPER DIRK', 'BIRD KEEPER HAROLD', 'KINDLER ANDRE', 'KINDLER FERRIS',
>   'DOME ACE TUCKER'
> ]
> ```
>
> </details>


<br>

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
>   'PKMN BREEDER (M) OSCAR', 'PKMN BREEDER (M) WILSON', 'PKMN BREEDER (F) CLARE', 'PKMN BREEDER (F) TESS',
>   'COOLTRAINER (M) ALONZO', 'COOLTRAINER (M) VINCE', 'COOLTRAINER (F) CARRIE', 'PKMN RANGER (M) TYLER',
>   'BLACK BELT RAUL', 'BATTLE GIRL ALANA', 'EXPERT (M) ALEXAS', 'EXPERT (F) NADIA', 'PSYCHIC (M) ROLANDO',
>   'PSYCHIC (M) STANLY', 'PSYCHIC (M) DARIO', 'PSYCHIC (F) KARLEE', 'PSYCHIC (F) JAYLIN', 'PSYCHIC (F) INGRID',
>   'POKÉMANIAC MARV', 'POKÉMANIAC LAYTON', 'GENTLEMAN BROOKS', 'GENTLEMAN GREGORY', 'TRIATHLETE (M RUNNER) MASON',
>   'TRIATHLETE (M BIKER) NICO', 'RUIN MANIAC HUGO', 'RUIN MANIAC BRYCE', 'HIKER DEV', 'HIKER COREY'
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
> db = Database()
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


<br>

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


<br>

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


### Specifying Moves

Moves can be passed as a string name (looked up from `data/moves.json`):


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
> result = calc_matchup(meta, ttar, "Meteor Mash")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> result = {
>   'rolls': [323, 326, 330, 334, 338, 342, 345, 349, 353, 357, 361, 364, 368, 372, 376, 380],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 323,
>   'max': 380,
>   'min_pct': 94.70,
>   'max_pct': 111.40,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.68, 2: 1.0},
> }
> ```
>
> </details>


<br>

> ```python
> print(format_result(result, "Meteor Mash"))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> Meteor Mash: 323-380 (94.7% - 111.4%) [HP: 341]
>   Per-hit rolls: (323, 326, 330, 334, 338, 342, 345, 349, 353, 357, 361, 364, 368, 372, 376, 380)
>   68.8% chance to 1HKO
>   guaranteed 2HKO
> ```
>
> </details>


The result dict contains: `rolls` (per-hit damage values), `attack_rolls` (combined multi-hit totals, None for single-hit), `hit_info`, `min`/`max` damage, `min_pct`/`max_pct` (as percentage of defender max HP), `defender_hp`, `defender_max_hp`, and `ko_chances` ({1: prob, 2: prob, ...}).

### Raw API

For fine-grained control, use `damage_rolls` + `ko_chance` directly:


> ```python
> rolls = damage_rolls(meta, ttar, "Meteor Mash")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> rolls = [323, 326, 330, 334, 338, 342, 345, 349, 353, 357, 361, 364, 368, 372, 376, 380]
> ```
>
> </details>


<br>

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


<br>

> ```python
> kos = ko_chance(rolls, ttar_hp)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> kos = {
>   1: 0.69,
>   2: 1.00,
> }
> ```
>
> </details>


### Attacker and Defender

Both can be either a frontier set dict (from the database) or a `CustomSet`. Frontier sets at non-default IVs/level:


> ```python
> calc_matchup(meta, ttar, "Meteor Mash", atk_ivs=15, def_ivs=15, atk_level=50, def_level=50)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201, 204],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 173,
>   'max': 204,
>   'min_pct': 103.60,
>   'max_pct': 122.20,
>   'defender_hp': 167,
>   'defender_max_hp': 167,
>   'ko_chances': {1: 1.0},
> }
> ```
>
> </details>


### Field Conditions


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


<br>

> ```python
> calc_matchup(starmie, ttar, "Surf", field=Field(light_screen=True))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [132, 134, 135, 137, 138, 140, 141, 143, 145, 146, 148, 149, 151, 152, 154, 156],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 132,
>   'max': 156,
>   'min_pct': 38.70,
>   'max_pct': 45.70,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 1.0},
> }
> ```
>
> </details>


<br>

> ```python
> calc_matchup(starmie, ttar, "Surf", field=Field(is_doubles=True))
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [132, 134, 135, 137, 138, 140, 141, 143, 145, 146, 148, 149, 151, 152, 154, 156],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 132,
>   'max': 156,
>   'min_pct': 38.70,
>   'max_pct': 45.70,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 0.0, 3: 1.0},
> }
> ```
>
> </details>


### Stat Boosts


> ```python
> calc_matchup(meta, ttar, "Meteor Mash", atk_boosts={"atk": 1})
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [484, 490, 495, 501, 507, 513, 518, 524, 530, 535, 541, 547, 552, 558, 564, 570],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 484,
>   'max': 570,
>   'min_pct': 141.90,
>   'max_pct': 167.20,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 1.0},
> }
> ```
>
> </details>


<br>

> ```python
> calc_matchup(meta, ttar, "Meteor Mash", atk_boosts={"atk": -1})
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


<br>

> ```python
> calc_matchup(meta, ttar, "Meteor Mash", def_boosts={"def": 2}, critical=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [647, 655, 662, 670, 678, 685, 693, 701, 708, 716, 723, 731, 739, 746, 754, 762],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 647,
>   'max': 762,
>   'min_pct': 189.70,
>   'max_pct': 223.50,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 1.0},
> }
> ```
>
> </details>


### Status Conditions


> ```python
> calc_matchup(meta, ttar, "Meteor Mash", atk_status="burn")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'rolls': [163, 165, 167, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192],
>   'attack_rolls': None,
>   'hit_info': {'type': 'single'},
>   'min': 163,
>   'max': 192,
>   'min_pct': 47.80,
>   'max_pct': 56.30,
>   'defender_hp': 341,
>   'defender_max_hp': 341,
>   'ko_chances': {1: 0.0, 2: 0.84, 3: 1.0},
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
> get_hit_info("Double Kick")
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


<br>

> ```python
> get_hit_info("Bullet Seed")
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


<br>

> ```python
> get_hit_info("Triple Kick")
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


<br>

> ```python
> get_hit_info("Earthquake")
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
> from frontierbrain3.damagecalc import combine_multi_hit_rolls
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


<br>

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


<br>

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


<br>

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


<br>

> ```python
> total_rolls = combine_multi_hit_rolls(per_hit, hit_info)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> total_rolls = [
>   196, 197, 197, 198, 198, 198, 199, 199, 200, 200, 200, 201, 201, 201, 201, 202, 202, 202, 202, 202, 202, 203, 203,
>   203, 203, 203, 203, 204, 204, 204, 204, 204, 204, 204, 205, 205, 205, 205, 205, 205, 205, 205, 206, 206, 206, 206,
>   206, 206, 206, 207, 207, 207, 207, 207, 207, 207, 207, 208, 208, 208, 208, 208, 208, 208, 208, 208, 209, 209, 209,
>   209, 209, 209, 209, 209, 209, 209, 209, 209, 210, 210, 210, 210, 210, 210, 210, 210, 210, 210, 210, 211, 211, 211,
>   211, 211, 211, 211, 211, 211, 211, 211, 211, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 213,
>   213, 213, 213, 213, 213, 213, 213, 213, 213, 213, 213, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214, 214,
>   214, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 216, 216, 216, 216, 216, 216, 216, 216, 216, 216,
>   216, 216, 216, 216, 217, 217, 217, 217, 217, 217, 217, 217, 217, 217, 218, 218, 218, 218, 218, 218, 218, 218, 218,
>   218, 218, 219, 219, 219, 219, 219, 219, 219, 219, 219, 219, 220, 220, 220, 220, 220, 220, 220, 220, 220, 221, 221,
>   221, 221, 221, 221, 221, 221, 222, 222, 222, 222, 222, 222, 222, 223, 223, 223, 223, 223, 223, 223, 223, 224, 224,
>   224, 224, 224, 225, 225, 225, 225, 225, 225, 226, 226, 226, 226, 226, 227, 227, 227, 227, 228, 228, 228, 229, 229,
>   230, 230, 232
> ]
> ```
>
> </details>


<br>

> ```python
> ko_chance(total_rolls, calc_stats(lax)["hp"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   1: 0.00,
>   2: 0.0001,
>   3: 1.00,
> }
> ```
>
> </details>


### Recoil and Drain Reference

Not applied in the damage formula (they don't affect the hit), but provided as constants for external calculations:


> ```python
> from frontierbrain3.damagecalc import RECOIL_MOVES, DRAIN_MOVES
> RECOIL_MOVES
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


<br>

> ```python
> DRAIN_MOVES
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

Tower trainers are grouped into tiers by index, each with fixed IVs and round eligibility. Trainer data is based on the [Bulbapedia Battle Frontier trainer list](https://bulbapedia.bulbagarden.net/wiki/List_of_Battle_Frontier_Trainers_in_Generation_III). The Ruby/Sapphire Battle Tower uses a different trainer list that is not currently supported.


> ```python
> from frontierbrain3.facilities.tower import TowerDatabase, get_tier, TIERS, BRAIN_IVS
> get_tier(250)
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


<br>

> ```python
> get_tier(150)
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


<br>

> ```python
> BRAIN_IVS
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
> tower.trainers.appearsInRound(8)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(100 trainers)
> [
>   'YOUNGSTER JAXON', 'YOUNGSTER LOGAN', 'LASS EMILEE', 'LASS JOSIE', 'CAMPER ARMANDO', 'CAMPER SKYLER',
>   'PICNICKER RUTH', 'PICNICKER MELODY', 'SWIMMER (M) PEDRO', 'SWIMMER (M) ERICK', 'SWIMMER (F) ELAINE',
>   'SWIMMER (F) JOYCE', 'POKÉFAN (M) TODD', 'POKÉFAN (M) GAVIN', 'POKÉFAN (F) MALORY', 'POKÉFAN (F) ESTHER',
>   'PKMN BREEDER (M) OSCAR', 'PKMN BREEDER (M) WILSON', 'PKMN BREEDER (F) CLARE', 'PKMN BREEDER (F) TESS',
>   'COOLTRAINER (M) LEON', 'COOLTRAINER (M) ALONZO', 'COOLTRAINER (M) VINCE', 'COOLTRAINER (M) BRYON',
>   'COOLTRAINER (F) AVA', 'COOLTRAINER (F) MIRIAM', 'COOLTRAINER (F) CARRIE', 'COOLTRAINER (F) GILLIAN',
>   'PKMN RANGER (M) TYLER', 'PKMN RANGER (M) CHAZ', 'PKMN RANGER (M) NELSON', 'PKMN RANGER (F) SHANIA',
>   'PKMN RANGER (F) STELLA', 'PKMN RANGER (F) DORINE', 'DRAGON TAMER MADDOX', 'DRAGON TAMER DAVIN',
>   'DRAGON TAMER TREVON', 'BLACK BELT MATEO', 'BLACK BELT BRET', 'BLACK BELT RAUL', 'BATTLE GIRL KAY',
>   'BATTLE GIRL ELENA', 'BATTLE GIRL ALANA', 'EXPERT (M) ALEXAS', 'EXPERT (M) WESTON', 'EXPERT (M) JASPER',
>   'EXPERT (F) NADIA', 'EXPERT (F) MIRANDA', 'EXPERT (F) EMMA', 'PSYCHIC (M) ROLANDO', 'PSYCHIC (M) STANLY',
>   'PSYCHIC (M) DARIO', 'PSYCHIC (F) KARLEE', 'PSYCHIC (F) JAYLIN', 'PSYCHIC (F) INGRID', 'HEX MANIAC DELILAH',
>   'HEX MANIAC CARLY', 'HEX MANIAC LEXIE', 'POKÉMANIAC MILLER', 'POKÉMANIAC MARV', 'POKÉMANIAC LAYTON',
>   'GENTLEMAN BROOKS', 'GENTLEMAN GREGORY', 'GENTLEMAN REESE', 'TRIATHLETE (M RUNNER) MASON',
>   'TRIATHLETE (M RUNNER) TOBY', 'TRIATHLETE (F RUNNER) DOROTHY', 'TRIATHLETE (F RUNNER) PIPER',
>   'TRIATHLETE (M SWIMMER) FINN', 'TRIATHLETE (M SWIMMER) SAMIR', 'TRIATHLETE (F SWIMMER) FIONA',
>   'TRIATHLETE (F SWIMMER) GLORIA', 'TRIATHLETE (M BIKER) NICO', 'TRIATHLETE (M BIKER) JEREMY',
>   'TRIATHLETE (F BIKER) CAITLIN', 'TRIATHLETE (F BIKER) REENA', 'BUG MANIAC AVERY', 'BUG MANIAC LIAM', 'FISHERMAN THEO',
>   'FISHERMAN BAILEY', 'RUIN MANIAC HUGO', 'RUIN MANIAC BRYCE', 'COLLECTOR GIDEON', 'COLLECTOR TRISTON',
>   'GUITARIST CHARLES', 'GUITARIST RAYMOND', 'BIRD KEEPER DIRK', 'BIRD KEEPER HAROLD', 'SAILOR OMAR', 'SAILOR PETER',
>   'HIKER DEV', 'HIKER COREY', 'KINDLER ANDRE', 'KINDLER FERRIS', 'PARASOL LADY ALIVIA', 'PARASOL LADY PAIGE',
>   'BEAUTY ANYA', 'BEAUTY DAWN', 'AROMA LADY ABBY', 'AROMA LADY GRETEL'
> ]
> ```
>
> </details>


<br>

> ```python
> tower.trainers.canBeLastInRound(7)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(80 trainers)
> [
>   'COOLTRAINER (M) LEON', 'COOLTRAINER (M) ALONZO', 'COOLTRAINER (M) VINCE', 'COOLTRAINER (M) BRYON',
>   'COOLTRAINER (F) AVA', 'COOLTRAINER (F) MIRIAM', 'COOLTRAINER (F) CARRIE', 'COOLTRAINER (F) GILLIAN',
>   'PKMN RANGER (M) TYLER', 'PKMN RANGER (M) CHAZ', 'PKMN RANGER (M) NELSON', 'PKMN RANGER (F) SHANIA',
>   'PKMN RANGER (F) STELLA', 'PKMN RANGER (F) DORINE', 'DRAGON TAMER MADDOX', 'DRAGON TAMER DAVIN',
>   'DRAGON TAMER TREVON', 'BLACK BELT MATEO', 'BLACK BELT BRET', 'BLACK BELT RAUL', 'BATTLE GIRL KAY',
>   'BATTLE GIRL ELENA', 'BATTLE GIRL ALANA', 'EXPERT (M) ALEXAS', 'EXPERT (M) WESTON', 'EXPERT (M) JASPER',
>   'EXPERT (F) NADIA', 'EXPERT (F) MIRANDA', 'EXPERT (F) EMMA', 'PSYCHIC (M) ROLANDO', 'PSYCHIC (M) STANLY',
>   'PSYCHIC (M) DARIO', 'PSYCHIC (F) KARLEE', 'PSYCHIC (F) JAYLIN', 'PSYCHIC (F) INGRID', 'HEX MANIAC DELILAH',
>   'HEX MANIAC CARLY', 'HEX MANIAC LEXIE', 'POKÉMANIAC MILLER', 'POKÉMANIAC MARV', 'POKÉMANIAC LAYTON',
>   'GENTLEMAN BROOKS', 'GENTLEMAN GREGORY', 'GENTLEMAN REESE', 'TRIATHLETE (M RUNNER) MASON',
>   'TRIATHLETE (M RUNNER) TOBY', 'TRIATHLETE (F RUNNER) DOROTHY', 'TRIATHLETE (F RUNNER) PIPER',
>   'TRIATHLETE (M SWIMMER) FINN', 'TRIATHLETE (M SWIMMER) SAMIR', 'TRIATHLETE (F SWIMMER) FIONA',
>   'TRIATHLETE (F SWIMMER) GLORIA', 'TRIATHLETE (M BIKER) NICO', 'TRIATHLETE (M BIKER) JEREMY',
>   'TRIATHLETE (F BIKER) CAITLIN', 'TRIATHLETE (F BIKER) REENA', 'BUG MANIAC AVERY', 'BUG MANIAC LIAM', 'FISHERMAN THEO',
>   'FISHERMAN BAILEY', 'RUIN MANIAC HUGO', 'RUIN MANIAC BRYCE', 'COLLECTOR GIDEON', 'COLLECTOR TRISTON',
>   'GUITARIST CHARLES', 'GUITARIST RAYMOND', 'BIRD KEEPER DIRK', 'BIRD KEEPER HAROLD', 'SAILOR OMAR', 'SAILOR PETER',
>   'HIKER DEV', 'HIKER COREY', 'KINDLER ANDRE', 'KINDLER FERRIS', 'PARASOL LADY ALIVIA', 'PARASOL LADY PAIGE',
>   'BEAUTY ANYA', 'BEAUTY DAWN', 'AROMA LADY ABBY', 'AROMA LADY GRETEL'
> ]
> ```
>
> </details>


<br>

> ```python
> tower.trainers.appearsInRound(8).hasPokemon("Metagross")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(38 trainers)
> [
>   'PKMN BREEDER (M) OSCAR', 'PKMN BREEDER (M) WILSON', 'PKMN BREEDER (F) CLARE', 'PKMN BREEDER (F) TESS',
>   'COOLTRAINER (M) ALONZO', 'COOLTRAINER (M) VINCE', 'COOLTRAINER (F) CARRIE', 'PKMN RANGER (M) TYLER',
>   'PKMN RANGER (M) CHAZ', 'PKMN RANGER (F) SHANIA', 'PKMN RANGER (F) STELLA', 'BLACK BELT RAUL', 'BATTLE GIRL ALANA',
>   'EXPERT (M) ALEXAS', 'EXPERT (F) NADIA', 'PSYCHIC (M) ROLANDO', 'PSYCHIC (M) STANLY', 'PSYCHIC (M) DARIO',
>   'PSYCHIC (F) KARLEE', 'PSYCHIC (F) JAYLIN', 'PSYCHIC (F) INGRID', 'POKÉMANIAC MILLER', 'POKÉMANIAC MARV',
>   'POKÉMANIAC LAYTON', 'GENTLEMAN BROOKS', 'GENTLEMAN GREGORY', 'TRIATHLETE (M RUNNER) MASON',
>   'TRIATHLETE (M RUNNER) TOBY', 'TRIATHLETE (F RUNNER) DOROTHY', 'TRIATHLETE (F RUNNER) PIPER',
>   'TRIATHLETE (M BIKER) NICO', 'TRIATHLETE (M BIKER) JEREMY', 'TRIATHLETE (F BIKER) CAITLIN',
>   'TRIATHLETE (F BIKER) REENA', 'RUIN MANIAC HUGO', 'RUIN MANIAC BRYCE', 'HIKER DEV', 'HIKER COREY'
> ]
> ```
>
> </details>


<br>

> ```python
> tower.trainers.appearsInRound(8).Not.hasPokemon("Starmie")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> TrainerCollection(56 trainers)
> [
>   'YOUNGSTER JAXON', 'YOUNGSTER LOGAN', 'LASS EMILEE', 'LASS JOSIE', 'CAMPER ARMANDO', 'CAMPER SKYLER',
>   'PICNICKER RUTH', 'PICNICKER MELODY', 'POKÉFAN (M) TODD', 'POKÉFAN (M) GAVIN', 'POKÉFAN (F) MALORY',
>   'POKÉFAN (F) ESTHER', 'COOLTRAINER (M) ALONZO', 'COOLTRAINER (M) BRYON', 'COOLTRAINER (F) AVA',
>   'COOLTRAINER (F) MIRIAM', 'COOLTRAINER (F) GILLIAN', 'PKMN RANGER (M) NELSON', 'PKMN RANGER (F) DORINE',
>   'DRAGON TAMER MADDOX', 'DRAGON TAMER DAVIN', 'DRAGON TAMER TREVON', 'BLACK BELT MATEO', 'BLACK BELT BRET',
>   'BLACK BELT RAUL', 'BATTLE GIRL KAY', 'BATTLE GIRL ELENA', 'BATTLE GIRL ALANA', 'EXPERT (M) ALEXAS',
>   'EXPERT (M) JASPER', 'EXPERT (F) NADIA', 'EXPERT (F) EMMA', 'HEX MANIAC DELILAH', 'HEX MANIAC CARLY',
>   'HEX MANIAC LEXIE', 'POKÉMANIAC MILLER', 'POKÉMANIAC MARV', 'POKÉMANIAC LAYTON', 'GENTLEMAN REESE',
>   'BUG MANIAC AVERY', 'BUG MANIAC LIAM', 'RUIN MANIAC HUGO', 'RUIN MANIAC BRYCE', 'COLLECTOR GIDEON',
>   'COLLECTOR TRISTON', 'GUITARIST CHARLES', 'BIRD KEEPER DIRK', 'BIRD KEEPER HAROLD', 'SAILOR OMAR', 'SAILOR PETER',
>   'HIKER DEV', 'HIKER COREY', 'KINDLER ANDRE', 'KINDLER FERRIS', 'BEAUTY ANYA', 'BEAUTY DAWN'
> ]
> ```
>
> </details>


### Random Team Generation

Generates a random trainer + 3-set team respecting species and item clause:


> ```python
> tower.random_team(8)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'Cooltrainer (M) VINCE: Latios-3, Metagross-3, Lapras-4'
> ```
>
> </details>


<br>

> ```python
> tower.random_team(8, trainer_class="Dragon Tamer")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'Dragon Tamer TREVON: Latias-8, Nidoking-4, Altaria-4'
> ```
>
> </details>


<br>

> ```python
> tower.random_team(name="Brady")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> 'Youngster BRADY: Smeargle-1, Shroomish-1, Ledyba-1'
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
> get_group(500)
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


<br>

> ```python
> fac = FactoryDatabase()
> pool = fac.sets_in_groups([4, 5, 6, 7, 8])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> pool = [
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
>   {'Pokemon': 'Marowak', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Thick Club', 'Abilities': ['Rock Head', 'Lightningrod'], 'Moves': ['bonemerang', 'rockslide', 'icywind', 'headbutt'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 388, 'DexNum': 105},
>   {'Pokemon': 'Quagsire', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Damp', 'Water Absorb'], 'Moves': ['earthquake', 'brickbreak', 'counter', 'mudslap'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 389, 'DexNum': 195},
>   {'Pokemon': 'Clefable', 'SetNum': 1, 'Nature': 'Brave', 'Item': 'Leftovers', 'Abilities': ['Cute Charm'], 'Moves': ['metronome', 'doubleteam', 'reflect', 'followme'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 390, 'DexNum': 36},
>   {'Pokemon': 'Hariyama', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Thick Fat', 'Guts'], 'Moves': ['crosschop', 'rockslide', 'counter', 'fakeout'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 391, 'DexNum': 297},
>   {'Pokemon': 'Raichu', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Static'], 'Moves': ['thunderbolt', 'quickattack', 'lightscreen', 'doubleteam'], 'EVs': [0, 0, 170, 170, 0, 170], 'Index': 392, 'DexNum': 26},
>   {'Pokemon': 'Dewgong', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'NeverMeltIce', 'Abilities': ['Thick Fat'], 'Moves': ['icebeam', 'icywind', 'headbutt', 'fakeout'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 393, 'DexNum': 87},
>   {'Pokemon': 'Manectric', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Magnet', 'Abilities': ['Static', 'Lightningrod'], 'Moves': ['thunderbolt', 'flash', 'quickattack', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 394, 'DexNum': 310},
>   {'Pokemon': 'Vileplume', 'SetNum': 1, 'Nature': 'Impish', 'Item': 'Persim Berry', 'Abilities': ['Chlorophyll'], 'Moves': ['sludgebomb', 'petaldance', 'moonlight', 'aromatherapy'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 395, 'DexNum': 45},
>   {'Pokemon': 'Victreebel', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Sitrus Berry', 'Abilities': ['Chlorophyll'], 'Moves': ['gigadrain', 'sleeppowder', 'sweetscent', 'synthesis'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 396, 'DexNum': 71},
>   {'Pokemon': 'Electrode', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Focus Band', 'Abilities': ['Soundproof', 'Static'], 'Moves': ['thunderbolt', 'swift', 'lightscreen', 'protect'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 397, 'DexNum': 101},
>   {'Pokemon': 'Exploud', 'SetNum': 1, 'Nature': 'Impish', 'Item': 'Chesto Berry', 'Abilities': ['Soundproof'], 'Moves': ['hypervoice', 'shadowball', 'sleeptalk', 'rest'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 398, 'DexNum': 295},
>   {'Pokemon': 'Shiftry', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Miracle Seed', 'Abilities': ['Chlorophyll', 'Early Bird'], 'Moves': ['gigadrain', 'faintattack', 'quickattack', 'fakeout'], 'EVs': [0, 0, 170, 170, 170, 0], 'Index': 399, 'DexNum': 275},
>   {'Pokemon': 'Glalie', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Petaya Berry', 'Abilities': ['Inner Focus'], 'Moves': ['icebeam', 'crunch', 'hail', 'protect'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 400, 'DexNum': 362},
>   {'Pokemon': 'Ludicolo', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Shell Bell', 'Abilities': ['Swift Swim', 'Rain Dish'], 'Moves': ['surf', 'raindance', 'thunderpunch', 'firepunch'], 'EVs': [170, 0, 170, 170, 0, 0], 'Index': 401, 'DexNum': 272},
>   {'Pokemon': 'Hypno', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'TwistedSpoon', 'Abilities': ['Insomnia'], 'Moves': ['thunderpunch', 'firepunch', 'icepunch', 'hypnosis'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 402, 'DexNum': 97},
>   {'Pokemon': 'Golem', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Rock Head', 'Sturdy'], 'Moves': ['earthquake', 'bodyslam', 'counter', 'rocktomb'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 403, 'DexNum': 76},
>   {'Pokemon': 'Rhydon', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Lightningrod', 'Rock Head'], 'Moves': ['earthquake', 'rocktomb', 'scaryface', 'brickbreak'], 'EVs': [170, 170, 0, 0, 170, 0], 'Index': 404, 'DexNum': 112},
>   {'Pokemon': 'Alakazam', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Focus Band', 'Abilities': ['Synchronize', 'Inner Focus'], 'Moves': ['thunderpunch', 'firepunch', 'icepunch', 'thunderwave'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 405, 'DexNum': 65},
>   {'Pokemon': 'Weezing', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Levitate'], 'Moves': ['sludgebomb', 'willowisp', 'shadowball', 'smokescreen'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 406, 'DexNum': 110},
>   {'Pokemon': 'Kangaskhan', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Early Bird'], 'Moves': ['dizzypunch', 'brickbreak', 'counter', 'fakeout'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 407, 'DexNum': 115},
>   {'Pokemon': 'Electabuzz', 'SetNum': 1, 'Nature': 'Relaxed', 'Item': 'Cheri Berry', 'Abilities': ['Static'], 'Moves': ['thunderbolt', 'thunderwave', 'brickbreak', 'lightscreen'], 'EVs': [170, 0, 170, 170, 0, 0], 'Index': 408, 'DexNum': 125},
>   {'Pokemon': 'Tauros', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Persim Berry', 'Abilities': ['Intimidate'], 'Moves': ['earthquake', 'thrash', 'swagger', 'facade'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 409, 'DexNum': 128},
>   {'Pokemon': 'Slowbro', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Shell Bell', 'Abilities': ['Oblivious', 'Own Tempo'], 'Moves': ['surf', 'raindance', 'headbutt', 'icepunch'], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 410, 'DexNum': 80},
>   {'Pokemon': 'Slowking', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Leftovers', 'Abilities': ['Oblivious', 'Own Tempo'], 'Moves': ['psychic', 'brickbreak', 'amnesia', 'attract'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 411, 'DexNum': 199},
>   {'Pokemon': 'Miltank', 'SetNum': 1, 'Nature': 'Careful', 'Item': 'Focus Band', 'Abilities': ['Thick Fat'], 'Moves': ['facade', 'shadowball', 'counter', 'milkdrink'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 412, 'DexNum': 241},
>   {'Pokemon': 'Altaria', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Cheri Berry', 'Abilities': ['Natural Cure'], 'Moves': ['dragonclaw', 'aerialace', 'refresh', 'bodyslam'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 413, 'DexNum': 334},
>   {'Pokemon': 'Nidoqueen', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Poison Point'], 'Moves': ['sludgebomb', 'doublekick', 'bodyslam', 'counter'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 414, 'DexNum': 31},
>   {'Pokemon': 'Nidoking', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Poison Point'], 'Moves': ['horndrill', 'doublekick', 'bodyslam', 'counter'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 415, 'DexNum': 34},
>   {'Pokemon': 'Magmar', 'SetNum': 1, 'Nature': 'Relaxed', 'Item': 'Rawst Berry', 'Abilities': ['Flame Body'], 'Moves': ['flamethrower', 'smokescreen', 'brickbreak', 'barrier'], 'EVs': [170, 0, 170, 170, 0, 0], 'Index': 416, 'DexNum': 126},
>   {'Pokemon': 'Cradily', 'SetNum': 1, 'Nature': 'Relaxed', 'Item': 'Leftovers', 'Abilities': ['Suction Cups'], 'Moves': ['gigadrain', 'rockslide', 'barrier', 'confuseray'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 417, 'DexNum': 346},
>   {'Pokemon': 'Armaldo', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Scope Lens', 'Abilities': ['Battle Armor'], 'Moves': ['slash', 'aerialace', 'ancientpower', 'protect'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 418, 'DexNum': 348},
>   {'Pokemon': 'Golduck', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Shell Bell', 'Abilities': ['Damp', 'Cloud Nine'], 'Moves': ['hydropump', 'dig', 'brickbreak', 'lightscreen'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 419, 'DexNum': 55},
>   {'Pokemon': 'Rapidash', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Charcoal', 'Abilities': ['Run Away', 'Flash Fire'], 'Moves': ['flamethrower', 'doublekick', 'quickattack', 'protect'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 420, 'DexNum': 78},
>   {'Pokemon': 'Muk', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Poison Barb', 'Abilities': ['Stench', 'Sticky Hold'], 'Moves': ['sludgebomb', 'bodyslam', 'screech', 'minimize'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 421, 'DexNum': 89},
>   {'Pokemon': 'Gengar', 'SetNum': 1, 'Nature': 'Timid', 'Item': 'Leftovers', 'Abilities': ['Levitate'], 'Moves': ['dreameater', 'hypnosis', 'confuseray', 'attract'], 'EVs': [170, 0, 0, 170, 0, 170], 'Index': 422, 'DexNum': 94},
>   {'Pokemon': 'Ampharos', 'SetNum': 1, 'Nature': 'Relaxed', 'Item': 'Magnet', 'Abilities': ['Static'], 'Moves': ['thunder', 'raindance', 'thunderwave', 'attract'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 423, 'DexNum': 181},
>   {'Pokemon': 'Scizor', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Swarm'], 'Moves': ['metalclaw', 'aerialace', 'counter', 'quickattack'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 424, 'DexNum': 212},
>   {'Pokemon': 'Heracross', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Swarm', 'Guts'], 'Moves': ['megahorn', 'brickbreak', 'rocktomb', 'counter'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 425, 'DexNum': 214},
>   {'Pokemon': 'Ursaring', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Quick Claw', 'Abilities': ['Guts'], 'Moves': ['megakick', 'crunch', 'aerialace', 'counter'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 426, 'DexNum': 217},
>   {'Pokemon': 'Houndoom', 'SetNum': 1, 'Nature': 'Quirky', 'Item': 'Focus Band', 'Abilities': ['Early Bird', 'Flash Fire'], 'Moves': ['flamethrower', 'shadowball', 'counter', 'willowisp'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 427, 'DexNum': 229},
>   {'Pokemon': 'Donphan', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Sturdy'], 'Moves': ['earthquake', 'ancientpower', 'swagger', 'rest'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 428, 'DexNum': 232},
>   {'Pokemon': 'Claydol', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['earthquake', 'rockslide', 'swagger', 'psychup'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 429, 'DexNum': 344},
>   {'Pokemon': 'Wailord', 'SetNum': 1, 'Nature': 'Sassy', 'Item': 'Shell Bell', 'Abilities': ['Water Veil', 'Oblivious'], 'Moves': ['surf', 'icywind', 'bodyslam', 'roar'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 430, 'DexNum': 321},
>   {'Pokemon': 'Ninetales', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Rawst Berry', 'Abilities': ['Flash Fire'], 'Moves': ['flamethrower', 'roar', 'confuseray', 'willowisp'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 431, 'DexNum': 38},
>   {'Pokemon': 'Machamp', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Scope Lens', 'Abilities': ['Guts'], 'Moves': ['crosschop', 'rockslide', 'counter', 'scaryface'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 432, 'DexNum': 68},
>   {'Pokemon': 'Shuckle', 'SetNum': 1, 'Nature': 'Brave', 'Item': 'Chesto Berry', 'Abilities': ['Sturdy'], 'Moves': ['rollout', 'defensecurl', 'sleeptalk', 'rest'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 433, 'DexNum': 213},
>   {'Pokemon': 'Steelix', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Sitrus Berry', 'Abilities': ['Rock Head', 'Sturdy'], 'Moves': ['earthquake', 'dragonbreath', 'rocktomb', 'roar'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 434, 'DexNum': 208},
>   {'Pokemon': 'Tentacruel', 'SetNum': 1, 'Nature': 'Impish', 'Item': 'Persim Berry', 'Abilities': ['Clear Body', 'Liquid Ooze'], 'Moves': ['sludgebomb', 'icywind', 'barrier', 'confuseray'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 435, 'DexNum': 73},
>   {'Pokemon': 'Aerodactyl', 'SetNum': 1, 'Nature': 'Adamant', 'Item': "King's Rock", 'Abilities': ['Rock Head', 'Pressure'], 'Moves': ['ancientpower', 'dragonbreath', 'aerialace', 'roar'], 'EVs': [170, 170, 0, 0, 0, 170], 'Index': 436, 'DexNum': 142},
>   {'Pokemon': 'Porygon2', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Trace'], 'Moves': ['triattack', 'aerialace', 'shadowball', 'recover'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 437, 'DexNum': 233},
>   {'Pokemon': 'Gardevoir', 'SetNum': 1, 'Nature': 'Timid', 'Item': 'Leftovers', 'Abilities': ['Synchronize', 'Trace'], 'Moves': ['dreameater', 'hypnosis', 'magicalleaf', 'reflect'], 'EVs': [170, 0, 170, 0, 0, 170], 'Index': 438, 'DexNum': 282},
>   {'Pokemon': 'Exeggutor', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Quick Claw', 'Abilities': ['Chlorophyll'], 'Moves': ['solarbeam', 'sunnyday', 'synthesis', 'lightscreen'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 439, 'DexNum': 103},
>   {'Pokemon': 'Starmie', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Illuminate', 'Natural Cure'], 'Moves': ['psychic', 'confuseray', 'thunderwave', 'recover'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 440, 'DexNum': 121},
>   {'Pokemon': 'Flygon', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Levitate'], 'Moves': ['earthquake', 'steelwing', 'faintattack', 'facade'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 441, 'DexNum': 330},
>   {'Pokemon': 'Venusaur', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Chesto Berry', 'Abilities': ['Overgrow'], 'Moves': ['gigadrain', 'sunnyday', 'synthesis', 'sleeppowder'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 442, 'DexNum': 3},
>   {'Pokemon': 'Vaporeon', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Mystic Water', 'Abilities': ['Water Absorb'], 'Moves': ['surf', 'roar', 'bite', 'quickattack'], 'EVs': [0, 0, 170, 170, 170, 0], 'Index': 443, 'DexNum': 134},
>   {'Pokemon': 'Jolteon', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Cheri Berry', 'Abilities': ['Volt Absorb'], 'Moves': ['thunderbolt', 'thunderwave', 'attract', 'protect'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 444, 'DexNum': 135},
>   {'Pokemon': 'Flareon', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Sitrus Berry', 'Abilities': ['Flash Fire'], 'Moves': ['flamethrower', 'roar', 'bite', 'sandattack'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 445, 'DexNum': 136},
>   {'Pokemon': 'Meganium', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Overgrow'], 'Moves': ['solarbeam', 'sunnyday', 'lightscreen', 'synthesis'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 446, 'DexNum': 154},
>   {'Pokemon': 'Espeon', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Synchronize'], 'Moves': ['psychic', 'charm', 'calmmind', 'batonpass'], 'EVs': [0, 0, 170, 0, 170, 170], 'Index': 447, 'DexNum': 196},
>   {'Pokemon': 'Umbreon', 'SetNum': 1, 'Nature': 'Bold', 'Item': 'BrightPowder', 'Abilities': ['Synchronize'], 'Moves': ['confuseray', 'faintattack', 'doubleteam', 'batonpass'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 448, 'DexNum': 197},
>   {'Pokemon': 'Blastoise', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Torrent'], 'Moves': ['hydropump', 'raindance', 'bite', 'seismictoss'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 449, 'DexNum': 9},
>   {'Pokemon': 'Feraligatr', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Lum Berry', 'Abilities': ['Torrent'], 'Moves': ['surf', 'raindance', 'aerialace', 'roar'], 'EVs': [170, 0, 0, 170, 170, 0], 'Index': 450, 'DexNum': 160},
>   {'Pokemon': 'Aggron', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Sturdy', 'Rock Head'], 'Moves': ['irontail', 'earthquake', 'aerialace', 'roar'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 451, 'DexNum': 306},
>   {'Pokemon': 'Blaziken', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Quick Claw', 'Abilities': ['Blaze'], 'Moves': ['flamethrower', 'sunnyday', 'doublekick', 'roar'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 452, 'DexNum': 257},
>   {'Pokemon': 'Walrein', 'SetNum': 1, 'Nature': 'Quiet', 'Item': 'Leftovers', 'Abilities': ['Thick Fat'], 'Moves': ['blizzard', 'hail', 'yawn', 'protect'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 453, 'DexNum': 365},
>   {'Pokemon': 'Sceptile', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Leftovers', 'Abilities': ['Overgrow'], 'Moves': ['leafblade', 'leechseed', 'aerialace', 'detect'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 454, 'DexNum': 254},
>   {'Pokemon': 'Charizard', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Focus Band', 'Abilities': ['Blaze'], 'Moves': ['fireblast', 'sunnyday', 'roar', 'scaryface'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 455, 'DexNum': 6},
>   {'Pokemon': 'Typhlosion', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Focus Band', 'Abilities': ['Blaze'], 'Moves': ['fireblast', 'sunnyday', 'smokescreen', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 456, 'DexNum': 157},
>   {'Pokemon': 'Lapras', 'SetNum': 1, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Water Absorb', 'Shell Armor'], 'Moves': ['surf', 'attract', 'confuseray', 'sing'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 457, 'DexNum': 131},
>   {'Pokemon': 'Crobat', 'SetNum': 1, 'Nature': 'Quirky', 'Item': "King's Rock", 'Abilities': ['Inner Focus'], 'Moves': ['sludgebomb', 'bite', 'astonish', 'screech'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 458, 'DexNum': 169},
>   {'Pokemon': 'Swampert', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Torrent'], 'Moves': ['earthquake', 'counter', 'rest', 'curse'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 459, 'DexNum': 260},
>   {'Pokemon': 'Gyarados', 'SetNum': 1, 'Nature': 'Careful', 'Item': 'Lum Berry', 'Abilities': ['Intimidate'], 'Moves': ['return', 'bite', 'thunderwave', 'dragondance'], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 460, 'DexNum': 130},
>   {'Pokemon': 'Snorlax', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Immunity', 'Thick Fat'], 'Moves': ['facade', 'shadowball', 'attract', 'doubleteam'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 461, 'DexNum': 143},
>   {'Pokemon': 'Kingdra', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Swift Swim'], 'Moves': ['hydropump', 'dragonbreath', 'icywind', 'attract'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 462, 'DexNum': 230},
>   {'Pokemon': 'Blissey', 'SetNum': 1, 'Nature': 'Bold', 'Item': 'BrightPowder', 'Abilities': ['Natural Cure', 'Serene Grace'], 'Moves': ['toxic', 'doubleteam', 'sing', 'softboiled'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 463, 'DexNum': 242},
>   {'Pokemon': 'Milotic', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Marvel Scale'], 'Moves': ['hydropump', 'icywind', 'recover', 'mirrorcoat'], 'EVs': [170, 0, 170, 170, 0, 0], 'Index': 464, 'DexNum': 350},
>   {'Pokemon': 'Arcanine', 'SetNum': 1, 'Nature': 'Adamant', 'Item': "King's Rock", 'Abilities': ['Intimidate', 'Flash Fire'], 'Moves': ['flamethrower', 'extremespeed', 'crunch', 'bodyslam'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 465, 'DexNum': 59},
>   {'Pokemon': 'Salamence', 'SetNum': 1, 'Nature': 'Hardy', 'Item': "King's Rock", 'Abilities': ['Intimidate'], 'Moves': ['dragonclaw', 'aerialace', 'headbutt', 'rockslide'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 466, 'DexNum': 373},
>   {'Pokemon': 'Metagross', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Clear Body'], 'Moves': ['meteormash', 'aerialace', 'facade', 'lightscreen'], 'EVs': [0, 170, 0, 0, 170, 170], 'Index': 467, 'DexNum': 376},
>   {'Pokemon': 'Slaking', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Scope Lens', 'Abilities': ['Truant'], 'Moves': ['yawn', 'bulkup', 'swagger', 'aerialace'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 468, 'DexNum': 289},
>   {'Pokemon': 'Dugtrio', 'SetNum': 2, 'Nature': 'Adamant', 'Item': "King's Rock", 'Abilities': ['Sand Veil', 'Arena Trap'], 'Moves': ['earthquake', 'ancientpower', 'aerialace', 'triattack'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 469, 'DexNum': 51},
>   {'Pokemon': 'Medicham', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'Salac Berry', 'Abilities': ['Pure Power'], 'Moves': ['reversal', 'endure', 'psychic', 'fakeout'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 470, 'DexNum': 308},
>   {'Pokemon': 'Marowak', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Thick Club', 'Abilities': ['Rock Head', 'Lightningrod'], 'Moves': ['earthquake', 'rockslide', 'swordsdance', 'icywind'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 471, 'DexNum': 105},
>   {'Pokemon': 'Quagsire', 'SetNum': 2, 'Nature': 'Sassy', 'Item': 'Leftovers', 'Abilities': ['Damp', 'Water Absorb'], 'Moves': ['curse', 'attract', 'yawn', 'ancientpower'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 472, 'DexNum': 195},
>   {'Pokemon': 'Misdreavus', 'SetNum': 2, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'attract', 'thunderwave', 'confuseray'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 473, 'DexNum': 200},
>   {'Pokemon': 'Fearow', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Keen Eye'], 'Moves': ['drillpeck', 'triattack', 'attract', 'pursuit'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 474, 'DexNum': 22},
>   {'Pokemon': 'Granbull', 'SetNum': 2, 'Nature': 'Quiet', 'Item': 'White Herb', 'Abilities': ['Intimidate'], 'Moves': ['overheat', 'thunderbolt', 'icepunch', 'facade'], 'EVs': [0, 0, 0, 255, 255, 0], 'Index': 475, 'DexNum': 210},
>   {'Pokemon': 'Jynx', 'SetNum': 2, 'Nature': 'Impish', 'Item': 'BrightPowder', 'Abilities': ['Oblivious'], 'Moves': ['perishsong', 'meanlook', 'lovelykiss', 'protect'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 476, 'DexNum': 124},
>   {'Pokemon': 'Dusclops', 'SetNum': 2, 'Nature': 'Impish', 'Item': 'Leftovers', 'Abilities': ['Pressure'], 'Moves': ['toxic', 'confuseray', 'doubleteam', 'protect'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 477, 'DexNum': 356},
>   {'Pokemon': 'Dodrio', 'SetNum': 2, 'Nature': 'Adamant', 'Item': "King's Rock", 'Abilities': ['Run Away', 'Early Bird'], 'Moves': ['drillpeck', 'doubleedge', 'faintattack', 'protect'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 478, 'DexNum': 85},
>   {'Pokemon': 'Mr. Mime', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Liechi Berry', 'Abilities': ['Soundproof'], 'Moves': ['batonpass', 'swagger', 'psychup', 'psychic'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 479, 'DexNum': 122},
>   {'Pokemon': 'Lanturn', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Salac Berry', 'Abilities': ['Volt Absorb', 'Illuminate'], 'Moves': ['flail', 'endure', 'thunderbolt', 'surf'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 480, 'DexNum': 171},
>   {'Pokemon': 'Breloom', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'BrightPowder', 'Abilities': ['Effect Spore'], 'Moves': ['gigadrain', 'leechseed', 'focuspunch', 'spore'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 481, 'DexNum': 286},
>   {'Pokemon': 'Forretress', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Sturdy'], 'Moves': ['earthquake', 'doubleedge', 'counter', 'protect'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 482, 'DexNum': 205},
>   {'Pokemon': 'Skarmory', 'SetNum': 2, 'Nature': 'Careful', 'Item': 'BrightPowder', 'Abilities': ['Keen Eye', 'Sturdy'], 'Moves': ['spikes', 'roar', 'drillpeck', 'toxic'], 'EVs': [170, 170, 0, 0, 170, 0], 'Index': 483, 'DexNum': 227},
>   {'Pokemon': 'Whiscash', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'Shell Bell', 'Abilities': ['Oblivious'], 'Moves': ['surf', 'earthquake', 'spark', 'futuresight'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 484, 'DexNum': 340},
>   {'Pokemon': 'Xatu', 'SetNum': 2, 'Nature': 'Impish', 'Item': 'Leftovers', 'Abilities': ['Synchronize', 'Early Bird'], 'Moves': ['fly', 'toxic', 'confuseray', 'attract'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 485, 'DexNum': 178},
>   {'Pokemon': 'Clefable', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Cute Charm'], 'Moves': ['meteormash', 'cosmicpower', 'doubleteam', 'followme'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 486, 'DexNum': 36},
>   {'Pokemon': 'Hariyama', 'SetNum': 2, 'Nature': 'Quiet', 'Item': 'Quick Claw', 'Abilities': ['Thick Fat', 'Guts'], 'Moves': ['crosschop', 'firepunch', 'icepunch', 'thunderpunch'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 487, 'DexNum': 297},
>   {'Pokemon': 'Raichu', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Static'], 'Moves': ['thunderbolt', 'reversal', 'endure', 'agility'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 488, 'DexNum': 26},
>   {'Pokemon': 'Dewgong', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Shell Bell', 'Abilities': ['Thick Fat'], 'Moves': ['blizzard', 'doubleedge', 'encore', 'disable'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 489, 'DexNum': 87},
>   {'Pokemon': 'Manectric', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Petaya Berry', 'Abilities': ['Static', 'Lightningrod'], 'Moves': ['thunder', 'raindance', 'crunch', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 490, 'DexNum': 310},
>   {'Pokemon': 'Vileplume', 'SetNum': 2, 'Nature': 'Bold', 'Item': 'BrightPowder', 'Abilities': ['Chlorophyll'], 'Moves': ['ingrain', 'doubleteam', 'toxic', 'gigadrain'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 491, 'DexNum': 45},
>   {'Pokemon': 'Victreebel', 'SetNum': 2, 'Nature': 'Serious', 'Item': 'Leftovers', 'Abilities': ['Chlorophyll'], 'Moves': ['gigadrain', 'sludgebomb', 'sleeppowder', 'attract'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 492, 'DexNum': 71},
>   {'Pokemon': 'Electrode', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Soundproof', 'Static'], 'Moves': ['thunder', 'raindance', 'doubleteam', 'swagger'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 493, 'DexNum': 101},
>   {'Pokemon': 'Exploud', 'SetNum': 2, 'Nature': 'Quirky', 'Item': 'Focus Band', 'Abilities': ['Soundproof'], 'Moves': ['solarbeam', 'sunnyday', 'earthquake', 'counter'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 494, 'DexNum': 295},
>   {'Pokemon': 'Shiftry', 'SetNum': 2, 'Nature': 'Impish', 'Item': 'Chesto Berry', 'Abilities': ['Chlorophyll', 'Early Bird'], 'Moves': ['leechseed', 'dig', 'doubleteam', 'rest'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 495, 'DexNum': 275},
>   {'Pokemon': 'Glalie', 'SetNum': 2, 'Nature': 'Quirky', 'Item': 'Salac Berry', 'Abilities': ['Inner Focus'], 'Moves': ['explosion', 'endure', 'bodyslam', 'icywind'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 496, 'DexNum': 362},
>   {'Pokemon': 'Ludicolo', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Swift Swim', 'Rain Dish'], 'Moves': ['surf', 'icebeam', 'thunderpunch', 'firepunch'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 497, 'DexNum': 272},
>   {'Pokemon': 'Hypno', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'TwistedSpoon', 'Abilities': ['Insomnia'], 'Moves': ['hypnosis', 'nightmare', 'dreameater', 'psychic'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 498, 'DexNum': 97},
>   {'Pokemon': 'Golem', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Rock Head', 'Sturdy'], 'Moves': ['focuspunch', 'substitute', 'doubleteam', 'rest'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 499, 'DexNum': 76},
>   {'Pokemon': 'Rhydon', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Lightningrod', 'Rock Head'], 'Moves': ['earthquake', 'horndrill', 'rockslide', 'brickbreak'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 500, 'DexNum': 112},
>   {'Pokemon': 'Alakazam', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Synchronize', 'Inner Focus'], 'Moves': ['psychic', 'calmmind', 'thunderwave', 'recover'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 501, 'DexNum': 65},
>   {'Pokemon': 'Weezing', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Sitrus Berry', 'Abilities': ['Levitate'], 'Moves': ['memento', 'sludgebomb', 'facade', 'destinybond'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 502, 'DexNum': 110},
>   {'Pokemon': 'Kangaskhan', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Early Bird'], 'Moves': ['crushclaw', 'shadowball', 'attract', 'rest'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 503, 'DexNum': 115},
>   {'Pokemon': 'Electabuzz', 'SetNum': 2, 'Nature': 'Quirky', 'Item': 'Leftovers', 'Abilities': ['Static'], 'Moves': ['thunder', 'raindance', 'attract', 'focuspunch'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 504, 'DexNum': 125},
>   {'Pokemon': 'Tauros', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Intimidate'], 'Moves': ['doubleedge', 'earthquake', 'doubleteam', 'rest'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 505, 'DexNum': 128},
>   {'Pokemon': 'Slowbro', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Leftovers', 'Abilities': ['Oblivious', 'Own Tempo'], 'Moves': ['surf', 'icebeam', 'calmmind', 'yawn'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 506, 'DexNum': 80},
>   {'Pokemon': 'Slowking', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Oblivious', 'Own Tempo'], 'Moves': ['yawn', 'thunderwave', 'surf', 'psychic'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 507, 'DexNum': 199},
>   {'Pokemon': 'Miltank', 'SetNum': 2, 'Nature': 'Careful', 'Item': 'Leftovers', 'Abilities': ['Thick Fat'], 'Moves': ['focuspunch', 'shadowball', 'attract', 'thunderwave'], 'EVs': [170, 170, 0, 0, 170, 0], 'Index': 508, 'DexNum': 241},
>   {'Pokemon': 'Altaria', 'SetNum': 2, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Natural Cure'], 'Moves': ['perishsong', 'dragonbreath', 'pursuit', 'attract'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 509, 'DexNum': 334},
>   {'Pokemon': 'Nidoqueen', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Shell Bell', 'Abilities': ['Poison Point'], 'Moves': ['doubleedge', 'earthquake', 'aerialace', 'rockslide'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 510, 'DexNum': 31},
>   {'Pokemon': 'Nidoking', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Shell Bell', 'Abilities': ['Poison Point'], 'Moves': ['megakick', 'earthquake', 'shadowball', 'brickbreak'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 511, 'DexNum': 34},
>   {'Pokemon': 'Magmar', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Quick Claw', 'Abilities': ['Flame Body'], 'Moves': ['fireblast', 'smokescreen', 'thunderpunch', 'confuseray'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 512, 'DexNum': 126},
>   {'Pokemon': 'Cradily', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Sitrus Berry', 'Abilities': ['Suction Cups'], 'Moves': ['earthquake', 'ancientpower', 'swagger', 'psychup'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 513, 'DexNum': 346},
>   {'Pokemon': 'Armaldo', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Battle Armor'], 'Moves': ['irontail', 'ancientpower', 'brickbreak', 'knockoff'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 514, 'DexNum': 348},
>   {'Pokemon': 'Golduck', 'SetNum': 2, 'Nature': 'Quirky', 'Item': 'Lum Berry', 'Abilities': ['Damp', 'Cloud Nine'], 'Moves': ['crosschop', 'surf', 'swagger', 'psychup'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 515, 'DexNum': 55},
>   {'Pokemon': 'Rapidash', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Leftovers', 'Abilities': ['Run Away', 'Flash Fire'], 'Moves': ['fireblast', 'bounce', 'doubleteam', 'attract'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 516, 'DexNum': 78},
>   {'Pokemon': 'Muk', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'Chesto Berry', 'Abilities': ['Stench', 'Sticky Hold'], 'Moves': ['curse', 'rest', 'sludgebomb', 'dynamicpunch'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 517, 'DexNum': 89},
>   {'Pokemon': 'Gengar', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Levitate'], 'Moves': ['sludgebomb', 'shadowball', 'confuseray', 'willowisp'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 518, 'DexNum': 94},
>   {'Pokemon': 'Ampharos', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'BrightPowder', 'Abilities': ['Static'], 'Moves': ['thunderpunch', 'firepunch', 'focuspunch', 'thunderwave'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 519, 'DexNum': 181},
>   {'Pokemon': 'Scizor', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Swarm'], 'Moves': ['silverwind', 'steelwing', 'swordsdance', 'lightscreen'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 520, 'DexNum': 212},
>   {'Pokemon': 'Heracross', 'SetNum': 2, 'Nature': 'Jolly', 'Item': 'Lum Berry', 'Abilities': ['Swarm', 'Guts'], 'Moves': ['megahorn', 'earthquake', 'attract', 'bulkup'], 'EVs': [255, 0, 0, 0, 0, 255], 'Index': 521, 'DexNum': 214},
>   {'Pokemon': 'Ursaring', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Guts'], 'Moves': ['doubleedge', 'earthquake', 'brickbreak', 'counter'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 522, 'DexNum': 217},
>   {'Pokemon': 'Houndoom', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Early Bird', 'Flash Fire'], 'Moves': ['fireblast', 'crunch', 'roar', 'rest'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 523, 'DexNum': 229},
>   {'Pokemon': 'Donphan', 'SetNum': 2, 'Nature': 'Jolly', 'Item': 'Quick Claw', 'Abilities': ['Sturdy'], 'Moves': ['flail', 'endure', 'earthquake', 'rocktomb'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 524, 'DexNum': 232},
>   {'Pokemon': 'Claydol', 'SetNum': 2, 'Nature': 'Calm', 'Item': 'Leftovers', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'earthquake', 'doubleteam', 'cosmicpower'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 525, 'DexNum': 344},
>   {'Pokemon': 'Wailord', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Water Veil', 'Oblivious'], 'Moves': ['doubleedge', 'rest', 'curse', 'amnesia'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 526, 'DexNum': 321},
>   {'Pokemon': 'Ninetales', 'SetNum': 2, 'Nature': 'Quirky', 'Item': 'Lum Berry', 'Abilities': ['Flash Fire'], 'Moves': ['heatwave', 'bodyslam', 'grudge', 'sunnyday'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 527, 'DexNum': 38},
>   {'Pokemon': 'Machamp', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Guts'], 'Moves': ['crosschop', 'earthquake', 'bulkup', 'rest'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 528, 'DexNum': 68},
>   {'Pokemon': 'Shuckle', 'SetNum': 2, 'Nature': 'Careful', 'Item': 'Leftovers', 'Abilities': ['Sturdy'], 'Moves': ['sandstorm', 'dig', 'flash', 'doubleteam'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 529, 'DexNum': 213},
>   {'Pokemon': 'Steelix', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'Leftovers', 'Abilities': ['Rock Head', 'Sturdy'], 'Moves': ['earthquake', 'dragonbreath', 'sandstorm', 'block'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 530, 'DexNum': 208},
>   {'Pokemon': 'Tentacruel', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'Leftovers', 'Abilities': ['Clear Body', 'Liquid Ooze'], 'Moves': ['toxic', 'gigadrain', 'confuseray', 'surf'], 'EVs': [170, 0, 170, 170, 0, 0], 'Index': 531, 'DexNum': 73},
>   {'Pokemon': 'Aerodactyl', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Choice Band', 'Abilities': ['Rock Head', 'Pressure'], 'Moves': ['hyperbeam', 'earthquake', 'aerialace', 'ancientpower'], 'EVs': [170, 170, 0, 0, 0, 170], 'Index': 532, 'DexNum': 142},
>   {'Pokemon': 'Porygon2', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Trace'], 'Moves': ['solarbeam', 'sunnyday', 'thunderwave', 'recover'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 533, 'DexNum': 233},
>   {'Pokemon': 'Gardevoir', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Chesto Berry', 'Abilities': ['Synchronize', 'Trace'], 'Moves': ['psychic', 'calmmind', 'doubleteam', 'rest'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 534, 'DexNum': 282},
>   {'Pokemon': 'Exeggutor', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'Chesto Berry', 'Abilities': ['Chlorophyll'], 'Moves': ['return', 'curse', 'sleeppowder', 'rest'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 535, 'DexNum': 103},
>   {'Pokemon': 'Starmie', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Illuminate', 'Natural Cure'], 'Moves': ['hydropump', 'thunder', 'raindance', 'recover'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 536, 'DexNum': 121},
>   {'Pokemon': 'Flygon', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Levitate'], 'Moves': ['solarbeam', 'fireblast', 'crunch', 'sunnyday'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 537, 'DexNum': 330},
>   {'Pokemon': 'Venusaur', 'SetNum': 2, 'Nature': 'Bold', 'Item': 'BrightPowder', 'Abilities': ['Overgrow'], 'Moves': ['leechseed', 'gigadrain', 'doubleteam', 'lightscreen'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 538, 'DexNum': 3},
>   {'Pokemon': 'Vaporeon', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Shell Bell', 'Abilities': ['Water Absorb'], 'Moves': ['surf', 'icebeam', 'bodyslam', 'shadowball'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 539, 'DexNum': 134},
>   {'Pokemon': 'Jolteon', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'Scope Lens', 'Abilities': ['Volt Absorb'], 'Moves': ['thunderbolt', 'dig', 'doublekick', 'roar'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 540, 'DexNum': 135},
>   {'Pokemon': 'Flareon', 'SetNum': 2, 'Nature': 'Relaxed', 'Item': 'Quick Claw', 'Abilities': ['Flash Fire'], 'Moves': ['curse', 'attract', 'doubleedge', 'shadowball'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 541, 'DexNum': 136},
>   {'Pokemon': 'Meganium', 'SetNum': 2, 'Nature': 'Calm', 'Item': 'Leftovers', 'Abilities': ['Overgrow'], 'Moves': ['leechseed', 'substitute', 'doubleteam', 'grasswhistle'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 542, 'DexNum': 154},
>   {'Pokemon': 'Espeon', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Chesto Berry', 'Abilities': ['Synchronize'], 'Moves': ['psychic', 'shadowball', 'calmmind', 'rest'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 543, 'DexNum': 196},
>   {'Pokemon': 'Umbreon', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Synchronize'], 'Moves': ['curse', 'screech', 'doubleteam', 'doubleedge'], 'EVs': [170, 170, 0, 0, 170, 0], 'Index': 544, 'DexNum': 197},
>   {'Pokemon': 'Blastoise', 'SetNum': 2, 'Nature': 'Brave', 'Item': 'Shell Bell', 'Abilities': ['Torrent'], 'Moves': ['hydropump', 'megakick', 'brickbreak', 'mirrorcoat'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 545, 'DexNum': 9},
>   {'Pokemon': 'Feraligatr', 'SetNum': 2, 'Nature': 'Sassy', 'Item': 'Quick Claw', 'Abilities': ['Torrent'], 'Moves': ['surf', 'dragonclaw', 'brickbreak', 'scaryface'], 'EVs': [170, 0, 0, 170, 170, 0], 'Index': 546, 'DexNum': 160},
>   {'Pokemon': 'Aggron', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Scope Lens', 'Abilities': ['Sturdy', 'Rock Head'], 'Moves': ['focuspunch', 'earthquake', 'rockslide', 'thunderwave'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 547, 'DexNum': 306},
>   {'Pokemon': 'Blaziken', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Scope Lens', 'Abilities': ['Blaze'], 'Moves': ['blazekick', 'megakick', 'thunderpunch', 'brickbreak'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 548, 'DexNum': 257},
>   {'Pokemon': 'Walrein', 'SetNum': 2, 'Nature': 'Quirky', 'Item': 'Focus Band', 'Abilities': ['Thick Fat'], 'Moves': ['earthquake', 'icebeam', 'curse', 'doubleteam'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 549, 'DexNum': 365},
>   {'Pokemon': 'Sceptile', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Overgrow'], 'Moves': ['leafblade', 'thunderpunch', 'attract', 'doubleteam'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 550, 'DexNum': 254},
>   {'Pokemon': 'Charizard', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Blaze'], 'Moves': ['earthquake', 'aerialace', 'dragondance', 'smokescreen'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 551, 'DexNum': 6},
>   {'Pokemon': 'Typhlosion', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'Scope Lens', 'Abilities': ['Blaze'], 'Moves': ['flamethrower', 'thunderpunch', 'aerialace', 'rockslide'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 552, 'DexNum': 157},
>   {'Pokemon': 'Lapras', 'SetNum': 2, 'Nature': 'Timid', 'Item': 'Quick Claw', 'Abilities': ['Water Absorb', 'Shell Armor'], 'Moves': ['surf', 'icebeam', 'bodyslam', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 553, 'DexNum': 131},
>   {'Pokemon': 'Crobat', 'SetNum': 2, 'Nature': 'Calm', 'Item': 'Leftovers', 'Abilities': ['Inner Focus'], 'Moves': ['toxic', 'gigadrain', 'confuseray', 'doubleteam'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 554, 'DexNum': 169},
>   {'Pokemon': 'Swampert', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Quick Claw', 'Abilities': ['Torrent'], 'Moves': ['surf', 'earthquake', 'counter', 'mirrorcoat'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 555, 'DexNum': 260},
>   {'Pokemon': 'Gyarados', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Intimidate'], 'Moves': ['hydropump', 'thunderbolt', 'fireblast', 'blizzard'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 556, 'DexNum': 130},
>   {'Pokemon': 'Snorlax', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Immunity', 'Thick Fat'], 'Moves': ['earthquake', 'rockslide', 'curse', 'rest'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 557, 'DexNum': 143},
>   {'Pokemon': 'Kingdra', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Chesto Berry', 'Abilities': ['Swift Swim'], 'Moves': ['surf', 'icebeam', 'dragonbreath', 'rest'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 558, 'DexNum': 230},
>   {'Pokemon': 'Blissey', 'SetNum': 2, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Natural Cure', 'Serene Grace'], 'Moves': ['seismictoss', 'sing', 'attract', 'substitute'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 559, 'DexNum': 242},
>   {'Pokemon': 'Milotic', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'Focus Band', 'Abilities': ['Marvel Scale'], 'Moves': ['surf', 'icebeam', 'safeguard', 'mirrorcoat'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 560, 'DexNum': 350},
>   {'Pokemon': 'Arcanine', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Lum Berry', 'Abilities': ['Intimidate', 'Flash Fire'], 'Moves': ['fireblast', 'sunnyday', 'crunch', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 561, 'DexNum': 59},
>   {'Pokemon': 'Salamence', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'Leftovers', 'Abilities': ['Intimidate'], 'Moves': ['doubleedge', 'crunch', 'swagger', 'protect'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 562, 'DexNum': 373},
>   {'Pokemon': 'Metagross', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Clear Body'], 'Moves': ['earthquake', 'meteormash', 'psychup', 'swagger'], 'EVs': [170, 0, 0, 0, 170, 170], 'Index': 563, 'DexNum': 376},
>   {'Pokemon': 'Slaking', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Truant'], 'Moves': ['megakick', 'shadowball', 'yawn', 'amnesia'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 564, 'DexNum': 289},
>   {'Pokemon': 'Dugtrio', 'SetNum': 3, 'Nature': 'Adamant', 'Item': "King's Rock", 'Abilities': ['Sand Veil', 'Arena Trap'], 'Moves': ['earthquake', 'doubleedge', 'sludgebomb', 'fissure'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 565, 'DexNum': 51},
>   {'Pokemon': 'Medicham', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Scope Lens', 'Abilities': ['Pure Power'], 'Moves': ['dynamicpunch', 'thunderpunch', 'icepunch', 'firepunch'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 566, 'DexNum': 308},
>   {'Pokemon': 'Misdreavus', 'SetNum': 3, 'Nature': 'Bold', 'Item': 'BrightPowder', 'Abilities': ['Levitate'], 'Moves': ['perishsong', 'meanlook', 'thunderwave', 'confuseray'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 567, 'DexNum': 200},
>   {'Pokemon': 'Fearow', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Scope Lens', 'Abilities': ['Keen Eye'], 'Moves': ['drillpeck', 'return', 'steelwing', 'faintattack'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 568, 'DexNum': 22},
>   {'Pokemon': 'Granbull', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Intimidate'], 'Moves': ['doubleedge', 'earthquake', 'sludgebomb', 'rockslide'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 569, 'DexNum': 210},
>   {'Pokemon': 'Jynx', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Quick Claw', 'Abilities': ['Oblivious'], 'Moves': ['dreameater', 'lovelykiss', 'attract', 'substitute'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 570, 'DexNum': 124},
>   {'Pokemon': 'Dusclops', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Pressure'], 'Moves': ['psychup', 'swagger', 'shadowball', 'earthquake'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 571, 'DexNum': 356},
>   {'Pokemon': 'Dodrio', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Run Away', 'Early Bird'], 'Moves': ['doubleedge', 'drillpeck', 'steelwing', 'faintattack'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 572, 'DexNum': 85},
>   {'Pokemon': 'Mr. Mime', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Choice Band', 'Abilities': ['Soundproof'], 'Moves': ['trick', 'torment', 'psychic', 'thunderbolt'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 573, 'DexNum': 122},
>   {'Pokemon': 'Lanturn', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Volt Absorb', 'Illuminate'], 'Moves': ['hydropump', 'thunder', 'confuseray', 'raindance'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 574, 'DexNum': 171},
>   {'Pokemon': 'Breloom', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Effect Spore'], 'Moves': ['irontail', 'focuspunch', 'attract', 'spore'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 575, 'DexNum': 286},
>   {'Pokemon': 'Forretress', 'SetNum': 3, 'Nature': 'Quiet', 'Item': 'Focus Band', 'Abilities': ['Sturdy'], 'Moves': ['explosion', 'earthquake', 'gigadrain', 'zapcannon'], 'EVs': [0, 170, 0, 170, 170, 0], 'Index': 576, 'DexNum': 205},
>   {'Pokemon': 'Whiscash', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Chesto Berry', 'Abilities': ['Oblivious'], 'Moves': ['sleeptalk', 'rest', 'surf', 'fissure'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 577, 'DexNum': 340},
>   {'Pokemon': 'Xatu', 'SetNum': 3, 'Nature': 'Jolly', 'Item': "King's Rock", 'Abilities': ['Synchronize', 'Early Bird'], 'Moves': ['drillpeck', 'psychic', 'gigadrain', 'steelwing'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 578, 'DexNum': 178},
>   {'Pokemon': 'Skarmory', 'SetNum': 3, 'Nature': 'Careful', 'Item': 'Chesto Berry', 'Abilities': ['Keen Eye', 'Sturdy'], 'Moves': ['toxic', 'curse', 'rest', 'fly'], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 579, 'DexNum': 227},
>   {'Pokemon': 'Marowak', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Thick Club', 'Abilities': ['Rock Head', 'Lightningrod'], 'Moves': ['earthquake', 'rockslide', 'swordsdance', 'brickbreak'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 580, 'DexNum': 105},
>   {'Pokemon': 'Quagsire', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Damp', 'Water Absorb'], 'Moves': ['earthquake', 'sludgebomb', 'doubleedge', 'curse'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 581, 'DexNum': 195},
>   {'Pokemon': 'Clefable', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Cute Charm'], 'Moves': ['thunderbolt', 'icebeam', 'flamethrower', 'magicalleaf'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 582, 'DexNum': 36},
>   {'Pokemon': 'Hariyama', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Thick Fat', 'Guts'], 'Moves': ['crosschop', 'earthquake', 'rockslide', 'facade'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 583, 'DexNum': 297},
>   {'Pokemon': 'Raichu', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'Cheri Berry', 'Abilities': ['Static'], 'Moves': ['thunder', 'raindance', 'irontail', 'attract'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 584, 'DexNum': 26},
>   {'Pokemon': 'Dewgong', 'SetNum': 3, 'Nature': 'Bold', 'Item': 'Chesto Berry', 'Abilities': ['Thick Fat'], 'Moves': ['horndrill', 'sheercold', 'sleeptalk', 'rest'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 585, 'DexNum': 87},
>   {'Pokemon': 'Manectric', 'SetNum': 3, 'Nature': 'Quirky', 'Item': 'Lum Berry', 'Abilities': ['Static', 'Lightningrod'], 'Moves': ['thunderbolt', 'irontail', 'thunderwave', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 586, 'DexNum': 310},
>   {'Pokemon': 'Vileplume', 'SetNum': 3, 'Nature': 'Quirky', 'Item': 'Leftovers', 'Abilities': ['Chlorophyll'], 'Moves': ['attract', 'stunspore', 'sludgebomb', 'gigadrain'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 587, 'DexNum': 45},
>   {'Pokemon': 'Victreebel', 'SetNum': 3, 'Nature': 'Quirky', 'Item': 'BrightPowder', 'Abilities': ['Chlorophyll'], 'Moves': ['stunspore', 'ingrain', 'gigadrain', 'sludgebomb'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 588, 'DexNum': 71},
>   {'Pokemon': 'Electrode', 'SetNum': 3, 'Nature': 'Naughty', 'Item': 'Liechi Berry', 'Abilities': ['Soundproof', 'Static'], 'Moves': ['explosion', 'thunderbolt', 'thunderwave', 'endure'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 589, 'DexNum': 101},
>   {'Pokemon': 'Exploud', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'White Herb', 'Abilities': ['Soundproof'], 'Moves': ['overheat', 'icebeam', 'thunderpunch', 'extrasensory'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 590, 'DexNum': 295},
>   {'Pokemon': 'Shiftry', 'SetNum': 3, 'Nature': 'Quirky', 'Item': 'Focus Band', 'Abilities': ['Chlorophyll', 'Early Bird'], 'Moves': ['solarbeam', 'sunnyday', 'explosion', 'synthesis'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 591, 'DexNum': 275},
>   {'Pokemon': 'Glalie', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Shell Bell', 'Abilities': ['Inner Focus'], 'Moves': ['blizzard', 'earthquake', 'doubleedge', 'shadowball'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 592, 'DexNum': 362},
>   {'Pokemon': 'Ludicolo', 'SetNum': 3, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Swift Swim', 'Rain Dish'], 'Moves': ['leechseed', 'raindance', 'doubleteam', 'gigadrain'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 593, 'DexNum': 272},
>   {'Pokemon': 'Hypno', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Insomnia'], 'Moves': ['psychup', 'swagger', 'megakick', 'shadowball'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 594, 'DexNum': 97},
>   {'Pokemon': 'Golem', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Rock Head', 'Sturdy'], 'Moves': ['explosion', 'earthquake', 'flamethrower', 'brickbreak'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 595, 'DexNum': 76},
>   {'Pokemon': 'Rhydon', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Lightningrod', 'Rock Head'], 'Moves': ['megahorn', 'crushclaw', 'earthquake', 'horndrill'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 596, 'DexNum': 112},
>   {'Pokemon': 'Alakazam', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Choice Band', 'Abilities': ['Synchronize', 'Inner Focus'], 'Moves': ['trick', 'disable', 'psychic', 'skillswap'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 597, 'DexNum': 65},
>   {'Pokemon': 'Weezing', 'SetNum': 3, 'Nature': 'Quirky', 'Item': 'Focus Band', 'Abilities': ['Levitate'], 'Moves': ['explosion', 'sludgebomb', 'flamethrower', 'thunderbolt'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 598, 'DexNum': 110},
>   {'Pokemon': 'Kangaskhan', 'SetNum': 3, 'Nature': 'Jolly', 'Item': 'Salac Berry', 'Abilities': ['Early Bird'], 'Moves': ['reversal', 'endure', 'thunderbolt', 'earthquake'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 599, 'DexNum': 115},
>   {'Pokemon': 'Electabuzz', 'SetNum': 3, 'Nature': 'Quirky', 'Item': 'Lum Berry', 'Abilities': ['Static'], 'Moves': ['firepunch', 'icepunch', 'thunderbolt', 'crosschop'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 600, 'DexNum': 125},
>   {'Pokemon': 'Tauros', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'Leftovers', 'Abilities': ['Intimidate'], 'Moves': ['doubleedge', 'earthquake', 'flamethrower', 'icebeam'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 601, 'DexNum': 128},
>   {'Pokemon': 'Slowbro', 'SetNum': 3, 'Nature': 'Quiet', 'Item': 'Quick Claw', 'Abilities': ['Oblivious', 'Own Tempo'], 'Moves': ['surf', 'psychic', 'shadowball', 'attract'], 'EVs': [0, 0, 0, 255, 255, 0], 'Index': 602, 'DexNum': 80},
>   {'Pokemon': 'Slowking', 'SetNum': 3, 'Nature': 'Quiet', 'Item': 'Quick Claw', 'Abilities': ['Oblivious', 'Own Tempo'], 'Moves': ['psychic', 'surf', 'icebeam', 'earthquake'], 'EVs': [0, 170, 170, 170, 0, 0], 'Index': 603, 'DexNum': 199},
>   {'Pokemon': 'Miltank', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Salac Berry', 'Abilities': ['Thick Fat'], 'Moves': ['reversal', 'endure', 'earthquake', 'shadowball'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 604, 'DexNum': 241},
>   {'Pokemon': 'Altaria', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Natural Cure'], 'Moves': ['sing', 'dragondance', 'earthquake', 'aerialace'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 605, 'DexNum': 334},
>   {'Pokemon': 'Nidoqueen', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Poison Point'], 'Moves': ['thunderbolt', 'flamethrower', 'icebeam', 'crunch'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 606, 'DexNum': 31},
>   {'Pokemon': 'Nidoking', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Leppa Berry', 'Abilities': ['Poison Point'], 'Moves': ['horndrill', 'fireblast', 'blizzard', 'surf'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 607, 'DexNum': 34},
>   {'Pokemon': 'Magmar', 'SetNum': 3, 'Nature': 'Impish', 'Item': 'Scope Lens', 'Abilities': ['Flame Body'], 'Moves': ['megakick', 'crosschop', 'irontail', 'counter'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 608, 'DexNum': 126},
>   {'Pokemon': 'Cradily', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Leftovers', 'Abilities': ['Suction Cups'], 'Moves': ['substitute', 'solarbeam', 'sunnyday', 'recover'], 'EVs': [0, 0, 170, 170, 170, 0], 'Index': 609, 'DexNum': 346},
>   {'Pokemon': 'Armaldo', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Battle Armor'], 'Moves': ['earthquake', 'rockslide', 'brickbreak', 'swordsdance'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 610, 'DexNum': 348},
>   {'Pokemon': 'Golduck', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'Shell Bell', 'Abilities': ['Damp', 'Cloud Nine'], 'Moves': ['hydropump', 'crosschop', 'blizzard', 'protect'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 611, 'DexNum': 55},
>   {'Pokemon': 'Rapidash', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'White Herb', 'Abilities': ['Run Away', 'Flash Fire'], 'Moves': ['overheat', 'solarbeam', 'sunnyday', 'hypnosis'], 'EVs': [170, 0, 0, 170, 0, 170], 'Index': 612, 'DexNum': 78},
>   {'Pokemon': 'Muk', 'SetNum': 3, 'Nature': 'Quiet', 'Item': 'Lum Berry', 'Abilities': ['Stench', 'Sticky Hold'], 'Moves': ['sludgebomb', 'thunderbolt', 'flamethrower', 'icepunch'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 613, 'DexNum': 89},
>   {'Pokemon': 'Gengar', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Quick Claw', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'thunderbolt', 'gigadrain', 'skillswap'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 614, 'DexNum': 94},
>   {'Pokemon': 'Ampharos', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Focus Band', 'Abilities': ['Static'], 'Moves': ['thunderbolt', 'megakick', 'irontail', 'brickbreak'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 615, 'DexNum': 181},
>   {'Pokemon': 'Scizor', 'SetNum': 3, 'Nature': 'Careful', 'Item': 'Focus Band', 'Abilities': ['Swarm'], 'Moves': ['reversal', 'endure', 'agility', 'slash'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 616, 'DexNum': 212},
>   {'Pokemon': 'Heracross', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Swarm', 'Guts'], 'Moves': ['megahorn', 'earthquake', 'rockslide', 'brickbreak'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 617, 'DexNum': 214},
>   {'Pokemon': 'Ursaring', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Guts'], 'Moves': ['firepunch', 'thunderpunch', 'icepunch', 'crunch'], 'EVs': [170, 0, 0, 170, 0, 170], 'Index': 618, 'DexNum': 217},
>   {'Pokemon': 'Houndoom', 'SetNum': 3, 'Nature': 'Quirky', 'Item': 'White Herb', 'Abilities': ['Early Bird', 'Flash Fire'], 'Moves': ['overheat', 'shadowball', 'sludgebomb', 'doubleedge'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 619, 'DexNum': 229},
>   {'Pokemon': 'Donphan', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Sturdy'], 'Moves': ['fissure', 'earthquake', 'rockslide', 'secretpower'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 620, 'DexNum': 232},
>   {'Pokemon': 'Claydol', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'icebeam', 'solarbeam', 'sunnyday'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 621, 'DexNum': 344},
>   {'Pokemon': 'Wailord', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Chesto Berry', 'Abilities': ['Water Veil', 'Oblivious'], 'Moves': ['hydropump', 'fissure', 'doubleteam', 'rest'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 622, 'DexNum': 321},
>   {'Pokemon': 'Ninetales', 'SetNum': 3, 'Nature': 'Quirky', 'Item': 'BrightPowder', 'Abilities': ['Flash Fire'], 'Moves': ['fireblast', 'irontail', 'confuseray', 'attract'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 623, 'DexNum': 38},
>   {'Pokemon': 'Machamp', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Quick Claw', 'Abilities': ['Guts'], 'Moves': ['crosschop', 'fireblast', 'thunderpunch', 'icepunch'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 624, 'DexNum': 68},
>   {'Pokemon': 'Shuckle', 'SetNum': 3, 'Nature': 'Careful', 'Item': 'Leftovers', 'Abilities': ['Sturdy'], 'Moves': ['substitute', 'attract', 'toxic', 'doubleteam'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 625, 'DexNum': 213},
>   {'Pokemon': 'Steelix', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Rock Head', 'Sturdy'], 'Moves': ['earthquake', 'bodyslam', 'rockslide', 'explosion'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 626, 'DexNum': 208},
>   {'Pokemon': 'Tentacruel', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Shell Bell', 'Abilities': ['Clear Body', 'Liquid Ooze'], 'Moves': ['surf', 'gigadrain', 'icebeam', 'mirrorcoat'], 'EVs': [0, 0, 170, 170, 0, 170], 'Index': 627, 'DexNum': 73},
>   {'Pokemon': 'Aerodactyl', 'SetNum': 3, 'Nature': 'Hardy', 'Item': "King's Rock", 'Abilities': ['Rock Head', 'Pressure'], 'Moves': ['doubleedge', 'rockslide', 'fireblast', 'dragonclaw'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 628, 'DexNum': 142},
>   {'Pokemon': 'Porygon2', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Trace'], 'Moves': ['psychic', 'triattack', 'thunderwave', 'recover'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 629, 'DexNum': 233},
>   {'Pokemon': 'Gardevoir', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Synchronize', 'Trace'], 'Moves': ['psychic', 'icepunch', 'firepunch', 'magicalleaf'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 630, 'DexNum': 282},
>   {'Pokemon': 'Exeggutor', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Leftovers', 'Abilities': ['Chlorophyll'], 'Moves': ['leechseed', 'gigadrain', 'toxic', 'explosion'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 631, 'DexNum': 103},
>   {'Pokemon': 'Starmie', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Illuminate', 'Natural Cure'], 'Moves': ['surf', 'psychic', 'thunderbolt', 'icebeam'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 632, 'DexNum': 121},
>   {'Pokemon': 'Flygon', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Scope Lens', 'Abilities': ['Levitate'], 'Moves': ['earthquake', 'dragonclaw', 'flamethrower', 'gigadrain'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 633, 'DexNum': 330},
>   {'Pokemon': 'Venusaur', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Scope Lens', 'Abilities': ['Overgrow'], 'Moves': ['doubleedge', 'sludgebomb', 'earthquake', 'sleeppowder'], 'EVs': [0, 170, 170, 0, 170, 0], 'Index': 634, 'DexNum': 3},
>   {'Pokemon': 'Vaporeon', 'SetNum': 3, 'Nature': 'Calm', 'Item': 'Quick Claw', 'Abilities': ['Water Absorb'], 'Moves': ['surf', 'icebeam', 'acidarmor', 'batonpass'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 635, 'DexNum': 134},
>   {'Pokemon': 'Jolteon', 'SetNum': 3, 'Nature': 'Bold', 'Item': 'BrightPowder', 'Abilities': ['Volt Absorb'], 'Moves': ['thunderbolt', 'thunderwave', 'agility', 'batonpass'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 636, 'DexNum': 135},
>   {'Pokemon': 'Flareon', 'SetNum': 3, 'Nature': 'Jolly', 'Item': 'Quick Claw', 'Abilities': ['Flash Fire'], 'Moves': ['shadowball', 'flail', 'endure', 'overheat'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 637, 'DexNum': 136},
>   {'Pokemon': 'Meganium', 'SetNum': 3, 'Nature': 'Jolly', 'Item': 'Salac Berry', 'Abilities': ['Overgrow'], 'Moves': ['earthquake', 'flail', 'endure', 'gigadrain'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 638, 'DexNum': 154},
>   {'Pokemon': 'Espeon', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Synchronize'], 'Moves': ['psychic', 'bite', 'wish', 'reflect'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 639, 'DexNum': 196},
>   {'Pokemon': 'Umbreon', 'SetNum': 3, 'Nature': 'Bold', 'Item': 'BrightPowder', 'Abilities': ['Synchronize'], 'Moves': ['swagger', 'psychup', 'attract', 'shadowball'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 640, 'DexNum': 197},
>   {'Pokemon': 'Blastoise', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'Focus Band', 'Abilities': ['Torrent'], 'Moves': ['surf', 'earthquake', 'icebeam', 'counter'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 641, 'DexNum': 9},
>   {'Pokemon': 'Feraligatr', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Scope Lens', 'Abilities': ['Torrent'], 'Moves': ['hydropump', 'crunch', 'earthquake', 'rockslide'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 642, 'DexNum': 160},
>   {'Pokemon': 'Aggron', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Sturdy', 'Rock Head'], 'Moves': ['surf', 'thunder', 'fireblast', 'blizzard'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 643, 'DexNum': 306},
>   {'Pokemon': 'Blaziken', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Salac Berry', 'Abilities': ['Blaze'], 'Moves': ['overheat', 'earthquake', 'endure', 'reversal'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 644, 'DexNum': 257},
>   {'Pokemon': 'Walrein', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Quick Claw', 'Abilities': ['Thick Fat'], 'Moves': ['sheercold', 'fissure', 'surf', 'attract'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 645, 'DexNum': 365},
>   {'Pokemon': 'Sceptile', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'Scope Lens', 'Abilities': ['Overgrow'], 'Moves': ['leafblade', 'earthquake', 'crushclaw', 'aerialace'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 646, 'DexNum': 254},
>   {'Pokemon': 'Charizard', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Blaze'], 'Moves': ['flamethrower', 'dragonclaw', 'bite', 'brickbreak'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 647, 'DexNum': 6},
>   {'Pokemon': 'Typhlosion', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Salac Berry', 'Abilities': ['Blaze'], 'Moves': ['earthquake', 'overheat', 'endure', 'reversal'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 648, 'DexNum': 157},
>   {'Pokemon': 'Lapras', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'BrightPowder', 'Abilities': ['Water Absorb', 'Shell Armor'], 'Moves': ['doubleedge', 'psychic', 'confuseray', 'dragondance'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 649, 'DexNum': 131},
>   {'Pokemon': 'Crobat', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Scope Lens', 'Abilities': ['Inner Focus'], 'Moves': ['aircutter', 'doubleedge', 'shadowball', 'screech'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 650, 'DexNum': 169},
>   {'Pokemon': 'Swampert', 'SetNum': 3, 'Nature': 'Brave', 'Item': 'Shell Bell', 'Abilities': ['Torrent'], 'Moves': ['surf', 'earthquake', 'icebeam', 'counter'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 651, 'DexNum': 260},
>   {'Pokemon': 'Gyarados', 'SetNum': 3, 'Nature': 'Quirky', 'Item': 'Quick Claw', 'Abilities': ['Intimidate'], 'Moves': ['surf', 'thunder', 'raindance', 'earthquake'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 652, 'DexNum': 130},
>   {'Pokemon': 'Snorlax', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Immunity', 'Thick Fat'], 'Moves': ['megakick', 'shadowball', 'swagger', 'psychup'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 653, 'DexNum': 143},
>   {'Pokemon': 'Kingdra', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Salac Berry', 'Abilities': ['Swift Swim'], 'Moves': ['flail', 'hydropump', 'dragondance', 'endure'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 654, 'DexNum': 230},
>   {'Pokemon': 'Blissey', 'SetNum': 3, 'Nature': 'Bold', 'Item': 'Focus Band', 'Abilities': ['Natural Cure', 'Serene Grace'], 'Moves': ['fireblast', 'blizzard', 'calmmind', 'softboiled'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 655, 'DexNum': 242},
>   {'Pokemon': 'Milotic', 'SetNum': 3, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Marvel Scale'], 'Moves': ['surf', 'blizzard', 'attract', 'recover'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 656, 'DexNum': 350},
>   {'Pokemon': 'Arcanine', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'White Herb', 'Abilities': ['Intimidate', 'Flash Fire'], 'Moves': ['overheat', 'extremespeed', 'crunch', 'aerialace'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 657, 'DexNum': 59},
>   {'Pokemon': 'Salamence', 'SetNum': 3, 'Nature': 'Hardy', 'Item': 'Salac Berry', 'Abilities': ['Intimidate'], 'Moves': ['doubleedge', 'earthquake', 'crunch', 'endure'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 658, 'DexNum': 373},
>   {'Pokemon': 'Metagross', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Clear Body'], 'Moves': ['earthquake', 'meteormash', 'doubleteam', 'rest'], 'EVs': [170, 170, 0, 0, 0, 170], 'Index': 659, 'DexNum': 376},
>   {'Pokemon': 'Slaking', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Choice Band', 'Abilities': ['Truant'], 'Moves': ['earthquake', 'shadowball', 'aerialace', 'brickbreak'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 660, 'DexNum': 289},
>   {'Pokemon': 'Dugtrio', 'SetNum': 4, 'Nature': 'Adamant', 'Item': "King's Rock", 'Abilities': ['Sand Veil', 'Arena Trap'], 'Moves': ['earthquake', 'doubleedge', 'rockslide', 'fissure'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 661, 'DexNum': 51},
>   {'Pokemon': 'Medicham', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Lum Berry', 'Abilities': ['Pure Power'], 'Moves': ['megakick', 'psychic', 'shadowball', 'rockslide'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 662, 'DexNum': 308},
>   {'Pokemon': 'Misdreavus', 'SetNum': 4, 'Nature': 'Timid', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['destinybond', 'psychic', 'shadowball', 'thunderbolt'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 663, 'DexNum': 200},
>   {'Pokemon': 'Fearow', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Lum Berry', 'Abilities': ['Keen Eye'], 'Moves': ['drillpeck', 'doubleedge', 'steelwing', 'skyattack'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 664, 'DexNum': 22},
>   {'Pokemon': 'Granbull', 'SetNum': 4, 'Nature': 'Brave', 'Item': 'Choice Band', 'Abilities': ['Intimidate'], 'Moves': ['megakick', 'earthquake', 'crunch', 'shadowball'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 665, 'DexNum': 210},
>   {'Pokemon': 'Jynx', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Oblivious'], 'Moves': ['psychic', 'icebeam', 'lovelykiss', 'faketears'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 666, 'DexNum': 124},
>   {'Pokemon': 'Dusclops', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Pressure'], 'Moves': ['doubleedge', 'shadowball', 'curse', 'rest'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 667, 'DexNum': 356},
>   {'Pokemon': 'Dodrio', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Salac Berry', 'Abilities': ['Run Away', 'Early Bird'], 'Moves': ['flail', 'endure', 'drillpeck', 'facade'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 668, 'DexNum': 85},
>   {'Pokemon': 'Mr. Mime', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Soundproof'], 'Moves': ['psychic', 'thunderbolt', 'icepunch', 'firepunch'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 669, 'DexNum': 122},
>   {'Pokemon': 'Lanturn', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Volt Absorb', 'Illuminate'], 'Moves': ['surf', 'thunderbolt', 'icebeam', 'confuseray'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 670, 'DexNum': 171},
>   {'Pokemon': 'Breloom', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Effect Spore'], 'Moves': ['focuspunch', 'sludgebomb', 'spore', 'doubleteam'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 671, 'DexNum': 286},
>   {'Pokemon': 'Forretress', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Sturdy'], 'Moves': ['explosion', 'earthquake', 'rockslide', 'doubleedge'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 672, 'DexNum': 205},
>   {'Pokemon': 'Whiscash', 'SetNum': 4, 'Nature': 'Quiet', 'Item': 'Quick Claw', 'Abilities': ['Oblivious'], 'Moves': ['fissure', 'surf', 'earthquake', 'icebeam'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 673, 'DexNum': 340},
>   {'Pokemon': 'Xatu', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Petaya Berry', 'Abilities': ['Synchronize', 'Early Bird'], 'Moves': ['psychic', 'drillpeck', 'shadowball', 'confuseray'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 674, 'DexNum': 178},
>   {'Pokemon': 'Skarmory', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Keen Eye', 'Sturdy'], 'Moves': ['drillpeck', 'steelwing', 'counter', 'rockslide'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 675, 'DexNum': 227},
>   {'Pokemon': 'Marowak', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Thick Club', 'Abilities': ['Rock Head', 'Lightningrod'], 'Moves': ['earthquake', 'rockslide', 'swordsdance', 'megakick'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 676, 'DexNum': 105},
>   {'Pokemon': 'Quagsire', 'SetNum': 4, 'Nature': 'Sassy', 'Item': 'Leftovers', 'Abilities': ['Damp', 'Water Absorb'], 'Moves': ['surf', 'earthquake', 'icebeam', 'amnesia'], 'EVs': [0, 170, 0, 170, 170, 0], 'Index': 677, 'DexNum': 195},
>   {'Pokemon': 'Clefable', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Focus Band', 'Abilities': ['Cute Charm'], 'Moves': ['megakick', 'psychic', 'shadowball', 'softboiled'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 678, 'DexNum': 36},
>   {'Pokemon': 'Hariyama', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Scope Lens', 'Abilities': ['Thick Fat', 'Guts'], 'Moves': ['crosschop', 'earthquake', 'rockslide', 'fakeout'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 679, 'DexNum': 297},
>   {'Pokemon': 'Raichu', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'BrightPowder', 'Abilities': ['Static'], 'Moves': ['thunderbolt', 'thunderwave', 'protect', 'megakick'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 680, 'DexNum': 26},
>   {'Pokemon': 'Dewgong', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Lum Berry', 'Abilities': ['Thick Fat'], 'Moves': ['sheercold', 'icebeam', 'surf', 'signalbeam'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 681, 'DexNum': 87},
>   {'Pokemon': 'Manectric', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Static', 'Lightningrod'], 'Moves': ['thunderbolt', 'crunch', 'thunderwave', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 682, 'DexNum': 310},
>   {'Pokemon': 'Vileplume', 'SetNum': 4, 'Nature': 'Quiet', 'Item': 'Quick Claw', 'Abilities': ['Chlorophyll'], 'Moves': ['solarbeam', 'sludgebomb', 'sunnyday', 'synthesis'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 683, 'DexNum': 45},
>   {'Pokemon': 'Victreebel', 'SetNum': 4, 'Nature': 'Quirky', 'Item': 'BrightPowder', 'Abilities': ['Chlorophyll'], 'Moves': ['gigadrain', 'doubleedge', 'sludgebomb', 'synthesis'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 684, 'DexNum': 71},
>   {'Pokemon': 'Electrode', 'SetNum': 4, 'Nature': 'Naughty', 'Item': 'Lum Berry', 'Abilities': ['Soundproof', 'Static'], 'Moves': ['explosion', 'thunderbolt', 'thunderwave', 'mirrorcoat'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 685, 'DexNum': 101},
>   {'Pokemon': 'Exploud', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'White Herb', 'Abilities': ['Soundproof'], 'Moves': ['megakick', 'earthquake', 'shadowball', 'overheat'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 686, 'DexNum': 295},
>   {'Pokemon': 'Shiftry', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Focus Band', 'Abilities': ['Chlorophyll', 'Early Bird'], 'Moves': ['explosion', 'gigadrain', 'megakick', 'fakeout'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 687, 'DexNum': 275},
>   {'Pokemon': 'Glalie', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Leftovers', 'Abilities': ['Inner Focus'], 'Moves': ['icebeam', 'earthquake', 'crunch', 'shadowball'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 688, 'DexNum': 362},
>   {'Pokemon': 'Ludicolo', 'SetNum': 4, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Swift Swim', 'Rain Dish'], 'Moves': ['leechseed', 'raindance', 'doubleteam', 'toxic'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 689, 'DexNum': 272},
>   {'Pokemon': 'Hypno', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Insomnia'], 'Moves': ['psychic', 'thunderpunch', 'firepunch', 'icepunch'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 690, 'DexNum': 97},
>   {'Pokemon': 'Golem', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Rock Head', 'Sturdy'], 'Moves': ['explosion', 'earthquake', 'rockslide', 'doubleedge'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 691, 'DexNum': 76},
>   {'Pokemon': 'Rhydon', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Lightningrod', 'Rock Head'], 'Moves': ['megahorn', 'earthquake', 'rockslide', 'horndrill'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 692, 'DexNum': 112},
>   {'Pokemon': 'Alakazam', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Synchronize', 'Inner Focus'], 'Moves': ['psychic', 'thunderpunch', 'firepunch', 'icepunch'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 693, 'DexNum': 65},
>   {'Pokemon': 'Weezing', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Levitate'], 'Moves': ['explosion', 'sludgebomb', 'frustration', 'shadowball'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 694, 'DexNum': 110},
>   {'Pokemon': 'Kangaskhan', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Early Bird'], 'Moves': ['megakick', 'earthquake', 'aerialace', 'shadowball'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 695, 'DexNum': 115},
>   {'Pokemon': 'Electabuzz', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Scope Lens', 'Abilities': ['Static'], 'Moves': ['thunderbolt', 'psychic', 'megakick', 'crosschop'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 696, 'DexNum': 125},
>   {'Pokemon': 'Tauros', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'BrightPowder', 'Abilities': ['Intimidate'], 'Moves': ['doubleedge', 'rocktomb', 'thunderbolt', 'surf'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 697, 'DexNum': 128},
>   {'Pokemon': 'Slowbro', 'SetNum': 4, 'Nature': 'Sassy', 'Item': 'Quick Claw', 'Abilities': ['Oblivious', 'Own Tempo'], 'Moves': ['psychic', 'surf', 'earthquake', 'icebeam'], 'EVs': [0, 0, 0, 255, 255, 0], 'Index': 698, 'DexNum': 80},
>   {'Pokemon': 'Slowking', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Quick Claw', 'Abilities': ['Oblivious', 'Own Tempo'], 'Moves': ['psychic', 'surf', 'icebeam', 'flamethrower'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 699, 'DexNum': 199},
>   {'Pokemon': 'Miltank', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Lum Berry', 'Abilities': ['Thick Fat'], 'Moves': ['doubleedge', 'curse', 'doubleteam', 'milkdrink'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 700, 'DexNum': 241},
>   {'Pokemon': 'Altaria', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Shell Bell', 'Abilities': ['Natural Cure'], 'Moves': ['dragonclaw', 'earthquake', 'flamethrower', 'icebeam'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 701, 'DexNum': 334},
>   {'Pokemon': 'Nidoqueen', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'White Herb', 'Abilities': ['Poison Point'], 'Moves': ['superpower', 'sludgebomb', 'earthquake', 'shadowball'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 702, 'DexNum': 31},
>   {'Pokemon': 'Nidoking', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Lum Berry', 'Abilities': ['Poison Point'], 'Moves': ['megahorn', 'sludgebomb', 'earthquake', 'thunder'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 703, 'DexNum': 34},
>   {'Pokemon': 'Magmar', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Scope Lens', 'Abilities': ['Flame Body'], 'Moves': ['flamethrower', 'psychic', 'crosschop', 'confuseray'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 704, 'DexNum': 126},
>   {'Pokemon': 'Cradily', 'SetNum': 4, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Suction Cups'], 'Moves': ['toxic', 'ingrain', 'mirrorcoat', 'gigadrain'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 705, 'DexNum': 346},
>   {'Pokemon': 'Armaldo', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Choice Band', 'Abilities': ['Battle Armor'], 'Moves': ['doubleedge', 'earthquake', 'aerialace', 'rockslide'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 706, 'DexNum': 348},
>   {'Pokemon': 'Golduck', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Scope Lens', 'Abilities': ['Damp', 'Cloud Nine'], 'Moves': ['surf', 'crosschop', 'icebeam', 'aerialace'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 707, 'DexNum': 55},
>   {'Pokemon': 'Rapidash', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'White Herb', 'Abilities': ['Run Away', 'Flash Fire'], 'Moves': ['overheat', 'doubleedge', 'irontail', 'doublekick'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 708, 'DexNum': 78},
>   {'Pokemon': 'Muk', 'SetNum': 4, 'Nature': 'Brave', 'Item': 'Quick Claw', 'Abilities': ['Stench', 'Sticky Hold'], 'Moves': ['sludgebomb', 'brickbreak', 'gigadrain', 'explosion'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 709, 'DexNum': 89},
>   {'Pokemon': 'Gengar', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'firepunch', 'icepunch', 'destinybond'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 710, 'DexNum': 94},
>   {'Pokemon': 'Ampharos', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Static'], 'Moves': ['thunderbolt', 'firepunch', 'thunderwave', 'reflect'], 'EVs': [0, 0, 255, 255, 0, 0], 'Index': 711, 'DexNum': 181},
>   {'Pokemon': 'Scizor', 'SetNum': 4, 'Nature': 'Careful', 'Item': 'BrightPowder', 'Abilities': ['Swarm'], 'Moves': ['silverwind', 'swordsdance', 'agility', 'batonpass'], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 712, 'DexNum': 212},
>   {'Pokemon': 'Heracross', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Salac Berry', 'Abilities': ['Swarm', 'Guts'], 'Moves': ['megahorn', 'earthquake', 'reversal', 'endure'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 713, 'DexNum': 214},
>   {'Pokemon': 'Ursaring', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Guts'], 'Moves': ['doubleedge', 'earthquake', 'rockslide', 'aerialace'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 714, 'DexNum': 217},
>   {'Pokemon': 'Houndoom', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'White Herb', 'Abilities': ['Early Bird', 'Flash Fire'], 'Moves': ['overheat', 'solarbeam', 'crunch', 'sunnyday'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 715, 'DexNum': 229},
>   {'Pokemon': 'Donphan', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Sturdy'], 'Moves': ['fissure', 'earthquake', 'rockslide', 'irontail'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 716, 'DexNum': 232},
>   {'Pokemon': 'Claydol', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'earthquake', 'shadowball', 'explosion'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 717, 'DexNum': 344},
>   {'Pokemon': 'Wailord', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Quick Claw', 'Abilities': ['Water Veil', 'Oblivious'], 'Moves': ['surf', 'icebeam', 'earthquake', 'fissure'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 718, 'DexNum': 321},
>   {'Pokemon': 'Ninetales', 'SetNum': 4, 'Nature': 'Quirky', 'Item': 'White Herb', 'Abilities': ['Flash Fire'], 'Moves': ['overheat', 'doubleedge', 'confuseray', 'willowisp'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 719, 'DexNum': 38},
>   {'Pokemon': 'Machamp', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Scope Lens', 'Abilities': ['Guts'], 'Moves': ['crosschop', 'earthquake', 'flamethrower', 'rockslide'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 720, 'DexNum': 68},
>   {'Pokemon': 'Shuckle', 'SetNum': 4, 'Nature': 'Careful', 'Item': 'Chesto Berry', 'Abilities': ['Sturdy'], 'Moves': ['toxic', 'doubleteam', 'wrap', 'rest'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 721, 'DexNum': 213},
>   {'Pokemon': 'Steelix', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Rock Head', 'Sturdy'], 'Moves': ['earthquake', 'irontail', 'doubleedge', 'explosion'], 'EVs': [0, 255, 0, 0, 255, 0], 'Index': 722, 'DexNum': 208},
>   {'Pokemon': 'Tentacruel', 'SetNum': 4, 'Nature': 'Quirky', 'Item': 'Shell Bell', 'Abilities': ['Clear Body', 'Liquid Ooze'], 'Moves': ['hydropump', 'sludgebomb', 'icebeam', 'mirrorcoat'], 'EVs': [0, 170, 170, 170, 0, 0], 'Index': 723, 'DexNum': 73},
>   {'Pokemon': 'Aerodactyl', 'SetNum': 4, 'Nature': 'Hardy', 'Item': "King's Rock", 'Abilities': ['Rock Head', 'Pressure'], 'Moves': ['doubleedge', 'earthquake', 'fireblast', 'bite'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 724, 'DexNum': 142},
>   {'Pokemon': 'Porygon2', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Trace'], 'Moves': ['psychic', 'thunderbolt', 'icebeam', 'recover'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 725, 'DexNum': 233},
>   {'Pokemon': 'Gardevoir', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Synchronize', 'Trace'], 'Moves': ['psychic', 'thunderbolt', 'icepunch', 'firepunch'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 726, 'DexNum': 282},
>   {'Pokemon': 'Exeggutor', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'BrightPowder', 'Abilities': ['Chlorophyll'], 'Moves': ['psychic', 'gigadrain', 'sludgebomb', 'explosion'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 727, 'DexNum': 103},
>   {'Pokemon': 'Starmie', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Illuminate', 'Natural Cure'], 'Moves': ['psychic', 'thunderbolt', 'icebeam', 'recover'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 728, 'DexNum': 121},
>   {'Pokemon': 'Flygon', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Scope Lens', 'Abilities': ['Levitate'], 'Moves': ['earthquake', 'dragonclaw', 'doubleedge', 'crunch'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 729, 'DexNum': 330},
>   {'Pokemon': 'Venusaur', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Lum Berry', 'Abilities': ['Overgrow'], 'Moves': ['solarbeam', 'sludgebomb', 'sunnyday', 'earthquake'], 'EVs': [0, 170, 0, 170, 170, 0], 'Index': 730, 'DexNum': 3},
>   {'Pokemon': 'Vaporeon', 'SetNum': 4, 'Nature': 'Calm', 'Item': 'Lum Berry', 'Abilities': ['Water Absorb'], 'Moves': ['surf', 'icebeam', 'acidarmor', 'rest'], 'EVs': [170, 0, 0, 170, 170, 0], 'Index': 731, 'DexNum': 134},
>   {'Pokemon': 'Jolteon', 'SetNum': 4, 'Nature': 'Timid', 'Item': "King's Rock", 'Abilities': ['Volt Absorb'], 'Moves': ['thunderbolt', 'thunderwave', 'bite', 'shadowball'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 732, 'DexNum': 135},
>   {'Pokemon': 'Flareon', 'SetNum': 4, 'Nature': 'Quiet', 'Item': 'Quick Claw', 'Abilities': ['Flash Fire'], 'Moves': ['overheat', 'sunnyday', 'doubleedge', 'shadowball'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 733, 'DexNum': 136},
>   {'Pokemon': 'Meganium', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'BrightPowder', 'Abilities': ['Overgrow'], 'Moves': ['gigadrain', 'earthquake', 'ancientpower', 'bodyslam'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 734, 'DexNum': 154},
>   {'Pokemon': 'Espeon', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Synchronize'], 'Moves': ['psychic', 'bite', 'attract', 'calmmind'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 735, 'DexNum': 196},
>   {'Pokemon': 'Umbreon', 'SetNum': 4, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Synchronize'], 'Moves': ['confuseray', 'toxic', 'faintattack', 'doubleteam'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 736, 'DexNum': 197},
>   {'Pokemon': 'Blastoise', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Focus Band', 'Abilities': ['Torrent'], 'Moves': ['surf', 'earthquake', 'icebeam', 'mirrorcoat'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 737, 'DexNum': 9},
>   {'Pokemon': 'Feraligatr', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Scope Lens', 'Abilities': ['Torrent'], 'Moves': ['hydropump', 'icebeam', 'earthquake', 'aerialace'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 738, 'DexNum': 160},
>   {'Pokemon': 'Aggron', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Sturdy', 'Rock Head'], 'Moves': ['doubleedge', 'earthquake', 'rockslide', 'aerialace'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 739, 'DexNum': 306},
>   {'Pokemon': 'Blaziken', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'White Herb', 'Abilities': ['Blaze'], 'Moves': ['overheat', 'earthquake', 'thunderpunch', 'rockslide'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 740, 'DexNum': 257},
>   {'Pokemon': 'Walrein', 'SetNum': 4, 'Nature': 'Quiet', 'Item': 'BrightPowder', 'Abilities': ['Thick Fat'], 'Moves': ['surf', 'icebeam', 'earthquake', 'sheercold'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 741, 'DexNum': 365},
>   {'Pokemon': 'Sceptile', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Overgrow'], 'Moves': ['leafblade', 'dragonclaw', 'crunch', 'thunderpunch'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 742, 'DexNum': 254},
>   {'Pokemon': 'Charizard', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'White Herb', 'Abilities': ['Blaze'], 'Moves': ['overheat', 'earthquake', 'aerialace', 'rockslide'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 743, 'DexNum': 6},
>   {'Pokemon': 'Typhlosion', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'White Herb', 'Abilities': ['Blaze'], 'Moves': ['overheat', 'thunderpunch', 'earthquake', 'crushclaw'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 744, 'DexNum': 157},
>   {'Pokemon': 'Lapras', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Water Absorb', 'Shell Armor'], 'Moves': ['surf', 'icebeam', 'thunderbolt', 'psychic'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 745, 'DexNum': 131},
>   {'Pokemon': 'Crobat', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Inner Focus'], 'Moves': ['sludgebomb', 'aerialace', 'shadowball', 'confuseray'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 746, 'DexNum': 169},
>   {'Pokemon': 'Swampert', 'SetNum': 4, 'Nature': 'Quiet', 'Item': 'Shell Bell', 'Abilities': ['Torrent'], 'Moves': ['surf', 'earthquake', 'icebeam', 'mirrorcoat'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 747, 'DexNum': 260},
>   {'Pokemon': 'Gyarados', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Intimidate'], 'Moves': ['return', 'earthquake', 'dragondance', 'rest'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 748, 'DexNum': 130},
>   {'Pokemon': 'Snorlax', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Immunity', 'Thick Fat'], 'Moves': ['doubleedge', 'shadowball', 'brickbreak', 'curse'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 749, 'DexNum': 143},
>   {'Pokemon': 'Kingdra', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Chesto Berry', 'Abilities': ['Swift Swim'], 'Moves': ['doubleedge', 'icebeam', 'dragondance', 'rest'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 750, 'DexNum': 230},
>   {'Pokemon': 'Blissey', 'SetNum': 4, 'Nature': 'Bold', 'Item': 'Focus Band', 'Abilities': ['Natural Cure', 'Serene Grace'], 'Moves': ['icebeam', 'calmmind', 'counter', 'softboiled'], 'EVs': [0, 0, 255, 0, 255, 0], 'Index': 751, 'DexNum': 242},
>   {'Pokemon': 'Milotic', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Leftovers', 'Abilities': ['Marvel Scale'], 'Moves': ['surf', 'icebeam', 'recover', 'mirrorcoat'], 'EVs': [0, 0, 170, 170, 170, 0], 'Index': 752, 'DexNum': 350},
>   {'Pokemon': 'Arcanine', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'White Herb', 'Abilities': ['Intimidate', 'Flash Fire'], 'Moves': ['overheat', 'extremespeed', 'crunch', 'doubleedge'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 753, 'DexNum': 59},
>   {'Pokemon': 'Salamence', 'SetNum': 4, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Intimidate'], 'Moves': ['doubleedge', 'earthquake', 'aerialace', 'dragondance'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 754, 'DexNum': 373},
>   {'Pokemon': 'Metagross', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Quick Claw', 'Abilities': ['Clear Body'], 'Moves': ['meteormash', 'psychic', 'earthquake', 'shadowball'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 755, 'DexNum': 376},
>   {'Pokemon': 'Slaking', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Truant'], 'Moves': ['thunderbolt', 'flamethrower', 'icebeam', 'yawn'], 'EVs': [0, 0, 0, 255, 255, 0], 'Index': 756, 'DexNum': 289},
>   {'Pokemon': 'Articuno', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Pressure'], 'Moves': ['icebeam', 'waterpulse', 'icywind', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 757, 'DexNum': 144},
>   {'Pokemon': 'Zapdos', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Lum Berry', 'Abilities': ['Pressure'], 'Moves': ['thunderbolt', 'drillpeck', 'thunderwave', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 758, 'DexNum': 145},
>   {'Pokemon': 'Moltres', 'SetNum': 1, 'Nature': 'Docile', 'Item': 'Lum Berry', 'Abilities': ['Pressure'], 'Moves': ['flamethrower', 'aerialace', 'mudslap', 'roar'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 759, 'DexNum': 146},
>   {'Pokemon': 'Raikou', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Chesto Berry', 'Abilities': ['Pressure'], 'Moves': ['thunderbolt', 'thunderwave', 'calmmind', 'rest'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 760, 'DexNum': 243},
>   {'Pokemon': 'Entei', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Chesto Berry', 'Abilities': ['Pressure'], 'Moves': ['flamethrower', 'doubleteam', 'calmmind', 'rest'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 761, 'DexNum': 244},
>   {'Pokemon': 'Suicune', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Chesto Berry', 'Abilities': ['Pressure'], 'Moves': ['surf', 'doubleteam', 'calmmind', 'rest'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 762, 'DexNum': 245},
>   {'Pokemon': 'Regirock', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'White Herb', 'Abilities': ['Clear Body'], 'Moves': ['superpower', 'earthquake', 'rockslide', 'explosion'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 763, 'DexNum': 377},
>   {'Pokemon': 'Regice', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Chesto Berry', 'Abilities': ['Clear Body'], 'Moves': ['icebeam', 'thunderbolt', 'amnesia', 'rest'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 764, 'DexNum': 378},
>   {'Pokemon': 'Registeel', 'SetNum': 1, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Clear Body'], 'Moves': ['metalclaw', 'curse', 'amnesia', 'rest'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 765, 'DexNum': 379},
>   {'Pokemon': 'Latias', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'thunderbolt', 'icebeam', 'dragonclaw'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 766, 'DexNum': 380},
>   {'Pokemon': 'Latios', 'SetNum': 1, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'thunderbolt', 'icebeam', 'dragonclaw'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 767, 'DexNum': 381},
>   {'Pokemon': 'Articuno', 'SetNum': 2, 'Nature': 'Impish', 'Item': 'Leftovers', 'Abilities': ['Pressure'], 'Moves': ['substitute', 'toxic', 'blizzard', 'doubleteam'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 768, 'DexNum': 144},
>   {'Pokemon': 'Zapdos', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'BrightPowder', 'Abilities': ['Pressure'], 'Moves': ['thunder', 'raindance', 'drillpeck', 'doubleteam'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 769, 'DexNum': 145},
>   {'Pokemon': 'Moltres', 'SetNum': 2, 'Nature': 'Hardy', 'Item': 'White Herb', 'Abilities': ['Pressure'], 'Moves': ['overheat', 'aerialace', 'doubleteam', 'protect'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 770, 'DexNum': 146},
>   {'Pokemon': 'Raikou', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Pressure'], 'Moves': ['thunder', 'raindance', 'doubleteam', 'reflect'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 771, 'DexNum': 243},
>   {'Pokemon': 'Entei', 'SetNum': 2, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Pressure'], 'Moves': ['fireblast', 'sunnyday', 'solarbeam', 'reflect'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 772, 'DexNum': 244},
>   {'Pokemon': 'Suicune', 'SetNum': 2, 'Nature': 'Calm', 'Item': 'Leftovers', 'Abilities': ['Pressure'], 'Moves': ['toxic', 'dive', 'doubleteam', 'protect'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 773, 'DexNum': 245},
>   {'Pokemon': 'Regirock', 'SetNum': 2, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Clear Body'], 'Moves': ['earthquake', 'rockslide', 'counter', 'explosion'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 774, 'DexNum': 377},
>   {'Pokemon': 'Regice', 'SetNum': 2, 'Nature': 'Quiet', 'Item': 'BrightPowder', 'Abilities': ['Clear Body'], 'Moves': ['thunder', 'raindance', 'blizzard', 'brickbreak'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 775, 'DexNum': 378},
>   {'Pokemon': 'Registeel', 'SetNum': 2, 'Nature': 'Quiet', 'Item': 'BrightPowder', 'Abilities': ['Clear Body'], 'Moves': ['thunderbolt', 'icepunch', 'earthquake', 'aerialace'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 776, 'DexNum': 379},
>   {'Pokemon': 'Latias', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Quick Claw', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'thunderbolt', 'icebeam', 'earthquake'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 777, 'DexNum': 380},
>   {'Pokemon': 'Latios', 'SetNum': 2, 'Nature': 'Docile', 'Item': 'Quick Claw', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'thunderbolt', 'icebeam', 'earthquake'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 778, 'DexNum': 381},
>   {'Pokemon': 'Articuno', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'BrightPowder', 'Abilities': ['Pressure'], 'Moves': ['icebeam', 'facade', 'aerialace', 'protect'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 779, 'DexNum': 144},
>   {'Pokemon': 'Zapdos', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'Leftovers', 'Abilities': ['Pressure'], 'Moves': ['thunderbolt', 'drillpeck', 'thunderwave', 'substitute'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 780, 'DexNum': 145},
>   {'Pokemon': 'Moltres', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Chesto Berry', 'Abilities': ['Pressure'], 'Moves': ['fireblast', 'sunnyday', 'doubleteam', 'rest'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 781, 'DexNum': 146},
>   {'Pokemon': 'Raikou', 'SetNum': 3, 'Nature': 'Modest', 'Item': "King's Rock", 'Abilities': ['Pressure'], 'Moves': ['thunderbolt', 'thunderwave', 'quickattack', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 782, 'DexNum': 243},
>   {'Pokemon': 'Entei', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'Lum Berry', 'Abilities': ['Pressure'], 'Moves': ['flamethrower', 'doubleedge', 'swagger', 'psychup'], 'EVs': [0, 255, 0, 0, 0, 255], 'Index': 783, 'DexNum': 244},
>   {'Pokemon': 'Suicune', 'SetNum': 3, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Pressure'], 'Moves': ['surf', 'icebeam', 'raindance', 'roar'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 784, 'DexNum': 245},
>   {'Pokemon': 'Regirock', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Clear Body'], 'Moves': ['rockslide', 'earthquake', 'curse', 'rest'], 'EVs': [255, 0, 0, 0, 255, 0], 'Index': 785, 'DexNum': 377},
>   {'Pokemon': 'Regice', 'SetNum': 3, 'Nature': 'Quiet', 'Item': 'Lum Berry', 'Abilities': ['Clear Body'], 'Moves': ['icebeam', 'thunderbolt', 'thunderwave', 'explosion'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 786, 'DexNum': 378},
>   {'Pokemon': 'Registeel', 'SetNum': 3, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Clear Body'], 'Moves': ['ancientpower', 'amnesia', 'counter', 'explosion'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 787, 'DexNum': 379},
>   {'Pokemon': 'Latias', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'Focus Band', 'Abilities': ['Levitate'], 'Moves': ['dragonclaw', 'thunderbolt', 'icebeam', 'earthquake'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 788, 'DexNum': 380},
>   {'Pokemon': 'Latios', 'SetNum': 3, 'Nature': 'Docile', 'Item': 'Focus Band', 'Abilities': ['Levitate'], 'Moves': ['dragonclaw', 'thunderbolt', 'icebeam', 'earthquake'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 789, 'DexNum': 381},
>   {'Pokemon': 'Articuno', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Chesto Berry', 'Abilities': ['Pressure'], 'Moves': ['blizzard', 'doubleedge', 'rest', 'reflect'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 790, 'DexNum': 144},
>   {'Pokemon': 'Zapdos', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Shell Bell', 'Abilities': ['Pressure'], 'Moves': ['thunderbolt', 'drillpeck', 'thunderwave', 'lightscreen'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 791, 'DexNum': 145},
>   {'Pokemon': 'Moltres', 'SetNum': 4, 'Nature': 'Quiet', 'Item': 'White Herb', 'Abilities': ['Pressure'], 'Moves': ['overheat', 'doubleedge', 'steelwing', 'safeguard'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 792, 'DexNum': 146},
>   {'Pokemon': 'Raikou', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Pressure'], 'Moves': ['thunderbolt', 'bite', 'thunderwave', 'reflect'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 793, 'DexNum': 243},
>   {'Pokemon': 'Entei', 'SetNum': 4, 'Nature': 'Modest', 'Item': "King's Rock", 'Abilities': ['Pressure'], 'Moves': ['flamethrower', 'bite', 'doubleteam', 'reflect'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 794, 'DexNum': 244},
>   {'Pokemon': 'Suicune', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Pressure'], 'Moves': ['surf', 'icebeam', 'bite', 'reflect'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 795, 'DexNum': 245},
>   {'Pokemon': 'Regirock', 'SetNum': 4, 'Nature': 'Careful', 'Item': 'Leftovers', 'Abilities': ['Clear Body'], 'Moves': ['rockslide', 'brickbreak', 'doubleteam', 'thunderwave'], 'EVs': [170, 170, 0, 0, 170, 0], 'Index': 796, 'DexNum': 377},
>   {'Pokemon': 'Regice', 'SetNum': 4, 'Nature': 'Bold', 'Item': 'Leftovers', 'Abilities': ['Clear Body'], 'Moves': ['icebeam', 'hail', 'doubleteam', 'thunderwave'], 'EVs': [255, 0, 255, 0, 0, 0], 'Index': 797, 'DexNum': 378},
>   {'Pokemon': 'Registeel', 'SetNum': 4, 'Nature': 'Impish', 'Item': 'Leftovers', 'Abilities': ['Clear Body'], 'Moves': ['ancientpower', 'earthquake', 'doubleteam', 'thunderwave'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 798, 'DexNum': 379},
>   {'Pokemon': 'Latias', 'SetNum': 4, 'Nature': 'Docile', 'Item': 'Leftovers', 'Abilities': ['Levitate'], 'Moves': ['mistball', 'shadowball', 'charm', 'reflect'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 799, 'DexNum': 380},
>   {'Pokemon': 'Latios', 'SetNum': 4, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['lusterpurge', 'thunderbolt', 'icebeam', 'dragonclaw'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 800, 'DexNum': 381},
>   {'Pokemon': 'Gengar', 'SetNum': 5, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'shadowball', 'thunderbolt', 'firepunch'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 801, 'DexNum': 94},
>   {'Pokemon': 'Gengar', 'SetNum': 6, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'shadowball', 'thunderbolt', 'icepunch'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 802, 'DexNum': 94},
>   {'Pokemon': 'Gengar', 'SetNum': 7, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'thunderbolt', 'firepunch', 'destinybond'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 803, 'DexNum': 94},
>   {'Pokemon': 'Gengar', 'SetNum': 8, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['psychic', 'thunderbolt', 'icepunch', 'destinybond'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 804, 'DexNum': 94},
>   {'Pokemon': 'Ursaring', 'SetNum': 5, 'Nature': 'Adamant', 'Item': 'Choice Band', 'Abilities': ['Guts'], 'Moves': ['megakick', 'aerialace', 'rockslide', 'brickbreak'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 805, 'DexNum': 217},
>   {'Pokemon': 'Ursaring', 'SetNum': 6, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Guts'], 'Moves': ['hyperbeam', 'yawn', 'swordsdance', 'doubleteam'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 806, 'DexNum': 217},
>   {'Pokemon': 'Ursaring', 'SetNum': 7, 'Nature': 'Docile', 'Item': 'Quick Claw', 'Abilities': ['Guts'], 'Moves': ['facade', 'earthquake', 'crunch', 'bulkup'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 807, 'DexNum': 217},
>   {'Pokemon': 'Ursaring', 'SetNum': 8, 'Nature': 'Docile', 'Item': 'Quick Claw', 'Abilities': ['Guts'], 'Moves': ['facade', 'earthquake', 'crunch', 'brickbreak'], 'EVs': [170, 170, 0, 170, 0, 0], 'Index': 808, 'DexNum': 217},
>   {'Pokemon': 'Machamp', 'SetNum': 5, 'Nature': 'Adamant', 'Item': 'Scope Lens', 'Abilities': ['Guts'], 'Moves': ['crosschop', 'doubleedge', 'earthquake', 'rockslide'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 809, 'DexNum': 68},
>   {'Pokemon': 'Machamp', 'SetNum': 6, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Guts'], 'Moves': ['crosschop', 'earthquake', 'counter', 'rocktomb'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 810, 'DexNum': 68},
>   {'Pokemon': 'Machamp', 'SetNum': 7, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Guts'], 'Moves': ['focuspunch', 'substitute', 'attract', 'doubleteam'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 811, 'DexNum': 68},
>   {'Pokemon': 'Machamp', 'SetNum': 8, 'Nature': 'Adamant', 'Item': 'Focus Band', 'Abilities': ['Guts'], 'Moves': ['revenge', 'rockslide', 'facade', 'counter'], 'EVs': [255, 255, 0, 0, 0, 0], 'Index': 812, 'DexNum': 68},
>   {'Pokemon': 'Gardevoir', 'SetNum': 5, 'Nature': 'Docile', 'Item': 'Salac Berry', 'Abilities': ['Synchronize', 'Trace'], 'Moves': ['psychic', 'shadowball', 'endure', 'destinybond'], 'EVs': [170, 0, 170, 0, 0, 170], 'Index': 813, 'DexNum': 282},
>   {'Pokemon': 'Gardevoir', 'SetNum': 6, 'Nature': 'Timid', 'Item': 'Lum Berry', 'Abilities': ['Synchronize', 'Trace'], 'Moves': ['psychic', 'thunderbolt', 'willowisp', 'destinybond'], 'EVs': [255, 0, 0, 0, 0, 255], 'Index': 814, 'DexNum': 282},
>   {'Pokemon': 'Gardevoir', 'SetNum': 7, 'Nature': 'Bold', 'Item': 'Quick Claw', 'Abilities': ['Synchronize', 'Trace'], 'Moves': ['psychic', 'calmmind', 'willowisp', 'destinybond'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 815, 'DexNum': 282},
>   {'Pokemon': 'Gardevoir', 'SetNum': 8, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Synchronize', 'Trace'], 'Moves': ['psychic', 'magicalleaf', 'attract', 'doubleteam'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 816, 'DexNum': 282},
>   {'Pokemon': 'Starmie', 'SetNum': 5, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Illuminate', 'Natural Cure'], 'Moves': ['surf', 'psychic', 'recover', 'lightscreen'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 817, 'DexNum': 121},
>   {'Pokemon': 'Starmie', 'SetNum': 6, 'Nature': 'Calm', 'Item': 'Leftovers', 'Abilities': ['Illuminate', 'Natural Cure'], 'Moves': ['surf', 'confuseray', 'thunderwave', 'recover'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 818, 'DexNum': 121},
>   {'Pokemon': 'Starmie', 'SetNum': 7, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Illuminate', 'Natural Cure'], 'Moves': ['psychic', 'icebeam', 'cosmicpower', 'recover'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 819, 'DexNum': 121},
>   {'Pokemon': 'Starmie', 'SetNum': 8, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Illuminate', 'Natural Cure'], 'Moves': ['surf', 'thunderbolt', 'cosmicpower', 'recover'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 820, 'DexNum': 121},
>   {'Pokemon': 'Lapras', 'SetNum': 5, 'Nature': 'Docile', 'Item': 'Shell Bell', 'Abilities': ['Water Absorb', 'Shell Armor'], 'Moves': ['psychic', 'thunderbolt', 'irontail', 'doubleedge'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 821, 'DexNum': 131},
>   {'Pokemon': 'Lapras', 'SetNum': 6, 'Nature': 'Modest', 'Item': 'BrightPowder', 'Abilities': ['Water Absorb', 'Shell Armor'], 'Moves': ['hydropump', 'thunder', 'raindance', 'blizzard'], 'EVs': [255, 0, 0, 255, 0, 0], 'Index': 822, 'DexNum': 131},
>   {'Pokemon': 'Lapras', 'SetNum': 7, 'Nature': 'Calm', 'Item': 'Leppa Berry', 'Abilities': ['Water Absorb', 'Shell Armor'], 'Moves': ['sheercold', 'horndrill', 'rest', 'sleeptalk'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 823, 'DexNum': 131},
>   {'Pokemon': 'Lapras', 'SetNum': 8, 'Nature': 'Calm', 'Item': 'Quick Claw', 'Abilities': ['Water Absorb', 'Shell Armor'], 'Moves': ['sheercold', 'horndrill', 'sing', 'attract'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 824, 'DexNum': 131},
>   {'Pokemon': 'Snorlax', 'SetNum': 5, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Immunity', 'Thick Fat'], 'Moves': ['megakick', 'shadowball', 'brickbreak', 'counter'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 825, 'DexNum': 143},
>   {'Pokemon': 'Snorlax', 'SetNum': 6, 'Nature': 'Adamant', 'Item': 'Leftovers', 'Abilities': ['Immunity', 'Thick Fat'], 'Moves': ['earthquake', 'shadowball', 'brickbreak', 'counter'], 'EVs': [0, 255, 255, 0, 0, 0], 'Index': 826, 'DexNum': 143},
>   {'Pokemon': 'Snorlax', 'SetNum': 7, 'Nature': 'Adamant', 'Item': 'Quick Claw', 'Abilities': ['Immunity', 'Thick Fat'], 'Moves': ['hyperbeam', 'shadowball', 'earthquake', 'curse'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 827, 'DexNum': 143},
>   {'Pokemon': 'Snorlax', 'SetNum': 8, 'Nature': 'Adamant', 'Item': 'Chesto Berry', 'Abilities': ['Immunity', 'Thick Fat'], 'Moves': ['return', 'shadowball', 'bellydrum', 'rest'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 828, 'DexNum': 143},
>   {'Pokemon': 'Salamence', 'SetNum': 5, 'Nature': 'Adamant', 'Item': 'BrightPowder', 'Abilities': ['Intimidate'], 'Moves': ['facade', 'earthquake', 'rockslide', 'dragondance'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 829, 'DexNum': 373},
>   {'Pokemon': 'Salamence', 'SetNum': 6, 'Nature': 'Hardy', 'Item': 'Lum Berry', 'Abilities': ['Intimidate'], 'Moves': ['headbutt', 'aerialace', 'crunch', 'dragondance'], 'EVs': [170, 0, 170, 0, 170, 0], 'Index': 830, 'DexNum': 373},
>   {'Pokemon': 'Salamence', 'SetNum': 7, 'Nature': 'Modest', 'Item': 'Lum Berry', 'Abilities': ['Intimidate'], 'Moves': ['flamethrower', 'dragonclaw', 'crunch', 'brickbreak'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 831, 'DexNum': 373},
>   {'Pokemon': 'Salamence', 'SetNum': 8, 'Nature': 'Modest', 'Item': 'Leftovers', 'Abilities': ['Intimidate'], 'Moves': ['flamethrower', 'dragonclaw', 'crunch', 'attract'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 832, 'DexNum': 373},
>   {'Pokemon': 'Metagross', 'SetNum': 5, 'Nature': 'Jolly', 'Item': 'Quick Claw', 'Abilities': ['Clear Body'], 'Moves': ['explosion', 'earthquake', 'rockslide', 'brickbreak'], 'EVs': [170, 170, 0, 0, 0, 170], 'Index': 833, 'DexNum': 376},
>   {'Pokemon': 'Metagross', 'SetNum': 6, 'Nature': 'Hardy', 'Item': 'BrightPowder', 'Abilities': ['Clear Body'], 'Moves': ['meteormash', 'psychic', 'icepunch', 'thunderpunch'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 834, 'DexNum': 376},
>   {'Pokemon': 'Metagross', 'SetNum': 7, 'Nature': 'Hardy', 'Item': 'Shell Bell', 'Abilities': ['Clear Body'], 'Moves': ['earthquake', 'shadowball', 'icepunch', 'thunderpunch'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 835, 'DexNum': 376},
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
>   {'Pokemon': 'Latios', 'SetNum': 8, 'Nature': 'Docile', 'Item': "King's Rock", 'Abilities': ['Levitate'], 'Moves': ['psychic', 'shadowball', 'earthquake', 'aerialace'], 'EVs': [0, 170, 0, 170, 0, 170], 'Index': 850, 'DexNum': 381}
> ]
> ```
>
> </details>


### Team Type and Phrase

Every Factory team gets a "type" (most common Pokemon type) and a "phrase" (battle style description):


> ```python
> from frontierbrain3.facilities.factory import FactoryDatabase, team_type, team_phrase
> fac = FactoryDatabase()
> sample_team = fac.sets_in_groups([7, 8])[:3]
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> sample_team = [
>   {'Pokemon': 'Medicham', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Lum Berry', 'Abilities': ['Pure Power'], 'Moves': ['megakick', 'psychic', 'shadowball', 'rockslide'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 662, 'DexNum': 308},
>   {'Pokemon': 'Misdreavus', 'SetNum': 4, 'Nature': 'Timid', 'Item': 'Lum Berry', 'Abilities': ['Levitate'], 'Moves': ['destinybond', 'psychic', 'shadowball', 'thunderbolt'], 'EVs': [0, 0, 0, 255, 0, 255], 'Index': 663, 'DexNum': 200},
>   {'Pokemon': 'Fearow', 'SetNum': 4, 'Nature': 'Hardy', 'Item': 'Lum Berry', 'Abilities': ['Keen Eye'], 'Moves': ['drillpeck', 'doubleedge', 'steelwing', 'skyattack'], 'EVs': [0, 255, 0, 255, 0, 0], 'Index': 664, 'DexNum': 22}
> ]
> ```
>
> </details>


<br>

> ```python
> team_type(sample_team)
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


<br>

> ```python
> team_phrase(sample_team)
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
> ids, typ, phrase = fac.random_team("open", 5)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ids = ['Walrein-1', 'Breloom-4', 'Claydol-1']
> typ = 'No Type'
> phrase = 'appears to be slow and steady'
> ```
>
> </details>


<br>

> ```python
> ids, typ, phrase = fac.random_team("open", 5, target_type="Water")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ids = ['Gyarados-4', 'Flareon-2', 'Starmie-7']
> typ = 'Water'
> phrase = 'appears to be free-spirited and unrestrained'
> ```
>
> </details>


<br>

> ```python
> ids, typ, phrase = fac.random_team("open", 5, target_phrase=4)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ids = ['Exeggutor-4', 'Steelix-3', 'Registeel-4']
> typ = 'Steel'
> phrase = 'appears to be high risk, high return'
> ```
>
> </details>


<br>

> ```python
> ids, typ, phrase = fac.random_team("lv50", 1, target_type="Fire", target_phrase=1)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ids = ['Growlithe-1', 'Magby-1', 'Clamperl-1']
> typ = 'Fire'
> phrase = 'appears to be one based on total preparation'
> ```
>
> </details>


Phrase numbers: 0=none, 1=preparation, 2=slow/steady, 3=endurance, 4=high-risk, 5=weaken foe, 6=unpredictable, 7=battle flow, 8=flex.

---

## Battle Dome (`facilities.dome`)

### Seeding

The Dome gives each team a seed using a formula based on the Pokemon's stats, types, and levels. The seed affects where the players and opponents are placed in the bracket, and having the highest seed possible is advantageous to the player. The higher seed wins in case of a tie (except for Dome Ace Tucker, who will always win ties), unlike every other facility where a tie counts as a loss for the player.


> ```python
> from frontierbrain3 import Database, CustomSet
> from frontierbrain3.facilities.dome import calc_seed
> db = Database()
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


<br>

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


<br>

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


<br>

> ```python
> team = [meta, lax, ttar]
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


<br>

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


<br>

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


<br>

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
> tower = TowerDatabase()
> set_lookup = {f"{s['Pokemon']}-{s['SetNum']}": s for s in tower._sets}
> best_seed = 0
> best_team = ""
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
> print(f"Highest enemy seed: {best_seed}")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> Highest enemy seed: 4190
> ```
>
> </details>


<br>

> ```python
> print(f"Team: {best_team}")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> Team: Cooltrainer (M) ALONZO: Charizard-4, Feraligatr-3, Kingdra-1
> ```
>
> </details>


After simulating 1000 random enemy teams, the highest seed found gives a rough upper bound on what the player needs to beat. This is an easy way to estimate how high your team's seed should be to guarantee the #1 position.

---

## Battle Palace (`facilities.palace`)

In the Palace, Pokemon choose their own moves. Each turn, the game first selects a move **category** (Attack, Defense, or Support) based on the Pokemon's nature. Then it picks one of the Pokemon's moves in that category uniformly at random (1/N chance if the category has N moves). If the Pokemon has no move in the selected category, it has a 50% chance to randomly use any move, and a 50% chance to do nothing for that turn.

### Move Categories

Palace classifies every move as attack, defense, or support:


> ```python
> from frontierbrain3.facilities.palace import get_move_category, categorize_moveset
> get_move_category("Earthquake"), get_move_category("Swords Dance"), get_move_category("Thunder Wave")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> ('attack', 'defense', 'support')
> ```
>
> </details>


<br>

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
> get_nature_ratios("Adamant")
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


<br>

> ```python
> get_nature_ratios("Adamant", low_hp=True)
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
> moves = ["Earthquake", "Rock Slide", "Swords Dance", "Protect"]
> get_action_probabilities("Adamant", moves)
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


<br>

> ```python
> get_move_probabilities("Adamant", moves)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'Earthquake': 0.23,
>   'Rock Slide': 0.23,
>   'Swords Dance': 0.19,
>   'Protect': 0.19,
>   'nothing': 0.15,
> }
> ```
>
> </details>


### Multi-Turn Analysis

Analyze probabilities over multiple turns, either by category or by specific move. Category defaults to "attack" but can be set to "defense" or "support":


> ```python
> from frontierbrain3.facilities.palace import (
>     multi_turn_probabilities, move_turn_probabilities,
>     cumulative_attack_prob, expected_attacks, multi_turn_mixed_hp,
> )
> moves = ["Earthquake", "Rock Slide", "Swords Dance", "Protect"]
> multi_turn_probabilities("Adamant", moves, 5)
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


<br>

> ```python
> move_turn_probabilities("Adamant", moves, 5, "Earthquake")
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


<br>

> ```python
> cumulative_attack_prob("Adamant", moves, 5, 3)
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


<br>

> ```python
> expected_attacks("Adamant", moves, 5)
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


<br>

> ```python
> multi_turn_mixed_hp("Adamant", moves, 3, 2)
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

Rank all 25 natures by how likely they are to use a given category (defaults to "attack"):


> ```python
> from frontierbrain3.facilities.palace import rank_natures, low_hp_message, DOUBLES_TARGETING
> rank_natures(["Earthquake", "Rock Slide", "Swords Dance", "Protect"])
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   ('Sassy', 0.895), ('Impish', 0.7525), ('Brave', 0.7374999999999999), ('Hardy', 0.69), ('Timid', 0.69),
>   ('Docile', 0.6150000000000001), ('Naive', 0.6150000000000001), ('Quiet', 0.6150000000000001),
>   ('Quirky', 0.6150000000000001), ('Hasty', 0.5924999999999999), ('Jolly', 0.5), ('Lax', 0.4875),
>   ('Serious', 0.47750000000000004), ('Adamant', 0.4575), ('Mild', 0.455), ('Rash', 0.4425), ('Careful', 0.44),
>   ('Calm', 0.42500000000000004), ('Bold', 0.425), ('Relaxed', 0.4), ('Modest', 0.39999999999999997), ('Lonely', 0.3375),
>   ('Bashful', 0.32999999999999996), ('Naughty', 0.225), ('Gentle', 0.21)
> ]
> ```
>
> </details>


<br>

> ```python
> rank_natures(["Earthquake", "Rock Slide", "Swords Dance", "Protect"], category="defense")
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   ('Gentle', 0.73), ('Naughty', 0.725), ('Bashful', 0.61), ('Calm', 0.525), ('Careful', 0.52), ('Mild', 0.515),
>   ('Modest', 0.5), ('Lonely', 0.3875), ('Adamant', 0.3875), ('Hasty', 0.3825), ('Bold', 0.325), ('Relaxed', 0.3),
>   ('Docile', 0.275), ('Naive', 0.275), ('Quiet', 0.275), ('Quirky', 0.275), ('Rash', 0.27249999999999996),
>   ('Serious', 0.2475), ('Lax', 0.23750000000000002), ('Jolly', 0.2), ('Brave', 0.1875), ('Timid', 0.17),
>   ('Hardy', 0.15000000000000002), ('Impish', 0.1225), ('Sassy', 0.075)
> ]
> ```
>
> </details>


<br>

> ```python
> low_hp_message("Adamant", "Metagross")
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


<br>

> ```python
> DOUBLES_TARGETING["adamant"]
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


<br>

> ```python
> DOUBLES_TARGETING["brave"]
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
> EVENTS
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


<br>

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


<br>

> ```python
> get_event_probabilities(all_full_hp=False)
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


<br>

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
> from frontierbrain3.facilities.pike import get_status_chances, status_targets
> status_targets(1)
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


<br>

> ```python
> status_targets(6)
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


<br>

> ```python
> status_targets(11)
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


Status probabilities accounting for immunities (example team: Metagross / Tauros / Latios):


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
> from frontierbrain3.facilities.pike import pike_wild_pokemon
> pike_wild_pokemon(100, lv50=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'species': 'Seviper', 'ability': 'Shed Skin', 'level': 46, 'rate': 26, 'moves': ['Toxic', 'Glare', 'Sludge Bomb', 'Body Slam']},
>   {'species': 'Milotic', 'ability': 'Marvel Scale', 'level': 46, 'rate': 26, 'moves': ['Toxic', 'Hypnosis', 'Body Slam', 'Surf']},
>   {'species': 'Dusclops', 'ability': 'Pressure', 'level': 45, 'rate': 48, 'moves': ['Will-O-Wisp', 'Mean Look', 'Toxic', 'Shadow Punch']}
> ]
> ```
>
> </details>


<br>

> ```python
> pike_wild_pokemon(300, lv50=True)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'species': 'Seviper', 'ability': 'Shed Skin', 'level': 46, 'rate': 26, 'moves': ['Toxic', 'Glare', 'Sludge Bomb', 'Body Slam']},
>   {'species': 'Milotic', 'ability': 'Marvel Scale', 'level': 46, 'rate': 26, 'moves': ['Toxic', 'Hypnosis', 'Body Slam', 'Surf']},
>   {'species': 'Electrode', 'ability': 'Soundproof', 'level': 45, 'rate': 48, 'moves': ['Explosion', 'Selfdestruct', 'Thunder', 'Toxic']}
> ]
> ```
>
> </details>


<br>

> ```python
> pike_wild_pokemon(900, lv50=False)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'species': 'Seviper', 'ability': 'Shed Skin', 'level': [60, 96], 'rate': 26, 'moves': ['Toxic', 'Glare', 'Sludge Bomb', 'Poison Fang']},
>   {'species': 'Milotic', 'ability': 'Marvel Scale', 'level': [60, 96], 'rate': 26, 'moves': ['Toxic', 'Hypnosis', 'Body Slam', 'Ice Beam']},
>   {'species': 'Wobbuffet', 'ability': 'Shadow Tag', 'level': [60, 95], 'rate': 48, 'moves': ['Counter', 'Mirror Coat', 'Safeguard', 'Encore']}
> ]
> ```
>
> </details>


### Hints


> ```python
> from frontierbrain3.facilities.pike import HINTS
> HINTS
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> {
>   'nostalgia': {'text': 'For some odd reason, I felt a wave of nostalgia coming from it...', 'events': ['status', 'partial_heal']},
>   'people': {'text': 'Is it...A Trainer? I sense the presence of people...', 'events': ['single_battle', 'full_heal']},
>   'aroma': {'text': 'It seems to have the distinct aroma of Pokemon wafting around it...', 'events': ['wild_pokemon', 'hard_battle_heal']},
>   'whispering': {'text': 'I seem to have heard something... It may have been whispering...', 'events': ['no_event', 'double_battle']},
>   'dreadful': {'text': 'From every path I sense a dreadful presence...', 'events': ['pike_queen']},
> }
> ```
>
> </details>


---

## Battle Pyramid (`facilities.pyramid`)

For more details, see the [Bulbapedia Battle Pyramid page](https://bulbapedia.bulbagarden.net/wiki/Battle_Pyramid).

### Round Themes and Wild Pokemon

20 rounds, each with a theme and 8 wild Pokemon:


> ```python
> from frontierbrain3.facilities.pyramid import pyramid_wild_pokemon, ROUND_THEMES
> ROUND_THEMES
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


<br>

> ```python
> pyramid_wild_pokemon(1)
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
>   {'species': 'Jolteon', 'ability': None, 'lv50': [35, 45], 'open_offset': [-11, -1], 'moves': ['Thunder Wave', 'Thunder', 'Pin Missile', 'Quick Attack']}
> ]
> ```
>
> </details>


<br>

> ```python
> pyramid_wild_pokemon(1, floor=3)
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
>   {'pokemon': {'species': 'Manectric', 'ability': None, 'lv50': [34, 44], 'open_offset': [-13, -3], 'moves': ['Thunder Wave', 'Thunder', 'Quick Attack']}, 'rate': 5}
> ]
> ```
>
> </details>


Encounter data includes species, ability, level ranges, and moves. Rounds cycle after 20 (round 21 = round 1, etc.).

### Floor Mechanics


> ```python
> from frontierbrain3.facilities.pyramid import FLOOR_TABLE, SLOT_RATES, get_floor_encounter_rate
> FLOOR_TABLE[1]
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


<br>

> ```python
> SLOT_RATES
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


<br>

> ```python
> get_floor_encounter_rate(7)
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
> get_items(1, 3)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'item': 'Hyper Potion', 'rate': 15}, {'item': 'Fluffy Tail', 'rate': 15}, {'item': 'Cheri Berry', 'rate': 31},
>   {'item': 'Ether', 'rate': 10}, {'item': 'Lum Berry', 'rate': 10}, {'item': 'Revive', 'rate': 10},
>   {'item': 'Bright Powder', 'rate': 3}, {'item': 'Shell Bell', 'rate': 3}, {'item': 'Max Revive', 'rate': 3}
> ]
> ```
>
> </details>


<br>

> ```python
> get_pickup_items(1)
> ```
>
> <details>
> <summary>Output</summary>
>
> ```
> [
>   {'item': 'Hyper Potion', 'rate': 30}, {'item': 'Fluffy Tail', 'rate': 10}, {'item': 'Cheri Berry', 'rate': 10},
>   {'item': 'Ether', 'rate': 10}, {'item': 'Lum Berry', 'rate': 10}, {'item': 'Revive', 'rate': 10},
>   {'item': 'Bright Powder', 'rate': 5}, {'item': 'Shell Bell', 'rate': 5}, {'item': 'Max Revive', 'rate': 5},
>   {'item': 'Sacred Ash', 'rate': 5}
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