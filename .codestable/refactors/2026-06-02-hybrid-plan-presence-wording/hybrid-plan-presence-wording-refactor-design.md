---
doc_type: refactor-design
refactor: 2026-06-02-hybrid-plan-presence-wording
status: draft
scope: `.codestable/reference/shared-conventions.md`、`.codestable/reference/system-overview.md`、`.codestable/architecture/ARCHITECTURE.md`、`cs-feat/SKILL.md`、`cs-feat-design/SKILL.md` 中与 hybrid feature / plan 门槛相关的段落
summary: 收敛 hybrid plan 的入口与总览口径，明确“是否选择 hybrid”和“进入 hybrid 后 plan 必须存在”是两个不同层次
---

# hybrid-plan-presence-wording refactor design

## 1. 本次范围

- 从 scan 勾选了哪几条：#1、#2、#3
- 明确不做的：无
- 预估总工作量：小
- 总风险档位：中（不改行为，但会收紧 hybrid / legacy 的文案边界）

## 2. 前置依赖

- 无测试前置：本次只改共享约定与技能文档口径，属于声明式内容，按 refactor 前置检查豁免测试覆盖要求。
- 无调用方搜索前置：本次只处理 feature 流程的文案边界，不涉及代码调用图。

## 3. 执行顺序

### 步骤 1：把 cs-feat 中的 hybrid plan 说法收敛成分支级硬门槛
- 引用方法：M-L3-06 Layer Rectification
- 具体操作：更新 `cs-feat/SKILL.md` 的 feature 目录树与阶段表，让它能明确表达：legacy 仍是 `design + checklist + acceptance`，hybrid 则是 `design + plan + checklist + acceptance`；如果保留“可选”语义，只允许它描述“是否选择 hybrid”，不允许它落在“进入 hybrid 后 plan 是否可缺”。
- 退出信号：`cs-feat` 单独阅读时，用户已经能分清“选不选 hybrid”与“选了 hybrid 之后 plan 必须存在”是两层不同判断。
- 验证责任：AI 自证
- 回滚：若改动误伤 legacy 口径，恢复 legacy/hybrid 并存描述，再重新收紧 hybrid 分支。

### 步骤 2：收紧 cs-feat-design 中关于 hybrid plan 生成的模糊措辞
- 引用方法：M-L2-04 Move Function
- 具体操作：更新 `cs-feat-design/SKILL.md` 开头关于产物的总述，把“预留或衔接 plan”收敛成“hybrid feature 在 approved design 后生成真实 plan，并由 design + plan 抽 checklist”；同时保持历史 feature 重开和初始化模式的现有边界不变。
- 退出信号：`cs-feat-design` 首段、生成顺序、历史 feature 重开三处关于 hybrid plan 的说法已经一致，不再出现“占位式 plan 也可以”的阅读歧义。
- 验证责任：AI 自证
- 回滚：若改完后初始化模式或 legacy 路径被误写成默认带 plan，恢复那部分路径说明，再单独收紧 hybrid 分支描述。

### 步骤 3：给 system-overview 与 architecture 补一句直白摘要
- 引用方法：M-L3-06 Layer Rectification
- 具体操作：在 `.codestable/reference/system-overview.md` 与 `.codestable/architecture/ARCHITECTURE.md` 各补一条简洁摘要，直说“hybrid feature 一旦采用 hybrid 口径，plan 就是必备产物；缺失时 implement / acceptance / workflow-check 都应失败”。不重复展开 shared conventions 的细节规则。
- 退出信号：overview / architecture 读者只扫总览层，也能直接读到 hybrid 的硬门槛，不需要自行从多条细则里拼结论。
- 验证责任：AI 自证
- 回滚：若补充过长、开始重复 shared conventions 的完整协议，就删回摘要句，只保留最短门槛表达。

## 4. 风险与看点

- 高风险点 1：把“hybrid 是否启用”与“hybrid 启用后 plan 是否必备”混成一句，导致 legacy 路径被误收紧。控制方式：所有改动都显式区分这两个判断层次。
- 高风险点 2：overview / architecture 补充过量，重新长成 shared conventions 的平行副本。控制方式：只加摘要句，不重写协议正文。
- 高风险点 3：`cs-feat-design` 的首段收紧后，如果忽略后文现有历史 feature / 初始化模式边界，可能造成单文件内部自相矛盾。控制方式：以三处联读结果作为验收标准。
