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
- **roadmap item**：roadmap items.yaml 中的一条子 feature 记录，承载 slug、依赖、状态与 feature 目录名。
- **feature directory binding**：`YYYY-MM-DD-{slug}` 目录名是 roadmap item、design、plan、checklist、acceptance 之间的唯一绑定键。
- **plan presence rule**：legacy feature 可没有 `plan.md`；hybrid feature 一旦由 design 采用 hybrid 口径，就必须存在真实 `plan.md`。
- **workflow-check**：工作流协议校验模式，读取 feature 目录与 roadmap items.yaml，检查 frontmatter、绑定关系、plan presence 与 step alignment。
- **legacy repository**：已接入 `.codestable/`，但历史 feature 仍大量停留在 legacy 口径的仓库。
- **forward-only adoption**：新规范只约束新 feature 或明确重开的 feature，不追溯回填全部历史产物。
- **minimal backfill**：历史 feature 重开时只补继续走流程所需的最小字段和文件。

## 3. 子系统 / 模块索引

- **工作流共享契约层**：由 `.codestable/reference/shared-conventions.md` 承载跨技能共享口径，定义 feature、roadmap、requirement、architecture 等项目级产物的结构与职责边界。
- **feature 流程**：默认主线是 `design → checklist → implement → acceptance`；复杂 feature 可以在 design 之后引入 `plan` 层，形成 `design → plan → checklist → implement → acceptance` 的 hybrid 流程。hybrid 口径下的生成顺序固定为 approved design → plan → checklist；一旦采用 hybrid 口径，`plan.md` 就是必备产物。
- **workflow-check 校验层**：由 `.codestable/tools/validate-yaml.py --workflow-check` 承担，对 feature 目录与 roadmap items 的协议一致性做只读预检查。
- **黄金样板层**：`.codestable/features/2026-06-02-first-hybrid-example/` 是当前仓库的首条完整 hybrid 工作流样板，用于给用户和后续 feature 作者直接参考。

## 4. 关键架构决定

- **feature intent 边界**：`{slug}-intent.md` 是 feature 的可选前置草稿（pre-design seed），共享身份由 `.codestable/reference/shared-conventions.md` 定义；`cs-feat` 只负责 intent/brainstorm 的路由判断；`cs-feat-design` 负责初始化模式的草稿骨架与读取。详见 `.codestable/compound/2026-06-02-decision-feature-intent-artifact-boundary.md`。

## 5. 已知约束 / 硬边界

- design 永远是 feature 范围与约束的唯一方案源；plan、checklist、acceptance 都不能越权改 scope。
- hybrid feature 一旦采用 hybrid 口径，`plan.md` 就是必备输入；implement 与 acceptance 都必须把它当作输入之一；legacy feature 则继续按 `design + checklist` 工作。
- checklist 只承载机器可读状态；hybrid feature 的 detailed step narrative 固定写在 `plan.md`。
- roadmap 状态只允许 design 写 `in-progress`、acceptance 写 `done`；plan 不单独维护 progress 状态。
- workflow-check 只报告协议错误，不自动改写文档。
- 历史 feature 默认保持当时口径有效；只有新 feature 或显式重开的 feature 才要求补 `workflow` / `plan.md`。
- roadmap、requirement、architecture 的写回责任仍在 acceptance，不前移到 plan。
