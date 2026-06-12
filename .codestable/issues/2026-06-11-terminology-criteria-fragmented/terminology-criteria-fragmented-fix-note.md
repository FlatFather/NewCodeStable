---
doc_type: issue-fix
issue: 2026-06-11-terminology-criteria-fragmented
status: completed
fixed_files: [.codestable/reference/terminology.md, .codestable/reference/system-overview.md, cs-issue/SKILL.md, cs/SKILL.md, cs-feat/SKILL.md]
related: [terminology-criteria-fragmented-report.md, terminology-criteria-fragmented-analysis.md]
tags: [workflow, terminology, maintainability, routing]
---

# terminology criteria fragmented 修复记录

## 修复方案

采用方案 A：新增 `.codestable/reference/terminology.md` 集中定义关键术语判据。

## 修复内容

### 1. 创建 `.codestable/reference/terminology.md`

**新建文件**：`.codestable/reference/terminology.md`

**内容**：集中定义 5 类关键术语判据
1. feature vs issue
2. learning vs trick vs decision vs explore
3. fastforward vs 标准 feature
4. issue 标准路径 vs 快速通道
5. brainstorm vs intent

**设计**：
- 每个小节独立定义一组判据
- 包含判别口诀、灰色地带、判定规则
- 末尾说明维护方式

### 2. 修改 `.codestable/reference/system-overview.md`

**位置 1**：第 69-78 节"沉淀类四个子技能如何区分"

**修改前**：
- 完整列出 learning / trick / decision / explore 的定义

**修改后**：
- 保留一句摘要："区别在记录内容的性质"
- 指向 terminology.md 第 2 节
- 保留文档类型说明与 doc_type 字段区分

**位置 2**：第 100-103 节"进一步参考"

**新增**：
```markdown
- `.codestable/reference/terminology.md` — 关键术语与路由判据（feature vs issue、沉淀类技能区分、fastforward 判据等）
```

### 3. 修改 `cs-issue/SKILL.md`

**位置**：第 104-110 节"与 feature 工作流的边界"

**修改前**：
- 完整定义 issue / feature

**修改后**：
- 保留短定义
- 新增"完整判据见 `.codestable/reference/terminology.md` 第 1 节"
- 保留灰色地带说明

### 4. 修改 `cs/SKILL.md`

**位置**：第 128-136 节沉淀类技能判别口诀

**修改前**：
- 完整判别口诀

**修改后**：
- 在标题后新增"（完整判据见 `.codestable/reference/terminology.md` 第 2 节）"
- 保留判别口诀（局部可读性）

### 5. 修改 `cs-feat/SKILL.md`

**位置**：第 119-123 节"与 issue 工作流的边界"

**修改前**：
- issue = bug / 异常 / 文档错误（缺"性能问题"）

**修改后**：
- issue = bug / 异常 / 文档错误 / 性能问题（补齐）
- 新增"完整判据见 `.codestable/reference/terminology.md` 第 1 节"
- 保留灰色地带说明

## 验证结果

### 1. 复现步骤验证

- [x] terminology.md 已创建并包含 5 类判据
- [x] system-overview.md 已更新，增加 terminology 指针
- [x] cs-issue / cs / cs-feat 已更新，保留短摘要并指向 terminology

### 2. 期望行为验证

- [x] 关键术语判据有单一权威来源
- [x] 各 skill 保留短摘要 + 指针，降低跳转成本
- [x] 修改判据时只需改 terminology.md

### 3. 影响面回归

- [x] feature / issue 边界定义已统一（cs-feat 补齐"性能问题"）
- [x] 沉淀类技能判据已归口到 terminology
- [x] 不影响其他 skill 或功能

## 修复方式

- 新建 terminology.md 作为权威来源
- 修改相关 skill 保留短摘要并指向 terminology
- 修正 cs-feat 的 issue 定义（补齐"性能问题"）

## 后续建议

后续新增 workflow 或术语判据时：
1. 在 `.codestable/reference/terminology.md` 增加对应小节
2. 在相关 skill 增加短摘要 + 指针
3. 确认所有相关入口的判据表述一致
