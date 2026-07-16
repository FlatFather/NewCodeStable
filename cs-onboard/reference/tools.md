# CodeStable 工具用法参考

本文件由 `cs-onboard` 复制到项目的 `.codestable/reference/tools.md`，所有 CodeStable 子技能用项目相对路径 `.codestable/reference/tools.md` 引用。

`.codestable/tools/` 下共享脚本的完整用法参考。子技能里只写本技能特有的 1-2 行典型查询；完整语法和示例看这里。

---

## 0. build-status.py

生成 workflow 的 machine-readable status spine。它只读取 canonical `.codestable/` artifacts，确定性输出 `.codestable/status.json`，并显式记录 freshness / consistency / bridge-hint 边界。

### 基本语法

```bash
python .codestable/tools/build-status.py
python .codestable/tools/build-status.py --repo-root /path/to/repo
python .codestable/tools/build-status.py --check
python .codestable/tools/build-status.py --check --json
```

### 默认输入

- `.codestable/features/**`
- `.codestable/issues/**`
- `.codestable/refactors/**`
- `.codestable/audits/**`

### 明确非输入

- `.ccg/tasks/*/task.json`
- `context.jsonl`
- `STATUS.md`

### 输出语义

- `status.json` 是 **derived-only** 状态脊柱，不是 authority
- `freshness.canonical_digest` 用于判断生成结果是否已 stale
- `--check --json` 输出 machine-readable freshness：`fresh` 返回 0、`stale` 返回 1、canonical `conflict` 返回 2
- lane item 同时区分：
  - `canonical`：直接从正式产物读取的事实
  - `derived`：由 canonical facts 推导出的阶段视图
  - `consistency`：`clean | compatibility | conflict`
- `bridge_hints` 只登记边界说明，不参与状态推导

### 消费约束

- 若当前 canonical digest 与 `status.json.freshness.canonical_digest` 不一致，消费方必须回退到 canonical inspection
- 若 item 的 `consistency.state = conflict`，消费方不得把该 item 的 derived state 作为最终结论
- `STATUS.md` 缺失不影响任何路由行为

---

## 0. check-workflow-contracts.py

工作流契约只读校验器。用于检查共享资产 manifest parity、repo-local 副本、活跃 workflow 口径一致性，以及所有 Git 跟踪 Markdown 的行数上限。`markdown-line-limit-exemptions.json` 中有理由的 fixture 可被显式豁免。脚本只读、确定性、无额外依赖。

### 基本语法

```bash
python .codestable/tools/check-workflow-contracts.py
python .codestable/tools/check-workflow-contracts.py --repo-root /path/to/repo
python .codestable/tools/check-workflow-contracts.py --json
```

### 默认检查项

- `cs-onboard/reference/shared-asset-manifest.yaml` 与 `.codestable/reference/shared-asset-manifest.yaml` 的 parity
- manifest 声明的 `source` / `destination` 文件是否存在、是否仍落在共享合同路径前缀下
- 被活跃 workflow 文档引用的 `.codestable/reference/*` / `.codestable/tools/*` 是否真实存在且已写入 manifest
- 活跃 / 公共文档是否仍使用标准 feature 主线：`cs-feat → cs-feat-design → cs-feat-plan → cs-feat-impl → cs-feat-accept`
- 活跃 workflow 文档是否违反 `.codestable/` 路径契约
- Markdown 文档是否超过仓库当前行数上限（默认从 `CLAUDE.md` / `AGENTS.md` 读取，当前为 500）
- 历史 legacy feature 是否被兼容读取而非误判为硬失败

### 严格 / 兼容分层

- **严格失败**：活跃 workflow 文档、公共文档、manifest parity、共享资产缺失、被重开的 hybrid feature 缺少 `plan.md` 或 `checklist.yaml`
- **兼容警告**：历史 / 归档 artifact 的旧口径、未重开的 legacy feature 缺少 `plan.md` 或 design 里没有 `workflow`；已审查的历史警告仅可通过 `workflow-contract-warning-baseline.json` 基线化，新警告仍会报告。
- **样板例外**：仓库内显式标记为 sample/example 的 feature，在仓库级运行中按 compatibility warning 处理；严格失败场景由 `tests/fixtures/workflow-contracts/` 单独覆盖

### Fixtures

推荐 fixtures 目录：`tests/fixtures/workflow-contracts/`。至少覆盖：

- 缺失共享资产
- destination 路径错误
- 活跃 feature-flow wording drift
- Markdown 超过行数上限
- legacy feature 兼容例外

---

## 1. search-yaml.py

通用 YAML frontmatter 搜索工具。从项目根目录运行，无需安装额外依赖（PyYAML 可选，有则用，无则内建 fallback parser）。

### 基本语法

```bash
python .codestable/tools/search-yaml.py --dir {目录} [--filter key=value]... [--query "全文关键词"] [--sort-by FIELD [--order asc|desc]] [--full] [--json]
```

### filter 语法

- `key=value`：字段精确匹配（大小写不敏感）
- `key~=value`：字符串字段子串匹配；列表字段元素包含匹配
- `key=a|b|c` / `key~=a|b|c`：同一字段多个候选值，候选之间是 OR；在 PowerShell / Bash 中请给整个 filter 加引号，例如 `--filter "doc_type=decision|explore|learning"`

### 排序语法

- `--sort-by FIELD`：按 frontmatter 字段排序（典型字段：`last_reviewed`、`date`、`updated_at`）
- `--order desc|asc`：`desc` 默认，新的在前；`asc` 老的在前（查"谁最久没更新"用这个）
- 字段缺失 / 值为空的文档一律排到最后，不干扰前排结论

### 常用命令

沉淀类文档统一在 `.codestable/compound/`，用 `doc_type` 字段区分四个子技能的产物，内部还有各自的细分字段：

```bash
# 按 doc_type 筛选
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=learning
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter "doc_type=decision|explore|learning" --filter status=active
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=decision --filter status=active
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=trick --filter status=active
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=explore --filter status=active

# doc_type + 子技能内部细分字段
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=learning --filter track=pitfall
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=decision --filter category=constraint
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=trick --filter type=pattern
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=explore --filter type=question

# 按 tag（列表元素包含匹配）
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter tags~=prisma

# 全文搜索
python .codestable/tools/search-yaml.py --dir .codestable/compound --query "shadow database"

# 按领域/框架/语言筛选
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=decision --filter area=frontend
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=trick --filter framework~=vue
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=trick --filter language=typescript

# 搜索 feature 方案 doc
python .codestable/tools/search-yaml.py --dir .codestable/features --filter doc_type=feature-design --filter status=approved

# 输出控制
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter doc_type=decision --filter status=active --full
python .codestable/tools/search-yaml.py --dir .codestable/compound --filter tags~=llm --json

# 按时间排序
python .codestable/tools/search-yaml.py --dir .codestable/compound --sort-by date --order desc                     # 最近归档的在前
python .codestable/tools/search-yaml.py --dir .codestable/library-docs --sort-by last_reviewed --order asc         # 最久没 review 的在前（找陈旧文档）
python .codestable/tools/search-yaml.py --dir .codestable/guides --filter status=current --sort-by last_reviewed --order asc
```

### 典型使用场景

| 场景 | 命令建议 |
|---|---|
| feature-design 开始前查已有归档 | 搜 `.codestable/compound` 目录，按 `--query "{关键词}"` 全文搜；要分类看就加 `--filter "doc_type=learning\|trick\|decision\|explore"` |
| issue-analyze 根因分析前查历史 | 搜 `.codestable/compound` `--filter doc_type=learning --filter track=pitfall`、再搜 `--filter doc_type=trick --filter type=library`，按相关组件/框架过滤 |
| 归档落盘后查重叠 | 搜 `.codestable/compound --query "{关键词}" --json`，看有无语义重叠 |
| 新人了解项目规约 | `--dir .codestable/compound --filter doc_type=decision --filter status=active` |
| 按技术栈浏览技巧 | `--dir .codestable/compound --filter doc_type=trick --filter language={语言} --filter status=active` |
| 找最久没 review 的库文档 / 指南 | `--dir {目录} --filter status=current --sort-by last_reviewed --order asc` |
| 看最近沉淀了哪些经验 | `--dir .codestable/compound --filter doc_type=learning --sort-by date --order desc` |

---

## 2. validate-yaml.py

YAML 语法校验工具。用于验证 frontmatter 语法和必填字段，也支持 feature workflow contract 校验。

```bash
# 校验单个文件的 YAML 语法
python .codestable/tools/validate-yaml.py --file {文件路径} --yaml-only

# 校验必填字段
python .codestable/tools/validate-yaml.py --file {文件路径} --require doc_type --require status

# 批量校验目录下所有文件
python .codestable/tools/validate-yaml.py --dir {目录} --require doc_type --require status

# 校验一条 feature 的 workflow contract（design / plan / checklist / roadmap 绑定）
python .codestable/tools/validate-yaml.py \
  --feature-dir .codestable/features/{feature-dir} \
  --roadmap .codestable/roadmap/{roadmap}/{roadmap}-items.yaml \
  --workflow-check
```

### workflow-check 规则

- `design_workflow`：design frontmatter 的 `workflow` 只能是 `legacy|hybrid`
- `plan_presence`：`workflow: hybrid` 时必须存在 `{slug}-plan.md`
- `binding_rule`：`design.feature = items.feature`；hybrid 时 `plan.feature = design.feature`
- `step_alignment`：plan step 数量与 checklist step 数量一致
- 输出是只读诊断：规则名 + 文件路径 + 失败原因，不自动改写文档

### 历史 feature 适用边界

- workflow-check 默认用于**新 feature**和**被重开的历史 feature**
- 历史 feature 如果只是留档、不继续推进，则缺 `workflow` 或 `plan.md` 不应直接被视为错误
- 如果用户决定重开旧 feature，再按 `legacy` 或 `hybrid` 路径补最小必要字段和产物后运行 workflow-check
---

## 4. sync-skills.sh

将仓库技能同步到允许的本地安装目录；该脚本不属于 onboarding shared bundle。

```bash
.codestable/tools/sync-skills.sh --dry-run cs-feat
.codestable/tools/sync-skills.sh cs-feat
.codestable/tools/sync-skills.sh --verify cs-feat
```

`--verify` 只比较仓库源码与已安装副本（会解析 symlink），不创建目录、不写入文件；发现缺失或 drift 时返回非零。
