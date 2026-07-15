"""Text-level checks for the Markdown-defined routing protocol."""

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class SkillRoutingContractTests(unittest.TestCase):
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

    def test_feature_design_does_not_require_plan_stage_checklist(self):
        content = text("cs-feat-design/SKILL.md")
        self.assertNotIn("`{slug}-checklist.yaml` 已落盘并通过", content)
        self.assertIn("不要求 plan/checklist", content)


if __name__ == "__main__":
    unittest.main()
