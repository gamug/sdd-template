#!/usr/bin/env python3
"""
Software Discovery Package Validator

This script inspects a discovery specification Markdown file or directory
to verify compliance with the Tech Use Case Discovery framework.
Checks for mandatory sections, requirement IDs, EARS syntax, ADR completeness,
and MoSCoW prioritization.

Usage:
    python validate_discovery.py <path_to_markdown_file_or_directory>
"""

import sys
import os
import re

REQUIRED_SECTIONS = [
    ("Use Cases", [r"use case", r"uc-\d+"]),
    ("Functional Requirements", [r"functional requirement", r"fr-\d+"]),
    ("User Stories", [r"user stor", r"us-\d+"]),
    ("Tech Stack Selection", [r"tech stack", r"technology stack", r"mcdm"]),
    ("Architecture Decision Records", [r"architecture decision", r"adr-\d+"]),
    ("Dev Environment Setup", [r"dev environment", r"development environment", r"docker"]),
    ("Risk Assessment & Roadmap", [r"risk", r"roadmap", r"mvp"])
]

EARS_KEYWORDS = ["shall", "when", "while", "where", "if"]
MOSCOW_KEYWORDS = ["must have", "should have", "could have", "won't have"]


def analyze_content(content: str, filename: str):
    print(f"\n==========================================")
    print(f" Validating Discovery Spec: {filename}")
    print(f"==========================================\n")
    
    issues = []
    warnings = []
    passes = []

    content_lower = content.lower()

    # 1. Check Mandatory Sections
    print("--- 1. Mandatory Section Coverage ---")
    for section_name, patterns in REQUIRED_SECTIONS:
        found = any(re.search(pat, content_lower) for pat in patterns)
        if found:
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

    ears_found = [kw for kw in EARS_KEYWORDS if kw in content_lower]
    if len(ears_found) >= 3:
        print(f"  [PASS] EARS syntax keywords detected: {', '.join(ears_found)}")
        passes.append("EARS syntax detected")
    else:
        print(f"  [WARN] Weak EARS notation usage. Keywords found: {', '.join(ears_found)}")
        warnings.append("Weak EARS notation usage")

    # 3. Check ADR Completeness
    print("\n--- 3. Architecture Decision Records (ADR) Check ---")
    adr_matches = re.findall(r"ADR-\d+", content, re.IGNORECASE)
    if adr_matches:
        print(f"  [PASS] Found {len(set(adr_matches))} unique ADR ID(s): {', '.join(sorted(set(adr_matches)))}")
        has_context = "context" in content_lower
        has_decision = "decision" in content_lower
        has_consequences = "consequences" in content_lower or "trade-off" in content_lower or "pros" in content_lower
        
        if has_context and has_decision and has_consequences:
            print("  [PASS] ADR structural elements complete (Context, Decision, Consequences/Trade-offs).")
            passes.append("ADR structural elements complete")
        else:
            print("  [WARN] Incomplete ADR structure. Ensure Context, Decision, and Consequences are documented.")
            warnings.append("Incomplete ADR structure")
    else:
        print("  [WARN] No ADR-xxx records detected.")
        warnings.append("No ADR-xxx records detected.")

    # 4. Check MoSCoW Prioritization
    print("\n--- 4. MoSCoW MVP Scoping Check ---")
    moscow_found = [kw for kw in MOSCOW_KEYWORDS if kw in content_lower]
    if moscow_found:
        print(f"  [PASS] MoSCoW priorities identified: {', '.join(moscow_found)}")
        passes.append("MoSCoW priorities present")
    else:
        print("  [WARN] MoSCoW priorities missing (Must Have, Should Have, Could Have, Won't Have).")
        warnings.append("MoSCoW priorities missing")

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
    if len(sys.argv) < 2:
        print("Usage: python validate_discovery.py <path_to_markdown_file_or_directory>")
        sys.exit(1)

    target_path = sys.argv[1]

    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' does not exist.")
        sys.exit(1)

    all_success = True

    if os.path.isfile(target_path):
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
        success = analyze_content(content, os.path.basename(target_path))
        if not success:
            all_success = False
    else:
        md_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(target_path) for f in filenames if f.endswith(".md")]
        if not md_files:
            print(f"No Markdown files found in directory '{target_path}'.")
            sys.exit(1)
            
        combined_content = ""
        for file_path in md_files:
            with open(file_path, "r", encoding="utf-8") as f:
                combined_content += f"\n\n--- FILE: {file_path} ---\n\n" + f.read()
                
        success = analyze_content(combined_content, f"Directory: {target_path}")
        if not success:
            all_success = False

    if not all_success:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
