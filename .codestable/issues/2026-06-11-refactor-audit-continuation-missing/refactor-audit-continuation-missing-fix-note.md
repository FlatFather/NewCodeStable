---
doc_type: issue-fix
issue: 2026-06-11-refactor-audit-continuation-missing
status: completed
fixed_files: [.codestable/reference/workflow-continuation.md, cs-refactor/SKILL.md, cs-audit/SKILL.md]
related: [refactor-audit-continuation-missing-report.md, refactor-audit-continuation-missing-analysis.md]
tags: [workflow, continuation, cs-refactor, cs-audit]
---

# refactor audit continuation missing 修复记录

## 修复方案

采用方案 A：补充适用范围 + 实现 continuation-first 规则。

## 修复内容

### 1. 修改 `.codestable/reference/workflow-continuation.md`

**位置**：第 13 行

**修改前**：
```markdown
- 顶层入口：`cs`、`cs-feat`、`cs-issue`
```

**修改后**：
```markdown
- 顶层入口：`cs`、`cs-feat`、`cs-issue`、`cs-refactor`、`cs-audit`
```

**理由**：将 `cs-refactor` 和 `cs-audit` 正式纳入 continuation-first 适用范围。

### 2. 修改 `cs-refactor/SKILL.md`

**位置**：第 60 行（在"阶段 1：scan"之前插入）

**新增内容**：
- 增加"短回复 continuation-first"节
- 检测短回复信号
- Glob `.codestable/refactors/` 查找唯一候选目录
- 根据已有产物状态判断 scan / design / apply 阶段
- 多个候选停下来让用户选
- 引用 `.codestable/reference/workflow-continuation.md` 详细协议

**参考实现**：`cs-feat/SKILL.md` 和 `cs-issue/SKILL.md`

### 3. 修改 `cs-audit/SKILL.md`

**位置**：第 53 行（在"工作流 Phase 1"之前插入）

**新增内容**：
- 增加"短回复 continuation-first"节
- 检测短回复信号
- Glob `.codestable/audits/` 查找唯一候选目录
- 根据 index.md / finding-*.md 状态判断恢复 Phase
- 多个候选停下来让用户选
- 引用 `.codestable/reference/workflow-continuation.md` 详细协议

**参考实现**：`cs/SKILL.md`

## 验证结果

### 1. 复现步骤验证

- [x] 协议文档已明确列出 `cs-refactor` 和 `cs-audit`
- [x] `cs-refactor/SKILL.md` 已增加 continuation-first 规则
- [x] `cs-audit/SKILL.md` 已增加 continuation-first 规则

### 2. 期望行为验证

- [x] 所有顶层 workflow 入口（cs / cs-feat / cs-issue / cs-refactor / cs-audit）续作行为一致
- [x] 用户在 refactor / audit 流程中输入"继续"时，可自动恢复已有目录状态

### 3. 影响面回归

- [x] 不影响已有 feature / issue 流程
- [x] 仅新增 refactor / audit 的续作支持
- [x] 修改范围符合 analysis 声明（3 份文档）

## 修复方式

- 纯文档修改，无代码变更
- 参考已有 cs-feat / cs-issue / cs 实现
- 遵循 continuation-first 协议规范

## 后续建议

无。修复已完整覆盖根因。
