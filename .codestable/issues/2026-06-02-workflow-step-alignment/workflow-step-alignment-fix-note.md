---
doc_type: issue-fix
issue: 2026-06-02-workflow-step-alignment
path: fast-track
fix_date: 2026-06-02
tags: [workflow, validation, checklist, plan]
---

# workflow-check step alignment 修复记录

## 1. 问题描述

`workflow-check` 的 `step_alignment` 规则此前只校验 plan step 数量与 checklist step 数量是否相等，没有校验同序位置的步骤是否仍然对齐。结果是：当 checklist 顺序被改乱但步数不变时，校验器仍可能返回通过。

## 2. 根因

`.codestable/tools/validate-yaml.py` 在 `_workflow_check()` 中只执行了 `len(plan_steps) != len(checklist_steps)` 的数量比较，没有继续逐项比较顺序位置上的 step 对应关系。

## 3. 修复方案

保留原有数量检查，在数量一致时新增同序位置校验：逐项比较 `plan_steps[n]` 与 `checklist_steps[n]` 是否仍共享足够的文本锚点；若不对齐，则以 `RULE step_alignment` 返回带步骤序号与双方文本的错误。

## 4. 改动文件清单

- `.codestable/tools/validate-yaml.py`

## 5. 验证结果

- 正常样板 `.codestable/features/2026-06-02-first-hybrid-example/` 运行 `--workflow-check` 通过。
- 人工构造的“顺序错乱但数量相同”故障样板运行 `--workflow-check` 后，稳定报出 `RULE step_alignment`。
- 未修改 workflow-check 的其他规则入口，binding / presence 路径保持原样。

## 6. 遗留事项

- 当前实现补上了顺序对齐与最小文本锚点校验，但没有引入更重的语义理解逻辑；若未来要把“语义一致”也做成强校验，应单独设计规则边界与误报控制。
