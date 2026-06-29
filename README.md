<div align="center">

# CodeStable

![](./asset/PromotionalImage.png)

[English](./README.en.md) · **中文**

**面向严肃工程的 AI 编码工作流**

<p>
  <img src="https://img.shields.io/badge/status-beta-F59E0B?style=flat-square" alt="Status"/>
  <img src="https://img.shields.io/badge/skills-22-6366F1?style=flat-square" alt="Skills"/>
  <img src="https://img.shields.io/badge/license-MIT-10B981?style=flat-square" alt="License"/>
</p>

</div>

---

## 安装

```bash
npx skills add https://github.com/FlatFather/NewCodeStable
```

本地开发调试最新版时：

```bash
npx skills add "/Users/kong/self/github/NewCodeStable"
```

升级：

```bash
npx skills update
```

---

## 先怎么开始

### 新仓库 / 还没接入

```bash
/cs-onboard
```

### 已接入，但不知道该用哪个

```bash
/cs
```

`cs` 只做一件事：把你的诉求路由到正确的 `cs-*` 子技能。

---

## CodeStable 是什么

CodeStable 编排的不是 Agent 团队，而是**软件本身的生命周期**。

它把需求、架构、feature、issue、refactor、audit、知识沉淀这些要素，统一落在项目内的 **`.codestable/`** 里，让人和 AI 都能读到同一套工程状态。

### 权威边界

- **canonical state**：`.codestable/` 下的正式产物
- **generated state**：`.codestable/status.json`，只作发现 / 路由加速
- **bridge hints**：`.ccg/tasks/*/task.json`，只作恢复提示

一句话：**canonical artifacts 永远高于 generated state 和 bridge hints**。

规范性定义统一见：
- [`.codestable/reference/workflow-contract.md`](./.codestable/reference/workflow-contract.md)

---

## 工作流概览

### 标准主线

| 场景 | 主线 |
|---|---|
| 新功能 | `cs-feat-design → cs-feat-plan → cs-feat-impl → cs-feat-accept` |
| 修 bug | `cs-issue-report → cs-issue-analyze → cs-issue-fix` |
| 重构 | `cs-refactor`（标准三阶段：scan → design → apply） |
| 主动扫描问题 | `cs-audit` |

### 快路径

- `cs-feat-ff`：小需求的 feature fastforward
- `cs-refactor-ff`：小范围、行为等价的重构 fastforward

### 讨论入口

- `cs-brainstorm`：想法还没收敛时先分诊
- `cs-roadmap`：大需求先拆 roadmap，再拆子 feature

> fastforward 只在低复杂度边界内成立；一旦超阈值，会自动回到标准 lane。详细边界见相关指南和术语文档。

---

## 常用入口

| 你现在想做什么 | 从这里开始 |
|---|---|
| 接入 CodeStable | `cs-onboard` |
| 不知道该用哪个技能 | `cs` |
| 做新功能 | `cs-feat` |
| 修 bug | `cs-issue` |
| 做重构 | `cs-refactor` |
| 扫一遍哪里有问题 | `cs-audit` |
| 摸代码 / 调研实现 | `cs-explore` |
| 记录决定 / 经验 / 技巧 | `cs-decide` / `cs-learn` / `cs-trick` |

---

## 进一步阅读

### 规范性入口

- [`.codestable/reference/workflow-contract.md`](./.codestable/reference/workflow-contract.md) — truth source、continuation、generated state、distribution
- [`.codestable/reference/system-overview.md`](./.codestable/reference/system-overview.md) — CodeStable 体系总览
- [`.codestable/reference/terminology.md`](./.codestable/reference/terminology.md) — feature / issue / fastforward 等术语判据
- [`.codestable/reference/status-schema.md`](./.codestable/reference/status-schema.md) — `status.json` schema

### 工作流指南

- [`docs/dev/feature-workflow.md`](./docs/dev/feature-workflow.md)
- [`docs/dev/issue-workflow.md`](./docs/dev/issue-workflow.md)
- [`docs/dev/refactor-workflow.md`](./docs/dev/refactor-workflow.md)

---

## 为什么这样设计

很多 AI 编码框架解决的是：**怎么把 Agent 编排得更强**。

CodeStable 解决的是：**怎么让严肃软件工程的状态、约束、决策、历史，在多轮开发之后仍然可检索、可追溯、可复用**。

所以它默认：
- 人在环
- 文档和代码同属工程状态
- 流程分阶段，不让 AI 一口气越过所有 checkpoint

---

<div align="center">

MIT License · 作者 [@liuzhengdong](https://github.com/liuzhengdongfortest)

</div>
