---
doc_type: refactor-scan
refactor: 2026-06-02-intent-artifact-boundary
status: user-reviewed
scope: `.codestable/reference/shared-conventions.md`、`cs-feat/SKILL.md`、`cs-feat-design/SKILL.md` 中与 `{slug}-intent.md` 身份和入口口径相关的段落
summary: 发现 3 条结构类优化点，核心是为 intent.md 明确权威身份，并收敛 shared conventions 与 feature 入口技能之间的口径
---

# intent-artifact-boundary scan

## 总览

- 扫描范围：`.codestable/reference/shared-conventions.md`、`/Users/kong/.claude/skills/cs-feat/SKILL.md`、`/Users/kong/.claude/skills/cs-feat-design/SKILL.md`
- 发现 3 条优化点：结构 3 / 性能 0 / 可读性 0
- 按风险：低 0 / 中 3 / 高 0
- 建议先做：#1 #3（先定 intent 身份，再统一入口依赖方向）
- 建议慎做 / 后做：#2（和 #1 互斥，只在你明确不想把 intent 作为共享产物时才做）
- 前置检查 7 条全过：✓

## 条目

### [#1] 把 intent.md 正式登记为 feature 的前置产物 ✓

- **位置**：`.codestable/reference/shared-conventions.md:27-34`、`/Users/kong/.claude/skills/cs-feat/SKILL.md:27-33`、`/Users/kong/.claude/skills/cs-feat-design/SKILL.md:24-33`
- **分类**：结构
- **现状**：`cs-feat` 和 `cs-feat-design` 已把 `{slug}-intent.md` 当成初始化模式产物和 design 输入，但 feature 目录的权威结构里还没有它
- **问题**：同一产物的“是否正式存在”被拆成两套口径：共享约定 0 处登记，入口技能 3 处依赖；这会让目录结构、路由判断和后续维护出现双真相源
- **建议**：在 `shared-conventions.md` 的 feature 目录结构与 feature 产物职责边界中补登 `{slug}-intent.md`，明确它是 design 前的可选前置草稿，不参与 implement / acceptance
- **建议映射的方法**：M-L2-04
- **风险**：中（会把一个当前局部实现细节提升为共享协议，需要顺手定义生命周期和边界）
- **验证**：AI 自证（逐条核对 shared conventions 与两个入口技能对 intent 的说法一致）
- **范围**：约 20-35 行 / 3 文件

### [#2] 把 intent.md 降级为 cs-feat-design 的局部输入 ✗

✗ 理由：不想把 intent 降级成局部输入。

- **位置**：`/Users/kong/.claude/skills/cs-feat/SKILL.md:27-33`、`/Users/kong/.claude/skills/cs-feat/SKILL.md:73-76`、`/Users/kong/.claude/skills/cs-feat/SKILL.md:91-98`
- **分类**：结构
- **现状**：`cs-feat` 把 `{slug}-intent.md` 画进 feature 目录树，还把“intent 已填好”当成标准入口状态，但共享约定并未承认它是 feature 聚合根的一部分
- **问题**：入口技能把同一个对象同时当作“目录里的正式产物”和“设计前临时草稿”，职责边界混在一起；相关表述至少出现 6 处，后续更新容易继续漂移
- **建议**：如果你不想让 intent 成为共享产物，就把 `cs-feat` 中关于 intent 的文件树、阶段产出和标准入口表述全部降级为“仅 design 初始化模式的临时输入”
- **建议映射的方法**：M-L3-06
- **风险**：中（会改变用户对 feature 目录权威结构的认知，且与 #1 互斥）
- **验证**：AI 自证（确认 `cs-feat` 不再把 intent 画成 feature 流程正式产物，且 `cs-feat-design` 仍保留初始化模式）
- **范围**：约 15-30 行 / 2 文件

### [#3] 统一 intent 与 brainstorm 的入口分工说明 ✓

- **位置**：`/Users/kong/.claude/skills/cs-feat/SKILL.md:71-76`、`/Users/kong/.claude/skills/cs-feat/SKILL.md:91-98`、`/Users/kong/.claude/skills/cs-feat-design/SKILL.md:18-19`、`/Users/kong/.claude/skills/cs-feat-design/SKILL.md:61-63`
- **分类**：结构
- **现状**：`cs-feat` 已写了 brainstorm vs intent 的区别，`cs-feat-design` 也解释了初始化模式为何停在 intent，但两边都各自带一套入口说明
- **问题**：同一入口分工至少在 4 处重复定义，且缺少单一依赖方向；后续如果 intent 身份有变化，需要手工同步多处入口说明
- **建议**：无论选 #1 还是 #2，都把 `cs-feat` 和 `cs-feat-design` 的 intent/brainstorm 分工收敛成一套说法：`cs-feat` 只负责路由判断，`cs-feat-design` 负责初始化模式细节，shared conventions 负责产物身份
- **建议映射的方法**：M-L3-06
- **风险**：中（要小心只收敛依赖方向，不改变现有分诊行为）
- **验证**：AI 自证（核对 `cs-feat` 不再重复讲初始化细节，`cs-feat-design` 不再越权定义共享身份）
- **范围**：约 15-25 行 / 2 文件
