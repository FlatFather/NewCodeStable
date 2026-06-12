---
doc_type: issue-analysis
issue: 2026-06-11-feat-plan-boundary-drift
status: confirmed
root_cause_type: duplication
related: [feat-plan-boundary-drift-report.md]
tags: [workflow, cs-feat-plan, arch-drift, documentation]
---

# feat plan boundary drift 根因分析

## 1. 问题定位

| 关键位置 | 说明 |
|---|---|
| `cs-feat-plan/SKILL.md:12` | 职责描述："把已批准 design 展开成可执行的 `plan.md`，并从 `design + plan` 抽出 `checklist.yaml`" |
| `.codestable/reference/shared-conventions.md:146-148` | 职责描述："由 `cs-feat-plan` 在 approved design 后生成；先落 `plan.md`，再从 design + plan 抽 `steps` + `checks`" |
| `.codestable/reference/shared-conventions.md:156` | 职责描述："基于已批准 design 生成 `plan.md` 与 `checklist.yaml`；design 仍然只决定范围和切片策略，不把 detailed step narrative 塞回 checklist" |
| `cs-feat-design/SKILL.md:12` | 提及 cs-feat-plan："后续由 `cs-feat-plan` 基于已批准 design 生成 `{slug}-plan.md` 与 `{slug}-checklist.yaml`" |

## 2. 失败路径还原

**正常路径（理想状态）**：
1. cs-feat-plan 的职责边界在单一权威文档中定义
2. 相关 skill 引用该定义或保留完全一致的摘要
3. 修改职责时只需改权威定义
4. 所有相关文档对 plan / checklist 派生关系的描述一致

**失败路径（当前状态）**：
1. cs-feat-plan 的职责在 3 处分别描述
2. 三处表述存在微妙差异：
   - `cs-feat-plan/SKILL.md:12`：强调"从 `design + plan` 抽出 `checklist.yaml`"
   - `shared-conventions.md:146`：描述顺序为"先落 `plan.md`，再从 design + plan 抽 `steps` + `checks`"
   - `shared-conventions.md:156`：强调"基于已批准 design 生成"，并说明 design 不把 narrative 塞回 checklist
3. 维护者阅读不同文档时可能对 plan / checklist 派生链理解不一致
4. 例如可能误以为 checklist 只从 design 派生，忽略 plan 的中间作用

**分叉点**：cs-feat-plan 职责边界在多处独立描述，没有统一标准表述。

## 3. 根因

**根因类型**：duplication（重复维护）

**根因描述**：

cs-feat-plan 作为新增的显式阶段，其职责边界在不同文档中的表述存在微妙差异。

实际派生链应该是：
```
design (scope source)
  ↓
cs-feat-plan 生成 plan.md (step source)
  ↓
cs-feat-plan 从 design + plan 抽 checklist.yaml (status carrier)
```

但当前三处描述：
- `cs-feat-plan/SKILL.md:12`：暗示 checklist 派生自 design + plan
- `shared-conventions.md:146`：明确先落 plan，再从 design + plan 抽 checklist
- `shared-conventions.md:156`：强调"基于 design 生成 plan 与 checklist"，可能让人误以为两者并列从 design 派生

这些差异虽然微妙，但会影响维护者对 plan 阶段职责的理解。

**是否有多个根因**：否，单一根因为职责边界描述分散且未统一标准表述。

## 4. 影响面

- **影响范围**：涉及 cs-feat-plan 阶段的理解与实现
- **潜在受害模块**：
  - skill 维护者：不清楚 plan 阶段到底负责什么
  - 用户：在 design / plan / impl 阶段切换时理解产物关系困难
- **数据完整性风险**：低。不会损坏产物，但可能导致错误理解 plan / checklist 映射关系
- **严重程度复核**：维持 P1。plan 阶段是标准 feature 主线的关键阶段，职责边界不一致会影响实现理解

## 5. 修复方案

### 方案 A：统一为标准表述（推荐）

**做什么**：
在所有涉及 cs-feat-plan 的文档中使用统一标准表述：

> `cs-feat-plan` 基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)。其中 checklist 的 `steps` 从 plan 的推进顺序派生，`checks` 从 design 各节约束派生。

具体修改：
1. `cs-feat-plan/SKILL.md:12`：替换为标准表述
2. `shared-conventions.md:146-148`：替换为标准表述
3. `shared-conventions.md:156`：替换为标准表述
4. `cs-feat-design/SKILL.md:12`：保持简短指针，确认不与标准表述冲突

**优点**：
- 所有相关文档对 cs-feat-plan 职责的描述完全一致
- 明确派生链：design → plan → checklist
- 改动范围适中（3-4 处）

**缺点 / 风险**：
- 需要同步修改多处文档
- 标准表述可能比当前某些描述更长

**影响面**：
- 修改文件：`cs-feat-plan/SKILL.md`、`shared-conventions.md`（2 处）、可能涉及 `cs-feat-design/SKILL.md`

### 方案 B：增加派生链图

**做什么**：
在 `shared-conventions.md` 或 `system-overview.md` 增加 feature 产物派生链图：
```
design (scope source) → plan (step source) → checklist (status carrier)
                         ↓                      ↓
                    cs-feat-impl 读取    cs-feat-impl 更新状态
```

**优点**：
- 视觉化展示派生关系
- 不改变现有文本表述

**缺点 / 风险**：
- 不解决文本表述不一致问题
- 图和文本仍可能分别维护导致漂移

**影响面**：
- 修改文件：`shared-conventions.md` 或 `system-overview.md`

### 方案 C：合并为单一权威定义

**做什么**：
- 在 `shared-conventions.md` 第 2 节定义完整 cs-feat-plan 职责
- 其他 skill 只保留指针："职责边界见 shared-conventions 第 2 节"

**优点**：
- 单一权威来源
- 避免重复维护

**缺点 / 风险**：
- 增加跳转成本
- shared-conventions 已较长，继续增加可能接近 300 行限制

**影响面**：
- 修改文件：`shared-conventions.md`、`cs-feat-plan/SKILL.md`、`cs-feat-design/SKILL.md`

### 推荐方案

**推荐方案 A**，理由：
1. **直接解决根因**：统一所有相关文档的表述
2. **改动范围适中**：只需修改 3-4 处
3. **明确派生链**：标准表述明确了 design → plan → checklist 的关系
4. **保留局部可读性**：各 skill 仍保留完整职责描述，不必跳转
