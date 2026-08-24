# CodeStable 术语与判据

本文档集中定义 CodeStable workflow 中的关键术语判据，作为所有 skill 路由判断的单一权威来源。

---

## 1. feature vs issue

**feature**：从来没有的东西要加进来——新功能 / 新能力。

**issue**：本来应该好的东西坏了——已有代码里的 bug / 异常行为 / 文档错误 / 性能问题。

**灰色地带**：
- feature 实现时发现的 bug → 记成新 issue，不在 feature PR 顺手修
- 修 issue 过程中发现需要新增能力才能真正解决 → 先用 issue 工作流把记录和分析做完，再视情况开 feature

---

## 2. learning vs trick vs decision vs explore

四者都是存档文档类型，区别在记录内容的性质：

- **learning**（回顾）：做 X 时踩了 Y，留个教训 → `cs-learn`
- **trick**（处方）：以后做 X 就这样做的可复用模式 → `cs-trick`
- **decision**（规约）：全项目今后都得遵守的技术决定 → `cs-decide`
- **explore**（证据）：调查了一个问题，留份证据存档 → `cs-explore`

**判别口诀**：
- 回顾"做 X 时踩了 Y" → `cs-learn`
- 处方"以后做 X 就这样做" → `cs-trick`
- 规定"全项目今后都按 X 来" → `cs-decide`
- 调查"X 现在是什么样" → `cs-explore`
- 一两行常驻提示"CodeStable 技能每次启动都得知道 X" → `cs-note`（写到 `.codestable/attention.md`）

四者共用 `.codestable/compound/` 目录，靠 frontmatter 的 `doc_type` 字段和文件名中间的类型段区分。

---

## 3. fastforward 边界合同

**shared fastforward contract**（跨 feature / refactor 共用）：
- fastforward 只在**低仪式成本路径**的前提持续成立时可用：范围小、决策空间小、AI 可一次对话内完成并自证
- fastforward 只加速执行，**不改变 authority ordering**：canonical artifacts 仍高于 generated state 与 bridge hints
- 一旦任一阈值被突破，或出现标准主线级别的决策复杂度，workflow **自动 normalizes** 到对应标准 lane
- auto-normalize 是**单向**的：触发后不再继续沿用 fastforward 语义硬推到底
- 不确定是否还算 fastforward 时，默认回标准 lane，不低估范围

### feature fastforward

**可继续留在 `cs-feat-ff` 的条件**：
- 需求小到不值得走完整 design / plan 阶段
- 范围清晰，无新的术语冲突或架构决策
- 改动量预估 < 50 行，且不跨 3+ 文件
- 不需要 `plan` 级的多步编排与阶段 gate

**自动 normalize 到标准 feature lane**（从 `cs-feat-design` 续上）的触发条件：
- 改动涉及多个子系统或新增架构边界判断
- 需要引入新术语、统一旧术语，或与现有命名冲突
- 需求追加后让范围明显扩张，或推进步骤已经需要 `plan` 才能稳定执行
- 局部快写已不足以表达 scope / risk / acceptance 契约

### refactor fastforward

**可继续留在 `cs-refactor-ff` 的条件**：
- 行为等价是确定前提
- 改动集中在单函数 / 单组件 / 单文件
- 优化点 ≤ 3 处，且都能对应到经典重构方法
- 有测试 / 类型检查 / 既有验证手段可自证
- 不需要 HUMAN 目视验证，不碰公开接口

**自动 normalize 到标准 refactor lane**（回 `cs-refactor` 从 scan 续上）的触发条件：
- 改动跨 > 1 文件或优化点持续膨胀
- 需要 Parallel Change / Strangler Fig / 分层纠偏等标准 refactor 方法库能力
- 没有测试能覆盖，或需要 HUMAN 目视 / 跨模块确认
- 出现行为变更风险、公开接口变化、或已不再是"小重构"

---

## 4. issue 标准路径 vs 快速通道

**快速通道**（同时满足）：
1. AI 读完代码后对根因高度有把握（能明确指出 file:line + 原因）
2. 修复改动很小（1-2 处）
3. 无跨模块影响风险

**标准路径**（任一触发）：
- 根因有多个候选
- 不确定影响面
- 需要先复现才能定位
- 用户希望留完整分析存档

**判定**：是否进快速通道由 `cs-issue-report` 的启动检查做唯一正式判定。一旦进标准路径默认不再二次改判。

---

## 5. brainstorm vs intent

**brainstorm**（思考模式）：
- 想法还模糊，边界未定
- AI 是思考伙伴，帮用户澄清需求
- 输出：结构化的诉求说明，不直接落代码
- 下一步：澄清后走 feature / issue / roadmap

**intent**（执行模式）：
- 用户已知道做什么，直接表达诉求
- AI 是执行者，按用户指令分诊到对应 workflow
- 输出：直接进入 feature / issue / refactor / audit 流程

**判定**：用户说"我有个想法还没想清楚" / "先 brainstorm 一下" → `cs-brainstorm`；用户直接说"加个 X 功能" / "修个 Y bug" → 直接路由。

---

## 维护说明

- 本文件是所有 skill 路由判据的权威来源
- 修改判据时只需改本文件，再同步到相关 skill 的短摘要
- 新增 workflow 或术语时补充对应小节
