---
doc_type: issue-report
issue: 2026-06-17-docs-exceed-300-line-limit
status: confirmed
severity: P1
summary: 4 个核心文档超过 300 行限制违反项目编码规范
tags: [documentation, code-style, technical-debt]
---

# 4 个核心文档超过 300 行限制 Issue Report

## 1. 问题现象

项目中有 4 个 Markdown 文档的行数超过了 CLAUDE.md 中规定的 300 行上限，违反了项目编码规范：

1. `cs-feat-design/SKILL.md` - 369 行
2. `cs-feat-design/reference.md` - 352 行  
3. `cs-feat-accept/SKILL.md` - 311 行
4. `cs-refactor/reference/methods.md` - 394 行

## 2. 复现步骤

1. 在项目根目录执行：
   ```bash
   wc -l cs-feat-design/SKILL.md cs-feat-design/reference.md cs-feat-accept/SKILL.md cs-refactor/reference/methods.md
   ```
2. 观察到这 4 个核心技能文档的行数都超过 300 行限制

复现频率：稳定复现（文档行数固定）

## 3. 期望 vs 实际

**期望行为**：所有 Markdown 文档应该遵守 CLAUDE.md 规定，单个文件不超过 300 行；超过时应该拆分成多个文件

**实际行为**：4 个核心文档超过了 300 行限制，未进行拆分

## 4. 环境信息

- 涉及模块 / 功能：文档规范遵从性
- 相关文件：
  - `cs-feat-design/SKILL.md` (369 行)
  - `cs-feat-design/reference.md` (352 行)
  - `cs-feat-accept/SKILL.md` (311 行)
  - `cs-refactor/reference/methods.md` (394 行)
- 运行环境：开发环境（仓库源码）
- 其他上下文：CLAUDE.md 第 130 行明确规定"单md文档不能超过300行，超过必须拆分"

## 5. 严重程度

**P1 严重** — 违反了项目明确的编码规范，影响文档可维护性和 AI 阅读效率；不阻塞当前功能运行，但应尽快修复以保持代码库健康

## 备注

这 4 个文档都是 CodeStable 工作流的核心技能文档，需要在拆分时保持：
- 技能功能完整性
- 文档间引用关系正确
- 用户体验不受影响
