# spec-structure-contract 验收报告

> 阶段：阶段 3（验收闭环）
> 验收日期：2026-06-01
> 关联方案 doc：.codestable/features/2026-06-01-spec-structure-contract/spec-structure-contract-design.md

## 1. 接口契约核对

对照方案第 2.1 节名词层逐一核查。

**接口示例逐项核对**：
- [x] 目录契约示例（`.codestable/reference/shared-conventions.md`、`README.md`、`README.en.md`）：示例里的 `design / plan / checklist / acceptance` 四类产物都已出现，且说明与方案一致。
- [x] frontmatter 示例（`.codestable/reference/shared-conventions.md`）：`feature-plan` 已作为保留术语落入共享约定，未引入第二套 roadmap 状态字段。

**名词层“现状 → 变化”逐项核对**：
- [x] `feature-plan`：从“仓库里没有这一等产物”演进为共享约定中的一等术语，代码改动与方案一致。
- [x] legacy / hybrid feature：共享约定已显式区分两种合法口径，与方案一致。
- [x] `checklist.yaml`：已被重新定义为机器可读状态载体，而不是 narrative plan，与方案一致。
- [x] `acceptance.md`：已被重新定义为对照 design / plan（若存在）/ checklist 的核验与回写报告，与方案一致。

**流程图核对**（第 2.2 节开头 mermaid 图）：
- [x] `feature-design`、可选 `feature-plan`、`checklist`、`feature-impl`、`feature-accept` 在技能文档和共享约定中均有实际落点，流程关系一致。

## 2. 行为与决策核对

对照方案第 1 节 + 第 2.2 节。

**需求摘要逐项验证**：
- [x] 共享约定副本已明确四类产物职责边界与 legacy / hybrid 兼容口径。
- [x] `cs-feat`、`cs-feat-design`、`cs-feat-impl`、`cs-feat-accept` 已对齐新口径。
- [x] 只看项目副本文档与 README，就能分清 scope source、step source、status carrier、verification sink。
- [x] roadmap 起头 feature 仍由 design frontmatter 承载 `roadmap` / `roadmap_item`，plan 没有另起状态机。

**明确不做逐项核对**：
- [x] 没有实现 `feature-plan` 模板生成、校验脚本或自动回写逻辑。
- [x] 没有批量迁移历史 feature 目录，也没有新增“历史 feature 必须补 plan”的规则。
- [x] 没有修改 issue / refactor 流程去依赖 `feature-plan`。
- [x] 没有引入 `.ccg/` 平行真相源。
- [x] 没有在本 feature 中拍板“所有标准 feature 一律强制带 plan”。

**关键决策落地**：
- [x] design 继续做唯一范围源：`cs-feat-design/SKILL.md` 与共享约定都明确了这一点。
- [x] `feature-plan` 先落术语和职责，不落模板与校验：共享约定、README、技能文档均按该决策实现。
- [x] checklist 是状态投影：共享约定第 3 节与 implement / acceptance 文档都已体现。
- [x] acceptance 的输入扩展为 `design + plan(若存在) + checklist`：`cs-feat-accept/SKILL.md` 已体现。
- [x] 兼容策略只前向生效：共享约定与 system-overview 都明确保留 legacy feature 合法性。

**编排层“现状 → 变化”逐项核对**：
- [x] 现状里的 `design → checklist → implement → acceptance` 已保留给 legacy feature。
- [x] 变化里的 `design → plan → checklist → implement → acceptance` 已落成 hybrid 口径说明。
- [x] implement 与 acceptance 的消费边界已按变化同步更新。

**流程级约束核对**：
- [x] scope ownership：共享约定明确 design 是唯一 scope source。
- [x] step ownership：共享约定明确 plan 是 detailed step source，checklist 仅保留机器可读状态。
- [x] compatibility：legacy feature 继续有效。
- [x] writeback discipline：roadmap / requirement / architecture 回写仍在 acceptance。
- [x] observability：读者文档、共享约定、技能文档口径一致。

**挂载点反向核对（可卸载性）**：
- [x] `.codestable/reference/shared-conventions.md`：已按方案修改。
- [x] `cs-feat/SKILL.md`：已按方案修改。
- [x] `cs-feat-design/SKILL.md`：已按方案修改。
- [x] `cs-feat-impl/SKILL.md`：已按方案修改。
- [x] `cs-feat-accept/SKILL.md`：已按方案修改。
- [x] 反向核查：本 feature 的核心口径变更都落在挂载点和第 2.4 节声明的读者视图文件（`system-overview.md`、`README.md`、`README.en.md`）内，无额外挂载点漏记。
- [x] 拔除沙盘推演：按清单逆向撤销这些位置的改动后，`feature-plan / legacy / hybrid` 口径将从系统视角消失，无残留独立入口。

## 3. 验收场景核对

- [x] **S1**：打开 `.codestable/reference/shared-conventions.md`，能直接区分 design、plan、checklist、acceptance 四类产物的职责。
  - 证据来源：手工阅读 + diff
  - 结果：通过
- [x] **S2**：打开 `cs-feat/SKILL.md` 和 `cs-feat-design/SKILL.md`，能看出 hybrid feature 可以有 `feature-plan`，且 design 仍是范围源。
  - 证据来源：手工阅读 + diff
  - 结果：通过
- [x] **S3**：打开 `cs-feat-impl/SKILL.md` 和 `cs-feat-accept/SKILL.md`，能看出 checklist 是状态载体，plan 在存在时是下游输入之一。
  - 证据来源：手工阅读 + diff
  - 结果：通过
- [x] **S4**：文档明确允许没有 `feature-plan` 的 legacy feature 继续有效，不要求历史目录补 plan。
  - 证据来源：grep + 手工阅读
  - 结果：通过
- [x] **S5**：roadmap 起头 feature 的 `roadmap` / `roadmap_item` 口径与 `feature-plan` 共存，不引入第二套状态机。
  - 证据来源：共享约定 + `cs-feat-design/SKILL.md` + roadmap items
  - 结果：通过

本 feature 没有前端 UI 改动，无浏览器肉眼验证项。

## 4. 术语一致性

对照方案第 0 节 + 第 2.1 节命名 grep 代码：

- `feature-plan`：在共享约定、技能文档、README 与设计稿中命名一致。
- `legacy feature` / `hybrid feature`：在共享约定、设计稿和实现文档中命名一致。
- `scope source` / `step source` / `status carrier` / `verification sink`：在共享约定、设计稿和 implement 文档中命名一致。
- 防冲突：未发现与 `.ccg/` 或 issue / refactor 流程耦合的同名新概念。

## 5. 架构归并

- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已写入 `feature-design`、`feature-plan`、legacy / hybrid feature 等稳定名词。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已写入 feature 主流程从 legacy 主线扩展到可选 hybrid plan 层的动词骨架。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已写入 design 是唯一 scope source、acceptance 负责回写等跨 feature 稳定约束。

归并完成后，只看 `ARCHITECTURE.md` 已能知道系统存在 hybrid feature 口径以及它和 legacy feature 的关系。

## 6. requirement 回写

- [x] `requirement` 为空，且本 feature 没有新增最终用户可感能力，而是在整理工作流契约。
- [x] 结论：无 requirement 回写。

## 7. roadmap 回写

- [x] 方案 frontmatter 同时含 `roadmap: workflow-hybridization` 与 `roadmap_item: spec-structure-contract`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-items.yaml` 已将该条目从 `in-progress` 改为 `done`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md` 已同步把子 feature 清单中的状态改为 `done`，对应 feature 改为 `2026-06-01-spec-structure-contract`。
- [x] roadmap items YAML 已重新校验。

## 8. attention.md 候选盘点

- [x] 无候选：本 feature 未暴露需要补入 attention.md 的内容。

## 9. 遗留

- 后续优化点：继续推进 roadmap 中的 `execution-plan-artifact`、`feature-handoff-contract`、`plan-validation-rules`。
- 已知限制：当前只完成了术语与职责边界落盘，尚未实现 `feature-plan` 模板、校验脚本与自动化写回。
- 实现阶段顺手发现：`README.md` / `README.en.md` 与项目副本文档存在重复维护关系，后续可考虑单独做文档同步类 refactor。
