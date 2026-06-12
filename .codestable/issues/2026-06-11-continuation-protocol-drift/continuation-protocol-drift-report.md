---
doc_type: issue-report
issue: 2026-06-11-continuation-protocol-drift
status: confirmed
severity: P1
summary: continuation-first 摘要与详细协议分别维护，缺少同步机制，存在口径漂移风险
tags: [workflow, continuation, documentation, maintainability]
source_audit: .codestable/audits/2026-06-11-skill-workflow/finding-01.md
---

# continuation protocol drift Issue Report

## 1. 问题现象

`.codestable/reference/shared-conventions.md` 第 1.5 节保留 continuation-first 摘要，`.codestable/reference/workflow-continuation.md` 保留详细协议。两份文档分别维护，但目前没有版本号、同步检查脚本或其他机制保证二者一致。

审计发现：当 continuation-first 规则后续发生变更时，摘要和详细协议可能出现口径漂移，进而让不同 skill 读到不一致的续作规则。

## 2. 复现步骤

1. 打开 `.codestable/reference/shared-conventions.md` 第 1.5 节。
2. 打开 `.codestable/reference/workflow-continuation.md` 全文。
3. 对比两份文档中关于短回复、唯一候选约束、task 状态桥的描述。
4. 观察到：两份文档存在依赖关系，但没有显式版本号或自动同步检查。

复现频率：稳定。

## 3. 期望 vs 实际

**期望行为**：continuation-first 的摘要与详细协议之间有明确同步机制；协议变更时能提醒维护者同步更新摘要或引用版本。

**实际行为**：摘要与详细协议仅靠人工维护一致，没有自动或显式的同步防线。

## 4. 环境信息

- 涉及模块 / 功能：CodeStable workflow continuation 协议
- 相关文件 / 函数：
  - `.codestable/reference/shared-conventions.md:102-104`
  - `.codestable/reference/workflow-continuation.md:1-180`
- 运行环境：文档 / skill 工作流维护
- 其他上下文：来源于 `.codestable/audits/2026-06-11-skill-workflow/finding-01.md`

## 5. 严重程度

**P1** — 影响 10+ 个 skill 对 continuation-first 的一致理解；虽然当前未确认已漂移，但缺少同步机制会导致后续维护风险较高。

## 备注

审计建议优先考虑协议版本号或自动同步检查脚本。具体方案留到 analyze 阶段决定。
