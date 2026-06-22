# feature-plan 与 checklist 模板

## 3. {slug}-plan.md 格式

```markdown
---
doc_type: feature-plan
feature: {feature 目录名}
design: {slug}-design.md
status: draft
---

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

写作约束：
- plan 只展开已批准 design 的推进顺序，不重复术语表、需求摘要、明确不做。
- plan step 与 checklist step 一一对应，但 plan 写说明、checklist 写状态。
- `status`：`draft` / `approved` / `superseded`。

---

## 4. {slug}-checklist.yaml 格式

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

`steps`（`cs-feat-plan` 阶段产出）：

- 标准 feature：从 design 的推进策略切片 + plan 的分步计划共同抽取；plan 提供 step narrative，checklist 只保留 action / exit_signal / status
- 粒度是 paradigm 维度，**不写 file:line / 函数级**——具体落点是 implement 的事
- 切片顺序"最简 Workflow 先行 → 逐个节点填充"：
  - 后端：编排骨架（空实现跑通）→ 计算节点逐个填 → 接通加载/持久化 → 测试覆盖
  - 前端：静态结构 → 交互逻辑 → 状态接入 → 联调 / 样式收尾
- 4-8 步；每步必须有可独立验证的退出信号
- 第 2.5 节结论是"微重构"时，**第 1 步固定是"按第 2.5 节方案做微重构（只搬不改行为）"**，独立退出信号（如"全部测试通过 + 编译绿灯 + 行为相关 diff 为零"），跑通后再进 feature 主体步骤

`checks`（`cs-feat-plan` 阶段产出，提取来源）：

- 名词契约 ← 第 2.1 节关键接口签名
- 编排骨架 / 流程级约束 ← 第 2.2 节主流程关键步骤、流程级约束
- 挂载点 ← 第 2.3 节每个挂入点（acceptance 反向核对可卸载性）
- 范围守护 ← 第 1 节"明确不做"每条
- 验收场景 ← 第 3 节"关键场景清单"每条

不允许编造 design 里不存在的条目。
