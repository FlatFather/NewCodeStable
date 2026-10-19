# plan-validation-rules 验收报告

> 阶段：阶段 3（验收闭环）
> 验收日期：2026-06-02
> 关联方案 doc：.codestable/features/2026-06-02-plan-validation-rules/plan-validation-rules-design.md

## 1. 接口契约核对

对照方案第 2.1 节名词层逐一核查。

**接口示例逐项核对**：
- [x] workflow-check CLI 示例（`.codestable/reference/tools.md`）：已存在 `--feature-dir`、`--roadmap`、`--workflow-check` 调用形式。
- [x] 失败输出示例（设计 doc 第 2.1 节）：实现后的校验器已能输出 `RULE {rule}` + 文件路径 + 原因 的结构化错误。

**名词层“现状 → 变化”逐项核对**：
- [x] validation rule：从“只能校验 YAML/frontmatter 语法”升级为“能校验 workflow contract 语义”。
- [x] plan/checklist alignment：已落成真实 `step_alignment` 规则。
- [x] roadmap binding check：已落成真实 `roadmap_binding` 规则。
- [x] validator output：`ValidationResult` 已带 rule_results，文本输出可见规则名、文件、原因。

**流程图核对**（第 2.2 节开头 mermaid 图）：
- [x] 读取 feature 目录 → 识别 design/checklist/plan → 读取 roadmap item 绑定 → 执行规则集 → 输出 pass/fail，这条链路在 `validate-yaml.py` 中有实际落点。

## 2. 行为与决策核对

对照方案第 1 节 + 第 2.2 节。

**需求摘要逐项验证**：
- [x] 已有一个可执行入口能检查 plan/checklist/roadmap 绑定关系。
- [x] 校验输出能明确指出规则名、失败文件和错误原因。
- [x] legacy feature 不会因没有 `plan.md` 被误报失败。
- [x] hybrid feature 缺 plan、绑定不一致、step 不一致时会报错。

**明确不做逐项核对**：
- [x] 没有做 IDE 插件、浏览器界面或实时监听。
- [x] 没有重写整个 `.codestable/tools/` 工具栈，而是扩展现有 `validate-yaml.py`。
- [x] 没有批量修复历史 feature，只负责发现问题。
- [x] 没有处理 issue / refactor 的文档校验。

**关键决策落地**：
- [x] 复用现有 `validate-yaml.py`：本次没有新增平行 `validate-plan.py`。
- [x] 规则按协议口径分层：已落 `design_workflow`、`plan_presence`、`binding_rule`、`step_alignment`。
- [x] legacy 默认通过、hybrid 严格检查：通过样板与故障样板都已验证。
- [x] 输出对 AI agent 友好：错误文本已包含规则名、文件、失败原因。

**编排层“现状 → 变化”逐项核对**：
- [x] 现状里的“只校验 parse”仍保留为基础层。
- [x] 变化里的“文件语法 + 协议语义双层校验”已落在 workflow-check 模式。
- [x] 工具已根据 design frontmatter 的 `workflow` 标记区分 legacy / hybrid。

**流程级约束核对**：
- [x] backward-compatible：legacy feature 无 `plan.md` 不会误报。
- [x] strict for hybrid：hybrid 缺 plan、绑定不一致、step 不对齐会报错。
- [x] read-only validation：工具只报告，不自动改写文档。
- [x] deterministic：同一输入反复执行输出稳定一致。

**挂载点反向核对（可卸载性）**：
- [x] `.codestable/tools/validate-yaml.py`：已按方案扩展。
- [x] `.codestable/reference/tools.md`：已补 workflow-check 用法。
- [x] `.codestable/reference/shared-conventions.md`：已补“workflow-check 也应理解 plan presence rule”的说明。
- [x] `.codestable/features/2026-06-02-plan-validation-rules/`：当前 feature 样板已存在。
- [x] 通过样板 `2026-06-01-execution-plan-artifact/` 与故障样板 `2026-06-02-validation-failure-sample/` 已作为验证路径使用。
- [x] 反向核查：没有新增新的状态字段来配合校验器工作，只补了 `workflow: legacy|hybrid` 标记作为最小机器可读信号。
- [x] 拔除沙盘推演：移除 workflow-check 扩展和样板后，系统会退回“只能人工 review 协议一致性”的旧状态，无额外残留入口。

## 3. 验收场景核对

- [x] **S1**：校验器能区分 legacy / hybrid，不会把 legacy feature 缺 plan 误报为错误。
  - 证据来源：类型/脚本行为 + 通过样板验证
  - 结果：通过
- [x] **S2**：hybrid feature 缺 `plan.md` 时，校验器能给出明确失败信息。
  - 证据来源：故障样板运行结果
  - 结果：通过，稳定报 `RULE plan_presence`
- [x] **S3**：design / plan / checklist / roadmap item 绑定不一致时，校验器能指出具体文件和规则名。
  - 证据来源：工具逻辑 + 失败输出格式
  - 结果：通过，支持 `RULE roadmap_binding` / `RULE binding_rule`
- [x] **S4**：plan step 与 checklist step 不一致时，校验器能指出对齐失败。
  - 证据来源：工具逻辑
  - 结果：通过，支持 `RULE step_alignment`
- [x] **S5**：现有真实样板 feature 能通过新规则校验。
  - 证据来源：`execution-plan-artifact` 运行 workflow-check 通过
  - 结果：通过

本 feature 没有前端 UI 改动，无浏览器肉眼验证项。

## 4. 术语一致性

对照方案第 0 节 + 第 2.1 节命名 grep 代码：

- `validation rule`：在 design、acceptance 和工具实现语义中一致。
- `plan/checklist alignment`：在 design 与 `step_alignment` 规则中一致。
- `roadmap binding check`：在 design 与 `roadmap_binding` 规则中一致。
- `validator output`：在设计说明与 `ValidationResult.rule_results` 输出中一致。
- 防冲突：未发现把校验器写成自动修复器的表述。

## 5. 架构归并

- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已补充 `workflow-check` 名词。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已补充“从人工 review 协议一致性升级到工具先做预检查”的动词骨架。
- [x] 架构 doc `.codestable/architecture/ARCHITECTURE.md`：已补充“workflow-check 只报告不改写”的流程级约束。

归并完成后，只看 `ARCHITECTURE.md` 已能知道系统中存在一层工作流协议校验器。

## 6. requirement 回写

- [x] `requirement` 为空，且本 feature 没有新增最终用户可感能力，而是在细化工作流工具链。
- [x] 结论：无 requirement 回写。

## 7. roadmap 回写

- [x] 方案 frontmatter 同时含 `roadmap: workflow-hybridization` 与 `roadmap_item: plan-validation-rules`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-items.yaml` 已将该条目从 `in-progress` 改为 `done`。
- [x] `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md` 已同步把子 feature 清单中的状态改为 `done`，对应 feature 改为 `2026-06-02-plan-validation-rules`。
- [x] roadmap items YAML 已重新校验。

## 8. attention.md 候选盘点

- [x] 无候选：本 feature 未暴露需要补入 attention.md 的内容。

## 9. 遗留

- 后续优化点：继续推进 roadmap 中的 `migration-guidance`、`first-hybrid-example`。
- 已知限制：workflow-check 已能校验 binding / presence / step alignment，但故障样板仍是人工维护，不是自动生成。
- 实现阶段顺手发现：无新增顺手发现。
