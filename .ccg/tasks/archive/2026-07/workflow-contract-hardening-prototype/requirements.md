# Requirements — workflow-contract-hardening-prototype

## Goal
Eliminate repeated confirmation loops in the CodeStable skill workflow by making human checkpoint results canonical and machine-consumable, while preserving safety-critical approvals.

## Required behavior
1. A unique, fresh, blocker-free continuation must route directly and must not fall through to the generic “switch skill?” prompt.
2. Feature design approval, feature plan approval, issue fix-option selection, scope expansion, ambiguity, and conflicts remain explicit human gates.
   Once a required gate is approved and persisted, the same reply must immediately hand off to the unique next stage; a second “continue?” prompt is forbidden.
3. Feature plan approval is persisted in `{slug}-plan.md` as `status: approved`; implementation may auto-continue only after that state exists.
4. A draft issue report remains in `cs-issue-report`; only `status: confirmed` may route to `cs-issue-analyze`.
5. `cs-feat-design` must not require plan-stage artifacts in its exit conditions.
6. Generated status remains advisory and derives transitions only from canonical `.codestable/` artifacts; `.ccg/tasks/**` must not affect output.
7. Source and onboarding copies of generated-state tooling must remain identical.

## Non-goals
- Removing mandatory design/plan/fix-option approvals.
- Making `.ccg/tasks/**` a workflow authority.
- Adding a new runtime dispatcher or changing unrelated workflow lanes.

## Validation
- Automated transition tests for draft/approved feature plans and draft/confirmed issue reports.
- Determinism and `.ccg` non-authority regression test.
- Skill-text contract tests for direct continuation, plan status persistence, draft report routing, and design-stage ownership.
- Existing status builder and workflow-contract validator checks.
