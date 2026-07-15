# status.json Schema

`status.json` 是由 `.codestable/tools/build-status.py` 从 canonical workflow artifacts 确定性生成的只读状态脊柱。

## 目标

- 为顶层发现 / 路由提供快速机读索引
- 汇总当前 workflow lanes 的派生阶段视图
- 明确 generated state、canonical state、bridge hints 的边界
- 为 continuation router 提供受约束的 advisory fields

## 非目标

- 不成为新的 authority
- 不替代 `.codestable/` 下的正式产物
- 不把 `.ccg/tasks/*/task.json` 提升为主 workflow 状态
- 不要求存在 `STATUS.md`

## 顶层结构

```json
{
  "schema_version": "1.2",
  "generator": { ... },
  "authority": { ... },
  "freshness": { ... },
  "bridge_hints": { ... },
  "lanes": { ... },
  "summary": { ... }
}
```

## 顶层字段

### `schema_version`
- 当前 schema 版本
- 生成器与消费方升级时用来做兼容判断

### `generator`
- `name`：生成器文件名
- `version`：生成器实现版本
- `deterministic_sort`：固定为 `true`
- `canonical_roots`：本次生成实际读取的 canonical roots

### `authority`
- `canonical_precedence`：固定为 `true`
- `generated_state_rank`：generated state 在 authority ordering 中的层级
- `bridge_hints_rank`：bridge hints 在 authority ordering 中的层级
- `status_md_required`：固定为 `false`

### `freshness`
- `state`：`fresh | conflict`
- `canonical_digest`：本次 canonical artifact 快照摘要
- `source_count`：参与摘要计算的 canonical 文件数
- `stale_if_digest_changes`：固定为 `true`
- `check_command`：建议消费方如何验证当前 `status.json` 是否过期
- `reasons`：若生成时已发现 canonical 冲突，则列出原因

说明：generated state 的过期判定不依赖 wall-clock 时间，而依赖 canonical digest 是否变化。

### `bridge_hints`
- `included`：固定为 `false`
- `sources`：仅记录 bridge hint 路径模式，说明它们不是生成输入
- `note`：说明 bridge hints 只能辅助恢复，不得覆盖 canonical state

### `lanes`
当前最小覆盖：
- `features`
- `issues`
- `refactors`
- `audits`

每个 lane 包含：
- `count`
- `active_count`
- `items`

### `summary`
- `feature_count`
- `issue_count`
- `refactor_count`
- `audit_count`
- `active_count`
- `compatibility_count`
- `conflict_count`

## Lane Item 结构

```json
{
  "key": "2026-06-05-skill-continuation-first",
  "lane": "features",
  "path": ".codestable/features/...",
  "canonical": { ... },
  "derived": { ... },
  "consistency": { ... }
}
```

### `canonical`
只记录从 canonical artifact 直接读取的事实，例如：
- 产物文件名
- frontmatter 关键字段（`status` / `workflow` / `roadmap` / `roadmap_item` 等）
- checklist 进度统计

### `derived`
只记录从 canonical facts 推导出的 advisory 结论。

#### Required field names
- `stage`
- `active`
- `ready_for_next`
- `canonical_complete`
- `next_skill`
- `auto_continue_allowed`
- `continuation_mode`
- `needs_user_decision`
- `blockers`

#### Field semantics and allowed values
- `stage`：lane-specific 阶段标识字符串；必须可由 canonical artifacts 直接推导
- `active`：`true | false`
- `ready_for_next`：`true | false`
- `canonical_complete`：`true | false`
- `next_skill`：技能名字符串或 `null`；仅 advisory，不可作为 authority
- `auto_continue_allowed`：`true | false`
- `continuation_mode`：`auto | ask_user | terminal`
- `needs_user_decision`：`true | false`
- `blockers`：blocker code 数组，可为空

#### Blocker codes
仅允许以下 blocker codes：
- `terminal_stage`
- `canonical_conflict`
- `missing_required_artifact`
- `awaiting_design_approval`
- `awaiting_plan_approval`
- `awaiting_report_confirmation`
- `awaiting_fix_option_selection`
- `scope_expansion_required`
- `multiple_candidates`
- `ambiguous_next_step`

#### Blocker semantics
- `terminal_stage`：当前记录已到兼容或正式终点，不应继续自动前推
- `canonical_conflict`：canonical artifacts 之间存在显式矛盾
- `missing_required_artifact`：进入下一步所需的 canonical artifact 缺失
- `awaiting_design_approval`：设计已产出但尚未获得进入下一阶段的批准
- `awaiting_plan_approval`：plan/checklist 已产出但执行顺序尚未获得进入实现的批准
- `awaiting_report_confirmation`：issue report 尚未确认，不能进入根因分析
- `awaiting_fix_option_selection`：issue 分析后仍待用户在候选修复方案中做选择
- `scope_expansion_required`：下一步会超出当前已批准范围，必须先扩 scope
- `multiple_candidates`：存在多个合理续作候选，无法唯一恢复
- `ambiguous_next_step`：对象虽唯一，但下一步动作不唯一或无法稳定判定

### `consistency`
- `state`：`clean | compatibility | conflict`
- `reasons`：解释为什么是 compatibility 或 conflict

含义：
- `clean`：canonical 产物之间没有发现内部矛盾
- `compatibility`：历史 / 样板 / legacy 口径被兼容读取，但不作为严格失败
- `conflict`：canonical 产物之间存在必须显式处理的矛盾

兼容说明：issue 目录中只有 fix-note 的 fast-path 终态记录时，可以标记为 `compatibility`，不得仅因此视为 conflict。

## Consumer Obligations

1. `status.json` 只能由 canonical artifacts 生成。
2. `.ccg/tasks/*/task.json` 只能出现在 `bridge_hints` 元数据里，不得参与 lane state 推导。
3. 消费方若发现 `freshness.canonical_digest` 与当前 canonical digest 不一致，必须把 `status.json` 视为 stale，并回退到 canonical inspection。
4. 消费方若发现任一 item 的 `consistency.state = conflict`，不得把该 item 的 derived state 当作最终结论。
5. 消费方只有在以下条件同时成立时，才可据 `derived` 自动切换：
   - `freshness.state == fresh`
   - target `consistency.state != conflict`
   - exactly one eligible candidate exists
   - `derived.auto_continue_allowed == true`
   - `derived.needs_user_decision == false`
   - `blockers` 中不存在 safety-critical blocker
6. 不满足上述条件时，消费方必须询问用户，或把该状态视为 terminal / non-auto-continue。
7. `STATUS.md` 可选；缺失不影响 router 正常工作。
