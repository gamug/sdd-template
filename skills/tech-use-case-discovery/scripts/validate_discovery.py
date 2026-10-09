#!/usr/bin/env python3
"""
Software Discovery Package Validator

This script inspects a discovery specification Markdown file or directory
to verify compliance with the Tech Use Case Discovery framework.
Checks for mandatory sections, requirement IDs, EARS syntax, ADR completeness,
and MoSCoW prioritization.

Usage:
    python validate_discovery.py [--draft] <path_to_markdown_file_or_directory>
    python validate_discovery.py --hash <path_to_PRODUCT.md>

Without --draft the document must also be approved: an "Approval" section
with "Approved by:", "Approved on: YYYY-MM-DD", and
"Approved content: sha256:<hash>", and no "UNRESOLVED:" markers. The hash
binds the approval to the content the user saw: it covers the whole document
except the Approval and "Configuration Decisions" sections, so any later edit
fails validation until the user approves again. --hash prints the value to
record. Use --draft while PRODUCT.md is still being written (TASK-003).

Directory mode requires exactly one file named PRODUCT.md somewhere below the
provided directory and validates that file only.
"""

import hashlib
import sys
import os
import re

REQUIRED_SECTIONS = [
    ("Use Cases", r"^#{1,6}\s+.*use case", r"\bUC-\d+\b"),
    ("Functional Requirements", r"^#{1,6}\s+.*functional requirement", r"\bFR-\d+\b"),
    ("User Stories", r"^#{1,6}\s+.*user stor", r"\bUS-\d+\b"),
    ("Tech Stack Selection", r"^#{1,6}\s+.*(?:tech stack|technology stack|mcdm)", None),
    ("Architecture Decision Records", r"^#{1,6}\s+.*architecture decision", r"\bADR-\d+\b"),
    ("Dev Environment Setup", r"^#{1,6}\s+.*(?:dev environment|development environment)", None),
    ("Risk Assessment & Roadmap", r"^#{1,6}\s+.*(?:risk|roadmap)", r"\b(?:RSK-\d+|MVP)\b"),
    ("Governance & Workflow", r"^#{1,6}\s+.*governance", None),
]

EARS_PATTERNS = [
    re.compile(r"\b(?:the|a|an)\s+[a-z][\w -]*?\s+shall\b", re.IGNORECASE),
    re.compile(r"\b(?:when|while|where|if)\b.*\bshall\b", re.IGNORECASE),
]
MOSCOW_KEYWORDS = ["must have", "should have", "could have", "won't have"]
UNRESOLVED_MARKER = "UNRESOLVED:"
APPROVAL_HEADING = re.compile(r"^(?:\d+\.\s*)?approval\s*$", re.IGNORECASE)
# Appended by validate_config.py scaffold (WI-002), after approval.
DECISIONS_HEADING = re.compile(r"^configuration decisions\s*$", re.IGNORECASE)


def get_sections(content: str):
    headings = list(re.finditer(r"^(#{1,6})\s+(.+?)\s*$", content, re.MULTILINE))
    sections = []
    for index, heading in enumerate(headings):
        level = len(heading.group(1))
        end = len(content)
        for next_heading in headings[index + 1:]:
            if len(next_heading.group(1)) <= level:
                end = next_heading.start()
                break
        sections.append((heading.group(2), content[heading.end():end], heading.start(), end))
    return sections


def most_specific(sections):
    """Drop sections that enclose another section in the same list."""
    return [
        section for section in sections
        if not any(
            other is not section and section[2] < other[2] < section[3]
            for other in sections
        )
    ]


def content_hash(content: str) -> str:
    """sha256 of the approved content: everything but Approval and Configuration Decisions."""
    content = content.replace("\r\n", "\n")
    excluded = [
        (start, end)
        for heading, _, start, end in get_sections(content)
        if APPROVAL_HEADING.match(heading) or DECISIONS_HEADING.match(heading)
    ]
    kept, position = [], 0
    for start, end in sorted(excluded):
        if start >= position:
            kept.append(content[position:start])
            position = end
    kept.append(content[position:])
    normalized = "\n".join(line.rstrip() for line in "".join(kept).split("\n")).strip()
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def check_approval(content: str, sections):
    issues = []
    unresolved = [
        line.strip() for line in content.splitlines() if UNRESOLVED_MARKER in line
    ]
    if unresolved:
        issues.append(f"{len(unresolved)} unresolved decision(s) remain ({UNRESOLVED_MARKER})")
    approval = [
        section_content
        for heading, section_content, _, _ in sections
        if APPROVAL_HEADING.match(heading)
    ]
    approved_by = approval and re.search(
        r"approved by\W*:?\**\s*(\S.*)$", approval[0], re.IGNORECASE | re.MULTILINE
    )
    approved_on = approval and re.search(
        r"approved on\W*:?\**\s*(\d{4}-\d{2}-\d{2})\b", approval[0], re.IGNORECASE
    )
    approved_content = approval and re.search(
        r"approved content\W*:?\**\s*`?(sha256:[0-9a-f]{64})\b", approval[0], re.IGNORECASE
    )
    if not (approved_by and approved_on and approved_content):
        issues.append(
            "Missing Approval section with 'Approved by:', 'Approved on: YYYY-MM-DD', "
            "and 'Approved content: sha256:<hash>' (print it with --hash)"
        )
    elif approved_content.group(1).lower() != content_hash(content):
        issues.append(
            "PRODUCT.md changed after approval (content hash mismatch). Show the changes "
            "to the user, and record a new approval and --hash only after they approve"
        )
    return issues


def analyze_content(content: str, filename: str, draft: bool = False):
    print(f"\n==========================================")
    print(f" Validating Discovery Spec: {filename}")
    print(f"==========================================\n")
    
    issues = []
    warnings = []
    passes = []

    sections = get_sections(content)

    # 1. Check Mandatory Sections
    print("--- 1. Mandatory Section Coverage ---")
    for section_name, heading_pattern, identifier_pattern in REQUIRED_SECTIONS:
        # An enclosing heading (e.g. a document title) must not satisfy the
        # check on behalf of a more specific, empty section beneath it.
        matching_sections = most_specific([
            section
            for section in sections
            if re.match(heading_pattern, f"# {section[0]}", re.IGNORECASE)
        ])
        is_complete = any(
            section_content.strip()
            and (
                identifier_pattern is None
                or re.search(identifier_pattern, f"{heading}\n{section_content}", re.IGNORECASE)
            )
            for heading, section_content, _, _ in matching_sections
        )
        if is_complete:
            print(f"  [PASS] {section_name}")
            passes.append(f"Section present: {section_name}")
        else:
            print(f"  [FAIL] Missing required section: {section_name}")
            issues.append(f"Missing required section: {section_name}")

    # 2. Check Requirement IDs and EARS syntax
    print("\n--- 2. Requirements & EARS Syntax Check ---")
    fr_matches = re.findall(r"FR-\d+", content, re.IGNORECASE)
    if fr_matches:
        print(f"  [PASS] Found {len(set(fr_matches))} unique Functional Requirement ID(s) ({', '.join(sorted(set(fr_matches))[:5])}...)")
        passes.append("Functional Requirement IDs present")
    else:
        print("  [WARN] No FR-xxx requirement IDs found.")
        warnings.append("No FR-xxx requirement IDs found.")

    requirement_lines = []
    for line in content.splitlines():
        table_match = re.match(r"^\s*\|\s*`?(FR-\d+)`?\s*\|", line, re.IGNORECASE)
        bullet_match = re.match(r"^\s*[-*]\s*`?(FR-\d+)`?\s*[:|-]", line, re.IGNORECASE)
        if table_match or bullet_match:
            requirement_lines.append(line)
    invalid_requirement_lines = [
        line for line in requirement_lines
        if not any(pattern.search(line) for pattern in EARS_PATTERNS)
    ]
    if requirement_lines and not invalid_requirement_lines:
        print(f"  [PASS] EARS syntax validated for {len(requirement_lines)} requirement line(s)")
        passes.append("EARS syntax validated")
    elif invalid_requirement_lines:
        print("  [FAIL] One or more functional requirements do not use a valid EARS form.")
        issues.append("Invalid EARS syntax in functional requirements")
    else:
        print("  [FAIL] No functional requirement lines found to validate.")
        issues.append("No functional requirement lines found")

    # 3. Check ADR Completeness
    print("\n--- 3. Architecture Decision Records (ADR) Check ---")
    adr_sections = [
        section_content
        for heading, section_content, _, _ in sections
        if re.search(r"\bADR-\d+\b", heading, re.IGNORECASE)
    ]
    if adr_sections:
        adr_ids = [
            adr_id
            for heading, *_ in sections
            for adr_id in re.findall(r"ADR-\d+", heading, re.IGNORECASE)
        ]
        print(f"  [PASS] Found {len(set(adr_ids))} unique ADR ID(s): {', '.join(sorted(set(adr_ids)))}")
        incomplete_adrs = [
            section_content
            for section_content in adr_sections
            if "context" not in section_content.lower()
            or "decision" not in section_content.lower()
            or "consequences" not in section_content.lower()
            or "trade-off" not in section_content.lower()
        ]
        if not incomplete_adrs:
            print("  [PASS] ADR structural elements complete (Context, Decision, Consequences/Trade-offs).")
            passes.append("ADR structural elements complete")
        else:
            print("  [FAIL] One or more ADRs are missing Context, Decision, or Consequences/Trade-offs.")
            issues.append("Incomplete ADR structure")
    else:
        print("  [FAIL] No ADR-xxx records detected.")
        issues.append("No ADR-xxx records detected")

    # 4. Check MoSCoW Prioritization
    print("\n--- 4. MoSCoW MVP Scoping Check ---")
    # Priorities count only inside requirement and user-story sections, with
    # typographic apostrophes normalized ("Won’t Have" == "Won't Have").
    prioritized_content = "\n".join(
        section_content
        for heading, section_content, _, _ in sections
        if re.match(r"^#{1,6}\s+.*(?:functional requirement|user stor)", f"# {heading}", re.IGNORECASE)
    ).lower().replace("\u2019", "'")
    moscow_found = [kw for kw in MOSCOW_KEYWORDS if kw in prioritized_content]
    missing_moscow = [kw for kw in MOSCOW_KEYWORDS if kw not in moscow_found]
    if not missing_moscow:
        print(f"  [PASS] All MoSCoW priorities identified: {', '.join(moscow_found)}")
        passes.append("Complete MoSCoW priorities present")
    else:
        print(f"  [FAIL] Missing MoSCoW priorities: {', '.join(missing_moscow)}")
        issues.append("Incomplete MoSCoW priorities")

    # 5. Check user approval
    print("\n--- 5. User Approval Check ---")
    if draft:
        print("  [SKIP] Draft mode: approval not required yet.")
    else:
        approval_issues = check_approval(content, sections)
        for issue in approval_issues:
            print(f"  [FAIL] {issue}")
        if approval_issues:
            issues.extend(approval_issues)
        else:
            print("  [PASS] Approved by the user with no unresolved decisions.")
            passes.append("User approval recorded")

    # Summary
    print("\n==========================================")
    print(" Validation Summary")
    print("==========================================")
    print(f"  Passes:   {len(passes)}")
    print(f"  Warnings: {len(warnings)}")
    print(f"  Errors:   {len(issues)}")

    if issues:
        print("\n  STATUS: FAILED - Please address critical errors above.")
        return False
    elif warnings:
        print("\n  STATUS: PASSED WITH WARNINGS - Document is complete but can be improved.")
        return True
    else:
        print("\n  STATUS: PASSED - Excellent discovery specification package!")
        return True


def main():
    flags = [arg for arg in sys.argv[1:] if arg in ("--draft", "--hash")]
    args = [arg for arg in sys.argv[1:] if arg not in flags]
    draft = "--draft" in flags
    if len(args) != 1 or len(flags) > 1:
        print("Usage: python validate_discovery.py [--draft] <path_to_markdown_file_or_directory>")
        print("       python validate_discovery.py --hash <path_to_PRODUCT.md>")
        sys.exit(1)

    target_path = args[0]

    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' does not exist.")
        sys.exit(1)

    if "--hash" in flags:
        if not os.path.isfile(target_path):
            print("Error: --hash needs the PRODUCT.md file.")
            sys.exit(1)
        with open(target_path, "r", encoding="utf-8") as f:
            print(content_hash(f.read()))
        sys.exit(0)

    all_success = True

    if os.path.isfile(target_path):
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
        success = analyze_content(content, os.path.basename(target_path), draft)
        if not success:
            all_success = False
    else:
        product_files = [
            os.path.join(dp, filename)
            for dp, _, filenames in os.walk(target_path)
            for filename in filenames
            if filename.lower() == "product.md"
        ]
        if not product_files:
            print(
                f"No PRODUCT.md found below directory '{target_path}'. "
                "Directory mode validates the generated PRODUCT.md only."
            )
            sys.exit(1)
        if len(product_files) > 1:
            print(
                f"Multiple PRODUCT.md files found below directory '{target_path}': "
                f"{', '.join(product_files)}"
            )
            sys.exit(1)

        product_file = product_files[0]
        with open(product_file, "r", encoding="utf-8") as f:
            content = f.read()

        success = analyze_content(content, product_file, draft)
        if not success:
            all_success = False

    if not all_success:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
