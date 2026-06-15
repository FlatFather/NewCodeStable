---
doc_type: refactor-scan
refactor: 2026-06-15-skill-startup-cache
date: 2026-06-15
scope: 24 个 cs-* 技能的"启动必读"段落
summary: 优化重复读取 attention.md 和 shared-conventions.md 造成的 token 浪费
status: pending_review
---

# skill-startup-cache 扫描清单

## 总览

**扫描范围**：24 个 cs-* 技能的 SKILL.md 文件（每个文件的"启动必读"段落）

**发现条数**：3 条优化点

**按分类分布**：
- L2 代码级重构：1 条（重复逻辑提取）
- L4 性能优化：2 条（缓存判断 + 文档拆分）

**按风险分布**：
- 低风险（AI 可自证）：2 条
- 中风险（需 HUMAN 验证）：1 条

**建议执行顺序**：
1. 先做 #1（重复逻辑提取到共享函数）— 为后续缓存判断打基础
2. 再做 #2（增加缓存判断逻辑）— 核心优化
3. 最后做 #3（拆分大文档）— 可选，进一步降低单次读取成本

**慎做项**：无

---

## 优化点 #1：提取"启动必读"段落到共享检查逻辑

**分类**：L2 代码级重构 - 重复逻辑提取  
**方法号**：M-L2-05（Extract Duplicate Logic）  
**风险**：低  
**预估工时**：1h  

**问题描述**：  
24 个技能的"启动必读"段落逐字重复相同的 3 行文本：
```markdown
开始任何判断或动作前，先读取 `.codestable/attention.md`；缺失则视为骨架不完整，提示先补齐或运行 `cs-onboard`，不要回退到外部 AI 入口文件。
```

**量化指标**：
- 重复次数：24 处
- 重复行数：3 行 × 24 = 72 行

**优化方法**：  
在每个技能的"启动必读"段落改为引用共享检查逻辑：
```markdown
## 启动必读

{{执行启动检查：读取 attention.md，检查骨架完整性}}
```

共享逻辑定义在 `.codestable/reference/boilerplate/startup-check.md`（P1-02 已创建）。

**退出信号**：  
- AI 自证：`grep "启动必读" */SKILL.md | wc -l` 仍为 24 行
- HUMAN：抽查 3 个技能实际运行无报错

**回滚策略**：  
`git revert` 本步提交

---

## 优化点 #2：增加缓存判断逻辑避免重复读取

**分类**：L4 性能优化 - 缓存判断  
**方法号**：M-L4-01（Add Caching Layer）  
**风险**：中  
**预估工时**：2h  

**问题描述**：  
同一轮对话中，多个技能重复读取相同文件：
- `attention.md`（~25 行）：feature 流程读 4 次
- `shared-conventions.md`（~330 行）：feature 流程读 4 次
- 总浪费：355 行 × 3 次冗余 = 1065 行 token

**量化指标**：
- 当前：每个技能启动必读取 2 个文件
- 目标：本轮对话首次读取后，后续技能复用缓存

**优化方法**：  
在"启动必读"段落增加缓存判断：
```markdown
## 启动必读

本技能启动前需要读取 `.codestable/attention.md`。

**缓存判断**（避免重复读取）：
- 检查本轮对话历史 tool_result 中是否已包含 `attention.md` 内容
- 已包含 → 输出"attention.md 已在本轮对话读取，复用上下文"
- 未包含 → 执行 Read

同理适用于 `.codestable/reference/shared-conventions.md`。
```

**退出信号**：  
- AI 自证：运行完整 feature 流程（design → plan → impl → accept），观察 Read 调用次数
- HUMAN：确认技能行为无变化（仍能正常读取到 attention.md 内容）

**回滚策略**：  
`git revert` 本步提交

---

## 优化点 #3：（可选）拆分 shared-conventions.md 降低单次读取成本

**分类**：L4 性能优化 - 文档拆分  
**方法号**：M-L4-06（Split Large Document）  
**风险**：低  
**预估工时**：1h  

**问题描述**：  
`shared-conventions.md` 约 330 行，包含多个独立主题（feature 产物 / checklist 生命周期 / roadmap 衔接等）。大部分技能只需要其中 1-2 个主题，但每次必须读取全文。

**量化指标**：
- 当前：单次读取 330 行
- 目标：按需读取 50-100 行

**优化方法**：  
拆分为：
- `shared-conventions-core.md`（~80 行）— 目录结构 + 命名规则
- `shared-conventions-feature.md`（~120 行）— feature 产物职责
- `shared-conventions-checklist.md`（~80 行）— checklist 生命周期
- `shared-conventions-roadmap.md`（~50 行）— roadmap 衔接协议

各技能按需引用对应模块。

**退出信号**：  
- AI 自证：所有技能 SKILL.md 中的引用路径更新完成
- HUMAN：确认技能仍能读取到所需规则

**回滚策略**：  
合并回单文件 + 更新所有引用

---

## 用户勾选区

请对每条优化点标记 ✓（执行）或 ✗（不执行，需附理由）：

- [ ] #1：提取"启动必读"到共享检查逻辑
- [ ] #2：增加缓存判断逻辑
- [ ] #3：（可选）拆分 shared-conventions.md

---

## 备注

- #1 是 #2 的前置依赖（先统一格式，再加缓存判断）
- #3 可独立执行，但与 #2 组合效果最佳
- 如果只做 #2，预估节省 token：~1000 行/次完整流程
- 如果 #2 + #3 组合，预估节省 token：~1200 行/次完整流程
