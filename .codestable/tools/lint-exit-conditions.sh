#!/usr/bin/env bash
# Lint exit conditions format across all cs-* skills
# Ensures consistent use of Markdown checklist format: - [ ]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_ROOT="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

ERRORS=0

lint_skill() {
  local skill_path="$1"
  local skill_name="$(basename "$skill_path")"

  if [[ ! -f "$skill_path/SKILL.md" ]]; then
    return
  fi

  # Extract exit conditions section
  local exit_section
  exit_section=$(awk '/## 退出条件/,/^## / {if (!/^## / || /## 退出条件/) print}' "$skill_path/SKILL.md" | tail -n +2)

  if [[ -z "$exit_section" ]]; then
    return  # No exit conditions section, skip
  fi

  # Check format: should only contain - [ ] lines (and optional prose before them)
  local checklist_lines
  checklist_lines=$(echo "$exit_section" | grep -E "^- " || true)

  if [[ -z "$checklist_lines" ]]; then
    echo "✗ $skill_name: No checklist items found in 退出条件 section" >&2
    ((ERRORS++))
    return
  fi

  # All checklist lines should be - [ ] format
  local bad_lines
  bad_lines=$(echo "$checklist_lines" | grep -v "^- \[ \]" || true)

  if [[ -n "$bad_lines" ]]; then
    echo "✗ $skill_name: Non-standard checklist format:" >&2
    echo "$bad_lines" | sed 's/^/    /' >&2
    ((ERRORS++))
    return
  fi

  echo "✓ $skill_name"
}

# Find all cs-* skills
for skill_dir in "$SKILLS_ROOT"/cs-*; do
  if [[ -d "$skill_dir" ]]; then
    lint_skill "$skill_dir"
  fi
done

if [[ $ERRORS -gt 0 ]]; then
  echo "" >&2
  echo "Found $ERRORS skill(s) with format issues." >&2
  exit 1
else
  echo ""
  echo "All skills use consistent exit condition format."
  exit 0
fi
