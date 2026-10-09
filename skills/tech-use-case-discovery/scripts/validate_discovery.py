#!/usr/bin/env python3
"""
Software Discovery Package Validator

This script inspects a discovery specification Markdown file or directory
to verify compliance with the Tech Use Case Discovery framework.
Checks for mandatory sections, requirement IDs (FR-001 is reserved for
initialization), unique FR/UC/US/ADR IDs, EARS syntax, ADR completeness, and
MoSCoW prioritization. validate() returns the results; validate_config.py
uses it in-process as the discovery gate.

Usage:
    python validate_discovery.py [--draft] <path_to_markdown_file_or_directory>
    python validate_discovery.py --hash <path_to_PRODUCT.md>

Without --draft the document must also be approved: an "Approval" section
with "Approved by:", "Approved on: YYYY-MM-DD", and
"Approved content: sha256:<hash>", and no "UNRESOLVED:" markers. The hash
binds the approval to the content the user saw: it covers the whole document
except the Approval and "## Configuration Decisions" sections, so any later edit
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
# Appended by validate_config.py scaffold (WI-002), after approval. Only this
# exact H2 is the decisions table; any other spelling is ordinary content.
DECISIONS_HEADING = "Configuration Decisions"
TRADE_OFF_PATTERN = re.compile(r"trade[- ]?offs?", re.IGNORECASE)
# FR-001 is the SDD initialization requirement; product requirements start at FR-002.
RESERVED_FR = "FR-001"
# An ID followed by "-" is a sub-item (e.g. UC-01-EX1), not a definition.
HEADING_ID_PATTERN = re.compile(r"\b(?:UC|US|ADR)-\d+\b(?!-)", re.IGNORECASE)


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


def is_decisions_section(content: str, heading: str, start: int) -> bool:
    return heading == DECISIONS_HEADING and content.startswith("## ", start)


def strip_unapproved(content: str) -> str:
    """The approved content: content without the Approval and Configuration Decisions sections.

    Shared with validate_config.py, so neither section can be approved content
    or cited as evidence for a configuration value.
    """
    content = content.replace("\r\n", "\n")
    excluded = [
        (start, end)
        for heading, _, start, end in get_sections(content)
        if APPROVAL_HEADING.match(heading) or is_decisions_section(content, heading, start)
    ]
    kept, position = [], 0
    for start, end in sorted(excluded):
        if start >= position:
            kept.append(content[position:start])
            position = end
    kept.append(content[position:])
    return "".join(kept)


def content_hash(content: str) -> str:
    """sha256 of the approved content: everything but Approval and Configuration Decisions."""
    normalized = "\n".join(line.rstrip() for line in strip_unapproved(content).split("\n")).strip()
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def use_utf8_output():
    """Print '§' and other non-ASCII text as UTF-8, also when output is piped on Windows."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


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


# Each check returns [(status, message)]; validate() runs them all and
# print_report() is the only place that prints.
PASS, WARN, FAIL, SKIP = "PASS", "WARN", "FAIL", "SKIP"


def check_sections(sections):
    results = []
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
            results.append((PASS, section_name))
        else:
            results.append((FAIL, f"Missing required section: {section_name}"))
    return results


def requirement_rows(content: str):
    """[(FR id, line)] for every functional requirement table row or bullet."""
    rows = []
    for line in content.splitlines():
        match = re.match(r"^\s*\|\s*`?(FR-\d+)`?\s*\|", line, re.IGNORECASE) or re.match(
            r"^\s*[-*]\s*`?(FR-\d+)`?\s*[:|-]", line, re.IGNORECASE
        )
        if match:
            rows.append((match.group(1).upper(), line))
    return rows


def check_requirements(content: str):
    results = []
    fr_ids = sorted({fr_id.upper() for fr_id in re.findall(r"FR-\d+", content, re.IGNORECASE)})
    if fr_ids:
        results.append((PASS, f"Found {len(fr_ids)} Functional Requirement ID(s) ({', '.join(fr_ids[:5])}...)"))
    else:
        results.append((WARN, "No FR-xxx requirement IDs found."))

    rows = requirement_rows(content)
    if any(fr_id == RESERVED_FR for fr_id, _ in rows):
        results.append((
            FAIL,
            f"{RESERVED_FR} is reserved for initialization; number product requirements from FR-002",
        ))
    invalid = [line for _, line in rows if not any(pattern.search(line) for pattern in EARS_PATTERNS)]
    if rows and not invalid:
        results.append((PASS, f"EARS syntax validated for {len(rows)} requirement line(s)"))
    elif invalid:
        results.append((FAIL, "One or more functional requirements do not use a valid EARS form."))
    else:
        results.append((FAIL, "No functional requirement lines found to validate."))
    return results


def heading_id(heading: str):
    match = HEADING_ID_PATTERN.search(heading)
    return match.group(0).upper() if match else None


def check_unique_ids(content: str, sections):
    """FR rows and UC/US/ADR headings each define an ID once.

    A heading repeating the ID of a heading that encloses it (e.g. the flows
    of a use case) is part of that definition, not a second one.
    """
    definitions = [fr_id for fr_id, _ in requirement_rows(content)]
    for heading, _, start, _ in sections:
        own = heading_id(heading)
        if own and not any(
            outer_start < start < outer_end and heading_id(outer) == own
            for outer, _, outer_start, outer_end in sections
        ):
            definitions.append(own)
    duplicates = sorted({item for item in definitions if definitions.count(item) > 1})
    if duplicates:
        return [(FAIL, f"Duplicate ID definition(s): {', '.join(duplicates)}")]
    return [(PASS, f"{len(definitions)} FR, UC, US, and ADR ID(s) are each defined once")]


def check_adrs(sections):
    adr_sections = [
        section_content
        for heading, section_content, _, _ in sections
        if re.search(r"\bADR-\d+\b", heading, re.IGNORECASE)
    ]
    if not adr_sections:
        return [(FAIL, "No ADR-xxx records detected.")]
    adr_ids = sorted({
        adr_id.upper()
        for heading, *_ in sections
        for adr_id in re.findall(r"ADR-\d+", heading, re.IGNORECASE)
    })
    results = [(PASS, f"Found {len(adr_ids)} ADR ID(s): {', '.join(adr_ids)}")]
    incomplete_adrs = [
        section_content
        for section_content in adr_sections
        if "context" not in section_content.lower()
        or "decision" not in section_content.lower()
        or "consequences" not in section_content.lower()
        or not TRADE_OFF_PATTERN.search(section_content)
    ]
    if incomplete_adrs:
        results.append((FAIL, "One or more ADRs are missing Context, Decision, or Consequences/Trade-offs."))
    else:
        results.append((PASS, "ADR structural elements complete (Context, Decision, Consequences/Trade-offs)."))
    return results


def check_moscow(sections):
    # Priorities count only inside requirement and user-story sections, with
    # typographic apostrophes normalized ("Won’t Have" == "Won't Have").
    prioritized_content = "\n".join(
        section_content
        for heading, section_content, _, _ in sections
        if re.match(r"^#{1,6}\s+.*(?:functional requirement|user stor)", f"# {heading}", re.IGNORECASE)
    ).lower().replace("’", "'")
    missing = [kw for kw in MOSCOW_KEYWORDS if kw not in prioritized_content]
    if missing:
        return [(FAIL, f"Missing MoSCoW priorities: {', '.join(missing)}")]
    return [(PASS, f"All MoSCoW priorities identified: {', '.join(MOSCOW_KEYWORDS)}")]


def check_user_approval(content: str, sections, draft: bool):
    if draft:
        return [(SKIP, "Draft mode: approval not required yet.")]
    issues = check_approval(content, sections)
    if issues:
        return [(FAIL, issue) for issue in issues]
    return [(PASS, "Approved by the user with no unresolved decisions.")]


def validate(content: str, draft: bool = False):
    """Run every check and return [(title, [(status, message)])]."""
    sections = get_sections(content)
    return [
        ("Mandatory Section Coverage", check_sections(sections)),
        ("Requirements & EARS Syntax Check", check_requirements(content)),
        ("Unique Identifiers", check_unique_ids(content, sections)),
        ("Architecture Decision Records (ADR) Check", check_adrs(sections)),
        ("MoSCoW MVP Scoping Check", check_moscow(sections)),
        ("User Approval Check", check_user_approval(content, sections, draft)),
    ]


def failures(report):
    return [message for _, results in report for status, message in results if status == FAIL]


def print_report(report, filename: str) -> bool:
    print("\n==========================================")
    print(f" Validating Discovery Spec: {filename}")
    print("==========================================")
    for number, (title, results) in enumerate(report, 1):
        print(f"\n--- {number}. {title} ---")
        for status, message in results:
            print(f"  [{status}] {message}")

    statuses = [status for _, results in report for status, _ in results]
    print("\n==========================================")
    print(" Validation Summary")
    print("==========================================")
    print(f"  Passes:   {statuses.count(PASS)}")
    print(f"  Warnings: {statuses.count(WARN)}")
    print(f"  Errors:   {statuses.count(FAIL)}")

    if FAIL in statuses:
        print("\n  STATUS: FAILED - Fix the errors above.")
        return False
    if WARN in statuses:
        print("\n  STATUS: PASSED WITH WARNINGS")
        return True
    print("\n  STATUS: PASSED")
    return True


def analyze_content(content: str, filename: str, draft: bool = False) -> bool:
    return print_report(validate(content, draft), filename)


def main():
    use_utf8_output()
    flags =[arg for arg in sys.argv[1:] if arg in ("--draft", "--hash")]
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
