---
doc_type: refactor-scan
refactor: 2026-06-02-hybrid-plan-presence-wording
status: user-reviewed
scope: `.codestable/reference/shared-conventions.md`、`.codestable/reference/system-overview.md`、`.codestable/architecture/ARCHITECTURE.md`、`cs-feat/SKILL.md`、`cs-feat-design/SKILL.md` 中与 hybrid feature / plan 门槛相关的段落
summary: 发现 3 条结构类优化点，核心是把 hybrid plan 的入口口径收敛为“进入 hybrid 后 plan 是硬门槛”
---

# hybrid-plan-presence-wording scan

## 总览

- 扫描范围：`.codestable/reference/shared-conventions.md`、`.codestable/reference/system-overview.md`、`.codestable/architecture/ARCHITECTURE.md`、`cs-feat/SKILL.md`、`cs-feat-design/SKILL.md`
- 发现 3 条优化点：结构 3 / 性能 0 / 可读性 0
- 按风险：低 0 / 中 3 / 高 0
- 建议先做：#1 #2（先清掉 `cs-feat` 的松口径，再把 `cs-feat-design` 的“预留/衔接”措辞收紧）
- 建议慎做 / 后做：#3（只做轻量补齐，避免把 system-overview / architecture 重新写成第二套长协议）
- 前置检查 7 条全过：✓

## 条目

### [#1] 把 cs-feat 中残留的“hybrid 可选 plan”改成分支级硬门槛 ✓

- **位置**：`cs-feat/SKILL.md:31-32`、`cs-feat/SKILL.md:49`
- **分类**：结构
- **现状**：`cs-feat` 的目录树仍写 `{slug}-plan.md ← hybrid 可选执行计划`，阶段表仍把 hybrid 说成“design.md + checklist.yaml（初始化模式可先建 intent.md；hybrid 细节见 shared conventions）”，但没有直接表达“进入 hybrid 后 plan 是必备输入”
- **问题**：同一个入口文档里，“shared conventions 已把 hybrid plan 定成硬门槛”，而 `cs-feat` 仍保留“可选执行计划”这类松表述；同一规则在 2 处表达冲突，会让新用户误以为 hybrid 只是“可以多一份 plan”
- **建议**：把 `cs-feat` 中关于 `{slug}-plan.md` 的描述改成“hybrid 分支产物”或等价硬门槛措辞；若保留“可选”，只能用于“是否选择 hybrid”，不能用于“进入 hybrid 后 plan 是否可缺”
- **建议映射的方法**：M-L3-06
- **风险**：中（需要同时保持 legacy/hybrid 并存口径，不要误改成“所有 feature 都必须有 plan”）
- **验证**：AI 自证（核对 `cs-feat` 单独阅读时，已能区分“是否选 hybrid”与“选中 hybrid 后 plan 必须存在”）
- **范围**：约 6-12 行 / 1 文件

### [#2] 收紧 cs-feat-design 中“预留或衔接 plan”的模糊说法 ✓

- **位置**：`cs-feat-design/SKILL.md:12`
- **分类**：结构
- **现状**：`cs-feat-design` 开头仍写“对 hybrid feature，还会预留或衔接 `{slug}-plan.md` 这份详细执行步骤正文”
- **问题**：这里的“预留或衔接”语义太松，和同文件后面已写明的“升级 hybrid 时必须补 `workflow: hybrid` 并生成真实 `plan.md`”不完全一致；单文件内部就存在一处弱门槛、一处强门槛
- **建议**：把开头改成与当前协议一致的说法：hybrid feature 在 approved design 后生成真实 `plan.md`，并由 design + plan 抽 checklist；去掉“预留”这类会让人误解为占位文件也可以的词
- **建议映射的方法**：M-L2-04
- **风险**：中（要小心只收紧 hybrid 分支，不把初始化模式 / legacy 路径误写成强制带 plan）
- **验证**：AI 自证（核对 `cs-feat-design` 首段、生成顺序、历史 feature 重开三处说法一致）
- **范围**：约 4-10 行 / 1 文件

### [#3] 用最小改动补齐总览层对 hybrid 门槛的直白表达 ✓

- **位置**：`.codestable/reference/system-overview.md:18`、`.codestable/architecture/ARCHITECTURE.md:27-28`、`.codestable/architecture/ARCHITECTURE.md:37-39`
- **分类**：结构
- **现状**：system overview 和 architecture 已经整体上偏向正确口径，例如写了 `design → plan → checklist → implement → acceptance`，也写了 `plan presence rule`；但总览层对“进入 hybrid 后 plan 是硬门槛”还主要依赖读者自己从多条规则中推断
- **问题**：共享约定是权威没错，但总览层缺少一句直白摘要；后续读者若只扫 overview / architecture，仍需要自行拼出“是否选择 hybrid”和“选中 hybrid 后不得缺 plan”这两个层次
- **建议**：只补一句简洁摘要，不重复整套协议：例如明确“hybrid feature 一旦采用 hybrid 口径，plan 就是必备产物，缺失时 implement / acceptance / workflow-check 都应失败”
- **建议映射的方法**：M-L3-06
- **风险**：中（若写太多，会再次把 overview / architecture 变成 shared conventions 的平行协议副本）
- **验证**：AI 自证（确认 overview / architecture 只是补摘要，不新增第二套细节规则）
- **范围**：约 6-12 行 / 2 文件
