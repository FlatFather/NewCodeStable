---
doc_type: dev-guide
slug: feature-workflow
component: cs-feat
status: current
summary: 说明 CodeStable 当前的标准 feature 主线、`cs-feat-plan` 阶段职责，以及 fastforward 与历史 legacy 的边界
last_reviewed: 2026-06-03
tags: [workflow, feature, cs-feat, cs-feat-plan, codestable]
---

## 概述

CodeStable 当前的活跃 feature 主线已经从过去的“design 后直接 impl”演进为显式的：

`cs-feat-design → cs-feat-plan → cs-feat-impl → cs-feat-accept`

其中：
- `design` 只负责确定范围、术语、约束和验收契约
- `plan` 负责把已批准的 design 展开成**文件级改动计划**，并同时生成 `checklist.yaml`
- `impl` 只在 `design + plan + checklist` 都已齐备后才能启动
- `accept` 对照 `design + plan + checklist` 做最终核验

fastforward 继续作为小需求的独立快路径存在；历史 legacy 目录只作留档兼容读取，不再作为新 feature 的活跃标准口径。

## 前置依赖

使用这条主线前，项目应已完成 CodeStable 骨架接入，并具备：

- `.codestable/attention.md`
- `.codestable/reference/shared-conventions.md`
- `.codestable/reference/workflow-contract-continuation.md`
- `.codestable/reference/workflow-continuation.md`
- `.codestable/reference/system-overview.md`
- `.codestable/architecture/ARCHITECTURE.md`

此外，运行项目内 YAML / frontmatter 校验脚本时，优先使用：

```bash
.venv/bin/python .codestable/tools/validate-yaml.py ...
```

## 快速上手

### 1. 新建一条标准 feature

先走：

- `cs-feat` → 路由判断
- `cs-feat-design` → 产出并批准 `design.md`

此时还**不会**进入实现。

### 2. 进入 plan 阶段

当 `design.md` 已 approved 后，进入：

- `cs-feat-plan`

它会生成：

- `{slug}-plan.md`
- `{slug}-checklist.yaml`

并形成进入实现前的独立确认关口。这个关口只确认**执行顺序与步骤切分**，不重复确认已经 approved 的 design 意图。

如果用户在这条主线中只输入 `继续 / 确认 / 同意 / 跳过 / 继续下一步` 这类短回复，仓库内 skills 默认先按 **continuation-first** 恢复已有 feature 目录状态，再决定是否重新路由。规范性定义见 `.codestable/reference/workflow-contract-continuation.md`，lane-facing 摘要见 `.codestable/reference/workflow-continuation.md`。

当 canonical artifacts 唯一表明 `design.md` 已 approved，且 `plan.md + checklist.yaml` 已确认可执行时，后续 handoff 自动进入 `cs-feat-impl`；不会再追加一轮仅重复 design 意图的"要不要开始实现"确认。

### 3. 进入实现阶段

只有当下面三项都齐备时，才进入：

- `design.md`
- `plan.md`
- `checklist.yaml`

对应阶段：

- `cs-feat-impl`

当 canonical artifacts 唯一表明实现前提成立时，`cs-feat-impl` 自动从当前应执行的 step 开始推进；短回复 continuation 不要求额外的"现在开始实现吗"启动确认。

仍然必须保留的人类拍板点包括：
- feature design approval
- scope expansion beyond approved scope
- multi-candidate ambiguity
- refactor prerequisites / new concepts / unresolved edge cases that would change scope

### 4. 进入验收阶段

实现完成后，进入：

- `cs-feat-accept`

它会对照：

- `design.md`
- `plan.md`
- `checklist.yaml`

并补齐：
- 架构归并
- requirement 回写（如需要）
- roadmap 回写（如需要）
- acceptance 报告

当 checklist 已全部完成、实现汇报已输出、且没有 blocker 时，后续 continuation 会自动 handoff 到 `cs-feat-accept`；不会再额外追问一轮"是不是进入验收"。

## 自动 handoff 与保留确认点

### 自动 handoff

以下 handoff 在 canonical artifacts 唯一、fresh 且无 blocker 时自动发生：

- approved feature design → `cs-feat-plan`
- approved feature plan/checklist → `cs-feat-impl`
- completed feature checklist → `cs-feat-accept`
- continuation 短回复（`继续 / 确认 / 同意 / 继续下一步`）→ 当且仅当唯一候选存在时，直接续到对应阶段

### 仍然必须保留的确认

以下情况不能自动跳过：

- feature design approval
- scope expansion beyond approved scope
- multi-candidate ambiguity
- refactor prerequisites / new concepts / unresolved edge cases that change scope

### truth-source 优先级

- `.codestable/features/{slug}/` 下的 `design.md` / `plan.md` / `checklist.yaml` 是 canonical artifacts
- `status.json` 只提供 discovery / routing hint，**永远不能压过 canonical artifacts**
- `status.json` 缺失、stale、或与 feature 目录冲突时，必须回退到直接读取 canonical artifacts
- `.ccg/tasks/*/task.json` 只作 recovery hint，不提升为 workflow authority

## 核心概念

### design

`design.md` 是 **scope source**。

它回答：
- 做什么
- 为什么这么做
- 不做什么
- 术语和约束是什么

它**不负责**写细到每个文件怎么改。

### plan

`plan.md` 是 **step source**。

它承接已批准的 design，重点回答：
- 先做哪一步
- 每一步改哪些文件
- 为什么改这些文件
- 怎么验证这一步完成

plan 的意义不是“把 design 写得更长”，而是提供**文件级改动计划**。

### checklist

`checklist.yaml` 是 **status carrier**。

它记录：
- 执行步骤
- 退出信号
- 检查项状态

它不承载大段说明，说明留在 plan。

## 接口参考

### `cs-feat`

职责：
- 只做 feature 路由判断
- 把用户导向：brainstorm / design / plan / impl / accept / fastforward

### `cs-feat-design`

职责：
- 起草并批准 `design.md`
- 不再直接生成 `plan.md` / `checklist.yaml`

### `cs-feat-plan`

职责：
- 读取 approved design
- 生成 `plan.md`
- 生成 `checklist.yaml`
- 在进入实现前形成独立确认关口

### `cs-feat-impl`

职责：
- 读取 `design + plan + checklist`
- 按 checklist 状态推进实现
- 详细步骤解释以 plan 为准

### `cs-feat-accept`

职责：
- 对照 `design + plan + checklist` 验收
- 补 acceptance 报告
- 完成 architecture / requirement / roadmap 回写（如需要）

## 常见场景

### 场景 1：标准 feature

适用：
- 需要完整 spec 链
- 需要 plan 作为实现前的独立确认关口

流程：

`cs-feat` → `cs-feat-design` → `cs-feat-plan` → `cs-feat-impl` → `cs-feat-accept`

### 场景 2：小需求快路径

适用：
- 改动非常小
- 不值得走完整 spec 主线

流程：

- `cs-feat-ff`

注意：fastforward 是独立快路径，不经过 `cs-feat-plan`。

### 场景 3：历史 legacy 目录

适用：
- 只是阅读历史留档
- 不继续推进实现

处理方式：
- 可继续只读
- 不要求批量回填 `plan.md`

如果历史 feature 要继续推进，应先升级到当前标准主线，再继续后续阶段。

## 已知限制与注意事项

- 当前仓库仍保留历史 legacy 目录，但它们只作留档兼容读取，不再代表活跃标准主线。
- `cs-feat-plan/reference.md` 里的文件级 plan 模板后续仍可继续细化；当前已经足够表达“每个文件怎么改”。
- `workflow-check` 的适用边界仍需与新主线继续同步演进，尤其在“历史 legacy 目录兼容读取”与“新 feature 必须走 plan”之间保持清晰区分。

## 相关文档

- `.codestable/reference/shared-conventions.md`
- `.codestable/reference/workflow-contract-continuation.md`
- `.codestable/reference/workflow-continuation.md`
- `.codestable/reference/system-overview.md`
- `.codestable/architecture/ARCHITECTURE.md`
- `.codestable/features/2026-06-03-feature-plan-stage/feature-plan-stage-design.md`
- `.codestable/features/2026-06-03-feature-plan-stage/feature-plan-stage-plan.md`
- `.codestable/features/2026-06-03-feature-plan-stage/feature-plan-stage-acceptance.md`
