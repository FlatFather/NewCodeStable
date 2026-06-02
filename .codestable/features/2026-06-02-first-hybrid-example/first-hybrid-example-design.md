---
doc_type: feature-design
feature: 2026-06-02-first-hybrid-example
requirement:
roadmap: workflow-hybridization
roadmap_item: first-hybrid-example
status: approved
summary: 以一条真实 feature 产物链沉淀 hybrid 工作流样板，覆盖 design、plan、checklist、acceptance 与 roadmap/architecture 回写的完整闭环
tags: [workflow, example, hybrid, acceptance, roadmap]
---

# first-hybrid-example design

## 0. 术语约定

| 术语 | 定义 | 防冲突结论 |
|---|---|---|
| example feature | 不是新规则本身，而是用来演示新规则如何被完整使用的一条真实 feature | 本 feature 不再发明新协议，只消费前面已经落下的协议 |
| full hybrid chain | `design → plan → checklist → implement → acceptance → roadmap/architecture 回写` 的完整链路 | 这是本 feature 要交付给用户的最关键样板 |
| golden sample | 后续文档、技能和用户都可以优先参考的一条标准样例 | 本 feature 的 acceptance 后，仓库里应存在一条可复制的黄金样板 |
| sample drift | 样板文档和真实共享约定逐步脱节 | 本 feature 需要降低这种风险，让样板绑定到真实 current 规则 |

## 1. 决策与约束

### 需求摘要

**做什么**：用一条真实 feature 走完整 hybrid 工作流闭环，产出一套用户与后续技能都能直接参考的黄金样板，覆盖：
1. hybrid feature 的 design / plan / checklist / acceptance 四件套
2. roadmap item 从 `planned → in-progress → done` 的完整状态变化
3. architecture 的实际归并
4. workflow-check 在真实样板上的通过路径

**为谁**：NewCodeStable 的维护者、后续 feature 作者，以及第一次上手这套流程的用户。维护者需要一条“看这条就知道怎么做”的标准样板；用户需要在没有看完所有技能文档的情况下，也能通过一个完整例子理解整套流程。

**成功标准**：
1. 当前仓库里存在一条结构完整、状态完整、回写完整的 hybrid 样板 feature。
2. 样板引用的口径都来自当前 shared conventions / tools / architecture，而不是自定义另一套说法。
3. 用户只看这条 feature 目录，就能理解 hybrid 流程的主要产物和阶段关系。
4. workflow-check 能在这条样板上通过。

**明确不做**：
- 不再引入新的工作流协议。
- 不把所有历史 feature 重写成样板风格。
- 不做第二套“教程版”平行文档；样板本身就是教程。
- 不实现图形化导航页或 README 大改。

### 复杂度档位

走“项目内部工具”默认档位，仅偏离两项：
- 可读性 = public（偏离默认 team 的原因：这条样板就是给用户和后续 feature 作者看的）
- 可测试性 = tested（偏离默认 testable 的原因：样板需要经过 workflow-check 和 acceptance 双验证，才能称为黄金样板）

### 关键决策

1. **样板优先复用现有真实 feature，而不是另造虚构 demo**  
   虚构 demo 很容易和真实协议脱节；本 feature 应以真实目录、真实状态、真实校验结果为基础整理黄金样板。

2. **样板是“真实闭环产物”，不是另起一套文档类型**  
   不新增 tutorial-specific frontmatter；直接使用 design/plan/checklist/acceptance 现有产物类型。

3. **样板必须绑定当前共享约定**  
   如果 shared conventions 以后变了，样板也应能被 acceptance 重新核对，而不是变成一份只供阅读的旧教程。

## 2. 名词与编排

### 2.1 名词层

#### 现状

- 仓库里已经有多条实现新规则的 feature，但它们各自聚焦单一主题：职责边界、plan 产物、handoff 协议、validation、migration。来源：`.codestable/features/`。
- 当前还没有一条以“完整示范 hybrid 工作流”为唯一目标的 feature 样板。即使 `execution-plan-artifact` 已有 design/plan/checklist/acceptance，它的目标仍是“把 plan 产物落地”，不是“作为黄金教程样板”。

#### 变化

- 新增一条显式定位为 `golden sample` 的 hybrid feature 样板。
- 这条样板要显式覆盖：
  - design：范围与约束
  - plan：详细步骤正文
  - checklist：状态载体
  - acceptance：核验与回写
- 样板还要在 acceptance 中证明：workflow-check 通过、roadmap item 已 done、architecture 已归并。

#### 接口示例

样板 feature 目录目标形态：

```text
.codestable/features/YYYY-MM-DD-first-hybrid-example/
├── first-hybrid-example-design.md
├── first-hybrid-example-plan.md
├── first-hybrid-example-checklist.yaml
└── first-hybrid-example-acceptance.md
```

frontmatter 示例：

```yaml
---
feature: YYYY-MM-DD-first-hybrid-example
workflow: hybrid
roadmap: workflow-hybridization
roadmap_item: first-hybrid-example
status: approved
---
```

### 2.2 编排层

```mermaid
flowchart LR
    A[选择真实规则集] --> B[起样板 design]
    B --> C[生成样板 plan]
    C --> D[生成 checklist]
    D --> E[实现 / 回写状态]
    E --> F[workflow-check 通过]
    F --> G[acceptance 回写 architecture + roadmap]
```

#### 现状

- 目前每条 feature 都只证明某一段规则能工作；用户需要拼多条 feature 才能理解完整 hybrid 闭环。
- workflow-check、migration guidance、handoff contract 都已存在，但还没有在同一条 feature 上完整汇合。

#### 变化

- 新增一条以“端到端证明 hybrid 流程成立”为目标的样板 feature。
- 样板流程要故意覆盖所有关键节点：design、plan、checklist、workflow-check、acceptance 回写。
- 样板 acceptance 之后，用户应能从单目录推断完整操作路径。

#### 流程级约束

- **real-current-rules only**：样板只能使用当前 shared conventions 允许的协议，不再自创简化版。
- **single-source example**：用户只需要看这一条 feature，就能理解完整 hybrid 链；不能再依赖另一份平行教程文档。
- **verifiable sample**：样板必须可被 workflow-check 和 acceptance 双验证。

### 2.3 挂载点清单

- `.codestable/features/2026-06-02-first-hybrid-example/`：新增黄金样板目录及四件套产物 — 修改
- `.codestable/roadmap/workflow-hybridization/workflow-hybridization-items.yaml`：绑定样板 feature 目录并推进状态 — 修改
- `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md`：同步样板条目状态 — 修改
- `.codestable/architecture/ARCHITECTURE.md`：归并“存在一条黄金 hybrid 样板”这一系统级事实（如确有必要）— 修改

### 2.4 推进策略

1. **选样板范围**：先明确样板要证明哪些环节，不再引入新协议  
   退出信号：样板目标覆盖 design / plan / checklist / acceptance / 回写五件事
2. **产物落齐**：生成 design + plan + checklist 四件套  
   退出信号：目录结构完整且 `workflow: hybrid` 明确
3. **链路自证**：让 workflow-check 在样板上通过  
   退出信号：样板能被工具验证，不只是人工阅读用
4. **验收归并**：完成 acceptance、architecture、roadmap 回写  
   退出信号：样板形成真正闭环

### 2.5 结构健康度与微重构

##### 评估
- 文件级 — 当前样板只会新增一个 feature 目录，不修改现有工具核心逻辑，无需微重构。
- 目录级 — `.codestable/features/` 已是标准聚合根，新增一个样板目录不会造成摊平问题。
- compound convention：当前 compound 为空，未命中可复用 convention。

##### 结论：不做

本 feature 不做微重构，原因是它的核心价值在于沉淀一条完整样板，而不是重整结构。

## 3. 验收契约

- **S1**：样板目录包含 design / plan / checklist / acceptance 四件套。
- **S2**：样板 design frontmatter 明确 `workflow: hybrid`、`roadmap`、`roadmap_item`。
- **S3**：workflow-check 在样板目录上通过。
- **S4**：acceptance 完成后，roadmap item 与 architecture 回写都完成。
- **S5**：用户只读样板目录，就能理解 hybrid 流程的主要阶段关系。

**明确不做的反向核对项**：
- 不应再新增教程专用文档类型。
- 不应为样板绕开现有共享约定。
- 不应把历史 feature 批量重写成样板。

## 4. 与项目级架构文档的关系

本 feature 完成后，architecture 至少要知道：
- 系统里存在一条可供参考的黄金 hybrid 样板
- hybrid 流程不只是规则集合，而是已有真实闭环实例
- workflow-check 和 acceptance 都能在该样板上跑通
