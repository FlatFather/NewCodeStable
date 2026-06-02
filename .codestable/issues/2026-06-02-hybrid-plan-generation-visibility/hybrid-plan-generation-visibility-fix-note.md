---
doc_type: issue-fix
issue: 2026-06-02-hybrid-plan-generation-visibility
path: fast-track
fix_date: 2026-06-02
tags: [workflow, hybrid, plan, cs-feat, cs-feat-design]
---

# hybrid plan generation visibility 修复记录

## 1. 问题描述

用户从 `cs-feat → cs-feat-design → cs-feat-impl → cs-feat-accept` 这条顶层 feature 流程去理解时，看不出 `plan.md` 会在什么阶段生成，因此容易误解为这条流程中不会生成 plan 文件。

## 2. 根因

`cs-feat-design` 内部其实已经定义了 hybrid 下的真实生成顺序：approved design → plan → checklist；但 `cs-feat` 的阶段产出与路由表没有把这一步显式暴露出来，`cs` 顶层总览也没有补一句说明，导致用户在顶层链路上建立了错误心智模型。

## 3. 修复方案

用最小改动把 hybrid 下的 plan 生成关口显式写出来：
- 在 `cs-feat/SKILL.md` 的阶段 1 产出中写明 hybrid 会在本阶段生成 `plan.md`，再从 design + plan 抽 checklist
- 在 `cs-feat/SKILL.md` 的路由表中补一条：若 hybrid 的 `plan.md` / checklist 还没落齐，继续回 `cs-feat-design`
- 在 `cs/SKILL.md` 的顶层总览中补一句：若采用 hybrid，由 `cs-feat-design` 在进入实现前生成 `plan.md`

## 4. 改动文件清单

- `cs-feat/SKILL.md`
- `cs/SKILL.md`

## 5. 验证结果

- `cs-feat/SKILL.md` 现在已明确：hybrid 下 `plan.md` 在阶段 1 生成，再从 design + plan 抽 checklist。
- `cs-feat/SKILL.md` 的路由表现在已明确：若 hybrid 的 `plan.md` / checklist 还没落齐，不应直接进 `cs-feat-impl`。
- `cs/SKILL.md` 的顶层流程总览现在已明确：若采用 hybrid，则由 `cs-feat-design` 在进入实现前生成 `plan.md`。

## 6. 遗留事项

- 这次修的是“顶层链路可见性”问题，不是 hybrid 规则本身；真正的 plan presence rule 仍以 `.codestable/reference/shared-conventions.md` 为权威正文。
