"""Text-level checks for the Markdown-defined routing protocol."""

from __future__ import annotations

import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_CHECK_PATH = REPO_ROOT / ".codestable/tools/check-workflow-contracts.py"
CONTRACT_CHECKER = runpy.run_path(str(CONTRACT_CHECK_PATH), run_name="skill_route_contract_tests")


def text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class SkillRoutingContractTests(unittest.TestCase):
    def test_shared_fastforward_contract_has_one_authoritative_definition(self):
        sections = []
        for skill in ("cs-feat-ff", "cs-refactor-ff"):
            content = text(f"{skill}/SKILL.md")
            section = content.split("## Shared fastforward contract\n", 1)[1].split("\n---", 1)[0]
            self.assertIn(".codestable/reference/terminology.md", section)
            self.assertNotIn("\n- ", section)
            sections.append(section)
        self.assertEqual(sections[0], sections[1])

    def test_startup_shared_conventions_are_on_demand(self):
        for path in sorted(REPO_ROOT.glob("cs*/SKILL.md")):
            with self.subTest(skill=path.parent.name):
                startup = path.read_text(encoding="utf-8").split("## 启动必读\n", 1)[1].split("\n## ", 1)[0].split("**缓存优化**", 1)[0]
                for line in startup.splitlines():
                    if "shared-conventions" not in line:
                        continue
                    self.assertNotIn("Hard-required", line)
                    self.assertTrue(any(marker in line for marker in ("On-demand", "命中后", "时读取", "时查")), line)

    def test_issue_fast_path_has_independent_exit_and_resume_rules(self):
        report = text("cs-issue-report/SKILL.md")
        exits = report.split("## 退出条件\n", 1)[1].split("\n---", 1)[0]
        self.assertIn("### 标准路径", exits)
        self.assertIn("### 快速通道", exits)
        self.assertIn("不要求补齐标准 report", exits)
        self.assertIn("已有 draft fix-note", text("cs-issue-fix/SKILL.md"))

    def test_root_router_keeps_continuation_out_of_generic_switch_prompt(self):
        content = text("cs/SKILL.md")
        self.assertIn("唯一 fresh 且无 blocker 的 canonical 候选", content)
        self.assertIn("只用于非 continuation 的普通路由", content)
        self.assertIn("并直接进入", content)


    def test_required_checkpoint_approval_is_consumed_once(self):
        self.assertIn("立即 handoff 到 `cs-feat-plan`", text("cs-feat-design/SKILL.md"))
        self.assertIn("立即 handoff 到 `cs-issue-analyze`", text("cs-issue-report/SKILL.md"))
        self.assertIn("立即 handoff 到 `cs-issue-fix`", text("cs-issue-analyze/SKILL.md"))
        self.assertIn("再直接切到 `cs-feat-impl`", text("cs-feat-plan/SKILL.md"))
        self.assertIn("立即 handoff 到 `cs-feat-accept`", text("cs-feat-impl/SKILL.md"))
        self.assertIn("同一回复中直接 handoff", text(".codestable/reference/workflow-continuation-feature.md"))
        self.assertIn("同一回复中直接 handoff", text(".codestable/reference/workflow-continuation-issue.md"))

    def test_feature_plan_persists_its_independent_approval(self):
        content = text("cs-feat-plan/SKILL.md")
        self.assertIn("`status` 从 `draft` 改为 `approved`", content)
        self.assertIn("`status=approved`", text("cs-feat-impl/SKILL.md"))

    def test_feature_router_requires_an_approved_plan_for_implementation(self):
        content = text("cs-feat/SKILL.md")
        self.assertIn("`plan.md` 已 `status=approved`", content)

    def test_issue_router_keeps_draft_reports_in_report_stage(self):
        content = text("cs-issue/SKILL.md")
        self.assertIn("`report.md` 是 `status=draft`", content)
        self.assertIn("`report.md` 已 `status=confirmed`", content)


    def test_downstream_skills_enforce_canonical_gate_status(self):
        self.assertIn("`{slug}-plan.md` 必须存在且 `status=approved`", text("cs-feat-accept/SKILL.md"))
        self.assertIn("`analysis.md` 是 `status=draft`", text("cs-issue/SKILL.md"))
        self.assertIn("`analysis.md` 已 `status=confirmed`", text("cs-issue/SKILL.md"))
        self.assertIn("退回 `cs-feat-plan` 生成", text("cs-feat-impl/SKILL.md"))
        self.assertNotIn("退回 `cs-feat-design` 生成", text("cs-feat-impl/SKILL.md"))
        self.assertIn("`status: completed`", text("cs-issue-fix/SKILL.md"))
        self.assertIn("status: completed", text("cs-issue-fix/reference.md"))

    def test_bridge_task_contract_stays_minimal_and_non_authoritative(self):
        content = text(".codestable/reference/workflow-contract-authority.md")
        self.assertIn("最小字段只保留 `id`、`status`、`canonical_path`、`canonical_kind`", content)
        self.assertIn("不能镜像或判定 canonical 阶段", content)

    def test_feature_design_does_not_require_plan_stage_checklist(self):
        content = text("cs-feat-design/SKILL.md")
        self.assertNotIn("`{slug}-checklist.yaml` 已落盘并通过", content)
        self.assertIn("不要求 plan/checklist", content)


class SkillRouteTargetTests(unittest.TestCase):
    def write(self, root: Path, relative: str, content: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def check_routes(self, root: Path):
        report = CONTRACT_CHECKER["Report"](root, 500)
        CONTRACT_CHECKER["check_skill_routes"](root, report)
        return report

    def test_repository_route_targets_exist(self):
        report = self.check_routes(REPO_ROOT)
        self.assertEqual([], [finding.to_dict() for finding in report.findings])

    def test_missing_target_in_each_routing_doc_is_rejected(self):
        paths = (
            "cs/SKILL.md", "cs-feat/SKILL.md", "cs-issue/SKILL.md",
            "cs-onboard/reference/system-overview.md", ".codestable/reference/system-overview.md",
        )
        for relative in paths:
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.write(root, "cs/SKILL.md", "---\nname: cs\n---\n")
                self.write(root, relative, "| 场景 | `cs-nonexistent` |\n")
                report = self.check_routes(root)
                self.assertEqual(["skill_route_missing"], [finding.rule for finding in report.findings])
                self.assertEqual(f"{relative}:1", report.findings[0].path)

    def test_matching_target_passes_but_mismatched_name_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write(root, "cs/SKILL.md", "| 任务 | `cs-example` / `cs-other` |\n")
            self.write(root, "cs-example/SKILL.md", "---\nname: cs-example\n---\n")
            self.write(root, "cs-other/SKILL.md", "---\nname: cs-other\n---\n")
            self.assertTrue(self.check_routes(root).ok)
            self.write(root, "cs-example/SKILL.md", "---\nname: wrong-name\n---\n")
            report = self.check_routes(root)
        self.assertEqual(["skill_route_name"], [finding.rule for finding in report.findings])

    def test_missing_frontmatter_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write(root, "cs/SKILL.md", "| 任务 | `cs-example` |\n")
            self.write(root, "cs-example/SKILL.md", "# Missing frontmatter\n")
            report = self.check_routes(root)
        self.assertEqual(["skill_route_name"], [finding.rule for finding in report.findings])

    def test_examples_and_prose_are_not_routing_targets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write(root, "cs/SKILL.md", "`cs-prose-only`\n\n```markdown\n| 示例 | `cs-example-only` |\n```\n")
            self.assertTrue(self.check_routes(root).ok)

    def test_consumer_project_does_not_require_skill_source_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write(root, ".codestable/reference/system-overview.md", "| 新功能 | `cs-feat` |\n")
            self.assertTrue(self.check_routes(root).ok)

    def test_cli_returns_failure_for_missing_route_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write(root, "cs-issue/SKILL.md", "| 问题 | `cs-missing` |\n")
            for relative in ("cs-onboard/reference/shared-asset-manifest.yaml", ".codestable/reference/shared-asset-manifest.yaml"):
                self.write(root, relative, "references: []\ntools: []\n")
            result = subprocess.run(
                [sys.executable, str(CONTRACT_CHECK_PATH), "--repo-root", str(root), "--json"],
                capture_output=True, text=True, check=False,
            )
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual(["skill_route_missing"], [finding["rule"] for finding in json.loads(result.stdout)["findings"]])


if __name__ == "__main__":
    unittest.main()
