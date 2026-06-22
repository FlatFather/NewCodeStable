---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "01"
nature: maintainability
severity: P1
confidence: high
title: continuation-first 摘要与详细协议存在口径漂移风险
status: fixed
fixed_by: inline
fixed_date: 2026-06-18
notes: 已引入 protocol_version 1.0 机制，shared-conventions 引用时标注版本号
tags: [continuation, shared-conventions, workflow-continuation, sync-risk]
---

# Finding-01: continuation-first 摘要与详细协议存在口径漂移风险

## 问题描述

`.codestable/reference/shared-conventions.md` 第 1.5 节保留 continuation-first **摘要**，`.codestable/reference/workflow-continuation.md` 保留**详细协议**。两份文档分别维护，但没有自动同步检查机制，存在口径漂移风险。

## 证据

**文件位置**：
- `/Users/kong/self/github/NewCodeStable/.codestable/reference/shared-conventions.md:102-104`
- `/Users/kong/self/github/NewCodeStable/.codestable/reference/workflow-continuation.md:1-180`

**当前状态**：
- `shared-conventions.md` 第 1.5 节：3 行摘要 + 指针
- `workflow-continuation.md`：180 行详细协议，包含适用范围、核心原则、处理规则、恢复顺序

**口径依赖关系**：
- 10+ 个 skill（cs / cs-feat / cs-issue / cs-feat-design / cs-feat-plan / cs-feat-impl / cs-feat-accept / cs-issue-report / cs-issue-analyze / cs-issue-fix）都引用这两份文档
- 摘要变更而详细协议未同步 → skill 读到不一致规则
- 详细协议变更而摘要未同步 → 用户在 shared-conventions 看到过时简述

## 为什么构成 P1

- **影响范围**：10+ 个 skill 依赖这两份文档的一致性
- **修复成本**：漂移发生后需要人工逐文档对比并回溯修改历史
- **可预防性**：可通过自动检查或版本号机制在 CI / pre-commit 阶段拦截

## 建议修复方案

**方案 A（推荐）：引入协议版本号**

1. `workflow-continuation.md` frontmatter 增加 `protocol_version: 1.0`
2. `shared-conventions.md` 第 1.5 节引用时声明：`详细协议见 workflow-continuation.md (v1.0)`
3. 修改协议时同步升级版本号，摘要也同步刷新

**方案 B：自动同步检查脚本**

1. 写 `.codestable/tools/check-continuation-sync.py`
2. 提取两份文档的关键规则点（如"短回复列表"、"唯一候选约束"）
3. pre-commit hook 或 CI 阶段运行，发现不一致时报错

**方案 C：合并回单文档**

- 把 `workflow-continuation.md` 合并回 `shared-conventions.md`
- 被拒原因：违反项目"单 md 不超 300 行"约束（当前 shared-conventions 已 300+ 行）

## 建议动作

走 **`cs-issue`** 流程修复：
1. `cs-issue-report`：记录本发现
2. `cs-issue-analyze`：选定方案 A 或 B
3. `cs-issue-fix`：实施并验证同步机制生效
