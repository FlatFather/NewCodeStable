# Workflow Contract — Generated State Semantics

## 定义

generated state 指从 canonical workflow artifacts 确定性生成的派生态，例如后续阶段使用的 `status.json`。

## 职责

- 加速顶层发现与路由
- 汇总当前 workflow 状态
- 暴露可机读但不新增 authority 的视图
- 以 `status.json` 形式承载 freshness / consistency / derived advisory hints / bridge-hint boundary

## 非职责

- 不定义新的 workflow 真相
- 不替代 `.codestable/` 下的 canonical artifacts
- 不从 `.ccg/tasks/*/task.json` 推导出比 canonical artifacts 更高的权威结论
- 不把 derived fields 升格为独立决策 authority

## 可暴露的派生字段

generated state 可以暴露以下 derived fields：

- `stage`
- `active`
- `ready_for_next`
- `canonical_complete`
- `next_skill`
- `auto_continue_allowed`
- `continuation_mode`
- `needs_user_decision`
- `blockers`

约束：

- 这些字段都必须由 canonical facts 确定性推导。
- 字段缺失应表示“无法可靠推导”，不能用 bridge hints 补齐成确定结论。
- `next_skill` 与相关字段只表示 advisory routing hint。
- `blockers` 只列出由 canonical state 或 consistency 判定直接导出的阻塞原因。

## 使用规则

- generated state 必须可由 canonical artifacts 重新生成。
- 消费方可以优先读取 generated state，但必须接受回退到 canonical artifacts。
- `status.json` 必须显式区分 canonical facts、derived state、consistency、bridge-hint boundary metadata。
- 一旦 generated state 缺失、过期、矛盾或无法验证，就视为不可用。

## 全局 Auto-Switch Predicate

automatic continuation 仅当以下条件同时成立时允许：

- `freshness.state == fresh`
- target `consistency.state != conflict`
- exactly one eligible candidate exists
- `derived.auto_continue_allowed == true`
- `derived.needs_user_decision == false`
- 不存在 safety-critical blocker

否则，消费方必须询问用户，或把该状态视为 terminal / non-auto-continue。

## Safety-Critical Blockers

以下 blocker 一旦出现，不能自动继续：

- `canonical_conflict`
- `missing_required_artifact`
- `awaiting_design_approval`
- `awaiting_fix_option_selection`
- `scope_expansion_required`
- `multiple_candidates`
- `ambiguous_next_step`

`terminal_stage` 不是冲突，但它会把当前对象归入 terminal，不允许继续自动前推。

## 失效条件

以下情况视为 generated state stale 或 invalid：

- canonical digest 已变化，导致 `freshness.state` 不再可验证为 `fresh`
- 与 canonical artifacts 的阶段、对象、状态相冲突
- target `consistency.state == conflict`
- 依赖 bridge hints 才能成立
- derived fields 无法由 canonical facts 稳定重建

说明：generated state 的可用性不依赖 wall-clock 时间，而依赖 canonical 输入是否仍一致。

## 兼容口径

- issue 目录中只有 fix-note 的历史 fast-path 记录，属于有效 compatibility terminal record。
- 这类记录可以使 `consistency.state = compatibility`，但不得被标记为 `canonical_conflict`。

## 优先级

- canonical artifacts > generated state
- workflow contract > generated state 摘要
