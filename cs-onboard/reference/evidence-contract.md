# Workflow Evidence Contract

## Scope

`evidence_contract: v1` is an opt-in contract for newly created workflow
artifacts. It adds machine-checkable verification evidence without requiring a
bulk migration of legacy artifacts.

Use it for new feature/refactor checklists and new completed acceptance or
fix-note reports. Existing artifacts remain readable compatibility history.

## Checklist Format

A v1 checklist declares the contract at top level:

```yaml
evidence_contract: v1
```

Every `steps` and `checks` item has:

- `id` — stable local identifier
- `status` — `pending`, `done`, `passed`, or `failed` as appropriate
- `verification` — method and expected observation
- `evidence` — result, verifier, and verification time

Minimal shape:

```yaml
steps:
  - id: step-1
    action: "Implement the slice"
    exit_signal: "The behaviour is available"
    verification:
      method: command
      expected: "Focused tests pass"
    evidence:
      result: pending
      verified_at: null
      verified_by: null
    status: pending
```

When an item becomes `done` or `passed`, its evidence must contain a concrete
non-`pending` result, `verified_at: YYYY-MM-DD`, and `verified_by: ai | user |
ci`. A command result should include the command and exit code in the result;
manual/browser validation should name the observed path or scenario.

## Completion Reports

An opt-in `feature-acceptance` or `issue-fix` report uses
`evidence_contract: v1` in frontmatter and contains:

- `## 验证证据` — command/observation, result, verifier, and date
- `## 遗留风险` — explicit `无` is allowed only after review

Never include credentials, tokens, or private production data in evidence.

## Validation

Run:

```bash
python .codestable/tools/check-workflow-evidence.py
```

The tool only validates opt-in artifacts. This allows new work to ratchet up
quality while historical records keep their original contract. CI runs the
same checker through `scripts/verify.sh`.
