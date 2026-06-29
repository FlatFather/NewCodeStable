# Workflow Contract — Distribution Semantics

## Source of Shared References

共享 reference 的模板源位于 `cs-onboard/reference/`。

项目内运行时副本位于 `.codestable/reference/`。

## 分发原则

- `cs-onboard/reference/*` 是 shared reference source
- `.codestable/reference/*` 是 repo-local copy
- repo-local copy 应与 source 在语义上保持对齐

## Canonical Form

workflow contract 必须采用：

- 一个入口索引：`workflow-contract.md`
- 多个主题模块：`workflow-contract-*.md`

## 修改规则

- 改共享口径时，先改 `cs-onboard/reference/*`
- 当前仓库若已存在 repo-local copy，需要同步更新 `.codestable/reference/*`
- 其他技能不得把共享契约私藏在自己的 skill 包路径里充当权威副本

## 摘要文档约束

以下文档只能摘要引用契约，不得各自重写规范：

- `shared-conventions.md`
- `system-overview.md`
- `workflow-continuation.md`
- 顶层路由技能摘要
