---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "06"
nature: performance
severity: P2
confidence: medium
title: .codestable/attention.md 在每个技能启动时都重复读取
status: fixed
fixed_by: inline
fixed_date: 2026-06-18
notes: 所有技能已实现"缓存优化"机制 - 已在本轮对话读取的文件跳过重复 Read
tags: [performance, context-cost, attention-md, repetitive-read]
---

# Finding-06: attention.md 在每个技能启动时都重复读取

## 问题描述

所有 skill 的"启动必读"都要求读取 `.codestable/attention.md`。在单轮对话中连续触发多个 skill 时，同一文件被重复读取多次，增加 AI 上下文成本。

## 证据

**典型场景**：用户输入"做新功能 X"
1. `cs` 入口 → Read `attention.md`
2. 路由到 `cs-feat` → Read `attention.md`
3. 路由到 `cs-feat-design` → Read `attention.md`

同一文件被读取 **3 次**。

**文件大小**：当前 `attention.md` 约 25 行，成本可控；但项目注意事项累积后可能增长到 100+ 行。

## 为什么构成 P2

- 当前成本低，不阻塞功能
- 但累积读取成本随 skill 链路长度线性增长
- 未来 `attention.md` 增长后成本更明显

## 建议修复方案

**方案 A：skill 入口预加载**
- 在会话开始时预读 `attention.md`，缓存到上下文
- 各 skill 启动检查时跳过重复读取

**方案 B：链式传递上下文**
- 顶层 skill 读取后传递给子 skill
- 需要修改 skill 调用协议

**方案 C：保持现状**
- 当前成本可接受
- 等 `attention.md` 超过 50 行再优化

## 建议动作

走 **`cs-refactor`** 流程（与 Finding-07/08 合并处理）。
