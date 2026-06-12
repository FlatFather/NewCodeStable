<!--
本文件是所有 CodeStable skill 的"启动必读"段落权威来源。

修改本文件后，需要同步到所有 skill 的 SKILL.md（通常在第 8-10 行）。

同步命令示例：
grep -l "## 启动必读" */SKILL.md | xargs -I {} sed -i '' '8,10c\
## 启动必读\
\
开始任何判断或动作前，先读取 `.codestable/attention.md`；缺失则视为骨架不完整，提示先补齐或运行 `cs-onboard`，不要回退到外部 AI 入口文件。
' {}
-->

## 启动必读

开始任何判断或动作前，先读取 `.codestable/attention.md`；缺失则视为骨架不完整，提示先补齐或运行 `cs-onboard`，不要回退到外部 AI 入口文件。
