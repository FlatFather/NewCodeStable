# Workflow Contract — Continuation Semantics

## 核心原则

- continuation-first 只适用于明显短回复或恢复信号。
- 只有存在唯一且可验证的续作候选时才允许自动继续。
- continuation 的判断结果永远不能覆盖 canonical artifacts。
- 自动切换语义是 router 的消费规则，不是新的 authority 来源。

## Continuation Signals

默认信号包括：

- `继续`
- `确认`
- `同意`
- `按这个修`
- `跳过`
- `继续下一步`
- `resume`
- `go on`

这些信号只表示“可能在继续”，不自动代表“可以无询问切换到下一技能”。

## 恢复顺序

1. 判断输入是否属于 continuation signal。
2. 优先检查 canonical artifacts 能否定位唯一活跃对象。
3. 再检查 generated state 是否 fresh，且 consistency 不为 conflict。
4. 必要时才读取 bridge hints 辅助恢复。
5. 若唯一候选成立，且自动继续前提成立，则恢复到对应 lane / 阶段。
6. 若任一前提不成立，则停止自动继续并要求用户选择、确认或补充信息。

## 何时允许自动继续

automatic continuation 只在以下条件同时成立时允许：

- 输入命中 continuation signal，或明显是在延续上一轮已确认流程。
- canonical artifacts 能定位到恰好一个 eligible candidate。
- 该候选没有要求用户先做设计批准、方案选择、范围确认等人工决策。
- generated state 给出的 derived 结论与 canonical artifacts 一致。
- `workflow-contract-generated-state.md` 中定义的全局 auto-switch predicate 成立。

## 何时必须询问用户

以下任一情况，router 都必须询问用户，而不是自动切换：

- 同时存在多个合理候选
- 用户补充了新的范围、目标、限制或例外
- canonical artifacts 与 generated state 或 bridge hints 冲突
- 现有文档不足以判断下一步
- 当前候选处于 terminal state
- 当前候选需要设计批准、修复方案选择或其他显式人工确认
- derived state 标记 `needs_user_decision = true`
- `blockers` 中存在 safety-critical blocker，或导致下一步不再唯一的 blocker

## Continuation Modes

router 消费 `continuation_mode` 时只可按以下语义理解：

- `auto`：允许在不新增用户选择的前提下继续既有流程
- `ask_user`：存在用户决策缺口，必须先询问
- `terminal`：当前记录可作为完成或停止点，不应再自动前推

如遇无法稳定归类的情况，必须按 `ask_user` 处理。

## 告知义务

命中 continuation 后，响应中至少说明：

1. 识别到这是继续已有流程
2. 识别到的对象是什么
3. 将从哪个阶段或步骤继续，或为什么必须先询问用户

## 与 lane 文档的关系

- 本模块定义 continuation 的规范性语义。
- `workflow-continuation.md` 只保留 lane-facing 摘要与阅读指针。
- 各技能若要解释 continuation，必须链接回本模块，而不是重复定义规则。
