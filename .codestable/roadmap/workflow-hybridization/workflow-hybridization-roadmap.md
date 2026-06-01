---
doc_type: roadmap
slug: workflow-hybridization
status: active
created: 2026-06-01
last_reviewed: 2026-06-01
tags: [codestable, ccg, workflow, planning, spec]
related_requirements: []
related_architecture: []
---

# NewCodeStable 工作流融合路线图

## 1. 背景

NewCodeStable 当前是从 CodeStable fork 而来，已经接入了 `.codestable/` 骨架，但还没有把“怎么把 CodeStable 和 CCG 的优点融合起来”固化成可执行的规划层文档。

用户已经明确了目标方向：保留 CodeStable 的 `.codestable/` 目录结构与以软件实体为中心的组织方式，同时吸收 CCG 在实施计划上的优势，尤其是把“做什么”拆成更易执行、更易跟踪的分步骤计划。参考样本显示，两边各有明显长处：CodeStable 风格的 design 文档在需求摘要、术语约定、决策与约束上足够完整，而 CCG 风格的 `plan.md` 在步骤拆解、验证路径、执行顺序上更适合直接落地。

因此，这份 roadmap 的目标不是新增一个孤立 feature，而是规划 NewCodeStable 作为融合式工作流体系的演进路径：哪些共享约定需要升级、哪些文档职责需要重新切分、feature 流程如何衔接新的执行计划层，以及如何让后续每条 feature 都能稳定复用这套新范式。

## 2. 范围与明确不做

### 本 roadmap 覆盖
- 定义 NewCodeStable 的融合目标与边界
- 规划 `.codestable/` 体系中 design / checklist / execution plan / acceptance 之间的新职责分工
- 规划 roadmap、feature、shared conventions 之间的接口契约
- 拆出后续可独立推进的子 feature 种子

### 明确不做
- 不在本 roadmap 里直接修改所有现有 `cs-*` 技能文档或代码
- 不把 CCG 的整套目录结构（如 `.ccg/tasks/`）原样搬进 `.codestable/`
- 不在本 roadmap 阶段决定所有具体文件内容措辞；这里只定结构、协议和拆解
- 不顺手重写 requirements / architecture / 其他现有 feature 文档
- 不处理“多模型协作流程”本身；本次重点是 spec 与执行规划的产物体系
- 不引入第二套并行真相源，避免 `.codestable` 与 `.ccg` 同时成为主工作流

## 3. 模块拆分（概设）

```text
workflow-hybridization
├── Module A: Spec Information Architecture
├── Module B: Execution Planning Layer
├── Module C: Workflow State & Handoff Protocol
└── Module D: Migration & Adoption Path
```

### 模块 A · Spec Information Architecture
- **职责**：定义 `.codestable/` 下 design、roadmap、checklist、acceptance 各自该承载什么信息，避免“需求说明”和“执行步骤”混写或缺位。
- **承载的子 feature**：spec-structure-contract, feature-design-template-upgrade
- **触碰的现有代码 / 模块**：`.codestable/reference/shared-conventions.md`、相关 `cs-*` 技能说明、模板文件

### 模块 B · Execution Planning Layer
- **职责**：引入比现有 checklist 更强的“执行步骤”表达能力，让 feature 在进入实现前就有一份可执行、可验证、可逐步推进的计划产物。
- **承载的子 feature**：execution-plan-artifact, plan-validation-rules
- **触碰的现有代码 / 模块**：`cs-feat-design`、`cs-feat-impl`、共享 YAML/Markdown 模板

### 模块 C · Workflow State & Handoff Protocol
- **职责**：定义 roadmap → feature-design → feature-impl → feature-acceptance 的交接协议，确保 design、plan、checklist、items.yaml 各自职责清晰且状态联动一致。
- **承载的子 feature**：feature-handoff-contract, acceptance-writeback-contract
- **触碰的现有代码 / 模块**：`.codestable/reference/shared-conventions.md`、`cs-roadmap`、`cs-feat-design`、`cs-feat-accept`

### 模块 D · Migration & Adoption Path
- **职责**：定义已有 CodeStable 仓库如何逐步采用新融合方式，避免一次性推翻旧设计；给出兼容期策略与最小落地顺序。
- **承载的子 feature**：migration-guidance, first-hybrid-example
- **触碰的现有代码 / 模块**：reference 文档、guide 文档、示例 feature 产物

## 4. 模块间接口契约 / 共享协议（架构层详设）

### 4.1 Spec Artifact Responsibility Contract

**方向**：Module A → Module B / Module C  
**形式**：共享文档协议

**契约**：

```text
Roadmap:
  负责“大需求拆解、模块边界、跨 feature 接口契约、子 feature 列表”
  不负责“单条 feature 的详细实现步骤”

Feature Design:
  负责“需求摘要、术语约定、关键决策、成功标准、挂载点、边界”
  不负责“逐步实施顺序的细颗粒执行说明”

Execution Plan:
  负责“单条 feature 的分步骤执行方案、每步退出信号、验证命令、风险与缓解”
  不重复定义 design 已拍板的需求和约束

Checklist:
  负责“执行状态追踪与验收勾选”
  不替代 execution plan 的文字说明

Acceptance:
  负责“对照 design + plan + checklist 做结果核验，并回写 roadmap / architecture / requirements 所需状态”
```

**约束**：
- 单条 feature 只能有一个 design 真相源
- 单条 feature 只能有一个 execution plan 真相源
- execution plan 必须引用 design，不允许脱离 design 独立拍板范围
- checklist 是状态载体，不是详细说明书

### 4.2 Feature Design → Execution Plan Handoff Contract

**方向**：Module A → Module B  
**形式**：frontmatter + 文件命名协议

**契约**：

```yaml
feature_design_frontmatter:
  feature: YYYY-MM-DD-{slug}
  status: approved
  roadmap: {roadmap-slug} | null
  roadmap_item: {item-slug} | null

execution_plan_file:
  path: .codestable/features/YYYY-MM-DD-{slug}/{slug}-plan.md

execution_plan_frontmatter:
  doc_type: feature-plan
  feature: YYYY-MM-DD-{slug}
  design: {slug}-design.md
  status: draft | approved | superseded
```

**执行步骤结构**：

```yaml
steps:
  - step: 1
    title: string
    goal: string
    touches: [path-or-module]
    exit_signal: string
    verification: [command-or-check]
```

**约束**：
- 只有 design `status: approved` 后才能生成正式 execution plan
- plan 中每一步必须有 exit signal
- plan 中每一步必须指向 design 中已存在的范围与约束，不能自行扩 scope
- 一个 feature 若走标准流程，plan 与 checklist 必须同时存在；ff 通道除外

### 4.3 Execution Plan → Checklist Contract

**方向**：Module B → Module C  
**形式**：字段映射协议

**契约**：

```text
plan.step[n] <-> checklist.steps[n]

plan.step.title        -> checklist.steps[n].title
plan.step.exit_signal  -> checklist.steps[n].done_definition
plan.step.verification -> checklist.steps[n].checks
```

**约束**：
- checklist 中的步骤顺序必须与 plan 对齐
- 若 implement 阶段要新增或拆分步骤，必须同时更新 plan 与 checklist
- checklist 可以更短，但不能包含 plan 中不存在的“幽灵步骤”

### 4.4 Roadmap Item → Feature Seed Contract

**方向**：Module C → Module A / Module B  
**形式**：roadmap items.yaml + feature frontmatter 协议

**契约**：

```yaml
roadmap_item:
  slug: string
  description: string
  depends_on: [slug]
  status: planned | in-progress | done | dropped
  feature: YYYY-MM-DD-{slug} | null
  minimal_loop: boolean
  notes: string | null
```

启动 feature 时：

```yaml
feature_design_frontmatter:
  roadmap: workflow-hybridization
  roadmap_item: {item-slug}
```

**约束**：
- roadmap item 只定义“做哪条 feature”，不承载单 feature 详细执行计划
- feature-design 启动时将 roadmap item 标记为 `in-progress`
- acceptance 完成时将 roadmap item 标记为 `done`
- dropped 保留历史，不删除

### 4.5 Migration Compatibility Contract

**方向**：Module D → 全模块  
**形式**：兼容策略协议

**契约**：

```text
Legacy Feature (old style):
  design + checklist + acceptance

Hybrid Feature (new style):
  design + plan + checklist + acceptance

Compatibility Rule:
  旧 feature 不强制回填 plan
  新 feature 若命中“复杂实现 / 多阶段执行 / 高验证需求”，必须使用 plan
```

**约束**：
- 不批量回填历史 feature 的 plan 文档
- 新规范先从新 feature 开始采用
- 是否要求“所有新 feature 必带 plan”，由后续 decision 文档拍板

### 4.x 共享数据结构 / 状态

```yaml
hybrid_feature_artifacts:
  design:
    purpose: scope_and_decisions
  plan:
    purpose: execution_steps_and_validation
  checklist:
    purpose: execution_tracking
  acceptance:
    purpose: result_verification_and_writeback

roadmap_item_status_flow:
  planned -> in-progress -> done
  planned -> dropped
```

## 5. 子 feature 清单

1. **spec-structure-contract** — 明确 design / plan / checklist / acceptance 的职责边界，并更新共享约定
   - 所属模块：Spec Information Architecture
   - 依赖：无
   - 状态：done
   - 对应 feature：2026-06-01-spec-structure-contract
   - 备注：这是后续所有融合动作的基础

2. **execution-plan-artifact** — 为标准 feature 流程新增 `feature-plan` 产物与模板
   - 所属模块：Execution Planning Layer
   - 依赖：spec-structure-contract
   - 状态：planned
   - 对应 feature：未启动
   - 备注：核心目标是把 CCG `plan.md` 的分步优势引入 `.codestable/features/`

3. **feature-handoff-contract** — 定义 roadmap、design、plan、checklist、acceptance 的状态交接与 frontmatter 协议
   - 所属模块：Workflow State & Handoff Protocol
   - 依赖：spec-structure-contract, execution-plan-artifact
   - 状态：planned
   - 对应 feature：未启动
   - 备注：避免 plan 成为脱离主流程的旁路产物

4. **plan-validation-rules** — 扩展校验脚本或规则，验证 plan/checklist/roadmap item 的一致性
   - 所属模块：Execution Planning Layer / Workflow State & Handoff Protocol
   - 依赖：feature-handoff-contract
   - 状态：planned
   - 对应 feature：未启动
   - 备注：让新规范可检查而不是只靠人工记忆

5. **migration-guidance** — 为已有仓库和老 feature 定义新旧规范并存的采用策略
   - 所属模块：Migration & Adoption Path
   - 依赖：feature-handoff-contract
   - 状态：planned
   - 对应 feature：未启动
   - 备注：避免“一刀切”迁移

6. **first-hybrid-example** — 用一条真实 feature 走完整 hybrid 流程，产出示例
   - 所属模块：Migration & Adoption Path
   - 依赖：plan-validation-rules, migration-guidance
   - 状态：planned
   - 对应 feature：未启动
   - 备注：作为后续技能与文档的演示样板

**最小闭环**：第 2 条 `execution-plan-artifact` 做完后，系统就能对“新 feature 如何同时拥有 design + 可执行 plan + checklist”给出最窄端到端路径；但从依赖上看，真正的起点仍是第 1 条 `spec-structure-contract`。

## 6. 排期思路

这份 roadmap 先按“定义规则，再引入产物，再打通交接，最后给迁移路径和示例”推进。

第一阶段必须先把职责边界讲清，否则 execution plan 很容易和 design 重复，或者反过来把 design 空心化。第二阶段再把 plan 产物正式引进 feature 目录，让 CCG 的执行力优势有固定落点。第三阶段处理状态交接和校验规则，避免 roadmap、feature、acceptance 各写各的。最后再补迁移说明和真实样例，降低存量项目采用成本。

## 7. 观察项

- 当前 `.codestable/reference/shared-conventions.md` 里已经详细定义了 checklist 生命周期；若引入 plan，需要避免与现有 checklist 描述冲突
- 当前 `system-overview.md` 里仍把 feature 主流程描述为 `design → implement → acceptance`，如果 hybrid 方案通过，后续需要补上 plan 层
- 是否要求“所有标准 feature 都必须有 plan”，还是只在复杂 feature 中启用，后续需要单独拍板
- `verify-module` 当前更偏源码模块检查，对 `.codestable` 工作流目录会误报，后续如果把 roadmap / feature 目录当一等产物管理，可能需要新增专门校验器
