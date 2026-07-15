# Review — sync-local-workflow-skills

## Result
- Synced 11 workflow skills from the repository to the effective local targets under `~/.agents/skills/`.
- `~/.claude/skills/<skill>` symlinks resolve to those targets.
- `diff -qr` confirmed every installed skill exactly matches its repository source.
- A second sync dry-run completed with no reported differences.

## Skills
`cs`, `cs-feat`, `cs-feat-accept`, `cs-feat-design`, `cs-feat-impl`, `cs-feat-plan`, `cs-issue`, `cs-issue-report`, `cs-issue-analyze`, `cs-issue-fix`, `cs-onboard`.
