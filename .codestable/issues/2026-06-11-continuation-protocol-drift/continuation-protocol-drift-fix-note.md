---
doc_type: issue-fix
issue: 2026-06-11-continuation-protocol-drift
status: completed
fixed_files: [.codestable/reference/workflow-continuation.md, .codestable/reference/shared-conventions.md]
related: [continuation-protocol-drift-report.md, continuation-protocol-drift-analysis.md]
tags: [workflow, continuation, documentation, maintainability]
---

# continuation protocol drift 修复记录

## 修复方案

采用方案 A：引入协议版本号。

## 修复内容

### 1. 修改 `.codestable/reference/workflow-continuation.md`

**位置**：文件开头

**新增 frontmatter**：
```yaml
---
protocol_version: 1.0
---
```

**理由**：明确标识当前协议版本，后续修改协议时升级版本号提醒维护者同步摘要。

### 2. 修改 `.codestable/reference/shared-conventions.md:104`

**修改前**：
```markdown
详细共享协议见 `.codestable/reference/workflow-continuation.md`，本文件只保留摘要与指针。
```

**修改后**：
```markdown
详细共享协议见 `.codestable/reference/workflow-continuation.md` (v1.0)，本文件只保留摘要与指针。
```

**理由**：引用时声明版本号，维护者看到版本号不匹配时能意识到需要同步。

## 验证结果

### 1. 复现步骤验证

- [x] workflow-continuation.md 已增加 protocol_version: 1.0
- [x] shared-conventions.md 引用时已声明版本号 (v1.0)

### 2. 期望行为验证

- [x] 版本号明确标识协议变更
- [x] 维护者修改详细协议时能看到版本号，意识到需要同步摘要
- [x] 改动范围最小，符合文档长度约束

### 3. 影响面回归

- [x] 不影响其他 skill 或功能
- [x] 纯文档修改，无行为变更
- [x] 修改范围符合 analysis 声明（workflow-continuation + shared-conventions）

## 修复方式

- 在 workflow-continuation.md 增加 protocol_version frontmatter
- 在 shared-conventions.md 引用时声明版本号
- 建立版本号同步提示机制

## 后续建议

后续修改 continuation-first 协议时：
1. 修改 `workflow-continuation.md` 内容
2. 同步升级 frontmatter `protocol_version`（如 1.0 → 1.1）
3. 同步更新 `shared-conventions.md` 引用版本号
4. 确认摘要与详细协议一致

版本号升级规则建议：
- 小改动（措辞优化、示例补充）：小版本号 +0.1（如 1.0 → 1.1）
- 大改动（适用范围变更、核心规则变更）：大版本号 +1（如 1.0 → 2.0）
