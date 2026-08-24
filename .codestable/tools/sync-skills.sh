#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEST_ROOT="${CLAUDE_SKILLS_DIR:-}"
TARGET="${SKILLS_TARGET:-agents}"
DRY_RUN=0
VERIFY_ONLY=0

# Safety: whitelist of allowed destination roots — ONLY agents now
ALLOWED_DESTS=(
  "$HOME/.agents/skills"
)

check_dest_allowed() {
  local dest="$1"
  local allowed
  for allowed in "${ALLOWED_DESTS[@]}"; do
    if [[ "$dest" == "$allowed" || "$dest" == "$allowed/"* ]]; then
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
  sync-skills.sh [--target agents] [--dry-run|--verify] [skill-name ...]

Examples:
  sync-skills.sh --dry-run
  sync-skills.sh --dry-run cs cs-feat cs-feat-design
  sync-skills.sh cs-feat

Safety:
  - Logical target must be agents (fixed)
  - Physical destination root must be exactly ~/.agents/skills (or a child skill path)
  - Use --dry-run first to preview changes before applying
  - Use --verify to check installed-copy drift without writing

Behavior:
  - Scans the repository root for top-level skill directories containing SKILL.md
  - Syncs each selected skill to ~/.agents/skills/<skill-name>
  - If the destination is a symlink, resolves the real target directory first
  - Uses rsync --delete so destination matches source exactly
  - --verify exits 1 when a selected installed copy is missing or differs
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
    --verify)
      VERIFY_ONLY=1
      shift
      ;;
    --target)
      [[ $# -ge 2 ]] || { echo "ERROR: --target requires a value" >&2; exit 2; }
      TARGET="$2"
      shift 2
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

if [[ $DRY_RUN -eq 1 && $VERIFY_ONLY -eq 1 ]]; then
  echo "ERROR: --dry-run and --verify cannot be used together" >&2
  exit 2
fi

case "$TARGET" in
  agents) TARGET_ROOTS=("${DEST_ROOT:-$HOME/.agents/skills}") ;;
  *) echo "ERROR: --target must be agents (fixed)" >&2; exit 2 ;;
esac

for root in "${TARGET_ROOTS[@]}"; do
  check_dest_allowed "$root"
done

case "$(uname -s)" in
  Darwin|Linux) ;;
  *) echo "ERROR: sync-skills.sh supports macOS/Linux/WSL; use WSL on Windows" >&2; exit 4 ;;
esac
command -v rsync >/dev/null 2>&1 || { echo "ERROR: rsync is required" >&2; exit 4; }

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
DRIFT_COUNT=0
for skill_file in "${SKILL_FILES[@]}"; do
  src_dir="$(dirname "$skill_file")"
  slug="$(basename "$src_dir")"

  if ! matches_selected "$slug"; then
    continue
  fi

  for logical_root in "${TARGET_ROOTS[@]}"; do
    dest_link="$logical_root/$slug"
    if [[ -e "$dest_link" || -L "$dest_link" ]]; then
      dest_dir="$(resolve_dest "$dest_link")"
    else
      dest_dir="$dest_link"
    fi

    if [[ $VERIFY_ONLY -eq 0 ]]; then
      mkdir -p "$dest_dir"
    fi

    echo "== $slug =="
    echo "source: $src_dir/"
    echo "logical target: $dest_link/"
    echo "physical target: $dest_dir/"

    if [[ $VERIFY_ONLY -eq 1 ]]; then
      if [[ ! -d "$dest_dir" ]]; then
        echo "DRIFT: installed skill is missing"
        DRIFT_COUNT=$((DRIFT_COUNT + 1))
      else
        diff=$(rsync -rnic --delete "$src_dir/" "$dest_dir/")
        if [[ -n "$diff" ]]; then
          echo "DRIFT:"
          printf '%s\n' "$diff"
          DRIFT_COUNT=$((DRIFT_COUNT + 1))
        else
          echo "OK: installed copy matches source"
        fi
      fi
    elif [[ $DRY_RUN -eq 1 ]]; then
      rsync -an --delete "$src_dir/" "$dest_dir/"
    else
      rsync -a --delete "$src_dir/" "$dest_dir/"
    fi

    SYNC_COUNT=$((SYNC_COUNT + 1))
    echo
  done

done

if [[ $SYNC_COUNT -eq 0 ]]; then
  echo "No matching skills selected." >&2
  exit 2
fi

if [[ $VERIFY_ONLY -eq 1 ]]; then
  if [[ $DRIFT_COUNT -gt 0 ]]; then
    echo "Verification failed: $DRIFT_COUNT of $SYNC_COUNT skill(s) drifted." >&2
    exit 1
  fi
  echo "Verification complete: $SYNC_COUNT skill(s) match installed copies."
elif [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run complete: $SYNC_COUNT skill(s) checked."
else
  echo "Sync complete: $SYNC_COUNT skill(s) updated."
fi
