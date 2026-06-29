# CodeStable 共享口径 — Core

本模块定义目录结构与命名规则。

其他模块：
- `shared-conventions-feature.md` — feature 产物职责边界
- `shared-conventions-checklist.md` — checklist 生命周期
- `shared-conventions-roadmap.md` — roadmap ↔ feature 衔接

---

## 0. 目录结构与路径命名

onboard 完成后骨架（`cs-onboard` 负责搭建）：

```
.codestable/
├── attention.md           CodeStable 技能启动必读的项目注意事项
├── requirements/          能力愿景层（"用户需要什么、系统提供什么能力来满足"，过去/现在/未来）
│   ├── VISION.md           中心索引（按 status 分组，每条带 pitch 一句话）
│   └── {slug}.md           一个能力一份，扁平（cs-req 产出）
├── architecture/          架构中心目录（"用什么结构实现"，只记现状）
│   ├── ARCHITECTURE.md    总入口（索引 + 关键架构决定）
│   └── {type}-{slug}.md   子系统 / 模块 doc（cs-arch 产出）
├── roadmap/               规划层（"接下来怎么做这块大需求 + 模块怎么切 + 接口怎么定"）
│   └── {slug}/            一个大需求一个子目录（cs-roadmap 产出）
│       ├── {slug}-roadmap.md   主文档：背景 / 范围 / 模块拆分 / 接口契约 / 子 feature 清单 / 排期
│       ├── {slug}-items.yaml   机器可读子 feature 清单，acceptance 回写状态
│       └── drafts/             可选
├── features/              feature spec 聚合根
│   └── YYYY-MM-DD-{slug}/  每个 feature 一个目录
│       ├── {slug}-brainstorm.md  （可选，case 2 时产出）
│       ├── {slug}-intent.md      （可选，design 前置草稿；初始化模式产出）
│       ├── {slug}-design.md      （标准 / hybrid；范围与约束唯一方案源）
│       ├── {slug}-plan.md        （hybrid 可选；详细执行步骤正文）
│       ├── {slug}-checklist.yaml （标准 / hybrid；机器可读状态载体）
│       ├── {slug}-acceptance.md  （标准 / hybrid；验收与回写）
│       └── {slug}-ff-note.md     （fastforward 通道唯一产物，与上面诸项互斥）
├── issues/                issue spec 聚合根
│   └── YYYY-MM-DD-{slug}/
│       ├── {slug}-report.md
│       ├── {slug}-analysis.md   （根因不显然才有）
│       └── {slug}-fix-note.md
├── refactors/             refactor spec 聚合根
│   └── YYYY-MM-DD-{slug}/
│       ├── {slug}-scan.md
│       ├── {slug}-refactor-design.md
│       ├── {slug}-checklist.yaml
│       └── {slug}-apply-notes.md
├── compound/              沉淀类文档统一目录
│   └── YYYY-MM-DD-{doc_type}-{slug}.md
│                          doc_type ∈ {learning, trick, decision, explore}
├── brainstorm/            brainstorm 阶段 spike 实验代码区（cs-brainstorm 临时产出）
│   └── {slug}/            一次 spike 一个子目录，文件名随意
│                          验完不强制清理，结论回写到对应 brainstorm note
├── tools/                 跨工作流共享脚本（onboard 从技能包释放）
└── reference/             共享参考文档（onboard 从技能包释放）
```

### 命名规则

- 需求文档：`requirements/{slug}.md`（能力愿景，不带日期前缀，扁平不分组）；中心索引 `requirements/VISION.md`
- roadmap：`roadmap/{slug}/`（不带日期前缀，平铺不嵌套）
- feature / issue / refactor 目录：带日期前缀 `YYYY-MM-DD-{slug}`
- 沉淀类：`compound/YYYY-MM-DD-{doc_type}-{slug}.md`，日期用**归档当天**
- 架构 doc：`architecture/{type}-{slug}.md`（长效，不带日期前缀）；总入口固定 `ARCHITECTURE.md`
- 项目注意事项入口固定为 `.codestable/attention.md`，所有 CodeStable 子技能启动前必须读取；不再兼容 `AGENTS.md` / `CLAUDE.md` 等外部入口

### 架构 doc 分组规则（同类聚合）

`architecture/` 下用文件名第一段作 type 标记：`ui-chat.md` 和 `ui-events.md` 同 `ui` 类。**所有架构 doc 必须 `{type}-{slug}.md`**——只有一份的也要带合理 type 段（如 `cli-entry.md`），否则未来同类出现时聚合不了。

**触发**：某 type 在 `architecture/` 根目录达到 ≥6 份时（即新加第 6 份那次），把这一类全部收进同名子目录。

**收入后**：去掉 type 前缀。`ui-chat.md` → `ui/chat.md`。

**只升不降**：删到 ≤5 份也不折回平铺。

**触发时谁负责**：`cs-arch` 的 `backfill` / `update` 模式在 Phase 6 落盘前主动检查并搬迁；命中阈值时这次操作要把"本次新加 / 改的 + 已有同类全部"一起搬，并同步改 `ARCHITECTURE.md` 链接（搬迁本身要在 Phase 5 给用户 review，不偷偷做）。`check` 模式不主动搬迁，但发现 ≥6 仍平铺时在报告末尾列为观察项。

### 改目录结构

改 `cs-onboard/reference/shared-conventions.md` 模板，新项目 onboard 时带上新版本；已有项目手动同步 `.codestable/reference/shared-conventions.md`。
