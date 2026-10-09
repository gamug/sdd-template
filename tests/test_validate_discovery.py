"""Regression tests for validate_discovery.py (sections, IDs, EARS, risks, MoSCoW, approval, templates)."""

import os
import shutil
import tempfile
import unittest

from fixtures import DISCOVERY_SCRIPT, FRAGMENTS, PRODUCT_TEMPLATE, SAMPLE, TEMPLATES, read, run, write
import validate_discovery


class DiscoveryTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="sdd-test-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.sample = read(SAMPLE).replace("\r\n", "\n")

    def validate(self, content, *flags):
        path = os.path.join(self.dir, "docs", "PRODUCT.md")
        write(path, content)
        return run(DISCOVERY_SCRIPT, *flags, path)

    def approved(self, product):
        """Re-record the approval hash, as if the user approved this content."""
        return product.replace(
            validate_discovery.content_hash(self.sample), validate_discovery.content_hash(product)
        )

    def assertFails(self, result, message):
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(message, result.stdout)

    def test_sample_passes(self):
        result = run(DISCOVERY_SCRIPT, SAMPLE)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_draft_skips_approval(self):
        draft = self.sample.split("## 9. Approval")[0] + "UNRESOLVED: which database?\n"
        self.assertEqual(self.validate(draft, "--draft").returncode, 0)
        result = self.validate(draft)
        self.assertFails(result, "unresolved decision(s) remain")
        self.assertIn("Missing Approval section", result.stdout)

    def test_edit_after_approval_fails(self):
        edited = self.sample.replace("integration branch `main`", "integration branch `develop`")
        self.assertFails(self.validate(edited), "changed after approval")

    def test_hash_ignores_approval_decisions_and_line_endings(self):
        expected = validate_discovery.content_hash(self.sample)
        with_decisions = self.sample + "\n## Configuration Decisions\n\n| Key | Value | Source |\n"
        self.assertEqual(validate_discovery.content_hash(with_decisions), expected)
        self.assertEqual(validate_discovery.content_hash(self.sample.replace("\n", "\r\n")), expected)
        reapproved = self.sample.replace("2026-01-15", "2026-02-01")
        self.assertEqual(validate_discovery.content_hash(reapproved), expected)
        self.assertEqual(self.validate(with_decisions).returncode, 0)

    def test_only_exact_decisions_heading_is_excluded_from_hash(self):
        expected = validate_discovery.content_hash(self.sample)
        for heading in ("### Configuration Decisions", "## configuration decisions"):
            # Inserted before the Approval section so it isn't a subsection of it.
            product = self.sample.replace(
                "## 9. Approval", f"{heading}\n\nAdded after approval.\n\n## 9. Approval"
            )
            self.assertNotEqual(validate_discovery.content_hash(product), expected, heading)

    def test_adr_trade_off_spellings(self):
        for spelling in ("Tradeoffs", "Trade offs", "trade-off"):
            product = self.sample.replace("Trade-offs", spelling)
            self.assertEqual(self.validate(product, "--draft").returncode, 0, spelling)
        product = self.sample.replace("Trade-offs", "Compromises")
        self.assertFails(self.validate(product, "--draft"), "One or more ADRs are missing")

    def test_fr_001_is_reserved_for_initialization(self):
        product = self.sample.replace("| `FR-002` |", "| `FR-001` |")
        self.assertFails(self.validate(product, "--draft"), "FR-001 is reserved for initialization")

    def test_duplicate_ids_fail(self):
        # Reviewer's repro: a second FR-002 row used to pass as "4 unique" IDs.
        product = self.sample.replace("| `FR-003` |", "| `FR-002` |")
        self.assertFails(self.validate(product, "--draft"), "Duplicate ID definition(s): FR-002")
        product = self.sample.replace("## 6. Development Environment Setup", (
            "### `ADR-001`: A second record\n\nContext, decision, consequences, trade-offs.\n\n"
            "## 6. Development Environment Setup"
        ))
        self.assertFails(self.validate(product, "--draft"), "Duplicate ID definition(s): ADR-001")

    def test_sub_items_of_an_id_are_not_duplicates(self):
        # The sample's "Exception Flow `UC-001-EX1`" sits under "Use Case `UC-001`".
        self.assertIn("UC-001-EX1", self.sample)
        product = self.sample.replace("#### Basic Flow (Happy Path)", "#### Basic Flow of `UC-001`")
        result = self.validate(product, "--draft")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("are each defined once", result.stdout)

    def test_empty_approver_fails(self):
        # Reviewer's repro: the next line used to be read as the approver.
        product = self.sample.replace("- **Approved by**: Product Owner (example)", "- **Approved by**:")
        self.assertFails(self.validate(product), "Missing Approval section")

    def test_ids_use_three_digits(self):
        product = self.sample.replace("`US-001`", "`US-01`")
        self.assertFails(self.validate(product, "--draft"), "IDs use three digits (e.g. UC-001): US-01")

    def test_risk_score_is_impact_times_probability(self):
        product = self.sample.replace("| Medium (2) | Medium (2) | **4** |", "| Medium (2) | Medium (2) | **5** |")
        self.assertFails(self.validate(product, "--draft"), "RSK-002: Score 5 is not Impact x Probability (4)")

    def test_high_risk_needs_mitigation(self):
        lines = self.sample.split("\n")
        row = next(index for index, line in enumerate(lines) if line.startswith("| `RSK-001` |"))
        lines[row] = lines[row].rsplit("|", 2)[0] + "|  |"
        self.assertFails(self.validate("\n".join(lines), "--draft"), "RSK-001: score 9 needs a mitigation plan")

    def test_risk_rows_are_required_and_unique(self):
        product = "\n".join(line for line in self.sample.split("\n") if "`RSK-00" not in line)
        result = self.validate(product, "--draft")
        self.assertFails(result, "Missing required section: Risk Assessment & Roadmap")
        self.assertIn("No RSK-xxx risk rows found", result.stdout)
        product = self.sample.replace("| `RSK-002` |", "| `RSK-001` |")
        self.assertFails(self.validate(product, "--draft"), "Duplicate ID definition(s): RSK-001")

    def test_product_template_passes_draft(self):
        result = run(DISCOVERY_SCRIPT, "--draft", PRODUCT_TEMPLATE)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_fragments_fit_the_product_template(self):
        # Fragments are pasted into PRODUCT.md: no document title of their own,
        # and every ID uses the three-digit format.
        for name in FRAGMENTS:
            text = read(os.path.join(TEMPLATES, name))
            self.assertFalse(any(line.startswith("# ") for line in text.split("\n")), name)
            self.assertIn("product-template.md", text, name)
            malformed = [
                match.group(0) for match in validate_discovery.ID_PATTERN.finditer(text)
                if len(match.group(1)) != 3
            ]
            self.assertEqual(malformed, [], name)

    def test_hash_flag_prints_recorded_hash(self):
        path = os.path.join(self.dir, "PRODUCT.md")
        write(path, self.sample)
        result = run(DISCOVERY_SCRIPT, "--hash", path)
        self.assertEqual(result.stdout.strip(), validate_discovery.content_hash(self.sample))
        self.assertIn(result.stdout.strip(), self.sample)

    def test_typographic_wont_have_passes(self):
        product = self.sample.replace("**MVP Won't Have**", "**MVP Won’t Have**")
        product = product.replace(
            validate_discovery.content_hash(self.sample), validate_discovery.content_hash(product)
        )
        result = self.validate(product)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_moscow_outside_requirement_sections_fails(self):
        product = self.sample.replace("**MVP Won't Have**", "**MVP Out of scope**")
        product = product.replace("## 7. Risk Assessment", "Won't have: batch uploads.\n\n## 7. Risk Assessment")
        self.assertFails(self.validate(product, "--draft"), "Won't Have is not stated")

    def test_moscow_needs_real_priorities(self):
        # Reviewer's repro: all Must Have plus the fragment's placeholder priority passed.
        product = self.sample.replace("| Should Have |", "| Must Have |").replace("| Could Have |", "| Must Have |")
        product = product.replace("- **MVP Won't Have**: Batch processing of multiple FITS files in one request.\n", "")
        product = product.replace(
            "- **Priority**: Must Have", "- **Priority**: [Must Have / Should Have / Could Have / Won't Have]"
        )
        result = self.validate(product, "--draft")
        self.assertFails(result, "US-001: Priority must be one of")
        self.assertIn("Won't Have is not stated", result.stdout)
        product = self.sample.replace("| Must Have |", "| Should Have |").replace(
            "- **Priority**: Must Have", "- **Priority**: Should Have"
        )
        self.assertFails(self.validate(product, "--draft"), "No requirement or user story is Must Have")
        product = self.sample.replace("| Could Have |", "| Could Have | Must Have |")
        self.assertFails(self.validate(product, "--draft"), "FR-005: needs exactly one MoSCoW priority")

    def test_ears_pattern_column_matches_statement(self):
        # Reviewer's repro: a WHEN statement labelled State-Driven passed.
        product = self.sample.replace("| `FR-002` | Event-Driven |", "| `FR-002` | State-Driven |")
        self.assertFails(
            self.validate(product, "--draft"), "FR-002: declared State-Driven, but the statement is event-driven"
        )
        product = self.sample.replace("| `FR-003` | Ubiquitous |", "| `FR-003` | Complex |")
        self.assertFails(self.validate(product, "--draft"), "FR-003: unknown EARS pattern 'Complex'")

    def test_references_must_resolve(self):
        # Reviewer's repro: a trace to a use case that doesn't exist passed.
        product = self.sample.replace("| Must Have | `UC-001` |", "| Must Have | `UC-009` |", 1)
        self.assertFails(self.validate(product, "--draft"), "Reference(s) to undefined ID(s): UC-009")
        product = self.sample.replace("(`UC-001-EX1`)", "(`UC-002-EX1`)")
        self.assertFails(self.validate(product, "--draft"), "Reference(s) to undefined ID(s): UC-002")

    def test_placeholders_fail_approval_and_warn_in_draft(self):
        # Reviewer's repro: an approved document full of template placeholders passed.
        product = self.approved(self.sample.replace("- **Naming**:", "- **Owner**: [Team name]\n- **Naming**:"))
        draft = self.validate(product, "--draft")
        self.assertEqual(draft.returncode, 0, draft.stdout)
        self.assertIn("[WARN] 1 template placeholder(s) left, e.g. [Team name]", draft.stdout)
        self.assertFails(self.validate(product), "[FAIL] 1 template placeholder(s) left")

    def test_links_task_boxes_and_code_are_not_placeholders(self):
        addition = "- **Docs**: [Astropy](https://www.astropy.org), `config[key]`, [ ] and [x] boxes.\n"
        product = self.approved(self.sample.replace("- **Naming**:", addition + "- **Naming**:"))
        result = self.validate(product)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_guidance_notes_do_not_block_approval(self):
        # The product template's note mentions UNRESOLVED: and placeholders.
        note = "> Mark every open decision with `UNRESOLVED:` and replace each [placeholder].\n\n"
        product = self.approved(self.sample.replace("## 1. Executive Summary", note + "## 1. Executive Summary"))
        result = self.validate(product)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_filled_approval_on_unfilled_template_fails(self):
        template = read(PRODUCT_TEMPLATE).replace("\r\n", "\n")
        template = template.replace("- **Approved by**: [Name or role]", "- **Approved by**: Product Owner")
        template = template.replace("- **Approved on**: [YYYY-MM-DD]", "- **Approved on**: 2026-10-01")
        template = template.replace(
            "- **Approved content**: [Output of `validate_discovery.py --hash docs/PRODUCT.md` for the approved version]",
            f"- **Approved content**: `{validate_discovery.content_hash(template)}`",
        )
        self.assertFails(self.validate(template), "template placeholder(s) left")

    def test_enclosing_heading_does_not_satisfy_empty_sections(self):
        product = (
            "# Use Case, Functional Requirement, User Story, Tech Stack, Architecture Decision, "
            "Dev Environment, Risk, Governance Package\n\nUC-001 FR-001 US-001 ADR-001 RSK-001 MVP\n\n"
            "## Use Cases\n\n## User Stories\n\n## Risks\n"
        )
        result = self.validate(product, "--draft")
        self.assertFails(result, "Missing required section: Use Cases")
        self.assertIn("Missing required section: Risk Assessment & Roadmap", result.stdout)

    def test_directory_mode_requires_product(self):
        self.assertEqual(run(DISCOVERY_SCRIPT, self.dir).returncode, 1)
        write(os.path.join(self.dir, "docs", "PRODUCT.md"), self.sample)
        self.assertEqual(run(DISCOVERY_SCRIPT, self.dir).returncode, 0)


if __name__ == "__main__":
    unittest.main()
