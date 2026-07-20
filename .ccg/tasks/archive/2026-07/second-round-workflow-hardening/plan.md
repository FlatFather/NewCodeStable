# Implementation Plan

External planning was attempted in parallel. Antigravity is unavailable (`agy` missing) and Claude did not return before timeout, so this plan is based on direct repository inspection.

1. Make `scripts/verify.sh` CI-safe and source-oriented; add GitHub Actions.
2. Add shared `check-ccg-tasks.py` with active/archive lifecycle validation and a controlled legacy baseline.
3. Harden warning baseline validation for duplicates, stale entries, missing targets, and review dates.
4. Add `scripts/check-model-backends.sh` with bounded probes and explicit degraded exit semantics.
5. Introduce shared `workflow-routing.py` as a pure executable decision helper and test multi-candidate/stale/conflict/blocker cases.
6. Extend `sync-skills.sh` with `--target claude|agents|all`, safer exact-root checks, physical-target reporting, and platform diagnostics.
7. Update shared manifests/docs, run complete tests, dual review attempt, archive task.
