#!/usr/bin/env python3
"""
Configuration Consistency Validator

Checks that values in the root config.yaml (or constitution.yaml.example)
that describe the same fact do not drift apart.

Currently checked:
    - runtime.version must admit the Python version of devcontainer.image
      when the image is a devcontainers Python image.

Usage:
    uv run --with pyyaml python .specify/scripts/validate_config.py [config.yaml]
"""

import re
import sys

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Run with `uv run --with pyyaml python ...`.")
    sys.exit(1)

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


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except OSError as error:
        print(f"Error: cannot read '{path}': {error}")
        sys.exit(1)

    issues = check_python_runtime(config)
    for issue in issues:
        print(f"[FAIL] {issue}")
    if issues:
        sys.exit(1)
    print(f"[PASS] {path}: runtime and devcontainer values are consistent.")


if __name__ == "__main__":
    main()
