---
doc_type: feature-plan
feature: 2026-06-03-feature-plan-stage
design: feature-plan-stage-design.md
status: approved
---

# feature-plan-stage execution plan

## 1. 执行目标

这份 plan 只承接已批准的 design，目标是把 `cs-feat-plan` 从想法变成真实 workflow 阶段：让活跃 feature 流程只保留 fastforward 与 hybrid 两条路径，其中标准路径在进入 impl 前必须显式经过 `plan.md + checklist.yaml` 生成与确认关口。

## 2. 分步计划

### Step 1 — 改造顶层 feature 路由
- **目标**：让 `cs-feat` 顶层阶段表与路由规则显式出现 `cs-feat-plan`，并删除 legacy 作为活跃主线路径
- **触碰范围**：`cs-feat/SKILL.md`
- **退出信号**：顶层链路已经能读成 `design → plan → impl → accept`，且只剩 fastforward / hybrid 两类 feature 路径
- **验证**：Read `cs-feat/SKILL.md`，确认阶段表和路由表都出现 `cs-feat-plan`，且无 legacy 主线路由
- **文件级改动计划**：
  - `cs-feat/SKILL.md`：把阶段表从四/五阶段口径改成显式 `design → plan → impl → accept`
  - `cs-feat/SKILL.md`：把路由表中的“design 已 approved 直接进 impl”拆成“design 已 approved → cs-feat-plan；plan/checklist 已齐 → cs-feat-impl`
  - `cs-feat/SKILL.md`：移除把 legacy 当作活跃标准路径的说法，只保留 fastforward 与 hybrid
  - `cs/SKILL.md`：把体系总览中的新增能力主线改成显式 `cs-feat-design → cs-feat-plan → cs-feat-impl → cs-feat-accept`

### Step 2 — 切分 design 阶段职责
- **目标**：让 `cs-feat-design` 停止直接落 plan/checklist，只负责 approved design 并引导去 `cs-feat-plan`
- **触碰范围**：`cs-feat-design/SKILL.md`、`cs-feat-design/reference.md`
- **退出信号**：design 阶段只输出 approved design；plan/checklist 生成责任已从 design 阶段移除
- **验证**：grep `生成 {slug}-plan.md`、`checklist` 的职责描述，确认责任已经移出 design 阶段
- **文件级改动计划**：
  - `cs-feat-design/SKILL.md`：把阶段描述改成“只产 design，不再直接落盘 plan/checklist”
  - `cs-feat-design/SKILL.md`：把“方案确认后生成 plan/checklist”改成“引导进入 cs-feat-plan”
  - `cs-feat-design/SKILL.md`：删除 legacy 继续作为重开主线的说法，改成历史 feature 若继续推进必须升级到新口径
  - `cs-feat-design/reference.md`：把 design/reference 对 plan/checklist 的职责说明改成由 `cs-feat-plan` 消费与生成

### Step 3 — 落地真实 cs-feat-plan skill
- **目标**：新增 `cs-feat-plan` skill，承接 plan 与 checklist 的生成和单独确认
- **触碰范围**：`cs-feat-plan/`
- **退出信号**：仓库里存在真实 `cs-feat-plan/SKILL.md`，且它能说明输入、输出、review 和退出条件
- **验证**：find `cs-feat-plan/` 并 Read `SKILL.md`
- **文件级改动计划**：
  - `cs-feat-plan/SKILL.md`：定义阶段定位、启动检查、生成原则、汇报模板、退出条件
  - `cs-feat-plan/reference.md`：提供 plan/checklist 模板，明确 plan 采用文件级改动计划写法
  - `cs-feat-plan/reference.md`：把每个 Step 的正文模板补成“目标 / 触碰范围 / 退出信号 / 验证 / 文件级改动计划”结构

### Step 4 — 回写共享口径与下游消费
- **目标**：让 shared conventions、system overview、architecture、impl、accept 对新阶段说法一致，并删除 legacy 作为活跃标准口径
- **触碰范围**：`.codestable/reference/shared-conventions.md`、`.codestable/reference/system-overview.md`、`.codestable/architecture/ARCHITECTURE.md`、`cs-feat-impl/SKILL.md`、`cs-feat-accept/SKILL.md`
- **退出信号**：文档层已经不再把 legacy 写成活跃标准路径，也不再把 plan/checklist 生成说成 design 阶段内部动作；impl/accept 明确读取 design + plan + checklist
- **验证**：grep `cs-feat-plan`、`design + plan + checklist`、`approved design → plan → checklist`，并确认 legacy 仅以历史留档语义出现
- **文件级改动计划**：
  - `.codestable/reference/shared-conventions.md`：删除 legacy 作为活跃标准口径，改写 checklist 生成责任到 `cs-feat-plan`
  - `.codestable/reference/system-overview.md`：把 feature 主线与单次动作说明改成 fastforward + hybrid 的双轨
  - `.codestable/architecture/ARCHITECTURE.md`：把核心概念、子系统索引、硬边界中的 legacy/hybrid 关系改成“legacy archive + hybrid active”
  - `cs-feat-impl/SKILL.md`：阶段号、输入前提、主线口径统一改成 design + plan + checklist
  - `cs-feat-accept/SKILL.md`：阶段号、验收输入说明统一改成 design + plan + checklist，并去掉 legacy 活跃主线假设

### Step 5 — 样板与路由自证
- **目标**：用当前 feature 作为第一条“显式 plan 阶段 + 删除 legacy 主线”的样板
- **触碰范围**：`.codestable/features/2026-06-03-feature-plan-stage/` 当前样板、自身 checklist、必要时相关样板 feature
- **退出信号**：当前 feature 目录能作为第一条显式 plan 阶段样板，且从顶层入口到 impl 前的关口完整可见
- **验证**：Read 当前 feature 目录产物，人工核对 `cs` / `cs-feat` / `cs-feat-plan` / `cs-feat-impl` 的链路可追踪
- **文件级改动计划**：
  - `.codestable/features/2026-06-03-feature-plan-stage/feature-plan-stage-design.md`：回写新的阶段定义与 plan 边界
  - `.codestable/features/2026-06-03-feature-plan-stage/feature-plan-stage-plan.md`：以文件级改动计划格式重写 Step 1~5
  - `.codestable/features/2026-06-03-feature-plan-stage/feature-plan-stage-checklist.yaml`：与新 plan 一一映射，保证步骤标题与退出信号同步

## 3. 风险与回退

- 风险 R1：把 `cs-feat-plan` 做成 design 的尾巴，用户仍然感知不到单独 checkpoint。
  - 回退 / 止损：以 `cs-feat` 顶层阶段表和路由表为准，先让入口可见，再做内部职责切分。
- 风险 R2：删除 legacy 后仍在某些技能文案里留下活跃主线痕迹，造成新旧规则混写。
  - 回退 / 止损：以 shared conventions 为协议正文，清点 `cs-feat*`、overview、architecture 的活跃路径描述。
- 风险 R3：误把 fastforward 也拉进 `cs-feat-plan`，导致小需求通道退化。
  - 回退 / 止损：所有改动都显式保留 fastforward 豁免，不把它纳入标准 spec 主线。

## 4. 与 checklist 的映射

- Step 1 → checklist.steps[0]
- Step 2 → checklist.steps[1]
- Step 3 → checklist.steps[2]
- Step 4 → checklist.steps[3]
- Step 5 → checklist.steps[4]
