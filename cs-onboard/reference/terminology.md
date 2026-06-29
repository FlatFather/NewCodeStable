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

## 3. fastforward vs 标准 feature

**fastforward**（快速通道）：
- 需求小到"不值得走完整 design / plan 阶段"
- 范围清晰，无决策空间
- 改动量预估 < 50 行
- AI 可以一次对话内完成 + 自证（有测试或可快速验证）

**标准 feature**（标准主线）：
- 需求涉及多个模块或接口设计
- 存在方案选择空间，需要文档化决策依据
- 改动量 ≥ 50 行或跨 3+ 文件
- 需要分阶段推进：design → plan → implement → acceptance

**判定**：不确定时默认走标准主线，不要低估范围。

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
