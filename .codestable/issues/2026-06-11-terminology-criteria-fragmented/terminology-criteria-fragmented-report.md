---
doc_type: issue-report
issue: 2026-06-11-terminology-criteria-fragmented
status: confirmed
severity: P1
summary: feature/issue 等关键术语判据分散在多个 skill 和 reference 中，存在维护不一致风险
tags: [workflow, terminology, maintainability, routing]
source_audit: .codestable/audits/2026-06-11-skill-workflow/finding-03.md
---

# terminology criteria fragmented Issue Report

## 1. 问题现象

多个关键术语或路由判据分散写在不同 skill 与 reference 文档中，例如 feature vs issue、沉淀类技能区分、fastforward vs 标准 feature。部分判据存在轻微差异。

审计发现：这些判据没有集中到单一权威来源，后续修改时容易遗漏同步，导致不同入口给用户不同建议。

## 2. 复现步骤

1. 打开 `cs-feat/SKILL.md` 的 feature / issue 边界说明。
2. 打开 `cs-issue/SKILL.md` 的 feature / issue 边界说明。
3. 对比两处定义。
4. 观察到：两处定义基本一致，但 `cs-issue` 中 issue 额外包含“性能问题”。
5. 再对比 `cs/SKILL.md` 与 `.codestable/reference/system-overview.md` 中对 learning / trick / decision / explore 的区分。
6. 观察到：同类判据在多个位置重复维护。

复现频率：稳定。

## 3. 期望 vs 实际

**期望行为**：关键术语判据有单一权威来源；各 skill 只引用该来源或保留极简摘要。

**实际行为**：判据散落在多个 skill 与 reference 中，部分措辞已有轻微差异。

## 4. 环境信息

- 涉及模块 / 功能：CodeStable skill 路由与术语判据
- 相关文件 / 函数：
  - `cs-feat/SKILL.md:119-123`
  - `cs-issue/SKILL.md:104-109`
  - `cs/SKILL.md:127-135`
  - `.codestable/reference/system-overview.md:69-78`
- 运行环境：文档 / skill 工作流维护
- 其他上下文：来源于 `.codestable/audits/2026-06-11-skill-workflow/finding-03.md`

## 5. 严重程度

**P1** — 路由判据影响用户进入哪个工作流，若口径不一致会直接导致错误分诊或重复解释。

## 备注

审计建议创建 `.codestable/reference/terminology.md` 或其他单一权威来源。具体方案留到 analyze 阶段决定。
