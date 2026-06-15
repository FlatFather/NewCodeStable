---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "13"
nature: security
severity: P2
confidence: low
title: sync-skills.sh 使用 rsync --delete，目标目录误配置时存在删除风险
status: open
tags: [security, sync-skills, rsync, deletion-risk]
---

# Finding-13: sync-skills.sh 使用 rsync --delete 存在删除风险

## 问题描述

`.codestable/tools/sync-skills.sh` 使用 `rsync -a --delete` 同步 skill，若目标目录误配置（如 `CLAUDE_SKILLS_DIR` 被设为 `/`），存在意外删除风险。

## 证据

**sync-skills.sh:101**
```bash
rsync -a --delete "$src_dir/" "$dest_dir/"
```

**风险场景**：
- 用户误设 `CLAUDE_SKILLS_DIR=/tmp/important-files`
- rsync --delete 会删除 `/tmp/important-files` 中不在源目录的所有文件

## 为什么构成 P2

- 正常使用场景下，目标目录是 `~/.claude/skills/` 或 `~/.agents/skills/`，风险低
- 但误配置时后果严重（数据丢失）
- 脚本已有 `--dry-run` 模式，但非强制预演

## 建议修复方案

**方案 A：目标路径白名单**
- 限制 `CLAUDE_SKILLS_DIR` 只能是已知安全路径（`~/.claude/skills`, `~/.agents/skills`）

**方案 B：强制 --dry-run 预演**
- 首次运行或目标变更时强制 dry-run，让用户确认

**方案 C：增加确认提示**
- 在 rsync 前打印 `src → dest`，让用户确认

## 建议动作

走 **`cs-issue`** 流程（增加安全防护）。
