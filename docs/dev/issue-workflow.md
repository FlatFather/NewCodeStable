---
doc_type: dev-guide
slug: issue-workflow
component: cs-issue
status: current
summary: 说明 CodeStable 当前 issue 主线、快速通道、continuation 语义，以及 truth-source 与 generated-state 边界
last_reviewed: 2026-06-25
tags: [workflow, issue, cs-issue, codestable]
---

## 概述

CodeStable 当前的 issue 主线是：

`cs-issue-report → cs-issue-analyze → cs-issue-fix`

其中：
- `report` 只负责把问题现象、复现步骤、期望 vs 实际、环境与严重度落档
- `analyze` 负责读代码定位根因、评估影响面、给 2-3 个修复方案
- `fix` 只在方案已确认后定点修复、验证、写 `fix-note.md`

简单问题可走 issue 快速通道；历史目录继续只作留档兼容读取，不改变当前主线语义。

## 前置依赖

使用这条主线前，项目应已完成 CodeStable 骨架接入，并具备：

- `.codestable/attention.md`
- `.codestable/reference/shared-conventions.md`
- `.codestable/reference/workflow-contract-continuation.md`
- `.codestable/reference/workflow-continuation.md`
- `.codestable/reference/system-overview.md`
- `.codestable/reference/status-schema.md`
- `.codestable/status.json`（可选但推荐；缺失时回退 canonical inspection）

## 快速上手

### 1. 新建一条标准 issue

先走：

- `cs-issue` → 路由判断
- `cs-issue-report` → 产出并确认 `report.md`

此时还**不会**进入修复。

### 2. 进入 analyze 阶段

当用户确认 report 并将 `report.md` 写为 `status: confirmed` 后，同一确认直接进入：

- `cs-issue-analyze`

它会产出：

- `{slug}-analysis.md`

并形成进入修复前的独立确认关口。

如果用户在这条主线中只输入 `继续 / 确认 / 同意 / 按这个修 / 跳过 / 继续下一步` 这类短回复，仓库内 skills 默认先按 **continuation-first** 恢复已有 issue 目录状态，再决定是否重新路由。规范性定义见 `.codestable/reference/workflow-contract-continuation.md`，lane-facing 摘要见 `.codestable/reference/workflow-continuation.md`。

当用户确认修复方案并将 `analysis.md` 写为 `status: confirmed` 时，同一确认自动 handoff 到 `cs-issue-fix`；不会再追加一轮仅重复既有结论的“现在开始修吗”确认。

### 3. 进入 fix 阶段

只有当下面任一入口成立时，才进入：

- `analysis.md` 已存在且方案已确认
- 或快速通道已在 report 阶段完成根因与方案确认

对应阶段：

- `cs-issue-fix`

标准路径中，只要 `analysis.md` 已 confirmed 且唯一 canonical 路径明确，`cs-issue-fix` 会直接开始修复；快速通道中，只要用户已经确认根因与修复方案，后续 continuation 也会直接进入修复。

仍然必须保留的人类拍板点包括：
- issue fix-option / root-cause selection
- scope expansion beyond chosen fix path
- multi-candidate ambiguity
- refactor prerequisites / new concepts / unresolved edge cases that would change scope

## Truth source 与 generated state

issue lane 的真实状态以 `.codestable/issues/{slug}/` 下正式产物为准：

- `report.md`
- `analysis.md`
- `fix-note.md`；标准或带 report 的快速通道只有在 `status: completed` 时才是终态，历史 fix-note-only 记录继续兼容

`status.json` 只是 generated-state discovery spine：
- fresh 时可用于优先发现候选 issue 与阶段
- 缺失、stale、或与 canonical artifacts 冲突时，必须回退到直接读取 issue 目录
- **status.json 派生出的 hint 永远不能压过 canonical artifacts**

`.ccg/tasks/*/task.json` 只作 recovery hint，不得提升为 issue 主 workflow authority。

## 自动 handoff 与保留确认点

### 自动 handoff

以下 handoff 在 canonical artifacts 唯一且无 blocker 时自动发生：

- confirmed issue report → `cs-issue-analyze`
- confirmed issue analysis → `cs-issue-fix`
- 快速通道中已确认根因与修复方案 → `cs-issue-fix`
- continuation 短回复（`继续 / 确认 / 同意 / 按这个修 / 继续下一步`）→ 当且仅当唯一候选存在时，直接续到对应阶段

### 仍然必须保留的确认

以下情况不能自动跳过：

- issue fix-option / root-cause selection
- scope expansion beyond chosen fix path
- multi-candidate ambiguity
- refactor prerequisites / new concepts / unresolved edge cases that change scope

### 兼容性终态记录

历史与快速通道兼容时，只有 `fix-note.md` 的 issue 目录也视为有效终态记录；它是允许保留的 fast-path terminal record，不要求为了补齐形式而强制回填多余产物。

## 快速通道

### 适用条件

仅当以下条件同时满足时，才留在 issue 快速通道：

1. 根因一眼可确认（能明确指出 `file:line` + 原因）
2. 修复改动很小（1-2 处）
3. 无跨模块影响风险

### 自动回标准路径

若在快速通道中出现任一情况，workflow 自动回到标准 issue lane：

- 根因有多个候选
- 需要进一步复现或更多运行时证据
- 修复范围扩张到多模块
- 用户希望保留完整分析档案
- 修复方案已具有标准 analyze 阶段的决策复杂度

触发后不再沿用快速通道硬推到底，而是回 `cs-issue-report` / `cs-issue-analyze` 的标准链路继续。

## 常见场景

### 场景 1：标准 issue

流程：

`cs-issue` → `cs-issue-report` → `cs-issue-analyze` → `cs-issue-fix`

### 场景 2：快速通道

流程：

- `cs-issue-report` 内完成快速判定
- 用户确认根因和修复方案
- `cs-issue-fix` 直接修复与验证

### 场景 3：历史 issue 目录

适用：
- 只是阅读历史留档
- 不继续推进修复

处理方式：
- 可继续只读
- 不要求批量回填新字段

## 相关文档

- `.codestable/reference/shared-conventions.md`
- `.codestable/reference/workflow-contract.md`
- `.codestable/reference/workflow-contract-continuation.md`
- `.codestable/reference/workflow-continuation.md`
- `.codestable/reference/status-schema.md`
- `.codestable/reference/terminology.md`
- `.codestable/architecture/ARCHITECTURE.md`
