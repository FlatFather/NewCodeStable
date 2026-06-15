# 步骤 3：缓存判断逻辑模板

## 标准模板（适用于大多数技能）

```markdown
## 启动必读

本技能启动前需读取：
- `.codestable/attention.md` — 项目注意事项
- `.codestable/reference/shared-conventions.md` — 跨技能共享口径

**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。
```

## 按需引用模块的技能

### 引用 core 的技能（8 个）

```markdown
## 启动必读

本技能启动前需读取：
- `.codestable/attention.md` — 项目注意事项
- `.codestable/reference/shared-conventions-core.md` — 目录结构与命名规则

**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。
```

**适用技能**：cs-arch, cs-feat-accept, cs-feat-design, cs-feat-impl, cs-feat-plan, cs-issue-analyze, cs-issue-fix, cs-issue-report

### 引用 feature 的技能（3 个）

cs-feat-design, cs-feat-plan 需要组合多个模块，单独处理。

### cs-feat（引用 feature）

```markdown
## 启动必读

本技能启动前需读取：
- `.codestable/attention.md` — 项目注意事项
- `.codestable/reference/shared-conventions-feature.md` — feature 产物职责边界

**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。
```

### cs-feat-design（引用 core + feature + roadmap）

```markdown
## 启动必读

本技能启动前需读取：
- `.codestable/attention.md` — 项目注意事项
- `.codestable/reference/shared-conventions-core.md` — 目录结构与命名规则
- `.codestable/reference/shared-conventions-feature.md` — feature 产物职责边界
- `.codestable/reference/shared-conventions-roadmap.md` — roadmap ↔ feature 衔接（从 roadmap 起头时）

**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。
```

### cs-feat-plan（引用 core + feature + checklist）

```markdown
## 启动必读

本技能启动前需读取：
- `.codestable/attention.md` — 项目注意事项
- `.codestable/reference/shared-conventions-core.md` — 目录结构与命名规则
- `.codestable/reference/shared-conventions-feature.md` — feature 产物职责边界
- `.codestable/reference/shared-conventions-checklist.md` — checklist 生命周期

**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。
```

### cs-feat-accept（引用 core + feature + roadmap + 主文件）

```markdown
## 启动必读

本技能启动前需读取：
- `.codestable/attention.md` — 项目注意事项
- `.codestable/reference/shared-conventions-core.md` — 目录结构与命名规则
- `.codestable/reference/shared-conventions-feature.md` — feature 产物职责边界
- `.codestable/reference/shared-conventions-roadmap.md` — roadmap ↔ feature 衔接
- `.codestable/reference/shared-conventions.md` — 收尾推荐与提交规则

**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。

**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。
```

## 引用主文件的技能（通用版本）

大多数其他技能引用主文件（第 1, 3-7 节），使用标准模板即可。
