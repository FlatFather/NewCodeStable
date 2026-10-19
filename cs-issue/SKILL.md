---
name: cs-issue
description: 修 bug 的子流程入口，把"发现问题"走到验证修复闭环，留下 report / analysis / fix-note 三份文件。触发：用户说"修 bug"、"有个问题"、"修复 XX"。只做路由，根据已有产物走 report / analyze / fix。简单问题走快速通道。
---

# cs-issue

## 启动必读

`cs-issue` 只做问题分类和阶段路由；先确认“新问题还是现有 issue 续作”，再读取命中资料：

- **Fast probe（每次）**：用户问题；若是短回复、带 issue slug 或明确说“继续”，再读取 fresh `status.json` 或指定 issue 目录的最小索引。
- **Handoff gate（命中后）**：`.codestable/attention.md` 在要进入具体 issue 工作前读取；`shared-conventions.md` 只在状态冲突、命名 / 目录语义不清或用户要求解释流程时读取。
- **不在路由层定位根因**：代码、日志、architecture、requirements 与 compound 由 report / analyze / fix 在路径确定后按需读取；路由层不得为猜根因而全仓扫描。

**缓存优化**：本轮已验证的 candidate、freshness 与 attention 复用；attention 缺失时提示先补齐或运行 `cs-onboard`。

修 bug 直觉是"找到错的地方改了完事"，但这个直觉路径反复制造同样的麻烦：

1. 问题描述只在脑子里改完就忘——三个月后 bug 再现没复现步骤留存
2. 根因没分析就动手——改了表面现象深层问题等下次爆发
3. 修复范围扩散——发现一个 bug 顺手改五处引入新问题，无法追溯
4. 没验收闭环——怎么判断改好了？改好了什么？没记录

issue 工作流在"看到问题"和"动手改代码"之间塞缓冲：

```
发现问题 → 清晰记录（report）→ 根因分析（analyze）→ 定点修复 + 验证（fix）
```

本技能不写任何东西，只看当前 issue 走到哪步、决定触发哪个子技能。

---

## 文件放哪儿

```
.codestable/issues/{YYYY-MM-DD}-{slug}/
├── {slug}-report.md           ← 阶段 1 问题报告
├── {slug}-analysis.md         ← 阶段 2 根因分析
└── {slug}-fix-note.md         ← 阶段 3 修复记录（必出产物）
```

日期取**发现 / 提报问题当天**定了不动。slug 能一眼看出是什么问题（`auth-token-leak`、`null-pointer-on-empty-list`）。

`{slug}-fix-note.md` 是阶段 3 **必出产物**——无论修复简单还是复杂都要写。它不是仪式，是回溯凭证：没有它下次类似问题来你只能从 git log 反推。

所有 issue 文档带 YAML frontmatter（`doc_type` 分别为 `issue-report` / `issue-analysis` / `issue-fix`）便于 `search-yaml.py` 按 severity / tags / status 检索。

---

## 两条路径

### 标准路径（问题复杂或根因不明）

| 阶段 | 子技能 | 主导 | 产出 |
|---|---|---|---|
| 1 问题报告 | `cs-issue-report` | 用户描述，AI 引导 | `{slug}-report.md` |
| 2 根因分析 | `cs-issue-analyze` | AI 读代码分析，用户确认 | `{slug}-analysis.md` |
| 3 修复验证 | `cs-issue-fix` | AI 按分析定点修复，用户验证 | 代码 + `{slug}-fix-note.md` + scoped-commit |

阶段间有人工 checkpoint——让用户在每阶段结束有一次明确把关，防止 AI 一口气从问题跑到代码跑出来才发现走偏。

### 快速通道（问题简单、根因一眼确定）

下面**同时满足**才进：

1. AI 读完代码后对根因高度有把握（能明确指出 file:line + 原因）
2. 修复改动很小（1-2 处）
3. 无跨模块影响风险

流程压缩成：AI 读代码 → 直接告知根因 + 修复方案 → 用户确认并建立 `status: draft` 的 `{slug}-fix-note.md` → AI 修复 → 用户验证通过 → AI 补全并完成 `{slug}-fix-note.md`。不产出 analysis。

**判定口径**：是否进快速通道由 `cs-issue-report` 的启动检查做唯一正式判定。一旦进标准路径默认不再二次改判——避免三个阶段对路径各说各话。

**不能**走快速通道：根因有多个候选 / 修复范围涉及多模块 / 需要先复现才能定位 / 用户希望留完整分析存档。

---

## 路由

按最小读取顺序路由，而不是每次先扫整个 issue lane：

1. **短回复 / 续作**：先运行 `workflow-routing.py`；唯一 fresh 候选直接进入 candidate 阶段，不额外 `Glob` 所有 issue。
2. **指定 issue**：只检查该目录的 report / analysis / fix-note；`status.json` 仅用于加速发现，stale 或冲突时才回退到这个目录的 direct inspection。
3. **新问题**：先判断它是 issue、feature 还是需要澄清；不在 router 层预读代码、日志或所有旧 issue。
4. **多个候选或状态冲突**：再列出候选或读取必要 canonical artifact，不能靠口头阶段说明绕过状态核验。

| 当前状态 | 触发哪个子技能 |
|---|---|
| 用户只回 `继续 / 确认 / 同意 / 按这个修 / 跳过 / 继续下一步` 这类短回复，且存在唯一候选 issue 目录 | **先按 continuation-first 续作**：直接根据该目录现有产物判断 report / analyze / fix，不重复按新 issue 路由 |
| 刚发现问题，没有任何文件 | `cs-issue-report`（那里判断走标准还是快速） |
| `report.md` 是 `status=draft`，没 `analysis.md` | `cs-issue-report`：完成 report checkpoint；不得提前进入 analyze |
| `report.md` 已 `status=confirmed`，有未 `completed` 的 `fix-note.md`，没 `analysis.md` | `cs-issue-fix`（快速通道，draft fix-note 是已确认方案的恢复记录） |
| `report.md` 已 `status=confirmed`，没 `analysis.md` 和 `fix-note.md` | `cs-issue-analyze`（包括用户刚在 report 阶段明确回复“确认 / 继续”的续作场景） |
| `analysis.md` 是 `status=draft`，代码还没改 | `cs-issue-analyze`：完成 fix-option checkpoint；不得提前进入 fix |
| `analysis.md` 已 `status=confirmed`，代码还没改 | `cs-issue-fix` |
| 代码已改，还没修复验证记录 | `cs-issue-fix`（走验证） |
| 不确定 | 自己读已有文件按上表对号 |

### continuation-first 约束

当用户输入是 `继续 / 确认 / 同意 / 按这个修 / 跳过 / 继续下一步` 这类短回复时，本技能先做 continuation-first：

1. 先看是否存在**唯一候选 issue 目录**（可优先参考 fresh `status.json` 的 issue lanes）
2. 命中 → 直接按该目录现有产物判断 report / analyze / fix；若 `status.json` 缺失、stale、或与 canonical artifacts 冲突，则以 issue 目录里的 report / analysis / fix-note 为准
3. 多个候选 → 列给用户选，不猜
4. 没有候选 → 才按普通 issue 路由处理

fresh helper 返回唯一 `continue` 时，直接传递 `{issue path, stage, blocker}` 给下游；不要为了二次确认再全量扫描 issue 目录。只有 `inspect_canonical` 或候选冲突时才扩展读取。

如果需要恢复桥接信息，可参考 `.ccg/tasks/*/task.json`，但它**只作 task 状态桥 / recovery hint**，不能替代 issue 目录里的 report / analysis / fix-note 真相源。详细协议见 `.codestable/reference/workflow-continuation.md`。

---

用户描述的是**新功能需求而不是 bug** → 告诉用户走 `cs-feat`。

---

## 质量执行约束

- **Hard-required**：用户问题，以及续作 / 指定 issue 命中时的 canonical artifact 与 fresh status。
- **On-demand**：attention、shared conventions、代码、architecture、requirements、compound 与 bridge hint 只在路径判定或证据需要时读取。
- **证据**：快速通道必须保留 file:line、改动范围、风险与验证方式；标准路径不在路由层伪造根因。
- 共同底线见 `.codestable/reference/skill-quality-contract.md`。

## 退出条件

- [ ] 已判定问题属于 issue、feature 或需进一步澄清
- [ ] 已按 canonical report/analysis/fix-note 状态路由，且 continuation 不重复消费 checkpoint
- [ ] 快速通道满足根因明确、改动小、无跨模块风险和可验证条件
- [ ] 唯一无 blocker 的下一阶段已 handoff；否则已列出需用户选择的缺口

## 与 feature 工作流的边界

- issue：本来应该好的东西坏了——已有代码里的 bug / 异常行为 / 文档错误 / 性能问题
- feature：从来没有的东西要加进来——新功能 / 新能力

完整判据见 `.codestable/reference/terminology.md` 第 1 节。

灰色地带：修 issue 过程中发现需要新增能力才能真正解决——**先用 issue 工作流把记录和分析做完，再视情况开 feature**。不在 issue 里偷偷做新功能，理由跟 feature 不在 PR 里偷偷修 bug 一样：混着改分不清这次到底改了什么范围。

---

## 相关文档

- `.codestable/reference/system-overview.md` — CodeStable 体系总览
- `.codestable/reference/shared-conventions.md` — 跨阶段共享口径
- `.codestable/attention.md` — CodeStable 启动注意事项和项目硬约束
- `.codestable/architecture/ARCHITECTURE.md` — 根因分析时可能要查
