---
doc_type: issue-report
issue: 2026-06-11-refactor-audit-continuation-missing
status: confirmed
severity: P1
summary: cs-refactor 与 cs-audit 未显式纳入 continuation-first，短回复续作行为与其他 workflow 入口不一致
tags: [workflow, continuation, cs-refactor, cs-audit]
source_audit: .codestable/audits/2026-06-11-skill-workflow/finding-05.md
---

# refactor audit continuation missing Issue Report

## 1. 问题现象

`workflow-continuation.md` 当前适用范围列出了 `cs`、`cs-feat`、`cs-issue` 以及 feature / issue 阶段 skill，但没有列出 `cs-refactor` 与 `cs-audit`。

审计发现：`cs-refactor` 与 `cs-audit` 同样是 CodeStable 工作流入口，但未显式声明 continuation-first 续作规则，导致用户在这些流程中输入“继续”时的行为可能与 feature / issue 不一致。

## 2. 复现步骤

1. 打开 `.codestable/reference/workflow-continuation.md:10-21`。
2. 查看 continuation-first 的适用范围。
3. 打开 `cs/SKILL.md:116-124`、`cs-feat/SKILL.md:89-97`、`cs-issue/SKILL.md:86-96`。
4. 观察到：这些入口已有 continuation-first 规则。
5. 对比 `cs-refactor` 与 `cs-audit` 的工作流定位。
6. 观察到：`workflow-continuation.md` 未把 `cs-refactor` / `cs-audit` 纳入适用范围。

复现频率：稳定。

## 3. 期望 vs 实际

**期望行为**：所有有阶段产物、可中断续作的 CodeStable 工作流入口都明确声明 continuation-first 行为，或明确说明为何排除。

**实际行为**：feature / issue 入口明确支持 continuation-first，refactor / audit 未明确支持或排除。

## 4. 环境信息

- 涉及模块 / 功能：CodeStable continuation-first 续作协议
- 相关文件 / 函数：
  - `.codestable/reference/workflow-continuation.md:10-21`
  - `cs/SKILL.md:116-124`
  - `cs-feat/SKILL.md:89-97`
  - `cs-issue/SKILL.md:86-96`
  - `cs-audit/SKILL.md`
  - `cs-refactor/SKILL.md`
- 运行环境：文档 / skill 工作流维护
- 其他上下文：来源于 `.codestable/audits/2026-06-11-skill-workflow/finding-05.md`

## 5. 严重程度

**P1** — 续作行为是当前 workflow 的核心改进点；同类入口不一致会导致用户体验不稳定，并可能重复执行审计或重构扫描。

## 备注

审计建议将 `cs-refactor` / `cs-audit` 纳入 continuation-first 适用范围，并补对应入口规则；若决定排除，也应在协议中说明理由。具体方案留到 analyze 阶段决定。
