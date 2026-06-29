# Workflow Contract — Shared Concepts

## Active Workflow

active workflow 指当前仓库正在使用并要求新文档遵守的工作流规则集合。

## Lane

lane 指一类有独立正式产物和阶段语义的主线流程，例如：

- feature
- issue
- refactor
- audit

## Canonical Artifact

canonical artifact 指 `.codestable/` 中能直接表达真实 workflow 状态的正式文档或清单。

## Bridge Hint

bridge hint 指只为恢复上下文、定位续作、提升可发现性而存在的辅助状态；它不是 authority。

## Generated State

generated state 指从 canonical artifacts 推导出的只读派生态，用于索引、汇总和加速消费。

## Router-Facing Summary

router-facing summary 指 `cs/SKILL.md`、`system-overview.md` 一类面向入口路由的说明文本。它们可以解释入口行为，但不拥有独立规范权。

## Shared Reference Source

shared reference source 指 `cs-onboard/reference/` 中由 onboard 复制到项目的模板来源。

## Repo-Local Copy

repo-local copy 指当前项目下 `.codestable/reference/` 的运行时共享参考副本。

## Normative vs Summary

- normative：定义必须遵守的规则
- summary：为路由、教学或导航提供压缩表达

workflow contract 模块属于 normative；大多数路由说明属于 summary。
