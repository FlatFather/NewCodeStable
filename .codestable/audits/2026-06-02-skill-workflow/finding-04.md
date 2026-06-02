---
doc_type: audit-finding
audit: 2026-06-02-skill-workflow
finding_id: "maintainability-04"
nature: maintainability
severity: P2
confidence: medium
suggested_action: cs-refactor
status: open
---

# Finding 04：workflow 规则在 roadmap / reference / architecture / skill 中重复定义过多，后续更新成本高

## 速答

当前 hybrid workflow 的关键规则同时分散在 roadmap、shared conventions、architecture、tools、skills、feature acceptance 样板中。信息是丰富了，但也形成了明显的“多处重复定义”结构，后续每改一条规则都要手动追很多落点。

## 关键证据

- `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md:75` 到 `.codestable/roadmap/workflow-hybridization/workflow-hybridization-roadmap.md:95` — roadmap 自己完整定义了 design / plan / checklist / acceptance 的职责边界。
- `.codestable/reference/shared-conventions.md:113` 到 `.codestable/reference/shared-conventions.md:129` — shared conventions 再次定义同一组职责边界，并补了 plan presence rule。
- `.codestable/architecture/ARCHITECTURE.md:12` 到 `.codestable/architecture/ARCHITECTURE.md:19` — architecture 继续以术语表形式重复定义 feature-plan / hybrid feature / workflow-check。
- `/Users/kong/.claude/skills/cs-feat-impl/SKILL.md:76` 到 `/Users/kong/.claude/skills/cs-feat-impl/SKILL.md:79` — implement 技能再次在正文里重述 legacy / hybrid / plan / checklist 的关系。
- `.codestable/reference/maintainer-notes.md:48` 到 `.codestable/reference/maintainer-notes.md:50` — 维护规则已经承认“每次扩展都要同步更新 system-overview 和相关子技能”，说明当前模型本身依赖多处手动同步。

## 影响

这不是立即会把流程跑坏的问题，但会显著增加未来修改成本。任何一条规则（例如 workflow-check 能力边界、hybrid 的必备产物、前置输入种类）发生变化，都容易出现“主约定已改，入口技能没改；技能改了，样板没改；样板改了，architecture 还留旧话术”的滞后链。

## 修复方向

收敛“规则原文”的唯一权威出处。建议让：
- `shared-conventions.md` 负责协议正文；
- `architecture/ARCHITECTURE.md` 只保留稳定术语和结构事实；
- `skills` 只保留阶段动作与链接，不重复展开完整协议；
- `roadmap` 在已落地后减少继续充当长期协议文档的职责。

## 建议动作

`cs-refactor`，因为这是流程文档架构层面的减重和去重复，不是单个缺陷修补。