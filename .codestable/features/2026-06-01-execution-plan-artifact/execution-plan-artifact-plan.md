---
doc_type: feature-plan
feature: 2026-06-01-execution-plan-artifact
design: execution-plan-artifact-design.md
status: approved
---

# execution-plan-artifact execution plan

## 1. 执行目标

这份 plan 只承接已批准的 design，回答：如何把 `feature-plan` 从抽象术语落成真实产物、模板和消费链路，并且不把 detailed execution narrative 再塞回 design 或 checklist。

## 2. 分步计划

### Step 1 — 补 plan 模板骨架
- **目标**：让 `cs-feat-design/reference.md` 能生成完整 `{slug}-plan.md`
- **触碰范围**：`cs-feat-design/reference.md`
- **退出信号**：reference 文档里存在 `feature-plan` frontmatter、固定节结构和 step 示例
- **验证**：Read `cs-feat-design/reference.md`，确认有 `## 3. {slug}-plan.md 格式`

### Step 2 — 锁定 design 生成顺序
- **目标**：让 `cs-feat-design/SKILL.md` 明确 hybrid feature 的生成顺序是 approved design → plan → checklist
- **触碰范围**：`cs-feat-design/SKILL.md`
- **退出信号**：技能说明不再只描述 design/checklist 二联产物
- **验证**：grep `生成 \\`{slug}-plan.md\\`` 与 `approved design → plan → checklist`

### Step 3 — 对齐共享约定
- **目标**：把 plan 的 frontmatter、固定节和 checklist 映射写回 shared conventions
- **触碰范围**：`.codestable/reference/shared-conventions.md`
- **退出信号**：共享约定能独立解释 plan 如何生成和消费
- **验证**：grep `执行目标`、`分步计划`、`与 checklist 的映射`

### Step 4 — 同步下游消费口径
- **目标**：让 implement / acceptance 把 plan 当真实产物输入
- **触碰范围**：`cs-feat-impl/SKILL.md`、`cs-feat-accept/SKILL.md`
- **退出信号**：文档表述从“若存在 plan”升级为“hybrid 时 plan 是真实输入”
- **验证**：Read 两份技能文档，确认措辞已升级

### Step 5 — 产出样板 feature 自证
- **目标**：在当前 feature 目录里留下真实 `plan.md` 样板
- **触碰范围**：`.codestable/features/2026-06-01-execution-plan-artifact/`
- **退出信号**：目录里同时存在 design / plan / checklist 三类产物，且职责不冲突
- **验证**：find 当前 feature 目录并人工核对三份文档职责分离

## 3. 风险与回退

- 风险 R1：plan 模板与 checklist 职责再次重叠，导致两份文档都在写 detailed narrative。
  - 回退 / 止损：以 design 为 scope source、plan 为 step source、checklist 为 status carrier 三分口径逐条回查。
- 风险 R2：只改了术语，不生成真实样板，导致下游仍无法按真实产物消费。
  - 回退 / 止损：当前 feature 必须留一份真实 `execution-plan-artifact-plan.md`，否则本 feature 不算完成。

## 4. 与 checklist 的映射

- Step 1 → checklist.steps[0]
- Step 2 → checklist.steps[1]
- Step 3 → checklist.steps[2]
- Step 4 → checklist.steps[3]
- Step 5 → checklist.steps[4]
