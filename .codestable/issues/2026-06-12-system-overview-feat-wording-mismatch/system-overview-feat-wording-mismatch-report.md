---
doc_type: issue-report
issue: 2026-06-12-system-overview-feat-wording-mismatch
status: confirmed
severity: P2
summary: system-overview.md 对 feature 主线的阶段名称与 cs-feat/SKILL.md 五阶段表存在措辞差异
tags: [documentation, system-overview, cs-feat, wording, consistency]
source_audit: .codestable/audits/2026-06-11-skill-workflow/finding-10.md
---

# system overview feat wording mismatch Issue Report

## 1. 问题现象

`system-overview.md:18` 描述 feature 主线为"design → plan → implement → acceptance"。

`cs-feat/SKILL.md:46-53` 五阶段表描述阶段名称为：
- 阶段 3：分步实现
- 阶段 4：验收闭环

存在措辞不一致：
- `system-overview` 用英文"implement"和"acceptance"
- `cs-feat` 用中文"分步实现"和"验收闭环"

## 2. 复现步骤

1. 打开 `.codestable/reference/system-overview.md:18`
2. 看到"design → plan → implement → acceptance"
3. 打开 `cs-feat/SKILL.md:46-53`
4. 观察到：五阶段表用"分步实现"和"验收闭环"

复现频率：稳定（文档状态）

## 3. 期望 vs 实际

**期望行为**：system-overview 与 cs-feat 对相同阶段使用一致的名称（全用中文或全用英文缩写）

**实际行为**：system-overview 用英文，cs-feat 用中文，措辞不统一

## 4. 环境信息

- 涉及模块 / 功能：文档体系 feature 主线描述
- 相关文件 / 函数：
  - `.codestable/reference/system-overview.md:18`
  - `cs-feat/SKILL.md:46-53`
- 运行环境：文档层面
- 其他上下文：审计 finding-10 指出此问题

## 5. 严重程度

**P2** — 措辞差异不影响理解，但不统一可能让读者困惑是否是两套不同流程，属于文档一致性优化

## 备注

来源：`.codestable/audits/2026-06-11-skill-workflow/finding-10.md`

建议修复方向：统一为中文全称（分步实现、验收闭环）或英文缩写（impl、accept），保持一致。
