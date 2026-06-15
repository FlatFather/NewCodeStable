---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "08"
nature: performance
severity: P2
confidence: low
title: workflow-continuation.md 约 180 行，接近 300 行约束上限
status: open
tags: [performance, workflow-continuation, length-constraint]
---

# Finding-08: workflow-continuation.md 接近长度约束上限

## 问题描述

`workflow-continuation.md` 当前约 180 行，虽未超过项目"单 md 不超 300 行"的硬约束，但已占用 60%。未来扩展空间有限。

## 证据

**当前行数**：180 行（已读取确认）  
**项目约束**：单 md 不超 300 行  
**剩余空间**：120 行

**潜在扩展需求**：
- 新增 refactor / audit 的 continuation 规则（Finding-05）
- 补充更多短回复样例
- 增加恢复失败的兜底规则

## 为什么构成 P2

- 当前未超限，不阻塞功能
- 但预留空间不足，未来扩展需要提前规划
- 超限后需要紧急拆分，成本更高

## 建议修复方案

**方案 A：拆为 base + extensions**
```
workflow-continuation-base.md    (核心原则 + 通用规则，100 行)
workflow-continuation-feat.md    (feature 流程专属规则)
workflow-continuation-issue.md   (issue 流程专属规则)
workflow-continuation-refactor.md (refactor 流程专属规则)
```

**方案 B：提取 FAQ 到独立文件**
- 把"反向边界"、"常见误区"等提取到 `workflow-continuation-faq.md`

**方案 C：保持现状，等超限再拆**
- 当前可控，120 行缓冲足够短期使用

## 建议动作

走 **`cs-refactor`** 流程（与 Finding-06/07 合并处理）。
