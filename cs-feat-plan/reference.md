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
- **关键判断点**：{这一步里唯一容易分叉的地方一句话说清楚——不写代码，只写"遇到 X 情况怎么选"}
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
evidence_contract: v1

steps:
  - id: step-1
    action: "{paradigm 维度的切片}：{动作描述}"
    exit_signal: "{退出信号，可独立验证}"
    verification:
      method: command | typecheck | test | grep | manual
      expected: "{期望观察结果}"
    evidence:
      result: pending
      verified_at: null
      verified_by: null
    status: pending

checks:
  - id: check-1
    item: "{检查项描述}"
    source: 名词契约 | 编排骨架 | 流程级约束 | 挂载点 | 范围守护 | 验收场景
    verification:
      method: command | typecheck | test | grep | manual
      expected: "{期望观察结果}"
    evidence:
      result: pending
      verified_at: null
      verified_by: null
    status: pending
```

`evidence_contract: v1` 是新生成 checklist 的硬要求。条目变为
`done` / `passed` 前，必须把 `evidence.result` 写成具体命令或观察结果，
`verified_at` 写 `YYYY-MM-DD`，`verified_by` 写 `ai | user | ci`。
详细规则见 `.codestable/reference/evidence-contract.md`。

## 4. 派生规则

- `plan.md` 只承接 approved design，不重复需求摘要与术语表
- `checklist.yaml` 从 design + plan 共同派生
- `steps` 粒度是 paradigm 维度，不写 file:line / 函数级
- `checks` 不允许编造 design 里不存在的条目
- `id` 必须在当前 checklist 内稳定且唯一，后续回写不得因排序改变含义
