#!/usr/bin/env python3
"""
build-status.py — deterministically generate .codestable/status.json from canonical artifacts.

Inputs:
  - .codestable/features/**
  - .codestable/issues/**
  - .codestable/refactors/**
  - .codestable/audits/**

Explicit non-inputs:
  - .ccg/tasks/**
  - context.jsonl
  - STATUS.md

The generated file is a convenience spine only. Canonical artifacts always outrank it.
"""

import argparse
import hashlib
import json
from pathlib import Path

TERMINAL_STAGE = "terminal_stage"
CANONICAL_CONFLICT = "canonical_conflict"
MISSING_REQUIRED_ARTIFACT = "missing_required_artifact"
AWAITING_DESIGN_APPROVAL = "awaiting_design_approval"
AWAITING_PLAN_APPROVAL = "awaiting_plan_approval"
AWAITING_REPORT_CONFIRMATION = "awaiting_report_confirmation"
AWAITING_FIX_OPTION_SELECTION = "awaiting_fix_option_selection"
SCOPE_EXPANSION_REQUIRED = "scope_expansion_required"
MULTIPLE_CANDIDATES = "multiple_candidates"
AMBIGUOUS_NEXT_STEP = "ambiguous_next_step"
SCHEMA_VERSION = "1.2"
GENERATOR_VERSION = "0.3.0"
STATE_ORDER = {"clean": 0, "compatibility": 1, "conflict": 2}

FEATURE_ARTIFACT_SPECS = [
    ("design", "design", ["-design.md"], False),
    ("plan", "plan", ["-plan.md"], False),
    ("checklist", "checklist", ["-checklist.yaml"], False),
    ("acceptance", "acceptance", ["-acceptance.md"], False),
    ("ff_note", "ff-note", ["-ff-note.md"], False),
]
ISSUE_ARTIFACT_SPECS = [
    ("report", "report", ["-report.md"], False),
    ("analysis", "analysis", ["-analysis.md"], False),
    ("fix_note", "fix-note", ["-fix-note.md"], False),
]
REFACTOR_ARTIFACT_SPECS = [
    ("scan", "scan", ["-scan.md"], True),
    ("design", "design", ["-refactor-design.md", "-design.md"], True),
    ("checklist", "checklist", ["-checklist.yaml"], True),
    ("apply_notes", "apply-notes", ["-apply-notes.md"], True),
    ("completion_report", "completion-report", ["-completion-report.md"], True),
]
LANE_BUILDERS = {
    "features": "feature_item",
    "issues": "issue_item",
    "refactors": "refactor_item",
    "audits": "audit_item",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_frontmatter(path: Path) -> dict:
    text = read_text(path)
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    meta = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.strip().startswith("#") or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        meta[key.strip()] = raw.strip().strip("'\"")
    return meta


def artifact_names(directory: Path, suffixes: list[str]) -> list[str]:
    matches = []
    for child in directory.iterdir():
        if child.is_file() and any(child.name.endswith(suffix) for suffix in suffixes):
            matches.append(child.name)
    return sorted(matches)


def first_name(names: list[str]) -> str | None:
    return names[0] if names else None


def lane_slug(directory_name: str) -> str:
    parts = directory_name.split("-", 3)
    if (
        len(parts) == 4
        and len(parts[0]) == 4
        and len(parts[1]) == 2
        and len(parts[2]) == 2
        and parts[0].isdigit()
        and parts[1].isdigit()
        and parts[2].isdigit()
    ):
        return parts[3]
    return directory_name


def canonical_artifact_names(directory: Path, suffixes: list[str], slug: str) -> list[str]:
    matches = artifact_names(directory, suffixes)
    slug_prefix = f"{slug}-"
    preferred = [name for name in matches if name.startswith(slug_prefix)]
    return preferred or matches


def file_list(directory: Path, *names: str | None) -> list[Path]:
    return [directory / name for name in names if name]


def checklist_progress(path: Path | None) -> dict:
    if path is None or not path.exists():
        return {"total": 0, "done": 0}

    total = 0
    done = 0
    current_is_step = False
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if stripped.startswith("- action:"):
            total += 1
            current_is_step = True
        elif stripped.startswith("status:") and current_is_step:
            status = stripped.partition(":")[2].strip().strip("'\"")
            if status in {"done", "passed"}:
                done += 1
            current_is_step = False
        elif stripped.startswith("- "):
            current_is_step = False
    return {"total": total, "done": done}


def relpath(path: Path, repo_root: Path) -> str:
    return str(path.relative_to(repo_root))


def digest_files(paths: list[Path], repo_root: Path) -> str:
    hasher = hashlib.sha256()
    for path in sorted(paths, key=lambda item: relpath(item, repo_root)):
        hasher.update(relpath(path, repo_root).encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
        hasher.update(b"\0")
    return f"sha256:{hasher.hexdigest()}"


def has_sample_marker(meta: dict, directory_name: str) -> bool:
    name = directory_name.lower()
    if any(token in name for token in ("sample", "example")):
        return True
    tags = meta.get("tags", "")
    if isinstance(tags, str) and any(token in tags.lower() for token in ("sample", "example", "fixture")):
        return True
    summary = str(meta.get("summary") or "").lower()
    return any(token in summary for token in ("样板", "示例", "sample", "example", "fixture"))


def status_value(path: Path | None) -> str:
    if path is None:
        return ""
    return str(extract_frontmatter(path).get("status") or "").strip().lower()


def promote_state(current: str, candidate: str) -> str:
    return candidate if STATE_ORDER[candidate] > STATE_ORDER[current] else current


def note_consistency(state: str, reasons: list[str], candidate: str, message: str) -> str:
    reasons.append(message)
    return promote_state(state, candidate)


def add_multiple_candidate_consistency(
    state: str,
    reasons: list[str],
    label: str,
    names: list[str],
) -> str:
    if len(names) <= 1:
        return state
    return note_consistency(
        state,
        reasons,
        "conflict",
        f"multiple {label} artifacts found: {', '.join(names)}",
    )


def gather_artifacts(
    directory: Path,
    specs: list[tuple[str, str, list[str], bool]],
    *,
    slug: str | None = None,
) -> tuple[dict, str, list[str]]:
    selected = {}
    state = "clean"
    reasons: list[str] = []
    for key, label, suffixes, use_slug in specs:
        names = canonical_artifact_names(directory, suffixes, slug or "") if use_slug else artifact_names(directory, suffixes)
        selected[key] = first_name(names)
        state = add_multiple_candidate_consistency(state, reasons, label, names)
    return selected, state, reasons


def transition_result(
    *,
    active: bool,
    canonical_complete: bool,
    next_skill: str | None = None,
    auto_continue_allowed: bool = False,
    needs_user_decision: bool = False,
    blockers: list[str] | None = None,
) -> dict:
    return {
        "active": active,
        "canonical_complete": canonical_complete,
        "next_skill": next_skill,
        "auto_continue_allowed": auto_continue_allowed,
        "needs_user_decision": needs_user_decision,
        "blockers": blockers or [],
    }


def finalize_derived(
    *,
    stage: str,
    active: bool,
    canonical_complete: bool,
    next_skill: str | None,
    auto_continue_allowed: bool,
    needs_user_decision: bool,
    blockers: list[str],
    consistency_state: str,
) -> dict:
    ordered_blockers = list(dict.fromkeys(blockers))
    if consistency_state == "conflict" and CANONICAL_CONFLICT not in ordered_blockers:
        ordered_blockers.append(CANONICAL_CONFLICT)

    if canonical_complete:
        if TERMINAL_STAGE not in ordered_blockers:
            ordered_blockers.append(TERMINAL_STAGE)
        continuation_mode = "terminal"
        next_skill = None
        auto_continue_allowed = False
        needs_user_decision = False
    elif auto_continue_allowed:
        continuation_mode = "auto"
    else:
        continuation_mode = "ask_user"
        if next_skill is None and not ordered_blockers:
            ordered_blockers.append(AMBIGUOUS_NEXT_STEP)
            needs_user_decision = True

    return {
        "stage": stage,
        "active": active,
        "ready_for_next": next_skill is not None and not canonical_complete,
        "canonical_complete": canonical_complete,
        "next_skill": next_skill,
        "auto_continue_allowed": auto_continue_allowed,
        "continuation_mode": continuation_mode,
        "needs_user_decision": needs_user_decision,
        "blockers": ordered_blockers,
    }


def make_item(
    *,
    directory: Path,
    repo_root: Path,
    lane: str,
    canonical: dict,
    derived: dict,
    consistency_state: str,
    consistency_reasons: list[str],
) -> dict:
    return {
        "key": directory.name,
        "lane": lane,
        "path": relpath(directory, repo_root),
        "canonical": canonical,
        "derived": finalize_derived(consistency_state=consistency_state, **derived),
        "consistency": {
            "state": consistency_state,
            "reasons": consistency_reasons,
        },
    }


def feature_stage(artifacts: dict, progress: dict) -> str:
    if artifacts["acceptance"]:
        return "accepted"
    if progress["total"] > 0 and progress["done"] == progress["total"]:
        return "ready_for_acceptance"
    if artifacts["plan"] or artifacts["checklist"]:
        return "planned"
    if artifacts["design"]:
        return "designed"
    return "empty"


def feature_transition(
    stage: str,
    artifacts: dict,
    design_status: str,
    plan_status: str,
    progress: dict,
    workflow: str | None,
) -> dict:
    has_acceptance = bool(artifacts["acceptance"])
    active = stage != "empty"
    design_approved = design_status == "approved"
    plan_approved = plan_status == "approved"
    has_plan_and_checklist = bool(artifacts["plan"] and artifacts["checklist"])
    has_partial_plan_state = bool(artifacts["plan"] or artifacts["checklist"])
    checklist_complete = progress["total"] > 0 and progress["done"] == progress["total"]
    legacy_accepted = has_acceptance and (
        workflow == "legacy" or (workflow is None and not artifacts["plan"])
    )

    if legacy_accepted:
        return transition_result(active=False, canonical_complete=True)
    if artifacts["design"] and not design_approved:
        return transition_result(
            active=active,
            canonical_complete=False,
            needs_user_decision=True,
            blockers=[AWAITING_DESIGN_APPROVAL],
        )
    if has_acceptance and not has_plan_and_checklist:
        return transition_result(
            active=active,
            canonical_complete=False,
            needs_user_decision=True,
            blockers=[MISSING_REQUIRED_ARTIFACT],
        )
    if has_acceptance and not plan_approved:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-feat-plan",
            needs_user_decision=True,
            blockers=[AWAITING_PLAN_APPROVAL],
        )
    if has_acceptance and not checklist_complete:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-feat-impl",
            needs_user_decision=True,
            blockers=[MISSING_REQUIRED_ARTIFACT],
        )
    if has_acceptance:
        return transition_result(active=False, canonical_complete=True)
    if design_approved and not has_partial_plan_state:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-feat-plan",
            auto_continue_allowed=True,
        )
    if design_approved and has_plan_and_checklist and not plan_approved:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-feat-plan",
            needs_user_decision=True,
            blockers=[AWAITING_PLAN_APPROVAL],
        )
    if design_approved and has_plan_and_checklist and not checklist_complete:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-feat-impl",
            auto_continue_allowed=True,
        )
    if design_approved and has_plan_and_checklist and checklist_complete:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-feat-accept",
            auto_continue_allowed=True,
        )
    if has_partial_plan_state and not artifacts["design"]:
        return transition_result(
            active=active,
            canonical_complete=False,
            needs_user_decision=True,
            blockers=[MISSING_REQUIRED_ARTIFACT],
        )
    if design_approved and has_partial_plan_state and not has_plan_and_checklist:
        return transition_result(
            active=active,
            canonical_complete=False,
            needs_user_decision=True,
            blockers=[MISSING_REQUIRED_ARTIFACT],
        )
    if stage != "empty":
        return transition_result(
            active=active,
            canonical_complete=False,
            needs_user_decision=True,
            blockers=[AMBIGUOUS_NEXT_STEP],
        )
    return transition_result(active=False, canonical_complete=False)


def feature_item(directory: Path, repo_root: Path) -> tuple[dict, list[Path]]:
    artifacts, state, reasons = gather_artifacts(directory, FEATURE_ARTIFACT_SPECS)
    design_path = directory / artifacts["design"] if artifacts["design"] else None
    plan_path = directory / artifacts["plan"] if artifacts["plan"] else None
    checklist_path = directory / artifacts["checklist"] if artifacts["checklist"] else None
    meta = extract_frontmatter(design_path) if design_path else {}
    plan_meta = extract_frontmatter(plan_path) if plan_path else {}
    progress = checklist_progress(checklist_path)
    workflow = meta.get("workflow") or None

    if workflow is None and artifacts["plan"]:
        candidate = "compatibility" if has_sample_marker(meta, directory.name) else "conflict"
        state = note_consistency(state, reasons, candidate, "plan.md exists but design frontmatter is missing workflow: hybrid")
    elif workflow not in (None, "hybrid", "legacy"):
        state = note_consistency(state, reasons, "conflict", f"unexpected workflow value: {workflow}")
    elif workflow == "legacy":
        state = note_consistency(state, reasons, "compatibility", "legacy workflow remains compatibility-only")

    stage = feature_stage(artifacts, progress)
    derived = feature_transition(
        stage, artifacts, status_value(design_path), status_value(plan_path), progress, workflow
    )
    files = file_list(directory, *artifacts.values())
    canonical = {
        "artifacts": artifacts,
        "frontmatter": {
            "status": meta.get("status"),
            "plan_status": plan_meta.get("status"),
            "workflow": workflow,
            "roadmap": meta.get("roadmap"),
            "roadmap_item": meta.get("roadmap_item"),
        },
        "checklist_progress": progress,
    }
    item = make_item(
        directory=directory,
        repo_root=repo_root,
        lane="features",
        canonical=canonical,
        derived={"stage": stage, **derived},
        consistency_state=state,
        consistency_reasons=reasons,
    )
    return item, files


def issue_stage(artifacts: dict) -> str:
    if artifacts["fix_note"]:
        return "resolved"
    if artifacts["analysis"]:
        return "analyzed"
    if artifacts["report"]:
        return "reported"
    return "empty"


def issue_transition(
    stage: str,
    artifacts: dict,
    report_status: str,
    analysis_status: str,
    fix_note_status: str,
) -> dict:
    has_fix_note = bool(artifacts["fix_note"])
    active = stage != "empty"
    has_report = bool(artifacts["report"])
    has_analysis = bool(artifacts["analysis"])
    fix_note_only_terminal = (
        has_fix_note
        and not has_report
        and not has_analysis
        and fix_note_status in {"", "completed"}
    )
    confirmed_fast_path_terminal = (
        has_fix_note
        and has_report
        and report_status == "confirmed"
        and not has_analysis
        and fix_note_status == "completed"
    )

    if fix_note_only_terminal or confirmed_fast_path_terminal:
        return transition_result(active=False, canonical_complete=True)
    if has_fix_note and not has_report and not has_analysis:
        return transition_result(
            active=True,
            canonical_complete=False,
            next_skill="cs-issue-fix",
            auto_continue_allowed=True,
        )
    if has_report and report_status != "confirmed":
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-issue-report",
            needs_user_decision=True,
            blockers=[AWAITING_REPORT_CONFIRMATION],
        )
    if has_analysis and analysis_status != "confirmed":
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-issue-analyze",
            needs_user_decision=True,
            blockers=[AWAITING_FIX_OPTION_SELECTION],
        )
    if has_fix_note and has_analysis and fix_note_status == "completed":
        return transition_result(active=False, canonical_complete=True)
    if has_analysis:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-issue-fix",
            auto_continue_allowed=True,
        )
    if has_report:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-issue-analyze",
            auto_continue_allowed=True,
        )
    if stage != "empty":
        return transition_result(
            active=active,
            canonical_complete=False,
            needs_user_decision=True,
            blockers=[AMBIGUOUS_NEXT_STEP],
        )
    return transition_result(active=False, canonical_complete=False)


def issue_item(directory: Path, repo_root: Path) -> tuple[dict, list[Path]]:
    artifacts, state, reasons = gather_artifacts(directory, ISSUE_ARTIFACT_SPECS)
    report_path = directory / artifacts["report"] if artifacts["report"] else None
    analysis_path = directory / artifacts["analysis"] if artifacts["analysis"] else None
    fix_note_path = directory / artifacts["fix_note"] if artifacts["fix_note"] else None

    if artifacts["fix_note"] and not artifacts["report"] and not artifacts["analysis"]:
        state = note_consistency(state, reasons, "compatibility", "fast-path resolved issue without retained report/analysis")
    if artifacts["analysis"] and status_value(report_path) != "confirmed":
        state = note_consistency(
            state,
            reasons,
            "conflict",
            "analysis.md exists but report.md is absent or not status=confirmed",
        )

    stage = issue_stage(artifacts)
    derived = issue_transition(
        stage,
        artifacts,
        status_value(report_path),
        status_value(analysis_path),
        status_value(fix_note_path),
    )
    files = file_list(directory, artifacts["report"], artifacts["analysis"], artifacts["fix_note"])
    canonical = {"artifacts": artifacts}
    item = make_item(
        directory=directory,
        repo_root=repo_root,
        lane="issues",
        canonical=canonical,
        derived={"stage": stage, **derived},
        consistency_state=state,
        consistency_reasons=reasons,
    )
    return item, files


def refactor_stage(artifacts: dict) -> str:
    if artifacts["completion_report"]:
        return "completed"
    if artifacts["apply_notes"]:
        return "applied"
    if artifacts["design"] or artifacts["checklist"]:
        return "planned"
    if artifacts["scan"]:
        return "scanned"
    return "empty"


def refactor_transition(stage: str, artifacts: dict) -> dict:
    canonical_complete = bool(artifacts["completion_report"])
    active = stage not in {"completed", "empty"}

    if canonical_complete:
        return transition_result(active=active, canonical_complete=True)
    if artifacts["apply_notes"]:
        return transition_result(
            active=active,
            canonical_complete=False,
            needs_user_decision=True,
            blockers=[TERMINAL_STAGE],
        )
    if artifacts["design"] and artifacts["checklist"]:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-refactor-apply",
            auto_continue_allowed=True,
        )
    if artifacts["scan"]:
        return transition_result(
            active=active,
            canonical_complete=False,
            next_skill="cs-refactor-design",
            auto_continue_allowed=True,
        )
    if stage != "empty":
        return transition_result(
            active=active,
            canonical_complete=False,
            needs_user_decision=True,
            blockers=[AMBIGUOUS_NEXT_STEP],
        )
    return transition_result(active=False, canonical_complete=False)


def refactor_item(directory: Path, repo_root: Path) -> tuple[dict, list[Path]]:
    artifacts, state, reasons = gather_artifacts(
        directory,
        REFACTOR_ARTIFACT_SPECS,
        slug=lane_slug(directory.name),
    )
    stage = refactor_stage(artifacts)
    derived = refactor_transition(stage, artifacts)
    files = file_list(
        directory,
        artifacts["scan"],
        artifacts["design"],
        artifacts["checklist"],
        artifacts["apply_notes"],
        artifacts["completion_report"],
    )
    canonical = {"artifacts": artifacts}
    item = make_item(
        directory=directory,
        repo_root=repo_root,
        lane="refactors",
        canonical=canonical,
        derived={"stage": stage, **derived},
        consistency_state=state,
        consistency_reasons=reasons,
    )
    return item, files


def audit_item(directory: Path, repo_root: Path) -> tuple[dict, list[Path]]:
    index_names = artifact_names(directory, ["index.md"])
    finding_files = sorted(
        child.name
        for child in directory.iterdir()
        if child.is_file() and child.name.startswith("finding-") and child.name.endswith(".md")
    )
    index_name = first_name(index_names)
    stage = "reported" if index_name or finding_files else "empty"
    state = add_multiple_candidate_consistency("clean", [], "index", index_names)
    reasons: list[str] = []
    state = add_multiple_candidate_consistency(state, reasons, "index", index_names)
    derived = transition_result(
        active=stage == "reported",
        canonical_complete=False,
        needs_user_decision=stage == "reported",
        blockers=[] if stage == "empty" else [AMBIGUOUS_NEXT_STEP],
    )
    files = file_list(directory, index_name)
    files.extend(directory / name for name in finding_files)
    canonical = {
        "artifacts": {
            "index": index_name,
            "findings": finding_files,
        }
    }
    item = make_item(
        directory=directory,
        repo_root=repo_root,
        lane="audits",
        canonical=canonical,
        derived={"stage": stage, **derived},
        consistency_state=state,
        consistency_reasons=reasons,
    )
    return item, files


def scan_lane(repo_root: Path, lane: str, builder_name: str) -> tuple[list[dict], list[Path]]:
    lane_root = repo_root / ".codestable" / lane
    if not lane_root.exists():
        return [], []

    items = []
    files = []
    builder = globals()[builder_name]
    for directory in sorted(child for child in lane_root.iterdir() if child.is_dir() and not child.name.startswith(".")):
        item, item_files = builder(directory, repo_root)
        items.append(item)
        files.extend(item_files)
    return items, files


def lane_summary(items: list[dict]) -> dict:
    return {
        "count": len(items),
        "active_count": sum(1 for item in items if item["derived"]["active"]),
        "items": items,
    }


def scan_all_lanes(repo_root: Path) -> tuple[dict, list[Path], int, int]:
    lanes = {}
    all_files = []
    compatibility_count = 0
    conflict_count = 0

    for lane, builder_name in LANE_BUILDERS.items():
        items, lane_files = scan_lane(repo_root, lane, builder_name)
        lanes[lane] = lane_summary(items)
        all_files.extend(lane_files)
        compatibility_count += sum(1 for item in items if item["consistency"]["state"] == "compatibility")
        conflict_count += sum(1 for item in items if item["consistency"]["state"] == "conflict")

    return lanes, all_files, compatibility_count, conflict_count


def build_status(repo_root: Path) -> dict:
    lanes, all_files, compatibility_count, conflict_count = scan_all_lanes(repo_root)
    freshness_state = "conflict" if conflict_count else "fresh"

    return {
        "schema_version": SCHEMA_VERSION,
        "generator": {
            "name": "build-status.py",
            "version": GENERATOR_VERSION,
            "deterministic_sort": True,
            "canonical_roots": [
                ".codestable/features",
                ".codestable/issues",
                ".codestable/refactors",
                ".codestable/audits",
            ],
        },
        "authority": {
            "canonical_precedence": True,
            "generated_state_rank": 3,
            "bridge_hints_rank": 4,
            "status_md_required": False,
        },
        "freshness": {
            "state": freshness_state,
            "canonical_digest": digest_files(all_files, repo_root),
            "source_count": len(all_files),
            "stale_if_digest_changes": True,
            "check_command": "python .codestable/tools/build-status.py --check",
            "reasons": [] if not conflict_count else [f"{conflict_count} canonical conflict(s) detected"],
        },
        "bridge_hints": {
            "included": False,
            "sources": [".ccg/tasks/*/task.json"],
            "note": "Bridge-only hints are intentionally excluded and can never outrank canonical artifacts.",
        },
        "lanes": lanes,
        "summary": {
            "feature_count": lanes["features"]["count"],
            "issue_count": lanes["issues"]["count"],
            "refactor_count": lanes["refactors"]["count"],
            "audit_count": lanes["audits"]["count"],
            "active_count": sum(summary["active_count"] for summary in lanes.values()),
            "compatibility_count": compatibility_count,
            "conflict_count": conflict_count,
        },
    }


def normalize_repo_root(raw: str) -> Path:
    return Path(raw).expanduser().absolute()


def normalize_output_path(repo_root: Path, raw: str) -> Path:
    raw_path = Path(raw).expanduser()
    output_path = raw_path if raw_path.is_absolute() else repo_root / raw_path
    output_path = output_path.absolute()
    try:
        output_path.relative_to(repo_root)
    except ValueError as exc:
        raise SystemExit("--output must stay under --repo-root") from exc
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic .codestable/status.json")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--output", default=".codestable/status.json", help="Output path")
    parser.add_argument("--check", action="store_true", help="Verify output matches the current canonical snapshot")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable verification output (requires --check)")
    args = parser.parse_args()

    repo_root = normalize_repo_root(args.repo_root)
    output_path = normalize_output_path(repo_root, args.output)
    payload = build_status(repo_root)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    if args.json_output and not args.check:
        parser.error("--json requires --check")

    if args.check:
        current = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        matches = current == rendered
        expected_state = payload["freshness"]["state"]
        state = "conflict" if expected_state == "conflict" else ("fresh" if matches else "stale")
        result = {
            "ok": state == "fresh",
            "freshness": {
                "state": state,
                "expected_state": expected_state,
                "canonical_digest": payload["freshness"]["canonical_digest"],
            },
            "output": str(output_path.relative_to(repo_root)),
            "matches_canonical_snapshot": matches,
        }
        if args.json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return {"fresh": 0, "stale": 1, "conflict": 2}[state]

    output_path.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
