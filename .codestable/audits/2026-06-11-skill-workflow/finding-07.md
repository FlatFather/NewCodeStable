---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "07"
nature: performance
severity: P2
confidence: medium
title: shared-conventions.md 被多个阶段技能在同一轮对话中重复读取
status: open
tags: [performance, shared-conventions, repetitive-read]
---

# Finding-07: shared-conventions.md 被多个阶段技能重复读取

## 问题描述

`shared-conventions.md`（约 300 行）被多个阶段 skill 引用。在 feature 主线中，design → plan → impl → accept 四个阶段都可能读取同一文件，产生重复上下文成本。

## 证据

**典型场景**：完整 feature 流程
1. `cs-feat-design` 启动检查 → Read `shared-conventions.md`
2. `cs-feat-plan` 启动检查 → Read `shared-conventions.md`
3. `cs-feat-impl` 启动检查 → Read `shared-conventions.md`
4. `cs-feat-accept` 启动检查 → Read `shared-conventions.md`

同一 300 行文件被读取 **4 次**。

## 为什么构成 P2

- 文件较大（300 行），重复读取成本明显
- 但并非每个阶段都需要全文（如 impl 主要用第 7 节反射检查）
- 可通过按需读取或缓存优化

## 建议修复方案

**方案 A：拆分为子文件**
- 把 `shared-conventions.md` 拆为多个主题文件
- 各 skill 只读取需要的部分

**方案 B：会话级缓存**
- 类似 Finding-06，在会话开始时预读

**方案 C：指针化**
- 各 skill 只保留需要的章节指针，按需 Read offset/limit

## 建议动作

走 **`cs-refactor`** 流程（与 Finding-06/08 合并处理）。
