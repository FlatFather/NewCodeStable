#!/usr/bin/env python3
"""
check-workflow-contracts.py — Read-only validator for CodeStable workflow contracts.

Checks:
  1. shared asset manifest parity (source + repo-local copies match)
  2. manifest-declared source/destination assets exist and use the right path prefixes
  3. referenced .codestable/reference/* and .codestable/tools/* assets are present
  4. active workflow docs do not drift to old codestable/ path naming
  5. active/public docs keep the canonical feature-flow wording
  6. active workflow docs stay within the markdown line-limit policy
  7. historical legacy feature artifacts warn in compatibility mode instead of failing

Designed for AI agent use: deterministic, read-only, structured output, no required
external dependencies.
"""

import argparse
import json
import re
import sys
from pathlib import Path

_HAS_PYYAML = False
try:
    import yaml  # type: ignore
    _HAS_PYYAML = True
except ImportError:
    pass

PLACEHOLDER_NAMES = {"xxx.md"}
OLD_FLOW_ZH = "`cs-feat` → `cs-feat-design` → `cs-feat-impl` → `cs-feat-accept`"
OLD_FLOW_EN = "`cs-feat` → `cs-feat-design` → `cs-feat-impl` → `cs-feat-accept`"
ACTIVE_PUBLIC_DOCS = [
    "README.md",
    "README.en.md",
    "cs/SKILL.md",
    "docs/dev/feature-workflow.md",
    ".codestable/reference/shared-conventions.md",
    ".codestable/reference/shared-conventions-feature.md",
    ".codestable/reference/system-overview.md",
    ".codestable/reference/workflow-contract.md",
    ".codestable/reference/workflow-contract-authority.md",
    ".codestable/reference/workflow-contract-continuation.md",
    ".codestable/reference/workflow-contract-distribution.md",
    ".codestable/reference/workflow-contract-generated-state.md",
    ".codestable/reference/workflow-contract-shared-concepts.md",
]

FEATURE_FLOW_EXPECTATIONS = {
    "README.md": [
        ".codestable/reference/workflow-contract.md",
    ],
    "README.en.md": [
        ".codestable/reference/workflow-contract.md",
    ],
    "cs/SKILL.md": [
        "`cs-feat-design` → `cs-feat-plan` → `cs-feat-impl` → `cs-feat-accept`",
    ],
    "docs/dev/feature-workflow.md": [
        "`cs-feat-design → cs-feat-plan → cs-feat-impl → cs-feat-accept`",
    ],
    ".codestable/reference/system-overview.md": [
        "design + plan + checklist + acceptance",
        "design → plan → implement → acceptance",
    ],
    ".codestable/reference/shared-conventions-feature.md": [
        "design + plan + checklist + acceptance",
    ],
}


def _parse_yaml_scalar(val: str):
    val = val.strip()
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1]
        return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
    lower = val.lower()
    if lower in ("true", "yes"):
        return True
    if lower in ("false", "no"):
        return False
    if lower in ("null", "~", ""):
        return None
    return val.strip("'\"")


def parse_yaml_text(text: str):
    if _HAS_PYYAML:
        try:
            data = yaml.safe_load(text)
            return (data or {}), None
        except yaml.YAMLError as exc:
            return None, str(exc)

    result = {}
    current_section = None
    current_item = None
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.endswith(":") and not stripped.startswith("-"):
            key = stripped[:-1]
            if key in ("references", "tools"):
                result[key] = []
                current_section = result[key]
                current_item = None
                continue
            current_section = None
            result[key] = {}
            continue
        if stripped.startswith("- "):
            if current_section is None:
                continue
            current_item = {}
            current_section.append(current_item)
            stripped = stripped[2:].strip()
            if ":" in stripped:
                key, _, value = stripped.partition(":")
                current_item[key.strip()] = _parse_yaml_scalar(value)
            continue
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            if current_item is not None and raw.startswith("  "):
                current_item[key.strip()] = _parse_yaml_scalar(value)
            else:
                result[key.strip()] = _parse_yaml_scalar(value)
    return result, None


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4 :].strip()
    meta, _ = parse_yaml_text(fm_text)
    if not isinstance(meta, dict):
        return {}, body
    return meta, body


def is_sample_feature(feature_dir: Path, meta: dict, body: str) -> bool:
    name = feature_dir.name.lower()
    if any(token in name for token in ("sample", "example")):
        return True

    tags = meta.get("tags") or []
    if isinstance(tags, list):
        lowered_tags = {str(tag).lower() for tag in tags}
        if lowered_tags & {"sample", "example", "fixture", "golden-sample"}:
            return True

    summary = str(meta.get("summary") or "").lower()
    body_lower = (body or "").lower()
    markers = ["样板", "示例", "sample", "example", "golden sample", "fixture"]
    return any(marker in summary or marker in body_lower for marker in markers)


class Finding:
    def __init__(self, level: str, rule: str, path: str, message: str):
        self.level = level
        self.rule = rule
        self.path = path
        self.message = message

    def to_dict(self):
        return {
            "level": self.level,
            "rule": self.rule,
            "path": self.path,
            "message": self.message,
        }


class Report:
    def __init__(self, repo_root: Path, line_limit: int):
        self.repo_root = repo_root
        self.line_limit = line_limit
        self.findings = []

    def error(self, rule: str, path, message: str):
        self.findings.append(Finding("error", rule, str(path), message))

    def warn(self, rule: str, path, message: str):
        self.findings.append(Finding("warning", rule, str(path), message))

    @property
    def error_count(self) -> int:
        return sum(1 for finding in self.findings if finding.level == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for finding in self.findings if finding.level == "warning")

    @property
    def ok(self) -> bool:
        return self.error_count == 0

    def to_dict(self):
        return {
            "ok": self.ok,
            "repoRoot": str(self.repo_root),
            "lineLimit": self.line_limit,
            "errors": self.error_count,
            "warnings": self.warning_count,
            "findings": [finding.to_dict() for finding in self.findings],
        }


def rel_path(root: Path, path: Path) -> str:
    return str(path.relative_to(root))


def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8"), None
    except OSError as exc:
        return None, str(exc)


def existing_paths(root: Path, relative_paths):
    paths = []
    for rel in relative_paths:
        path = root / rel
        if path.exists():
            paths.append(path)
    return paths


def collect_line_limit_docs(root: Path):
    docs = set(existing_paths(root, [
        "README.md",
        "README.en.md",
        "cs/SKILL.md",
    ]))
    for pattern in ["docs/dev/*.md", ".codestable/reference/*.md", "cs-onboard/reference/*.md"]:
        docs.update(path for path in root.glob(pattern) if path.is_file())
    return sorted(docs)


def collect_reference_scan_files(root: Path):
    files = set(existing_paths(root, ["README.md", "README.en.md"]))
    files.update(path for path in root.glob("docs/dev/*.md") if path.is_file())
    files.update(path for path in root.glob(".codestable/reference/*") if path.is_file())
    files.update(path for path in root.glob("cs-onboard/reference/*") if path.is_file())
    for skill_dir in root.glob("cs*"):
        if not skill_dir.is_dir():
            continue
        for md_file in skill_dir.rglob("*.md"):
            if md_file.is_file():
                files.add(md_file)
    return sorted(files)


def detect_line_limit(root: Path, override: int | None):
    if override is not None:
        return override, []
    limits = []
    for rel in ("CLAUDE.md", "AGENTS.md"):
        path = root / rel
        if not path.exists():
            continue
        text, err = read_text(path)
        if err:
            continue
        match = re.search(r"单md文档不能超过(\d+)行", text or "")
        if match:
            limits.append((rel, int(match.group(1))))
            continue
        match = re.search(r"cannot exceed (\d+) lines", text or "", re.IGNORECASE)
        if match:
            limits.append((rel, int(match.group(1))))
    if not limits:
        return 500, []
    return max(limit for _, limit in limits), limits


def parse_manifest(path: Path):
    text, err = read_text(path)
    if err:
        return None, err
    parsed, parse_err = parse_yaml_text(text)
    if parse_err:
        return None, parse_err
    if not isinstance(parsed, dict):
        return None, "Manifest must be a YAML mapping"
    references = parsed.get("references") or []
    tools = parsed.get("tools") or []
    if not isinstance(references, list) or not isinstance(tools, list):
        return None, "Manifest references/tools must be lists"
    parsed["references"] = references
    parsed["tools"] = tools
    return parsed, None


def check_manifest_parity(root: Path, report: Report):
    source_manifest = root / "cs-onboard/reference/shared-asset-manifest.yaml"
    repo_manifest = root / ".codestable/reference/shared-asset-manifest.yaml"
    manifests = {}
    for label, path in (("source", source_manifest), ("repo", repo_manifest)):
        if not path.exists():
            report.error("manifest_missing", rel_path(root, path), f"Missing {label} manifest")
            continue
        parsed, err = parse_manifest(path)
        if err:
            report.error("manifest_parse", rel_path(root, path), err)
            continue
        manifests[label] = parsed

    if set(manifests) != {"source", "repo"}:
        return None

    if manifests["source"] != manifests["repo"]:
        report.error(
            "manifest_copy_drift",
            ".codestable/reference/shared-asset-manifest.yaml",
            "Source and repo-local shared-asset manifests differ",
        )

    declared = {"references": set(), "tools": set()}
    for section, source_prefix, dest_prefix in (
        ("references", "cs-onboard/reference/", ".codestable/reference/"),
        ("tools", "cs-onboard/tools/", ".codestable/tools/"),
    ):
        seen_sources = set()
        seen_destinations = set()
        for index, item in enumerate(manifests["source"].get(section, []), start=1):
            if not isinstance(item, dict):
                report.error("manifest_entry_type", source_manifest, f"{section}[{index}] is not a mapping")
                continue
            source = item.get("source")
            destination = item.get("destination")
            if not source or not destination:
                report.error("manifest_entry_fields", source_manifest, f"{section}[{index}] is missing source or destination")
                continue
            if not str(source).startswith(source_prefix):
                report.error("manifest_source_prefix", source_manifest, f"{source} must start with {source_prefix}")
            if not str(destination).startswith(dest_prefix):
                report.error("manifest_destination_prefix", source_manifest, f"{destination} must start with {dest_prefix}")
            if source in seen_sources:
                report.error("manifest_duplicate_source", source_manifest, f"Duplicate source entry: {source}")
            if destination in seen_destinations:
                report.error("manifest_duplicate_destination", source_manifest, f"Duplicate destination entry: {destination}")
            seen_sources.add(source)
            seen_destinations.add(destination)
            declared[section].add((str(source), str(destination)))
            source_path = root / str(source)
            dest_path = root / str(destination)
            if not source_path.exists():
                report.error("manifest_declared_source_missing", rel_path(root, source_path), "Manifest-declared source asset is missing")
            if not dest_path.exists():
                report.error("manifest_declared_destination_missing", rel_path(root, dest_path), "Manifest-declared destination asset is missing")
    return declared


def check_referenced_assets(root: Path, report: Report, declared):
    if declared is None:
        return
    asset_pattern = re.compile(r"\.codestable/(reference|tools)/([A-Za-z0-9._/-]+)")
    seen = set()
    for path in collect_reference_scan_files(root):
        text, err = read_text(path)
        if err:
            report.error("read_error", rel_path(root, path), err)
            continue
        for section, name in asset_pattern.findall(text or ""):
            if not name or name in PLACEHOLDER_NAMES or "{" in name or "}" in name:
                continue
            destination = f".codestable/{section}/{name}"
            source = f"cs-onboard/{section}/{name}"
            key = (source, destination)
            if key in seen:
                continue
            seen.add(key)
            source_path = root / source
            dest_path = root / destination
            if not source_path.exists() or not dest_path.exists():
                report.error(
                    "shared_asset_missing",
                    rel_path(root, path),
                    f"Referenced shared asset {destination} is missing from source bundle or project bundle",
                )
            section_name = "references" if section == "reference" else "tools"
            if key not in declared.get(section_name, set()):
                report.error(
                    "manifest_parity",
                    rel_path(root, path),
                    f"Referenced shared asset {destination} is not declared in shared-asset-manifest.yaml",
                )


def check_path_contract(root: Path, report: Report):
    pattern = re.compile(r"(?<!\.)codestable/")
    for path in existing_paths(root, ACTIVE_PUBLIC_DOCS):
        text, err = read_text(path)
        if err:
            report.error("read_error", rel_path(root, path), err)
            continue
        for line_number, line in enumerate((text or "").splitlines(), start=1):
            if pattern.search(line):
                report.error(
                    "path_contract",
                    f"{rel_path(root, path)}:{line_number}",
                    "Found codestable/ path that conflicts with the canonical .codestable/ contract",
                )


def check_feature_flow_wording(root: Path, report: Report):
    forbidden = {
        "README.md": [OLD_FLOW_ZH],
        "README.en.md": [OLD_FLOW_EN],
        "cs/SKILL.md": ["`cs-feat-design` → `cs-feat-impl` → `cs-feat-accept`"],
        "docs/dev/feature-workflow.md": ["`cs-feat-design → cs-feat-impl → cs-feat-accept`"],
    }
    for rel, expected_strings in FEATURE_FLOW_EXPECTATIONS.items():
        path = root / rel
        if not path.exists():
            continue
        text, err = read_text(path)
        if err:
            report.error("read_error", rel, err)
            continue
        for expected in expected_strings:
            if expected not in (text or ""):
                report.error("feature_flow_wording", rel, f"Missing canonical active feature-flow wording: {expected}")
        for bad in forbidden.get(rel, []):
            if bad in (text or ""):
                report.error("feature_flow_wording", rel, f"Found outdated feature-flow wording: {bad}")


def check_markdown_line_limit(root: Path, report: Report):
    for path in collect_line_limit_docs(root):
        text, err = read_text(path)
        if err:
            report.error("read_error", rel_path(root, path), err)
            continue
        lines = (text or "").count("\n") + 1
        if lines > report.line_limit:
            report.error(
                "markdown_line_limit",
                rel_path(root, path),
                f"{lines} lines exceeds the repository markdown limit of {report.line_limit}",
            )


def check_legacy_features(root: Path, report: Report):
    feature_root = root / ".codestable/features"
    if not feature_root.is_dir():
        return
    for feature_dir in sorted(path for path in feature_root.iterdir() if path.is_dir() and not path.name.startswith(".")):
        design_files = sorted(feature_dir.glob("*-design.md"))
        if not design_files:
            continue
        plan_exists = any(feature_dir.glob("*-plan.md"))
        checklist_exists = any(feature_dir.glob("*-checklist.yaml"))
        acceptance_exists = any(feature_dir.glob("*-acceptance.md"))
        for design_path in design_files:
            text, err = read_text(design_path)
            if err:
                report.error("read_error", rel_path(root, design_path), err)
                continue
            meta, body = parse_frontmatter(text or "")
            sample_feature = is_sample_feature(feature_dir, meta, body)
            workflow = meta.get("workflow")
            if workflow == "hybrid":
                if not plan_exists:
                    if sample_feature:
                        report.warn(
                            "sample_feature_compat",
                            rel_path(root, design_path),
                            "Sample/example feature missing plan.md is treated as a compatibility warning at repository scope",
                        )
                    else:
                        report.error(
                            "feature_plan_presence",
                            rel_path(root, design_path),
                            "Active hybrid feature is missing plan.md",
                        )
                if not checklist_exists:
                    if sample_feature:
                        report.warn(
                            "sample_feature_compat",
                            rel_path(root, design_path),
                            "Sample/example feature missing checklist.yaml is treated as a compatibility warning at repository scope",
                        )
                    else:
                        report.error(
                            "feature_checklist_presence",
                            rel_path(root, design_path),
                            "Active hybrid feature is missing checklist.yaml",
                        )
            elif workflow == "legacy":
                report.warn(
                    "legacy_feature_compat",
                    rel_path(root, design_path),
                    "Legacy workflow is treated as compatibility-mode history, not active failure",
                )
            elif workflow is None:
                if plan_exists:
                    if sample_feature:
                        report.warn(
                            "sample_feature_compat",
                            rel_path(root, design_path),
                            "Sample/example feature with plan.md but no workflow is treated as a compatibility warning at repository scope",
                        )
                    else:
                        report.error(
                            "feature_workflow_missing",
                            rel_path(root, design_path),
                            "Feature has plan.md but design frontmatter is missing workflow: hybrid",
                        )
                elif checklist_exists or acceptance_exists:
                    report.warn(
                        "legacy_feature_compat",
                        rel_path(root, design_path),
                        "Historical feature missing workflow/plan is treated as a compatibility warning",
                    )
            else:
                report.error(
                    "design_workflow",
                    rel_path(root, design_path),
                    f"Unexpected workflow value: {workflow}",
                )


def print_text_report(report: Report, line_limit_sources):
    print(f"Checked workflow contracts at {report.repo_root}")
    if line_limit_sources:
        rendered = ", ".join(f"{path}={limit}" for path, limit in line_limit_sources)
        print(f"Markdown line limit: {report.line_limit} ({rendered})")
    else:
        print(f"Markdown line limit: {report.line_limit}")
    print(f"Errors: {report.error_count}, warnings: {report.warning_count}\n")
    for finding in report.findings:
        level = "ERROR" if finding.level == "error" else "WARN"
        print(f"[{level}] {finding.rule} :: {finding.path}")
        print(f"  {finding.message}")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only validator for CodeStable workflow contracts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo-root", default=".", help="Repository root to validate (default: current directory)")
    parser.add_argument("--line-limit", type=int, default=None, help="Override detected markdown line limit")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output findings as JSON")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = Path(args.repo_root).resolve()
    line_limit, line_limit_sources = detect_line_limit(root, args.line_limit)
    report = Report(root, line_limit)
    declared = check_manifest_parity(root, report)
    check_referenced_assets(root, report, declared)
    check_path_contract(root, report)
    check_feature_flow_wording(root, report)
    check_markdown_line_limit(root, report)
    check_legacy_features(root, report)

    if args.json_output:
        payload = report.to_dict()
        payload["lineLimitSources"] = [
            {"path": path, "limit": limit} for path, limit in line_limit_sources
        ]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_text_report(report, line_limit_sources)
    sys.exit(0 if report.ok else 1)


if __name__ == "__main__":
    main()
