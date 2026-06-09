---
doc_type: learning
track: knowledge
date: 2026-06-05
slug: detect-task-continuation-before-rerouting
component: ccg-engine
tags: [workflow, routing, continuation, task, gate, ccg-go]
---

## 背景

这次在使用 `/ccg:go` 推进 CodeStable 工作流时，出现了明显的“重复进入流程”问题。

典型表现是：

- 用户已经处在某个进行中的 task 里
- 只是回复了 `继续`、`确认跳过`、`同意跳过` 这类 continuation / gate 应答
- 但顶层入口仍把这句话当成**一个新的自然语言请求**
- 重新执行意图分析、策略选择、task 创建或阶段路由
- 最终导致同一条流程被反复导向 `cs-feat-design` / 再次确认跳过协作 / 再次建议下一步

这说明问题不在单个 feature skill，而在**顶层入口和阶段 skill 之间的续作边界没有收好**。

## 指导原则

当工作流已经引入了 `task.json`、`currentPhase`、`nextAction`、`gate` 这类显式状态机后，顶层入口必须优先判断：

- 用户是在**发起新任务**
- 还是在**继续已有任务**

如果命中 continuation，就应：

1. 先定位唯一的 `in_progress` task
2. 读取该 task 的 `strategy / currentPhase / nextAction / gate`
3. 直接从已有状态继续
4. 不再重新跑入口级 Phase 1 分析、task 创建、策略选择

对 gate 回复也一样：如果用户输入的是对当前 gate 的肯定或否定反馈，就应该被当成**状态推进信号**，而不是新的需求描述。

## 为什么重要

如果 continuation 不先于 rerouting 处理，分阶段 workflow 会天然出现“双重路由”问题：

- **外层入口**试图判断“现在应该走哪条策略”
- **内层阶段 skill**试图判断“现在应该走哪个阶段”

两层都做路由，结果就是：

- 用户一句“继续”，被解释成新的任务
- 用户一句“同意跳过”，被解释成新的意图分析输入
- 原本已经存在的 task 状态失去作用
- `task.json` 只是被创建了，但没有真正承担“恢复上下文”的职责

这会直接破坏用户心智模型：用户以为自己在推进同一个流程，系统却表现得像“每次都从入口重新开始”。

## 何时适用

适用于所有满足下面条件的工作流入口：

1. 顶层入口支持自然语言分发
2. 底层阶段依赖显式状态推进（如 `task.json` / `gate` / `nextAction`）
3. 用户在流程中会频繁输入短回复：
   - `继续`
   - `确认`
   - `同意`
   - `按这个修`
   - `跳过`
   - `继续下一步`

尤其在这种结构里必须优先应用：

- 顶层入口负责选策略
- 阶段 skill 负责执行阶段细则
- 中间通过 task 状态文件衔接

这时如果没有 continuation-first 规则，几乎一定会出现重复路由。

## 示例

这次修复 `/ccg:go` 时，新增的不是另一个更复杂的路由规则，而是一层更早的判断：

- 在 Phase 0 / Phase 1 之前
- 先检查 `.ccg/tasks/*/task.json`
- 如果存在唯一的 `in_progress` task
- 且用户输入是明显的 continuation / gate 回复
- 就直接恢复该 task，而不是重新做无状态分析

具体收益是：

- `继续` 不再重新触发 feature 路由判断
- `同意跳过` 不再重新触发协作确认
- `gate == user_approval_required` 时，用户的短回复会被视为当前 gate 的正式反馈
- 顶层入口与阶段 skill 的职责边界重新清晰：
  - **入口负责首次分发**
  - **task 状态负责续作恢复**
  - **阶段 skill 负责阶段推进**
