#!/usr/bin/env python3
"""
Configuration Builder, Validator, and Constitution Renderer

The constitution template (.specify/memory/constitution.md) is the contract for
the root config.yaml: every {{key}}, {{#each key}}, and {{#if key}} placeholder
is a key the project must decide. Decisions come from the approved
docs/PRODUCT.md; the source of every value is recorded in its
"Configuration Decisions" table.

Usage (from the repository root):
    uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py scaffold [--force]
    uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py check
    uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py render [--verify]

Modes:
    scaffold  Write a config.yaml skeleton with every required key and the
              PRODUCT.md section each one usually comes from, and append an
              empty "## Configuration Decisions" table to docs/PRODUCT.md.
    check     Fail on missing or empty keys, missing item fields, keys without
              a verifiable recorded source, and recorded values that differ
              from config.yaml (collections as compact JSON).
    render    Run check, then render .sdd/constitution.md. Fails if any
              placeholder is left. --verify only compares the rendered output
              with the existing file and fails when it is out of date.

Every mode first requires an approved docs/PRODUCT.md that passes
validate_discovery.py, which also provides the PRODUCT.md section parser.

Options (before the mode):
    --template PATH   default .specify/memory/constitution.md
    --config PATH     default config.yaml
    --product PATH    default docs/PRODUCT.md
"""

import argparse
import json
import os
import re
import subprocess
import sys

import validate_discovery

DEFAULT_TEMPLATE = os.path.join(".specify", "memory", "constitution.md")
DEFAULT_OUTPUT = os.path.join(".sdd", "constitution.md")
DISCOVERY_VALIDATOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate_discovery.py")
DECISIONS_HEADING = validate_discovery.DECISIONS_HEADING

COMMENT_PATTERN = re.compile(r"\{\{!--.*?--\}\}\n*", re.DOTALL)
TOKEN_PATTERN = re.compile(r"\{\{\s*([#/]?)\s*([^{}]*?)\s*\}\}")
KEY_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)*$")
SOURCE_PATTERN = re.compile(r"^(?:PRODUCT\.md\s*§\s*\S.*|user,\s*\d{4}-\d{2}-\d{2})$")

NULL_VALUES = ("", "null", "~")
ROW_SPLIT = re.compile(r"(?<!\\)\|")
# Synthesized by the agent (TASK-006), so they can't be quoted from PRODUCT.md
# and must be confirmed by the user.
USER_CONFIRMED_KEYS = ("domain_sections",)

SCALAR = "scalar"
LIST = "list"
MAP = "map"

# Where the discovery workflow records each top-level decision.
SOURCE_HINTS = {
    "project": "Dev Environment Setup / Governance & Workflow",
    "runtime": "Tech Stack Selection / Dev Environment Setup",
    "project_structure": "Dev Environment Setup",
    "naming": "Use Cases / Functional Requirements",
    "agent": "Governance & Workflow",
    "commands": "Dev Environment Setup",
    "quality": "Governance & Workflow",
    "code_git": "Governance & Workflow",
    "known_constraints": "Risk Assessment / Architecture Decision Records",
    "domain_sections": "Use Cases / Functional Requirements / ADRs",
    "governance": "Governance & Workflow",
}


class TemplateError(Exception):
    pass


# ---------------------------------------------------------------------------
# Template parsing
# ---------------------------------------------------------------------------

def tokenize(template: str):
    """Split the template into text and tag tokens.

    A block tag ({{#...}} or {{/...}}) alone on its line consumes the whole
    line, so blocks do not leave blank lines behind.
    """
    template = COMMENT_PATTERN.sub("", template)
    tokens = []
    position = 0
    for match in TOKEN_PATTERN.finditer(template):
        start, end = match.start(), match.end()
        prefix, body = match.group(1), match.group(2)
        if prefix:
            line_start = template.rfind("\n", 0, start) + 1
            line_end = template.find("\n", end)
            line_end = len(template) if line_end == -1 else line_end
            if (
                line_start >= position
                and not template[line_start:start].strip()
                and not template[end:line_end].strip()
            ):
                start, end = line_start, min(line_end + 1, len(template))
        tokens.append(("text", template[position:start]))
        tokens.append((prefix or "var", body))
        position = end
    tokens.append(("text", template[position:]))
    return tokens


def parse(template: str):
    """Return a node list: ("text", s) | ("var", name) | (block, name, children)."""
    root = []
    stack = [("root", None, root)]
    for kind, body in tokenize(template):
        if kind == "text":
            if body:
                stack[-1][2].append(("text", body))
        elif kind == "var":
            stack[-1][2].append(("var", body))
        elif kind == "#":
            block, _, name = body.partition(" ")
            if block not in ("each", "if") or not name.strip():
                raise TemplateError(f"Unsupported block: {{{{#{body}}}}}")
            node = (block, name.strip(), [])
            stack[-1][2].append(node)
            stack.append(node)
        else:
            if len(stack) == 1 or stack[-1][0] != body:
                raise TemplateError(f"Unexpected closing tag: {{{{/{body}}}}}")
            stack.pop()
    if len(stack) > 1:
        raise TemplateError(f"Unclosed block: {{{{#{stack[-1][0]} {stack[-1][1]}}}}}")
    return root


def new_spec(kind, optional):
    return {"kind": kind, "fields": {}, "optional": optional}


def scan(nodes, required=None, item=None, optional=False, field_optional=False):
    """Collect {key: spec} for every root key the template uses.

    item is the spec of the enclosing {{#each}} (its "fields" receive
    {{this.field}} and {{#each this.field}} names). Keys inside {{#if}} are
    optional: they may be absent, empty, or false. Item fields are optional
    only under an {{#if}} inside the item itself.
    """
    if required is None:
        required = {}
    for node in nodes:
        kind, name = node[0], node[1]
        if kind == "text":
            continue
        if kind == "var":
            if name == "@key":
                if item is not None:
                    item["kind"] = MAP
            elif name.startswith("this."):
                if item is not None:
                    item["fields"].setdefault(name[len("this."):], new_spec(SCALAR, field_optional))
            elif name != "this":
                if not KEY_PATTERN.match(name):
                    raise TemplateError(f"Invalid placeholder: {{{{{name}}}}}")
                required.setdefault(name, new_spec(SCALAR, optional))
            continue
        if name.startswith("this."):
            if item is None:
                raise TemplateError(f"{{{{#{kind} {name}}}}} outside an each block")
            spec = item["fields"].setdefault(
                name[len("this."):], new_spec(LIST if kind == "each" else SCALAR, field_optional or kind == "if")
            )
        else:
            if not KEY_PATTERN.match(name):
                raise TemplateError(f"Invalid block key: {name}")
            default = LIST if kind == "each" else SCALAR
            spec = required.setdefault(name, new_spec(default, optional or kind == "if"))
        if kind == "each":
            if spec["kind"] == SCALAR:
                spec["kind"] = LIST
            scan(node[2], required, spec, optional, False)
        else:
            scan(node[2], required, item, True, True)
    for spec in required.values():
        if spec["kind"] == SCALAR and spec["fields"]:
            spec["kind"] = LIST
    return required


def load_template(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as error:
        fail(f"cannot read template '{path}': {error}")
    try:
        nodes = parse(text)
        return nodes, scan(nodes)
    except TemplateError as error:
        fail(f"{path}: {error}")


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def lookup(config, key):
    node = config
    for part in key.split("."):
        if not isinstance(node, dict) or part not in node:
            return False, None
        node = node[part]
    return True, node


def format_value(value, name):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (str, int, float)) and value != "":
        return str(value)
    raise TemplateError(f"{{{{{name}}}}} needs a non-empty scalar value, got {value!r}")


def resolve(name, config, scope):
    if name == "this":
        return scope["item"]
    if name == "@key":
        return scope["key"]
    if name.startswith("this."):
        item = scope["item"]
        field = name[len("this."):]
        if not isinstance(item, dict) or field not in item:
            raise TemplateError(f"Missing field '{field}' in {scope['path']}")
        return item[field]
    found, value = lookup(config, name)
    if not found:
        raise TemplateError(f"Missing key: {name}")
    return value


def render_nodes(nodes, config, scope):
    output = []
    for node in nodes:
        kind = node[0]
        if kind == "text":
            output.append(node[1])
        elif kind == "var":
            output.append(format_value(resolve(node[1], config, scope), node[1]))
        elif kind == "if":
            found, value = (True, resolve(node[1], config, scope)) if node[1].startswith("this") \
                else lookup(config, node[1])
            if found and not is_absent(value):
                output.append(render_nodes(node[2], config, scope))
        else:
            collection = resolve(node[1], config, scope)
            if isinstance(collection, dict):
                entries = list(collection.items())
            elif isinstance(collection, list):
                entries = list(enumerate(collection))
            else:
                raise TemplateError(f"{{{{#each {node[1]}}}}} needs a list or mapping")
            for key, item in entries:
                child = {"item": item, "key": key, "path": f"{node[1]}[{key}]"}
                output.append(render_nodes(node[2], config, child))
    return "".join(output)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def is_empty(value) -> bool:
    if isinstance(value, str):
        return value.strip() in NULL_VALUES
    return value is None or (isinstance(value, (list, dict)) and len(value) == 0)


def is_absent(value) -> bool:
    """An optional ({{#if}}) value that turns its block off."""
    return is_empty(value) or value is False or (isinstance(value, str) and value.strip() == "false")


def check_value(key, value, spec, issues):
    kind = spec["kind"]
    if kind == LIST and not isinstance(value, list):
        issues.append(f"Expected a list: {key}")
        return
    if kind == MAP and not isinstance(value, dict):
        issues.append(f"Expected a mapping: {key}")
        return
    if kind == SCALAR and isinstance(value, (list, dict)):
        issues.append(f"Expected a scalar value: {key}")
        return
    if not spec["fields"]:
        return
    items = value.items() if isinstance(value, dict) else enumerate(value)
    for item_name, item in items:
        for field, field_spec in spec["fields"].items():
            field_key = f"{key}[{item_name}].{field}"
            if not isinstance(item, dict) or is_empty(item.get(field)):
                if not field_spec["optional"]:
                    issues.append(f"Missing field: {field_key}")
                continue
            check_value(field_key, item[field], field_spec, issues)


def check_required(config, required) -> list:
    issues = []
    for key, spec in sorted(required.items()):
        found, value = lookup(config, key)
        if spec["optional"] and (not found or is_absent(value)):
            continue
        if not found:
            issues.append(f"Missing key: {key}")
        elif is_empty(value):
            issues.append(f"Empty value: {key}")
        else:
            check_value(key, value, spec, issues)
    return issues


# ---------------------------------------------------------------------------
# PRODUCT.md: discovery gate and Configuration Decisions table
# ---------------------------------------------------------------------------

def require_approved_product(product_path: str):
    if not os.path.isfile(product_path):
        fail(f"'{product_path}' not found. Complete WI-001 (discovery) before configuring the project.")
    result = subprocess.run(
        [sys.executable, "-I", DISCOVERY_VALIDATOR, product_path],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        failures = [line.strip() for line in result.stdout.splitlines() if "[FAIL]" in line]
        detail = "\n  ".join(failures) or result.stdout.strip() or result.stderr.strip()
        fail(f"'{product_path}' is not an approved discovery package (WI-001):\n  {detail}")
    with open(product_path, "r", encoding="utf-8") as f:
        return f.read()


def decisions_section(product: str):
    product = product.replace("\r\n", "\n")
    for heading, text, start, _ in validate_discovery.get_sections(product):
        if validate_discovery.is_decisions_section(product, heading, start):
            return text
    return None


def parse_decisions(product: str):
    """Return ({key: (value, source)}, [malformed-row issues]) or (None, [])."""
    section = decisions_section(product)
    if section is None:
        return None, []
    rows, issues = {}, []
    for number, line in enumerate(section.splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("|") or re.match(r"^\|[\s:|-]+\|?$", stripped):
            continue
        cells = [cell.strip().replace("\\|", "|") for cell in ROW_SPLIT.split(stripped.strip("|"))]
        key = cells[0].strip("`")
        if key.lower() == "key":
            continue
        if len(cells) != 3 or not KEY_PATTERN.match(key):
            issues.append(
                f"Malformed {DECISIONS_HEADING} row {number}: {stripped!r} "
                "(expected | key | value | source |; escape '|' in values as '\\|')"
            )
            continue
        rows[key] = (strip_code(cells[1]), cells[2])
    return rows, issues


def strip_code(text: str) -> str:
    return text[1:-1] if len(text) >= 2 and text[0] == text[-1] == "`" else text


def evidence_sections(product: str):
    """Return [(heading, text, is_leaf)] for the approved content of PRODUCT.md.

    The Approval and Configuration Decisions sections are removed first, so a
    citation can never reach the recorded values themselves.
    """
    content = validate_discovery.strip_unapproved(product)
    sections = validate_discovery.get_sections(content)
    leaves = validate_discovery.most_specific(sections)
    return [
        (heading, f"{heading}\n{text}", (heading, text, start, end) in leaves)
        for heading, text, start, end in sections
    ]


def cited_sections(product: str, reference: str):
    """Return (every matching section, the leaf ones) as text.

    A section matches when its heading is, starts with the number of, or
    contains the reference. Only leaf sections (no subsections) are evidence,
    so a broad heading such as the document title cannot vouch for a value.
    """
    wanted = re.sub(r"[`*]", "", reference).strip().lower().rstrip(".")
    matches, leaves = [], []
    for title, text, is_leaf in evidence_sections(product):
        heading = re.sub(r"[`*]", "", title).strip().lower()
        number = re.match(r"^(\d+(?:\.\d+)*)\.?\s", heading)
        if heading == wanted or (number and number.group(1) == wanted) or (len(wanted) >= 3 and wanted in heading):
            matches.append(text)
            if is_leaf:
                leaves.append(text)
    return matches, leaves


def appears_in(value: str, text: str) -> bool:
    """True when value occurs in text as a whole token, not inside a longer one.

    "3.1" does not match "3.12.2" and "main" does not match "domain"; a value
    may still end a sentence ("Python 3.12.").
    """
    pattern = rf"(?<![\w.]){re.escape(value.strip())}(?!\w|\.\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def scalar_items(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from scalar_items(item)
    elif isinstance(value, list):
        for item in value:
            yield from scalar_items(item)
    elif isinstance(value, str) and not is_empty(value):
        yield value


def collection_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def normalize_collection(value):
    """Make recorded JSON comparable with BaseLoader output (all scalars text)."""
    if isinstance(value, dict):
        return {str(k): normalize_collection(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_collection(v) for v in value]
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def check_decisions(config, required, product) -> list:
    rows, issues = parse_decisions(product)
    if rows is None:
        return [f"docs/PRODUCT.md has no '## {DECISIONS_HEADING}' table. Run scaffold."]
    for key, spec in sorted(required.items()):
        if key not in rows:
            issues.append(f"No {DECISIONS_HEADING} row for: {key}")
            continue
        recorded, source = rows[key]
        found, value = lookup(config, key)
        if not SOURCE_PATTERN.match(source):
            issues.append(
                f"Invalid source for {key}: {source!r} "
                "(use 'PRODUCT.md § <section>' or 'user, YYYY-MM-DD')"
            )
        elif key in USER_CONFIRMED_KEYS and source.startswith("PRODUCT.md"):
            issues.append(
                f"Source for {key} must be 'user, YYYY-MM-DD': it is proposed from PRODUCT.md "
                "and confirmed by the user, not quoted from it"
            )
        elif source.startswith("PRODUCT.md"):
            reference = source.split("§", 1)[1]
            matches, sections = cited_sections(product, reference)
            if not matches:
                issues.append(f"Source for {key} cites a section PRODUCT.md does not have: {source!r}")
            elif not sections:
                issues.append(
                    f"Source for {key} cites a section with subsections: {source!r}. "
                    "Cite the specific subsection that states the value"
                )
            elif found:
                unsupported = [
                    item for item in scalar_items(value)
                    if not any(appears_in(item, text) for text in sections)
                ]
                if unsupported:
                    issues.append(
                        f"Value of {key} ({', '.join(map(repr, unsupported))}) does not appear in "
                        f"the cited section {source!r}; if the user decided it, use 'user, YYYY-MM-DD'"
                    )
        if not found or is_empty(value):
            continue
        if isinstance(value, (list, dict)):
            try:
                matches = normalize_collection(json.loads(recorded)) == value
            except ValueError:
                matches = False
            if not matches:
                issues.append(
                    f"Recorded value for {key} must be the compact JSON of config.yaml: {collection_text(value)}"
                )
        elif recorded != str(value):
            issues.append(f"Recorded value for {key} ({recorded!r}) differs from config.yaml ({value!r})")
    return issues


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

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
    return isinstance(node, dict) and "kind" in node and "optional" in node


def describe(spec) -> str:
    optional = " (optional)" if spec["optional"] else ""
    if spec["kind"] == SCALAR:
        return f"value{optional}"
    fields = ", ".join(spec["fields"])
    if spec["kind"] == LIST:
        return f"list{optional}" + (f" of {{{fields}}}" if fields else "")
    return f"map{optional} of <name>: " + (f"{{{fields}}}" if fields else "<value>")


def render_skeleton(tree, indent=0) -> str:
    lines = []
    pad = "  " * indent
    for name, node in tree.items():
        hint = SOURCE_HINTS.get(name) if indent == 0 else None
        if is_spec(node):
            empty = {SCALAR: "", LIST: " []", MAP: " {}"}[node["kind"]]
            source = f"; PRODUCT.md: {hint}" if hint else ""
            lines.append(f"{pad}{name}:{empty}  # {describe(node)}{source}")
        else:
            lines.append(f"{pad}{name}:" + (f"  # PRODUCT.md: {hint}" if hint else ""))
            lines.append(render_skeleton(node, indent + 1))
    return "\n".join(lines)


def load_config(path: str):
    try:
        import yaml
    except ImportError:
        fail("PyYAML is required. Run with `uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py ...`.")
    try:
        with open(path, "r", encoding="utf-8") as f:
            # BaseLoader keeps every scalar as written: dates stay ISO text and
            # versions such as 1.10 are not turned into floats.
            return yaml.load(f, Loader=yaml.BaseLoader) or {}
    except OSError as error:
        fail(f"cannot read '{path}': {error}")
    except yaml.YAMLError as error:
        fail(f"'{path}' is not valid YAML: {error}")


def scaffold(args):
    product = require_approved_product(args.product)
    _, required = load_template(args.template)
    if os.path.exists(args.config) and not args.force:
        fail(f"'{args.config}' already exists. Use --force to overwrite it.")
    header = (
        f"# Generated from {args.template} by validate_config.py scaffold.\n"
        f"# Fill each value from {args.product} and record its source in the\n"
        f"# '{DECISIONS_HEADING}' table there; ask the user for anything it does\n"
        "# not state. Then run: uv run --with pyyaml==6.0.2 python skills/tech-use-case-discovery/scripts/validate_config.py check\n"
    )
    with open(args.config, "w", encoding="utf-8") as f:
        f.write(header + render_skeleton(build_tree(required)) + "\n")
    print(f"[PASS] Wrote {len(required)} required key(s) to {args.config}.")

    if decisions_section(product) is None:
        rows = "\n".join(f"| `{key}` |  |  |" for key in sorted(required))
        with open(args.product, "a", encoding="utf-8") as f:
            f.write(
                f"\n## {DECISIONS_HEADING}\n\n"
                "Source is `PRODUCT.md § <section>` (an existing heading, or its number, with no\n"
                "subsections and whose text contains the value) or `user, YYYY-MM-DD` for\n"
                "values the user decided or confirmed. Lists and maps are recorded as compact JSON; escape `|` as `\\|`.\n\n"
                "| Key | Value | Source |\n| :--- | :--- | :--- |\n" + rows + "\n"
            )
        print(f"[PASS] Appended an empty '{DECISIONS_HEADING}' table to {args.product}.")


def run_check(args):
    """Load the inputs once and check them; render reuses the loaded template and config."""
    product = require_approved_product(args.product)
    nodes, required = load_template(args.template)
    config = load_config(args.config)
    issues = check_required(config, required) + check_decisions(config, required, product)
    report(issues, args.config)
    return nodes, config, required


def check(args):
    _, _, required = run_check(args)
    print(f"[PASS] {args.config} defines all {len(required)} template key(s) with recorded sources.")


def render(args):
    nodes, config, _ = run_check(args)
    try:
        rendered = render_nodes(nodes, config, {"item": None, "key": None, "path": ""})
    except TemplateError as error:
        fail(f"render failed: {error}")
    leftover = sorted(set(re.findall(r"\{\{[^}]*\}\}", rendered)))
    if leftover:
        fail(f"rendered output still contains placeholders: {', '.join(leftover)}")

    if args.verify:
        try:
            with open(args.output, "r", encoding="utf-8") as f:
                current = f.read()
        except OSError:
            fail(f"'{args.output}' does not exist. Run render.")
        if current != rendered:
            fail(f"'{args.output}' is out of date with {args.config}. Run render.")
        print(f"[PASS] {args.output} is up to date.")
        return
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"[PASS] Rendered {args.output} from {args.config}.")


def report(issues, config_path):
    for issue in issues:
        print(f"[FAIL] {issue}")
    if issues:
        print(f"\n{len(issues)} pending key(s) or inconsistencies in {config_path}.")
        sys.exit(1)


def fail(message: str):
    print(f"Error: {message}")
    sys.exit(1)


def main():
    validate_discovery.use_utf8_output()
    parser = argparse.ArgumentParser(description="Build, validate, and render the project configuration.")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE)
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--product", default=os.path.join("docs", "PRODUCT.md"))
    modes = parser.add_subparsers(dest="mode", required=True)
    scaffold_parser = modes.add_parser("scaffold")
    scaffold_parser.add_argument("--force", action="store_true")
    modes.add_parser("check")
    render_parser = modes.add_parser("render")
    render_parser.add_argument("--output", default=DEFAULT_OUTPUT)
    render_parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    {"scaffold": scaffold, "check": check, "render": render}[args.mode](args)


if __name__ == "__main__":
    main()
