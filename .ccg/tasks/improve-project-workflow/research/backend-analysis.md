# Backend analysis (Codex)

Source: Codex research run `019ef8e8-09bf-7e12-a229-aa3657df091f`.

## Executive summary
- NewCodeStable's core philosophy is strong: lifecycle-centered workflows, explicit checkpoints, and project-local shared references.
- The main weakness is workflow drift: multiple sources of truth, partial migration to `design → plan → impl → accept`, and shared references that skills expect but onboarding does not clearly provision.
- A second weakness is operational heaviness: many mandatory reads and manual recovery rules, without a compact machine-readable workflow state index.

## Key Codex findings
1. Unify the feature workflow source of truth.
2. Fix the reference provisioning gap introduced by split shared-conventions files.
3. Standardize continuation as a shipped contract, not a scattered convention.
4. Reduce root-entry cognitive load.
5. Add a machine-readable workflow state index.
6. Tighten skill size and modularity discipline.
7. Simplify the feature lane.
8. Bring issue/refactor lanes up to the same documentation maturity as the feature lane.
9. Clarify the boundary between project state and CCG task state.
10. Create a consistency test suite for the workflow repo itself.

## Recommended direction
Prefer a state-first hardening pass before larger workflow simplification: first unify contracts and recovery behavior, then reduce the visible workflow surface.
