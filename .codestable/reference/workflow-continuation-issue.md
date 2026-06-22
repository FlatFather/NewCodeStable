---
protocol_version: 1.0
extends: workflow-continuation-base.md
---

# Workflow Continuation Protocol — Issue Extension

本文件定义 **issue 主线**的 continuation-first 续作细则。

核心原则见 `workflow-continuation-base.md`。

---

## 顶层入口：cs-issue

收到用户输入后，顺序固定为：

1. 先看是不是短回复
2. 若是短回复，检查是否存在唯一候选续作
3. 若存在：直接恢复，不重复输出路由建议
4. 若不存在：回到现有路由判断

### 恢复顺序

优先看：
- 是否存在唯一相关 issue 目录
- 当前停在 report / analyze / fix 哪一阶段

若命中，直接继续该阶段；不要把 `按这个修` 一类回复重新理解成新 issue。

---

## 阶段 skill 续作规则

阶段 skill 收到 continuation 时，恢复顺序固定为：

1. **先读 spec 产物状态**
2. **task 文件只作桥接线索**
3. 恢复后向用户汇报"检测到上次做到 X，我从 Y 继续"

### cs-issue-report

先看是否已有同类 issue 目录，确认是更新还是新建。

当 report 阶段已经收口并且用户明确回复 `确认 / 继续 / 同意` 时，report skill 只负责结束当前 checkpoint；**真正的续作恢复应回到 `cs-issue` 顶层入口**，由它根据 `report.md` 已存在且 `analysis.md` 缺失的状态续到 `cs-issue-analyze`。

### cs-issue-analyze

先看 analysis 是否部分完成。

### cs-issue-fix

先看 fix-note 是否缺失、代码是否已改、验证是否完成。
