#!/usr/bin/env python3
"""
Parse README.md, execute each Python code block, and output a new
README with per-statement results in collapsible <details> sections.

Consecutive statements without output are merged into a single code
block. When a statement produces output, it and all preceding quiet
statements become one block with that output attached.

Usage:
    python build_readme.py                          # README.md -> README_with_output.md
    python build_readme.py --input README.md --output README_live.md
    python build_readme.py --inline                 # overwrite the input file
"""

import argparse
import ast
import io
import os
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

MAX_DICT_ITEMS = 50

try:
    LINE_WIDTH = os.get_terminal_size().columns
except (AttributeError, ValueError, OSError):
    LINE_WIDTH = 150

# Types whose repr is just noise (memory addresses, etc.)
_SUPPRESS_TYPES = set()

try:
    from frontierbrain3.frontier_db import Database, SetCollection, TrainerCollection
    _SUPPRESS_TYPES.add(Database)
    from frontierbrain3.facilities.tower import TowerDatabase
    _SUPPRESS_TYPES.add(TowerDatabase)
    from frontierbrain3.facilities.factory import FactoryDatabase
    _SUPPRESS_TYPES.add(FactoryDatabase)
except ImportError:
    SetCollection = None
    TrainerCollection = None


# -- Formatting ----------------------------------------------------------------

def _fmt_val(val) -> str:
    if isinstance(val, float):
        return f"{val:.4f}" if 0 < val < 0.01 else f"{val:.2f}"
    if isinstance(val, list) and len(repr(val)) > LINE_WIDTH:
        return _format_list(val)
    r = repr(val)
    r = re.sub(r'(\d+\.\d{2})\d+', r'\1', r)
    return r


def _format_list_inline(items: list, width: int = None) -> str:
    """Format a list with items wrapped across lines to fill available width."""
    if width is None:
        width = LINE_WIDTH
    if not items:
        return "[]"

    # Build comma-separated items, wrapping at width
    lines = ["["]
    current_line = "  "
    for i, item in enumerate(items):
        piece = repr(item)
        if i < len(items) - 1:
            piece += ","
        if len(current_line) + len(piece) + 1 > width and current_line.strip():
            lines.append(current_line)
            current_line = "  " + piece
        else:
            if current_line.strip():
                current_line += " " + piece
            else:
                current_line += piece
    if current_line.strip():
        lines.append(current_line)
    lines.append("]")
    return "\n".join(lines)


def _format_list(items: list, max_width=120) -> str:
    """Format a list. Short lists go on one line, longer ones wrap."""
    if not items:
        return "[]"
    r = repr(items)
    if len(r) <= max_width:
        return r
    return _format_list_inline(items)


def _format_dict(d: dict) -> str:
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


def _format_result(val) -> str:
    if SetCollection is not None and isinstance(val, SetCollection):
        ids = val.ids()
        return f"{repr(val)}\n{_format_list_inline(ids)}"
    if TrainerCollection is not None and isinstance(val, TrainerCollection):
        names = val.names()
        return f"{repr(val)}\n{_format_list_inline(names)}"
    if isinstance(val, dict):
        return _format_dict(val)
    if isinstance(val, list):
        return _format_list(val)
    return _fmt_val(val)


def _should_suppress(val) -> bool:
    return type(val) in _SUPPRESS_TYPES


# -- AST helpers ---------------------------------------------------------------

def _source_lines(node: ast.AST, code_lines: list[str]) -> str:
    if not hasattr(node, "lineno"):
        return "?"
    start = node.lineno - 1
    end = getattr(node, "end_lineno", node.lineno)
    return "\n".join(code_lines[start:end])


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


def _is_literal_assign(node: ast.AST) -> bool:
    """Return True if this is an assignment whose value is obvious from the code."""
    if not isinstance(node, ast.Assign):
        return False
    val = node.value
    return isinstance(val, (ast.List, ast.Dict, ast.Constant, ast.Tuple,
                            ast.JoinedStr, ast.Set,
                            ast.ListComp, ast.DictComp, ast.SetComp,
                            ast.GeneratorExp))


# -- Single statement execution ------------------------------------------------

def _exec_node(node: ast.AST, namespace: dict) -> str | None:
    """
    Execute one AST node. Returns output string if it produced something
    worth showing, or None.
    """
    output_parts = []

    if isinstance(node, ast.Expr):
        expr_code = compile(ast.Expression(node.value), "<readme>", "eval")
        captured = io.StringIO()
        with redirect_stdout(captured):
            result = eval(expr_code, namespace)
        stdout = captured.getvalue()
        if stdout.strip():
            output_parts.append(stdout.rstrip())
        if result is not None and not _should_suppress(result):
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
        if not _is_literal_assign(node):
            names = _assign_targets(node)
            for n in names:
                if n in namespace and not n.startswith("_"):
                    val = namespace[n]
                    if not _should_suppress(val):
                        output_parts.append(f"{n} = {_format_result(val)}")

    else:
        mod = ast.Module(body=[node], type_ignores=[])
        ast.fix_missing_locations(mod)
        captured = io.StringIO()
        with redirect_stdout(captured):
            exec(compile(mod, "<readme>", "exec"), namespace)
        stdout = captured.getvalue()
        if stdout.strip():
            output_parts.append(stdout.rstrip())

    combined = "\n".join(output_parts).strip()
    return combined if combined else None


# -- Emit helpers --------------------------------------------------------------

def _emit_block(output_lines: list, source_chunks: list[str],
                result: str | None, is_first: bool):
    """Emit one blockquote-wrapped code block with optional output."""
    if not is_first:
        output_lines.append("")
        output_lines.append("<br>")

    output_lines.append("")
    output_lines.append("> ```python")
    for chunk in source_chunks:
        for line in chunk.splitlines():
            output_lines.append(f"> {line}")
    output_lines.append("> ```")

    if result:
        output_lines.append(">")
        output_lines.append("> <details>")
        output_lines.append("> <summary>Output</summary>")
        output_lines.append(">")
        output_lines.append("> ```")
        for line in result.splitlines():
            output_lines.append(f"> {line}")
        output_lines.append("> ```")
        output_lines.append(">")
        output_lines.append("> </details>")

    output_lines.append("")


# -- Main builder --------------------------------------------------------------

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

            # Collect code lines (skip fences)
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # skip closing fence

            code = "\n".join(code_lines)
            if not code.strip():
                output_lines.append("```python")
                output_lines.extend(code_lines)
                output_lines.append("```")
                continue

            print(f"  Running block {block_num}...", end=" ", flush=True)

            try:
                tree = ast.parse(code, "<readme>")
            except SyntaxError as e:
                print(f"SYNTAX ERROR: {e}")
                output_lines.append("```python")
                output_lines.extend(code_lines)
                output_lines.append("```")
                continue

            # Execute statements one by one, accumulating source until output
            pending_source = []
            is_first_in_block = True

            for node in tree.body:
                src = _source_lines(node, code_lines)

                try:
                    result = _exec_node(node, namespace)
                except Exception as e:
                    result = f"ERROR: {type(e).__name__}: {e}"

                pending_source.append(src)

                if result is not None:
                    # Flush: emit accumulated source + this output
                    _emit_block(output_lines, pending_source, result,
                                is_first_in_block)
                    pending_source = []
                    is_first_in_block = False

            # Flush any remaining source without output
            if pending_source:
                _emit_block(output_lines, pending_source, None,
                            is_first_in_block)

            print("done")

        else:
            output_lines.append(lines[i])
            i += 1

    Path(output_path).write_text("\n".join(output_lines), encoding="utf-8")
    print(f"\nWrote {output_path} ({block_num} code blocks processed)")


def main():
    parser = argparse.ArgumentParser(
        description="Build README with executed code block outputs")
    parser.add_argument("--input", default="README.md", help="Input README path")
    parser.add_argument("--output", default=None, help="Output path")
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