# feature-design frontmatter 与节锚点

## 1. {slug}-design.md frontmatter

```markdown
---
doc_type: feature-design
feature: 2026-04-12-user-auth
requirement: user-auth-email
workflow: hybrid                    # 标准 feature 默认走 hybrid；历史 legacy 目录仅兼容读取
roadmap: permission-system           # 可选：本 feature 从某 roadmap 条目起头时填
roadmap_item: permission-rbac-core   # 可选：对应 roadmap items.yaml 里的 slug
status: draft
summary: 支持用户通过邮箱验证码登录后台
tags: [auth, email, login]
---
```

必填：`doc_type` / `feature` / `status` / `summary` / `tags`。

- `requirement`：填对应 req 的 slug；纯重构 / 技术债允许留空
- `roadmap` / `roadmap_item`：从 roadmap 条目起头时才填，两个一起填或一起空

## 2. 顶层节锚点

- `## 0. 术语约定`
- `## 1. 决策与约束`
- `## 1.5. 复用与扩展策略` ← **新增**，基于启动检查第 3 步的复用清单
- `## 2. 名词与编排` ← design 的灵魂，是 implement 的主输入
  - `### 2.1 名词层`
  - `### 2.2 编排层`
  - `### 2.3 挂载点清单`
  - `### 2.4 推进策略`
  - `### 2.5 结构健康度与微重构` ← 固定节，结论二选一 + 可选"超出范围的观察"
- `## 3. 验收契约`
- `## 4. 与项目级架构文档的关系`

