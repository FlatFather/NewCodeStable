---
doc_type: issue-analysis
issue: 2026-06-11-terminology-criteria-fragmented
status: confirmed
root_cause_type: duplication
related: [terminology-criteria-fragmented-report.md]
tags: [workflow, terminology, maintainability, routing]
---

# terminology criteria fragmented 根因分析

## 1. 问题定位

| 关键位置 | 说明 |
|---|---|
| `cs-feat/SKILL.md:120-121` | feature / issue 边界定义：issue 包含 bug / 异常 / 文档错误 |
| `cs-issue/SKILL.md:106-107` | feature / issue 边界定义：issue 额外包含“性能问题” |
| `cs/SKILL.md:128-136` | 沉淀类技能判别口诀 |
| `.codestable/reference/system-overview.md:69-78` | 沉淀类技能区分的权威说明，并写明“A 和 B 有什么不同”由本节负责 |
| `cs-feat/SKILL.md:60-62` | fastforward vs 标准 feature 判据，仅在 cs-feat 内定义 |

## 2. 失败路径还原

**正常路径（理想状态）**：
1. 关键术语和路由判据定义在单一权威文档中
2. 各 skill 只保留最小必要摘要或指向权威文档
3. 修改判据时只需改权威文档
4. 所有入口按同一套判据路由用户诉求

**失败路径（当前状态）**：
1. 判据散落在多个 skill / reference 中
2. 某个入口为了自解释复制一份定义
3. 后续修改时只改其中一处
4. 不同入口出现轻微差异，例如：
   - `cs-feat` 中 issue = bug / 异常 / 文档错误
   - `cs-issue` 中 issue = bug / 异常行为 / 文档错误 / 性能问题
5. 用户从不同入口进入时可能得到不同路由建议

**分叉点**：缺少“术语判据单一权威来源”；同时 `system-overview.md:78` 已经意识到部分判据应该集中负责，但该模式尚未覆盖 feature/issue、fastforward 等其他判据。

## 3. 根因

**根因类型**：duplication（重复维护）

**根因描述**：

CodeStable skill 体系中存在多类“A vs B”判据：
- feature vs issue
- learning vs trick vs decision vs explore
- fastforward vs 标准 feature
- issue 标准路径 vs 快速通道
- brainstorm vs intent

这些判据原本是路由层的核心规则，但当前分散写在对应 skill 内，以便单个 skill 自解释。这样虽然减少跳转，但带来两个问题：

1. **判据更新无法保证同步**：同一概念在多个 skill 中复述后，很容易出现轻微差异。
2. **新增 skill 难以发现权威来源**：维护者不知道应该复制哪个版本，或是否应该复述。

`system-overview.md:78` 已经为沉淀类技能建立了“由本节负责区分”的模式，但这套模式没有扩展到其他关键判据。

**是否有多个根因**：否，单一根因为关键术语判据缺少统一归口。

## 4. 影响面

- **影响范围**：所有依赖路由判据的入口 skill，尤其是 `cs`、`cs-feat`、`cs-issue`、`cs-brainstorm`
- **潜在受害模块**：用户诉求分诊、feature/issue 边界判断、沉淀类文档归档、fastforward 选择
- **数据完整性风险**：低。不会损坏产物，但可能把诉求落到错误流程，形成后续文档归类偏差
- **严重程度复核**：维持 P1。路由判据直接决定进入哪个 workflow，口径漂移会影响用户体验与产物质量

## 5. 修复方案

### 方案 A：新增 `.codestable/reference/terminology.md`（推荐）

**做什么**：
1. 创建 `.codestable/reference/terminology.md`，集中定义关键术语和判据：
   - feature vs issue
   - learning vs trick vs decision vs explore
   - fastforward vs 标准 feature
   - brainstorm vs intent
   - issue 标准路径 vs 快速通道
2. 在 `system-overview.md` 的“进一步参考”中加入 terminology 指针。
3. 在相关 skill 的判据段落保留短摘要，并注明“完整判据见 `.codestable/reference/terminology.md`”。

**优点**：
- 单一权威来源，判据维护成本最低
- 不继续膨胀 `shared-conventions.md`
- 新增 skill 时能直接引用 terminology

**缺点 / 风险**：
- 新增一个 reference 文件，使用者需要多读一个文档
- 需要同步修改多个 skill 的相关文案

**影响面**：
- 新建文件：`.codestable/reference/terminology.md`
- 修改文件：`system-overview.md`、`cs/SKILL.md`、`cs-feat/SKILL.md`、`cs-issue/SKILL.md` 等

### 方案 B：只在 `system-overview.md` 扩展判据区

**做什么**：
- 在 `system-overview.md` 增加所有关键判据
- 各 skill 引用 system-overview

**优点**：
- 不新建文件
- system-overview 已是体系总览，天然适合放高层判据

**缺点 / 风险**：
- `system-overview.md` 会继续变长
- 总览文档会混入过多细节，降低可读性
- 未来仍可能触及 300 行限制

**影响面**：
- 修改 `system-overview.md` 与多个 skill

### 方案 C：保持分散定义，增加同步检查

**做什么**：
- 保留当前各 skill 的判据文本
- 写脚本检查 feature/issue 等关键定义是否一致

**优点**：
- 不改变阅读路径
- 自动发现一部分漂移

**缺点 / 风险**：
- 治标不治本，判据仍需多处维护
- 文本一致性检查难以覆盖语义差异

**影响面**：
- 新增脚本，可能增加维护复杂度

### 推荐方案

**推荐方案 A**，理由：
1. **直接解决根因**：把关键术语判据归口到单一 reference 文件
2. **符合文档长度约束**：不继续膨胀 `shared-conventions.md` 或 `system-overview.md`
3. **可扩展**：后续新增 workflow 或术语时直接补 terminology
4. **保留局部可读性**：各 skill 可保留一句短摘要，不必完全跳转
