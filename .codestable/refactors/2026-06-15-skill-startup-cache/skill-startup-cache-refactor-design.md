---
doc_type: refactor-design
refactor: 2026-06-15-skill-startup-cache
status: draft
scope: 24 个 cs-* 技能的启动逻辑 + shared-conventions.md 拆分
summary: 通过共享检查逻辑 + 缓存判断 + 文档拆分，彻底解决重复读取造成的 token 浪费
---

# skill-startup-cache refactor design

## 1. 本次范围

**从 scan 勾选的条目**：
- ✓ #1：提取"启动必读"到共享检查逻辑（M-L2-05）
- ✓ #2：增加缓存判断逻辑（M-L4-01）
- ✓ #3：拆分 shared-conventions.md（M-L4-06）

**明确不做的**：
- 不修改技能的核心业务逻辑
- 不改变 attention.md 和 shared-conventions.md 的内容
- 不引入新的依赖或工具

**预估总工作量**：4h  
**总风险档位**：中（24 个文件批量改动，需要逐个验证）

---

## 2. 前置依赖

### 2.1 验证 boilerplate 文件已存在

- 文件：`.codestable/reference/boilerplate/startup-check.md`
- 状态：已存在（P1-02 创建）
- 验证方式：`Read` 确认内容完整

### 2.2 备份当前技能文件

- 在开始批量改动前，记录当前 git 状态
- 验证方式：`git status --short` 无未提交改动

### 2.3 准备测试技能列表

抽查技能列表（覆盖 feature / issue / compound 各类）：
- `cs-feat-design`
- `cs-feat-plan`
- `cs-issue-report`
- `cs-learn`

---

## 3. 执行顺序

### 步骤 1：拆分 shared-conventions.md

**引用方法**：M-L4-06（Split Large Document）

**具体操作**：
1. 创建 4 个拆分文件：
   - `shared-conventions-core.md`（目录结构 + 命名规则，第 0 节）
   - `shared-conventions-feature.md`（feature 产物职责，第 2 节）
   - `shared-conventions-checklist.md`（checklist 生命周期，第 3 节）
   - `shared-conventions-roadmap.md`（roadmap 衔接，第 2.5 节）
2. 保留原 `shared-conventions.md` 作为索引入口，包含：
   - frontmatter 说明已拆分
   - 各模块摘要 + 指向拆分文件的链接
3. 更新各技能 SKILL.md 中的引用路径（按需引用对应模块）

**退出信号**：
- AI 自证：`grep "shared-conventions" */SKILL.md` 所有引用路径正确
- HUMAN：抽查 4 个技能实际运行无报错

**验证责任**：HUMAN

**回滚**：`git revert` 本步提交

---

### 步骤 2：统一"启动必读"段落格式

**引用方法**：M-L2-05（Extract Duplicate Logic）

**具体操作**：
1. 在每个技能的"启动必读"段落改为标准格式：
   ```markdown
   ## 启动必读
   
   开始任何判断或动作前，先读取 `.codestable/attention.md`；缺失则视为骨架不完整，提示先补齐或运行 `cs-onboard`，不要回退到外部 AI 入口文件。
   ```
2. 确保 24 个技能格式完全一致（为步骤 3 批量替换做准备）

**退出信号**：
- AI 自证：`grep -A 2 "## 启动必读" */SKILL.md | grep "开始任何判断"` 返回 24 行
- HUMAN：无需验证（纯文本统一）

**验证责任**：AI 自证

**回滚**：`git revert` 本步提交

---

### 步骤 3：增加缓存判断逻辑到所有技能

**引用方法**：M-L4-01（Add Caching Layer）

**具体操作**：
1. 将"启动必读"段落替换为包含缓存判断的新版本：
   ```markdown
   ## 启动必读
   
   本技能启动前需要读取 `.codestable/attention.md`（项目注意事项）和 `.codestable/reference/shared-conventions-{module}.md`（跨技能共享口径）。
   
   **缓存优化**：
   - 如果本轮对话历史中已包含这些文件的内容，输出"已在本轮对话读取，复用上下文"并跳过 Read
   - 否则执行 Read
   
   **检查规则**：骨架不完整（attention.md 缺失）时，提示先补齐或运行 `cs-onboard`。
   ```
2. 批量应用到 24 个技能（使用 sed 或 Edit 逐个替换）

**退出信号**：
- AI 自证：
  - `grep "缓存优化" */SKILL.md | wc -l` 返回 24
  - 运行完整 feature 流程（design → plan → impl → accept），观察 Read 调用次数从 8 次降低到 2 次
- HUMAN：抽查 4 个技能实际运行，确认仍能正常读取 attention.md 内容

**验证责任**：HUMAN

**回滚**：`git revert` 本步提交

---

### 步骤 4：全量测试

**引用方法**：无（验证步骤）

**具体操作**：
1. 运行完整 feature 流程（`cs-feat-design` → `cs-feat-plan` → `cs-feat-impl` → `cs-feat-accept`）
2. 运行完整 issue 流程（`cs-issue-report` → `cs-issue-analyze` → `cs-issue-fix`）
3. 确认每个技能都能正常启动，且 Read 调用次数符合预期

**退出信号**：
- HUMAN：两条完整流程执行无报错
- HUMAN：确认 token 节省效果（Read 调用次数显著减少）

**验证责任**：HUMAN

**回滚**：无需回滚（验证步骤）

---

## 4. 风险与看点

**高风险步骤**：
- 步骤 1（文档拆分）：需要更新所有引用路径，遗漏会导致技能读取失败
- 步骤 3（批量替换）：24 个文件批量改动，任何一个格式错误都会导致该技能无法启动

**容易出错的点**：
- 拆分后的文档路径引用不一致
- 缓存判断逻辑描述不清晰，AI 无法正确执行
- 某些技能的"启动必读"段落格式特殊，批量替换会破坏

**缓解措施**：
- 每步完成后立即抽查 4 个技能
- 步骤 3 采用逐个文件 Edit 而非全局 sed（更安全）
- 保持 git 提交粒度细（每步一个 commit），便于回滚

---

## 5. 预期收益

**Token 节省**（按完整 feature 流程计算）：

- **当前**：
  - attention.md（25 行）× 4 次 = 100 行
  - shared-conventions.md（330 行）× 4 次 = 1320 行
  - **总计**：1420 行

- **优化后**：
  - attention.md（25 行）× 1 次 = 25 行
  - shared-conventions-{module}.md（平均 80 行）× 1 次 = 80 行
  - **总计**：105 行

- **节省**：1420 - 105 = **1315 行 / 次完整流程**（节省 93%）

---

## 6. 退出后续

完成后建议：
1. 更新 `.codestable/reference/system-overview.md`，说明新的文档结构
2. 在 `.codestable/compound/` 添加 learning 文档，记录"如何在技能中实现缓存判断"
3. 更新 `cs-onboard` 的模板，新项目自动采用拆分后的文档结构
