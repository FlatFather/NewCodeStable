# CodeStable 维护者说明

本文件由 `cs-onboard` 复制到项目的 `.codestable/reference/maintainer-notes.md`。维护 CodeStable 技能家族时需要反复查阅、但不适合放在各子技能正文里的说明。

## 0. Reference 阅读地图

第一次维护时先读 `system-overview.md` 了解实体和流程，再读 `workflow-contract.md` 确认规范入口；执行具体任务时只进入命中的分支，不把下图当作全量必读清单。

```text
reference/
├── system-overview.md                 体系速览与技能索引
├── workflow-contract.md               规范性入口（冲突时优先）
│   ├── workflow-contract-shared-concepts.md  共用概念
│   ├── workflow-contract-authority.md       真相源与冲突优先级
│   ├── workflow-contract-continuation.md    自动续作的允许与阻断条件
│   ├── workflow-contract-generated-state.md 派生状态与 freshness
│   └── workflow-contract-distribution.md    模板源与运行时副本
├── workflow-continuation.md           续作操作导航，不另立规范
│   ├── workflow-continuation-base.md        通用操作参考
│   ├── workflow-continuation-feature.md     feature 阶段 handoff
│   └── workflow-continuation-issue.md       issue 阶段与快速通道恢复
├── shared-conventions.md              共享规则导航及元数据、检索、编码、收尾
│   ├── shared-conventions-core.md          路径与命名
│   ├── shared-conventions-feature.md       feature 产物职责
│   ├── shared-conventions-checklist.md     checklist 生命周期
│   └── shared-conventions-roadmap.md       roadmap ↔ feature
├── terminology.md                    lane 区分与快路径判据
├── skill-quality-contract.md          启动成本、证据与退出质量
├── evidence-contract.md               新产物的机器可验证证据
├── status-schema.md                   status.json 字段与消费边界
├── tools.md                           校验、状态生成、检索与同步命令
├── shared-asset-manifest.yaml          source → destination 清单
├── code-dimensions.md                 代码结构分析维度
├── requirement-example.md             requirement 写作示例
└── markdown-line-limit-exemptions.json 行数校验的显式 fixture 豁免
```

- **改路由或恢复行为**：workflow contract → 命中的 lane 续作参考 → 对应 skill；不因操作参考的标题而降低规范性契约的优先级。
- **写产物**：当前模板 → 对应 shared-conventions 分片；总入口仅按需读相关节。统一读取策略见 `skill-quality-contract.md` 的“启动成本”。
- **改共享规则**：先改 `cs-onboard/reference/` 模板源，再按 manifest 更新 `.codestable/reference/` 副本；不能只改当前项目副本。
- **验证改动**：运行 `./scripts/verify.sh`；只核对共享资产或路由目标时可单独运行 `python .codestable/tools/check-workflow-contracts.py`。

---

## 1. 断点恢复

AI 对话随时可能中断（token 超限、网络断开、用户换设备）。各阶段发现自己不是从零开始时，必须优先检查已有产物的完成度，从上次停下的地方继续：

- **顶层短回复**：用户只回 `继续 / 确认 / 同意 / 按这个修 / 跳过 / 继续下一步` 时，先查是否存在唯一候选续作；命中才自动继续，多个候选停下来让用户选；`.ccg/tasks/*/task.json` 只作恢复桥，不是真相源
- **brainstorm**：如 `{slug}-brainstorm.md` 已有部分内容，读取后问用户"上次聊到 X，要接着聊还是推翻重来？"
- **design**：如 `{slug}-design.md` 已有部分节，逐节检查完成度，补齐缺失节，不重写已完成节
- **implement**：`{slug}-checklist.yaml` 中已 `done` 的步骤不重做，从第一个 `pending` 步骤开始
- **acceptance**：如 `{slug}-acceptance.md` 已有部分节，检查哪些节已填写（有实质 checklist 勾选），从下一个未完成节继续
- **issue-analyze**：如 `{slug}-analysis.md` 已存在，检查 5 节是否都有内容，缺失的补做，已有的不重写
- **issue-fix**：如代码已改但 `{slug}-fix-note.md` 不存在，直接进入验证 + 写 fix-note 环节

恢复时先向用户简短汇报："检测到上次工作到 X 阶段，我从 Y 继续"。

---

## 2. 扩展点

### 新增子工作流

新工作流定型后，在 `cs-onboard/reference/system-overview.md` 的技能索引和场景路由表里登记，并同步 `cs/SKILL.md` 与相关 lane 路由表；`check-workflow-contracts.py` 检查具体路由目标存在且 frontmatter `name` 与目录名一致。

### 跨阶段新约束

如果发现某条规则适用于所有阶段（例如所有 spec doc 都必须补某个字段），优先写进共享 reference（`shared-conventions.md` 或 `system-overview.md`），不要只改一个子技能。

### 新模板 / 新产物类型

如果引入新的 spec 产物（例如风险评估表、回滚预案），先在 `shared-conventions-core.md` 登记路径，再在对应阶段技能里引用。

### 共享术语表

如果 CodeStable 自己形成了稳定共享术语，应优先沉淀成共享 reference，而不是散落在多个子技能里重复定义。

### 跨工作流状态一览

目前查看"项目当前有几个 feature 在进行中、几个 issue 未关闭"仍需要手动查询。现在统一使用 `.codestable/tools/build-status.py` 生成 `.codestable/status.json` 作为 machine-readable spine；`STATUS.md` 仍然可选，不是路由前提。

---

## 3. 维护规则

- 每次扩展都要同步更新 `system-overview.md` 索引和相关子技能
- 不允许只在某个子技能里加东西而不在 `system-overview.md` 登记
- 共享说明先维护 `cs-onboard/reference/` 模板源，再刷新 `.codestable/reference/`，不要散落在各子技能里
