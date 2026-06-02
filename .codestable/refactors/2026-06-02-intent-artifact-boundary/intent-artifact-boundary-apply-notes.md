---
doc_type: refactor-apply-notes
refactor: 2026-06-02-intent-artifact-boundary
---

# intent-artifact-boundary apply notes

## 步骤 1: 把 intent 登记进 feature 共享目录契约
- 完成时间: 2026-06-02
- 改动文件: `.codestable/reference/shared-conventions.md`
- 验证结果: 已把 `{slug}-intent.md` 补进 feature 目录结构；新增 `feature intent` 元数据口径；在 feature 产物职责边界中明确它是 design 前的可选前置草稿，不参与 implement / acceptance。
- 偏离: 无

## 步骤 2: 收敛 cs-feat 的入口表述到路由层
- 完成时间: 2026-06-02
- 改动文件: `/Users/kong/.claude/skills/cs-feat/SKILL.md`
- 验证结果: 保留了 intent 初始化模式与 intent 已填好的路由判断；把文件树与阶段说明改成依赖 shared conventions / cs-feat-design，不再重复充当 intent 生命周期的第二权威来源。
- 偏离: 无

## 步骤 3: 收敛 cs-feat-design 的初始化模式说明到实现细节层
- 完成时间: 2026-06-02
- 改动文件: `/Users/kong/.claude/skills/cs-feat-design/SKILL.md`
- 验证结果: 保留了初始化模式的具体动作（建目录、写空 intent、停在 intent）；补充了“共享身份看 shared conventions，本技能负责草稿骨架与读取方式”的依赖方向。
- 偏离: 无
