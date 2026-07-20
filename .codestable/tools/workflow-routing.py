#!/usr/bin/env python3
"""Pure routing predicate for CodeStable continuation candidates."""

from __future__ import annotations

import argparse
import json
import sys

SAFETY_BLOCKERS = {
    "canonical_conflict",
    "missing_required_artifact",
    "awaiting_design_approval",
    "awaiting_plan_approval",
    "awaiting_report_confirmation",
    "awaiting_fix_option_selection",
    "scope_expansion_required",
    "multiple_candidates",
    "ambiguous_next_step",
    "terminal_stage",
}


def decide(status: dict) -> dict:
    freshness = status.get("freshness", {}).get("state")
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
    text = sys.stdin.read() if args.status == "-" else open(args.status, encoding="utf-8").read()
    print(json.dumps(decide(json.loads(text)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
