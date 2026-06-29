---
protocol_version: 1.0
---

# Workflow Continuation Protocol — Base

本文件定义 **continuation-first** 核心原则与通用规则。

特定工作流（feature / issue / refactor / audit）的续作细则见对应的扩展文档。

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

绝不默认猜"最近一个"或"最像的一个"。

### 2.3 task 状态桥，不是真相源

`.ccg/tasks/*/task.json` 与 `context.jsonl` 只作**恢复桥**：

- 帮顶层 skill 快速定位"上次做到哪里"
- 帮阶段 skill 知道"这次是从哪条入口续过来的"

它们**不是** feature / issue 工作流的真相源。

真正的 workflow 真相源仍然是：

- feature：`design.md` / `plan.md` / `checklist.yaml` / `acceptance.md`
- issue：`report.md` / `analysis.md` / `fix-note.md`

---

## 3. 短回复信号

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

## 4. 恢复时必须说清楚什么

命中 continuation 后，至少要向用户说明三件事：

1. 我检测到你是在继续已有流程
2. 当前识别到的对象是什么（feature / issue / task）
3. 我将从哪个阶段 / 哪一步继续

推荐格式：

```text
检测到你在继续 {对象}，当前停在 {阶段 / 步骤}，我从 {下一动作} 继续。
```

---

## 5. 反向边界

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

## 6. 特定工作流续作细则

每个工作流的续作规则细节见对应扩展文档：

- **feature 主线**：`.codestable/reference/workflow-continuation-feature.md`
- **issue 主线**：`.codestable/reference/workflow-continuation-issue.md`

---

## 7. 与其他文档的关系

- `shared-conventions.md:102-104`：只保留 continuation-first 摘要与指向本文件的指针
- `maintainer-notes.md`：记录维护者视角的断点恢复要求
- `system-overview.md`：记录体系级摘要，不展开细则
