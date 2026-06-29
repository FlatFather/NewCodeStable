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

**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。

`cs-feat-design` 负责把"做什么 / 为什么做 / 范围到哪"为人类拍板清楚；`cs-feat-plan` 接手后只做一件事：基于已批准 design 生成 `plan.md` (step source) 与 `checklist.yaml` (status carrier)。其中 checklist 的 `steps` 从 plan 的推进顺序派生，`checks` 从 design 各节约束派生。用户在进入实现前有一个单独的执行计划确认关口。

> 共享路径与命名约定看 `.codestable/reference/shared-conventions-core.md`。`plan.md` 是 step source，`checklist.yaml` 是 status carrier；详细生命周期看 `.codestable/reference/shared-conventions-feature.md` 和 `.codestable/reference/shared-conventions-checklist.md`；本阶段不改 scope。

---

## 启动检查

1. **design 已批准**——`{slug}-design.md` 必须存在且 `status=approved`
2. **尚未进入实现**——若代码已开始改动，先和用户确认是回补 plan，还是回 design 重新收口
3. **feature 目录已存在**——不在本阶段新建 feature 目录
4. **上下文读全**——读 approved design 全文 + `.codestable/attention.md` + 相关 shared conventions / architecture + `.codestable/reference/workflow-continuation.md`（如本次是短回复续作或涉及 task 状态桥）
5. **复用策略验证**（新增）：
   - 读取 design 第 1.5 节的复用策略
   - 如果策略是"扩展为主"，plan 的第一步必须是"读取现有函数 X 的实现"
   - 如果策略是"新增为主"，验证 design 第 1.5 节是否对每个"可扩展"项都有充分理由
   - 如果 design 缺少第 1.5 节（历史 design），提示"建议回 design 补充复用策略"

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

plan/checklist 落盘后，要明确进入实现前的独立关口：确认对象是**执行顺序与步骤切分**，不是再次确认已经 approved 的 design 意图。若 canonical artifacts 已唯一表明"plan/checklist 已确认可执行"，则后续由 `cs-feat-impl` 直接接手，不再重复补一轮"要不要现在开始实现"。

### 4. 扩展场景的特殊处理（复用优先）

当 design 第 1.5 节策略是"扩展为主"时，plan 的推进顺序必须体现扩展逻辑：

**扩展场景的 plan 模板**：
```markdown
## 2. 分步计划

### Step 1 — 读取并理解现有实现
- **目标**：深入理解要扩展的现有函数/模块
- **触碰范围**：{design 1.5 节列出的扩展点所在文件}
- **退出信号**：能准确描述现有逻辑流程、参数、返回值、调用方
- **验证**：阅读代码 + 跑现有测试

### Step 2 — 设计扩展方案细节
- **目标**：根据现有实现，细化扩展方式（参数/返回值/分支）
- **触碰范围**：确定扩展点的具体位置
- **退出信号**：扩展方案不破坏现有逻辑、有兼容性保证
- **验证**：设计 review（可选参数默认值、分支条件）

### Step 3 — 实施扩展
- **目标**：在现有函数/模块上实施扩展
- **触碰范围**：{具体文件}
- **退出信号**：新增逻辑正常工作、现有测试仍然通过
- **验证**：跑全量测试

### Step 4 — 补充测试覆盖新逻辑
- **目标**：为新增的扩展逻辑补充测试
- **触碰范围**：测试文件
- **退出信号**：新逻辑有测试覆盖
- **验证**：测试通过
```

**新增场景的 plan 模板**（design 1.5 节是"新增为主"）：
```markdown
## 2. 分步计划

### Step 1 — 确认无法复用（复查）
- **目标**：再次确认 design 1.5 节的"不扩展"理由仍然成立
- **触碰范围**：复用清单中列出的候选函数
- **退出信号**：确认每个候选函数确实不可扩展
- **验证**：快速阅读相关代码

### Step 2 — 新建模块/函数
- **目标**：按 design 创建新的实现
- ...
```

**判断规则**：
- design 第 1.5 节策略 = "扩展为主" → 使用扩展场景模板
- design 第 1.5 节策略 = "新增为主" → 使用新增场景模板（含复查步骤）
- design 缺少第 1.5 节 → 按传统流程，但在 plan 开头提示"建议回 design 补充复用策略"

---

## 流程

### 1. 生成 `{slug}-plan.md`

按 `cs-feat-design/reference-templates.md` 里的 plan 模板生成：
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

汇报后停在实现前关口：如果当前只完成了 plan/checklist 生成，就等待用户对执行顺序本身的反馈；如果随后收到 `继续 / 确认 / 同意 / 继续下一步` 且唯一候选已由 canonical artifacts 表明可以进入实现，则自动切到 `cs-feat-impl`，不再重复确认已批准的 design 意图。

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
