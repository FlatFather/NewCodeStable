---
doc_type: dev-guide
slug: refactor-workflow
component: cs-refactor
status: current
summary: 说明 CodeStable 当前 refactor 主线、fastforward 边界、continuation 语义，以及 truth-source 与 generated-state 边界
last_reviewed: 2026-06-25
tags: [workflow, refactor, cs-refactor, codestable]
---

## 概述

CodeStable 当前的 refactor 主线是：

`cs-refactor → scan → design → apply`

其中：
- `scan` 负责限定范围并产出优化点清单
- `design` 负责把勾选条目组织成执行顺序与 checklist
- `apply` 负责按步骤逐条执行与验证

单函数 / 单组件 / 单文件的小重构可走 refactor fastforward；一旦超出边界，workflow 自动回标准 lane。

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

### 1. 新建一条标准 refactor

先走：

- `cs-refactor` → 路由判断
- `scan` → 产出 `scan.md`

### 2. 进入 design 阶段

当 scan 条目已勾选后，进入：

- `design`

它会生成：

- `{slug}-refactor-design.md`
- `{slug}-checklist.yaml`

并形成进入 apply 前的独立确认关口。

如果用户在这条主线中只输入 `继续 / 确认 / 同意 / 跳过 / 继续下一步` 这类短回复，仓库内 skills 默认先按 **continuation-first** 恢复已有 refactor 目录状态，再决定是否重新路由。规范性定义见 `.codestable/reference/workflow-contract-continuation.md`，lane-facing 摘要见 `.codestable/reference/workflow-continuation.md`。

### 3. 进入 apply 阶段

只有当下面两项都齐备时，才进入：

- `refactor-design.md`
- `checklist.yaml`

对应阶段：

- `apply`

## Truth source 与 generated state

refactor lane 的真实状态以 `.codestable/refactors/{slug}/` 下正式产物为准：

- `scan.md`
- `refactor-design.md`
- `checklist.yaml`
- `apply-notes.md`

`status.json` 只是 generated-state discovery spine：
- fresh 时可用于优先发现候选 refactor 与阶段
- 缺失、stale、或与 canonical artifacts 冲突时，必须回退到直接读取 refactor 目录

`.ccg/tasks/*/task.json` 只作 recovery hint，不得提升为 refactor 主 workflow authority。

## Fastforward 边界

### 留在 `cs-refactor-ff` 的条件

仅当以下条件同时满足时，才继续留在 fastforward：

1. 行为等价是确定前提
2. 改动集中在单函数 / 单组件 / 单文件
3. 优化点 ≤ 3 处
4. 每处改动都能对应到经典重构方法
5. 有测试 / 类型检查 / 既有验证手段可自证
6. 不需要 HUMAN 目视验证，不碰公开接口

### 自动 normalize 到标准 refactor lane

若 fastforward 中出现任一情况，workflow 自动回到标准 refactor lane：

- 改动跨 > 1 文件
- 优化点膨胀到 3 处以上
- 需要 HUMAN 目视或跨模块确认
- 没有测试能覆盖
- 出现行为变更风险或公开接口变化
- 冒出经典 fastforward 方法清单之外的结构级动作

触发后不再继续沿用 fastforward 语义，而是回 `cs-refactor` 从 `scan` 续上。

## 常见场景

### 场景 1：标准 refactor

流程：

`cs-refactor` → `scan` → `design` → `apply`

### 场景 2：小重构快路径

流程：

- `cs-refactor-ff`

注意：fastforward 是独立快路径，不产 scan / design / checklist。

### 场景 3：历史 refactor 目录

适用：
- 只是阅读历史留档
- 不继续推进 apply

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
