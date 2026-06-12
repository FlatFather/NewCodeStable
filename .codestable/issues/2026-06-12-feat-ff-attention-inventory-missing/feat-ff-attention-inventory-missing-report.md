---
doc_type: issue-report
issue: 2026-06-12-feat-ff-attention-inventory-missing
status: confirmed
severity: P2
summary: cs-feat-ff 收尾推荐未包含 attention.md 候选盘点规则，可能遗漏环境坑点记录
tags: [workflow, cs-feat-ff, attention-md, rule-sync]
source_audit: .codestable/audits/2026-06-11-skill-workflow/finding-12.md
---

# feat ff attention inventory missing Issue Report

## 1. 问题现象

`cs-feat-accept/SKILL.md:189-198` 定义了"第 8 节 attention.md 候选盘点"规则，用于识别"每个 feature 都会撞一次"的环境 / 工具 / 工作流类信息（编译命令、代理配置、环境坑等）。

`cs-feat-ff/SKILL.md:183-187` 收尾推荐中只包含：
1. 沉淀 learning
2. 归档 decision
3. 代为 scoped-commit

**未包含 attention.md 候选盘点**，导致走 fastforward 路径时可能遗漏环境坑点记录。

## 2. 复现步骤

1. 阅读 `cs-feat-accept/SKILL.md:189-198`
2. 看到"第 8 节 attention.md 候选盘点"规则
3. 阅读 `cs-feat-ff/SKILL.md:183-187`
4. 观察到：收尾推荐只有 learning / decision / commit，无 attention.md 盘点提示

复现频率：稳定（文档状态）

## 3. 期望 vs 实际

**期望行为**：cs-feat-ff 收尾推荐中包含 attention.md 候选盘点提示，与 cs-feat-accept 保持一致（即使是轻量提示）

**实际行为**：cs-feat-ff 收尾推荐中完全没有 attention.md 盘点环节

## 4. 环境信息

- 涉及模块 / 功能：feature workflow 收尾环节，attention.md 候选盘点机制
- 相关文件 / 函数：
  - `cs-feat-accept/SKILL.md:189-198`（定义盘点规则）
  - `cs-feat-ff/SKILL.md:183-187`（收尾推荐，缺失盘点）
- 运行环境：文档规则层面
- 其他上下文：审计 finding-12 指出此问题

## 5. 严重程度

**P2** — fastforward 本身是跳过详细验收的轻量通道，但环境坑点仍可能暴露。未盘点会导致下次 feature 可能重复踩坑，属于规则补全优化

## 备注

来源：`.codestable/audits/2026-06-11-skill-workflow/finding-12.md`

建议修复方向：在 cs-feat-ff 收尾推荐中增加轻量 attention.md 盘点提示（一句话提示："发现需要记到 attention.md 的环境坑吗？"）
