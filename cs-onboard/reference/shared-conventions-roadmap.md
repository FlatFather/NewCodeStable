# CodeStable 共享口径 — Roadmap

本模块定义 roadmap ↔ feature 衔接协议。

其他模块：
- `shared-conventions-core.md` — 目录结构与命名规则
- `shared-conventions-feature.md` — feature 产物职责边界
- `shared-conventions-checklist.md` — checklist 生命周期

---

## 2.5 roadmap ↔ feature 衔接协议

`.codestable/roadmap/{slug}/{slug}-items.yaml` 是规划层和 feature 执行层的唯一接口。三个技能共同读写它——是 skill 都读写项目共享产物，不算耦合。

**items.yaml 状态机**：

```
planned  → in-progress  （cs-feat-design 启动 feature 时改）
in-progress → done      （cs-feat-accept 验收完成时改）
planned  → dropped      （cs-roadmap update 模式，用户决定不做时改）
```

`done` / `dropped` 是终态。需要回退重做的新加一条 slug 略改的条目，不改终态。

**cs-roadmap 的职责**：生成和维护 roadmap 主文档 + items.yaml；把 `planned` 改 `dropped`（用户放弃时）；不改 `in-progress` / `done`（feature 技能负责）。

**cs-feat-design 的职责**（从 roadmap 起头时）：

1. design.md frontmatter 加 `roadmap: {roadmap-slug}` + `roadmap_item: {子 feature slug}`
2. 写入并固定 `feature: YYYY-MM-DD-{slug}` 目录名，作为跨 design / plan / checklist / acceptance / items.yaml 的唯一绑定键
3. items.yaml 对应条目 `status: in-progress` + `feature: YYYY-MM-DD-{slug}`
4. 若 design 判定该 feature 采用 hybrid 口径：后续产物中必须存在 `{slug}-plan.md`，但**plan 不单独写 roadmap 状态**
5. 校验 yaml

直接起 feature（非 roadmap 来）两字段留空，不触发 roadmap 写。

**cs-feat-accept 的职责**：

1. 读 design frontmatter `roadmap` / `roadmap_item`
2. 空 → 跳过
3. 有值 → 先核对绑定关系：`design.feature = items.yaml.feature`；hybrid feature 还要核对 `plan.feature = design.feature`
4. 绑定一致后，把 items.yaml 对应条目 `status: done`；同步主文档子 feature 清单显示状态
5. 校验 yaml

回写是**实际写文件的动作**，验收报告要明确记录回写结果。

**最小闭环标记**：items.yaml 每份只有一条 `minimal_loop: true`，标记"做完后系统能端到端跑通最窄路径"。design 启动 `minimal_loop` 条目时优先级最高。
