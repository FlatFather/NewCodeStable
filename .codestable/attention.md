# Attention

本文件是 CodeStable 技能启动必读的项目注意事项入口。所有 CodeStable 子技能开始工作前必须读取它。

## 项目碎片知识

<!-- cs-note managed: 用 cs-note 维护，新条目按下面分节追加 -->

### 编译与构建

### 运行与本地起服务

### 测试

### 命令与脚本陷阱

- 运行 `.codestable/tools/*.py` 时优先使用 `.venv/bin/python`，因为本项目已在 `.venv` 中安装 `PyYAML`，系统 Python 可能只会走 fallback parser。
### 路径与目录约定

- 本地 `~/.claude/skills/*` 可能是 symlink，真实生效目录常在 `~/.agents/skills/*`；更新 skill 时优先改仓库源码，再用 `.codestable/tools/sync-skills.sh` 同步并开新会话验证。

### 环境变量与凭证

### 其他
