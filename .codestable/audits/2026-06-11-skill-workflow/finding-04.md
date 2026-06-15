---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "04"
nature: arch-drift
severity: P1
confidence: high
title: cs-feat-plan 职责边界在不同文档中表述不一致
status: open
tags: [cs-feat-plan, responsibility-boundary, arch-drift]
---

# Finding-04: cs-feat-plan 职责边界在不同文档中表述不一致

## 问题描述

`cs-feat-plan` 作为新增的显式阶段，其职责边界在不同文档中的表述存在微妙差异，容易导致理解混乱。

## 证据

**位置 1：`cs-feat-plan/SKILL.md:12`**
> `cs-feat-plan` 接手后只做一件事：把已批准 design 展开成可执行的 `plan.md`，并从 `design + plan` 抽出 `checklist.yaml`

**位置 2：`shared-conventions.md:146-148`**
> `cs-feat-plan` 基于已批准 design 生成 `plan.md` 与 `checklist.yaml`；design 仍然只决定范围和切片策略，不把 detailed step narrative 塞回 checklist

**位置 3：`cs-feat-design/SKILL.md:12`**
> 后续由 `cs-feat-plan` 基于已批准 design 生成 `{slug}-plan.md` 与 `{slug}-checklist.yaml`

**差异点**：
- 位置 1："从 `design + plan` 抽出 checklist" → 暗示 checklist 派生自两者
- 位置 2："基于 design 生成 plan 与 checklist" + "design 不把 narrative 塞回 checklist" → 暗示 checklist 来自 design，plan 是中间产物
- 位置 3：只说"基于 design 生成"，未明确 checklist 的派生链

**实际派生链**（根据 `feature-plan-stage-design.md` 确认）：
```
design (scope source)
  ↓
cs-feat-plan 生成 plan.md (step source)
  ↓
cs-feat-plan 从 design + plan 抽 checklist.yaml (status carrier)
```

但这条派生链在三处表述中并未统一。

## 为什么构成 P1

**影响范围**：
- skill 维护者：不清楚 plan 阶段到底负责什么
- 用户：在 design / plan / impl 阶段切换时理解产物关系困难

**架构理解风险**：
- 误以为 checklist 只从 design 派生 → 跳过 plan 阶段直接生成 checklist
- 误以为 plan 和 checklist 独立派生 → 不理解两者映射关系

## 建议修复方案

**方案 A（推荐）：统一为标准表述**

在所有涉及 `cs-feat-plan` 的文档中使用统一表述：

> `cs-feat-plan` 基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)；其中 checklist 的 steps 从 design 推进策略切片派生，checks 从 design 各节约束派生。

**方案 B：增加架构图**

在 `shared-conventions.md` 或 `system-overview.md` 增加 feature 产物派生链图：
```
design (scope source) → plan (step source) → checklist (status carrier)
                         ↓                      ↓
                    cs-feat-impl 读取    cs-feat-impl 更新状态
```

**方案 C：合并位置 1/2/3 为单一权威定义**

- 在 `shared-conventions.md` 第 2 节写清楚完整派生链
- 其他 skill 只保留指针："职责边界见 shared-conventions 第 2 节"

## 建议动作

走 **`cs-issue`** 流程：
1. 统一三处表述为方案 A
2. 可选：增加方案 B 的架构图
3. 验证所有相关 skill 职责描述一致
