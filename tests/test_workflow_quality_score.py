"""Regression coverage for the deterministic workflow quality scorer."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCORE_PATH = REPO_ROOT / ".codestable/tools/score-workflow.py"
EVIDENCE_PATH = REPO_ROOT / ".codestable/tools/check-workflow-evidence.py"


class WorkflowQualityScoreTests(unittest.TestCase):
    def run_score(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCORE_PATH), "--repo-root", str(root), *args, "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_repository_skills_meet_the_quality_bar(self):
        result = self.run_score(REPO_ROOT, "--check-skills", "--min-skill-score", "100")
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(0, payload["summary"]["skills_below_threshold"])
        self.assertEqual(100, payload["summary"]["skill_percent"])

    def test_missing_quality_contract_fails_the_skill_gate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "cs").mkdir()
            (root / "cs/SKILL.md").write_text(
                "---\nname: cs\ndescription: test\n---\n\n# cs\n\n## 启动必读\n\ntext\n",
                encoding="utf-8",
            )
            result = self.run_score(root, "--check-skills")
        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual(1, payload["summary"]["skills_below_threshold"])


class WorkflowEvidenceTests(unittest.TestCase):
    def run_evidence(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(EVIDENCE_PATH), "--repo-root", str(root), "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

    def write_checklist(self, root: Path, contract: bool, complete: bool, lane: str = "features") -> None:
        artifact_dir = root / f".codestable/{lane}/2026-01-01-demo"
        artifact_dir.mkdir(parents=True)
        evidence = {"result": "pytest passed", "verified_at": "2026-01-01", "verified_by": "ci"} if complete else {
            "result": "pending",
            "verified_at": None,
            "verified_by": None,
        }
        payload = {
            "feature": "2026-01-01-demo",
            "steps": [
                {
                    "id": "step-1",
                    "action": "implement",
                    "status": "done" if complete else "pending",
                    "verification": {"method": "command", "expected": "tests pass"},
                    "evidence": evidence,
                }
            ],
            "checks": [
                {
                    "id": "check-1",
                    "item": "verify",
                    "status": "passed" if complete else "pending",
                    "verification": {"method": "command", "expected": "tests pass"},
                    "evidence": dict(evidence),
                }
            ],
        }
        if contract:
            payload["evidence_contract"] = "v1"
        (artifact_dir / "demo-checklist.yaml").write_text(
            yaml.safe_dump(payload, sort_keys=False), encoding="utf-8"
        )

    def test_valid_v1_checklist_passes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.write_checklist(Path(temp_dir), contract=True, complete=True)
            result = self.run_evidence(Path(temp_dir))
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(0, payload["errors"])

    def test_valid_v1_refactor_checklist_is_scanned(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.write_checklist(Path(temp_dir), contract=True, complete=True, lane="refactors")
            result = self.run_evidence(Path(temp_dir))
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(1, payload["validated"])

    def test_completed_v1_item_without_evidence_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_checklist(root, contract=True, complete=True)
            path = root / ".codestable/features/2026-01-01-demo/demo-checklist.yaml"
            path.write_text(path.read_text(encoding="utf-8").replace("pytest passed", "pending"), encoding="utf-8")
            result = self.run_evidence(root)
        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(any(item["rule"] == "evidence_result" for item in payload["findings"]))

    def test_legacy_checklist_without_contract_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.write_checklist(Path(temp_dir), contract=False, complete=True)
            result = self.run_evidence(Path(temp_dir))
        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual(0, payload["validated"])

    def test_v1_report_missing_required_sections_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            report_dir = root / ".codestable/features/2026-01-01-demo"
            report_dir.mkdir(parents=True)
            (report_dir / "demo-acceptance.md").write_text(
                "---\nevidence_contract: v1\n---\n\n# Acceptance\n",
                encoding="utf-8",
            )
            result = self.run_evidence(root)
        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual(
            {"evidence_report_section"},
            {item["rule"] for item in payload["findings"]},
        )


if __name__ == "__main__":
    unittest.main()
