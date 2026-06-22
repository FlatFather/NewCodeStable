---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "02"
nature: maintainability
severity: P1
confidence: high
title: "启动必读"段落在 10+ 个技能中逐字重复，修改时易遗漏
status: fixed
fixed_by: .codestable/tools/inject-startup-boilerplate.py
fixed_date: 2026-06-18
notes: 创建自动化脚本统一管理启动必读段落；修复 cs-feat-plan 中文引号问题
tags: [duplication, skills, boilerplate, maintenance-cost]
---

# Finding-02: "启动必读"段落在 10+ 个技能中逐字重复

## 问题描述

所有阶段 skill 的 SKILL.md 都包含完全相同的"启动必读"段落（3 行）：

```markdown
## 启动必读

开始任何判断或动作前，先读取 `.codestable/attention.md`；缺失则视为骨架不完整，提示先补齐或运行 `cs-onboard`，不要回退到外部 AI 入口文件。
```

这段文本在至少 **10+ 个 skill** 中逐字复制。

## 证据

**命中文件**（已验证）：
- `cs-audit/SKILL.md:8-10`
- `cs-feat/SKILL.md:8-10`
- `cs-feat-design/SKILL.md:8-10`
- `cs-feat-plan/SKILL.md:8-10`
- `cs-feat-impl/SKILL.md:8-10`
- `cs-feat-accept/SKILL.md:8-10`
- `cs-issue/SKILL.md:8-10`
- `cs-issue-report/SKILL.md:8-10`
- `cs-issue-analyze/SKILL.md:?` (未读取但推测存在)
- `cs-issue-fix/SKILL.md:?` (未读取但推测存在)

**重复行数统计**：3 行 × 10+ 个文件 = 30+ 行重复文本

## 为什么构成 P1

**维护成本**：
- 修改"启动必读"规则时需要逐文件搜索替换
- 遗漏单个文件 → 该 skill 口径与其他 skill 不一致
- 新增 skill 时容易忘记复制这段或复制到旧版本

**已知变更风险**：
- `attention.md` 改名 → 需要改 10+ 处
- 增加"缺失时的 fallback 规则" → 需要改 10+ 处
- onboard 逻辑变更 → 需要改 10+ 处

## 建议修复方案

**方案 A（推荐）：提取到 shared include**

1. 创建 `.codestable/reference/boilerplate/startup-check.md`
2. 所有 skill 的"启动必读"节改为：`<!-- include: .codestable/reference/boilerplate/startup-check.md -->`
3. 写一个预处理脚本在 skill 加载时展开 include（或 AI 直接读 shared boilerplate）

**方案 B：生成脚本**

1. 写 `.codestable/tools/inject-boilerplate.py`
2. 从单一 boilerplate 源生成所有 skill 的"启动必读"节
3. pre-commit hook 自动运行，确保 boilerplate 同步

**方案 C：只保留指针**

- 所有 skill 的"启动必读"节改为一句话：`启动规则见 .codestable/reference/shared-conventions.md 第 X 节`
- 被拒原因：增加 skill 启动时的跳转成本

## 建议动作

走 **`cs-refactor`** 流程（行为不变、结构优化）：
1. 选定方案 A 或 B
2. 一次性重构所有 skill
3. 验证 boilerplate 修改后自动同步生效
