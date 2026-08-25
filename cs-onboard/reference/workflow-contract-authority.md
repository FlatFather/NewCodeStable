# Workflow Contract — Authority Ordering

## 目标

定义 CodeStable 工作流中“谁说了算”。

## Authority Ordering

1. `.codestable/` 下的 lane canonical artifacts
2. `.codestable/` 下的共享 reference 契约文档
3. 由 canonical artifacts 确定性生成的只读状态
4. `.ccg/tasks/*/task.json` 与同类 bridge hints
5. 路由摘要、README、教学性说明

该顺序不可交换。generated state 只能汇总 canonical truth，bridge hints 只能辅助恢复上下文。

## Canonical Artifacts

- feature：该 feature 目录下的 design / plan / checklist / acceptance / ff-note 等正式产物
- issue：该 issue 目录下的 report / analysis / fix-note
- refactor：该 refactor 目录下的 scan / design / checklist / apply-notes
- requirements / architecture / roadmap：各自目录中的正式文档

说明：issue 目录中只有 fix-note 的历史 fast-path 兼容记录，属于 compatibility terminal record，不构成 canonical conflict；report 已 confirmed 且 fix-note 未 completed（无 analysis）是进行中的 fast-path，同属 canonical，不是冲突。

## Bridge-Only Artifacts

以下内容只能帮助恢复上下文，不能提升为 authority：

- `.ccg/tasks/*/task.json`（最小字段只保留 `id`、`status`、`canonical_path`、`canonical_kind`；其中 canonical 字段仅建立关联，不能镜像或判定 canonical 阶段）
- `context.jsonl`
- 任何仅为恢复或路由生成的临时索引

## Derived Advisory Fields

generated state 中的以下字段都属于 derived advisory hints，不是新的 authority：

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

- 这些字段只能由 canonical facts 推导。
- 它们可以指导 router 决策顺序，但不能覆盖 canonical artifacts。
- `next_skill` 及相关字段只能表达建议的后续动作，不能单独作为跳转或完成判定依据。
- 一旦 derived advisory fields 与 canonical artifacts、shared contract docs 或 consistency 判定冲突，必须降级为不可采信提示。

## 冲突处理

- canonical artifact 与 bridge hint 冲突 → 以 canonical artifact 为准
- shared reference 摘要与 workflow contract 冲突 → 以 workflow contract 为准
- generated state 与 canonical artifact 冲突 → 视 generated state 为 stale 或 invalid
- fix-note-only issue compatibility terminal record → 视为 compatibility，不视为 canonical conflict

## 路由约束

- 顶层或 lane 路由可以读取 bridge hints 或 generated state 来提速
- 但一旦发现与 canonical artifact 不一致，必须回退到直接读取 canonical artifact
- 不得仅凭 `.ccg/tasks/*/task.json` 判定真实阶段完成度
- 不得仅凭 `next_skill`、`ready_for_next` 或 `auto_continue_allowed` 跳过对 canonical 情况的必要核验
