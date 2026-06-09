---
doc_type: decision
category: convention
date: 2026-06-09
slug: continuation-first-for-skill-workflows
status: active
area: codestable-workflow
tags: [workflow, continuation, routing, task-bridge, reference]
---

## 背景

本项目在 workflow skills 上已经形成了明确的分层：

- 顶层入口负责开放式分发（`cs`、`cs-feat`、`cs-issue`）
- 阶段 skill 负责 design / plan / impl / accept 或 report / analyze / fix 的推进
- `.codestable/` 下的 spec 产物承担真实阶段状态

但在真实使用里，用户经常不会重复描述完整诉求，而是只输入：

- `继续`
- `确认`
- `同意`
- `按这个修`
- `跳过`
- `继续下一步`

如果这些短回复被当成新的自然语言请求重新路由，就会出现重复进入流程、重复确认 gate、重复输出“建议走哪个 skill”的问题。

同时，本项目原本把越来越多的共享协议堆进 `.codestable/reference/shared-conventions.md`，已经逼近甚至超过单文档长度上限，继续往里堆 continuation 细则会违反项目规则。

## 决定

本项目内的 workflow skills 采用以下统一规约：

1. **短回复默认先按 continuation-first 处理**
   - 当用户输入 `继续 / 确认 / 同意 / 按这个修 / 跳过 / 继续下一步` 这类短回复时，先判断是否在继续已有流程，再决定是否重新路由。

2. **只有唯一候选续作时才自动继续**
   - 命中唯一候选的 feature / issue / task 恢复对象时，直接继续。
   - 如果有多个候选，必须停下来让用户选，不能猜“最近一个”或“最像的一个”。

3. **`.ccg/tasks/*/task.json` 只作恢复桥，不是真相源**
   - 它可以帮助顶层入口和阶段 skill 快速恢复上下文。
   - 但它不能替代 `.codestable/features/`、`.codestable/issues/` 下的 spec 产物状态。

4. **continuation 的详细共享协议独立成文**
   - 详细规则统一放在 `.codestable/reference/workflow-continuation.md`。
   - `.codestable/reference/shared-conventions.md` 只保留摘要与指针，不再承载完整 continuation 细则。

## 理由

- 顶层入口和阶段 skill 都可能处理用户的短回复；如果没有 continuation-first，就会天然形成双重路由。
- “唯一候选才自动继续”能把误续作风险降到最低；错猜流程对象的代价比多问一句更高。
- `.ccg/tasks/*/task.json` 适合作恢复桥，但不适合作新的 workflow 真相源；如果把它和 `.codestable/` 产物并列，会制造双状态机。
- continuation 细则已经足够独立，继续堆进 `shared-conventions.md` 会让总规约文件继续膨胀，违反单文档长度约束，也不利于维护。

## 考虑过的替代方案

### 只改顶层入口，不改阶段 skill

未采用。因为外层入口即使不重跑路由，阶段 skill 仍可能继续重复输出阶段结论或重复确认 gate。

### 把 `.ccg/tasks/*/task.json` 提升为主 workflow 状态源

未采用。因为这会和 `.codestable/features/`、`.codestable/issues/` 的 spec 状态形成双真相源。

### 继续把 continuation 细则写进 `shared-conventions.md`

未采用。因为该文件已经接近或达到单文档长度上限，继续堆规则会直接违反项目约束，也会进一步削弱可读性。

## 后果

- 后续凡是本项目内 workflow skills 遇到短回复，都应先检查 continuation-first，而不是默认按新诉求解释。
- 以后新增 continuation 相关规则，应优先补到 `workflow-continuation.md`，而不是继续把细节塞进 `shared-conventions.md`。
- `shared-conventions.md` 保持“总规约 + 摘要入口”定位；细分协议文件只在主题足够独立时新增。
- 如果未来要把 continuation-first 扩展到本仓库外的命令层（例如全局 `/ccg:go`），需要另开新决策，不自动外推本条规则。

## 相关文档

- `.codestable/reference/workflow-continuation.md`
- `.codestable/reference/shared-conventions.md`
- `.codestable/reference/maintainer-notes.md`
- `.codestable/reference/system-overview.md`
- `.codestable/architecture/ARCHITECTURE.md`
- `docs/dev/feature-workflow.md`
- `.codestable/features/2026-06-05-skill-continuation-first/skill-continuation-first-design.md`
- `.codestable/features/2026-06-05-skill-continuation-first/skill-continuation-first-acceptance.md`
