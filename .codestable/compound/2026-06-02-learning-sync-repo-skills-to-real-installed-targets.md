---
doc_type: learning
track: knowledge
date: 2026-06-02
slug: sync-repo-skills-to-real-installed-targets
component: local-skill-maintenance
tags: [skills, sync, symlink, local-dev, workflow]
---

## 背景

在本地维护 Claude skill 时，仓库里的 skill 源码与机器上实际生效的 skill 目录很容易漂移。这个问题在 `~/.claude/skills/*` 不是普通目录、而是符号链接时更隐蔽：表面上看是在改 `~/.claude/skills/...`，真实生效目录却可能落在 `~/.agents/skills/...`。

如果不先搞清楚真实目标目录，就容易出现两种错觉：

- 以为自己改的是已安装副本，其实改的是入口链接
- 以为仓库源码和本地生效内容一致，实际已经漂移

## 指导原则

统一在仓库里维护 skill 源码，再用项目内的同步脚本把改动同步到**真实生效目录**。

在这个项目里，推荐做法是：

1. 先改仓库根目录下的 skill 源码
2. 使用 `.codestable/tools/sync-skills.sh` 同步
3. 让脚本先解析 `~/.claude/skills/<slug>` 的 symlink，再写入真实目标目录
4. 同步后优先开新会话验证 skill 行为

## 为什么重要

这样做能避免两类长期维护问题：

- **双真相源**：仓库里一份、机器上生效目录又一份，最后不知道哪份才是准的
- **误判同步状态**：只看 `~/.claude/skills` 的表面路径，没看到真实目标目录，导致改动没真正落到运行时会读取的位置

把“仓库源码是权威来源、同步脚本负责下发”固定下来之后，本地 skill 的维护方式会稳定很多。

## 何时适用

适用于所有“本地已安装 skill 的真实目录可能和仓库源码分离”的场景，尤其是：

- `~/.claude/skills/<slug>` 是 symlink
- 真实 skill 文件落在别的目录（如 `~/.agents/skills/<slug>`）
- 你既在仓库里开发 skill，又要立刻在本机验证它的触发和行为

## 示例

这次的具体做法就是：

- 先在 `NewCodeStable/` 仓库里修改 `cs`、`cs-feat` 等 skill 源码
- 再用 `.codestable/tools/sync-skills.sh` 做 dry-run 和正式同步
- 脚本自动把 `~/.claude/skills/cs`、`~/.claude/skills/cs-feat` 解析到真实目录 `~/.agents/skills/...`
- 同步完成后，再开新会话验证最新 skill 是否生效
