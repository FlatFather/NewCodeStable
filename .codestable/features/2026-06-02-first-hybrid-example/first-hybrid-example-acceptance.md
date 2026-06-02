# first-hybrid-example 验收报告

> 阶段：阶段 3（验收闭环）
> 验收日期：2026-06-02
> 关联方案 doc：.codestable/features/2026-06-02-first-hybrid-example/first-hybrid-example-design.md

## 1. 接口契约核对

对照方案第 2.1 节名词层逐一核查。

**接口示例逐项核对**：
- [x] 样板目录目标形态：当前目录已具备 design / plan / checklist / acceptance 四件套。
- [x] frontmatter 示例：design frontmatter 已明确 `workflow: hybrid`、`roadmap`、`roadmap_item`，与方案一致。
- [x] plan frontmatter 与 checklist 映射：当前样板 plan 与 checklist 的 step 数量和顺序可被 workflow-check 验证通过。

**名词层“现状 → 变化”逐项核对**：
- [x] example feature：已从概念变成真实样板目录。
- [x] full hybrid chain：已在当前样板上覆盖 design / plan / checklist / acceptance / 回写全链路。
- [x] golden sample：当前目录已经是仓库里的第一条完整黄金样板。
- [x] sample drift：样板所用口径都直接来自当前 shared conventions / tools / architecture，无平行私有规则。

**流程图核对**（第 2.2 节开头 mermaid 图）：
- [x] 选择真实规则集 → 起样板 design → 生成样板 plan → 生成 checklist → workflow-check → acceptance 回写，这条链在实际产物中都有落点。

## 2. 行为与决策核对

对照方案第 1 节 + 第 2.2 节。

**需求摘要逐项验证**：
- [x] 当前仓库里已存在一条结构完整、状态完整、回写完整的 hybrid 样板 feature。
- [x] 样板引用的口径都来自当前 shared conventions / tools / architecture。
- [x] 只看样板目录即可理解 hybrid 流程的主要产物和阶段关系。
- [x] workflow-check 已在样板目录上通过。

**明确不做逐项核对**：
- [x] 没有引入新的工作流协议。
- [x] 没有把所有历史 feature 重写成样板风格。
- [x] 没有新增教程专用文档类型。
- [x] 没有改 README 或做图形化导航页。

**关键决策落地**：
- [x] 样板优先复用现有真实规则：当前样板直接绑定当前 shared conventions / workflow-check。
- [x] 样板是“真实闭环产物”：使用现有 design/plan/checklist/acceptance 类型，没有另起教程 frontmatter。
- [x] 样板必须绑定当前共享约定：workflow-check 与 acceptance 都已在该目录上跑通。

**编排层“现状 → 变化”逐项核对**：
- [x] 现状里的“用户需要拼多条 feature 才能理解完整 hybrid 闭环”已被这条样板改进。
- [x] 变化里的关键节点（design、plan、checklist、workflow-check、acceptance 回写）都在同一目录中形成闭环。

**流程级约束核对**：
- [x] real-current-rules only：样板没有绕开当前共享约定。
- [x] single-source example：当前目录自身已经足够展示完整 hybrid 链。
- [x] verifiable sample：workflow-check 和 acceptance 都已通过。

**挂载点反向核对（可卸载性）**：
- [x] `.codestable/features/2026-06-02-first-hybrid-example/`：已按方案创建完整样板目录。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-items.yaml`：已绑定样板目录并推进状态。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md`：已同步样板条目状态。
- [x] `.codestable/architecture/ARCHITECTURE.md`：已归并“存在一条黄金 hybrid 样板”的系统级事实。
- [x] 反向核查：本样板没有引入教程专用文档类型或第二套状态源。
- [x] 拔除沙盘推演：移除该目录及其 roadmap/architecture 引用后，系统只会失去黄金样板，不影响底层规则本身。

## 3. 验收场景核对

- [x] **S1**：样板目录包含 design / plan / checklist / acceptance 四件套。
  - 证据来源：目录核查
  - 结果：通过
- [x] **S2**：样板 design frontmatter 明确 `workflow: hybrid`、`roadmap`、`roadmap_item`。
  - 证据来源：design frontmatter
  - 结果：通过
- [x] **S3**：workflow-check 在样板目录上通过。
  - 证据来源：命令执行
  - 结果：通过
- [x] **S4**：acceptance 完成后，roadmap item 与 architecture 回写都完成。
  - 证据来源：items.yaml、roadmap 主文档、ARCHITECTURE.md
  - 结果：通过
- [x] **S5**：用户只读样板目录，就能理解 hybrid 流程的主要阶段关系。
  - 证据来源：四件套文档内容
  - 结果：通过

本 feature 没有前端 UI 改动，无浏览器肉眼验证项。

## 4. 术语一致性

对照方案第 0 节 + 第 2.1 节命名 grep 代码：

- `example feature` / `golden sample`：在 design 与 acceptance 中命名一致。
- `full hybrid chain`：在 design、plan、acceptance 中命名一致。
- 防冲突：未发现样板绕开当前共享约定的表述。

## 5. 架构归并

- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已归并“存在一条黄金 hybrid 样板”这一系统级事实。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：样板证明 hybrid 流程不是抽象规则集合，而是已有真实闭环实例。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：workflow-check 和 acceptance 都能在样板上跑通。

归并完成后，只看架构总入口即可知道仓库里存在一个当前可参考的黄金样板。

## 6. requirement 回写

- [x] `requirement` 为空，且本 feature 没有新增最终用户可感能力，而是在沉淀工作流样板。
- [x] 结论：无 requirement 回写。

## 7. roadmap 回写

- [x] 方案 frontmatter 同时含 `roadmap: workflow-hybridization` 与 `roadmap_item: first-hybrid-example`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-items.yaml` 已将该条目从 `in-progress` 改为 `done`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md` 已同步把子 feature 清单中的状态改为 `done`，对应 feature 改为 `2026-06-02-first-hybrid-example`。
- [x] roadmap items YAML 已重新校验。

## 8. attention.md 候选盘点

- [x] 无候选：本 feature 未暴露需要补入 attention.md 的内容。

## 9. 遗留

- 后续优化点：无，`workflow-hybridization` roadmap 所有条目均已完成。
- 已知限制：黄金样板依赖当前 shared conventions；后续规则变更后仍需像普通 feature 一样重新验收保持同步。
- 实现阶段顺手发现：无新增顺手发现。
