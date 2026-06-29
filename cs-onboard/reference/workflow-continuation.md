# Workflow Continuation Protocol

本文件改为 **lane-facing 摘要**。continuation-first 的规范性定义现在统一收敛到：

- `workflow-contract-continuation.md`
- `workflow-contract-authority.md`

本文件只保留“哪些 lane 需要关心 continuation”以及“遇到 continuation 时该去读哪里”。

## 先读什么

1. 先读 `workflow-contract-continuation.md` 了解 continuation-first、唯一候选、恢复顺序
2. 再读 `workflow-contract-authority.md` 了解 canonical artifacts 与 bridge hints 的优先级
3. 最后按所在 lane 读取本地技能或指南的阶段说明

## 哪些技能适用

- 顶层入口：`cs`、`cs-feat`、`cs-issue`、`cs-refactor`、`cs-audit`
- feature 阶段：`cs-feat-design`、`cs-feat-plan`、`cs-feat-impl`、`cs-feat-accept`
- issue 阶段：`cs-issue-report`、`cs-issue-analyze`、`cs-issue-fix`

## lane-facing 摘要

- 用户输入像 `继续`、`确认`、`同意` 这类短回复时，先按 workflow contract 做 continuation 检测
- 只有存在唯一候选续作时，才允许自动继续
- `.ccg/tasks/*/task.json` 只作 bridge hint，不替代 `.codestable/` 下正式 workflow 产物

## lane 读取提示

- feature lane：继续前先看该 feature 目录下的正式产物状态
- issue lane：继续前先看该 issue 目录下的正式产物状态
- 顶层入口：只有在 workflow contract 允许时，才可用恢复结果替代普通路由

## 与其他文档的关系

- `shared-conventions.md`：保留 continuation-first 摘要与指针
- `system-overview.md`：保留体系级摘要
- `workflow-contract.md`：规范性入口
- `workflow-contract-continuation.md`：规范性 continuation 语义
- `workflow-contract-authority.md`：规范性 authority ordering
