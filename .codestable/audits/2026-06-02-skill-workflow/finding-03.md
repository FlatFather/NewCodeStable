---
doc_type: audit-finding
audit: 2026-06-02-skill-workflow
finding_id: "arch-drift-03"
nature: arch-drift
severity: P1
confidence: medium
suggested_action: cs-refactor
status: open
---

# Finding 03：`{slug}-intent.md` 已进入 feature 流程入口，但未进入共享目录契约

## 速答

`intent.md` 已经被 `cs-feat` / `cs-feat-design` 当成正式前置输入和初始化模式产物使用，但 `.codestable/reference/shared-conventions.md` 的 feature 目录权威结构里没有它。这意味着“入口技能承认它存在，目录契约却没有登记它”。

## 关键证据

- `/Users/kong/.claude/skills/cs-feat/SKILL.md:29` — feature 目录文件树包含 `{slug}-intent.md`，并定义为“阶段 1 可选前置草稿”。
- `/Users/kong/.claude/skills/cs-feat/SKILL.md:73` 与 `/Users/kong/.claude/skills/cs-feat/SKILL.md:75` — 路由表明确把“初始化模式 / intent 已填好”当成正式入口状态。
- `/Users/kong/.claude/skills/cs-feat-design/SKILL.md:19` 与 `/Users/kong/.claude/skills/cs-feat-design/SKILL.md:32` — design 技能明确支持初始化模式并创建空的 `{slug}-intent.md`。
- `.codestable/reference/shared-conventions.md:27` 到 `.codestable/reference/shared-conventions.md:34` — feature 目录权威结构只登记了 brainstorm / design / plan / checklist / acceptance / ff-note，没有 `intent.md`。

## 影响

当一个文件已经参与“目录初始化、路由判断、design 输入”时，它就不再只是局部实现细节，而是共享流程的一部分。若共享约定缺位，后续就会出现三种分叉：有人把它当正式产物维护，有人把它当临时草稿忽略，有人根本不会在新项目骨架或检索工具里考虑它。

## 修复方向

先拍板 `intent.md` 的身份：
- 如果它是正式前置产物，就把它补进 `shared-conventions.md`，说明它与 brainstorm note 的边界；
- 如果它只是 design 阶段的临时输入，就应把入口技能的目录树和“阶段产物”表达降级，避免它看起来像长期共享产物。

## 建议动作

`cs-refactor`，因为这里需要先整理 feature 前置输入层的职责边界，再统一更新路由与共享约定。