# migration-guidance 验收报告

> 阶段：阶段 3（验收闭环）
> 验收日期：2026-06-02
> 关联方案 doc：.codestable/features/2026-06-02-migration-guidance/migration-guidance-design.md

## 1. 接口契约核对

对照方案第 2.1 节名词层逐一核查。

**接口示例逐项核对**：
- [x] “旧 feature 保持原样”示例：已明确历史目录缺 plan / 缺 workflow marker 时不自动改。
- [x] “重开 legacy”示例：已明确补 `workflow: legacy` 即可继续老口径。
- [x] “重开 hybrid”示例：已明确补 `workflow: hybrid` + 真实 `plan.md`。

**名词层“现状 → 变化”逐项核对**：
- [x] legacy repository：已从隐含背景升级为明确术语。
- [x] migration guidance：已在共享约定、技能文档和样例文件中形成真实指导。
- [x] forward-only adoption：已在共享约定中明确为默认迁移总则。
- [x] historical backfill / minimal backfill：已明确只在重开时补最小必要产物。

**流程图核对**（第 2.2 节开头 mermaid 图）：
- [x] 历史 feature → 是否重开 → 原样 / 重开 legacy / 升级 hybrid 的流程分岔，在 shared conventions、design skill 和 samples 中均有实际落点。

## 2. 行为与决策核对

对照方案第 1 节 + 第 2.2 节。

**需求摘要逐项验证**：
- [x] 共享约定中已明确 legacy 仓库与历史 feature 的默认处理原则。
- [x] 已定义 3 种迁移场景：原样保持、重开 legacy、重开 hybrid。
- [x] design / acceptance / tools 在读历史 feature 时已明确不误报“缺 plan 就非法”。
- [x] 用户可通过样例判断是否需要回填以及回填到什么程度。

**明确不做逐项核对**：
- [x] 没有实现批量迁移脚本。
- [x] 没有自动扫描并重写历史 feature 目录。
- [x] 没有要求所有现有仓库立刻补 `workflow` 或 `plan.md`。
- [x] 没有处理 issue / refactor 的历史迁移。
- [x] 没有实现跨仓库迁移控制台或 dashboard。

**关键决策落地**：
- [x] forward-only：共享约定已明确新协议默认只约束新 feature 或显式重开的 feature。
- [x] minimal backfill：样例和 design/acceptance 说明都只要求补最小必要字段。
- [x] workflow marker 只对新设计或重开设计要求显式写出：shared conventions 已明确历史 design 缺字段不算错。
- [x] migration guidance 是 read-before-act 规则：本次改动没有自动修复器。

**编排层“现状 → 变化”逐项核对**：
- [x] 现状里的“规则已能区分 legacy/hybrid，但缺迁移指导”判断成立。
- [x] 变化里的三种迁移分岔已落成真实文本与样例。
- [x] workflow-check 的适用边界已被迁移指导收紧，不再默认覆盖所有历史目录。

**流程级约束核对**：
- [x] forward-only：未见自动追溯改老 feature 的逻辑。
- [x] minimal backfill：重开时只补继续走流程所需最小产物。
- [x] explicit marker for new work：新设计和重开的设计才要求显式 `workflow`。
- [x] no silent upgrade：acceptance 文档已明确不能静默把 legacy 升级成 hybrid。

**挂载点反向核对（可卸载性）**：
- [x] `.codestable/reference/shared-conventions.md`：已按方案修改。
- [x] `.codestable/reference/tools.md`：已补 workflow-check 的历史适用边界。
- [x] `cs-feat-design/SKILL.md`：已补“历史 feature 重开”入口。
- [x] `cs-feat-accept/SKILL.md`：已补重开场景下的验收说明。
- [x] `.codestable/features/2026-06-02-migration-guidance/`：已新增 design/checklist/samples 三件套样例。
- [x] 反向核查：没有新增迁移脚本、批处理工具或第二套状态文件。
- [x] 拔除沙盘推演：撤销上述挂载点后，系统会退回“只有新规则、没有迁移指导”的状态，无残留迁移入口。

## 3. 验收场景核对

- [x] **S1**：共享约定能回答历史 feature 默认是否需要补 plan / workflow marker。
  - 证据来源：手工阅读 + diff
  - 结果：通过
- [x] **S2**：`cs-feat-design` 能在旧 feature 重开时给出明确迁移路径。
  - 证据来源：手工阅读 + diff
  - 结果：通过
- [x] **S3**：workflow-check 的适用边界对历史未重开的 feature 足够清晰，不会误伤。
  - 证据来源：tools 说明 + shared conventions
  - 结果：通过
- [x] **S4**：重开 legacy 与重开 hybrid 的最小补写清单明确。
  - 证据来源：样例文件 + design
  - 结果：通过
- [x] **S5**：迁移指导样例足够让用户人工判断自己的 feature 属于哪条路径。
  - 证据来源：migration-guidance-samples.md
  - 结果：通过

本 feature 没有前端 UI 改动，无浏览器肉眼验证项。

## 4. 术语一致性

对照方案第 0 节 + 第 2.1 节命名 grep 代码：

- `legacy repository`：在 design 与 acceptance 中命名一致。
- `migration guidance`：在 design、samples 与 acceptance 中命名一致。
- `forward-only adoption` / `minimal backfill`：在 design、shared conventions 和 acceptance 中命名一致。
- 防冲突：未发现把历史缺字段直接当作错误的矛盾表述。

## 5. 架构归并

- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已补充 `legacy repository`、`forward-only adoption`、`minimal backfill` 三个稳定名词。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已补充“历史 feature 保持原样，重开时再选择 legacy/hybrid 路径”的动词骨架。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已补充“workflow-check 不应误伤未重开的历史产物”的流程级约束。

归并完成后，只看 `ARCHITECTURE.md` 已能理解新旧工作流并存时的迁移策略。

## 6. requirement 回写

- [x] `requirement` 为空，且本 feature 没有新增最终用户可感能力，而是在细化工作流迁移策略。
- [x] 结论：无 requirement 回写。

## 7. roadmap 回写

- [x] 方案 frontmatter 同时含 `roadmap: workflow-hybridization` 与 `roadmap_item: migration-guidance`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-items.yaml` 已将该条目从 `in-progress` 改为 `done`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md` 已同步把子 feature 清单中的状态改为 `done`，对应 feature 改为 `2026-06-02-migration-guidance`。
- [x] roadmap items YAML 已重新校验。

## 8. attention.md 候选盘点

- [x] 无候选：本 feature 未暴露需要补入 attention.md 的内容。

## 9. 遗留

- 后续优化点：只剩最后一条 `first-hybrid-example`。
- 已知限制：迁移指导已经落盘，但仍依赖用户按样例手工判断场景，不会自动识别某条历史 feature 属于哪类。
- 实现阶段顺手发现：无新增顺手发现。
