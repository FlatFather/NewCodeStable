---
name: cs-feat-plan
description: feature 流程阶段 2——基于已批准的 `{slug}-design.md` 生成 `{slug}-plan.md` 与 `{slug}-checklist.yaml`，在进入实现前形成独立确认关口。触发：用户说"开始出计划"、"生成 plan"、"设计已过开始拆执行步骤"，或 `{slug}-design.md` 已 approved 但 plan/checklist 尚未落齐。
---

# cs-feat-plan

## 启动必读

开始任何判断或动作前，先读取 `.codestable/attention.md`；缺失则视为骨架不完整，提示先补齐或运行 `cs-onboard`，不要回退到外部 AI 入口文件。

`cs-feat-design` 负责把“做什么 / 为什么做 / 范围到哪”为人类拍板清楚；`cs-feat-plan` 接手后只做一件事：把已批准 design 展开成可执行的 `plan.md`，并从 `design + plan` 抽出 `checklist.yaml`，让用户在进入实现前有一个单独的执行计划确认关口。

> 共享路径与命名约定看 `.codestable/reference/shared-conventions.md`。`plan.md` 是 step source，`checklist.yaml` 是 status carrier；本阶段不改 scope。

---

## 启动检查

1. **design 已批准**——`{slug}-design.md` 必须存在且 `status=approved`
2. **尚未进入实现**——若代码已开始改动，先和用户确认是回补 plan，还是回 design 重新收口
3. **feature 目录已存在**——不在本阶段新建 feature 目录
4. **上下文读全**——读 approved design 全文 + `.codestable/attention.md` + 相关 shared conventions / architecture

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
