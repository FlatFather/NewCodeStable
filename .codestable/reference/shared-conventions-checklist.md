# CodeStable 共享口径 — Checklist

本模块定义 checklist 生命周期与职责划分。

其他模块：
- `shared-conventions-core.md` — 目录结构与命名规则
- `shared-conventions-feature.md` — feature 产物职责边界
- `shared-conventions-roadmap.md` — roadmap ↔ feature 衔接

---

## 3. {slug}-checklist.yaml 生命周期

- 是 feature 工作流的机器可读状态载体，不是详细执行步骤正文
- `cs-feat-plan` 基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)。其中 checklist 的 `steps` 从 plan 的推进顺序派生，`checks` 从 design 各节约束派生
- 标准 feature 的 checklist 步骤顺序和状态推进必须与 `{slug}-plan.md` 对齐；详细步骤解释仍写在 plan，不回流到 checklist
- `cs-feat-ff` **不生成** checklist（也不写 design / acceptance），是跳过 spec 流程直接写代码的超轻量通道；唯一留下的痕迹是动手后回写的 `{slug}-ff-note.md`（轻量回顾，参与 scoped-commit、可被 cs-arch / cs-req backfill 检索到）

`steps` 的粒度是 **编排-计算分离维度的切片策略**——按"先编排骨架、后计算节点、最后持久化与测试"写（最简 Workflow 先行 → 逐个节点填充），**不下沉到 file:line / 函数级**。具体改哪个文件由 implement 阶段决定。

**design 的职责**：

- 提供 plan/checklist 派生所需的推进策略切片（第 2.4），但不直接落盘 `steps` / `checks`
- 提取 `checks` 的来源：第 1 节"明确不做"→ 范围守护；第 2.1 接口 → 名词契约；第 2.2 主流程 + 流程级约束 → 编排骨架；第 2.3 挂载点 → 挂载点；第 3 节场景清单 → 验收场景
- `cs-feat-plan` 基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)。其中 checklist 的 `steps` 从 plan 的推进顺序派生，`checks` 从 design 各节约束派生

**implement 的职责**：

- 对标准 feature：同时读取已批准 design 与 plan；按 checklist 状态推进，但详细步骤解释、退出信号展开和验证路径以 plan 为准
- 实现到具体文件级时需要拆分某步、或发现微重构是其前置（参考第 7 节反射检查）→ 跟用户对齐后追加 / 拆分 steps，**不偷偷做**
- 不改写 `checks`

**acceptance 的职责**：

- 对标准 feature：按 `design + plan + checklist` 核验，仍只更新 `checks[].status`，不重写 `steps`

**写作约束**：子技能描述 checklist 时只补本阶段读 / 写哪一部分，不重新定义生命周期。
