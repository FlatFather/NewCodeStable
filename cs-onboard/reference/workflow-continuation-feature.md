---
protocol_version: 1.0
extends: workflow-continuation-base.md
---

# Workflow Continuation Protocol — Feature Extension

本文件定义 **feature 主线**的 continuation-first 续作细则。

核心原则见 `workflow-continuation-base.md`。

---

## 顶层入口：cs-feat

收到用户输入后，顺序固定为：

1. 先看是不是短回复
2. 若是短回复，检查是否存在唯一候选续作
3. 若存在：直接恢复，不重复输出路由建议
4. 若不存在：回到现有路由判断

### 恢复顺序

优先看：
- 是否存在唯一相关 feature 目录
- 该目录当前停在哪个阶段（design / plan / impl / accept）

若命中，直接基于已有产物状态继续；不要重复给出同一个路由结论。

---

## 阶段 skill 续作规则

阶段 skill 收到 continuation 时，恢复顺序固定为：

1. **先读 spec 产物状态**
2. **task 文件只作桥接线索**
3. 恢复后向用户汇报"检测到上次做到 X，我从 Y 继续"

### cs-feat-design

先看 design / intent / brainstorm 已有产物。

当 design 阶段已经整体 review 通过并且用户明确回复 `同意 / 继续 / 确认` 时，design skill 只负责结束当前 checkpoint；**真正的续作恢复应回到 `cs-feat` 顶层入口**，由它根据 `design.md` 已 approved 且 `plan.md` / `checklist.yaml` 未落齐的状态续到 `cs-feat-plan`。

### cs-feat-plan

先看 design 是否 approved、plan/checklist 是否已存在。

### cs-feat-impl

先看 checklist 哪些 steps 已 done。

### cs-feat-accept

先看 acceptance 哪些节已完成。
