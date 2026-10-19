#!/usr/bin/env python3
"""Score CodeStable skill design and workflow artifact quality.

The score is intentionally deterministic and evidence-oriented.  It does not
replace canonical state or claim that a high score proves semantic correctness.
Its purpose is to make missing workflow safeguards visible and ratchet new
skills/artifacts toward a shared quality bar.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


QUALITY_CONTRACT = ".codestable/reference/skill-quality-contract.md"
DEFAULT_MIN_SKILL_SCORE = 80
MAX_MARKDOWN_LINES = 500


@dataclass
class ScoreResult:
    name: str
    path: str
    score: int
    max_score: int
    checks: list[dict]


def check(condition: bool, points: int, message: str) -> dict:
    return {
        "passed": condition,
        "points": points if condition else 0,
        "max_points": points,
        "message": message,
    }


def score_from_checks(name: str, path: Path, checks: list[dict]) -> ScoreResult:
    return ScoreResult(
        name=name,
        path=str(path),
        score=sum(item["points"] for item in checks),
        max_score=sum(item["max_points"] for item in checks),
        checks=checks,
    )


def markdown_lines(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def has_frontmatter_field(content: str, field: str) -> bool:
    if not content.startswith("---\n"):
        return False
    end = content.find("\n---", 4)
    if end == -1:
        return False
    return bool(re.search(rf"(?m)^{re.escape(field)}:\s*\S+", content[4:end]))


def find_skill_paths(root: Path) -> Iterable[Path]:
    root_skill = root / "cs/SKILL.md"
    if root_skill.exists():
        yield root_skill
    yield from sorted(root.glob("cs-*/SKILL.md"))


def score_skill(root: Path, path: Path) -> ScoreResult:
    content = path.read_text(encoding="utf-8")
    relative = path.relative_to(root)
    checks = [
        check(has_frontmatter_field(content, "name"), 10, "frontmatter defines name"),
        check(has_frontmatter_field(content, "description"), 10, "frontmatter defines description"),
        check("## 启动必读" in content, 10, "defines startup material"),
        check("## 退出条件" in content or "## 退出" in content, 15, "defines an exit condition"),
        check("- [ ]" in content, 10, "uses checklist-form exit conditions"),
        check(QUALITY_CONTRACT in content, 15, "links to the shared quality contract"),
        check("Hard-required" in content or "硬必读" in content, 10, "distinguishes hard-required input"),
        check("On-demand" in content or "按需读取" in content, 10, "distinguishes on-demand input"),
        check("证据" in content or "evidence" in content.lower(), 5, "states an evidence requirement"),
        check(markdown_lines(path) <= MAX_MARKDOWN_LINES, 5, "stays within the Markdown line limit"),
    ]
    return score_from_checks(path.parent.name, relative, checks)


def is_compatibility_path(path: Path) -> bool:
    name = path.parent.name.lower()
    text = path.read_text(encoding="utf-8") if path.suffix == ".md" else ""
    return any(token in name for token in ("sample", "example", "legacy")) or "workflow: legacy" in text


def artifact_paths(root: Path) -> Iterable[tuple[str, Path]]:
    for lane in ("features", "issues", "refactors", "audits"):
        lane_root = root / f".codestable/{lane}"
        if not lane_root.exists():
            continue
        for directory in sorted(path for path in lane_root.iterdir() if path.is_dir() and path.name != "archive"):
            yield lane, directory


def has_evidence(directory: Path) -> bool:
    evidence_markers = ("验证", "evidence", "verified", "test", "测试", "file:", "结果")
    for path in directory.glob("*.md"):
        text = path.read_text(encoding="utf-8").lower()
        if any(marker.lower() in text for marker in evidence_markers):
            return True
    return False


def score_artifact(root: Path, lane: str, directory: Path, status: dict | None) -> ScoreResult:
    relative = directory.relative_to(root)
    compatibility = any(is_compatibility_path(path) for path in directory.glob("*.md"))
    state = ""
    if status:
        state = str(status.get("consistency", {}).get("state", ""))
    checks = [
        check(any(directory.glob("*.md")), 25, "contains canonical Markdown artifacts"),
        check(state in {"", "clean", "compatibility"}, 25, "has no canonical consistency conflict"),
        check(has_evidence(directory), 25, "records verification or code evidence"),
        check(not compatibility, 25, "is not a legacy/sample compatibility artifact"),
    ]
    return score_from_checks(f"{lane}:{directory.name}", relative, checks)


def load_status(root: Path) -> dict:
    path = root / ".codestable/status.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def indexed_items(status: dict) -> dict[str, dict]:
    items: dict[str, dict] = {}
    for lane_data in status.get("lanes", {}).values():
        for item in lane_data.get("items", []):
            if item.get("path"):
                items[str(item["path"])] = item
    return items


def render_text(payload: dict) -> None:
    summary = payload["summary"]
    print(
        "Skill quality: "
        f"{summary['skill_score']}/{summary['skill_max_score']} "
        f"({summary['skill_percent']}%)"
    )
    print(
        "Artifact quality (advisory): "
        f"{summary['artifact_score']}/{summary['artifact_max_score']} "
        f"({summary['artifact_percent']}%)"
    )
    print(f"Skills below threshold: {summary['skills_below_threshold']}")
    print(f"Advisory artifact findings: {summary['artifact_findings']}")
    for result in payload["skills"]:
        if result["score"] < payload["min_skill_score"]:
            missing = [item["message"] for item in result["checks"] if not item["passed"]]
            print(f"[SKILL] {result['path']}: {result['score']}/{result['max_score']} — {', '.join(missing)}")
    for result in payload["artifacts"]:
        if result["score"] < result["max_score"]:
            missing = [item["message"] for item in result["checks"] if not item["passed"]]
            print(f"[ADVISORY] {result['path']}: {result['score']}/{result['max_score']} — {', '.join(missing)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score CodeStable workflow quality.")
    parser.add_argument("--repo-root", default=".", help="Repository root (default: current directory)")
    parser.add_argument("--min-skill-score", type=int, default=DEFAULT_MIN_SKILL_SCORE)
    parser.add_argument("--check-skills", action="store_true", help="Fail when a skill scores below the threshold")
    parser.add_argument("--strict-artifacts", action="store_true", help="Fail when a non-compatibility artifact is incomplete")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = Path(args.repo_root).resolve()
    status = load_status(root)
    status_items = indexed_items(status)
    skills = [asdict(score_skill(root, path)) for path in find_skill_paths(root)]
    artifacts = [
        asdict(score_artifact(root, lane, directory, status_items.get(str(directory.relative_to(root)))))
        for lane, directory in artifact_paths(root)
    ]

    skill_score = sum(item["score"] for item in skills)
    skill_max_score = sum(item["max_score"] for item in skills)
    artifact_score = sum(item["score"] for item in artifacts)
    artifact_max_score = sum(item["max_score"] for item in artifacts)
    below_threshold = [item for item in skills if item["score"] < args.min_skill_score]
    strict_artifact_failures = [
        item
        for item in artifacts
        if item["score"] < item["max_score"] and not any("compatibility" in check["message"] for check in item["checks"] if not check["passed"])
    ]
    payload = {
        "version": 1,
        "quality_contract": QUALITY_CONTRACT,
        "min_skill_score": args.min_skill_score,
        "skills": skills,
        "artifacts": artifacts,
        "summary": {
            "skill_score": skill_score,
            "skill_max_score": skill_max_score,
            "skill_percent": round(skill_score * 100 / skill_max_score) if skill_max_score else 100,
            "artifact_score": artifact_score,
            "artifact_max_score": artifact_max_score,
            "artifact_percent": round(artifact_score * 100 / artifact_max_score) if artifact_max_score else 100,
            "skills_below_threshold": len(below_threshold),
            "artifact_findings": sum(1 for item in artifacts if item["score"] < item["max_score"]),
        },
    }
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        render_text(payload)

    if args.check_skills and below_threshold:
        sys.exit(1)
    if args.strict_artifacts and strict_artifact_failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
