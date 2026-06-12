---
doc_type: issue-fix
issue: 2026-06-12-feat-ff-attention-inventory-missing
status: completed
fixed_files: [cs-feat-ff/SKILL.md]
related: [feat-ff-attention-inventory-missing-report.md]
tags: [workflow, cs-feat-ff, attention-md, rule-sync]
---

# feat ff attention inventory missing 修复记录

## 修复方案

快速通道：在 `cs-feat-ff/SKILL.md` 收尾推荐中增加 attention.md 候选盘点提示。

## 修复内容

### 修改 `cs-feat-ff/SKILL.md:183-187`

**修改前**：
```markdown
按 `shared-conventions.md` 第 3 节"feature-ff"收尾推荐顺序逐项一句话提示（用户"不用"立即跳过）：

1. 暴露的坑 → "沉淀 learning？（`cs-learn`）"
2. 拍板的长期约束 → "归档决定？（`cs-decide`）"
3. 最后问是否代为 scoped-commit
```

**修改后**：
```markdown
按 `shared-conventions.md` 第 3 节"feature-ff"收尾推荐顺序逐项一句话提示（用户"不用"立即跳过）：

1. 暴露的坑 → "沉淀 learning？（`cs-learn`）"
2. 拍板的长期约束 → "归档决定？（`cs-decide`）"
3. 环境坑点 → "发现需要记到 attention.md 的吗？（`cs-note`）"
4. 最后问是否代为 scoped-commit
```

**理由**：补充 attention.md 候选盘点提示，与 `cs-feat-accept` 第 8 节保持一致（轻量版本）。fastforward 虽跳过详细验收，但仍可能暴露环境坑点，需提示盘点。

## 验证结果

- [x] cs-feat-ff 收尾推荐已增加 attention.md 盘点提示
- [x] 与 cs-feat-accept 保持一致（轻量版本）
- [x] 按顺序：learning → decision → attention → commit

## 修复方式

快速通道：补充轻量 attention.md 盘点提示。
