---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "03"
nature: maintainability
severity: P1
confidence: medium
title: 术语判据分散在多个技能，无统一权威定义
status: partially-fixed
fixed_by: inline
fixed_date: 2026-06-18
notes: 核心路由判据（cs/cs-feat/cs-issue）已引用 terminology.md；其他技能提到相关概念时可继续补充引用
tags: [terminology, fragmentation, decision-criteria]
---

# Finding-03: 术语判据分散在多个技能，无统一权威定义

## 问题描述

多个常见术语的**判据**（如何判断 A 还是 B）分散在不同 skill 中，没有统一权威定义。当判据需要更新时，容易遗漏某个 skill 导致判断不一致。

## 证据

**典型案例 1：feature vs issue 边界**

- `cs-feat/SKILL.md:119-123`：
  ```markdown
  - feature：从来没有的东西要加进来（新功能 / 新能力）
  - issue：本来应该好的东西坏了（bug / 异常 / 文档错误）
  ```

- `cs-issue/SKILL.md:104-109`：
  ```markdown
  - issue：本来应该好的东西坏了——已有代码里的 bug / 异常行为 / 文档错误 / 性能问题
  - feature：从来没有的东西要加进来——新功能 / 新能力
  ```

→ 两处定义**微小差异**（issue 在 cs-issue 中多了"性能问题"）

**典型案例 2：沉淀类四技能区分**

- `cs/SKILL.md:127-135`：判别口诀
- `system-overview.md:69-78`：区分说明

→ **两处重复**，未来修改需同步

**典型案例 3：fastforward vs 标准 feature 边界**

- `cs-feat/SKILL.md:60`：fastforward 判据
- `cs-feat-design/SKILL.md`：未显式重复此判据

→ 判据**只在一处**，其他 skill 靠隐式理解

## 为什么构成 P1

**影响范围**：
- 判据不一致 → 用户在不同入口得到矛盾建议
- 判据更新遗漏 → 部分 skill 沿用旧规则

**维护成本**：
- 每次改判据需要 grep 所有 skill
- 新 skill 作者不知道判据散落在哪里

## 建议修复方案

**方案 A（推荐）：统一到 terminology reference**

1. 创建 `.codestable/reference/terminology.md`
2. 收口所有"A vs B"类判据：
   - feature vs issue
   - learning vs trick vs decision vs explore
   - fastforward vs 标准 feature
   - 标准路径 vs 快速通道（issue）
3. 各 skill 只保留指针："判据见 terminology.md"

**方案 B：合并到 shared-conventions 专节**

- 在 `shared-conventions.md` 增加"术语判据"专节
- 被拒原因：shared-conventions 已超 300 行，继续堆积会违反长度约束

**方案 C：保持现状，增加同步检查**

- 写脚本检查各 skill 的判据是否一致
- 被拒原因：治标不治本，仍需人工维护多处

## 建议动作

走 **`cs-refactor`** 流程：
1. 创建 `terminology.md` 或在 shared-conventions 专节统一判据
2. 所有 skill 改为引用统一判据
3. 验证判据修改后只需改一处
