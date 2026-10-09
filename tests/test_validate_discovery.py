"""Regression tests for validate_discovery.py (sections, EARS, MoSCoW, approval)."""

import os
import shutil
import tempfile
import unittest

from fixtures import DISCOVERY_SCRIPT, SAMPLE, read, run, write
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
        self.assertFails(self.validate(product, "--draft"), "Missing MoSCoW priorities: won't have")

    def test_enclosing_heading_does_not_satisfy_empty_sections(self):
        product = (
            "# Use Case, Functional Requirement, User Story, Tech Stack, Architecture Decision, "
            "Dev Environment, Risk, Governance Package\n\nUC-01 FR-001 US-01 ADR-001 RSK-01 MVP\n\n"
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
