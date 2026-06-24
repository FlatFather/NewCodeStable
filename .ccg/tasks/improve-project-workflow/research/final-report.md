# Workflow improvement report

Scope note: per user instruction, this report is synthesized from the Codex analysis plus direct repository evidence read by Claude. A later Gemini run succeeded in the background, but it is not used as the basis of this report.

## Executive summary
NewCodeStable's problem is no longer lack of workflow concepts; it is contract drift. The repository already has enough lanes, gates, and shared references. What is missing is a single canonical contract for feature flow, onboarding assets, continuation/state, and maintenance validation. The fastest leverage comes from tightening those contracts before adding more workflow surface.

## Highest-priority improvements
1. Finish the feature-flow migration to a single canonical chain.
2. Align public documentation with the actual runtime model (`.codestable/`, active entities, active lanes).
3. Bring `cs-onboard`'s shipped reference bundle up to the level required by current skills.
4. Collapse continuation/state handling into one generated source of truth.
5. Shrink the cognitive load of the `cs` root router.
6. Normalize the fastforward contract across feature/refactor lanes.
7. Replace re-entry after checkpoints with direct next-step continuation guidance.
8. Add repo self-tests for referenced files, workflow-chain consistency, and markdown size limits.

## Recommended sequence
- Quick wins: fix doc drift, onboarding bundle drift, checkpoint UX, and automated consistency checks.
- Structural: add a generated workflow status index, continuation contract normalization, and issue/refactor dev guides.
- Architecture: move routing/continuation/progress to a shared machine-readable state model.
