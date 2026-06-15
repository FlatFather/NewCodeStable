---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "09"
nature: maintainability
severity: P2
confidence: medium
title: feature / issue 退出条件 checklist 格式不统一
status: open
tags: [exit-condition, checklist-format, consistency]
---

# Finding-09: feature / issue 退出条件 checklist 格式不统一

## 问题描述

各阶段 skill 的退出条件 checklist 格式存在微小差异，部分用 `- [ ]`，部分用纯列表，不利于自动化 lint。

## 证据

**格式 A（标准 Markdown checklist）**：
- `cs-feat-design/SKILL.md:238-249`：使用 `- [ ]` 格式

**格式 B（纯列表）**：
- 部分 skill 使用纯 `-` 列表（未逐一确认）

## 为什么构成 P2

- 不影响功能，但格式不统一
- 无法用自动化工具检查退出条件完整性

## 建议修复方案

**方案 A：统一为 Markdown checklist**
- 所有退出条件用 `- [ ]` 格式
- 可用 markdownlint 自动检查

**方案 B：统一为纯列表**
- 简化格式，去掉 `[ ]`

## 建议动作

走 **`cs-refactor`** 流程（批量统一格式）。
