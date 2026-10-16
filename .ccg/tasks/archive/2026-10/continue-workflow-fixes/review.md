# Review

## Scope of Fixes

1. `workflow-routing.py`: unique candidates with active blockers or user decision gates now return `action: ask_user` with the candidate, `next_skill`, and blockers intact, preventing premature fallback to standard routing.
2. `sync-skills.sh`: resolved destinations are verified against the physical canonical path of allowed roots, preventing subfolder symlinks from escaping the whitelist.
3. `check-workflow-contracts.py`: expired warning baseline dates (`review_after`) now fail as errors instead of passive warnings.

## Verification

- `./scripts/verify.sh` passed.
- 48 unit tests passed, including new regressions for symlink escapes, blocked candidate preservation, and expired baselines.
- Shared onboarding tools match canonical tools exactly.
