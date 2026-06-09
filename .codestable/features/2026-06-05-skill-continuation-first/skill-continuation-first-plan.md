---
doc_type: feature-plan
feature: 2026-06-05-skill-continuation-first
design: skill-continuation-first-design.md
status: draft
---

# skill-continuation-first execution plan

## 1. 执行目标

这份 plan 只承接已批准 design，回答“按什么顺序做、每步怎么判断完成”。本轮执行目标是：在不修改全局 `/ccg:go`、不把 `.ccg/tasks/` 提升为主真相源的前提下，为本项目仓库内的顶层 skill、阶段 skill 与共享文档补齐 continuation-first 续作规则，并把超长的 continuation 共享协议拆到独立 reference 文件，让短回复优先恢复已有 task / 阶段状态，避免重复路由。

## 2. 分步计划

### Step 1 — 拆共享协议：新增独立 reference，并给 shared-conventions 留摘要入口
- **目标**：先把 continuation-first 的详细共享协议从已超长的 `shared-conventions.md` 中拆出，落到新的独立 reference 文件，同时保留旧入口的摘要与指针。
- **触碰范围**：`.codestable/reference/workflow-continuation.md`、`.codestable/reference/shared-conventions.md`、`.codestable/reference/maintainer-notes.md`、`.codestable/reference/system-overview.md`、`.codestable/architecture/ARCHITECTURE.md`
- **退出信号**：新 reference 文件已承载 continuation-first、短回复词表、唯一候选约束、task 状态桥边界；`shared-conventions.md` 只保留摘要与读取指针，且两份文档都满足单文档长度约束。
- **验证**：
  - grep `continuation-first`、`task 状态桥`、`唯一候选` 在新 reference / shared / architecture 路径中可命中
  - `wc -l` 确认 `shared-conventions.md` 与新 reference 文件都不超过 300 行
  - 人工检查 `shared-conventions.md` 没再承载 continuation 详细正文

### Step 2 — 改顶层入口：让 `cs`、`cs-feat`、`cs-issue` 先恢复再路由
- **目标**：在顶层入口规则里显式加入短回复 continuation-first，确保 `继续 / 确认 / 同意 / 按这个修 / 跳过 / 继续下一步` 不再默认被当成全新诉求。
- **触碰范围**：`cs/SKILL.md`、`cs-feat/SKILL.md`、`cs-issue/SKILL.md`
- **退出信号**：三个顶层入口都写清楚：先检查唯一候选续作；命中则继续；多个候选停下让用户选；无候选才走现有路由。
- **验证**：
  - grep `继续`、`按这个修`、`唯一候选`、`续作` 在上述 skill 中命中
  - 人工检查顶层出口文案不再默认只给“建议触发哪个 skill”这一条路径

### Step 3 — 改阶段 skill：统一 feature / issue 的续作恢复口径
- **目标**：把 feature 与 issue 两条主线的阶段 skill 都收口成“先恢复已有阶段，再决定是否补问 / 回退”，避免阶段层继续重复给路由结论或重复确认 gate。
- **触碰范围**：`cs-feat-design/SKILL.md`、`cs-feat-plan/SKILL.md`、`cs-feat-impl/SKILL.md`、`cs-feat-accept/SKILL.md`、`cs-issue-report/SKILL.md`、`cs-issue-analyze/SKILL.md`、`cs-issue-fix/SKILL.md`
- **退出信号**：feature / issue 阶段技能都明确“双通道恢复”：优先读既有 spec 产物状态，task 文件只作桥接索引；缺恢复对象时才回退入口或补问。
- **验证**：
  - grep `断点恢复`、`task`、`继续`、`恢复` 在上述阶段 skill 中命中
  - 人工检查没有任何阶段把 task 文件写成 scope / step / acceptance 的真相源

### Step 4 — 补用户可见文档：解释为什么短回复不会重复进入流程
- **目标**：把 continuation-first 的用户心智模型写进仓库文档，避免维护者和使用者继续按“每次短回复都等于新请求”理解流程。
- **触碰范围**：`docs/dev/feature-workflow.md`，必要时补 `README.md` / `README.en.md` 中 workflow 概述对应段落
- **退出信号**：至少有一份对外开发文档解释了 continuation-first 的目的、边界、与 task 状态桥的关系，以及独立 reference 文件的读取位置。
- **验证**：
  - grep `continuation-first`、`短回复`、`重复路由` 在开发文档中命中
  - 人工检查文档描述与 shared conventions / workflow-continuation / skills 口径一致

### Step 5 — 做静态收口：检查两条主线和文档口径一致
- **目标**：在进入实现后收口前，核对 feature / issue 两条主线、顶层入口、共享文档之间没有互相打架的说法。
- **触碰范围**：本次实际改动的 skill 与文档文件；feature checklist
- **退出信号**：`validate-yaml.py` 能通过 feature 文档校验；grep continuation 相关关键词时，仓库内现状口径一致，没有一处仍默认“短回复=新请求”。
- **验证**：
  - `.venv/bin/python .codestable/tools/validate-yaml.py --file .codestable/features/2026-06-05-skill-continuation-first/skill-continuation-first-plan.md`
  - `.venv/bin/python .codestable/tools/validate-yaml.py --file .codestable/features/2026-06-05-skill-continuation-first/skill-continuation-first-checklist.yaml --yaml-only`
  - grep `continuation-first|唯一候选|task 状态桥|短回复|workflow-continuation` 交叉核对仓库现状文件

## 3. 风险与回退

- **风险 R1：只拆文档，不改 skill，仍然会重复确认**
  如果 continuation-first 只停留在 shared reference，技能本身仍会按旧逻辑输出重复路由或 gate。
  **回退 / 止损**：把顶层入口和阶段 skill 的更新保持为独立步骤，不把“文档拆分完成”误当成行为完成。

- **风险 R2：task 文件被误提升成主 workflow 状态源**
  如果文档写法不够严谨，后续维护者可能误以为 `.ccg/tasks/` 决定 design / plan / checklist / acceptance 的状态。
  **回退 / 止损**：在 workflow-continuation、shared conventions、maintainer notes、architecture 四处同时强调“task 状态桥，不是真相源”。

- **风险 R3：多候选续作时自动猜测，反而把用户带错流程**
  continuation-first 最大的误伤点是“猜错该继续哪个 task / feature / issue”。
  **回退 / 止损**：坚持唯一候选约束；多个候选必须停下来问。

- **风险 R4：shared-conventions 摘要和独立 reference 脱节**
  拆出去后如果摘要指针没同步，后续维护者可能仍只读 shared-conventions，错过完整协议。
  **回退 / 止损**：在摘要入口明确写“详见 workflow-continuation.md”，并把它列入 system-overview / feature-workflow 的相关文档。

## 4. 与 checklist 的映射

- Step 1 → checklist.steps[0]
- Step 2 → checklist.steps[1]
- Step 3 → checklist.steps[2]
- Step 4 → checklist.steps[3]
- Step 5 → checklist.steps[4]
