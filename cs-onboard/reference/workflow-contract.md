# Workflow Contract

本文件是当前仓库内 CodeStable 工作流契约的唯一总入口。凡是描述 truth source、continuation、generated state、分发同步、跨 lane 共用语义的规范性规则，都以这里及其模块为准。

## 适用范围

- 当前仓库内的 `.codestable/reference/*`
- 顶层路由技能摘要
- lane 说明文档中的规范性引用

## 读取顺序

1. `workflow-contract-shared-concepts.md`
2. `workflow-contract-authority.md`
3. `workflow-contract-continuation.md`
4. `workflow-contract-generated-state.md`
5. `workflow-contract-distribution.md`

## 模块边界

- `workflow-contract-shared-concepts.md`
  - 定义 lane、canonical artifact、bridge hint、generated state、router-facing summary 等跨 lane 共用概念
- `workflow-contract-authority.md`
  - 定义 authority ordering、truth-source 边界、冲突处理优先级，以及 derived advisory fields 的降级规则
- `workflow-contract-continuation.md`
  - 定义 continuation-first、唯一候选约束、何时允许自动继续、何时必须向用户询问
- `workflow-contract-generated-state.md`
  - 定义 generated state 的职责、可暴露字段、失效条件、只读消费规则
- `workflow-contract-distribution.md`
  - 定义 shared reference source、repo-local copy、同步要求与禁止事项

## 使用规则

- 其他文档可以保留摘要，但不得重写这里已定义的规范性规则。
- 其他文档若需要提及规范，优先写“摘要 + 指针”，不要复制完整条款。
- 当契约模块与非契约文档表述冲突时，以本契约模块为准。
- automatic continuation 的规范性语义只定义在 `workflow-contract-continuation.md` 与 `workflow-contract-generated-state.md`；其他文档只可引用，不可另立口径。

## 非目标

- 不定义各 lane 的详细执行模板
- 不替代 `shared-conventions.md` 的目录与 frontmatter 规则
- 不替代用户指南中的教学性示例
