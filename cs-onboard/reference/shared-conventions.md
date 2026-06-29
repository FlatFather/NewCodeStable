# CodeStable 共享口径

由 `cs-onboard` 复制到项目的 `.codestable/reference/shared-conventions.md`。所有 CodeStable 子技能用项目相对路径引用——跨子技能共享但不适合堆在单个技能里的规范的唯一权威版本。

skill 本身不共享文件系统（每个 skill 是独立安装单元），共享口径不能放在某个 skill 内部被别的 skill 引用。放在"工作项目"里对所有 skill 都可达。

## workflow 契约入口

工作流的规范性规则已集中到 `workflow-contract.md` 及其模块：

- truth source / authority ordering → `workflow-contract-authority.md`
- continuation-first / 恢复边界 → `workflow-contract-continuation.md`
- generated state 语义 → `workflow-contract-generated-state.md`
- source/copy 分发关系 → `workflow-contract-distribution.md`

---

## 模块导航

本文档已按主题拆分为多个模块，按需引用：

- **`shared-conventions-core.md`** — 目录结构与命名规则（第 0 节）
  - 骨架目录定义、命名规则、架构 doc 分组规则
- **`shared-conventions-feature.md`** — feature 产物职责边界（第 2 节）
  - hybrid feature 标准口径、四类产物职责、迁移总则
- **`shared-conventions-checklist.md`** — checklist 生命周期（第 3 节）
  - checklist 职责划分、design / implement / acceptance 各阶段读写规则
- **`shared-conventions-roadmap.md`** — roadmap ↔ feature 衔接（第 2.5 节）
  - items.yaml 状态机、cs-roadmap / cs-feat-design / cs-feat-accept 职责

本文件保留第 1、3-7 节（共享元数据、收尾提交、归档检索、守护规则、反射检查），为所有技能共用。

---

## 1. 共享元数据口径

**feature spec**：design / acceptance 共用 `doc_type` / `feature` / `status` / `summary` / `tags`。子技能只补特有字段。design 采用标准口径时固定写 `workflow: hybrid`；历史 legacy 目录若保留原字段，可继续只读兼容。

**feature intent**：`{slug}-intent.md` 是 feature 的**可选前置草稿**，用于用户在 design 前先写下需求概要 / 大致做法 / 相关数据结构。frontmatter 固定为 `doc_type=feature-intent`、`feature`、`status=draft`、`summary`；它供 `cs-feat-design` 的初始化模式和正式起草入口读取，不参与 implement / acceptance 生命周期，也不替代 brainstorm note。

**issue spec**：report / analysis / fix-note 共用 `doc_type` / `issue` / `status` / `tags`。`severity` / `root_cause_type` / `path` 由对应阶段按需补。

**归档类（compound）**：

- learning / trick / decision / explore 四类**统一写入 `.codestable/compound/`**
- 每个文档 frontmatter 顶部带 `doc_type`（learning / trick / decision / explore）作跨子技能归属判定
- 文件名 `YYYY-MM-DD-{doc_type}-{slug}.md`——日期打头便于 `ls` 排序，type 段在中间便于 grep
- 各子技能在 `doc_type` 之外保留专属 frontmatter（learning 的 `track` / trick 的 `type` / decision 的 `category` / explore 的 `type`）
- 各子技能只认自己的 `doc_type` 不读写别家
- `status` 等通用字段语义和本文件保持一致

**外部读者文档**（guidedoc / libdoc）：frontmatter 由各自子技能定义。无特殊说明：`draft` = 待 review，`current` = 当前有效，`outdated` = 代码已变更待同步。

**写作约束**：子技能提字段时优先写"额外字段"或"阶段状态变化"，不重复展开整套通用字段。

### 1.5 continuation-first 摘要
- 本仓库内 skills 遇到 `继续 / 确认 / 同意 / 按这个修 / 跳过 / 继续下一步` 这类短回复时，默认先做 continuation-first 检测；只有存在**唯一候选续作**时才自动继续，多个候选必须停下来让用户选。
- `.ccg/tasks/*/task.json` 只作**task 状态桥**，不替代 feature / issue spec 产物的真相源地位；规范性定义见 `.codestable/reference/workflow-contract-continuation.md` 与 `.codestable/reference/workflow-contract-authority.md`，本文件只保留摘要与指针。

---

## 3. 阶段收尾推荐

**feature-acceptance** 收尾按顺序判断：

1. `cs-learn`：沉淀经验
2. `cs-decide`：长期约束 / 选型
3. `cs-guide`：开发者 / 用户指南
4. `cs-libdoc`：公开 API 参考
5. `scoped-commit`

**issue-fix** 收尾按顺序判断：

1. `cs-learn`：坑点
2. `cs-decide`：暴露的长期约束
3. `scoped-commit`

**feature-ff** 收尾按顺序判断（比标准 acceptance 短，没有 architecture / req 回写动作）：

1. `cs-learn`：动手过程暴露的坑
2. `cs-decide`：动手过程拍板的长期约束
3. `scoped-commit`

**统一规则**：一律一句话提示；用户说"不用"立即跳过；不强制；上游主动提示，下游承接执行。

---

## 4. 收尾提交（scoped-commit）

acceptance / issue-fix 走完后把本次产物提交为一个 commit：

- **范围**：本次工作改到的代码 + 相关 spec 文档 + 本次实际更新过的架构 doc + 本次实际更新过的 roadmap items.yaml / 主文档
- **不该进**：和本次工作无关的顺手修改；属于"下次另起 feature / issue"的扩大范围
- **提交前确认**：用户没明确同意不要 `git commit`
- **commit message**：一句话说清"做了什么"，不贴 spec 目录路径

子技能只描述本阶段特有提交范围，通用规则看这里。

---

## 5. 归档检索规则

feature-design / issue-analyze / issue-fix 动手前到 `.codestable/compound/` 搜已有沉淀：

- 总是先搜 `architecture/` 和 `compound/`
- 在 `compound/` 用 `doc_type` 过滤（learning / trick / decision / explore）
- 搜到的结果只作参考输入，不盲目套用——可能已 `outdated` 或不适合当前上下文
- 搜到和当前方向冲突的 decision → **必须**正面回应"为什么仍然这么做"或调整方向

子技能只补本阶段查询命令。完整搜索语法看 `.codestable/reference/tools.md`。

---

## 6. 归档类子技能共享守护规则

`cs-learn` / `cs-trick` / `cs-decide` / `cs-explore` 共享下面这组规则。子技能正文只写特有反模式，通用看这里：

1. **只增不删**——已归档除非被明确取代（`status=superseded`）否则不删；理由丢失成本极高
2. **宁缺毋滥**——用户说不出理由的节直接省略，不要 AI 编造
3. **不替用户写实质内容**——AI 负责起草结构和串联语言，实质结论必须来自用户或可追溯的代码证据
4. **attention.md 检查**——写完后若沉淀暴露出"每次启动都该知道"的一两行硬约束，提示用户用 `cs-note` 追加到 `.codestable/attention.md`；不要直接改外部 AI 入口
5. **起草前先查重叠**——动手写前用 `search-yaml.py --query` 查语义相近的旧文档。命中就把候选列给用户在三条路径里选：
   - **更新已有**（默认优先）：沿用原文件名和原创建日期，**不新建**；frontmatter 补 `updated: YYYY-MM-DD`；超出小修在文末加"YYYY-MM-DD 更新"简述
   - **supersede**：旧文档保留原文，`status: superseded` + `superseded-by: {新文件名}`，正文顶部加 `**[已取代]** 见 {新 slug}`；新文档 frontmatter 带 `supersedes: {旧文件名}`
   - **确实是不同主题**：新建，文末"相关文档"列出已有那条说明区别
6. **识别用户意图是"改已有"还是"记新的"**——用户说"改 / 更新 / 修订 / 补充 {某条}"、明确指向某条旧文档、或话题高度重合时默认走"更新已有"，不要闷头新建。分不清就问。

各子技能只认自己的 `doc_type`，不读写别家产物。

---

## 7. 写代码时的反射检查

`cs-feat-impl` 和 `cs-issue-fix` 共用。AI 默认会往"大函数 / 大文件 / god class / 处处特殊分支"漂，这一节把漂移截在发生那一刻。

**不是阈值，是触发器**——硬数字会诱发为拆而拆把自然聚合的代码切碎。每条都是"遇到 X 情况就停下来问自己"。

| 触发场景 | 停下来问自己 |
|---|---|
| 要往一个已经很长的文件追加代码时 | 文件承担几件事？新加的是已有职责延伸还是第 N+1 件事？是第 N+1 就默认新建文件 |
| 要给已经很多方法的类加方法时 | 新方法是核心职责的自然扩展，还是把类推向"什么都能干"？ |
| 写的函数已超过一屏时 | 函数在做几件事？几件事就拆 |
| 要加 `if (特殊情况) { 特殊处理 }` 分支时 | 抽象维度选错了？正确做法可能是把特殊路径和通用路径分成不同函数 / 策略 / 类 |
| 要 copy-paste 一段代码时 | 能抽成共用还是只字面相似？能抽就抽 |
| 要给函数加第 4+ 个参数时 | 函数做的事是不是太多了？参数列表是 API 恶化的早期信号 |
| 要新写"万能工具类 / helper"时 | 真没归属还是只是想不起来放哪儿就先堆 util？ |

**停下来之后**：反射检查只把问题提出来，结论用户定。停下来想清楚的动作（拆 / 新建 / 重命名 / 抽共用）会让改动超出现有 steps 范围 → 跟用户对齐再决定（纳入当前推进 / 记顺手发现留后续）。

不许偷偷拆完继续写，也不许忽略信号硬冲。默认动作是停、问、再继续。
