---
doc_type: issue-analysis
issue: 2026-06-11-refactor-audit-continuation-missing
status: confirmed
root_cause_type: missing-feature
related: [refactor-audit-continuation-missing-report.md]
tags: [workflow, continuation, cs-refactor, cs-audit]
---

# refactor audit continuation missing 根因分析

## 1. 问题定位

| 关键位置 | 说明 |
|---|---|
| `.codestable/reference/workflow-continuation.md:13-15` | continuation-first 适用范围明确列出 `cs`、`cs-feat`、`cs-issue`，未列出 `cs-refactor` / `cs-audit` |
| `cs-refactor/SKILL.md:1-100` | 无短回复 continuation-first 处理规则 |
| `cs-audit/SKILL.md:1-100` | 无短回复 continuation-first 处理规则 |
| `cs/SKILL.md:116-124` | 参考实现：短回复 continuation-first 节 |
| `cs-feat/SKILL.md:89-97` | 参考实现：路由表 + continuation-first 约束 |
| `cs-issue/SKILL.md:86-96` | 参考实现：路由表 + continuation-first 约束 |

## 2. 失败路径还原

**正常路径（cs-feat / cs-issue）**：
1. 用户在 feature / issue 流程中输入"继续"
2. 顶层 skill 检测短回复 → 触发 continuation-first
3. Glob `.codestable/features/` 或 `.codestable/issues/`
4. 找到唯一候选目录 → 恢复已有产物状态
5. 直接路由到对应阶段 skill，不重复给路由建议

**失败路径（cs-refactor / cs-audit）**：
1. 用户在 refactor / audit 流程中输入"继续"
2. 顶层 skill **未检测短回复** → 按普通新诉求处理
3. 重新做路由判断或重新扫描
4. 用户体验：明明在继续同一个任务，却被当成新任务重新处理

**分叉点**：`workflow-continuation.md:13-15` — 适用范围未明确包含 `cs-refactor` / `cs-audit`，导致这两个 skill 未实现 continuation-first 规则。

## 3. 根因

**根因类型**：missing-feature（功能缺失）

**根因描述**：

`workflow-continuation.md` 在设计时优先覆盖了 feature / issue 主流程，但未显式声明 `cs-refactor` 与 `cs-audit` 是否适用。

这两个 skill 同样具备"顶层入口 + 阶段产物 + 可中断续作"特征，理应纳入 continuation-first 适用范围，但当前：
1. 协议文档未列出这两个 skill
2. `cs-refactor/SKILL.md` 和 `cs-audit/SKILL.md` 未实现短回复检测与目录状态恢复逻辑
3. 用户在这两个流程中输入"继续"时，无法自动恢复已有 refactor / audit 目录状态

**是否有多个根因**：否，单一根因为协议适用范围遗漏。

## 4. 影响面

- **影响范围**：仅影响 `cs-refactor` 与 `cs-audit` 流程的短回复续作场景；不影响 feature / issue 流程
- **潜在受害模块**：使用 refactor / audit 流程的用户，在中断后输入"继续"会被重新路由或重新扫描
- **数据完整性风险**：无。不会丢失已有 refactor / audit 产物，只是不能自动续作
- **严重程度复核**：维持 P1。虽不影响核心 feature / issue 流程，但 continuation-first 是当前 workflow 核心改进点，同类入口不一致会降低用户体验

## 5. 修复方案

### 方案 A：补充适用范围 + 实现 continuation-first 规则（推荐）

**做什么**：
1. 修改 `workflow-continuation.md:13-15`，补充：
   ```markdown
   - 顶层入口：`cs`、`cs-feat`、`cs-issue`、`cs-refactor`、`cs-audit`
   ```
2. 在 `cs-refactor/SKILL.md` 路由表前增加"短回复 continuation-first"节（参考 `cs-feat` / `cs-issue` 写法）：
   - 检测短回复信号
   - Glob `.codestable/refactors/` 查找唯一候选目录
   - 根据已有产物状态判断 scan / design / apply
   - 多个候选停下来让用户选
3. 在 `cs-audit/SKILL.md` Phase 1 范围收敛前增加短回复检测（参考 `cs` 写法）：
   - 检测短回复信号
   - Glob `.codestable/audits/` 查找唯一候选目录
   - 根据已有 index.md / finding-*.md 状态恢复
   - 多个候选停下来让用户选

**优点**：
- 补齐协议覆盖，所有顶层 workflow 入口续作行为一致
- 修复成本低（纯文档 + 轻量逻辑补充）
- 不影响已有 feature / issue 流程

**缺点 / 风险**：
- 需要同步修改 3 份文档（workflow-continuation.md + 2 个 SKILL.md）
- cs-refactor / cs-audit 的阶段产物状态判断需要新增逻辑（但可参考已有 cs-feat / cs-issue 实现）

**影响面**：
- 修改文件：`workflow-continuation.md`、`cs-refactor/SKILL.md`、`cs-audit/SKILL.md`
- 不影响其他 skill
- 不涉及代码改动，仅文档与 skill 规则补充

### 方案 B：明确排除 refactor / audit

**做什么**：
在 `workflow-continuation.md` 第 1 节"不适用"增加：
```markdown
- `cs-refactor`、`cs-audit`（原因：审计与重构通常一次完成，中断续作场景较少）
```

**优点**：
- 修改最少（只改 1 份文档）
- 明确协议边界

**缺点 / 风险**：
- 同类顶层入口行为不一致，用户难以预测哪些支持续作
- 实际使用中 audit / refactor 也可能中断（如审计大模块时分批扫描）
- 无合理技术理由排除这两个 skill

**影响面**：
- 修改文件：`workflow-continuation.md`
- 不解决用户体验不一致问题

### 方案 C：引入通用 continuation 机制

**做什么**：
- 把 continuation-first 提升为所有顶层 skill 的通用协议
- 在 `shared-conventions.md` 定义通用续作规则
- 所有顶层 skill 自动继承

**优点**：
- 长期架构更优雅
- 后续新增 skill 自动支持 continuation

**缺点 / 风险**：
- 改动范围大，需要重构多个 skill
- 可能引入不需要 continuation 的 skill（如一次性工具类 skill）
- 成本过高

**影响面**：
- 修改多份文档与 skill
- 风险较高

### 推荐方案

**推荐方案 A**，理由：
1. **改动范围适中**：只需修改 3 份文档，且可参考已有 cs-feat / cs-issue 实现
2. **直接解决根因**：补齐协议覆盖，让所有顶层入口行为一致
3. **风险可控**：纯文档与规则补充，不涉及代码改动
4. **用户体验改进明显**：refactor / audit 流程支持续作后，用户可以中断后继续，避免重复扫描
