---
doc_type: decision
category: convention
date: 2026-06-02
slug: hybrid-plan-presence-boundary
status: active
area: codestable-workflow
tags: [hybrid, feature-plan, workflow, plan-presence, checklist]
---

## 背景

在 NewCodeStable 的 feature 流程里，hybrid 口径已经通过 shared conventions、implement、acceptance、workflow-check 和真实样板逐步收紧成完整链路：`design → plan → checklist → implement → acceptance`。

但在这次收敛之前，入口与总览层仍残留弱门槛表达，例如把 `{slug}-plan.md` 写成“可选执行计划”或“预留 / 衔接 plan”。这会让读者误以为 hybrid 只是“可以多一份 plan”，而不是一旦采用 hybrid 口径就必须存在真实 `plan.md`。

## 决定

对于 feature 流程，必须明确区分两层判断：

1. **是否选择 hybrid**：这是 feature 流程的一层分支判断。
2. **一旦采用 hybrid 口径**：`plan.md` 就是必备产物与必备输入，不得缺失。

这条决定要求三层口径同时一致：

- **共享约定层**：`.codestable/reference/shared-conventions.md` 是关于 `plan presence rule` 的权威定义处。
- **入口 / 阶段技能层**：
  - `cs-feat` 必须把“是否选 hybrid”与“选中 hybrid 后 plan 必须存在”分开表达
  - `cs-feat-design` 必须明确 hybrid 下的生成顺序是 `approved design → plan → checklist`
- **总览层**：`system-overview.md` 和 `ARCHITECTURE.md` 只补摘要句，说明 hybrid 的硬门槛，但不复制 shared conventions 的整套协议正文。

## 理由

- hybrid 流程已经不再只是“可选增强”，而是有真实校验器和真实样板支撑的协议分支，入口文案不能再保留弱门槛表达
- 把“是否选 hybrid”和“进入 hybrid 后 plan 是否必备”拆成两层判断，能避免误把 legacy 路径也收紧成默认带 plan
- 让 shared conventions 负责协议正文、让技能文档负责入口与阶段动作、让 overview / architecture 只保留摘要，有助于减少重复定义和后续漂移

## 考虑过的替代方案

### 保留“可选 plan”表达，只靠 shared conventions 兜底

未采用。因为入口文案是用户和维护者最容易先读到的地方；如果入口仍保留弱门槛，后续 implement / acceptance / workflow-check 的强门槛只会表现成“后面突然失败”，而不是前面就建立正确心智模型。

## 后果

- 后续凡是修改 hybrid / legacy 分支边界的文案，必须先检查是否同时守住这两层判断
- `cs-feat` 不应再把 `{slug}-plan.md` 描述成“hybrid 可附带产物”
- `cs-feat-design` 不应再用“预留 / 衔接 plan”这类能被理解成占位文件也可以的词
- `system-overview.md` 与 `ARCHITECTURE.md` 可以保留门槛摘要，但不应长成 shared conventions 的第二套详细协议

## 相关文档

- `.codestable/reference/shared-conventions.md`
- `.codestable/reference/system-overview.md`
- `.codestable/architecture/ARCHITECTURE.md`
- `cs-feat/SKILL.md`
- `cs-feat-design/SKILL.md`
- `.codestable/refactors/2026-06-02-hybrid-plan-presence-wording/hybrid-plan-presence-wording-refactor-design.md`
