---
name: cs-feat-accept
description: feature 流程阶段 4——验收闭环：对照 design / plan 核实现 + 回写 architecture / requirement / roadmap，最后产出 {slug}-acceptance.md。触发：用户说"功能写完了验收一下"、"做最后检查"、"准备 merge"、"出验收报告"。前置依赖 cs-feat-impl 完成。
---

# cs-feat-accept

## 启动必读

本技能启动前需读取：
- `.codestable/attention.md` — 项目注意事项
- `.codestable/reference/shared-conventions-core.md` — 目录结构与命名规则
- `.codestable/reference/shared-conventions-feature.md` — feature 产物职责边界
- `.codestable/reference/shared-conventions-roadmap.md` — roadmap ↔ feature 衔接
- `.codestable/reference/shared-conventions.md` — 收尾推荐与提交规则

**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。

代码已经写完，但流程没结束。本阶段只适用于标准 `design + plan + checklist` feature，做四件事，缺一不可：

1. **核对实现有没有偏离方案**——逐层对照 `{slug}-design.md` 与 `{slug}-plan.md`；发现偏差当场修，**不是在报告里"记一下"**就过去
2. **把 feature 归并到整体架构**——对照方案第 4 节，实际去更新架构中心目录下的相关 doc
3. **能力落档到 requirement**——draft req 对应的能力实现完成后升级为 current（保留愿景，追加变更日志）；从未写过 req 的能力 backfill
4. **完成状态回写到 roadmap**——方案 frontmatter 有 `roadmap` / `roadmap_item` 字段时**必须**改 items.yaml 对应条目为 `done` 并同步主文档

漏掉任何一件的代价：架构 doc 过期下个 feature 读到错信息；req 和实际能力脱节；roadmap 规划层和实际进度脱节，下次推进会重复跑流程。

**没产出报告 = 工作流未完成**。后人查"上次这个功能验收时确认了哪些行为"，没报告就只能翻 git diff 重新推断。

> 共享路径与命名约定看 `.codestable/reference/shared-conventions-core.md`。

---

## 跟 design 的章节强依赖

本技能整套对照表按 design 当前章节编号硬编码。**design 升级章节名 / 编号时本技能必须同步**，否则下面所有"第 X 节"指针都指错地方。

**标准 design 章节快照**：

- 第 0 节：术语约定
- 第 1 节：决策与约束（需求摘要 / 复杂度档位 / 关键决策 / 前置依赖）
- 第 2 节：名词与编排（2.1 名词层 / 2.2 编排层 / 2.3 挂载点 / 2.4 推进策略）
- 第 3 节：验收契约（关键场景清单 + 反向核对项）
- 第 4 节：与项目级架构文档的关系

**Fastforward**：`cs-feat-ff` 不产出 design / plan / checklist / acceptance，写完并经用户确认后由该技能自身回写 `ff-note.md` 闭环；不得把它当成标准验收流程的输入。

---

## 启动检查

1. **代码确实实现到位**——git status / 最近提交看到本功能改动，否则退回 implement
2. **方案 doc 完整**——frontmatter `doc_type=feature-design` / `feature` 一致 / `status=approved` / `summary` 非空 / `tags` ≥ 2；标准 design 第 0/1/2/3 节 + 第 4 节已填写
3. **`{slug}-checklist.yaml`**——存在且 `feature` 一致；`steps` 全 `done`（有 `pending` 退回 implement）；`checks` 非空全 `pending`
4. **plan 已批准且上下文读全**——标准 feature 的 `{slug}-plan.md` 必须存在且 `status=approved`；缺失或仍为 draft 就退回 `cs-feat-plan` 完成 execution-order checkpoint。随后读方案 doc 全文（重点：第 1 节明确不做、2.1 接口示例、2.2 流程级约束、2.3 挂载点、第 3 节场景）+ checklist + plan 全文 + 第 4 节提到的所有架构 doc + 本次代码改动（git log / diff）；若有 roadmap 起头，验收前还必须核对 `design.feature = items.yaml.feature` 与 `plan.feature = design.feature`
5. **断点恢复**——`{slug}-acceptance.md` 已存在且部分填好 → 从下一个未完成节继续，跳过 checks 中已 `passed` 的项；汇报"上次做到第 X 节，从第 Y 节继续"
6. **短回复 continuation-first**——如果用户这轮输入只是 `继续 / 确认 / 同意 / 跳过 / 继续下一步`，先按已有 acceptance / checklist / plan 状态恢复；必要时再参考 `.ccg/tasks/*/task.json` 作为恢复桥，但不把 task 文件当成验收真相源

---

## 验收报告模板与核对指南

逐节填写**别跳节**。完整报告模板和 9 个核对节的填写要求见 `acceptance-checklist-guide.md`。

执行时必须按该指南逐节核对；发现偏差先修代码或回填方案 doc，不允许只在报告里记录“已知偏差”。

---

## 核对节奏

逐节做。每节完成后**逐条更新 `{slug}-checklist.yaml` 的 `checks`**：通过 → `passed`，失败 → `failed`（先修代码 / 方案再改回 `passed`）。所有 checks 全 `passed` 后报告才算完成。

第 1/2 节最容易暴露偏离，先做。第 2 节挂载点反向核对**必须实际 grep + 沙盘推演**，不能凭印象勾选。第 5/6/7 节是写文件的动作，不是自评。

---

## 退出条件

- [ ] 验收报告 9 节都填完
- [ ] 第 1/2 节核对全部勾选，无未处理偏差（含挂载点 grep + 拔除沙盘推演）
- [ ] **第 2.5 节复用策略审查全部勾选**，过度新增已识别（如有）
- [ ] 第 3 节场景核对全部勾选，前端已浏览器验证
- [ ] 第 4 节术语一致性无遗漏
- [ ] 第 5 节归并：每条有明确结论，需要更新的 doc 已实际写入
- [ ] 第 6 节 req 回写有结论：跳过 / 未变 / 已 backfill / draft→current / 已 update
- [ ] 第 7 节 roadmap 回写有结论：跳过（非 roadmap 起头）/ 已更新（items.yaml + 主文档同步，yaml 通过校验）
- [ ] checklist 所有 checks 都 `passed`
- [ ] 用户终审确认

---

## 退出后

告诉用户："验收报告已就绪，架构文档已归并，cs-feat 工作流走完。后续 BUG 走 issue 流程。"

按 `.codestable/reference/shared-conventions.md` 第 3 节（阶段收尾推荐）（阶段收尾推荐）收尾推荐顺序逐项一句话提示（用户说"不用"立刻跳过）：

1. 复用价值的坑点 / 经验 → "需要沉淀 learning 吗？（`cs-learn`）"
2. 长期约束 / 技术选型 → "需要归档决定吗？（`cs-decide`）"
   - **特检**：design 第 2.5 节是否有"建议沉淀的 convention"段。有就把那条规则原文念给用户："design 2.5 建议沉淀这条 convention：『{规则一句话}』，跑通了，要不要现在 `cs-decide` 归档？"——这种是 design 阶段就识别出的稳定模式，比一般"问问看"更应该主动提
3. 接口变更 / 用户可见行为变更 → "需要更新指南吗？（`cs-guide`）"
4. 库公开接口（组件 / 函数 / 命令）变了 → "需要更新 API 参考吗？（`cs-libdoc`）"
5. 第 8 节有 attention.md 候选 → 逐条问"候选 X 加到 attention.md 吗？" 用户明确同意 → 触发 `cs-note` 走分节归类 / 查重 / 软上限检查（不在 accept 里手写，避免和 cs-note 各搞一套口径）；**一次一条**
6. 最后问是否代为 scoped-commit

收尾提交规则看 `.codestable/reference/shared-conventions.md` 第 4 节（收尾提交）（收尾提交）。提交范围：功能代码 + 方案 doc + 验收报告 + 本次实际更新的架构 doc / req doc / roadmap items.yaml + 主文档。

---

## 容易踩的坑

- "测试都过了" → 测试通过 ≠ 验收场景满足，要逐条核对第 3 节
- "我肉眼看了一下" → 按清单走，逐项勾选
- 接口偏差在报告里写"已知偏差"而不修代码 / 回填方案
- 挂载点反向核对只看清单不 grep——漏记的挂载点溜进项目，后面拔不干净
- 第 3 节前端改动只 typecheck 没浏览器跑过
- 第 5 节归并写"整体不影响架构"一句话带过，没逐条核查
- 架构 doc 需要更新而只写"建议以后更新"——归并是当下动作不是建议
- 第 7 节只改 items.yaml 没同步主文档，两份不一致
- frontmatter 有 `roadmap` 却在第 7 节写"跳过"——有值就必须回写
- 报告写完没让用户终审就宣告完成
- 用户没明确同意就 `git commit`
