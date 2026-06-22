#!/usr/bin/env python3
"""
自动注入"启动必读"段落的缓存优化和检查规则模板。

用法：
  python inject-startup-boilerplate.py --check     # 检查哪些技能需要更新
  python inject-startup-boilerplate.py --apply     # 应用更新
  python inject-startup-boilerplate.py --validate  # 验证所有技能一致性
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# 标准模板
CACHE_OPTIMIZATION = """
**缓存优化**：上述文件若已在本轮对话中读取过，输出"已复用上下文"并跳过 Read；否则执行 Read。
""".strip()

CHECK_RULE = """
**检查规则**：attention.md 缺失时，提示先补齐或运行 `cs-onboard`。
""".strip()


def find_skill_files(repo_root: Path) -> List[Path]:
    """查找所有 cs-*/SKILL.md 文件"""
    return sorted(repo_root.glob("cs-*/SKILL.md"))


def extract_startup_section(content: str) -> Tuple[str, str, str]:
    """
    提取启动必读段落的三部分：
    1. 文件列表（到第一个 **）
    2. 缓存优化（**缓存优化** 到下一个 **）
    3. 检查规则（**检查规则** 到下一个 ##）

    返回: (file_list, cache_opt, check_rule)
    """
    match = re.search(
        r'## 启动必读\n\n(本技能启动前需读取：\n(?:- `.+`.*\n)+)\n'
        r'(\*\*缓存优化\*\*：.+?)\n\n'
        r'(\*\*检查规则\*\*：.+?)\n\n',
        content,
        re.DOTALL
    )

    if not match:
        return None, None, None

    return match.group(1), match.group(2), match.group(3)


def check_consistency(skill_file: Path) -> bool:
    """检查一个技能文件的缓存优化和检查规则是否一致"""
    # 特殊技能跳过
    skill_name = skill_file.parent.name
    if skill_name in ['cs-onboard', 'cs-note']:
        # cs-onboard 是初始化工具，cs-note 管理 attention.md
        return True

    content = skill_file.read_text(encoding='utf-8')
    file_list, cache_opt, check_rule = extract_startup_section(content)

    if not cache_opt or not check_rule:
        print(f"❌ {skill_name}: 未找到标准格式的启动必读段落")
        return False

    # 标准化比较（去除多余空格和换行）
    cache_ok = ' '.join(cache_opt.strip().split()) == ' '.join(CACHE_OPTIMIZATION.split())
    check_ok = ' '.join(check_rule.strip().split()) == ' '.join(CHECK_RULE.split())

    if not cache_ok or not check_ok:
        print(f"⚠️  {skill_name}: 缓存优化={cache_ok}, 检查规则={check_ok}")
        if not cache_ok:
            print(f"   期望: {' '.join(CACHE_OPTIMIZATION.split())[:60]}...")
            print(f"   实际: {' '.join(cache_opt.strip().split())[:60]}...")
        return False

    return True


def apply_fix(skill_file: Path, dry_run: bool = True) -> bool:
    """应用标准模板修复"""
    skill_name = skill_file.parent.name

    # 特殊技能跳过
    if skill_name in ['cs-onboard', 'cs-note']:
        return False

    content = skill_file.read_text(encoding='utf-8')
    file_list, cache_opt, check_rule = extract_startup_section(content)

    if not file_list:
        print(f"⏭️  {skill_name}: 跳过（未找到标准格式）")
        return False

    # 构造新的启动必读段落
    new_section = f"## 启动必读\n\n{file_list}\n{CACHE_OPTIMIZATION}\n\n{CHECK_RULE}\n\n"

    # 替换
    new_content = re.sub(
        r'## 启动必读\n\n.+?\n\n(?=##|\Z)',
        new_section,
        content,
        count=1,
        flags=re.DOTALL
    )

    if dry_run:
        print(f"✓ {skill_file.parent.name}: 将更新")
        return True
    else:
        skill_file.write_text(new_content, encoding='utf-8')
        print(f"✅ {skill_file.parent.name}: 已更新")
        return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    mode = sys.argv[1]
    repo_root = Path(__file__).parent.parent.parent
    skill_files = find_skill_files(repo_root)

    print(f"找到 {len(skill_files)} 个技能文件\n")

    if mode == "--check":
        need_fix = []
        for skill_file in skill_files:
            if not check_consistency(skill_file):
                need_fix.append(skill_file)

        if need_fix:
            print(f"\n需要更新的技能: {len(need_fix)}/{len(skill_files)}")
        else:
            print("\n✅ 所有技能已一致")

    elif mode == "--apply":
        updated = 0
        for skill_file in skill_files:
            if apply_fix(skill_file, dry_run=False):
                updated += 1

        print(f"\n✅ 已更新 {updated} 个技能")

    elif mode == "--validate":
        all_ok = True
        for skill_file in skill_files:
            if not check_consistency(skill_file):
                all_ok = False

        if all_ok:
            print("\n✅ 所有技能已一致")
            sys.exit(0)
        else:
            print("\n❌ 存在不一致的技能")
            sys.exit(1)

    else:
        print(f"未知模式: {mode}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
