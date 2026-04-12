#!/usr/bin/env python3
"""
Parse README.md, execute each Python code block, and output a new
README with results inserted in collapsible <details> sections.

Usage:
    python build_readme.py                          # README.md -> README_with_output.md
    python build_readme.py --input README.md --output README_live.md
    python build_readme.py --inline                 # overwrite the input file
"""

import argparse
import ast
import io
import re
import sys
import textwrap
from contextlib import redirect_stdout
from pathlib import Path


def run_block_repl(code: str, namespace: dict) -> str:
    """
    Execute a code block in REPL style, capturing output for every statement.
    Returns the combined output string.
    """
    code_lines = code.splitlines()
    output_parts = []

    try:
        tree = ast.parse(code, "<readme>")
    except SyntaxError as e:
        return f"SyntaxError: {e}"

    for node in tree.body:
        src = _source_line(node, code_lines)

        try:
            if isinstance(node, ast.Expr):
                expr_code = compile(ast.Expression(node.value), "<readme>", "eval")
                captured = io.StringIO()
                with redirect_stdout(captured):
                    result = eval(expr_code, namespace)
                stdout = captured.getvalue()
                if stdout.strip():
                    output_parts.append(stdout.rstrip())
                if result is not None:
                    output_parts.append(f">>> {src}")
                    output_parts.append(_format_result(result))

            elif isinstance(node, ast.Assign):
                mod = ast.Module(body=[node], type_ignores=[])
                ast.fix_missing_locations(mod)
                captured = io.StringIO()
                with redirect_stdout(captured):
                    exec(compile(mod, "<readme>", "exec"), namespace)
                stdout = captured.getvalue()
                if stdout.strip():
                    output_parts.append(stdout.rstrip())
                names = _assign_targets(node)
                if names:
                    for n in names:
                        if n in namespace and not n.startswith("_"):
                            output_parts.append(f">>> {src}")
                            output_parts.append(f"{n} = {_format_result(namespace[n])}")

            else:
                mod = ast.Module(body=[node], type_ignores=[])
                ast.fix_missing_locations(mod)
                captured = io.StringIO()
                with redirect_stdout(captured):
                    exec(compile(mod, "<readme>", "exec"), namespace)
                stdout = captured.getvalue()
                if stdout.strip():
                    output_parts.append(stdout.rstrip())

        except Exception as e:
            output_parts.append(f">>> {src}")
            output_parts.append(f"  ERROR: {type(e).__name__}: {e}")

    return "\n".join(output_parts)


def _source_line(node: ast.AST, code_lines: list[str]) -> str:
    if hasattr(node, "lineno"):
        idx = node.lineno - 1
        if 0 <= idx < len(code_lines):
            line = code_lines[idx].strip()
            if hasattr(node, "end_lineno") and node.end_lineno > node.lineno:
                return line + " ..."
            return line
    return "?"


def _assign_targets(node: ast.Assign) -> list[str]:
    names = []
    for target in node.targets:
        if isinstance(target, ast.Name):
            names.append(target.id)
        elif isinstance(target, ast.Tuple):
            for elt in target.elts:
                if isinstance(elt, ast.Name):
                    names.append(elt.id)
    return names


MAX_LIST_ITEMS = 15    # show first/last N items for long lists
MAX_DICT_ITEMS = 20   # show first N entries for long dicts


def _format_result(val, max_width=120) -> str:
    """Format a value for display in the output block."""
    # Import here to avoid circular issues at module level
    try:
        from frontierbrain3.frontier_db import SetCollection, TrainerCollection
        if isinstance(val, SetCollection):
            ids = val.ids()
            return f"{repr(val)}\n{_format_list(ids)}"
        if isinstance(val, TrainerCollection):
            names = val.names()
            return f"{repr(val)}\n{_format_list(names)}"
    except ImportError:
        pass

    if isinstance(val, dict):
        return _format_dict(val)
    if isinstance(val, list):
        return _format_list(val)
    return _fmt_val(val)


def _format_list(items: list, max_width=120) -> str:
    """Format a list, truncating the middle if too long."""
    if not items:
        return "[]"
    if len(items) <= MAX_LIST_ITEMS * 2:
        r = repr(items)
        if len(r) <= max_width:
            return r
        # Multi-line but still all items
        lines = ["["]
        for item in items:
            lines.append(f"  {_fmt_val(item)},")
        lines.append("]")
        return "\n".join(lines)
    # Truncate: show first N and last N
    lines = [f"[  # {len(items)} items"]
    for item in items[:MAX_LIST_ITEMS]:
        lines.append(f"  {_fmt_val(item)},")
    lines.append(f"  ... ({len(items) - MAX_LIST_ITEMS * 2} more) ...")
    for item in items[-MAX_LIST_ITEMS:]:
        lines.append(f"  {_fmt_val(item)},")
    lines.append("]")
    return "\n".join(lines)


def _format_dict(d: dict) -> str:
    """Format a dict, truncating if too many entries."""
    if not d:
        return "{}"
    items = list(d.items())
    if len(items) <= MAX_DICT_ITEMS:
        lines = ["{"]
        for k, v in items:
            lines.append(f"  {repr(k)}: {_fmt_val(v)},")
        lines.append("}")
        return "\n".join(lines)
    lines = [f"{{  # {len(items)} entries"]
    for k, v in items[:MAX_DICT_ITEMS]:
        lines.append(f"  {repr(k)}: {_fmt_val(v)},")
    lines.append(f"  ... ({len(items) - MAX_DICT_ITEMS} more) ...")
    lines.append("}")
    return "\n".join(lines)


def _fmt_val(val) -> str:
    if isinstance(val, float):
        return f"{val:.4f}" if 0 < val < 0.01 else f"{val:.2f}"
    if isinstance(val, list) and len(val) > MAX_LIST_ITEMS * 2:
        return f"[{repr(val[0])}, {repr(val[1])}, ... {len(val)} items ... {repr(val[-2])}, {repr(val[-1])}]"
    r = repr(val)
    r = re.sub(r'(\d+\.\d{2})\d+', r'\1', r)
    return r


def build_readme(input_path: str, output_path: str):
    text = Path(input_path).read_text(encoding="utf-8")
    lines = text.splitlines()
    namespace = {"__builtins__": __builtins__}

    output_lines = []
    i = 0
    block_num = 0

    while i < len(lines):
        if lines[i].strip().startswith("```python"):
            block_num += 1

            # Collect the code block including fences
            block_start = i
            code_lines = []
            output_lines.append(lines[i])  # opening fence
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                output_lines.append(lines[i])
                i += 1
            if i < len(lines):
                output_lines.append(lines[i])  # closing fence
                i += 1

            code = "\n".join(code_lines)

            # Skip trivially empty blocks
            stripped = code.strip()
            if not stripped:
                continue

            # Run the block
            print(f"  Running block {block_num}...", end=" ", flush=True)
            result = run_block_repl(code, namespace)
            print("done")

            # Insert output in a <details> block if there's any output
            if result.strip():
                output_lines.append("")
                output_lines.append("<details>")
                output_lines.append("<summary>Output</summary>")
                output_lines.append("")
                output_lines.append("```")
                output_lines.append(result)
                output_lines.append("```")
                output_lines.append("")
                output_lines.append("</details>")
                output_lines.append("")
        else:
            output_lines.append(lines[i])
            i += 1

    Path(output_path).write_text("\n".join(output_lines), encoding="utf-8")
    print(f"\nWrote {output_path} ({block_num} code blocks processed)")


def main():
    parser = argparse.ArgumentParser(
        description="Build README with executed code block outputs")
    parser.add_argument("--input", default="README.md", help="Input README path")
    parser.add_argument("--output", default=None, help="Output path (default: README_with_output.md)")
    parser.add_argument("--inline", action="store_true", help="Overwrite the input file")
    args = parser.parse_args()

    if args.inline:
        out = args.input
    elif args.output:
        out = args.output
    else:
        stem = Path(args.input).stem
        out = f"{stem}_with_output.md"

    build_readme(args.input, out)


if __name__ == "__main__":
    main()