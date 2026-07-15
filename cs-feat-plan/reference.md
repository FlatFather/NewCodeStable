# feature-plan 阶段参考模板

本文件提供 `cs-feat-plan` 使用的 `{slug}-plan.md` 与 `{slug}-checklist.yaml` 参考格式。

## 1. `{slug}-plan.md` frontmatter

```markdown
---
doc_type: feature-plan
feature: 2026-04-12-user-auth
design: user-auth-design.md
status: draft
---
```

生成初稿时使用 `status: draft`；用户确认执行顺序与步骤切分后，`cs-feat-plan` 必须将其改为 `status: approved`，这是进入 `cs-feat-impl` 的 canonical 前提。

## 2. `{slug}-plan.md` 正文结构

```markdown
# {slug} execution plan

## 1. 执行目标

一句话说明：这份 plan 只承接已批准 design，回答“按什么顺序做、每步怎么判断完成”。

## 2. 分步计划

### Step 1 — {步骤标题}
- **目标**：{这一步要达成什么}
- **触碰范围**：{文件 / 模块 / 文档路径，允许是高层级}
- **退出信号**：{什么现象代表这一步完成}
- **验证**：{grep / 命令 / 手工检查 / 类型系统 / 测试}

### Step 2 — ...

## 3. 风险与回退

- 风险 R1：{可能踩坑}
- 回退 / 止损：{如果这一步走偏，怎么停下来}

## 4. 与 checklist 的映射

- Step 1 → checklist.steps[0]
- Step 2 → checklist.steps[1]
```

## 3. `{slug}-checklist.yaml` 格式

```yaml
feature: {feature 目录名}
created: YYYY-MM-DD

steps:
  - action: "{paradigm 维度的切片}：{动作描述}"
    exit_signal: "{退出信号，可独立验证}"
    status: pending

checks:
  - item: "{检查项描述}"
    source: 名词契约 | 编排骨架 | 流程级约束 | 挂载点 | 范围守护 | 验收场景
    status: pending
```

## 4. 派生规则

- `plan.md` 只承接 approved design，不重复需求摘要与术语表
- `checklist.yaml` 从 design + plan 共同派生
- `steps` 粒度是 paradigm 维度，不写 file:line / 函数级
- `checks` 不允许编造 design 里不存在的条目
