"""Regression tests for canonical workflow continuation transitions."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_STATUS_PATH = REPO_ROOT / ".codestable/tools/build-status.py"
CONTRACT_CHECK_PATH = REPO_ROOT / ".codestable/tools/check-workflow-contracts.py"


def load_build_status_module():
    spec = importlib.util.spec_from_file_location("workflow_build_status", BUILD_STATUS_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build_status = load_build_status_module()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class WorkflowStatusTransitionTests(unittest.TestCase):
    def feature_item(self, plan_status: str) -> dict:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            feature_dir = root / ".codestable/features/2026-07-15-plan-gate"
            write(
                feature_dir / "plan-gate-design.md",
                "---\nstatus: approved\nworkflow: hybrid\n---\n# Design\n",
            )
            write(
                feature_dir / "plan-gate-plan.md",
                f"---\nstatus: {plan_status}\n---\n# Plan\n",
            )
            write(
                feature_dir / "plan-gate-checklist.yaml",
                "steps:\n  - action: implement\n    status: pending\n",
            )
            item, _ = build_status.feature_item(feature_dir, root)
            return item

    def issue_item(self, report_status: str) -> dict:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".codestable/issues/2026-07-15-report-gate"
            write(
                issue_dir / "report-gate-report.md",
                f"---\nstatus: {report_status}\n---\n# Report\n",
            )
            item, _ = build_status.issue_item(issue_dir, root)
            return item

    def test_draft_plan_remains_at_explicit_plan_approval_gate(self):
        derived = self.feature_item("draft")["derived"]

        self.assertEqual("cs-feat-plan", derived["next_skill"])
        self.assertFalse(derived["auto_continue_allowed"])
        self.assertTrue(derived["needs_user_decision"])
        self.assertIn("awaiting_plan_approval", derived["blockers"])

    def test_approved_plan_auto_continues_to_implementation(self):
        derived = self.feature_item("approved")["derived"]

        self.assertEqual("cs-feat-impl", derived["next_skill"])
        self.assertTrue(derived["auto_continue_allowed"])
        self.assertFalse(derived["needs_user_decision"])
        self.assertEqual([], derived["blockers"])

    def test_draft_report_does_not_auto_continue_to_analysis(self):
        derived = self.issue_item("draft")["derived"]

        self.assertEqual("cs-issue-report", derived["next_skill"])
        self.assertFalse(derived["auto_continue_allowed"])
        self.assertTrue(derived["needs_user_decision"])
        self.assertIn("awaiting_report_confirmation", derived["blockers"])

    def test_confirmed_report_auto_continues_to_analysis(self):
        derived = self.issue_item("confirmed")["derived"]

        self.assertEqual("cs-issue-analyze", derived["next_skill"])
        self.assertTrue(derived["auto_continue_allowed"])
        self.assertFalse(derived["needs_user_decision"])


    def test_acceptance_cannot_complete_a_feature_with_a_draft_plan(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            feature_dir = root / ".codestable/features/2026-07-15-premature-acceptance"
            write(
                feature_dir / "premature-acceptance-design.md",
                "---\nstatus: approved\nworkflow: hybrid\n---\n# Design\n",
            )
            write(
                feature_dir / "premature-acceptance-plan.md",
                "---\nstatus: draft\n---\n# Plan\n",
            )
            write(
                feature_dir / "premature-acceptance-checklist.yaml",
                "steps:\n  - action: implement\n    status: done\n",
            )
            write(feature_dir / "premature-acceptance-acceptance.md", "# Partial acceptance\n")
            item, _ = build_status.feature_item(feature_dir, root)

        derived = item["derived"]
        self.assertFalse(derived["canonical_complete"])
        self.assertEqual("cs-feat-plan", derived["next_skill"])
        self.assertIn("awaiting_plan_approval", derived["blockers"])

    def test_analysis_cannot_bypass_an_unconfirmed_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".codestable/issues/2026-07-15-invalid-analysis-order"
            write(issue_dir / "invalid-analysis-order-report.md", "---\nstatus: draft\n---\n# Report\n")
            write(issue_dir / "invalid-analysis-order-analysis.md", "---\nstatus: confirmed\n---\n# Analysis\n")
            item, _ = build_status.issue_item(issue_dir, root)

        self.assertEqual("conflict", item["consistency"]["state"])
        self.assertEqual("cs-issue-report", item["derived"]["next_skill"])
        self.assertFalse(item["derived"]["auto_continue_allowed"])
        self.assertIn("awaiting_report_confirmation", item["derived"]["blockers"])
        self.assertIn("canonical_conflict", item["derived"]["blockers"])


    def test_premature_acceptance_with_pending_steps_returns_to_implementation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            feature_dir = root / ".codestable/features/2026-07-15-pending-acceptance"
            write(
                feature_dir / "pending-acceptance-design.md",
                "---\nstatus: approved\nworkflow: hybrid\n---\n# Design\n",
            )
            write(feature_dir / "pending-acceptance-plan.md", "---\nstatus: approved\n---\n# Plan\n")
            write(
                feature_dir / "pending-acceptance-checklist.yaml",
                "steps:\n  - action: implement\n    status: pending\n",
            )
            write(feature_dir / "pending-acceptance-acceptance.md", "# Partial acceptance\n")
            item, _ = build_status.feature_item(feature_dir, root)

        self.assertFalse(item["derived"]["canonical_complete"])
        self.assertEqual("cs-feat-impl", item["derived"]["next_skill"])
        self.assertIn("missing_required_artifact", item["derived"]["blockers"])

    def test_legacy_accepted_feature_remains_a_compatibility_terminal(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            feature_dir = root / ".codestable/features/2026-07-15-legacy-accepted"
            write(feature_dir / "legacy-accepted-design.md", "---\nstatus: approved\n---\n# Design\n")
            write(
                feature_dir / "legacy-accepted-checklist.yaml",
                "steps:\n  - action: implement\n    status: done\n",
            )
            write(feature_dir / "legacy-accepted-acceptance.md", "# Acceptance\n")
            item, _ = build_status.feature_item(feature_dir, root)

        self.assertTrue(item["derived"]["canonical_complete"])
        self.assertEqual("terminal", item["derived"]["continuation_mode"])

    def test_fix_note_cannot_bypass_a_draft_standard_issue(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".codestable/issues/2026-07-15-premature-fix-note"
            write(issue_dir / "premature-fix-note-report.md", "---\nstatus: draft\n---\n# Report\n")
            write(issue_dir / "premature-fix-note-analysis.md", "---\nstatus: draft\n---\n# Analysis\n")
            write(issue_dir / "premature-fix-note-fix-note.md", "# Fix note\n")
            item, _ = build_status.issue_item(issue_dir, root)

        self.assertFalse(item["derived"]["canonical_complete"])
        self.assertEqual("cs-issue-report", item["derived"]["next_skill"])
        self.assertIn("awaiting_report_confirmation", item["derived"]["blockers"])


    def test_missing_workflow_with_a_plan_is_not_legacy(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            feature_dir = root / ".codestable/features/2026-07-15-modern-without-workflow"
            write(feature_dir / "modern-without-workflow-design.md", "---\nstatus: approved\n---\n# Design\n")
            write(feature_dir / "modern-without-workflow-plan.md", "---\nstatus: draft\n---\n# Plan\n")
            write(
                feature_dir / "modern-without-workflow-checklist.yaml",
                "steps:\n  - action: implement\n    status: done\n",
            )
            write(feature_dir / "modern-without-workflow-acceptance.md", "# Acceptance\n")
            item, _ = build_status.feature_item(feature_dir, root)

        self.assertFalse(item["derived"]["canonical_complete"])
        self.assertTrue(item["derived"]["active"])
        self.assertEqual("cs-feat-plan", item["derived"]["next_skill"])
        self.assertIn("awaiting_plan_approval", item["derived"]["blockers"])
        self.assertEqual("conflict", item["consistency"]["state"])

    def test_confirmed_fast_path_requires_a_completed_fix_note(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".codestable/issues/2026-07-15-fast-path"
            write(issue_dir / "fast-path-report.md", "---\nstatus: confirmed\n---\n# Report\n")
            write(issue_dir / "fast-path-fix-note.md", "---\nstatus: completed\n---\n# Fix note\n")
            completed, _ = build_status.issue_item(issue_dir, root)
            write(issue_dir / "fast-path-fix-note.md", "---\nstatus: draft\n---\n# Fix note\n")
            premature, _ = build_status.issue_item(issue_dir, root)

        self.assertTrue(completed["derived"]["canonical_complete"])
        self.assertEqual("terminal", completed["derived"]["continuation_mode"])
        self.assertFalse(premature["derived"]["canonical_complete"])
        self.assertTrue(premature["derived"]["active"])
        self.assertEqual("cs-issue-analyze", premature["derived"]["next_skill"])


    def test_standard_fix_note_requires_completed_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".codestable/issues/2026-07-15-standard-fix"
            write(issue_dir / "standard-fix-report.md", "---\nstatus: confirmed\n---\n# Report\n")
            write(issue_dir / "standard-fix-analysis.md", "---\nstatus: confirmed\n---\n# Analysis\n")
            write(issue_dir / "standard-fix-fix-note.md", "---\nstatus: draft\n---\n# Fix note\n")
            draft, _ = build_status.issue_item(issue_dir, root)
            write(issue_dir / "standard-fix-fix-note.md", "---\nstatus: completed\n---\n# Fix note\n")
            completed, _ = build_status.issue_item(issue_dir, root)

        self.assertFalse(draft["derived"]["canonical_complete"])
        self.assertTrue(draft["derived"]["active"])
        self.assertEqual("cs-issue-fix", draft["derived"]["next_skill"])
        self.assertTrue(completed["derived"]["canonical_complete"])
        self.assertEqual("terminal", completed["derived"]["continuation_mode"])


    def test_draft_fix_note_only_resumes_fix_but_legacy_note_stays_terminal(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issue_dir = root / ".codestable/issues/2026-07-15-fix-note-only"
            note = issue_dir / "fix-note-only-fix-note.md"
            write(note, "---\nstatus: draft\n---\n# Fix note\n")
            draft, _ = build_status.issue_item(issue_dir, root)
            write(note, "# Legacy fix note\n")
            legacy, _ = build_status.issue_item(issue_dir, root)

        self.assertFalse(draft["derived"]["canonical_complete"])
        self.assertTrue(draft["derived"]["active"])
        self.assertEqual("cs-issue-fix", draft["derived"]["next_skill"])
        self.assertTrue(draft["derived"]["auto_continue_allowed"])
        self.assertTrue(legacy["derived"]["canonical_complete"])
        self.assertEqual("terminal", legacy["derived"]["continuation_mode"])

    def test_ccg_bridge_changes_do_not_change_generated_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            feature_dir = root / ".codestable/features/2026-07-15-bridge-boundary"
            write(
                feature_dir / "bridge-boundary-design.md",
                "---\nstatus: approved\nworkflow: hybrid\n---\n# Design\n",
            )
            before = json.dumps(build_status.build_status(root), sort_keys=True)
            write(
                root / ".ccg/tasks/stale-bridge/task.json",
                '{"status": "in_progress", "nextAction": "repeat forever"}\n',
            )
            after = json.dumps(build_status.build_status(root), sort_keys=True)

        self.assertEqual(before, after)

    def test_check_json_reports_stale_when_snapshot_is_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            result = subprocess.run(
                [sys.executable, str(BUILD_STATUS_PATH), "--repo-root", str(root), "--check", "--json"],
                capture_output=True,
                text=True,
                check=False,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        self.assertEqual("stale", payload["freshness"]["state"])
        self.assertFalse(payload["matches_canonical_snapshot"])

    def test_check_json_requires_check_flag(self):
        result = subprocess.run(
            [sys.executable, str(BUILD_STATUS_PATH), "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("--json requires --check", result.stderr)

    def test_contract_checker_enforces_tracked_markdown_and_honors_explicit_fixture_exemption(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "AGENTS.md", "单md文档不能超过5行\n")
            write(root / ".gitignore", "")
            write(root / "README.md", "one\ntwo\nthree\nfour\nfive\nsix\n")
            write(
                root / ".codestable/reference/markdown-line-limit-exemptions.json",
                '{"version": 1, "exemptions": [{"path": "fixture.md", "reason": "test fixture"}]}\n',
            )
            write(root / "fixture.md", "one\ntwo\nthree\nfour\nfive\nsix\n")
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "AGENTS.md", "README.md", "fixture.md"], check=True)
            result = subprocess.run(
                [sys.executable, str(CONTRACT_CHECK_PATH), "--repo-root", str(root), "--json"],
                capture_output=True,
                text=True,
                check=False,
            )

        payload = json.loads(result.stdout)
        failures = [item for item in payload["findings"] if item["rule"] == "markdown_line_limit"]
        self.assertEqual(1, result.returncode)
        self.assertEqual(["README.md"], [item["path"] for item in failures])

    def test_onboard_builder_copy_matches_canonical_tool(self):
        source = (REPO_ROOT / "cs-onboard/tools/build-status.py").read_bytes()
        canonical = BUILD_STATUS_PATH.read_bytes()
        self.assertEqual(canonical, source)


if __name__ == "__main__":
    unittest.main()
