---
doc_type: issue-report
issue: 2026-06-11-feat-plan-boundary-drift
status: confirmed
severity: P1
summary: cs-feat-plan 的职责边界在多个文档中表述不一致，可能导致 plan/checklist 派生关系理解错误
tags: [workflow, cs-feat-plan, arch-drift, documentation]
source_audit: .codestable/audits/2026-06-11-skill-workflow/finding-04.md
---

# feat plan boundary drift Issue Report

## 1. 问题现象

`cs-feat-plan` 的职责边界在 `cs-feat-plan/SKILL.md`、`cs-feat-design/SKILL.md` 和 `.codestable/reference/shared-conventions.md` 中表述不完全一致。

审计发现：不同文档对 `plan.md` 与 `checklist.yaml` 的派生关系描述存在微妙差异，可能让维护者误解 checklist 是只从 design 派生，还是从 design + plan 派生。

## 2. 复现步骤

1. 打开 `cs-feat-plan/SKILL.md:12`。
2. 打开 `.codestable/reference/shared-conventions.md:146-148`。
3. 打开 `cs-feat-design/SKILL.md:12`。
4. 对比三处对 `cs-feat-plan` 的职责描述。
5. 观察到：三处都说 plan 阶段生成 `plan.md` 与 `checklist.yaml`，但对 checklist 的派生链描述不完全一致。

复现频率：稳定。

## 3. 期望 vs 实际

**期望行为**：所有文档对 `cs-feat-plan` 的职责边界使用同一套标准表述，明确 design 是 scope source、plan 是 step source、checklist 是 status carrier。

**实际行为**：三处表述存在微妙差异，未形成统一标准句式或派生链图。

## 4. 环境信息

- 涉及模块 / 功能：feature 标准主线中的 `cs-feat-plan` 阶段
- 相关文件 / 函数：
  - `cs-feat-plan/SKILL.md:12`
  - `.codestable/reference/shared-conventions.md:146-148`
  - `cs-feat-design/SKILL.md:12`
- 运行环境：文档 / skill 工作流维护
- 其他上下文：来源于 `.codestable/audits/2026-06-11-skill-workflow/finding-04.md`

## 5. 严重程度

**P1** — `cs-feat-plan` 是标准 feature 主线的关键阶段，职责边界不一致会影响 design → plan → impl 的执行理解。

## 备注

审计建议统一为标准表述，并可选增加 feature 产物派生链图。具体方案留到 analyze 阶段决定。
