---
doc_type: decision
category: convention
date: 2026-06-02
slug: hybrid-as-default-feature-mode
status: active
area: codestable-workflow
tags: [legacy, hybrid, feature, workflow, migration]
---

## 背景

当前 NewCodeStable 的 feature 流程允许两种口径并存：

- legacy：`design + checklist + acceptance`
- hybrid：`design + plan + checklist + acceptance`

这套并存策略在过渡期是有价值的，因为历史 feature 不需要被批量回填 `plan.md`，现有仓库也能平滑迁移。

但项目方向已经进一步明确：legacy 不应长期作为与 hybrid 对等的默认路径，而应逐步退化为**历史兼容口径**；新 feature 的默认标准应向 hybrid 收敛。

## 决定

项目的 feature 工作流采用下面的长期方向：

1. **legacy feature 暂时保留，但仅作为历史兼容口径**
2. **hybrid feature 作为新 feature 的默认目标口径**
3. **不批量回填历史 feature 的 `plan.md`**
4. **重开旧 feature 时优先升级到 hybrid**
5. **新 feature 默认优先 hybrid，只有明确命中例外时才不生成 `plan.md`**

这里的“例外”应当是显式而克制的，例如：
- fastforward 小改动
- 范围极小、checklist 已足够表达推进节奏的 feature
- 其他经明确判断“不值得单独写 plan”的特例

## 理由

- legacy 与 hybrid 长期完全对等，会让顶层流程、技能文案和校验边界一直处于“双默认”状态，后续维护成本高
- hybrid 已经提供更完整的执行路径表达能力：design 决定范围，plan 决定步骤，checklist 承担状态，因此更适合作为新 feature 的默认标准
- 不批量回填历史 feature，能避免为了“整齐”付出高成本；把迁移重点放在**新 feature 和重开的旧 feature**，更符合实际演进路径

## 考虑过的替代方案

### 长期双轨并存，把 legacy 和 hybrid 都视为正式默认路径

未采用。因为这会让“什么时候需要 plan、什么时候可以没有 plan”长期保持模糊，技能文案、总览入口和校验器边界都更容易继续漂移。

### 立即强制所有历史 feature 回填 `plan.md`

未采用。因为这会把大量存量目录卷入一次性清理，成本高且收益低，也违背当前 forward-only / minimal backfill 的迁移原则。

## 后果

- 后续应逐步把顶层技能、shared conventions、overview、architecture 的语气从“legacy / hybrid 并存且都推荐”收紧成“legacy 兼容保留、hybrid 默认推荐”
- workflow-check 的适用边界应继续保持：历史未重开的 legacy feature 不因缺 `plan.md` 被直接判错；但新 feature 和重开的 feature 应按新规则检查
- 以后如果要继续收紧口径（例如“除 fastforward 外新 feature 全部强制 hybrid”），应再新增或 supersede 一条 decision，而不是隐式改技能文案

## 相关文档

- `.codestable/reference/shared-conventions.md`
- `.codestable/reference/system-overview.md`
- `.codestable/architecture/ARCHITECTURE.md`
- `.codestable/compound/2026-06-02-decision-hybrid-plan-presence-boundary.md`
- `.codestable/compound/2026-06-02-decision-expose-workflow-gates-at-top-level.md`
