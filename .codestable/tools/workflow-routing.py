#!/usr/bin/env python3
"""Pure routing predicate for CodeStable continuation candidates."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SAFETY_BLOCKERS = {
    "canonical_conflict",
    "missing_required_artifact",
    "awaiting_design_approval",
    "awaiting_plan_approval",
    "awaiting_report_confirmation",
    "awaiting_fix_option_selection",
    "awaiting_acceptance_checks",
    "scope_expansion_required",
    "multiple_candidates",
    "ambiguous_next_step",
    "terminal_stage",
}


def verified_freshness(status_path: Path) -> str:
    repo_root = status_path.parent.parent
    command = [
        sys.executable,
        str(repo_root / ".codestable/tools/build-status.py"),
        "--repo-root",
        str(repo_root),
        "--output",
        str(status_path),
        "--check",
        "--json",
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        payload = json.loads(result.stdout)
    except (OSError, json.JSONDecodeError):
        return "unverifiable"
    return str(payload.get("freshness", {}).get("state") or "unverifiable")


def decide(status: dict, freshness: str | None = None) -> dict:
    freshness = freshness or status.get("freshness", {}).get("state")
    if freshness != "fresh":
        return {"action": "inspect_canonical", "reason": f"generated_state_{freshness or 'missing'}", "candidate": None}

    candidates = []
    for lane_name, lane in status.get("lanes", {}).items():
        for item in lane.get("items", []):
            derived = item.get("derived", {})
            blockers = set(derived.get("blockers") or [])
            eligible = (
                item.get("consistency", {}).get("state") != "conflict"
                and derived.get("auto_continue_allowed") is True
                and derived.get("needs_user_decision") is False
                and not (blockers & SAFETY_BLOCKERS)
            )
            if eligible:
                candidates.append({"lane": lane_name, "key": item.get("key"), "path": item.get("path"), "next_skill": derived.get("next_skill")})

    if not candidates:
        return {"action": "route_normally", "reason": "no_eligible_continuation", "candidate": None}
    if len(candidates) > 1:
        return {"action": "ask_user", "reason": "multiple_candidates", "candidate": None, "candidates": candidates}
    return {"action": "continue", "reason": "unique_eligible_candidate", "candidate": candidates[0]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("status", nargs="?", default="-")
    args = parser.parse_args()
    if args.status == "-":
        status = json.loads(sys.stdin.read())
        freshness = status.get("freshness", {}).get("state")
    else:
        status_path = Path(args.status).expanduser().resolve()
        status = json.loads(status_path.read_text(encoding="utf-8"))
        freshness = verified_freshness(status_path)
    print(json.dumps(decide(status, freshness), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
