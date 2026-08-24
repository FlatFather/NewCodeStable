---
doc_type: issue-fix
issue: 2026-06-18-feature-design-confirmation-does-not-continue
path: fast-track
fix_date: 2026-06-18
tags: [workflow, continuation, cs-feat, cs-feat-design]
status: completed
---

# feature design 确认后未续到 plan 修复记录

## 1. 问题描述

用户在 `cs-feat-design` 阶段完成整体 review 并明确回复“同意 / 继续 / 确认”后，当前口径只会口头说下一步是 `cs-feat-plan`，但没有把 continuation-first 的续作闭环写清楚。

## 2. 根因

`cs-feat-design/SKILL.md` 在“引导进入 `cs-feat-plan`”一节里只描述了“下一步是谁”，没有明确说明：

- design checkpoint 到此结束
- 用户若继续回复 `同意 / 继续 / 确认`
- 应回到 `cs-feat` 顶层入口
- 再由顶层按 continuation-first 根据 `design.md` 已 approved 且 `plan.md` / `checklist.yaml` 未落齐的状态续到 `cs-feat-plan`

因此 feature 主线的“确认后如何继续”闭环没有在 `cs-feat-design`、`cs-feat`、`workflow-continuation-feature.md` 之间显式收口。

## 3. 修复方案

采用最小改动的文档口径修复：

1. 在 `cs-feat-design/SKILL.md` 的“引导进入 `cs-feat-plan`”补齐确认后续作说明
2. 在 `cs-feat/SKILL.md` 路由表中明确：`design.md` 已 approved 且 `plan.md` / checklist 未落齐的场景包含“design 阶段刚确认后的续作”
3. 在 `.codestable/reference/workflow-continuation-feature.md` 中补齐：design checkpoint 收口后，真正的续作恢复应回到 `cs-feat` 顶层入口

## 4. 改动文件清单

- `cs-feat-design/SKILL.md`
- `cs-feat/SKILL.md`
- `.codestable/reference/workflow-continuation-feature.md`

## 5. 验证结果

- `git diff --check` 通过
- 修复文件行数正常：
  - `cs-feat-design/SKILL.md` — 278 行
  - `cs-feat/SKILL.md` — 224 行
  - `.codestable/reference/workflow-continuation-feature.md` — 57 行
- 关键文案已落盘：
  - `workflow-continuation-feature.md` 已明确“真正的续作恢复应回到 `cs-feat` 顶层入口”
  - `cs-feat` 路由表已明确“包括 design 阶段刚确认后的续作场景”
  - `cs-feat-design` 已明确说明确认后的正确续作入口

## 6. 遗留事项

- 本次是文档与协议口径修复，没有增加自动化测试或脚本级校验。
- 如果后续仍出现“用户确认后没有自动续作”的真实交互问题，需要另开 issue 检查 `cs` / `cs-feat` 调用链是否在运行时真正按该口径执行。
