---
doc_type: audit-finding
audit: 2026-06-11-skill-workflow
finding_id: "12"
nature: bug
severity: P2
confidence: medium
title: cs-feat-accept 第 8 节 attention.md 候选盘点规则未在 cs-feat-ff 中同步
status: fixed
fixed_by: inline
fixed_date: 2026-06-18
tags: [cs-feat-accept, cs-feat-ff, attention-md, rule-sync]
---

# Finding-12: attention.md 候选盘点规则未在 cs-feat-ff 同步

## 问题描述

`cs-feat-accept` 第 8 节定义了"attention.md 候选盘点"规则，用于识别"每个 feature 都会撞一次"的环境/工具信息。但 `cs-feat-ff` 作为独立快路径，未同步此规则。

## 证据

**cs-feat-accept/SKILL.md:189-198（第 8 节）**
> 回看本次实现，盘点"每个 feature 都会撞一次"的环境/工具/工作流类信息...

**cs-feat-ff 未读取**，但根据其定位（超轻量通道），推测未包含此盘点环节

## 为什么构成 P2

- fastforward 跳过详细验收，但仍可能暴露环境/工具坑点
- 未盘点 → 下次 feature 可能重复踩坑

## 建议修复方案

**方案 A：cs-feat-ff 增加轻量盘点**
- 在 ff 收尾时增加一句话提示："发现需要记到 attention.md 的吗？"

**方案 B：保持现状**
- fastforward 本就是跳过完整验收，盘点也可跳过

## 建议动作

走 **`cs-issue`** 流程（规则同步或明确豁免）。
