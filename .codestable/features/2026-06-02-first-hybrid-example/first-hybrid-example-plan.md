---
doc_type: feature-plan
feature: 2026-06-02-first-hybrid-example
design: first-hybrid-example-design.md
status: approved
---

# first-hybrid-example execution plan

## 1. 执行目标

这份 plan 只承接已批准的 design，目标是把当前仓库里的 hybrid 工作流整理成一条可直接模仿的黄金样板，并保证它通过 workflow-check 与 acceptance 双验证。

## 2. 分步计划

### Step 1 — 明确样板范围
- **目标**：确认这条样板只消费现有规则，不再引入新协议
- **触碰范围**：`first-hybrid-example-design.md`
- **退出信号**：样板目标已经覆盖 design / plan / checklist / acceptance / 回写五件事
- **验证**：人工核对 design 第 1 节成功标准

### Step 2 — 落齐四件套产物
- **目标**：让当前样板目录拥有 design / plan / checklist / acceptance 四件套
- **触碰范围**：`.codestable/features/2026-06-02-first-hybrid-example/`
- **退出信号**：目录中存在四件套文件，且 design frontmatter 明确 `workflow: hybrid`
- **验证**：find 当前目录并核对文件名

### Step 3 — 跑通 workflow-check
- **目标**：让这条样板通过 workflow-check 校验
- **触碰范围**：`.codestable/tools/validate-yaml.py` 的现有入口与当前样板目录
- **退出信号**：`--workflow-check` 对当前样板返回 0
- **验证**：运行 workflow-check 命令

### Step 4 — 完成验收归并
- **目标**：生成 acceptance 报告，并回写 architecture / roadmap
- **触碰范围**：当前样板 acceptance 文档、`ARCHITECTURE.md`、roadmap items/main doc
- **退出信号**：当前样板形成真正闭环
- **验证**：acceptance 完成后检查 roadmap item = done，架构文档已归并

## 3. 风险与回退

- 风险 R1：样板复制了旧样板的措辞，但和当前共享约定已脱节。
  - 回退 / 止损：所有关键说法都以 shared conventions / tools / architecture 当前版本为准，逐条回对。
- 风险 R2：样板四件套齐了，但 workflow-check 或 acceptance 仍未通过。
  - 回退 / 止损：以当前 feature 为唯一修正对象，先修产物一致性，再谈提交。

## 4. 与 checklist 的映射

- Step 1 → checklist.steps[0]
- Step 2 → checklist.steps[1]
- Step 3 → checklist.steps[2]
- Step 4 → checklist.steps[3]
