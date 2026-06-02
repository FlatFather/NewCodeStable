#!/usr/bin/env python3
"""
validate-yaml.py — Validate YAML frontmatter syntax in markdown files.

Scans markdown files for YAML frontmatter (--- ... ---) and checks:
  1. Frontmatter block is properly delimited (opening and closing ---)
  2. YAML syntax is valid (parseable without errors)
  3. (Optional) Required fields are present (--require flag)

Designed for AI agent use: structured output, exit code reflects pass/fail,
no required external dependencies (falls back to builtin parser if PyYAML unavailable).

Usage examples:
  # Validate all .md files under codestable/features
  python codestable/tools/validate-yaml.py --dir codestable/features

  # Validate a single file
  python codestable/tools/validate-yaml.py --file codestable/features/2026-04-11-auth/auth-design.md

  # Check that required fields exist in frontmatter
  python codestable/tools/validate-yaml.py --dir codestable/features --require doc_type --require status

  # JSON output for programmatic consumption
  python codestable/tools/validate-yaml.py --dir docs/api --json

  # Validate the libdoc manifest
  python codestable/tools/validate-yaml.py --file docs/api/manifest.yaml --yaml-only
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Force UTF-8 stdout/stderr on Windows where default codepage (e.g. GBK / cp936)
# can't encode the ✓ / ✗ icons used in text output. Safe no-op on POSIX.
# Streams that aren't a real TextIOWrapper (e.g. captured by pytest, redirected
# through some IDEs) raise io.UnsupportedOperation — a ValueError + OSError
# subclass — and we just leave the original encoding in place.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass


# ---------------------------------------------------------------------------
# YAML parsing
# ---------------------------------------------------------------------------

_HAS_PYYAML = False
try:
    import yaml  # type: ignore
    _HAS_PYYAML = True
except ImportError:
    pass


def _builtin_parse_yaml(text: str) -> dict:
    """Minimal YAML parser for flat key-value frontmatter (no nested structures)."""
    result: dict = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, raw = stripped.partition(":")
        val = raw.strip()
        # Inline list
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            result[key.strip()] = [
                item.strip().strip("'\"") for item in inner.split(",") if item.strip()
            ]
        else:
            result[key.strip()] = val.strip("'\"") if val else ""
    return result


def parse_yaml_text(text: str) -> tuple[dict | None, str | None]:
    """
    Parse a YAML string. Returns (parsed_dict, None) on success,
    or (None, error_message) on failure.
    """
    if _HAS_PYYAML:
        try:
            result = yaml.safe_load(text)
            if result is None:
                return {}, None
            if not isinstance(result, dict):
                return None, f"Expected a mapping, got {type(result).__name__}"
            return result, None
        except yaml.YAMLError as exc:
            return None, str(exc)
    else:
        # Builtin fallback — can only detect gross syntax issues
        try:
            result = _builtin_parse_yaml(text)
            return result, None
        except Exception as exc:
            return None, str(exc)


# ---------------------------------------------------------------------------
# Frontmatter extraction
# ---------------------------------------------------------------------------

def extract_frontmatter(text: str) -> tuple[str | None, str | None]:
    """
    Extract YAML frontmatter from a markdown file.
    Returns (frontmatter_text, None) on success,
    or (None, error_message) if frontmatter is missing or malformed.
    """
    if not text.startswith("---"):
        return None, "No opening '---' delimiter found"

    end = text.find("\n---", 3)
    if end == -1:
        return None, "No closing '---' delimiter found (frontmatter block not terminated)"

    fm_text = text[3:end].strip()
    if not fm_text:
        return None, "Frontmatter block is empty"

    return fm_text, None


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------

class ValidationResult:
    def __init__(self, file_path: str):
        self.file = file_path
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.fields: list[str] = []  # fields found in frontmatter
        self.rule_results: list[dict[str, str]] = []

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def add_rule_error(self, rule: str, file_path: str, message: str) -> None:
        self.rule_results.append({"rule": rule, "file": file_path, "message": message})
        self.errors.append(f"RULE {rule}: {file_path} — {message}")

    def to_dict(self) -> dict:
        d: dict = {"file": self.file, "status": "pass" if self.ok else "fail"}
        if self.errors:
            d["errors"] = self.errors
        if self.warnings:
            d["warnings"] = self.warnings
        if self.fields:
            d["fields"] = self.fields
        if self.rule_results:
            d["rule_results"] = self.rule_results
        return d


def _check_required(parsed: dict | None, required_fields: list[str] | None, result: ValidationResult) -> None:
    if not required_fields:
        return
    for field in required_fields:
        if field not in (parsed or {}):
            result.errors.append(f"Missing required field: '{field}'")


def _warn_if_builtin(result: ValidationResult) -> None:
    if not _HAS_PYYAML:
        result.warnings.append(
            "PyYAML not installed — using builtin fallback parser "
            "(may miss some syntax errors). Install with: pip install pyyaml"
        )


def _validate_file(
    file_path: Path,
    required_fields: list[str] | None,
    base_dir: Path | None,
    mode: str,  # "markdown" | "yaml"
) -> ValidationResult:
    display_path = str(file_path.relative_to(base_dir)) if base_dir else str(file_path)
    result = ValidationResult(display_path)

    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        result.errors.append(f"Cannot read file: {exc}")
        return result

    if mode == "markdown":
        yaml_text, extract_err = extract_frontmatter(text)
        if extract_err:
            result.errors.append(extract_err)
            return result
    else:
        yaml_text = text

    parsed, parse_err = parse_yaml_text(yaml_text)
    if parse_err:
        result.errors.append(f"YAML syntax error: {parse_err}")
        return result

    result.fields = list(parsed.keys()) if parsed else []
    _check_required(parsed, required_fields, result)
    _warn_if_builtin(result)
    return result


def validate_markdown_file(file_path, required_fields=None, base_dir=None):
    """Validate YAML frontmatter in a single markdown file."""
    return _validate_file(file_path, required_fields, base_dir, "markdown")


def validate_yaml_file(file_path, required_fields=None, base_dir=None):
    """Validate a pure YAML file (not markdown with frontmatter)."""
    return _validate_file(file_path, required_fields, base_dir, "yaml")


def _read_frontmatter_file(file_path: Path) -> tuple[dict | None, str | None]:
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"Cannot read file: {exc}"

    yaml_text, extract_err = extract_frontmatter(text)
    if extract_err:
        return None, extract_err

    parsed, parse_err = parse_yaml_text(yaml_text)
    if parse_err:
        return None, f"YAML syntax error: {parse_err}"
    return parsed or {}, None


def _infer_feature_kind(design_data: dict, has_plan: bool) -> str:
    if has_plan:
        return "hybrid"
    return "legacy"


def _parse_plan_steps(text: str) -> list[str]:
    return re.findall(r"^###\s+Step\s+\d+\s+—\s+(.+)$", text, re.MULTILINE)


def _extract_checklist_actions(text: str) -> list[str]:
    return re.findall(r'^\s*-\s+action:\s+"([^"]+)"$', text, re.MULTILINE)


def _extract_roadmap_item_feature(text: str, item_slug: str) -> str | None:
    pattern = re.compile(
        rf"^\s*-\s+slug:\s+{re.escape(item_slug)}\s*$([\s\S]*?)(?=^\s*-\s+slug:|\Z)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return None
    block = match.group(1)
    feature_match = re.search(r"^\s+feature:\s+(.+)$", block, re.MULTILINE)
    if not feature_match:
        return None
    value = feature_match.group(1).strip()
    return None if value == "null" else value


def _workflow_check(feature_dir: Path, roadmap_file: Path | None) -> list[ValidationResult]:
    result = ValidationResult(str(feature_dir))
    design_files = sorted(feature_dir.glob("*-design.md"))
    checklist_files = sorted(feature_dir.glob("*-checklist.yaml"))
    plan_files = sorted(feature_dir.glob("*-plan.md"))

    if len(design_files) != 1:
        result.add_rule_error("design_file", str(feature_dir), "Expected exactly one *-design.md file")
        return [result]
    if len(checklist_files) != 1:
        result.add_rule_error("checklist_file", str(feature_dir), "Expected exactly one *-checklist.yaml file")
        return [result]

    design_file = design_files[0]
    checklist_file = checklist_files[0]
    plan_file = plan_files[0] if plan_files else None

    design_data, design_err = _read_frontmatter_file(design_file)
    if design_err:
        result.add_rule_error("design_frontmatter", str(design_file), design_err)
        return [result]

    checklist_data, checklist_err = _validate_file(checklist_file, None, feature_dir, "yaml"), None
    if not checklist_data.ok:
        result.errors.extend(checklist_data.errors)
        result.warnings.extend(checklist_data.warnings)
        return [result]

    feature_name = design_data.get("feature", "")
    workflow = design_data.get("workflow", "legacy")
    if workflow not in ("legacy", "hybrid"):
        result.add_rule_error("design_workflow", str(design_file), "workflow must be 'legacy' or 'hybrid'")
    feature_kind = workflow if workflow in ("legacy", "hybrid") else _infer_feature_kind(design_data, plan_file is not None)

    plan_data: dict | None = None
    if plan_file is not None:
        plan_data, plan_err = _read_frontmatter_file(plan_file)
        if plan_err:
            result.add_rule_error("plan_frontmatter", str(plan_file), plan_err)
        else:
            for field in ("doc_type", "feature", "design", "status"):
                if field not in plan_data:
                    result.add_rule_error("plan_frontmatter", str(plan_file), f"Missing required field '{field}'")
            if plan_data.get("doc_type") != "feature-plan":
                result.add_rule_error("plan_frontmatter", str(plan_file), "doc_type must be 'feature-plan'")
            if plan_data.get("feature") != feature_name:
                result.add_rule_error("binding_rule", str(plan_file), "plan.feature must equal design.feature")
            if plan_data.get("design") != design_file.name:
                result.add_rule_error("binding_rule", str(plan_file), "plan.design must equal the design file name")

    if feature_kind == "hybrid" and plan_file is None:
        result.add_rule_error("plan_presence", str(design_file), "hybrid feature requires plan.md but it is missing")

    if feature_kind == "hybrid" and plan_file is not None:
        try:
            checklist_text = checklist_file.read_text(encoding="utf-8")
            checklist_steps = _extract_checklist_actions(checklist_text)
            if not checklist_steps:
                result.add_rule_error("step_alignment", str(checklist_file), "No checklist actions found")
            plan_text = plan_file.read_text(encoding="utf-8")
            plan_steps = _parse_plan_steps(plan_text)
            if len(plan_steps) != len(checklist_steps):
                result.add_rule_error("step_alignment", str(plan_file), "plan step count must equal checklist step count")
        except OSError as exc:
            result.add_rule_error("step_alignment", str(plan_file), f"Cannot read files: {exc}")

    if roadmap_file is not None:
        roadmap_result = _validate_file(roadmap_file, None, roadmap_file.parent, "yaml")
        if not roadmap_result.ok:
            result.errors.extend(roadmap_result.errors)
            result.warnings.extend(roadmap_result.warnings)
            return [result]
        roadmap_text = roadmap_file.read_text(encoding="utf-8")
        item_slug = design_data.get("roadmap_item")
        matched_feature = _extract_roadmap_item_feature(roadmap_text, item_slug)
        if matched_feature is None:
            result.add_rule_error("roadmap_binding", str(roadmap_file), f"No roadmap item or feature binding for slug '{item_slug}'")
        elif matched_feature != feature_name:
            result.add_rule_error("roadmap_binding", str(roadmap_file), "items.yaml feature must equal design.feature")

    _warn_if_builtin(result)
    return [result]


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_text_results(results: list[ValidationResult]) -> None:
    passed = sum(1 for r in results if r.ok)
    failed = len(results) - passed

    print(f"Validated {len(results)} file(s): {passed} passed, {failed} failed.\n")

    for r in results:
        icon = "✓" if r.ok else "✗"
        print(f"  {icon} {r.file}")
        for err in r.errors:
            print(f"      ERROR: {err}")
        for warn in r.warnings:
            print(f"      WARN:  {warn}")

    if failed > 0:
        print(f"\n{failed} file(s) have YAML errors.")
    else:
        print("\nAll files valid.")


def print_json_results(results: list[ValidationResult]) -> None:
    output = {
        "total": len(results),
        "passed": sum(1 for r in results if r.ok),
        "failed": sum(1 for r in results if not r.ok),
        "results": [r.to_dict() for r in results],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate YAML frontmatter in markdown files or pure YAML files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--dir", type=str, help="Directory to scan recursively for .md files")
    source.add_argument("--file", type=str, help="Single file to validate")
    source.add_argument("--feature-dir", type=str,
                        help="Feature directory to validate workflow contract (design/plan/checklist binding)")
    parser.add_argument("--roadmap", type=str,
                        help="Roadmap items YAML file used with --feature-dir for binding checks")
    parser.add_argument("--require", action="append", default=[], metavar="FIELD",
                        help="Require this field in frontmatter (repeatable)")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Output results as JSON")
    parser.add_argument("--yaml-only", action="store_true",
                        help="Treat input as pure YAML (not markdown with frontmatter). "
                             "Use for .yaml/.yml files like manifest.yaml.")
    parser.add_argument("--workflow-check", action="store_true",
                        help="Validate feature workflow contracts (design/plan/checklist/roadmap binding).")
    return parser


def _validate_single(path_str: str, require: list[str], yaml_only: bool) -> list[ValidationResult]:
    fp = Path(path_str)
    if not fp.exists():
        print(f"Error: File not found: {fp}", file=sys.stderr)
        sys.exit(2)
    if yaml_only or fp.suffix in (".yaml", ".yml"):
        return [validate_yaml_file(fp, require)]
    return [validate_markdown_file(fp, require)]


def _validate_directory(dir_str: str, require: list[str]) -> list[ValidationResult]:
    dp = Path(dir_str)
    if not dp.is_dir():
        print(f"Error: Directory not found: {dp}", file=sys.stderr)
        sys.exit(2)

    md_files = sorted(dp.rglob("*.md"))
    yaml_files = sorted(dp.rglob("*.yaml")) + sorted(dp.rglob("*.yml"))

    if not md_files and not yaml_files:
        print(f"No .md or .yaml files found under {dp}", file=sys.stderr)
        sys.exit(2)

    results = [validate_markdown_file(md, require, dp) for md in md_files]
    results += [validate_yaml_file(yf, require, dp) for yf in yaml_files]
    return results


def main() -> None:
    args = _build_parser().parse_args()

    if args.feature_dir:
        if not args.workflow_check:
            print("Error: --feature-dir requires --workflow-check", file=sys.stderr)
            sys.exit(2)
        roadmap_file = Path(args.roadmap) if args.roadmap else None
        results = _workflow_check(Path(args.feature_dir), roadmap_file)
    elif args.file:
        results = _validate_single(args.file, args.require, args.yaml_only)
    else:
        results = _validate_directory(args.dir, args.require)

    if args.json_output:
        print_json_results(results)
    else:
        print_text_results(results)

    sys.exit(0 if all(r.ok for r in results) else 1)


if __name__ == "__main__":
    main()
