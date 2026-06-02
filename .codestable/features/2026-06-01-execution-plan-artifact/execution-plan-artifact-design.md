---
doc_type: feature-design
feature: 2026-06-01-execution-plan-artifact
requirement:
workflow: hybrid
roadmap: workflow-hybridization
roadmap_item: execution-plan-artifact
status: approved
summary: 为 hybrid feature 正式引入 feature-plan 产物、模板与生成流程，让 detailed execution narrative 从 design 和 checklist 中解耦
tags: [workflow, feature-plan, checklist, design, codestable]
---

# execution-plan-artifact design

## 0. 术语约定

| 术语 | 定义 | 防冲突结论 |
|---|---|---|
| `feature-plan` | hybrid feature 的详细执行步骤正文，承接已批准 design，提供人类可读的分步执行说明 | 上一条 feature 已把该名词写入共享约定；本 feature 开始把它从“保留术语”变成“真实产物” |
| plan step | `feature-plan` 中的一步执行切片，描述目标、触碰范围、退出信号、验证方式 | 它和 checklist step 一一对应，但职责不同；plan 讲说明，checklist 讲状态 |
| plan template | `cs-feat-design` 用于生成 `{slug}-plan.md` 的固定结构 | 当前仓库没有该模板，需要本 feature 新增 |
| hybrid feature | 采用 `design + plan + checklist + acceptance` 的 feature 目录口径 | 本 feature 只为 hybrid feature 新增 plan，不改 legacy feature 的合法性 |

## 1. 决策与约束

### 需求摘要

**做什么**：为 NewCodeStable 的 hybrid feature 正式新增 `{slug}-plan.md` 产物和生成口径：当 feature 命中 hybrid 条件时，design 阶段除了产出 `design.md` 与 `checklist.yaml`，还要同时生成一份 `plan.md`，把 CCG 风格的 step-by-step 执行说明落到 `.codestable/features/` 目录下。

**为谁**：NewCodeStable 的维护者与使用者。维护者需要统一的 plan 结构和生成边界，避免每条 feature 各写各的执行步骤文风；使用者需要在实现前拿到一份比 checklist 更适合阅读、比 design 更聚焦执行顺序的计划正文。

**成功标准**：
1. `cs-feat-design` 的参考模板和流程说明能明确生成 `{slug}-plan.md`。
2. hybrid feature 的 `plan.md` 有固定 frontmatter 和固定节结构，能承载步骤说明、退出信号、验证方式。
3. checklist 只保留机器可读状态，不再被迫承担 detailed narrative。
4. implement 与 acceptance 能根据共享约定消费这份真实存在的 `plan.md`，而不是只消费抽象术语。

**明确不做**：
- 不在本 feature 中实现 plan/checklist/roadmap 的自动一致性校验脚本。
- 不在本 feature 中决定哪些 feature 默认必须走 hybrid；只实现“当走 hybrid 时 plan 怎么落”。
- 不批量为历史 feature 回填 `plan.md`。
- 不改 issue / refactor 的文档结构。
- 不实现浏览器 UI、CLI 交互或可视化编辑器来写 plan。

### 复杂度档位

走“项目内部工具”默认档位，仅偏离两项：
- 可读性 = public（偏离默认 team 的原因：plan 模板和文档结构会直接被用户阅读和复制）
- 可测试性 = tested（偏离默认 testable 的原因：至少要校验新生成的 checklist / roadmap 状态回写仍可通过 YAML 校验）

### 关键决策

1. **plan 由 design 阶段一次生成，不延迟到 implement 再补**  
   如果 implement 才生成 plan，执行者就会先动手再补文档，plan 会退化成事后总结，不再是执行输入。

2. **plan 只展开 design 已批准的推进顺序，不重复需求摘要和术语定义**  
   design 继续做 scope source；plan 只回答“按什么顺序做、每步怎么判断完成”。

3. **plan step 与 checklist step 一一对应，但不是同构文件**  
   plan 保存说明型字段（goal / touches / exit signal / verification），checklist 只保存状态与必要索引。

4. **legacy feature 不被自动升级**  
   plan 是 hybrid 口径的增强产物；历史 feature 和简单 feature 继续可以只用 design + checklist。

## 2. 名词与编排

### 2.1 名词层

#### 现状

- `feature-plan` 已是共享约定中的一等术语，但当前 feature 目录里还没有真实 `plan.md` 文件。来源：`.codestable/reference/shared-conventions.md` 第 2 节。
- `cs-feat-design/reference.md` 只提供 `design.md` 和 `checklist.yaml` 的模板，没有 `plan.md` 模板。来源：`cs-feat-design/reference.md`。
- `cs-feat-design/SKILL.md` 已说明 hybrid feature 可以有 `{slug}-plan.md`，但没有说明它的具体结构和生成时机。来源：`cs-feat-design/SKILL.md`。
- implement 与 acceptance 已知道“hybrid feature 可能存在 plan”，但当前仓库里没有一条真实 feature 产物作为输入样板。来源：`cs-feat-impl/SKILL.md`、`cs-feat-accept/SKILL.md`。

#### 变化

- 新增真实 feature 产物 `{slug}-plan.md`，位置固定在 feature 目录内，与 design/checklist/acceptance 并列。
- 新增 `feature-plan` frontmatter 约定：
  - `doc_type: feature-plan`
  - `feature: YYYY-MM-DD-{slug}`
  - `design: {slug}-design.md`
  - `status: draft | approved | superseded`
- 新增 plan 正文固定节：
  - `## 1. 执行目标`
  - `## 2. 分步计划`
  - `## 3. 风险与回退`
  - `## 4. 与 checklist 的映射`
- checklist 继续保留 `steps/checks/status`，但其 `steps` 不再承担详细说明，只做状态投影。

#### 接口示例

plan frontmatter 示例：

```yaml
---
doc_type: feature-plan
feature: 2026-06-01-demo
design: demo-design.md
status: approved
---
```

plan step 示例：

```markdown
## 2. 分步计划

### Step 1 — 生成 shared contract 骨架
- 目标：把新契约写进 shared conventions
- 触碰范围：.codestable/reference/shared-conventions.md
- 退出信号：共享约定可独立解释新产物职责
- 验证：grep 命中 feature-plan / legacy / hybrid 定义且无互相矛盾表述
```

对应 checklist step：

```yaml
- action: "共享契约骨架：把新契约写进 shared conventions"
  exit_signal: "共享约定可独立解释新产物职责"
  status: pending
```

### 2.2 编排层

```mermaid
flowchart LR
    A[已批准 design] --> B[生成 plan.md]
    B --> C[从 design + plan 抽 checklist]
    C --> D[implement 读取 design + plan + checklist]
    D --> E[acceptance 读取 design + plan + checklist]
```

#### 现状

- 当前 design 阶段在批准后直接生成 checklist，没有独立的 plan 产物层。来源：`cs-feat-design/SKILL.md`、`cs-feat-design/reference.md`。
- implement 与 acceptance 已支持“若存在 plan 则读取”，但这个条件在真实 feature 中尚未被满足。来源：`cs-feat-impl/SKILL.md`、`cs-feat-accept/SKILL.md`。

#### 变化

- hybrid feature 的设计闭环变为：**起草 design → 用户批准 → 生成 plan → 从 design + plan 抽 checklist → implement / acceptance 共同消费三者**。
- plan 成为 checklist 的上游说明层：plan 决定 narrative order，checklist 记录 machine-readable status。
- `cs-feat-design` 需要在落盘 approved design 时，同时生成 plan 和 checklist，并把 roadmap item 标为 `in-progress`。

#### 流程级约束

- **generation order**：先 approved design，再生成 plan，再抽 checklist；不能先写 checklist 再倒推 plan。
- **single source**：scope 只看 design，step narrative 只看 plan，状态只看 checklist。
- **compatibility**：legacy feature 不强制补 plan；只有显式采用 hybrid 的 feature 触发这一链路。
- **writeback discipline**：roadmap 状态仍由 design/acceptance 写回，不由 plan 单独维护。

### 2.3 挂载点清单

- `cs-feat-design/reference.md`：新增 `{slug}-plan.md` 模板和 checklist 映射口径 — 修改
- `cs-feat-design/SKILL.md`：新增生成 plan 的时机、顺序与输出边界 — 修改
- `.codestable/reference/shared-conventions.md`：补充 plan 真实产物的 frontmatter 与生成/消费规则 — 修改
- `cs-feat-impl/SKILL.md`：把“存在 plan 就读取”从约定补成真实输入前提 — 修改
- `cs-feat-accept/SKILL.md`：把“存在 plan 就验收”从约定补成真实输入前提 — 修改

### 2.4 推进策略

1. **plan 模板骨架**：先在 `cs-feat-design/reference.md` 新增 `{slug}-plan.md` 模板和 step 示例  
   退出信号：design 模板层能生成一份完整 plan 骨架
2. **design 生成顺序**：更新 `cs-feat-design/SKILL.md`，明确 approved design → plan → checklist 的生成顺序  
   退出信号：技能说明里不再只有 design/checklist 二联产物
3. **共享约定对齐**：把 plan 的 frontmatter、节结构、与 checklist 的映射写回 shared conventions  
   退出信号：共享约定能解释 plan 如何生成和消费
4. **下游消费口径**：同步 implement / acceptance 的输入说明  
   退出信号：下游文档能把 plan 当真实产物读取，而不是抽象占位词
5. **样板 feature 自证**：为当前 feature 自身生成一条真实 `execution-plan-artifact-plan.md` 样板，证明模板可落盘  
   退出信号：feature 目录里出现真实 plan 产物，且 checklist / design 仍保持职责分离

### 2.5 结构健康度与微重构

##### 评估
- 文件级 — `cs-feat-design/reference.md`：当前承担模板职责，新增 `plan.md` 模板是同一主题延伸，不需要拆文件。
- 文件级 — `.codestable/reference/shared-conventions.md`：已有 feature 产物职责章节，本次补充 plan 真实生成规则，仍属同一共享契约主题。
- 文件级 — `cs-feat-design/SKILL.md`：已承担 design 产物生成流程，本次新增 plan 生成顺序，职责未漂移。
- 目录级 — `.codestable/features/2026-06-01-execution-plan-artifact/`：将新增 design/checklist/plan 三份产物，目录规模健康。
- compound convention：当前 compound 为空，未命中可复用 convention。

##### 结论：不做

本 feature 不做微重构，原因是改动集中在既有模板和流程说明的增强，不涉及职责混杂或目录摊平问题。

## 3. 验收契约

- **S1**：`cs-feat-design/reference.md` 能提供完整 `{slug}-plan.md` 模板，包含 frontmatter 与固定节结构。
- **S2**：`cs-feat-design/SKILL.md` 明确 hybrid feature 的生成顺序是 approved design → plan → checklist。
- **S3**：共享约定能解释 plan 的 frontmatter、固定节和与 checklist 的映射。
- **S4**：implement 与 acceptance 文档把 plan 当真实输入，而不是“如果有就顺便读一下”的抽象占位词。
- **S5**：当前 feature 目录里有一份真实 `execution-plan-artifact-plan.md` 作为样板，且内容和 design / checklist 职责不冲突。

**明确不做的反向核对项**：
- 不应要求历史 feature 目录补 plan。
- 不应把 issue / refactor 的流程文档改成依赖 plan。
- 不应把 plan 写成新的 scope source。

## 4. 与项目级架构文档的关系

本 feature 会把 `feature-plan` 从抽象术语推进成真实产物，因此 acceptance 阶段应把以下内容归并到 `ARCHITECTURE.md`：

- **名词**：`feature-plan` 的 frontmatter 与固定节结构
- **动词骨架**：hybrid feature 的设计阶段新增 plan 生成环节
- **流程级约束**：approved design → plan → checklist 的顺序约束，以及 scope / step / status 的三分口径
