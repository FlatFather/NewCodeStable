# CodeStable 共享口径 — Feature

本模块定义 feature 产物职责边界与迁移规则。

其他模块：
- `shared-conventions-core.md` — 目录结构与命名规则
- `shared-conventions-checklist.md` — checklist 生命周期
- `shared-conventions-roadmap.md` — roadmap ↔ feature 衔接

---

## 2. feature 产物职责边界

feature 的活跃标准口径固定为：

- **hybrid feature**：`design + plan + checklist + acceptance`

fastforward 继续作为独立快路径存在；历史 legacy 目录（`design + checklist + acceptance`）仅作留档兼容读取，不再作为新 feature 或重开 feature 的活跃口径。

### 四类产物各写什么

- **`{slug}-intent.md`**：仅在初始化模式或用户主动先写半成品方案时出现。它记录 design 前的需求概要 / 大致做法 / 相关数据结构，是 feature 的 **pre-design seed**；后续由 `cs-feat-design` 读取并消化进正式 design，不作为 implement / acceptance 的输入。
- **`{slug}-design.md`**：范围、术语、成功标准、关键决策、流程级约束、挂载点、推进策略切片。它是 feature 的 **scope source**，也是唯一方案源。
- **`{slug}-plan.md`**：标准 feature 必备。承接已批准 design，展开详细执行顺序、每步退出信号、验证路径、风险与缓解。它是 feature 的 **step source**，不能反向改 scope。frontmatter 固定为 `doc_type / feature / design / status`；正文固定包含"执行目标 / 分步计划 / 风险与回退 / 与 checklist 的映射"四节。
- **`{slug}-checklist.yaml`**：标准 feature 必备。机器可读状态载体，记录 `steps` / `checks` 及状态变化。它是 **status carrier**，不是 narrative plan。
- **`{slug}-acceptance.md`**：对照 design / plan（若存在）/ checklist 做核验，并回写 architecture / requirement / roadmap。它是 **verification sink**。

### 共享约束

- intent 是 design 前的可选前置草稿；它帮助用户离线起草，但不改变后续 fastforward / hybrid 流程划分。
- design 永远是范围与约束的唯一方案源；plan、checklist、acceptance 都不能越权改 scope。
- 标准 feature 中，plan 负责对人可读的详细执行步骤；checklist 只保留机器可读状态。plan 初稿为 `status: draft`，执行顺序获批后必须写为 `status: approved`，实现阶段只消费 approved plan。
- 标准 feature 一旦进入实现，`plan.md` 与 `checklist.yaml` 就都必须存在；implement 与 acceptance 都必须把它们当作输入之一。
- issue / refactor 流程不依赖 `feature-plan`；本节只约束 feature 流程。
- **feature directory binding**：`YYYY-MM-DD-{slug}` 目录名是 roadmap item、design、plan、checklist、acceptance 之间的唯一绑定键，不再新增第二套 execution id。
- **plan presence rule**：活跃标准 feature 的 `plan.md` 与 `checklist.yaml` 必须在进入实现前存在；未重开的历史 legacy 目录可继续缺失并只作兼容读取；workflow-check 对新 feature 和被重开的 feature 仍应把缺失视为错误。

---

### 迁移总则

- **forward-only adoption**：新协议默认只约束新 feature；历史 legacy 目录保持当时口径留档，不自动追溯回填。
- **minimal backfill**：历史 feature 若要继续推进，应优先升级到新标准主线所需的最小字段/文件；不为"整齐"一次补齐所有旧产物。
- **legacy removal**：legacy 从活跃 workflow 定义中删除；新 feature 与重开 feature 都不再允许沿用 `design + checklist + acceptance` 作为主线。
- 历史 design 缺 `workflow` 字段不算错；新的标准 feature 设计固定写 `workflow: hybrid`。
- workflow-check 的默认适用边界是**新 feature 和被重开的 feature**；未重开的历史 legacy 目录不因缺 `workflow` 或 `plan.md` 被直接视为错误。
