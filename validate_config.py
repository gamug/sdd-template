#!/usr/bin/env python3
"""
Configuration Builder and Validator

Scans the constitution template for every `{{key}}` and `{{#each key}}`
placeholder and uses that list as the contract for the root config.yaml.

Usage:
    python validate_config.py scaffold [--output config.yaml] [--force]
    uv run --with pyyaml python validate_config.py check [config.yaml]

Modes:
    scaffold  Write a config.yaml skeleton containing every key the template
              requires, with empty values to be filled from docs/PRODUCT.md
              or an explicit user decision. Refuses to overwrite an existing
              file unless --force is given.
    check     Fail when a required key is missing or empty, when a collection
              item lacks a required field, or when related values drift
              (devcontainer.image Python version vs runtime.version).

Options:
    --template PATH   Constitution template to scan
                      (default: .specify/memory/constitution.md).
"""

import argparse
import os
import re
import sys

DEFAULT_TEMPLATE = os.path.join(".specify", "memory", "constitution.md")
TOKEN_PATTERN = re.compile(r"\{\{\s*([#/]?)\s*([^{}]*?)\s*\}\}")
KEY_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)*$")

SCALAR = "scalar"
LIST = "list"
MAP = "map"


def scan_template(template: str):
    """Return {dotted_key: spec} for every placeholder in the template.

    spec is {"kind": scalar|list|map, "fields": [...]}. A collection is a map
    when its block uses {{@key}}; "fields" lists the {{this.field}} names its
    items must define (empty when items are scalars).
    """
    required = {}
    stack = []
    for match in TOKEN_PATTERN.finditer(template):
        prefix, body = match.group(1), match.group(2)
        if prefix == "#":
            key = body[len("each"):].strip() if body.startswith("each") else ""
            if KEY_PATTERN.match(key):
                required.setdefault(key, {"kind": LIST, "fields": []})
                stack.append(key)
            else:
                stack.append(None)
        elif prefix == "/":
            if stack:
                stack.pop()
        elif body == "@key":
            if stack and stack[-1]:
                required[stack[-1]]["kind"] = MAP
        elif body.startswith("this."):
            if stack and stack[-1]:
                field = body[len("this."):]
                fields = required[stack[-1]]["fields"]
                if field not in fields:
                    fields.append(field)
        elif body != "this" and KEY_PATTERN.match(body):
            required.setdefault(body, {"kind": SCALAR, "fields": []})
    return required


def build_tree(required):
    tree = {}
    for key, spec in required.items():
        node = tree
        parts = key.split(".")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = spec
    return tree


def is_spec(node) -> bool:
    return isinstance(node, dict) and "kind" in node and "fields" in node


def render_skeleton(tree, indent=0) -> str:
    lines = []
    pad = "  " * indent
    for name, node in tree.items():
        if is_spec(node):
            kind, fields = node["kind"], node["fields"]
            if kind == SCALAR:
                lines.append(f"{pad}{name}:  # required value")
            elif kind == LIST:
                hint = f" items need: {', '.join(fields)}" if fields else " non-empty list"
                lines.append(f"{pad}{name}: []  #{hint}")
            else:
                hint = f" <name>: {{{', '.join(fields)}}}" if fields else " <name>: <value>"
                lines.append(f"{pad}{name}: {{}}  # map of{hint}")
        else:
            lines.append(f"{pad}{name}:")
            lines.append(render_skeleton(node, indent + 1))
    return "\n".join(lines)


def is_empty(value) -> bool:
    return value is None or (isinstance(value, (str, list, dict)) and len(value) == 0)


def lookup(config, key):
    node = config
    for part in key.split("."):
        if not isinstance(node, dict) or part not in node:
            return False, None
        node = node[part]
    return True, node


def check_required(config, required) -> list:
    issues = []
    for key, spec in sorted(required.items()):
        found, value = lookup(config, key)
        if not found:
            issues.append(f"Missing key: {key}")
            continue
        if is_empty(value):
            issues.append(f"Empty value: {key}")
            continue
        kind, fields = spec["kind"], spec["fields"]
        if kind == LIST and not isinstance(value, list):
            issues.append(f"Expected a list: {key}")
        elif kind == MAP and not isinstance(value, dict):
            issues.append(f"Expected a mapping: {key}")
        elif kind == SCALAR and isinstance(value, (list, dict)):
            issues.append(f"Expected a scalar value: {key}")
        elif fields:
            items = value.items() if isinstance(value, dict) else enumerate(value)
            for item_name, item in items:
                for field in fields:
                    if not isinstance(item, dict) or is_empty(item.get(field)):
                        issues.append(f"Missing field '{field}' in {key}.{item_name}")
    return issues


PYTHON_IMAGE_PATTERN = re.compile(r"devcontainers/python:(?:\d+-)?(\d+)\.(\d+)")
CONSTRAINT_PATTERN = re.compile(r"^\s*(>=|<=|==|>|<)\s*(\d+)(?:\.(\d+))?\s*$")


def satisfies(version, constraint: str) -> bool:
    for clause in constraint.split(","):
        match = CONSTRAINT_PATTERN.match(clause)
        if not match:
            raise ValueError(f"Unsupported version constraint: {clause!r}")
        operator, major, minor = match.group(1), int(match.group(2)), int(match.group(3) or 0)
        bound = (major, minor)
        if not {
            ">=": version >= bound,
            "<=": version <= bound,
            "==": version == bound,
            ">": version > bound,
            "<": version < bound,
        }[operator]:
            return False
    return True


def check_python_runtime(config) -> list:
    runtime = config.get("runtime") or {}
    image = (config.get("devcontainer") or {}).get("image")
    if str(runtime.get("language", "")).lower() != "python" or not image:
        return []
    match = PYTHON_IMAGE_PATTERN.search(str(image))
    if not match:
        return []
    image_version = (int(match.group(1)), int(match.group(2)))
    constraint = str(runtime.get("version", ""))
    try:
        if satisfies(image_version, constraint):
            return []
    except ValueError as error:
        return [str(error)]
    return [
        f"devcontainer.image uses Python {image_version[0]}.{image_version[1]}, "
        f"which does not satisfy runtime.version {constraint!r}."
    ]


def read_template(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as error:
        print(f"Error: cannot read template '{path}': {error}")
        sys.exit(1)


def scaffold(args):
    if os.path.exists(args.output) and not args.force:
        print(f"Error: '{args.output}' already exists. Use --force to overwrite it.")
        sys.exit(1)
    required = scan_template(read_template(args.template))
    header = (
        f"# Generated from {args.template} by validate_config.py scaffold.\n"
        "# Fill every value from docs/PRODUCT.md or an explicit user decision,\n"
        "# then run: uv run --with pyyaml python validate_config.py check\n"
    )
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(header + render_skeleton(build_tree(required)) + "\n")
    print(f"[PASS] Wrote {len(required)} required key(s) to {args.output}.")


def check(args):
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML is required. Run with `uv run --with pyyaml python ...`.")
        sys.exit(1)
    try:
        with open(args.config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except OSError as error:
        print(f"Error: cannot read '{args.config}': {error}")
        sys.exit(1)

    required = scan_template(read_template(args.template))
    issues = check_required(config, required) + check_python_runtime(config)
    for issue in issues:
        print(f"[FAIL] {issue}")
    if issues:
        print(f"\n{len(issues)} pending key(s) or inconsistencies in {args.config}.")
        sys.exit(1)
    print(f"[PASS] {args.config} defines all {len(required)} template key(s) consistently.")


def main():
    parser = argparse.ArgumentParser(description="Build and validate the root config.yaml.")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE)
    modes = parser.add_subparsers(dest="mode", required=True)
    scaffold_parser = modes.add_parser("scaffold")
    scaffold_parser.add_argument("--output", default="config.yaml")
    scaffold_parser.add_argument("--force", action="store_true")
    check_parser = modes.add_parser("check")
    check_parser.add_argument("config", nargs="?", default="config.yaml")
    args = parser.parse_args()
    scaffold(args) if args.mode == "scaffold" else check(args)


if __name__ == "__main__":
    main()
