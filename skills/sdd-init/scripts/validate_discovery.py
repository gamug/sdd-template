#!/usr/bin/env python3
"""
Software Discovery Package Validator

This script inspects a discovery specification Markdown file or directory
to verify compliance with the SDD discovery framework.
Checks for mandatory sections, requirement IDs (FR-001 is reserved for
initialization), three-digit FR/UC/US/ADR/RSK IDs defined once, EARS syntax,
ADR completeness, the risk matrix (Score = Impact x Probability, and a
mitigation plan for scores of 6 or more), and MoSCoW prioritization.
validate() returns the results; validate_config.py uses it in-process as the
discovery gate.

Usage:
    python validate_discovery.py [--draft] <path_to_markdown_file_or_directory>
    python validate_discovery.py --hash <path_to_PRODUCT.md>

Without --draft the document must also be approved: an "Approval" section
with "Approved by:", "First approved on: YYYY-MM-DD" (set on the first
approval and kept on every re-approval), "Approved on: YYYY-MM-DD", and
"Approved content: sha256:<hash>", and no "UNRESOLVED:" markers. The hash
binds the approval to the content the user saw: it covers the whole document
except the Approval and "## Configuration Decisions" sections, so any later edit
fails validation until the user approves again. --hash prints the value to
record. Use --draft while PRODUCT.md is still being written (TASK-003).

Lines starting with ">" are template guidance: every content check skips
them, but the hash covers them.

Directory mode requires exactly one file named PRODUCT.md somewhere below the
provided directory and validates that file only.
"""

import datetime
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
    ("Risk Assessment & Roadmap", r"^#{1,6}\s+.*(?:risk|roadmap)", r"\bRSK-\d+\b"),
    ("Governance & Workflow", r"^#{1,6}\s+.*governance", None),
]

EARS_PATTERNS = [
    re.compile(r"\b(?:the|a|an)\s+[a-z][\w -]*?\s+shall\b", re.IGNORECASE),
    re.compile(r"\b(?:when|while|where|if)\b.*\bshall\b", re.IGNORECASE),
]
UNRESOLVED_MARKER = "UNRESOLVED:"
APPROVAL_HEADING = re.compile(r"^(?:\d+\.\s*)?approval\s*$", re.IGNORECASE)
# Appended by validate_config.py scaffold (WI-002), after approval. Only this
# exact H2 is the decisions table; any other spelling is ordinary content.
DECISIONS_HEADING = "Configuration Decisions"
TRADE_OFF_PATTERN = re.compile(r"trade[- ]?offs?", re.IGNORECASE)
# FR-001 is the SDD initialization requirement; product requirements start at FR-002.
RESERVED_FR = "FR-001"
# An ID followed by "-" is a sub-item (e.g. UC-001-EX1), not a definition.
HEADING_ID_PATTERN = re.compile(r"\b(?:UC|US|ADR)-\d+\b(?!-)", re.IGNORECASE)
# Every ID uses three digits: FR-002, UC-001, US-001, ADR-001, RSK-001.
ID_PATTERN = re.compile(r"\b(?:FR|UC|US|ADR|RSK)-(\d+)\b", re.IGNORECASE)
RISK_COLUMNS = "| Risk ID | Description | Impact | Probability | Score | Mitigation Plan |"
MITIGATION_THRESHOLD = 6
# "> " blockquote lines are template guidance, not document content.
GUIDANCE_LINE = re.compile(r"^\s*>")
# "[...]" left from a template. Not placeholders: Markdown links "[text](url)"
# / "[text][ref]", task boxes "[ ]" / "[x]", numeric citations "[1]" /
# "[1, 2]" / "[1-3]", and footnotes "[^1]" / "[^note]: text".
PLACEHOLDER_PATTERN = re.compile(
    r"\[(?![ xX]\]|\^|\d+(?:\s*[,\u2013-]\s*\d+)*\])[^\]\n]+\](?![(\[])"
)
FR_SECTION = re.compile(r"^#{1,6}\s+.*functional requirement", re.IGNORECASE)
RISK_SECTION = re.compile(r"^#{1,6}\s+.*risk", re.IGNORECASE)
TABLE_SEPARATOR = re.compile(r"^\s*\|[\s:|-]+\|?\s*$")
EARS_FORMS = ("ubiquitous", "event-driven", "state-driven", "optional", "unwanted")
MOSCOW_VALUES = ("must have", "should have", "could have", "won't have")


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


def strip_guidance(content: str) -> str:
    """Blank every ">" guidance line, keeping line positions."""
    content = content.replace("\r\n", "\n")
    return "\n".join("" if GUIDANCE_LINE.match(line) else line for line in content.split("\n"))


def section_content(content: str, heading_pattern) -> str:
    """The text of every section whose heading matches, each line once."""
    ranges = sorted(
        (start, end) for heading, _, start, end in get_sections(content)
        if heading_pattern.match(f"# {heading}")
    )
    parts, position = [], 0
    for start, end in ranges:
        start = max(start, position)
        if start < end:
            parts.append(content[start:end])
            position = end
    return "\n".join(parts)


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


def approval_field(label: str, value: str, text: str):
    """Match "<label>: <value>" with the value on the label's own line.

    The label must start a phrase, so "approved on" does not match inside
    "First approved on".
    """
    return re.search(rf"(?<!\w)(?<!\w\s){label}[^\w\n]*{value}", text, re.IGNORECASE)


def field_date(match):
    try:
        return datetime.date.fromisoformat(match.group(1)) if match else None
    except ValueError:
        return None


def approval_date(content: str, label: str = "approved on"):
    """A date field of the Approval section, or None when absent or invalid."""
    content = content.replace("\r\n", "\n")
    for heading, text, _, _ in get_sections(content):
        if APPROVAL_HEADING.match(heading):
            return field_date(approval_field(label, r"(\d{4}-\d{2}-\d{2})\b", text))
    return None


def first_approval_date(content: str):
    """The "First approved on" date: kept on re-approval, so amendments do not
    invalidate configuration decisions made after the first approval."""
    return approval_date(content, "first approved on")


def check_approval(content: str, sections):
    issues = []
    unresolved = [
        line.strip()
        for line in content.splitlines()
        if UNRESOLVED_MARKER in line and not GUIDANCE_LINE.match(line)
    ]
    if unresolved:
        issues.append(f"{len(unresolved)} unresolved decision(s) remain ({UNRESOLVED_MARKER})")
    approval = [
        section_content
        for heading, section_content, _, _ in sections
        if APPROVAL_HEADING.match(heading)
    ]
    approved_by = approval and approval_field("approved by", r"(\w.*)", approval[0])
    first_on = approval and approval_field("first approved on", r"(\d{4}-\d{2}-\d{2})\b", approval[0])
    approved_on = approval and approval_field("approved on", r"(\d{4}-\d{2}-\d{2})\b", approval[0])
    approved_content = approval and approval_field(
        "approved content", r"(sha256:[0-9a-f]{64})\b", approval[0]
    )
    if not (approved_by and first_on and approved_on and approved_content):
        issues.append(
            "Missing Approval section with 'Approved by:', 'First approved on: YYYY-MM-DD', "
            "'Approved on: YYYY-MM-DD', and 'Approved content: sha256:<hash>' (print it with --hash)"
        )
        return issues
    # The label's separator can swallow "[", so search the whole field.
    if PLACEHOLDER_PATTERN.search(approved_by.group(0)):
        issues.append("'Approved by' is still a template placeholder; record who approved")
    if not (field_date(first_on) and field_date(approved_on)):
        issues.append("'First approved on' and 'Approved on' must be real dates (YYYY-MM-DD)")
    elif field_date(first_on) > field_date(approved_on):
        issues.append(
            f"'First approved on' ({first_on.group(1)}) is after 'Approved on' ({approved_on.group(1)})"
        )
    if approved_content.group(1).lower() != content_hash(content):
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
    """[(FR id, line)] for every table row or bullet that defines a functional
    requirement: only inside the Functional Requirements section. FR rows
    elsewhere (e.g. a traceability matrix) are references."""
    rows = []
    for line in section_content(content, FR_SECTION).splitlines():
        match = re.match(r"^\s*\|\s*`?(FR-\d+)`?\s*\|", line, re.IGNORECASE) or re.match(
            r"^\s*[-*]\s*`?(FR-\d+)`?\s*[:|-]", line, re.IGNORECASE
        )
        if match:
            rows.append((match.group(1).upper(), line))
    return rows


def table_cells(line: str):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def risk_rows(content: str):
    """[(RSK id, line)] for every risk table row in the Risk section."""
    rows = []
    for line in section_content(content, RISK_SECTION).splitlines():
        match = re.match(r"^\s*\|\s*`?(RSK-\d+)`?\s*\|", line, re.IGNORECASE)
        if match:
            rows.append((match.group(1).upper(), line))
    return rows


def check_risks(content: str):
    """Risk rows use RISK_COLUMNS; Score = Impact x Probability (1-3 each), and
    a score of MITIGATION_THRESHOLD or more needs a mitigation plan."""
    rows = risk_rows(content)
    if not rows:
        return [(FAIL, f"No RSK-xxx risk rows found (columns: {RISK_COLUMNS})")]
    issues = []
    for risk_id, line in rows:
        cells = table_cells(line)
        if len(cells) != 6:
            issues.append(f"{risk_id}: expected the columns {RISK_COLUMNS}")
            continue
        numbers = [re.search(r"\d+", cell) for cell in cells[2:5]]
        if not all(numbers):
            issues.append(f"{risk_id}: Impact, Probability, and Score must contain numbers")
            continue
        impact, probability, score = (int(number.group(0)) for number in numbers)
        if not (1 <= impact <= 3 and 1 <= probability <= 3):
            issues.append(f"{risk_id}: Impact and Probability use the 1-3 scale")
        elif score != impact * probability:
            issues.append(f"{risk_id}: Score {score} is not Impact x Probability ({impact * probability})")
        if score >= MITIGATION_THRESHOLD and not cells[5].strip("*_` -"):
            issues.append(f"{risk_id}: score {score} needs a mitigation plan")
    if issues:
        return [(FAIL, issue) for issue in issues]
    return [(PASS, f"{len(rows)} risk(s) scored as Impact x Probability, with mitigation where required")]


def ears_form(statement: str) -> str:
    """The EARS form a requirement statement is written in."""
    text = statement.strip(" *_`").lower()
    if re.match(r"when\b", text):
        return "event-driven"
    if re.match(r"while\b", text):
        return "state-driven"
    if re.match(r"where\b", text):
        return "optional"
    if re.match(r"if\b", text) and re.search(r"\bthen\b", text):
        return "unwanted"
    return "ubiquitous"


def ears_column_issues(content: str):
    """FR table rows whose EARS pattern column disagrees with their statement."""
    issues, header = [], None
    lines = section_content(content, FR_SECTION).splitlines()
    for index, line in enumerate(lines):
        if line.strip().startswith("|") and index + 1 < len(lines) and TABLE_SEPARATOR.match(lines[index + 1]):
            header = [name.lower() for name in table_cells(line)]
            continue
        match = re.match(r"^\s*\|\s*`?(FR-\d+)`?\s*\|", line, re.IGNORECASE)
        if not match or not header:
            continue
        pattern_column = next((k for k, name in enumerate(header) if "pattern" in name or "rule" in name), None)
        statement_column = next((k for k, name in enumerate(header) if "statement" in name), None)
        cells = table_cells(line)
        if pattern_column is None or pattern_column >= len(cells):
            continue
        declared_text = cells[pattern_column].strip("*_` ")
        declared = re.split(r"[\s/]+", declared_text.lower())[0]
        statement = cells[statement_column] if statement_column is not None and statement_column < len(cells) else line
        fr_id = match.group(1).upper()
        if declared not in EARS_FORMS:
            issues.append(f"{fr_id}: unknown EARS pattern {declared_text!r} (use {', '.join(EARS_FORMS)})")
        elif declared != ears_form(statement):
            issues.append(f"{fr_id}: declared {declared_text}, but the statement is {ears_form(statement)}")
    return issues


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
    mismatched = ears_column_issues(content)
    if rows and not invalid and not mismatched:
        results.append((PASS, f"EARS syntax validated for {len(rows)} requirement line(s)"))
    elif invalid:
        results.append((FAIL, "One or more functional requirements do not use a valid EARS form."))
    elif not rows:
        results.append((FAIL, "No functional requirement lines found to validate."))
    results.extend((FAIL, issue) for issue in mismatched)
    return results


def heading_id(heading: str):
    match = HEADING_ID_PATTERN.search(heading)
    return match.group(0).upper() if match else None


def check_unique_ids(content: str, sections):
    """IDs use three digits, and FR/RSK rows and UC/US/ADR headings each define an ID once.

    A heading repeating the ID of a heading that encloses it (e.g. the flows
    of a use case) is part of that definition, not a second one.
    """
    malformed = sorted({
        match.group(0).upper() for match in ID_PATTERN.finditer(content) if len(match.group(1)) != 3
    })
    if malformed:
        return [(FAIL, f"IDs use three digits (e.g. UC-001): {', '.join(malformed)}")]
    definitions = [row_id for row_id, _ in requirement_rows(content) + risk_rows(content)]
    for heading, _, start, _ in sections:
        own = heading_id(heading)
        if own and not any(
            outer_start < start < outer_end and heading_id(outer) == own
            for outer, _, outer_start, outer_end in sections
        ):
            definitions.append(own)
    results = []
    duplicates = sorted({item for item in definitions if definitions.count(item) > 1})
    if duplicates:
        results.append((FAIL, f"Duplicate ID definition(s): {', '.join(duplicates)}"))
    # Every mention must resolve; a sub-item such as UC-001-EX1 resolves through UC-001.
    referenced = {match.group(0).upper() for match in ID_PATTERN.finditer(content)}
    undefined = sorted(referenced - set(definitions) - {RESERVED_FR})
    if undefined:
        results.append((FAIL, f"Reference(s) to undefined ID(s): {', '.join(undefined)}"))
    return results or [
        (PASS, f"{len(definitions)} FR, UC, US, ADR, and RSK ID(s) are each defined once and every reference resolves")
    ]


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


def normalize_priority(text: str) -> str:
    # Typographic apostrophes count: "Won’t Have" == "Won't Have".
    return re.sub(r"\s+", " ", text.strip(" *_`").lower().replace("’", "'"))


def check_moscow(content: str, sections):
    """Every FR and user story has exactly one valid priority, at least one is
    Must Have, and Won't Have is stated (as a priority or a "Won't Have:" line)."""
    issues, priorities = [], []
    for fr_id, line in requirement_rows(content):
        if line.strip().startswith("|"):
            found = {normalize_priority(cell) for cell in table_cells(line)} & set(MOSCOW_VALUES)
        else:
            found = {value for value in MOSCOW_VALUES if value in normalize_priority(line)}
        if len(found) != 1:
            issues.append(f"{fr_id}: needs exactly one MoSCoW priority")
        priorities.extend(found)
    for heading, text, start, _ in sections:
        story = heading_id(heading)
        if not story or not story.startswith("US-") or any(
            outer_start < start < outer_end and heading_id(outer) == story
            for outer, _, outer_start, outer_end in sections
        ):
            continue
        match = re.search(r"^\s*[-*]?\s*\**priority\**[^\w\n]*(.+)$", text, re.IGNORECASE | re.MULTILINE)
        value = normalize_priority(match.group(1)) if match else ""
        if value not in MOSCOW_VALUES:
            issues.append(f"{story}: Priority must be one of Must Have, Should Have, Could Have, Won't Have")
        else:
            priorities.append(value)
    if "must have" not in priorities:
        issues.append("No requirement or user story is Must Have")
    prioritized_content = "\n".join(
        section_content
        for heading, section_content, _, _ in sections
        if re.match(r"^#{1,6}\s+.*(?:functional requirement|user stor)", f"# {heading}", re.IGNORECASE)
    )
    wont_line = re.search(r"won't have[*_ ]*:[*_ ]*\S", normalize_priority(prioritized_content))
    if "won't have" not in priorities and not wont_line:
        issues.append("Won't Have is not stated: give an FR or story that priority, or add a 'Won't Have:' line")
    if issues:
        return [(FAIL, issue) for issue in issues]
    return [(PASS, f"{len(priorities)} prioritized item(s), with Must Have and Won't Have stated")]


def check_placeholders(content: str, draft: bool):
    """Template "[...]" placeholders left in the approved content, outside code
    and guidance notes. The Configuration Decisions table (compact JSON lists)
    and the Approval section (checked on its own) are not template content."""
    found, fenced = [], False
    for line in strip_unapproved(content).splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced or GUIDANCE_LINE.match(line):
            continue
        found.extend(PLACEHOLDER_PATTERN.findall(re.sub(r"`[^`]*`", "", line)))
    if not found:
        return [(PASS, "No template placeholders left")]
    message = f"{len(found)} template placeholder(s) left, e.g. {', '.join(found[:3])}"
    return [(WARN if draft else FAIL, message)]


def check_user_approval(content: str, sections, draft: bool):
    if draft:
        return [(SKIP, "Draft mode: approval not required yet.")]
    issues = check_approval(content, sections)
    if issues:
        return [(FAIL, issue) for issue in issues]
    return [(PASS, "Approved by the user with no unresolved decisions.")]


def validate(content: str, draft: bool = False):
    """Run every check and return [(title, [(status, message)])].

    Content checks see the document without ">" guidance notes; the approval
    hash still covers the whole document.
    """
    body = strip_guidance(content)
    sections = get_sections(body)
    return [
        ("Mandatory Section Coverage", check_sections(sections)),
        ("Requirements & EARS Syntax Check", check_requirements(body)),
        ("Unique Identifiers", check_unique_ids(body, sections)),
        ("Risk Matrix Check", check_risks(body)),
        ("Architecture Decision Records (ADR) Check", check_adrs(sections)),
        ("MoSCoW MVP Scoping Check", check_moscow(body, sections)),
        ("Template Placeholders", check_placeholders(body, draft)),
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
