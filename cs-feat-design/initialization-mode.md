# cs-feat-design 初始化模式

本文件承接 `SKILL.md` 的初始化模式入口，说明如何帮用户建立 feature 目录和 `{slug}-intent.md` 前置草稿。

## 初始化模式：帮用户建目录和 intent 前置草稿

触发：用户想自己写一份半成品方案（`{slug}-intent.md`）作为后续 design 的输入，但不想手动建目录。

动作：

1. **和用户快速对齐两件事**——一句话需求概要 + 敲定 slug（小写字母、数字、连字符；`user-auth`、`export-csv` 这种）。日期取当天（frontmatter 用 `currentDate` 即可）。feature 目录命名是 `YYYY-MM-DD-{slug}`。
2. **创建 `.codestable/features/{YYYY-MM-DD}-{slug}/` 目录**。
3. **写一份空的 `{slug}-intent.md`** 作为草稿骨架，内容就是下面这段：

   ```markdown
   ---
   doc_type: feature-intent
   feature: {YYYY-MM-DD}-{slug}
   status: draft
   summary: {一句话需求，AI 按和用户对齐的结果填}
   ---

   # {slug} intent

   ## 背景 / 为什么做

   （一句话就够）

   ## 大致怎么做

   （100 字左右描述想法，含关键步骤 / 数据流）

   ## 相关数据结构 / 类型

   （贴相关 types、接口签名、或指向代码位置）

   ## 已知不做 / 待定

   （可选：明确的边界或自己也没想清楚的地方）
   ```

4. **告知用户"骨架已建好，填完后再来找我，我基于 intent 写正式 design"**，然后**本轮结束，不继续推进 design 流程**。

为什么在这里停？intent 的价值就是让用户离线思考、把脑子里的东西落到纸面。AI 继续问会把 intent 模式退化成 brainstorm，失去意义。

---
