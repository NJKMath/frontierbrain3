#!/usr/bin/env python3
"""
Extract and run every Python code block from README.md to verify correctness.

Blocks are executed sequentially in a shared namespace, so variables defined
in earlier blocks are available to later ones (matching how a reader would
build up state while following the README top to bottom).

Usage:
    python test_readme.py                # run all blocks
    python test_readme.py --stop         # stop on first failure
    python test_readme.py --block 5      # run only block 5
    python test_readme.py --list         # list all blocks without running
    python test_readme.py --from 8       # run blocks 8 onward
"""

import argparse
import re
import sys
import traceback
from pathlib import Path


def extract_blocks(readme_path: str) -> list[dict]:
    """Extract all ```python code blocks with context."""
    text = Path(readme_path).read_text(encoding="utf-8")
    lines = text.splitlines()

    blocks = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("```python"):
            # Walk backward to find the nearest heading
            heading = "(no heading)"
            for j in range(i - 1, -1, -1):
                if lines[j].startswith("#"):
                    heading = lines[j].lstrip("#").strip()
                    break

            # Collect code lines
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1

            code = "\n".join(code_lines)
            blocks.append({
                "index": len(blocks) + 1,
                "heading": heading,
                "code": code,
                "preview": code_lines[0].strip() if code_lines else "",
                "line_count": len(code_lines),
            })
        i += 1

    return blocks


def run_block(block: dict, namespace: dict, verbose: bool = True) -> bool:
    """Execute a code block. Returns True on success."""
    idx = block["index"]
    heading = block["heading"]
    code = block["code"]

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"  Block {idx}: {heading}")
        print(f"  ({block['line_count']} lines, starts with: {block['preview']!r})")
        print(f"{'=' * 60}")

    try:
        exec(compile(code, f"<README block {idx}>", "exec"), namespace)
        if verbose:
            print(f"  PASS")
        return True
    except Exception as e:
        if verbose:
            print(f"  FAIL: {type(e).__name__}: {e}")
            print()
            # Show the code with line numbers for debugging
            for i, line in enumerate(code.splitlines(), 1):
                print(f"    {i:3d} | {line}")
            print()
            traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Test README.md code blocks")
    parser.add_argument("--readme", default="README.md", help="Path to README")
    parser.add_argument("--stop", action="store_true", help="Stop on first failure")
    parser.add_argument("--block", type=int, help="Run only this block number")
    parser.add_argument("--list", action="store_true", help="List blocks, don't run")
    parser.add_argument("--from", type=int, dest="from_block", help="Start from this block")
    parser.add_argument("--quiet", action="store_true", help="Only show failures")
    args = parser.parse_args()

    readme_path = Path(args.readme)
    if not readme_path.exists():
        print(f"Error: {readme_path} not found")
        sys.exit(1)

    blocks = extract_blocks(str(readme_path))
    print(f"Found {len(blocks)} Python code blocks in {readme_path}\n")

    if args.list:
        for b in blocks:
            print(f"  {b['index']:3d}. [{b['heading']}] ({b['line_count']} lines)")
            print(f"       {b['preview']}")
        return

    # Filter blocks
    if args.block:
        blocks = [b for b in blocks if b["index"] == args.block]
        if not blocks:
            print(f"Error: block {args.block} not found")
            sys.exit(1)
    elif args.from_block:
        blocks = [b for b in blocks if b["index"] >= args.from_block]

    # Shared namespace across all blocks
    namespace = {"__builtins__": __builtins__}

    passed = 0
    failed = 0
    failed_blocks = []

    for block in blocks:
        verbose = not args.quiet or True  # always show block header
        ok = run_block(block, namespace, verbose=not args.quiet)
        if ok:
            passed += 1
        else:
            failed += 1
            failed_blocks.append(block["index"])
            if args.stop:
                print(f"\nStopping on first failure (--stop)")
                break

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  Results: {passed} passed, {failed} failed out of {passed + failed}")
    if failed_blocks:
        print(f"  Failed blocks: {failed_blocks}")
    print(f"{'=' * 60}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()