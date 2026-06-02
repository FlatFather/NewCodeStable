# migration guidance samples

## 1. 历史 feature 保持原样

适用：只是查阅、归档、参考，不继续推进实现。

- 不补 `workflow`
- 不补 `plan.md`
- 不运行 workflow-check 作为强制门槛

## 2. 历史 feature 重开并继续 legacy

适用：要继续推进，但不升级到 hybrid。

最小补写：
- 在 design frontmatter 补 `workflow: legacy`
- 保持 `design + checklist + acceptance`
- 不要求新增 `plan.md`

## 3. 历史 feature 重开并升级 hybrid

适用：要继续推进，且需要详细执行计划正文。

最小补写：
- 在 design frontmatter 补 `workflow: hybrid`
- 同目录新增真实 `plan.md`
- checklist 继续作为状态载体
- 之后 implement / acceptance 都按 hybrid 口径读取 plan
