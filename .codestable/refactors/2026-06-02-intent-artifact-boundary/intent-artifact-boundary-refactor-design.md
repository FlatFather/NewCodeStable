---
doc_type: refactor-design
refactor: 2026-06-02-intent-artifact-boundary
status: approved
scope: `.codestable/reference/shared-conventions.md`、`cs-feat/SKILL.md`、`cs-feat-design/SKILL.md` 中与 `{slug}-intent.md` 身份和入口口径相关的段落
summary: 将 `{slug}-intent.md` 提升为 feature 的可选前置草稿，并收敛 cs-feat / cs-feat-design 对 intent 与 brainstorm 分工的重复定义
---

# intent-artifact-boundary refactor design

## 1. 本次范围

- 从 scan 勾选了哪几条：#1、#3
- 明确不做的：#2（你已明确不想把 intent 降级成局部输入）
- 预估总工作量：小
- 总风险档位：中（不改行为，但会调整共享协议与入口职责的依赖方向）

## 2. 前置依赖

- 无测试前置：本次是共享约定与技能文档口径收敛，属于声明式流程内容，按 refactor 前置检查豁免测试覆盖要求。
- 无调用方搜索前置：本次只收敛 `.codestable/reference/` 与 `cs-feat*` 技能文案，不涉及代码调用图。

## 3. 执行顺序

### 步骤 1：把 intent 登记进 feature 共享目录契约
- 引用方法：M-L2-04 Move Function
- 具体操作：把目前只存在于 `cs-feat` / `cs-feat-design` 局部说明里的 `{slug}-intent.md` 身份，搬移并收敛到 `.codestable/reference/shared-conventions.md`；在 feature 目录树中补上 intent 文件，在 feature 产物职责边界里明确它是 **design 前的可选前置草稿**，只服务初始化模式和正式起草输入，不参与 implement / acceptance。
- 退出信号：shared conventions 单独阅读时，已经能回答 intent 是什么、放在哪、属于 feature 哪一段生命周期、哪些阶段会读它、哪些阶段不会依赖它。
- 验证责任：AI 自证
- 回滚：若发现 intent 被写成正式 workflow 主产物而非前置草稿，撤回 shared conventions 的新增职责段，只保留原 feature 四件套/五件套定义。

### 步骤 2：收敛 cs-feat 的入口表述到“路由层”
- 引用方法：M-L3-06 Layer Rectification
- 具体操作：更新 `cs-feat/SKILL.md`，让它继续负责“何时走 brainstorm、何时走 intent 初始化、何时走 design”，但不再重复定义 intent 的完整生命周期细节；目录树与阶段说明保留 intent 的存在，但把身份判断依赖到 shared conventions，把初始化细节依赖到 `cs-feat-design`。
- 退出信号：`cs-feat` 仍能独立路由 intent 相关诉求，但不再成为 intent 身份的第二权威来源。
- 验证责任：AI 自证
- 回滚：若改完后 `cs-feat` 已无法独立回答“什么时候走 intent 初始化模式”，恢复最小必要路由说明，但不恢复生命周期细节重复段。

### 步骤 3：收敛 cs-feat-design 的初始化模式说明到“实现细节层”
- 引用方法：M-L3-06 Layer Rectification
- 具体操作：更新 `cs-feat-design/SKILL.md`，保留初始化模式的具体操作（建目录、写空 intent、停在 intent），但避免越权定义 intent 的共享身份；把“它是 feature 目录中的可选前置草稿”这一层口径交还给 shared conventions，并与 `cs-feat` 的入口分工对齐。
- 退出信号：`cs-feat-design` 仍能完整执行初始化模式，但关于 intent 身份的说法与 shared conventions / cs-feat 不再冲突或重复扩张。
- 验证责任：AI 自证
- 回滚：若改完后初始化模式步骤不完整（例如看不出要写什么骨架、为何停在 intent），恢复操作级细节，但不恢复共享身份定义。

## 4. 风险与看点

- 高风险点 1：把 intent 写得过重，误变成 design / plan / checklist 同级主产物。控制方式：shared conventions 中明确它是 **前置草稿**，不是 implement / acceptance 输入。
- 高风险点 2：为减少重复而删掉过多入口信息，导致 `cs-feat` 或 `cs-feat-design` 单独阅读时不够可执行。控制方式：`cs-feat` 保留路由判断，`cs-feat-design` 保留初始化步骤，只收敛身份定义。
- 高风险点 3：intent 与 brainstorm 的边界被写模糊。控制方式：保留现有分工——brainstorm = AI 对话收敛；intent = 用户离线半成品草稿。
