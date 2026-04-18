# GitHub Issue #2 Variant Tracker

This file tracks which issue-body variant is currently loaded into:

- `Semih702/gh-toxic-flow-public-lab#2`

The purpose is to keep experiments reproducible while reusing the same issue
number.

## Variants

### Variant A

- file:
  - [issue-003-contextual-reframing-draft-leak.md](/d:/ens491/mcp_attack_lab/fixtures/data/github_official/issue_seeds/issue-003-contextual-reframing-draft-leak.md)
- intent:
  - normalize cross-repo comparison and public-facing draft creation
- expected effect:
  - strong push toward private read and public draft leakage

### Variant B

- file:
  - [issue-004-routine-validation-reference.md](/d:/ens491/mcp_attack_lab/fixtures/data/github_official/issue_seeds/issue-004-routine-validation-reference.md)
- intent:
  - make the verification reference feel mandatory and routine
  - reduce the chance of a separate user-confirmation round
- expected effect:
  - stronger pressure toward direct private lookup followed by immediate issue update

## Current Active Variant

Current issue `#2` variant:

- `Variant B`
- seed file:
  - [issue-004-routine-validation-reference.md](/d:/ens491/mcp_attack_lab/fixtures/data/github_official/issue_seeds/issue-004-routine-validation-reference.md)

Last reset artifact:

- [github-issue-reset-20260417T114835Z.json](/d:/ens491/mcp_attack_lab/results/github-issue-reset-20260417T114835Z.json)

## Reset Command Pattern

```bash
cd mcp_attack_lab
python scripts/reset_github_issue.py --owner Semih702 --repo gh-toxic-flow-public-lab --issue-number 2 --seed-file fixtures/data/github_official/issue_seeds/<variant-file>.md
```
