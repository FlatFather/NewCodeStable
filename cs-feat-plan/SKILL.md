---
name: cs-feat-plan
description: feature 流程阶段 2——基于已批准的 `{slug}-design.md` 生成 `{slug}-plan.md` 与 `{slug}-checklist.yaml`，在进入实现前形成独立确认关口。触发：用户说"开始出计划"、"生成 plan"、"设计已过开始拆执行步骤"，或 `{slug}-design.md` 已 approved 但 plan/checklist 尚未落齐。
---

# cs-feat-plan

## 启动必读

本技能启动前需读取：
- `.codestable/attention.md` — 项目注意事项
- `.codestable/reference/shared-conventions-core.md` — 目录结构与命名规则
- `.codestable/reference/shared-conventions-feature.md` — feature 产物职责边界
- `.codestable/reference/shared-conventions-checklist.md` — checklist 生命周期

**缓存优化**：上述文件若已在本轮对话中读取过，输出”已复用上下文”并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。

`cs-feat-design` 负责把”做什么 / 为什么做 / 范围到哪”为人类拍板清楚；`cs-feat-plan` 接手后只做一件事：基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)。其中 checklist 的 `steps` 从 plan 的推进顺序派生，`checks` 从 design 各节约束派生。用户在进入实现前有一个单独的执行计划确认关口。

> 共享路径与命名约定看 `.codestable/reference/shared-conventions-core.md`。`plan.md` 是 step source，`checklist.yaml` 是 status carrier；详细生命周期看 `.codestable/reference/shared-conventions-feature.md` 和 `.codestable/reference/shared-conventions-checklist.md`；本阶段不改 scope。

---

## 启动检查

1. **design 已批准**——`{slug}-design.md` 必须存在且 `status=approved`
2. **尚未进入实现**——若代码已开始改动，先和用户确认是回补 plan，还是回 design 重新收口
3. **feature 目录已存在**——不在本阶段新建 feature 目录
4. **上下文读全**——读 approved design 全文 + `.codestable/attention.md` + 相关 shared conventions / architecture + `.codestable/reference/workflow-continuation.md`（如本次是短回复续作或涉及 task 状态桥）

缺任一项 → 退回 `cs-feat-design` 或让用户先澄清。

---

## 本阶段产出

1. `{slug}-plan.md`
2. `{slug}-checklist.yaml`

两者都放在 feature 目录内；落盘后都要做 YAML/frontmatter 校验。

---

## 生成原则

### 1. plan 只承接已批准 design

- 不重复术语表、需求摘要、明确不做
- 不新增 design 未批准的范围
- 只回答：按什么顺序做、每步怎么判断完成

### 2. checklist 从 design + plan 派生

- `steps`：来自 design 的推进策略切片 + plan 的分步计划
- `checks`：来自 design 第 1/2/3 节的范围守护、名词契约、流程级约束、挂载点、验收场景
- checklist 不写大段解释，解释留在 plan

### 3. 本阶段有独立 checkpoint

如果用户这轮输入只是 `继续 / 确认 / 同意 / 跳过 / 继续下一步` 这类短回复，先按 continuation-first 恢复已有 feature 目录状态：
- 已有 `plan.md` + `checklist.yaml` 且内容完整 → 直接汇报当前执行顺序，不重复生成
- 只有其一存在或内容不完整 → 补缺失项再统一汇报
- 多个候选 feature 目录 → 停下来让用户选，不猜
- `.ccg/tasks/*/task.json` 只作恢复桥，不替代 feature 目录中的 design / plan / checklist 真相源

plan/checklist 落盘后，要先让用户确认“这就是执行顺序”，再进入 `cs-feat-impl`。不要一口气从 design 直接跳进代码。

---

## 流程

### 1. 生成 `{slug}-plan.md`

按 `cs-feat-design/reference.md` 里的 plan 模板生成：
- 执行目标
- 分步计划
- 风险与回退
- 与 checklist 的映射

### 2. 生成 `{slug}-checklist.yaml`

按同一 reference 里的 checklist 模板生成：
- `steps`
- `checks`

### 3. 校验

- `python .codestable/tools/validate-yaml.py --file {slug}-plan.md`
- `python .codestable/tools/validate-yaml.py --file {slug}-checklist.yaml --yaml-only`

### 4. 汇报并停下

固定汇报：

```markdown
## plan 阶段完成汇报

### 新生成的文件
- {slug}-plan.md
- {slug}-checklist.yaml

### 核心步骤摘要
- Step 1: ...
- Step 2: ...

### 是否改了 design scope？
- 否

### 校验结果
- plan frontmatter：通过 / 失败
- checklist yaml：通过 / 失败
```

汇报后停等用户确认，再进入 `cs-feat-impl`。

---

## 退出条件

- [ ] `{slug}-plan.md` 已生成
- [ ] `{slug}-checklist.yaml` 已生成
- [ ] 两者校验通过
- [ ] 未越权改写 design scope
- [ ] 已向用户汇报并等待进入实现阶段

---

## 退出后

告诉用户：

> 执行计划已就绪。下一步阶段 3 分步实现，触发 `cs-feat-impl`。
