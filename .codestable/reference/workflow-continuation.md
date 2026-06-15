---
protocol_version: 1.0
---

# Workflow Continuation Protocol

本文件是 **continuation-first** 协议的入口与完整合集。

**推荐阅读顺序**：
1. 先读本文件（核心原则 + feature/issue 续作规则）
2. 需要深入了解时，再读拆分后的模块化文档

**拆分后的文档结构**（v1.1+）：
- `workflow-continuation-base.md` — 核心原则与通用规则
- `workflow-continuation-feature.md` — feature 主线续作细则
- `workflow-continuation-issue.md` — issue 主线续作细则

本文件保留完整内容以兼容已有引用；未来可考虑仅保留摘要 + 指针。

---

## 1. 适用范围

只适用于**本项目仓库内**的 workflow skills：

- 顶层入口：`cs`、`cs-feat`、`cs-issue`、`cs-refactor`、`cs-audit`
- feature 阶段：`cs-feat-design`、`cs-feat-plan`、`cs-feat-impl`、`cs-feat-accept`
- issue 阶段：`cs-issue-report`、`cs-issue-analyze`、`cs-issue-fix`

**不适用**：
- 全局 `/ccg:go`
- `~/.claude/commands/*`
- 仓库外的其他命令层

---

## 2. 核心原则

### 2.1 continuation-first

用户输入属于短回复时，skills 必须先判断：

- 这是在**继续已有任务**
- 还是在**发起新诉求**

如果能安全定位到唯一续作对象，就先恢复它；只有在**没有可恢复对象**时，才回到普通路由流程。

### 2.2 唯一候选约束

只有在**唯一候选续作**成立时，才允许自动继续。

不满足唯一性时：
- 停下来
- 告诉用户有哪些候选
- 让用户明确选择

绝不默认猜“最近一个”或“最像的一个”。

### 2.3 task 状态桥，不是真相源

`.ccg/tasks/*/task.json` 与 `context.jsonl` 只作**恢复桥**：

- 帮顶层 skill 快速定位“上次做到哪里”
- 帮阶段 skill 知道“这次是从哪条入口续过来的”

它们**不是** feature / issue 工作流的真相源。

真正的 workflow 真相源仍然是：

- feature：`design.md` / `plan.md` / `checklist.yaml` / `acceptance.md`
- issue：`report.md` / `analysis.md` / `fix-note.md`

---

## 3. 哪些输入算短回复

默认覆盖下面这些 continuation 信号：

- `继续`
- `确认`
- `同意`
- `按这个修`
- `跳过`
- `继续下一步`
- `resume`
- `go on`

扩展规则：
- 字数很短
- 没有新的完整目标 / 范围 / 对象描述
- 明显是在回应上一步 checkpoint / gate

如果一句话既像短回复又像新诉求，默认**不要猜**，直接补问。

---

## 4. 顶层 skill 的处理规则

顶层入口（`cs` / `cs-feat` / `cs-issue`）收到用户输入后，顺序固定为：

1. 先看是不是短回复
2. 若是短回复，检查是否存在唯一候选续作
3. 若存在：直接恢复，不重复输出路由建议
4. 若不存在：回到现有路由判断

### 4.1 `cs`

优先看：
- 是否存在唯一相关 feature / issue 目录
- 是否存在唯一 in-progress task

若命中，直接建议继续对应入口或阶段，而不是再讲一遍体系总览。

### 4.2 `cs-feat`

优先看：
- 是否存在唯一相关 feature 目录
- 该目录当前停在哪个阶段（design / plan / impl / accept）

若命中，直接基于已有产物状态继续；不要重复给出同一个路由结论。

### 4.3 `cs-issue`

优先看：
- 是否存在唯一相关 issue 目录
- 当前停在 report / analyze / fix 哪一阶段

若命中，直接继续该阶段；不要把 `按这个修` 一类回复重新理解成新 issue。

---

## 5. 阶段 skill 的处理规则

阶段 skill 收到 continuation 时，恢复顺序固定为：

1. **先读 spec 产物状态**
2. **task 文件只作桥接线索**
3. 恢复后向用户汇报“检测到上次做到 X，我从 Y 继续”

### 5.1 feature 主线

- `cs-feat-design`：先看 design / intent / brainstorm 已有产物
- `cs-feat-plan`：先看 design 是否 approved、plan/checklist 是否已存在
- `cs-feat-impl`：先看 checklist 哪些 steps 已 done
- `cs-feat-accept`：先看 acceptance 哪些节已完成

### 5.2 issue 主线

- `cs-issue-report`：先看是否已有同类 issue 目录，确认是更新还是新建
- `cs-issue-analyze`：先看 analysis 是否部分完成
- `cs-issue-fix`：先看 fix-note 是否缺失、代码是否已改、验证是否完成

---

## 6. 恢复时必须说清楚什么

命中 continuation 后，至少要向用户说明三件事：

1. 我检测到你是在继续已有流程
2. 当前识别到的对象是什么（feature / issue / task）
3. 我将从哪个阶段 / 哪一步继续

推荐格式：

```text
检测到你在继续 {对象}，当前停在 {阶段 / 步骤}，我从 {下一动作} 继续。
```

---

## 7. 反向边界

下面这些情况**不要**自动续作：

- 有多个候选对象
- 用户补充了新的范围、目标或限制
- 当前 spec 产物状态与 task 桥接信息冲突
- 现有产物不足以判断应该继续哪一步

这时默认动作是：
- 停
- 列候选
- 让用户选

---

## 8. 与其他文档的关系

- `shared-conventions.md`：只保留 continuation-first 摘要与指针
- `maintainer-notes.md`：记录维护者视角的断点恢复要求
- `system-overview.md`：记录体系级摘要，不展开细则
- `docs/dev/feature-workflow.md`：记录用户可见的 feature 主线续作说明
