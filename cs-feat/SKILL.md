---
name: cs-feat
description: 新功能开发的子流程入口，把"加个 X 能力"从想法走到验收闭环。触发：用户说"做新功能"、"加个 X"、"实现 XX"。只做路由，根据已有产物决定走 brainstorm / design / plan / fastforward / implement / acceptance。不处理 bug。
---

# cs-feat

## 启动必读

本技能启动前需读取：
- `.codestable/attention.md` — 项目注意事项
- `.codestable/reference/shared-conventions-feature.md` — feature 产物职责边界

**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。

新功能流程在"需求"和"代码"之间塞了一份方案文件，让两边有交接点——AI 直接拿到需求就写代码会出三个老问题：名字跟原代码对不上、改着改着改出范围、改完不留存档。

```
(想法模糊先去 cs-brainstorm 分诊) → 方案设计（名词层 + 编排层 + 验收契约 + 推进策略切片）→ 执行计划（plan + checklist）→ 分步实现 → 验收闭环
```

brainstorm 是讨论层独立入口，会分诊：case 1（清楚 → 直接 design）/ case 2（小需求继续讨论 → 落 brainstorm note）/ case 3（大需求 → 移交 `cs-roadmap`）。只有 case 2 在 feature 目录产出 brainstorm note。

本技能不写代码不写文档，只做一件事：看当前 feature 走到哪步，告诉用户该触发哪个子技能。

---

## 文件放哪儿

```
.codestable/features/{feature}/
├── {slug}-brainstorm.md       ← 阶段 0 产物（仅 case 2 落盘）
├── {slug}-intent.md           ← 可选前置草稿（用户自己写半成品，供 design 读取）
├── {slug}-design.md           ← 阶段 1 方案文件（范围与约束唯一方案源）
├── {slug}-plan.md             ← 阶段 2 执行计划正文（标准 feature 必备）
├── {slug}-checklist.yaml      ← 阶段 2 生成 steps + checks，3/4 阶段更新 status
└── {slug}-acceptance.md       ← 阶段 4 验收报告
```

目录命名 `YYYY-MM-DD-{英文 slug}`，日期取首次创建当天定了不动；slug 小写字母 / 数字 / 连字符。

为什么聚一起：以后查"那个导出 CSV 功能当时怎么决定的"，brainstorm / design / acceptance 都在一处。feature 和 issue 分别放在 `.codestable/features/` 和 `.codestable/issues/` 因为归档逻辑不一样。

实现 feature 时顺手发现的 bug → 记成新 issue，**不在 feature PR 里偷偷修**——验收时分不清范围，git blame 找不到为什么改。

---

## 五个阶段

| 阶段 | 子技能 | 产出 | 谁主导 |
|---|---|---|---|
| 0 brainstorm（可选，独立入口） | `cs-brainstorm` | case 2 时产出 brainstorm note | AI 思考伙伴，用户拍板 |
| 1 方案设计 | `cs-feat-design` | design.md（初始化模式可先建 intent.md） | AI 起草，用户整体 review |
| 2 执行计划 | `cs-feat-plan` | plan.md + checklist.yaml | AI 起草，用户整体 review |
| 3 分步实现 | `cs-feat-impl` | 代码 + 阶段汇报 | AI 按方案执行 |
| 4 验收闭环 | `cs-feat-accept` | acceptance.md | AI 逐层核对，用户终审 |

阶段间有人工 checkpoint。上一阶段没拿到用户明确放行，下一阶段别开始——防止 AI 一口气从需求跑到代码、跑出来才发现走偏。

阶段 0 可选且是 feature 流程的**外部入口**——`cs-brainstorm` 同时服务 feature 和 roadmap。case 3（大需求）讨论被移交给 `cs-roadmap` 不再回 feature 流程；roadmap 拆出子 feature 后从 `cs-feat-design` 的"从 roadmap 条目起头"入口进来。

### Fastforward 模式

需求清楚 + 范围小时走完整五阶段太啰嗦。fastforward 把 design 压成 4 节（需求摘要 / 设计方案 / 验收标准 / 推进步骤），用户一次确认后直接实现。触发："快速模式"、"fastforward"、"直接开干"、"别那么多步骤"，去 `cs-feat-ff`。

**别走** fastforward：跨多个子系统、有术语冲突风险、推进步骤超过 4 步——这些情况跳过 design 意味着 AI 和用户没共同确认过同一份方案，实现完容易发现彼此理解不一样。

---

## 路由：用户现在该走哪个子技能

进入本技能先 Glob 一下 `.codestable/features/` 看已有产物。**不要只听用户口头描述**——用户说"设计写完了"不一定真完整，自己读一遍。

| 当前状态 | 触发哪个子技能 |
|---|---|
| 用户只回 `继续 / 确认 / 同意 / 跳过 / 继续下一步` 这类短回复，且存在唯一候选 feature 目录 | **先按 continuation-first 续作**：直接根据该目录现有产物判断 design / plan / impl / accept，不重复给新的路由结论 |
| 想法模糊，说不清真问题 / 边界 / 不做什么 | `cs-brainstorm` |
| 想法清晰（知道做什么 / 为谁 / 怎么算成功） | `cs-feat-design` |
| 用户说"开一个新需求 / 起草稿 / 新建 feature"想自己写半成品 | `cs-feat-design` 的"初始化模式"（建目录并起一份 intent 草稿，让用户填完再回） |
| 用户主动说"先 brainstorm 一下"、"有个想法没想清楚" | `cs-brainstorm` |
| `{slug}-intent.md` 已填好 | `cs-feat-design`（读 intent 作输入） |
| 用户说"快速模式 / fastforward" | `cs-feat-ff` |
| `{slug}-brainstorm.md` 已存在，要进设计 | `cs-feat-design` |
| `{slug}-design.md` 已 approved，`plan.md` / checklist 还没落齐 | `cs-feat-plan` |
| `{slug}-plan.md` + `{slug}-checklist.yaml` 已齐、代码没动 | `cs-feat-impl` |
| fastforward design 已确认 | `cs-feat-impl` |
| 代码已写完要验收 | `cs-feat-accept` |
| 用户说"我想要一个 X 系统"大需求 | 转 `cs-brainstorm` 分诊（大概率 case 3 → `cs-roadmap`） |
| roadmap 里某条子 feature 该启动 | `cs-feat-design` 的"从 roadmap 条目起头"入口 |
| 不确定 design 是否完整 | 自己读一遍，按上面对号 |

### continuation-first 约束

当用户输入是 `继续 / 确认 / 同意 / 跳过 / 继续下一步` 这类短回复时，本技能先做 continuation-first：

1. 先看是否存在**唯一候选 feature 目录**
2. 命中 → 直接按该目录现有产物判断当前阶段（design / plan / impl / accept）
3. 多个候选 → 列给用户选，不猜
4. 没有候选 → 才按普通 feature 路由处理

如果需要恢复桥接信息，可参考 `.ccg/tasks/*/task.json`，但它**只作 task 状态桥**，不能替代 feature 目录里的 design / plan / checklist / acceptance 真相源。详细协议见 `.codestable/reference/workflow-continuation.md`。

### 怎么判断该不该走阶段 0

判断信号不是"用户描述字数少"，是用户能不能清楚说出三件事：要解决的真问题 / 核心行为 / 一条明确的"不做什么"。三项有一项模糊就值得 brainstorm。

但别强推——用户明确说"想清楚了直接做设计"就尊重。不确定时问一句让用户选。**宁可漏判，别误判**——逼一个想清楚的用户做发散是浪费。

### brainstorm vs intent

两者都是 design 前置，区别在**谁在主导收敛**：

- brainstorm：用户脑子里模糊，AI 通过 `cs-brainstorm` 对话收敛；判 case 3 时移交 `cs-roadmap`，只有 case 2 落 brainstorm note
- intent：用户自己已经想好大致做法，想先写一份 `{slug}-intent.md` 前置草稿；路由到 `cs-feat-design` 的初始化模式

这里的职责只到**路由判断**为止：`intent.md` 作为 feature 可选前置草稿的共享身份看 `.codestable/reference/shared-conventions-feature.md`，草稿骨架和初始化步骤看 `cs-feat-design`。

用户模糊触发"开一个新需求"时默认问"你想先聊清楚（brainstorm）还是自己写草稿（intent）？"，别自己挑。

---

## 与 issue 工作流的边界

- feature：从来没有的东西要加进来（新功能 / 新能力）
- issue：本来应该好的东西坏了（bug / 异常 / 文档错误 / 性能问题）

完整判据见 `.codestable/reference/terminology.md` 第 1 节。

灰色地带：feature 实现时发现的 bug 记成新 issue，不在 feature PR 顺手修。

---

## 相关文档

- `.codestable/reference/system-overview.md` — CodeStable 体系总览
- `.codestable/reference/shared-conventions.md` — 跨阶段共享口径、目录结构、checklist 生命周期
- `.codestable/attention.md` — CodeStable 启动注意事项和项目硬约束
- 项目架构总入口 — 方案设计阶段需要查
