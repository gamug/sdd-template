"""Regression tests for validate_config.py (discovery gate, sources, render)."""

import os
import unittest

from fixtures import Project, read, write
import validate_config


class DiscoveryGateTest(unittest.TestCase):
    def test_refuses_without_product(self):
        project = Project(self)
        project.write()
        os.remove(project.product_path)
        os.remove(project.config_path)
        result = project.invoke("scaffold")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(os.path.exists(project.config_path))
        self.assertIn("Complete WI-001", result.stdout)

    def test_refuses_unapproved_product(self):
        project = Project(self)
        project.product = project.product.replace("- **Approved content**", "- **Content**")
        result = project.run("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("not an approved discovery package", result.stdout)
        self.assertIn("[FAIL] Missing Approval section", result.stdout)

    def test_refuses_product_edited_after_approval(self):
        # Reviewer's repro: fake evidence inserted after approval.
        project = Project(self)
        project.product = project.product.replace(
            "## 8. Governance & Workflow\n", "## 8. Governance & Workflow\n\nproject.kind-value\n"
        )
        project.set("project.kind", "project.kind-value", "PRODUCT.md § Governance")
        result = project.run("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("changed after approval", result.stdout)


class ScaffoldTest(unittest.TestCase):
    def test_scaffold_fill_check_render_verify(self):
        # The path every fork takes: scaffold -> fill -> check -> render -> verify.
        project = Project(self)
        write(project.product_path, project.product)
        result = project.invoke("scaffold")
        self.assertEqual(result.returncode, 0, result.stdout)

        config = validate_config.load_config(project.config_path)
        for key in project.required:
            self.assertTrue(validate_config.lookup(config, key)[0], key)
        self.assertIn("# PRODUCT.md: Governance & Workflow", read(project.config_path))
        product = read(project.product_path)
        self.assertEqual(product.count("\n## Configuration Decisions\n"), 1)
        for key in project.required:
            self.assertIn(f"| `{key}` |  |  |", product)

        rerun = project.invoke("scaffold")
        self.assertEqual(rerun.returncode, 1)
        self.assertIn("already exists", rerun.stdout)
        forced = project.invoke("scaffold", "--force")
        self.assertEqual(forced.returncode, 0, forced.stdout)
        self.assertEqual(read(project.product_path).count("\n## Configuration Decisions\n"), 1)

        unfilled = project.invoke("check")
        self.assertEqual(unfilled.returncode, 1)
        self.assertIn("Empty value: project.name", unfilled.stdout)

        for mode in (("check",), ("render",), ("render", "--verify")):
            result = project.run(*mode)
            self.assertEqual(result.returncode, 0, f"{mode}: {result.stdout}")


class CheckTest(unittest.TestCase):
    def assertCheckFails(self, project, message):
        result = project.run("check")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(message, result.stdout)

    def test_baseline_passes(self):
        result = Project(self).run("check")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_key(self):
        project = Project(self)
        del project.values["project.name"]
        self.assertCheckFails(project, "Missing key: project.name")

    def test_missing_decisions_row(self):
        project = Project(self)
        project.write()
        product = read(project.product_path)
        product = "\n".join(line for line in product.split("\n") if "`project.name`" not in line)
        write(project.product_path, product)
        result = project.invoke("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("No Configuration Decisions row for: project.name", result.stdout)

    def test_escaped_pipe_in_value(self):
        project = Project(self)
        project.set("commands.test", "pytest -q | tee test.log")
        result = project.run("check")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_fabricated_section(self):
        project = Project(self)
        project.set("project.name", "x-project-name", "PRODUCT.md § Deployment Strategy")
        self.assertCheckFails(project, "cites a section PRODUCT.md does not have")

    def test_document_title_is_not_evidence(self):
        # Reviewer's repro: the H1 spans the decisions table, so the row
        # vouched for itself.
        project = Project(self)
        project.set("project.name", "zzz-invented-name", "PRODUCT.md § Technical Discovery")
        self.assertCheckFails(
            project, "cites a section with subsections: 'PRODUCT.md § Technical Discovery'"
        )

    def test_decisions_table_is_not_citable(self):
        project = Project(self)
        project.set("project.name", "x-project-name", "PRODUCT.md § Configuration Decisions")
        self.assertCheckFails(project, "cites a section PRODUCT.md does not have")

    def test_collection_drift(self):
        project = Project(self)
        project.recorded["domain_sections"] = '[{"title":"Models","rules":["Pin checkpoints."]}]'
        self.assertCheckFails(project, "Recorded value for domain_sections must be the compact JSON")

    def test_value_sourced_from_section_that_contains_it(self):
        project = Project(self)
        project.set("runtime.version", "3.12.2", "PRODUCT.md § 6")
        result = project.run("check")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_value_embedded_in_longer_token_is_not_evidence(self):
        # Section 6 says "Python 3.12.2"; "3.1" must not count as sourced.
        project = Project(self)
        project.set("runtime.version", "3.1", "PRODUCT.md § 6")
        self.assertCheckFails(project, "does not appear in the cited section")

    def test_domain_sections_require_user_source(self):
        project = Project(self)
        project.set(
            "domain_sections",
            [{"title": "Use Case", "rules": ["Upload"]}],
            "PRODUCT.md § Use Case",
        )
        self.assertCheckFails(project, "Source for domain_sections must be 'user, YYYY-MM-DD'")

    def test_collection_items_need_evidence(self):
        project = Project(self)
        project.set("quality.ci_gate_order", ["ruff check", "mypy", "pytest -q"], "PRODUCT.md § Governance")
        self.assertEqual(project.run("check").returncode, 0)
        project.set("quality.ci_gate_order", ["ruff check", "bandit", "pytest -q"], "PRODUCT.md § Governance")
        self.assertCheckFails(project, "'bandit'")


class AppearsInTest(unittest.TestCase):
    def test_token_boundaries(self):
        self.assertTrue(validate_config.appears_in("3.12", "Python 3.12."))
        self.assertTrue(validate_config.appears_in("main", "integration branch `main`;"))
        self.assertFalse(validate_config.appears_in("3.1", "Python 3.12.2"))
        self.assertFalse(validate_config.appears_in("main", "the domain model"))
        self.assertFalse(validate_config.appears_in("env", "copy .env.example"))


class RenderTest(unittest.TestCase):
    def test_render_keeps_values_as_written_and_verifies(self):
        project = Project(self)
        result = project.run("render")
        self.assertEqual(result.returncode, 0, result.stdout)
        rendered = read(os.path.join(project.dir, ".sdd", "constitution.md"))
        self.assertNotIn("{{", rendered)
        self.assertIn("2026-01-15", rendered)
        self.assertIn("1.10", rendered)
        self.assertEqual(project.run("render", "--verify").returncode, 0)

    def test_verify_detects_stale_render(self):
        project = Project(self)
        self.assertEqual(project.run("render").returncode, 0)
        project.set("project.name", "renamed")
        result = project.run("render", "--verify")
        self.assertEqual(result.returncode, 1)
        self.assertIn("out of date", result.stdout)


if __name__ == "__main__":
    unittest.main()
