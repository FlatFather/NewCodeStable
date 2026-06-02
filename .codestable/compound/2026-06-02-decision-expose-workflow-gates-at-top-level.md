---
doc_type: decision
category: convention
date: 2026-06-02
slug: expose-workflow-gates-at-top-level
status: active
area: codestable-workflow
tags: [workflow, routing, top-level, hybrid, plan]
---

## 背景

在 NewCodeStable 的 feature 流程里，某些关键规则已经在子技能内部成立，但用户未必会直接从子技能开始理解流程。尤其是当用户只从顶层链路去看 `cs-feat → cs-feat-design → cs-feat-impl → cs-feat-accept` 时，如果关键门槛没有在入口、阶段产出或路由表中显式出现，就容易建立错误心智模型。

这次 hybrid feature 的 `plan.md` 就暴露了这个问题：`cs-feat-design` 内部其实已经定义了真实顺序 `approved design → plan → checklist`，但顶层链路没有把“plan 在进入实现前生成”这件事显式说出来，导致用户误以为这条流程中不会生成 `plan.md`。

## 决定

在 feature 工作流里，凡是决定用户能否进入下一阶段的**硬门槛 / 必备产物**，不能只藏在子技能内部，必须同时暴露在以下三个层次：

1. **顶层入口**：让用户在总览流程中就能看到关键关口的存在
2. **阶段产出**：让用户知道某个产物是在什么阶段生成的
3. **路由表**：让用户知道该产物缺失时不能继续往下走

对 hybrid feature，这条规则的具体表现是：

- 是否采用 hybrid，是一层分支选择
- 一旦采用 hybrid 口径，`plan.md` 就必须在进入实现前由 design 阶段生成
- 若 `plan.md` / checklist 还没落齐，就不应直接进入 `cs-feat-impl`

## 理由

- 用户最常先接触的是顶层入口和阶段链路，而不是某个子技能内部正文；如果关键门槛只存在于子技能内部，用户会在更早层级形成错误理解
- 当“规则已经存在但用户仍然误解流程”时，优先修复的通常不是底层协议，而是**顶层可见性**
- 把关键门槛同时暴露在入口、阶段产出和路由表中，可以减少“后面突然失败”的割裂感，让用户在进入下一阶段前就知道缺了什么

## 考虑过的替代方案

### 只在 shared conventions 或子技能内部保留规则，不补顶层链路

未采用。因为这会继续依赖用户自行从多份底层文档中拼出完整流程；而在真实使用里，用户常常是先看顶层入口和阶段路由，再决定往哪走。

## 后果

- 以后只要某条规则会决定“能不能进入下一阶段”，就应检查它是否已经出现在：顶层入口、阶段产出、路由表
- 新增 workflow 产物时，不应只在 shared conventions 或单个子技能里登记，还应检查顶层链路是否需要同步暴露该关口
- 顶层文档不需要复制 shared conventions 的整套协议，但必须保留足够建立正确心智模型的摘要句

## 相关文档

- `cs/SKILL.md`
- `cs-feat/SKILL.md`
- `cs-feat-design/SKILL.md`
- `.codestable/reference/shared-conventions.md`
- `.codestable/reference/system-overview.md`
- `.codestable/compound/2026-06-02-learning-expose-critical-workflow-gates-at-top-level.md`
