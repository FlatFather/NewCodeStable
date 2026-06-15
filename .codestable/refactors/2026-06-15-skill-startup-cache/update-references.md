# 技能引用路径更新映射表

根据每个技能实际引用的内容，映射到对应的拆分模块。

## 引用模块说明

- `core` = shared-conventions-core.md（第 0 节：目录结构与命名规则）
- `feature` = shared-conventions-feature.md（第 2 节：feature 产物职责边界）
- `checklist` = shared-conventions-checklist.md（第 3 节：checklist 生命周期）
- `roadmap` = shared-conventions-roadmap.md（第 2.5 节：roadmap ↔ feature 衔接）
- `main` = shared-conventions.md（第 1, 3-7 节：元数据、收尾、归档、反射检查）

## 技能引用映射

| 技能 | 当前引用节 | 需要的模块 |
|------|----------|----------|
| cs-arch | 第 0, 5, 6 节 | core, main |
| cs-audit | 第 5 节 | main |
| cs-brainstorm | 第 5 节 | main |
| cs-decide | 第 5, 6 节 | main |
| cs-explore | 第 5, 6 节 | main |
| cs-feat | 第 2 节 | feature |
| cs-feat-accept | 第 2, 2.5, 3 节 | feature, roadmap, checklist, main |
| cs-feat-design | 第 0, 2, 2.5, 5 节 | core, feature, roadmap, main |
| cs-feat-ff | 第 0, 2, 3 节 | core, feature, main |
| cs-feat-impl | 第 2, 3, 7 节 | feature, checklist, main |
| cs-feat-plan | 第 2, 3 节 | feature, checklist |
| cs-issue | - | - |
| cs-issue-analyze | 第 5 节 | main |
| cs-issue-fix | 第 3, 5, 7 节 | main |
| cs-issue-report | 第 0 节 | core |
| cs-learn | 第 5, 6 节 | main |
| cs-onboard | 第 0 节（模板源） | 需更新模板 |
| cs-refactor | 第 3, 5 节 | main |
| cs-req | 第 5 节 | main |
| cs-roadmap | 第 0, 2.5 节 | core, roadmap |
| cs-trick | 第 5, 6 节 | main |

## 更新策略

1. **引用整个文档的**：改为 `.codestable/reference/shared-conventions.md`（索引入口）
2. **引用特定节的**：改为对应的拆分模块
3. **cs-onboard**：需同时更新 `reference/` 模板目录
