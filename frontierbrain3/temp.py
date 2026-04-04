"""
Scans Data/moves.json for non-status moves with 0 or null power,
then checks whether each is referenced in damagecalc.py.

Prints unhandled moves so we know what to implement next.
"""

import json
import re
from pathlib import Path

MOVES_FILE    = Path(__file__).parent / "Data" / "moves.json"
DAMAGECALC_PY = Path(__file__).parent / "damagecalc.py"

# ── Load moves ────────────────────────────────────────────────────────────────

with open(MOVES_FILE, encoding="utf-8") as f:
    raw = json.load(f)

if isinstance(raw, list):
    moves = {m["name"]: m for m in raw}
else:
    moves = dict(raw)

# ── Load damagecalc source and normalize for scanning ─────────────────────────

calc_source = DAMAGECALC_PY.read_text(encoding="utf-8").lower()

# ── Classify ──────────────────────────────────────────────────────────────────

def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())

# Moves with 0/null power that still deal damage (variable BP, OHKO, etc.)
# Status moves genuinely do 0 damage and we can skip them.
# We identify status moves by category if available, otherwise by having
# no damage-dealing characteristics.

zero_power = []
for name, data in moves.items():
    power = data.get("power", 0) or 0
    if power != 0:
        continue

    cat = data.get("category", "").lower()

    # Skip pure status moves
    if cat == "status":
        continue

    zero_power.append((name, data))

# ── Check which are referenced in damagecalc.py ──────────────────────────────

handled   = []
unhandled = []

for name, data in sorted(zero_power, key=lambda x: x[0]):
    normalized = norm(name)
    # Check for the normalized name appearing as a string literal in the source
    if normalized in calc_source:
        handled.append((name, data))
    else:
        unhandled.append((name, data))

# ── Print results ─────────────────────────────────────────────────────────────

print(f"Total moves in DB: {len(moves)}")
print(f"Non-status moves with 0/null power: {len(zero_power)}")
print(f"  Already referenced in damagecalc.py: {len(handled)}")
print(f"  NOT referenced: {len(unhandled)}")

if handled:
    print(f"\n{'─'*60}")
    print("HANDLED (referenced in damagecalc.py):")
    print(f"{'─'*60}")
    for name, data in handled:
        cat  = data.get("category", "?")
        typ  = data.get("type", "?")
        desc = data.get("description", data.get("desc", ""))[:60]
        print(f"  {name:<20} {typ:<10} {cat:<10} {desc}")

if unhandled:
    print(f"\n{'─'*60}")
    print("UNHANDLED (not referenced in damagecalc.py):")
    print(f"{'─'*60}")
    for name, data in unhandled:
        cat  = data.get("category", "?")
        typ  = data.get("type", "?")
        desc = data.get("description", data.get("desc", ""))[:60]
        print(f"  {name:<20} {typ:<10} {cat:<10} {desc}")
else:
    print("\nAll non-status 0-power moves are referenced!")