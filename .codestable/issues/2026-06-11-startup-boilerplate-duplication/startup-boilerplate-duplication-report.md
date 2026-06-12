---
doc_type: issue-report
issue: 2026-06-11-startup-boilerplate-duplication
status: confirmed
severity: P1
summary: 多个 skill 的“启动必读”段落逐字重复，修改规则时容易遗漏同步
tags: [workflow, skills, duplication, maintainability]
source_audit: .codestable/audits/2026-06-11-skill-workflow/finding-02.md
---

# startup boilerplate duplication Issue Report

## 1. 问题现象

多个 skill 的 `SKILL.md` 都包含完全相同的“启动必读”段落，要求启动前读取 `.codestable/attention.md`。该规则当前以复制文本的方式散落在多个 skill 中。

审计发现：如果未来要修改启动检查规则，需要逐文件同步修改；遗漏任一 skill 会造成不同 skill 的启动口径不一致。

## 2. 复现步骤

1. 打开任意多个 CodeStable skill 的 `SKILL.md`。
2. 查看文件开头的 `## 启动必读` 段落。
3. 对比 `cs-feat/SKILL.md`、`cs-feat-plan/SKILL.md`、`cs-issue/SKILL.md`、`cs-issue-report/SKILL.md` 等文件。
4. 观察到：同一段启动规则被逐字复制到多个文件中。

复现频率：稳定。

## 3. 期望 vs 实际

**期望行为**：启动检查规则有单一权威来源，修改规则时只需改一处，或至少有生成/检查机制保证所有 skill 同步。

**实际行为**：启动检查规则以手工复制形式散落在多个 skill 中，缺少同步机制。

## 4. 环境信息

- 涉及模块 / 功能：CodeStable skill 启动检查规则
- 相关文件 / 函数：
  - `cs-audit/SKILL.md:8-10`
  - `cs-feat/SKILL.md:8-10`
  - `cs-feat-design/SKILL.md:8-10`
  - `cs-feat-plan/SKILL.md:8-10`
  - `cs-feat-impl/SKILL.md:8-10`
  - `cs-feat-accept/SKILL.md:8-10`
  - `cs-issue/SKILL.md:8-10`
  - `cs-issue-report/SKILL.md:8-10`
- 运行环境：文档 / skill 工作流维护
- 其他上下文：来源于 `.codestable/audits/2026-06-11-skill-workflow/finding-02.md`

## 5. 严重程度

**P1** — 当前功能可用，但重复规则影响所有 skill 的维护一致性；后续改启动策略时遗漏概率较高。

## 备注

审计建议考虑 shared include、生成脚本，或保留短指针到单一权威规则。具体方案留到 analyze 阶段决定。
