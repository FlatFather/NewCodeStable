---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "10"
nature: arch-drift
severity: P2
confidence: low
title: system-overview.md 主线描述与 cs-feat 实际阶段表存在微小差异
status: fixed
fixed_by: inline
fixed_date: 2026-06-18
tags: [arch-drift, system-overview, cs-feat, description-mismatch]
---

# Finding-10: system-overview.md 主线描述与 cs-feat 实际阶段表微小差异

## 问题描述

`system-overview.md` 对 feature 主线的描述与 `cs-feat/SKILL.md` 五阶段表存在措辞微小差异。

## 证据

**system-overview.md:18**
> - `cs-feat` — 新功能,design → plan → implement → acceptance

**cs-feat/SKILL.md:46-53（五阶段表）**
> | 阶段 | 子技能 | 产出 | 谁主导 |
> |---|---|---|---|
> | 0 brainstorm（可选） | `cs-brainstorm` | ... | ... |
> | 1 方案设计 | `cs-feat-design` | design.md | ... |
> | 2 执行计划 | `cs-feat-plan` | plan.md + checklist.yaml | ... |
> | 3 分步实现 | `cs-feat-impl` | 代码 + 阶段汇报 | ... |
> | 4 验收闭环 | `cs-feat-accept` | acceptance.md | ... |

**差异**：
- `system-overview` 用"implement"和"acceptance"
- `cs-feat` 用"分步实现"和"验收闭环"

## 为什么构成 P2

- 措辞差异不影响理解
- 但不统一可能让读者困惑是否是两套流程

## 建议修复方案

统一为 `design → plan → impl → accept` 缩写，或统一为中文全称。

## 建议动作

走 **`cs-issue`** 流程（文档微调）。
