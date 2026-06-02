---
doc_type: audit-finding
audit: 2026-06-02-skill-workflow
finding_id: "arch-drift-02"
nature: arch-drift
severity: P1
confidence: high
suggested_action: cs-refactor
status: open
---

# Finding 02：cs-feat 入口仍把 hybrid plan 说成“可附带”，与共享约定中的硬门槛冲突

## 速答

hybrid 流程已经把 `plan.md` 提升为正式产物和硬门槛，但 `cs-feat` 这个总入口仍用“hybrid 可附带 plan.md / 可附带 plan”描述它，口径偏松，容易误导后续维护者和用户。

## 关键证据

- `.codestable/reference/shared-conventions.md:128` — 明确规定：hybrid feature 一旦采用 hybrid 口径，就必须存在真实 `plan.md`，缺失时 implement / acceptance / workflow-check 都应失败。
- `.codestable/reference/shared-conventions.md:145` — 明确写了“hybrid feature 先生成 plan，再从 design + plan 抽 steps + checks”。
- `/Users/kong/.claude/skills/cs-feat-impl/SKILL.md:69` — implement 阶段已把 plan 定义为 hybrid 的“必须存在的真实输入”。
- `/Users/kong/.claude/skills/cs-feat/SKILL.md:31` — 文件树仍写 `{slug}-plan.md ← hybrid 可选执行计划`。
- `/Users/kong/.claude/skills/cs-feat/SKILL.md:49` — 阶段表仍写“design.md + checklist.yaml（hybrid 可附带 plan.md）”。

## 影响

`cs-feat` 是用户最容易先读到的入口技能。这里的措辞如果比共享约定更松，会直接制造错误心智模型：用户和维护者可能以为 hybrid 只是“可以多一份 plan 的增强版”，而不是“有 workflow marker 就必须带真实 plan 的协议分支”。这会造成路由误判、实现阶段被动失败，以及文档之间的二次同步成本。

## 修复方向

统一把入口口径改成：legacy 是 `design + checklist + acceptance`，hybrid 是 `design + plan + checklist + acceptance`；若保留“可选”字样，只能用于“是否选择 hybrid”，不能用于“进入 hybrid 后 plan 是否可缺”。

## 建议动作

`cs-refactor`，因为这是文档与技能入口层的职责重构和口径收敛，不是单点 bug 修补。