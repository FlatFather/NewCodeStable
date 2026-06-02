---
doc_type: refactor-apply-notes
refactor: 2026-06-02-hybrid-plan-presence-wording
---

# hybrid-plan-presence-wording apply notes

## 步骤 1: 把 cs-feat 中的 hybrid plan 说法收敛成分支级硬门槛
- 完成时间: 2026-06-02
- 改动文件: `cs-feat/SKILL.md`
- 验证结果: `{slug}-plan.md` 已从“hybrid 可选执行计划”收紧为“hybrid 分支必备执行计划”；阶段表补上“若采用 hybrid，则 plan 为必备输入”的说明。
- 偏离: 无

## 步骤 2: 收紧 cs-feat-design 中关于 hybrid plan 生成的模糊措辞
- 完成时间: 2026-06-02
- 改动文件: `cs-feat-design/SKILL.md`
- 验证结果: 开头总述已改为“approved design 后生成真实 plan，再从 design + plan 抽 checklist”；不再使用“预留或衔接 plan”这类弱门槛词。
- 偏离: 无

## 步骤 3: 给 system-overview 与 architecture 补一句直白摘要
- 完成时间: 2026-06-02
- 改动文件: `.codestable/reference/shared-conventions.md`、`.codestable/reference/system-overview.md`、`.codestable/architecture/ARCHITECTURE.md`
- 验证结果: 共享约定、体系总览、架构总入口都已明确“进入 hybrid 后 plan 是必备产物/输入”；补充保持在摘要级，没有复制 shared conventions 的整套细节。
- 偏离: 无
