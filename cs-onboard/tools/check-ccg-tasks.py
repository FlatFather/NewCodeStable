#!/usr/bin/env python3
"""Validate CCG bridge-task lifecycle without promoting it to workflow authority."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_ACTIVE = {"id", "title", "status"}
VALID_STATUS = {"in_progress", "completed", "blocked"}
VALID_CANONICAL_KINDS = {"feature", "issue", "refactor", "audit", "requirement", "roadmap", "architecture"}


def relative(root: Path, path: Path) -> str:
    return str(path.relative_to(root))


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, str(exc)


def load_legacy_baseline(root: Path) -> set[str]:
    path = root / ".codestable/reference/ccg-task-legacy-baseline.json"
    payload, error = load_json(path)
    if error or not isinstance(payload, dict):
        return set()
    return {str(item) for item in payload.get("completed_active_tasks", [])}


def validate(root: Path) -> dict:
    task_root = root / ".ccg/tasks"
    archive_root = task_root / "archive"
    findings = []
    legacy = load_legacy_baseline(root)
    active_files = sorted(path for path in task_root.glob("*/task.json") if path.is_file())
    archived_files = sorted(archive_root.glob("**/task.json")) if archive_root.is_dir() else []
    seen: dict[str, str] = {}

    def add(level: str, rule: str, path: Path, message: str) -> None:
        findings.append({"level": level, "rule": rule, "path": relative(root, path), "message": message})

    def inspect(path: Path, archived: bool) -> None:
        payload, error = load_json(path)
        if error:
            add("error", "task_json", path, error)
            return
        if not isinstance(payload, dict):
            add("error", "task_shape", path, "task.json must be an object")
            return
        missing = sorted(REQUIRED_ACTIVE - set(payload))
        if missing:
            add("error", "task_required_fields", path, f"missing fields: {', '.join(missing)}")
        task_id = str(payload.get("id") or path.parent.name)
        if task_id in seen:
            add("error", "task_duplicate_id", path, f"task id already appears at {seen[task_id]}")
        else:
            seen[task_id] = relative(root, path)
        status = payload.get("status")
        if status not in VALID_STATUS:
            add("error", "task_status", path, f"unexpected status: {status}")
        if archived and status == "in_progress":
            add("error", "archived_task_active", path, "archived task cannot remain in_progress")
        if not archived and status == "completed":
            level = "baseline" if task_id in legacy else "error"
            add(level, "completed_task_not_archived", path, "completed task must move under .ccg/tasks/archive/YYYY-MM/")
        canonical_path = payload.get("canonical_path")
        canonical_kind = payload.get("canonical_kind")
        if bool(canonical_path) != bool(canonical_kind):
            add("error", "task_canonical_link", path, "canonical_path and canonical_kind must appear together")
        if canonical_kind and canonical_kind not in VALID_CANONICAL_KINDS:
            add("error", "task_canonical_kind", path, f"unexpected canonical_kind: {canonical_kind}")
        if canonical_path and not (root / str(canonical_path)).exists():
            add("error", "task_canonical_path", path, f"canonical_path does not exist: {canonical_path}")

    for path in active_files:
        inspect(path, False)
    for path in archived_files:
        inspect(path, True)

    errors = sum(item["level"] == "error" for item in findings)
    warnings = sum(item["level"] == "warning" for item in findings)
    baselined = sum(item["level"] == "baseline" for item in findings)
    return {"ok": errors == 0, "errors": errors, "warnings": warnings, "baselined": baselined, "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    result = validate(root)
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"CCG tasks: errors={result['errors']}, warnings={result['warnings']}, baselined={result['baselined']}")
        for item in result["findings"]:
            print(f"[{item['level'].upper()}] {item['rule']} :: {item['path']}\n  {item['message']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
