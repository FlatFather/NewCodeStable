#!/usr/bin/env bash
# Bounded preflight for optional external-model collaborators.
set -uo pipefail

WRAPPER="${CODEAGENT_WRAPPER:-$HOME/.claude/bin/codeagent-wrapper}"
TIMEOUT_SECONDS="${MODEL_PREFLIGHT_TIMEOUT:-20}"
AVAILABLE=0
UNKNOWN=0
TOTAL=2

check_backend() {
  local backend="$1"
  if [[ ! -x "$WRAPPER" ]]; then
    echo "UNAVAILABLE $backend: wrapper not executable at $WRAPPER"
    return
  fi
  if [[ "$backend" == "antigravity" ]] && ! command -v agy >/dev/null 2>&1; then
    echo "UNAVAILABLE antigravity: agy not found on PATH"
    return
  fi
  if command -v timeout >/dev/null 2>&1; then
    timeout "$TIMEOUT_SECONDS" "$WRAPPER" --backend "$backend" - "$(pwd)" <<< 'OUTPUT: reply only OK' >/dev/null 2>&1
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout "$TIMEOUT_SECONDS" "$WRAPPER" --backend "$backend" - "$(pwd)" <<< 'OUTPUT: reply only OK' >/dev/null 2>&1
  elif [[ "$backend" == "claude" ]] && command -v claude >/dev/null 2>&1; then
    # Claude CLI has its own bounded-turn invocation; wrapper availability plus CLI discovery
    # is enough for preflight when GNU timeout is unavailable (for example stock macOS).
    echo "AVAILABLE claude: CLI discovered; live timeout probe skipped (no timeout/gtimeout)"
    AVAILABLE=$((AVAILABLE + 1))
    return
  else
    echo "UNKNOWN $backend: install timeout (or coreutils gtimeout) for a bounded live probe"
    UNKNOWN=$((UNKNOWN + 1))
    return
  fi
  if [[ $? -eq 0 ]]; then
    echo "AVAILABLE $backend"
    AVAILABLE=$((AVAILABLE + 1))
  else
    echo "UNAVAILABLE $backend: bounded probe failed"
  fi
}

check_backend antigravity
check_backend claude

if [[ $AVAILABLE -eq $TOTAL ]]; then
  echo "FULL: both external model backends are available"
  exit 0
elif [[ $AVAILABLE -gt 0 ]]; then
  echo "DEGRADED: $AVAILABLE/$TOTAL backends available; record degradation and use the available backend"
  exit 10
elif [[ $UNKNOWN -gt 0 ]]; then
  echo "DEGRADED: no backend was live-probed and $UNKNOWN state(s) are unknown; record degradation"
  exit 10
else
  echo "LOCAL_ONLY: no external backend available; skip repeated waits and record local-only analysis"
  exit 20
fi
