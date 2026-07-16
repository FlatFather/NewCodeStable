<div align="center">

# CodeStable

![](./asset/PromotionalImage.png)

**English** · [中文](./README.md)

**An AI coding workflow for serious software engineering**

<p>
  <img src="https://img.shields.io/badge/status-beta-F59E0B?style=flat-square" alt="Status"/>
  <img src="https://img.shields.io/badge/skills-22-6366F1?style=flat-square" alt="Skills"/>
  <img src="https://img.shields.io/badge/license-MIT-10B981?style=flat-square" alt="License"/>
</p>

</div>

---

## Install

```bash
npx skills add https://github.com/FlatFather/NewCodeStable
```

For local development against the latest working tree:

```bash
npx skills add "/Users/kong/self/github/NewCodeStable"
```

Upgrade:

```bash
npx skills update
```

---

## Maintenance and verification

After changing a workflow, run the unified quality gate:

```bash
./scripts/verify.sh
```

The script uses a repository-local temporary directory and checks generated state, workflow contracts, skill exit conditions, and Python regression tests. Set `PYTHON_BIN` to select an interpreter.

---

## How to start

### New repo / not onboarded yet

```bash
/cs-onboard
```

### Already onboarded, but don't know which skill fits

```bash
/cs
```

`cs` does one thing: route your intent to the right `cs-*` skill.

---

## What CodeStable is

CodeStable does **not** orchestrate agent teams first. It orchestrates the **lifecycle of the software itself**.

Requirements, architecture, features, issues, refactors, audits, and knowledge artifacts are all grounded in the project-local **`.codestable/`** workspace so both humans and AI can read the same engineering state.

### Authority boundaries

- **canonical state**: formal artifacts under `.codestable/`
- **generated state**: `.codestable/status.json`, used only for discovery / routing acceleration
- **bridge hints**: `.ccg/tasks/*/task.json`, used only for recovery hints

In short: **canonical artifacts always outrank generated state and bridge hints**.

Normative definition:
- [`.codestable/reference/workflow-contract.md`](./.codestable/reference/workflow-contract.md)

---

## Workflow at a glance

### Standard lanes

| Scenario | Lane |
|---|---|
| New feature | `cs-feat-design → cs-feat-plan → cs-feat-impl → cs-feat-accept` |
| Bug fix | `cs-issue-report → cs-issue-analyze → cs-issue-fix` |
| Refactor | `cs-refactor` (standard 3-stage flow: scan → design → apply) |
| Proactive problem scan | `cs-audit` |

### Fast paths

- `cs-feat-ff`: feature fastforward for small requests
- `cs-refactor-ff`: refactor fastforward for small, behavior-preserving changes

### Discussion / planning entry

- `cs-brainstorm`: triage when the idea is still fuzzy
- `cs-roadmap`: break down large work before splitting into sub-features

> Fastforward only holds inside low-complexity boundaries. Once thresholds are exceeded, it auto-normalizes back to the standard lane. See the workflow guides and terminology doc for details.

---

## Common entry points

| What you want to do | Start here |
|---|---|
| Onboard CodeStable | `cs-onboard` |
| Don't know which skill to use | `cs` |
| Build a new feature | `cs-feat` |
| Fix a bug | `cs-issue` |
| Run a refactor | `cs-refactor` |
| Scan for problems first | `cs-audit` |
| Explore how code works | `cs-explore` |
| Record decisions / lessons / tricks | `cs-decide` / `cs-learn` / `cs-trick` |

---

## Read next

### Normative references

- [`.codestable/reference/workflow-contract.md`](./.codestable/reference/workflow-contract.md) — truth source, continuation, generated state, distribution
- [`.codestable/reference/system-overview.md`](./.codestable/reference/system-overview.md) — full CodeStable system map
- [`.codestable/reference/terminology.md`](./.codestable/reference/terminology.md) — feature / issue / fastforward routing criteria
- [`.codestable/reference/status-schema.md`](./.codestable/reference/status-schema.md) — `status.json` schema

### Workflow guides

- [`docs/dev/feature-workflow.md`](./docs/dev/feature-workflow.md)
- [`docs/dev/issue-workflow.md`](./docs/dev/issue-workflow.md)
- [`docs/dev/refactor-workflow.md`](./docs/dev/refactor-workflow.md)

---

## Why this design

Many AI coding frameworks optimize for: **how to orchestrate agents better**.

CodeStable optimizes for: **how to keep serious software engineering state, constraints, decisions, and history readable, recoverable, and reusable over time**.

So the defaults are:
- human-in-the-loop
- docs and code are both engineering state
- staged workflows with checkpoints instead of letting AI skip straight to the end

---

<div align="center">

MIT License · by [@liuzhengdong](https://github.com/liuzhengdongfortest)

</div>
