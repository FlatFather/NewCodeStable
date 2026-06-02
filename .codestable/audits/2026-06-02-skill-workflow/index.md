---
doc_type: audit-index
audit: 2026-06-02-skill-workflow
scope: workflow-hybridization roadmap、最近 hybrid feature 样本、共享 reference 与 cs-feat 系列 skill 的流程一致性审计
created: 2026-06-02
status: active
total_findings: 4
---

# skill-workflow 审计报告

## 范围

本次扫描聚焦 CodeStable skill 流程本身，不扫业务代码。实际读取并对照了以下范围：

- `.codestable/roadmap/workflow-hybridization/`
- `.codestable/features/2026-06-01-*` 与 `.codestable/features/2026-06-02-*` 中与 hybrid 流程相关的 design / plan / checklist / acceptance 样本
- `.codestable/reference/shared-conventions.md`
- `.codestable/reference/system-overview.md`
- `.codestable/reference/tools.md`
- `.codestable/architecture/ARCHITECTURE.md`
- `.codestable/tools/validate-yaml.py`
- `cs-feat` / `cs-feat-design` / `cs-feat-impl` 等技能说明

重点维度：`bug`、`maintainability`、`arch-drift`。

## 总评

共发现 **4** 条问题：`bug × P1` 1 条，`arch-drift × P1` 2 条，`maintainability × P2` 1 条。整体上，这条 hybrid workflow 主线已经跑通，真实样板和 `workflow-check` 也能自证；但当前体系仍有一个明显短板：**规则口径在 roadmap / reference / architecture / skill 文档之间尚未完全收敛到单一表达**。最值得优先处理的是两类问题：

1. **校验器承诺强于真实实现**——文档说会校验 step 对齐的顺序/语义，但代码只校验数量；
2. **入口技能对 hybrid 流程的描述偏松**——会让后来维护者误以为 plan 仍是“可附带”，而不是 hybrid 的硬门槛。

这两类问题如果继续累积，会让“规则存在但执行时靠人脑补”的情况再次回流。

## 发现清单

| # | 性质 | 严重度 | 置信度 | 标题 | 文件 |
|---|---|---|---|---|---|
| 1 | bug | P1 | high | workflow-check 的 step_alignment 只校验数量，未覆盖文档承诺的顺序/语义 | [finding-01.md](finding-01.md) |
| 2 | arch-drift | P1 | high | cs-feat 入口仍把 hybrid plan 说成“可附带”，与共享约定中的硬门槛冲突 | [finding-02.md](finding-02.md) |
| 3 | arch-drift | P1 | medium | `{slug}-intent.md` 已进入 feature 流程入口，但未进入共享目录契约 | [finding-03.md](finding-03.md) |
| 4 | maintainability | P2 | medium | workflow 规则在 roadmap / reference / architecture / skill 中重复定义过多，后续更新成本高 | [finding-04.md](finding-04.md) |

## 按维度分布

| 性质 | P0 | P1 | P2 | 合计 |
|---|---|---|---|---|
| bug | 0 | 1 | 0 | 1 |
| security | 0 | 0 | 0 | 0 |
| performance | 0 | 0 | 0 | 0 |
| maintainability | 0 | 0 | 1 | 1 |
| arch-drift | 0 | 2 | 0 | 2 |
| **合计** | **0** | **3** | **1** | **4** |

## 下一步建议

- **P1 本迭代修**：
  - Finding 01：先开 `cs-issue`，因为这是“校验器声明与真实行为不一致”的协议 bug。
  - Finding 02：开 `cs-refactor`，把 `cs-feat`、`system-overview`、相关入口文案统一到同一条 hybrid 门槛表达。
  - Finding 03：开 `cs-refactor`，决定 `intent.md` 是正式共享产物还是仅 design 阶段临时输入，并把共享约定补齐。
- **P2 有空再看**：
  - Finding 04：开 `cs-refactor`，收敛 workflow 规则的唯一权威出处，减少 roadmap / architecture / skills 的重复定义。

当前范围内未发现 security / performance 级别的明显问题。