---
doc_type: issue-fix
status: completed
issue: 2026-06-17-docs-exceed-300-line-limit
path: standard
fix_date: 2026-06-17
related: [docs-exceed-300-line-limit-analysis.md]
tags: [documentation, code-style, technical-debt, refactoring]
---

# 4 个核心文档超过 300 行限制 修复记录

## 1. 实际采用方案

采用 analysis 确认的 **方案 A：按内容模块垂直拆分**。

具体执行：

1. `cs-feat-design/SKILL.md`
   - 拆出 `initialization-mode.md`
   - 拆出 `reuse-analysis-guide.md`
   - 主文件保留核心流程、入口说明和关键约束
2. `cs-feat-design/reference.md`
   - 拆出 `reference-frontmatter.md`
   - 拆出 `reference-templates.md`
   - 拆出 `reference-writing-guide.md`
   - 主文件改为参考入口导航
3. `cs-feat-accept/SKILL.md`
   - 拆出 `acceptance-checklist-guide.md`
   - 主文件保留启动检查、章节依赖、核对节奏、退出条件和收尾规则
4. `cs-refactor/reference/methods.md`
   - 拆出 `methods-L1-L2.md`
   - 拆出 `methods-L3.md`
   - 拆出 `methods-L4.md`
   - 主文件改为方法索引 + 速查入口
5. 补充更新运行时引用路径，确保技能文档仍能正确导航到拆分后的文件

## 2. 改动文件清单

### 修改文件
- `cs-feat-design/SKILL.md`
- `cs-feat-design/reference.md`
- `cs-feat-accept/SKILL.md`
- `cs-feat-plan/SKILL.md`
- `cs-refactor/SKILL.md`
- `cs-refactor-ff/SKILL.md`
- `cs-refactor/reference/methods.md`
- `cs-refactor/reference/scan-checklist-format.md`
- `.codestable/issues/2026-06-17-docs-exceed-300-line-limit/docs-exceed-300-line-limit-report.md`
- `.codestable/issues/2026-06-17-docs-exceed-300-line-limit/docs-exceed-300-line-limit-analysis.md`

### 新增文件
- `cs-feat-design/initialization-mode.md`
- `cs-feat-design/reuse-analysis-guide.md`
- `cs-feat-design/reference-frontmatter.md`
- `cs-feat-design/reference-templates.md`
- `cs-feat-design/reference-writing-guide.md`
- `cs-feat-accept/acceptance-checklist-guide.md`
- `cs-refactor/reference/methods-L1-L2.md`
- `cs-refactor/reference/methods-L3.md`
- `cs-refactor/reference/methods-L4.md`

## 3. 验证结果

### 复现步骤验证
按修订后的 report 第 2 节执行：

```bash
wc -l cs-feat-design/SKILL.md cs-feat-design/reference.md cs-feat-accept/SKILL.md cs-refactor/reference/methods.md
```

结果：
- `cs-feat-design/SKILL.md` → 277 行
- `cs-feat-design/reference.md` → 13 行
- `cs-feat-accept/SKILL.md` → 134 行
- `cs-refactor/reference/methods.md` → 58 行

4 个目标文件全部 ≤ 300 行，问题不再复现。

### 期望行为验证
期望行为是“4 个核心技能文档遵守单 md 文档不超过 300 行的项目约束，并在拆分后保持可用”。

验证结果：
- 4 个目标文件全部降到 300 行以内
- 新拆分文件也全部 ≤ 300 行
- 运行时旧引用已清理，入口文档已指向新拆分文件
- `git diff --check` 通过
- issue report / analysis frontmatter 校验通过

### 影响面回归
对 analysis 第 4 节涉及的潜在影响做了最基本回归：

- `cs-feat-design`：主流程仍保留在 `SKILL.md`，复用分析与参考模板通过拆分文件承接
- `cs-feat-plan`：已改为引用 `reference-templates.md`
- `cs-feat-accept`：主技能保留流程入口，模板与核对节迁到 `acceptance-checklist-guide.md`
- `cs-refactor` / `cs-refactor-ff`：已改为“索引 + 分层详情”模式
- `cs-refactor/reference/scan-checklist-format.md`：已同步到新方法库结构

### 额外验证
- `rg` 检查运行时旧引用：无残留
- `git diff --check`：通过
- `.codestable/issues/.../report.md` 与 `analysis.md`：frontmatter 校验通过

## 4. 遗留事项

- 本 issue 只修复最初确定的 4 个目标文件；仓库中仍有其他超过 300 行的 Markdown（如 `README.md`、`README.en.md`、`asset/` 下的设计资料、历史 `.codestable/refactors/` 产物），不在本次 issue 范围内。
- 如果项目希望把“300 行约束”扩展到 README、asset 文档、历史 spec 产物，建议后续另开新 issue 或 roadmap 统一治理。
- 本次未引入自动检查脚本；如果后续想防止再次超标，可单独开一个 issue 增加文档长度健康检查工具。
