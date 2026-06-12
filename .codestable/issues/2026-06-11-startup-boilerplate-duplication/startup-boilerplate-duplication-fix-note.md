---
doc_type: issue-fix
issue: 2026-06-11-startup-boilerplate-duplication
status: completed
fixed_files: [.codestable/reference/boilerplate/startup-check.md]
related: [startup-boilerplate-duplication-report.md, startup-boilerplate-duplication-analysis.md]
tags: [workflow, skills, boilerplate, maintainability]
---

# startup boilerplate duplication 修复记录

## 修复方案

采用方案 A（简化版）：建立 boilerplate 权威来源。

## 修复内容

### 1. 创建 `.codestable/reference/boilerplate/startup-check.md`

**新建文件**：`.codestable/reference/boilerplate/startup-check.md`

**内容**：
- 保存"启动必读"3 行文本作为权威来源
- 顶部 HTML 注释说明：
  - 这是所有 CodeStable skill 的"启动必读"段落权威来源
  - 修改本文件后需同步到所有 skill
  - 提供同步命令示例

**设计决策**：
- 各 skill 保留当前完整"启动必读"文本（不改为引用）
- 避免增加 skill 启动时的跳转成本
- 保持当前使用体验
- 建立"权威来源"概念，后续修改规则时先改 boilerplate 文件再同步

## 验证结果

### 1. 复现步骤验证

- [x] boilerplate 文件已创建
- [x] 文件包含完整"启动必读"段落
- [x] 顶部注释说明修改后需同步
- [x] 提供同步命令示例

### 2. 期望行为验证

- [x] 建立了单一权威来源
- [x] 后续修改规则时有明确的同步流程
- [x] 不影响当前 skill 使用体验（各 skill 保留完整文本）

### 3. 影响面回归

- [x] 仅新建 1 个文件，不修改现有 skill
- [x] 不影响任何 skill 的当前行为
- [x] 为后续维护建立了明确的权威来源

## 修复方式

- 创建 boilerplate 权威来源文件
- 各 skill 保持现状（不改为引用）
- 提供同步命令示例供维护者使用

## 后续建议

后续修改"启动必读"规则时：
1. 先修改 `.codestable/reference/boilerplate/startup-check.md`
2. 使用文件顶部提供的同步命令同步到所有 skill
3. 验证所有 skill 的"启动必读"段落一致

可选优化（不在本次 issue 范围）：
- 开发自动同步脚本
- 配置 pre-commit hook 检查一致性
