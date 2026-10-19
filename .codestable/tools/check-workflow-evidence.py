#!/usr/bin/env python3
"""Validate opt-in CodeStable workflow evidence contracts.

The checker intentionally validates only artifacts declaring
``evidence_contract: v1``. This preserves historical workflow artifacts while
making incomplete evidence a deterministic failure for new work.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


CONTRACT_VERSION = "v1"
COMPLETE_STATUSES = {"done", "passed"}


@dataclass
class Finding:
    level: str
    rule: str
    path: str
    message: str


def relative(root: Path, path: Path) -> str:
    return str(path.relative_to(root))


def has_v1_contract(text: str) -> bool:
    if yaml is None:
        return "evidence_contract: v1" in text
    try:
        payload = yaml.safe_load(text)
    except yaml.YAMLError:
        return False
    return isinstance(payload, dict) and payload.get("evidence_contract") == CONTRACT_VERSION


def check_checklist(root: Path, path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    if not has_v1_contract(text):
        return []
    try:
        payload = yaml.safe_load(text)
    except (yaml.YAMLError, AttributeError):
        payload = None
    if yaml is None or not isinstance(payload, dict):
        return [Finding("error", "evidence_yaml", relative(root, path), "checklist YAML could not be parsed")]
    findings: list[Finding] = []
    for section, identity_keys in (("steps", ("id", "action")), ("checks", ("id", "item"))):
        blocks = payload.get(section, [])
        if not blocks:
            findings.append(Finding("error", "evidence_section", relative(root, path), f"{section} must contain at least one item"))
            continue
        for index, block in enumerate(blocks, start=1):
            if not isinstance(block, dict):
                findings.append(Finding("error", "evidence_item", relative(root, path), f"{section}[{index}] must be a mapping"))
                continue
            label = f"{section}[{index}]"
            for key in identity_keys:
                if not block.get(key):
                    findings.append(Finding("error", "evidence_identity", relative(root, path), f"{label} is missing {key}"))
            verification = block.get("verification")
            if not isinstance(verification, dict) or not verification.get("method"):
                findings.append(Finding("error", "evidence_method", relative(root, path), f"{label}.verification is missing method"))
            evidence = block.get("evidence")
            if not isinstance(evidence, dict):
                findings.append(Finding("error", "evidence_payload", relative(root, path), f"{label} is missing evidence"))
                continue
            status = str(block.get("status") or "")
            if status in COMPLETE_STATUSES:
                result = evidence.get("result")
                verified_at = evidence.get("verified_at")
                verified_by = evidence.get("verified_by")
                if not result or str(result).lower() == "pending":
                    findings.append(Finding("error", "evidence_result", relative(root, path), f"{label} is {status} but has no concrete evidence.result"))
                if not verified_at or str(verified_at).lower() in {"null", "pending"}:
                    findings.append(Finding("error", "evidence_verified_at", relative(root, path), f"{label} is {status} but has no evidence.verified_at"))
                if not verified_by or str(verified_by).lower() in {"null", "pending"}:
                    findings.append(Finding("error", "evidence_verified_by", relative(root, path), f"{label} is {status} but has no evidence.verified_by"))
    return findings


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        values[key.strip()] = raw.strip().strip("'\"")
    return values


def check_report(root: Path, path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    if meta.get("evidence_contract") != CONTRACT_VERSION:
        return []
    findings: list[Finding] = []
    for heading in ("## 验证证据", "## 遗留风险"):
        if heading not in text:
            findings.append(Finding("error", "evidence_report_section", relative(root, path), f"missing required report section: {heading}"))
    return findings


def candidate_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for lane in ("features", "refactors"):
        lane_root = root / ".codestable" / lane
        if lane_root.exists():
            for path in lane_root.glob("*/*-checklist.yaml"):
                if "archive" not in path.parts:
                    paths.append(path)
    for lane in ("features", "issues"):
        lane_root = root / ".codestable" / lane
        if lane_root.exists():
            paths.extend(lane_root.glob("*/*-acceptance.md"))
            paths.extend(lane_root.glob("*/*-fix-note.md"))
    return sorted(set(path for path in paths if path.is_file()))


def validate(root: Path) -> dict:
    findings: list[Finding] = []
    validated = 0
    for path in candidate_paths(root):
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".yaml" and has_v1_contract(text):
            validated += 1
            findings.extend(check_checklist(root, path))
        elif path.suffix == ".md" and frontmatter(text).get("evidence_contract") == CONTRACT_VERSION:
            validated += 1
            findings.extend(check_report(root, path))
    errors = sum(finding.level == "error" for finding in findings)
    return {
        "ok": errors == 0,
        "contract": CONTRACT_VERSION,
        "validated": validated,
        "errors": errors,
        "findings": [asdict(finding) for finding in findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate opt-in workflow evidence contracts.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()
    result = validate(Path(args.repo_root).resolve())
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Workflow evidence: validated={result['validated']}, errors={result['errors']}")
        for finding in result["findings"]:
            print(f"[{finding['level'].upper()}] {finding['rule']} :: {finding['path']}\n  {finding['message']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
