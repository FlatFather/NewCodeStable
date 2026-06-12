---
doc_type: issue-analysis
issue: 2026-06-11-startup-boilerplate-duplication
status: confirmed
root_cause_type: duplication
related: [startup-boilerplate-duplication-report.md]
tags: [workflow, skills, boilerplate, maintainability]
---

# startup boilerplate duplication 根因分析

## 1. 问题定位

| 关键位置 | 说明 |
|---|---|
| `cs-feat/SKILL.md:8-10` | 启动必读段落（3 行） |
| `cs-issue/SKILL.md:8-10` | 启动必读段落（3 行），与 cs-feat 完全相同 |
| `cs-audit/SKILL.md:8-10` | 启动必读段落（3 行），与 cs-feat 完全相同 |
| `cs-arch/SKILL.md:8-10` | 启动必读段落（推测相同） |
| `cs-explore/SKILL.md:8-10` | 启动必读段落（推测相同） |
| 10+ 个 skill | 同一段文本逐字复制 |

## 2. 失败路径还原

**正常路径（理想状态）**：
1. 启动检查规则定义在单一权威来源
2. 各 skill 引用该来源或通过生成脚本自动同步
3. 修改规则时只需改一处，所有 skill 自动一致

**失败路径（当前状态）**：
1. 启动检查规则以手工复制形式散落在多个 skill
2. 新增 skill 时手动复制这段文本
3. 修改规则时需要逐个 skill grep 并手工替换
4. 遗漏某个 skill → 该 skill 与其他 skill 口径不一致

**分叉点**：没有单一权威来源或自动同步机制，导致维护者只能手工复制维护。

## 3. 根因

**根因类型**：duplication（重复维护）

**根因描述**：

CodeStable skill 体系在设计时，未为"所有 skill 共享的启动检查规则"建立单一权威来源或自动同步机制。

当前 10+ 个 skill 的 SKILL.md 都包含完全相同的"启动必读"段落（3 行），这段文本通过手工复制维护。每次修改启动规则时，维护者需要：
1. grep 找到所有包含该段落的 skill
2. 逐个文件手工替换
3. 确认没有遗漏

这种维护方式容易在以下场景出错：
- 新增 skill 时忘记复制或复制到旧版本
- 修改规则时遗漏某个 skill
- 不同 skill 被不同维护者修改导致微小差异

**是否有多个根因**：否，单一根因为缺少统一来源或自动同步机制。

## 4. 影响面

- **影响范围**：所有包含"启动必读"段落的 skill（10+ 个）
- **潜在受害模块**：当启动规则变更时（如 `attention.md` 改名、增加 fallback 规则），所有 skill 都需要同步更新
- **数据完整性风险**：无。纯文档问题，不影响运行时数据
- **严重程度复核**：维持 P1。虽不阻塞功能，但影响所有 skill 的维护一致性

## 5. 修复方案

### 方案 A：提取到 shared boilerplate（推荐）

**做什么**：
1. 创建 `.codestable/reference/boilerplate/startup-check.md`，内容为当前"启动必读"3 行文本
2. 所有 skill 的"启动必读"节改为一句话引用：
   ```markdown
   ## 启动必读
   
   启动规则见 `.codestable/reference/boilerplate/startup-check.md`。
   ```
   或直接在每个 skill 保留完整文本，但在 boilerplate 文件顶部注释说明"本文件是所有 skill 启动必读的权威来源，修改后需同步到各 skill"

**优点**：
- 单一权威来源，修改规则只需改一处
- 新增 skill 时引用该文件，不会复制到旧版本

**缺点 / 风险**：
- 需要修改 10+ 个 skill 文件
- 引用方式可能增加 skill 启动时的跳转成本（需要跳到另一个文件读取规则）

**影响面**：
- 新建文件：`.codestable/reference/boilerplate/startup-check.md`
- 修改文件：10+ 个 skill 的 SKILL.md（仅"启动必读"节）

### 方案 B：生成脚本

**做什么**：
1. 创建 `.codestable/tools/inject-boilerplate.py`
2. 从单一 boilerplate 源生成所有 skill 的"启动必读"节
3. pre-commit hook 或 CI 自动运行，确保 boilerplate 同步

**优点**：
- 单一权威来源
- 自动同步，无需手工维护
- 各 skill 保留完整文本，无跳转成本

**缺点 / 风险**：
- 需要开发生成脚本
- 需要配置 pre-commit hook 或 CI
- 增加项目复杂度

**影响面**：
- 新建文件：`.codestable/tools/inject-boilerplate.py`、boilerplate 源文件
- 可能修改：`.git/hooks/pre-commit` 或 CI 配置

### 方案 C：保留指针

**做什么**：
- 所有 skill 的"启动必读"节改为一句话：`启动规则见 .codestable/reference/shared-conventions.md 第 X 节`
- 在 `shared-conventions.md` 增加专节定义启动检查规则

**优点**：
- 单一权威来源
- 不需要新建文件或脚本

**缺点 / 风险**：
- 增加 skill 启动时的跳转成本
- `shared-conventions.md` 已超 300 行，继续增加会违反长度约束

**影响面**：
- 修改文件：`shared-conventions.md`、10+ 个 skill 的 SKILL.md

### 推荐方案

**推荐方案 A（简化版）**，理由：
1. **改动范围适中**：只需创建 1 个 boilerplate 文件 + 修改 10+ 个 skill
2. **单一权威来源**：修改规则只需改 boilerplate 文件，各 skill 保留完整文本（避免跳转成本）
3. **维护明确**：在 boilerplate 文件顶部注释说明"修改后需同步到各 skill"
4. **无需额外工具**：不需要开发生成脚本或配置 CI

**简化版具体做法**：
- 创建 `.codestable/reference/boilerplate/startup-check.md`，顶部注释说明这是权威来源
- 各 skill 保留当前完整"启动必读"文本，不改为引用（保持当前使用体验）
- 后续修改启动规则时，先改 boilerplate 文件，再 grep 同步到各 skill
- 这样至少建立了"权威来源"概念，降低维护者遗漏的风险
