# feature-handoff-contract 验收报告

> 阶段：阶段 3（验收闭环）
> 验收日期：2026-06-01
> 关联方案 doc：.codestable/features/2026-06-01-feature-handoff-contract/feature-handoff-contract-design.md

## 1. 接口契约核对

对照方案第 2.1 节名词层逐一核查。

**接口示例逐项核对**：
- [x] design frontmatter（design 文档本身 + `cs-feat-design/SKILL.md`）：`roadmap / roadmap_item / feature` 三者都在起手阶段承担绑定作用，和方案一致。
- [x] plan frontmatter 示例（共享约定已有 `doc_type / feature / design / status`）：继续成立，且本次没有引入第二套 plan 状态表。
- [x] roadmap item 示例（items.yaml）：`feature` 字段继续直接绑定到 feature 目录名，和方案一致。

**名词层“现状 → 变化”逐项核对**：
- [x] roadmap item：从“只有状态机字段”升级到“明确作为绑定与状态闭环入口”，改动与方案一致。
- [x] feature directory binding：已在共享约定中成为显式名词，代码改动与方案一致。
- [x] plan presence rule：已在共享约定、implement、acceptance 文档中落成真实门槛，和方案一致。
- [x] handoff contract：当前由 shared conventions + 三份技能文档共同承载，没有旁路协议。

**流程图核对**（第 2.2 节开头 mermaid 图）：
- [x] `planned → design 写 in-progress → hybrid 时 plan 必须存在 → acceptance 写 done` 在共享约定和技能文档中均有实际落点。

## 2. 行为与决策核对

对照方案第 1 节 + 第 2.2 节。

**需求摘要逐项验证**：
- [x] 共享约定已明确 roadmap item、design frontmatter、plan presence rule、acceptance 回写责任之间的关系。
- [x] `cs-feat-design`、`cs-feat-impl`、`cs-feat-accept` 对“什么时候必须存在 plan、什么时候可以没有 plan”说法一致。
- [x] roadmap 起头的 feature 能通过 design frontmatter、feature 目录名和 items.yaml 完成状态闭环，没有第二套状态源。
- [x] acceptance 已明确在 hybrid feature 下核验 plan 是否存在、是否与 design / items 绑定一致。

**明确不做逐项核对**：
- [x] 没有实现自动校验脚本。
- [x] 没有改 roadmap item 的字段集合，也没有新增第二份 plan 专用 yaml。
- [x] 没有决定“所有标准 feature 是否都必须有 plan”。
- [x] 没有处理 issue / refactor 与 roadmap 的衔接。
- [x] 没有做历史 feature 的批量补写与状态回填。

**关键决策落地**：
- [x] roadmap item 仍然只由 design 与 acceptance 写状态：shared conventions 已明确 design 写 `in-progress`、acceptance 写 `done`。
- [x] hybrid feature 的 plan presence rule 由 design 口径和产物存在性共同决定：implement / acceptance 都已把缺 plan 视为失败条件。
- [x] feature 目录名是唯一绑定键：`cs-feat-design/SKILL.md` 与 shared conventions 已明确。
- [x] acceptance 是唯一终态写回点：items.yaml 的 `done` 仍只由 acceptance 负责。

**编排层“现状 → 变化”逐项核对**：
- [x] 现状里的 roadmap → design → acceptance 状态回写骨架仍存在。
- [x] 变化里的三件事——绑定键、plan presence、终态回写——都已落在共享约定和技能文档中。
- [x] implement / acceptance 对 hybrid 口径的启动门槛已经从“可选读取”升级为“缺失即停”。

**流程级约束核对**：
- [x] state ownership：roadmap 状态只允许 design 写 `in-progress`、acceptance 写 `done`。
- [x] binding rule：feature 目录名是跨文档唯一绑定键。
- [x] plan presence：只有 hybrid 口径才强制 plan，一旦强制，缺失即失败。
- [x] no side channel：plan 不单独维护 progress 状态，不写 roadmap item 状态。

**挂载点反向核对（可卸载性）**：
- [x] `.codestable/reference/shared-conventions.md`：已按方案修改。
- [x] `cs-feat-design/SKILL.md`：已按方案修改。
- [x] `cs-feat-impl/SKILL.md`：已按方案修改。
- [x] `cs-feat-accept/SKILL.md`：已按方案修改。
- [x] 当前 feature 目录：design/checklist 样板已存在，可用于人工核验绑定关系。
- [x] 反向核查：没有发现额外挂载点或第二套状态文件。
- [x] 拔除沙盘推演：撤销上述挂载点和当前 feature 目录后，系统会退回“没有显式 handoff contract”的旧状态，无额外残留入口。

## 3. 验收场景核对

- [x] **S1**：共享约定能解释 roadmap item、design frontmatter、plan presence rule、acceptance 回写责任之间的关系。
  - 证据来源：手工阅读 + diff
  - 结果：通过
- [x] **S2**：`cs-feat-design` 说明了 design 阶段必须如何写 `roadmap / roadmap_item / feature` 绑定。
  - 证据来源：手工阅读 + diff
  - 结果：通过
- [x] **S3**：`cs-feat-impl` 说明 hybrid feature 缺 plan 时不能继续。
  - 证据来源：手工阅读 + diff
  - 结果：通过
- [x] **S4**：`cs-feat-accept` 说明验收时要核验 design / plan / items 的三向绑定，并回写 `done`。
  - 证据来源：手工阅读 + diff
  - 结果：通过
- [x] **S5**：当前 feature 目录和 roadmap item 之间的绑定关系可以被人工核验，无第二套状态源。
  - 证据来源：feature 目录 + items.yaml
  - 结果：通过

本 feature 没有前端 UI 改动，无浏览器肉眼验证项。

## 4. 术语一致性

对照方案第 0 节 + 第 2.1 节命名 grep 代码：

- `roadmap item`：在 design、shared conventions、acceptance 报告中命名一致。
- `feature directory binding`：在 design 和 shared conventions 中命名一致。
- `plan presence rule`：在 design、shared conventions、implement、acceptance 中命名一致。
- 防冲突：未发现第二份 plan 状态表或“plan 自己写 roadmap item 状态”的表述。

## 5. 架构归并

- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已补充 `roadmap item`、`feature directory binding`、`plan presence rule` 三个稳定名词。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已补充 design 写 `in-progress`、acceptance 写 `done`、hybrid 下 plan 是 design 与 checklist 之间必经节点的动词骨架。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已补充 plan 不单独维护 progress 状态的稳定约束。

归并完成后，只看 `ARCHITECTURE.md` 已能知道系统里工作流状态交接的主干规则。

## 6. requirement 回写

- [x] `requirement` 为空，且本 feature 没有新增最终用户可感能力，而是在细化工作流交接协议。
- [x] 结论：无 requirement 回写。

## 7. roadmap 回写

- [x] 方案 frontmatter 同时含 `roadmap: workflow-hybridization` 与 `roadmap_item: feature-handoff-contract`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-items.yaml` 已将该条目从 `in-progress` 改为 `done`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md` 已同步把子 feature 清单中的状态改为 `done`，对应 feature 改为 `2026-06-01-feature-handoff-contract`。
- [x] roadmap items YAML 已重新校验。

## 8. attention.md 候选盘点

- [x] 无候选：本 feature 未暴露需要补入 attention.md 的内容。

## 9. 遗留

- 后续优化点：继续推进 roadmap 中的 `plan-validation-rules`、`migration-guidance`、`first-hybrid-example`。
- 已知限制：当前状态交接与绑定协议已落盘，但还没有自动校验脚本保障三向绑定一致性。
- 实现阶段顺手发现：无新增顺手发现。
