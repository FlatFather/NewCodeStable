# Skill Quality Contract

## 目标

CodeStable 技能的质量不只看“能完成任务”，还看启动成本、路由准确性、证据密度、交互摩擦与退出可靠性。本文件定义所有 `cs-*` 技能共用的设计合同。lane 特有规则仍归各自技能与 lane 共享文档。

## 启动成本

技能必须把启动材料分为两类：

- **Hard-required**：每次执行本技能都必须读取的材料
- **On-demand**：只在输入、阶段或 artifact 命中相关信号时读取的材料

默认 hard-required 只允许：

- `.codestable/attention.md`
- 当前 lane / artifact 的 canonical 状态源
- 当前阶段的模板或写作指南

以下材料默认是 on-demand，不得写成无条件必读：

- architecture
- requirements
- roadmap
- compound
- guides / libdoc
- 不直接决定当前阶段的共享契约模块

技能可以声明例外，但必须在 `SKILL.md` 写明触发条件与不可省略原因。

路由类技能还必须先执行低成本 probe：确认 `.codestable/` 是否存在、读取 fresh
generated state 或指定 lane 的最小索引，然后才按需读取 attention、共享约定或具体
artifact。短回复优先走 continuation predicate；predicate 已给出唯一结论时，不得
为了“确认一下”再全量扫描其他 lane 或重读体系总览。

## 路由与决策

根路由和 lane 路由应输出可核查的决定要素：

- 当前 lane / stage
- 触发理由
- 下一步 skill
- confidence
- blockers

continuation-first、authority ordering、checkpoint 单次消费规则以 workflow contract 为准；技能只能摘要引用，不得另立规范。

## 证据要求

会产生质量结论或完成结论的技能必须保留证据：

- 代码结论：`file:line`
- 命令结论：command + result + exit code
- 验证结论：验证对象、时间、结果、剩余风险
- 用户结论：明确确认内容与时间
- 方案结论：选项、取舍、推荐理由

证据必须写入对应 canonical artifact，不能只留在对话里。历史兼容 artifact 可不回填；新 artifact 必须满足本合同。

## 交互摩擦

checkpoint 只保留在会改变范围、方案、行为、安全或存在多候选的位置。确定性 handoff 不得在用户已明确批准后追加“是否继续”类问题。

一次性收集结构化输入时，优先给默认表单并只追问缺失项；避免把固定字段逐条问成多轮问卷。

## 知识与文档生命周期

`cs-note`、`cs-learn`、`cs-guide`、`cs-libdoc` 一类内容型技能，写入前必须先判定
最小动作：**更新已有**、**新建**、**交叉链接**或**转交到更合适的技能**。先查目标
目录的索引、用户点名的旧文档和最可能重复项；不能因为“保险起见”把整个 compound / docs
目录全文读一遍。

- 一个 note 只承载一个稳定、每次都需要的事实；一个 learning 只承载一个可复用经验。
- guide 按一个读者任务组织，libdoc 按一个公开 entry 组织；重复的接口表、设计细节和日志只链接 canonical source，不复制。
- 批量文档先完成有代表性的样板并获得确认，再扩大；无法验证的内容标记为 skipped / outdated，而不是猜测补全。
- 每个新建或更新的文档保留来源、适用边界和复查触发点；记录结论，不粘贴原始长日志或完整对话。

## 退出质量

每个技能的退出条件必须覆盖：

- canonical artifact 已生成或更新
- 状态字段正确
- 必需证据已落盘
- 范围外事项已显式处理
- 下一步唯一时已直接 handoff；不唯一时已列出选项

## 评分口径

`score-workflow.py` 从两个层面评估：

1. **skill score**：检查各 `SKILL.md` 是否包含启动成本分层、证据要求与退出质量。工具默认阈值为 80，便于下游逐步接入；本仓库的 `scripts/verify.sh` 以 100 作为 CI 硬门。
2. **lane score**：检查 active artifacts 的结构、状态与证据密度。默认为 advisory，用于推动新产物质量；后续可通过 `--strict-artifacts` 升级为硬门。

历史 compatibility / legacy / sample artifacts 不参与 lane 硬门。
