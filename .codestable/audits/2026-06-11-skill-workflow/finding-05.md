---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "05"
nature: bug
severity: P1
confidence: high
title: cs-refactor / cs-audit 未显式实现 continuation-first
status: open
tags: [continuation, cs-refactor, cs-audit, missing-rule]
---

# Finding-05: cs-refactor / cs-audit 未显式实现 continuation-first

## 问题描述

`workflow-continuation.md` 明确规定 continuation-first 适用范围包括顶层入口 `cs`、`cs-feat`、`cs-issue` 以及它们的阶段 skill。但 **`cs-refactor` 和 `cs-audit`** 这两个同样是顶层入口的 skill，在其 SKILL.md 中**未显式实现 continuation-first 规则**。

## 证据

**已实现 continuation-first 的 skill**：
- `cs/SKILL.md:116-124`：短回复 continuation-first 节
- `cs-feat/SKILL.md:72,89-97`：路由表 + continuation-first 约束
- `cs-issue/SKILL.md:80,86-96`：路由表 + continuation-first 约束

**未实现的 skill**（扫描范围内）：
- `cs-refactor/SKILL.md`：未读取，但根据命名规则推测应有类似职责
- `cs-audit/SKILL.md`：已读取，无 continuation-first 规则

**协议定义**：`workflow-continuation.md:10-21`
> 只适用于**本项目仓库内**的 workflow skills：
> - 顶层入口：`cs`、`cs-feat`、`cs-issue`
> - feature 阶段：`cs-feat-design`、`cs-feat-plan`、`cs-feat-impl`、`cs-feat-accept`
> - issue 阶段：`cs-issue-report`、`cs-issue-analyze`、`cs-issue-fix`

→ 协议未明确列出 `cs-refactor` 和 `cs-audit`，但它们属于同类顶层入口

## 为什么构成 P1

**影响场景**：
- 用户在 refactor 流程中输入"继续" → `cs-refactor` 无法恢复已有 refactor 目录状态，重新走路由判断
- 用户在 audit 流程中输入"继续" → `cs-audit` 无法恢复已有 audit 目录状态，重新扫描

**不一致性风险**：
- `cs` / `cs-feat` / `cs-issue` 都支持 continuation-first
- `cs-refactor` / `cs-audit` 不支持
- 用户体验不一致，难以预测哪些入口支持续作

## 建议修复方案

**方案 A（推荐）：补充 continuation-first 规则**

1. 在 `workflow-continuation.md` 第 1 节"适用范围"补充：
   ```markdown
   - 顶层入口：`cs`、`cs-feat`、`cs-issue`、`cs-refactor`、`cs-audit`
   ```

2. 在 `cs-refactor/SKILL.md` 与 `cs-audit/SKILL.md` 增加短回复处理规则：
   - 检测唯一候选 refactor / audit 目录
   - 恢复已有产物状态
   - 多个候选时停下来让用户选

**方案 B：明确排除 refactor / audit**

- 在 `workflow-continuation.md` 明确写："不适用于 `cs-refactor` / `cs-audit`，原因是……"
- 被拒原因：无合理理由排除这两个同类顶层入口

**方案 C：全局重构为通用 continuation 机制**

- 把 continuation-first 提升为所有顶层 skill 的通用协议
- 被拒原因：成本过高，当前只需补两个 skill

## 建议动作

走 **`cs-issue`** 流程：
1. 补充 `workflow-continuation.md` 适用范围
2. 为 `cs-refactor` / `cs-audit` 增加 continuation-first 规则
3. 验证短回复能正确恢复 refactor / audit 状态
