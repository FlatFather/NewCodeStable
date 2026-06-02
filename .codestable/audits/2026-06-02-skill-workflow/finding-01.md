---
doc_type: audit-finding
audit: 2026-06-02-skill-workflow
finding_id: "bug-01"
nature: bug
severity: P1
confidence: high
suggested_action: cs-issue
status: open
---

# Finding 01：workflow-check 的 step_alignment 只校验数量，未覆盖文档承诺的顺序/语义

## 速答

当前 `workflow-check` 对 plan/checklist 的 `step_alignment` 只检查“数量相等”，没有检查“顺序一致”或“目标语义一致”；但多处设计与验收文档都把它描述成更强的保证。这会让一个**顺序错乱但数量相同**的 checklist 被误判为通过。

## 关键证据

- `.codestable/features/2026-06-02-plan-validation-rules/plan-validation-rules-design.md:19` — `plan/checklist alignment` 被定义为“数量、顺序、目标语义上的一致性”。
- `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md:162` — 共享契约明确写了“checklist 中的步骤顺序必须与 plan 对齐”。
- `.codestable/features/2026-06-02-first-hybrid-example/first-hybrid-example-acceptance.md:14` — 验收报告写的是“step 数量和顺序可被 workflow-check 验证通过”。
- `.codestable/tools/validate-yaml.py:329` — 实现只检查 `len(plan_steps) != len(checklist_steps)`，没有做顺序或语义比对。
- `.codestable/tools/validate-yaml.py:244` 与 `.codestable/tools/validate-yaml.py:248` — 代码虽然分别解析了 plan step 标题和 checklist action，但后续没有逐项比对。

## 影响

影响的是 workflow contract 校验的可信度，而不是单个样板文档。只要有人把 checklist 步骤顺序改乱但保留相同步数，`workflow-check` 仍可能返回通过，导致 implement / acceptance 误以为流程契约完好。对这套“先文档约束，再工具兜底”的体系来说，这是核心防线缺口。

## 修复方向

把 `step_alignment` 从“仅比数量”提升为“至少比顺序映射”，最低限度逐项比对 `plan_steps[n]` 与 `checklist_steps[n]`；若不准备做语义比对，就同步收缩文档承诺。

## 建议动作

`cs-issue`，因为这是一个真实的协议校验缺口，且代码实现与文档承诺已经发生偏差。