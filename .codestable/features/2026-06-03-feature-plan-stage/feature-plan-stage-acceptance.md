# feature-plan-stage 验收报告

> 阶段：阶段 4（验收闭环）
> 验收日期：2026-06-03
> 关联方案 doc：.codestable/features/2026-06-03-feature-plan-stage/feature-plan-stage-design.md

## 1. 接口契约核对

对照方案第 2.1 节名词层逐一核查。

**接口示例逐项核对**：
- [x] 标准 feature 用户可见链路目标形态：当前已能从 `cs-feat` 读到 `design → plan → impl → accept`，并在 `cs-feat-plan` 中看到 `plan.md + checklist.yaml` 的独立产出。

**名词层“现状 → 变化”逐项核对**：
- [x] `cs-feat-plan`：已从术语变成真实 skill 目录 `cs-feat-plan/`。
- [x] plan gate：已从隐含关口变成显式的顶层阶段与单独确认点。
- [x] standard feature path：已从 `design → impl → accept` 演进为 `design → plan → impl → accept`。
- [x] legacy removal：legacy 已退出活跃 workflow 定义，只保留历史留档兼容语义。

**流程图核对**（第 2.2 节开头 mermaid 图）：
- [x] `cs-feat → cs-feat-design → cs-feat-plan → cs-feat-impl → cs-feat-accept` 这条链在 `cs/SKILL.md`、`cs-feat/SKILL.md`、`cs-feat-plan/SKILL.md` 中都有实际落点。

## 2. 行为与决策核对

对照方案第 1 节 + 第 2.2 节。

**需求摘要逐项验证**：
- [x] `cs-feat` 顶层阶段表与路由规则已显式把 `plan` 阶段展示给用户。
- [x] `cs-feat-design` 已不再承担 `plan.md` / `checklist.yaml` 的落盘职责，只输出 approved design 并引导进入 `cs-feat-plan`。
- [x] 仓库中已新增真实 `cs-feat-plan` skill，负责生成 `plan.md` 与 `checklist.yaml`，并形成进入 impl 前的单独确认关口。
- [x] `cs-feat-impl` 的标准输入已固定为 `design + plan + checklist`。
- [x] 活跃 workflow 定义中已不再把 legacy 作为合法标准口径；新 feature 只剩 fastforward 与 hybrid 两条路径。

**明确不做逐项核对**：
- [x] 未重写 issue / refactor 流程。
- [x] 未批量为历史 feature 回填 `plan.md`。
- [x] 未把 `plan` 变成新的 scope source。
- [x] 未引入新的 UI 或外部可视化编辑器。
- [x] 未把 fastforward 改造成强制经过 `cs-feat-plan`。

**关键决策落地**：
- [x] `cs-feat-plan` 已作为所有标准 feature 的显式前置关口出现，而不再只是 hybrid 样板里的隐含步骤。
- [x] `checklist.yaml` 的生成职责已从 design 阶段移到 plan 阶段。
- [x] `plan.md` 的职责已强化为文件级改动计划，而不是更长的 design 摘要。
- [x] legacy 已从活跃 workflow 定义中删除。

**编排层“现状 → 变化”逐项核对**：
- [x] 方案批准与执行计划生成已拆成两个连续 checkpoint：`cs-feat-design` 与 `cs-feat-plan`。
- [x] `cs-feat` 顶层路由已能区分“approved design 但还没进入 plan 阶段”和“plan/checklist 已齐、可以进入 impl”。
- [x] `cs-feat-plan` 已成为标准主线的唯一 plan 生成入口，不再允许由 design 阶段直接越权生成 checklist。
- [x] legacy 已从主线中移除；顶层路由只保留 fastforward 与 standard hybrid 两类 feature 入口。

**流程级约束核对**：
- [x] scope / step / status 三分口径仍成立：design = scope source，plan = step source，checklist = status carrier。
- [x] 进入 impl 前必须有用户对 plan 的单独确认。
- [x] fastforward 仍保持豁免。
- [x] 历史 legacy 目录仅作留档兼容读取，不再作为新 feature 或重开 feature 的活跃主线。

**挂载点反向核对（可卸载性）**：
- [x] `cs-feat/SKILL.md`：已新增 `cs-feat-plan` 阶段与路由规则。
- [x] `cs-feat-design/SKILL.md`：已移除 plan/checklist 落盘职责，改为引导进入 `cs-feat-plan`。
- [x] `cs-feat-plan/SKILL.md`：已新增独立 skill，承接 plan/checklist 生成与单独确认。
- [x] `cs-feat-plan/reference.md`：已新增并明确 plan 以文件级改动计划组织。
- [x] `.codestable/reference/shared-conventions.md`：已删除 legacy 活跃口径，并改写 checklist 生成责任。
- [x] `.codestable/reference/system-overview.md` / `.codestable/architecture/ARCHITECTURE.md`：已更新主线与长期方向摘要。
- [x] `cs-feat-impl/SKILL.md` / `cs-feat-accept/SKILL.md`：已更新输入与阶段口径。
- [x] 反向核查：本 feature 的工作流入口与关键引用都落在上述清单内，没有发现清单外的新挂入点。
- [x] 拔除沙盘推演：移除 `cs-feat-plan`、恢复旧路由后，这个新流程能力会消失，说明挂载点边界清晰。

## 3. 验收场景核对

- [x] **S1**：`cs-feat` 的阶段表和路由规则显式暴露 `cs-feat-plan`。
  - 证据来源：文档核对
  - 结果：通过
- [x] **S2**：`cs-feat-design` 在 approved 后不再直接生成 plan/checklist，而是把用户引导到 `cs-feat-plan`。
  - 证据来源：文档核对
  - 结果：通过
- [x] **S3**：仓库中存在真实 `cs-feat-plan` skill，能从已批准 design 生成 `plan.md` 与 `checklist.yaml`。
  - 证据来源：文件存在性 + 文档核对
  - 结果：通过
- [x] **S4**：`shared-conventions` 已把 checklist 生成责任从 design 阶段改写为 plan 阶段，并删除 legacy 作为活跃标准口径。
  - 证据来源：共享约定核对
  - 结果：通过
- [x] **S5**：`cs-feat-impl` 只有在 design + plan + checklist 已齐时才启动；fastforward 路径不受影响。
  - 证据来源：impl / feat 文档核对
  - 结果：通过

本 feature 没有前端 UI 改动，无浏览器肉眼验证项。

## 4. 术语一致性

对照方案第 0 节 + 第 2.1 节命名 grep 代码：

- `cs-feat-plan`：在 design、plan、checklist、`cs-feat`、`cs-feat-plan` 中命名一致。
- `plan gate`：在 design 与 `cs-feat-plan` 说明中语义一致。
- `standard feature path`：在 design、`shared-conventions`、`system-overview`、`ARCHITECTURE` 中已统一到 `design + plan + checklist + acceptance`。
- `legacy removal`：在 design、`shared-conventions`、`system-overview`、`ARCHITECTURE` 中都已改成“历史留档兼容读取”。

## 5. 架构归并

- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已把 feature 主线更新为 `design → plan → implement → acceptance`。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已把 `legacy feature` 改成 `legacy feature archive`，说明它只作历史兼容读取。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已把标准 feature 的必备输入更新为 `plan.md + checklist.yaml`。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已保留 fastforward 作为独立快路径的总述。

归并完成后，只看 architecture 已能知道：
- 活跃标准主线是什么
- `cs-feat-plan` 在哪里插入
- legacy 现在是什么地位

## 6. requirement 回写

- [x] `requirement` 为空，且本 feature 属于 workflow / 工具链结构调整，不是新增最终用户可感能力。
- [x] 结论：无 requirement 回写。

## 7. roadmap 回写

- [x] `roadmap` / `roadmap_item` 两字段都空。
- [x] 结论：非 roadmap 起头，无 roadmap 回写。

## 8. attention.md 候选盘点

- [x] 无候选：本 feature 未暴露新的“一两行每次启动都必须先知道”的项目碎片知识。

## 9. 遗留

- 后续优化点：`cs-feat-design/reference.md` 与 `cs-feat-plan/reference.md` 之间仍可继续收敛成更明确的“文件级 plan 模板”示例，但不影响当前主线成立。
- 已知限制：历史 legacy 目录仍保留为留档兼容读取，尚未做批量清理。
- 实现阶段"顺手发现"列表：无。
