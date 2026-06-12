---
doc_type: issue-fix
issue: 2026-06-11-feat-plan-boundary-drift
status: completed
fixed_files: [cs-feat-plan/SKILL.md, .codestable/reference/shared-conventions.md]
related: [feat-plan-boundary-drift-report.md, feat-plan-boundary-drift-analysis.md]
tags: [workflow, cs-feat-plan, arch-drift, documentation]
---

# feat plan boundary drift 修复记录

## 修复方案

采用方案 A：统一为标准表述。

## 修复内容

### 标准表述

统一使用以下标准表述：

> `cs-feat-plan` 基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)。其中 checklist 的 `steps` 从 plan 的推进顺序派生，`checks` 从 design 各节约束派生。

### 1. 修改 `cs-feat-plan/SKILL.md:12`

**修改前**：
```markdown
把已批准 design 展开成可执行的 `plan.md`，并从 `design + plan` 抽出 `checklist.yaml`
```

**修改后**：
```markdown
基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)。其中 checklist 的 `steps` 从 plan 的推进顺序派生，`checks` 从 design 各节约束派生
```

**理由**：明确 plan 是 step source，checklist 是 status carrier，清晰说明派生关系。

### 2. 修改 `.codestable/reference/shared-conventions.md:146`

**修改前**：
```markdown
由 `cs-feat-plan` 在 approved design 后生成；`cs-feat-plan` 先落 `plan.md`，再从 design + plan 抽 `steps` + `checks`
```

**修改后**：
```markdown
`cs-feat-plan` 基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)。其中 checklist 的 `steps` 从 plan 的推进顺序派生，`checks` 从 design 各节约束派生
```

**理由**：使用标准表述，明确派生链。

### 3. 修改 `.codestable/reference/shared-conventions.md:156`

**修改前**：
```markdown
`cs-feat-plan` 基于已批准 design 生成 `plan.md` 与 `checklist.yaml`；design 仍然只决定范围和切片策略，不把 detailed step narrative 塞回 checklist
```

**修改后**：
```markdown
`cs-feat-plan` 基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)。其中 checklist 的 `steps` 从 plan 的推进顺序派生，`checks` 从 design 各节约束派生
```

**理由**：使用标准表述，统一派生关系描述。

### 4. 确认 `cs-feat-design/SKILL.md:12`

**当前内容**：
```markdown
后续由 `cs-feat-plan` 基于已批准 design 生成 `{slug}-plan.md` 与 `{slug}-checklist.yaml`
```

**确认**：此处为简短指针，与标准表述不冲突，保持不变。

## 验证结果

### 1. 复现步骤验证

- [x] 所有涉及 cs-feat-plan 的文档已使用统一标准表述
- [x] cs-feat-plan/SKILL.md 已更新
- [x] shared-conventions.md 两处均已更新
- [x] cs-feat-design/SKILL.md 确认不冲突

### 2. 期望行为验证

- [x] 所有相关文档对 cs-feat-plan 职责的描述完全一致
- [x] 明确派生链：design → plan → checklist
- [x] 标准表述清晰说明 plan 是 step source，checklist 是 status carrier

### 3. 影响面回归

- [x] 不影响其他 skill 或功能
- [x] 修改范围符合 analysis 声明（cs-feat-plan + shared-conventions 2 处）
- [x] cs-feat-design 简短指针与标准表述不冲突

## 修复方式

- 使用统一标准表述替换 3 处职责描述
- 明确 plan 是 step source，checklist 是 status carrier
- 明确派生关系：steps 从 plan 派生，checks 从 design 约束派生

## 后续建议

后续修改 cs-feat-plan 职责时：
1. 优先修改标准表述定义
2. 同步到所有引用该表述的文档
3. 确保派生链描述一致
