#!/usr/bin/env python3
"""
Parse README.md, execute each Python code block, and output a new
README with per-statement results in collapsible <details> sections.

Each statement within a code block becomes its own fenced code block
followed by a collapsible output section (if it produces output).

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
from contextlib import redirect_stdout
from pathlib import Path

MAX_LIST_ITEMS = 15
MAX_DICT_ITEMS = 20

# Types whose repr is just noise (memory addresses, etc.)
_SUPPRESS_TYPES = set()

try:
    from frontierbrain3.frontier_db import Database, SetCollection, TrainerCollection
    _SUPPRESS_TYPES.add(Database)
except ImportError:
    SetCollection = None
    TrainerCollection = None


# -- Formatting ----------------------------------------------------------------

def _fmt_val(val) -> str:
    if isinstance(val, float):
        return f"{val:.4f}" if 0 < val < 0.01 else f"{val:.2f}"
    if isinstance(val, list) and len(val) > MAX_LIST_ITEMS * 2:
        return (f"[{repr(val[0])}, {repr(val[1])}, "
                f"... {len(val)} items ... "
                f"{repr(val[-2])}, {repr(val[-1])}]")
    r = repr(val)
    r = re.sub(r'(\d+\.\d{2})\d+', r'\1', r)
    return r


def _format_list(items: list, max_width=120) -> str:
    if not items:
        return "[]"
    if len(items) <= MAX_LIST_ITEMS * 2:
        r = repr(items)
        if len(r) <= max_width:
            return r
        lines = ["["]
        for item in items:
            lines.append(f"  {_fmt_val(item)},")
        lines.append("]")
        return "\n".join(lines)
    lines = [f"[  # {len(items)} items"]
    for item in items[:MAX_LIST_ITEMS]:
        lines.append(f"  {_fmt_val(item)},")
    lines.append(f"  ... ({len(items) - MAX_LIST_ITEMS * 2} more) ...")
    for item in items[-MAX_LIST_ITEMS:]:
        lines.append(f"  {_fmt_val(item)},")
    lines.append("]")
    return "\n".join(lines)


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
        return f"{repr(val)}\n{_format_list(ids)}"
    if TrainerCollection is not None and isinstance(val, TrainerCollection):
        names = val.names()
        return f"{repr(val)}\n{_format_list(names)}"
    if isinstance(val, dict):
        return _format_dict(val)
    if isinstance(val, list):
        return _format_list(val)
    return _fmt_val(val)


def _should_suppress(val) -> bool:
    """Return True if this value's repr is just noise."""
    return type(val) in _SUPPRESS_TYPES


# -- AST helpers ---------------------------------------------------------------

def _source_lines(node: ast.AST, code_lines: list[str]) -> str:
    """Get the full source text for a node (possibly multi-line)."""
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


def _is_import(node: ast.AST) -> bool:
    return isinstance(node, (ast.Import, ast.ImportFrom))


# -- Statement grouping -------------------------------------------------------

def _group_statements(tree: ast.Module, code_lines: list[str]) -> list[dict]:
    """
    Group AST nodes into logical chunks. Consecutive imports merge into
    one group. Everything else is its own group.
    """
    groups = []
    pending_imports = []

    def flush_imports():
        if pending_imports:
            src = "\n".join(
                _source_lines(n, code_lines) for n in pending_imports
            )
            groups.append({"nodes": list(pending_imports), "source": src, "kind": "imports"})
            pending_imports.clear()

    for node in tree.body:
        if _is_import(node):
            pending_imports.append(node)
        else:
            flush_imports()
            src = _source_lines(node, code_lines)
            if isinstance(node, ast.Expr):
                groups.append({"nodes": [node], "source": src, "kind": "expr"})
            elif isinstance(node, ast.Assign):
                groups.append({"nodes": [node], "source": src, "kind": "assign"})
            else:
                groups.append({"nodes": [node], "source": src, "kind": "other"})

    flush_imports()
    return groups


# -- Execution -----------------------------------------------------------------

def _run_group(group: dict, namespace: dict) -> str | None:
    """
    Execute a statement group. Returns output string, or None if nothing
    worth showing.
    """
    nodes = group["nodes"]
    kind = group["kind"]
    output_parts = []

    for node in nodes:
        if kind == "imports" or kind == "other":
            mod = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(mod)
            captured = io.StringIO()
            with redirect_stdout(captured):
                exec(compile(mod, "<readme>", "exec"), namespace)
            stdout = captured.getvalue()
            if stdout.strip():
                output_parts.append(stdout.rstrip())

        elif kind == "expr":
            expr_code = compile(ast.Expression(node.value), "<readme>", "eval")
            captured = io.StringIO()
            with redirect_stdout(captured):
                result = eval(expr_code, namespace)
            stdout = captured.getvalue()
            if stdout.strip():
                output_parts.append(stdout.rstrip())
            if result is not None and not _should_suppress(result):
                output_parts.append(_format_result(result))

        elif kind == "assign":
            mod = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(mod)
            captured = io.StringIO()
            with redirect_stdout(captured):
                exec(compile(mod, "<readme>", "exec"), namespace)
            stdout = captured.getvalue()
            if stdout.strip():
                output_parts.append(stdout.rstrip())
            names = _assign_targets(node)
            for n in names:
                if n in namespace and not n.startswith("_"):
                    val = namespace[n]
                    if not _should_suppress(val):
                        output_parts.append(f"{n} = {_format_result(val)}")

    combined = "\n".join(output_parts).strip()
    return combined if combined else None


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
                # Empty block, just emit it as-is
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

            groups = _group_statements(tree, code_lines)

            for group in groups:
                src = group["source"]

                # Run it
                try:
                    result = _run_group(group, namespace)
                except Exception as e:
                    result = f"ERROR: {type(e).__name__}: {e}"

                # Emit as a blockquote-wrapped code block + optional output
                output_lines.append("")
                output_lines.append("> ```python")
                for src_line in src.splitlines():
                    output_lines.append(f"> {src_line}")
                output_lines.append("> ```")

                if result:
                    output_lines.append(">")
                    output_lines.append("> <details>")
                    output_lines.append("> <summary>Output</summary>")
                    output_lines.append(">")
                    output_lines.append("> ```")
                    for res_line in result.splitlines():
                        output_lines.append(f"> {res_line}")
                    output_lines.append("> ```")
                    output_lines.append(">")
                    output_lines.append("> </details>")
                output_lines.append("")

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