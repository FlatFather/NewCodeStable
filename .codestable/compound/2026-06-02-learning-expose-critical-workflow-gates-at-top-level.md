---
doc_type: learning
track: knowledge
date: 2026-06-02
slug: expose-critical-workflow-gates-at-top-level
component: codestable-workflow
tags: [workflow, hybrid, plan, routing, top-level-visibility]
---

## 背景

在 NewCodeStable 的 hybrid feature 流程里，`cs-feat-design` 内部其实已经定义了真实顺序：`approved design → plan → checklist`。但用户如果只沿着顶层链路去理解：`cs-feat → cs-feat-design → cs-feat-impl → cs-feat-accept`，会误以为中间不会生成 `plan.md`，因为顶层入口、阶段产出和路由表没有把这个关口显式暴露出来。

## 指导原则

当某条 workflow 规则已经在子技能内部成立，但它决定了用户是否能正确进入下一阶段时，必须把这个关口显式暴露在顶层链路里。

对 hybrid feature 来说，这条规则就是：一旦采用 hybrid 口径，`plan.md` 必须在进入实现前由 design 阶段生成。

## 为什么重要

如果顶层入口不显式暴露关键关口，用户就会建立错误心智模型：

- 以为规则不存在
- 以为中间某个产物不会生成
- 以为后续阶段“突然失败”是实现问题，而不是前一阶段的流程门槛没有被看见

这类问题不应该优先靠补底层规则解决，因为底层规则已经存在；真正缺的是**顶层可见性**。

## 何时适用

适用于所有分阶段工作流，尤其是满足下面两个条件时：

1. 某个阶段内部已经有明确的硬门槛或必备产物
2. 用户能从更上层入口直接决定是否进入下一阶段

这时就应该检查：

- 顶层入口有没有把这个门槛说出来
- 阶段产出有没有把这个产物写出来
- 路由表有没有把“缺这个产物时不能往下走”写出来

## 示例

这次 hybrid workflow 的修复就是一个例子：

- `cs-feat-design` 内部已经知道 hybrid 下要走 `design → plan → checklist`
- 但 `cs-feat` 的阶段产出和路由表没有明确写“hybrid 时 plan 在本阶段生成，未落齐不能进 impl”
- 修复时优先补的是顶层链路可见性，而不是继续往 shared conventions 或底层实现里堆规则
