# NewCodeStable 架构总入口

> 状态：骨架（待填充）
> 创建日期：2026-06-01

## 1. 项目简介

NewCodeStable 旨在演进为一个融合式工作流体系：保留 CodeStable 的 `.codestable/` 信息架构，同时吸收 CCG 在实施计划与执行分解上的优势。

## 2. 核心概念 / 术语表

- **feature-design**：单条 feature 的范围、术语、成功标准、关键决策与流程级约束的唯一方案源。
- **feature-plan**：hybrid feature 的详细执行步骤正文，承接已批准 design，只展开推进顺序、退出信号、验证路径与风险缓解。frontmatter 固定为 `doc_type / feature / design / status`，正文固定包含“执行目标 / 分步计划 / 风险与回退 / 与 checklist 的映射”。
- **legacy feature**：沿用 `design + checklist + acceptance` 的既有 feature 口径，不要求历史目录回填 plan。
- **hybrid feature**：采用 `design + plan + checklist + acceptance` 的增强口径；design 是 scope source，plan 是 step source，checklist 是 status carrier。

## 3. 子系统 / 模块索引

- **工作流共享契约层**：由 `.codestable/reference/shared-conventions.md` 承载跨技能共享口径，定义 feature、roadmap、requirement、architecture 等项目级产物的结构与职责边界。
- **feature 流程**：默认主线是 `design → checklist → implement → acceptance`；复杂 feature 可以在 design 之后引入 `plan` 层，形成 `design → plan → checklist → implement → acceptance` 的 hybrid 流程。hybrid 口径下的生成顺序固定为 approved design → plan → checklist。

## 4. 关键架构决定

## 5. 已知约束 / 硬边界

- design 永远是 feature 范围与约束的唯一方案源；plan、checklist、acceptance 都不能越权改 scope。
- hybrid feature 一旦存在 `plan.md`，implement 与 acceptance 都必须把它当作输入之一；legacy feature 则继续按 `design + checklist` 工作。
- checklist 只承载机器可读状态；hybrid feature 的 detailed step narrative 固定写在 `plan.md`。
- roadmap、requirement、architecture 的写回责任仍在 acceptance，不前移到 plan。
