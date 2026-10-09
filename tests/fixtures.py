"""Shared fixtures for the validator regression tests.

A Project is a scratch fork: the bundled, approved sample discovery package as
docs/PRODUCT.md, plus a config.yaml and Configuration Decisions table generated
from the real constitution template so every key is defined. Tests override
single values or sources and run the validators as the agent would.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "sdd-init", "scripts")
sys.path.insert(0, SCRIPTS)

import validate_config  # noqa: E402

CONFIG_SCRIPT = os.path.join(SCRIPTS, "validate_config.py")
DISCOVERY_SCRIPT = os.path.join(SCRIPTS, "validate_discovery.py")
TEMPLATE = os.path.normpath(validate_config.DEFAULT_TEMPLATE)
SAMPLE = os.path.join(ROOT, "skills", "sdd-init", "examples", "sample-discovery-output.md")
TEMPLATES = os.path.join(ROOT, "skills", "sdd-init", "templates")
PRODUCT_TEMPLATE = os.path.join(TEMPLATES, "product-template.md")
FRAGMENTS = (
    "use-case-template.md", "prd-user-stories-template.md", "tech-stack-evaluation-matrix.md",
    "adr-template.md", "dev-environment-checklist.md",
)
USER_SOURCE = "user, 2026-01-15"
PLAIN_SCALAR = re.compile(r"^[\w./-]+$")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def run(script, *args, cwd=None):
    return subprocess.run(
        [sys.executable, script, *args],
        capture_output=True, text=True, encoding="utf-8", cwd=cwd,
    )


def sample_value(spec, name="item"):
    def field_values(fields):
        return {field: sample_value(field_spec) for field, field_spec in fields.items()}

    if spec["kind"] == validate_config.SCALAR:
        return name
    if spec["kind"] == validate_config.LIST:
        return [field_values(spec["fields"])] if spec["fields"] else [name]
    return {"name": field_values(spec["fields"]) if spec["fields"] else name}


def scalar_yaml(value):
    # Plain scalars stay unquoted on purpose: dates and versions such as 1.10
    # must survive as written.
    return value if PLAIN_SCALAR.match(value) else json.dumps(value)


def to_yaml(tree, indent=0):
    lines = []
    for name, node in tree.items():
        pad = "  " * indent
        if isinstance(node, Leaf):
            value = node.value
            text = scalar_yaml(value) if isinstance(value, str) else json.dumps(value)
            lines.append(f"{pad}{name}: {text}")
        else:
            lines.append(f"{pad}{name}:")
            lines.extend(to_yaml(node, indent + 1))
    return lines


class Leaf:
    def __init__(self, value):
        self.value = value


class Project:
    def __init__(self, test_case):
        self.dir = tempfile.mkdtemp(prefix="sdd-test-")
        test_case.addCleanup(shutil.rmtree, self.dir, True)
        self.product_path = os.path.join(self.dir, "docs", "PRODUCT.md")
        self.config_path = os.path.join(self.dir, "config.yaml")
        self.product = read(SAMPLE).replace("\r\n", "\n")
        _, self.required = validate_config.load_template(TEMPLATE)
        self.values = {
            key: sample_value(spec, "x-" + key.replace(".", "-"))
            for key, spec in self.required.items()
        }
        self.values["governance.ratified"] = "2026-01-15"
        self.values["governance.version"] = "1.10"
        self.sources = {key: USER_SOURCE for key in self.required}
        self.recorded = {}

    def set(self, key, value, source=USER_SOURCE):
        self.values[key] = value
        self.sources[key] = source

    def write(self):
        tree = {}
        for key, value in self.values.items():
            node = tree
            parts = key.split(".")
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = Leaf(value)
        write(self.config_path, "\n".join(to_yaml(tree)) + "\n")

        rows = []
        for key in sorted(self.values):
            value = self.values[key]
            text = value if isinstance(value, str) else validate_config.collection_text(value)
            text = self.recorded.get(key, text).replace("|", "\\|")
            rows.append(f"| `{key}` | {text} | {self.sources[key]} |")
        write(
            self.product_path,
            self.product.rstrip("\n")
            + f"\n\n## {validate_config.DECISIONS_HEADING}\n\n"
            "| Key | Value | Source |\n| :--- | :--- | :--- |\n" + "\n".join(rows) + "\n",
        )

    def run(self, *mode):
        self.write()
        return self.invoke(*mode)

    def invoke(self, *mode):
        """Run validate_config.py on the files as they are on disk."""
        return run(
            CONFIG_SCRIPT,
            "--template", TEMPLATE,
            "--config", self.config_path,
            "--product", self.product_path,
            *mode,
            cwd=self.dir,
        )
