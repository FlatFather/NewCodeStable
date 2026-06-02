---
doc_type: decision
category: convention
date: 2026-06-02
slug: feature-intent-artifact-boundary
status: active
area: codestable-workflow
tags: [intent, feature, workflow, shared-conventions, routing]
---

## 背景

在 NewCodeStable 的 feature 流程里，`{slug}-intent.md` 已经被 `cs-feat` 和 `cs-feat-design` 当成真实入口使用：用户可以通过初始化模式先创建一份半成品草稿，后续再由 design 阶段读取并起正式方案。

但在这次收敛之前，`intent.md` 的身份只散落在入口技能说明里，没有进入 `.codestable/reference/shared-conventions.md` 的权威目录结构与产物职责边界。结果是同一个对象同时存在“入口技能实际依赖”和“共享约定未登记”两套口径，增加了后续维护和同步成本。

## 决定

将 `{slug}-intent.md` 定义为 **feature 的可选前置草稿（pre-design seed）**。

这条决定包含三层口径：

1. **共享身份**：`intent.md` 的权威身份由 `.codestable/reference/shared-conventions.md` 定义。
2. **路由职责**：`cs-feat` 只负责判断什么时候走 brainstorm、什么时候走 intent 初始化模式、什么时候直接进入 design。
3. **实现细节职责**：`cs-feat-design` 负责初始化模式的具体动作（建目录、写空 intent 草稿、停在 intent）以及正式起草时如何读取它，不再越权定义它的共享身份。

同时明确：
- `intent.md` 是 design 前置草稿，不是 design / plan / checklist / acceptance 的同级主产物
- 它供 design 阶段读取，不参与 implement / acceptance 生命周期
- 它不替代 brainstorm note，二者继续保留各自分工：brainstorm = AI 对话收敛，intent = 用户离线半成品草稿

## 理由

- 既然 `intent.md` 已经参与 feature 入口和初始化模式，就不应该继续停留在“局部实现细节”状态，需要进入共享口径
- 让 shared conventions 负责产物身份、让 `cs-feat` 负责路由、让 `cs-feat-design` 负责初始化细节，可以减少重复定义和后续漂移
- 保留 intent 与 brainstorm 的双入口，有利于同时支持“AI 帮用户聊清楚”和“用户先自己写半成品”两种收敛方式

## 考虑过的替代方案

### 把 `intent.md` 降级成 `cs-feat-design` 的局部输入

未采用。因为你已经明确不希望把 intent 降级成局部输入；而且它目前已经被 feature 入口技能显式路由和展示，继续把它留在共享约定之外，会保留双真相源问题。

## 后果

- 后续维护 feature 流程时，凡是涉及 `intent.md` 身份的口径修改，应先改 `.codestable/reference/shared-conventions.md`
- `cs-feat` 后续不应再扩张成 intent 生命周期的第二权威来源，只保留路由判断所需的最小说明
- `cs-feat-design` 可以继续演进初始化模式的操作细节，但若要改变 intent 的身份或生命周期，应回到共享约定或新 decision 处理

## 相关文档

- `.codestable/reference/shared-conventions.md`
- `/Users/kong/.claude/skills/cs-feat/SKILL.md`
- `/Users/kong/.claude/skills/cs-feat-design/SKILL.md`
- `.codestable/refactors/2026-06-02-intent-artifact-boundary/intent-artifact-boundary-refactor-design.md`
