#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEST_ROOT="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
DRY_RUN=0

# Safety: whitelist of allowed destination roots
ALLOWED_DESTS=(
  "$HOME/.claude/skills"
  "$HOME/.agents/skills"
)

check_dest_allowed() {
  local dest="$1"
  local allowed
  for allowed in "${ALLOWED_DESTS[@]}"; do
    if [[ "$dest" == "$allowed"* ]]; then
      return 0
    fi
  done
  echo "ERROR: Destination '$dest' is not in the allowed whitelist:" >&2
  printf "  %s\n" "${ALLOWED_DESTS[@]}" >&2
  exit 3
}

usage() {
  cat <<'EOF'
Usage:
  sync-skills.sh [--dry-run] [skill-name ...]

Examples:
  sync-skills.sh --dry-run
  sync-skills.sh --dry-run cs cs-feat cs-feat-design
  sync-skills.sh cs-feat
  CLAUDE_SKILLS_DIR=$HOME/.claude/skills sync-skills.sh cs-feat

Safety:
  - Destination root must be in the whitelist: ~/.claude/skills or ~/.agents/skills
  - Use --dry-run first to preview changes before applying

Behavior:
  - Scans the repository root for top-level skill directories containing SKILL.md
  - Syncs each selected skill to ~/.claude/skills/<skill-name>
  - If the destination is a symlink, resolves the real target directory first
  - Uses rsync --delete so destination matches source exactly
EOF
}

resolve_dest() {
  python3 - <<'PY' "$1"
import os, sys
print(os.path.realpath(sys.argv[1]))
PY
}

SELECTED=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      SELECTED+=("$1")
      shift
      ;;
  esac
done

# Safety check: validate destination root is in whitelist
check_dest_allowed "$DEST_ROOT"

matches_selected() {
  local slug="$1"
  if [[ ${#SELECTED[@]} -eq 0 ]]; then
    return 0
  fi
  local picked
  for picked in "${SELECTED[@]}"; do
    if [[ "$picked" == "$slug" ]]; then
      return 0
    fi
  done
  return 1
}

SKILL_FILES=()
while IFS= read -r skill_file; do
  SKILL_FILES+=("$skill_file")
done < <(find "$REPO_ROOT" -mindepth 2 -maxdepth 2 -name SKILL.md | sort)

if [[ ${#SKILL_FILES[@]} -eq 0 ]]; then
  echo "No skill sources found under $REPO_ROOT" >&2
  exit 1
fi

SYNC_COUNT=0
for skill_file in "${SKILL_FILES[@]}"; do
  src_dir="$(dirname "$skill_file")"
  slug="$(basename "$src_dir")"

  if ! matches_selected "$slug"; then
    continue
  fi

  dest_link="$DEST_ROOT/$slug"
  if [[ -e "$dest_link" || -L "$dest_link" ]]; then
    dest_dir="$(resolve_dest "$dest_link")"
  else
    dest_dir="$dest_link"
  fi

  mkdir -p "$dest_dir"

  echo "== $slug =="
  echo "source: $src_dir/"
  echo "target: $dest_dir/"

  if [[ $DRY_RUN -eq 1 ]]; then
    rsync -an --delete "$src_dir/" "$dest_dir/"
  else
    rsync -a --delete "$src_dir/" "$dest_dir/"
  fi

  SYNC_COUNT=$((SYNC_COUNT + 1))
  echo

done

if [[ $SYNC_COUNT -eq 0 ]]; then
  echo "No matching skills selected." >&2
  exit 2
fi

if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run complete: $SYNC_COUNT skill(s) checked."
else
  echo "Sync complete: $SYNC_COUNT skill(s) updated."
fi
