---
doc_type: issue-analysis
issue: 2026-06-11-continuation-protocol-drift
status: confirmed
root_cause_type: missing-guard
related: [continuation-protocol-drift-report.md]
tags: [workflow, continuation, documentation, maintainability]
---

# continuation protocol drift 根因分析

## 1. 问题定位

| 关键位置 | 说明 |
|---|---|
| `.codestable/reference/shared-conventions.md:102-104` | continuation-first 摘要（3 行） |
| `.codestable/reference/workflow-continuation.md:1-180` | continuation-first 详细协议（180 行） |
| 10+ 个 skill | 依赖这两份文档的一致性进行路由判断 |

## 2. 失败路径还原

**正常路径（理想状态）**：
1. continuation-first 的摘要与详细协议之间有同步机制
2. 修改详细协议时，触发摘要同步提示或自动检查
3. 所有 skill 读到一致的续作规则

**失败路径（当前状态）**：
1. 摘要与详细协议分别维护
2. 修改其中一处时，没有提示或检查机制
3. 随着时间推移，两处描述可能出现口径漂移
4. Skill 读到不一致的规则

**分叉点**：缺少同步机制（版本号、自动检查脚本或其他防护），导致维护者只能手工保持一致。

## 3. 根因

**根因类型**：missing-guard（缺少防护机制）

**根因描述**：

`shared-conventions.md` 第 1.5 节保留 continuation-first **摘要**，`workflow-continuation.md` 保留**详细协议**。两份文档分别维护，但没有：
- 版本号标识
- 自动同步检查脚本
- 修改提示机制

当前依赖维护者手工保持一致。虽然当前两份文档内容一致，但缺少防护机制会导致后续维护时容易遗漏同步，形成口径漂移风险。

**是否有多个根因**：否，单一根因为缺少同步防护机制。

## 4. 影响面

- **影响范围**：10+ 个 skill 依赖这两份文档的一致性（cs / cs-feat / cs-issue / cs-refactor / cs-audit 及其阶段 skill）
- **潜在受害模块**：当 continuation-first 规则变更时（如短回复列表、唯一候选约束、task 状态桥规则），所有依赖 skill 的续作行为
- **数据完整性风险**：无。不会损坏产物，但可能导致用户体验不一致
- **严重程度复核**：维持 P1。虽然当前未确认已漂移，但 continuation-first 是核心 workflow 改进点，缺少防护机制会导致后续维护风险较高

## 5. 修复方案

### 方案 A：引入协议版本号（推荐）

**做什么**：
1. 在 `workflow-continuation.md` frontmatter 增加 `protocol_version: 1.0`
2. 在 `shared-conventions.md` 第 1.5 节引用时声明：`详细协议见 workflow-continuation.md (v1.0)`
3. 修改协议时同步升级版本号，摘要也同步刷新

**优点**：
- 版本号明确标识协议变更
- 改动范围最小（只需增加 frontmatter + 引用版本号）
- 维护者修改详细协议时能意识到需要同步摘要

**缺点 / 风险**：
- 依赖人工升级版本号，仍可能遗漏
- 版本号不匹配时没有自动检查

**影响面**：
- 修改文件：`workflow-continuation.md`（增加 protocol_version）、`shared-conventions.md`（引用版本号）

### 方案 B：自动同步检查脚本

**做什么**：
1. 创建 `.codestable/tools/check-continuation-sync.py`
2. 提取两份文档的关键规则点（如"短回复列表"、"唯一候选约束"）
3. pre-commit hook 或 CI 阶段运行，发现不一致时报错

**优点**：
- 自动发现不一致
- 强制同步保证

**缺点 / 风险**：
- 需要开发检查脚本
- 需要配置 pre-commit hook 或 CI
- 增加项目复杂度
- 文本一致性检查难以覆盖语义差异

**影响面**：
- 新建文件：`.codestable/tools/check-continuation-sync.py`
- 可能修改：`.git/hooks/pre-commit` 或 CI 配置

### 方案 C：合并回单文档

**做什么**：
- 把 `workflow-continuation.md` 合并回 `shared-conventions.md`

**优点**：
- 单一权威来源，无同步问题

**缺点 / 风险**：
- 违反项目"单 md 不超 300 行"约束（当前 shared-conventions 已 300+ 行，workflow-continuation 180 行）
- 被明确拒绝的方案

**影响面**：
- 不推荐

### 推荐方案

**推荐方案 A**，理由：
1. **改动范围最小**：只需增加 protocol_version + 引用版本号
2. **明确标识变更**：版本号升级提醒维护者需要同步摘要
3. **符合文档长度约束**：不违反 300 行限制
4. **风险可控**：纯文档修改，不涉及脚本开发或 CI 配置
