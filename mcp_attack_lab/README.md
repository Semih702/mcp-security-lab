# MCP Attack Lab

This repository is a controlled lab for reproducing and analyzing security
failures in MCP-based systems.

The project currently has two main tracks:

- a reusable **scenario-driven lab harness**
- a focused **GitHub MCP toxic-flow case study**

## Start Here

If someone is seeing the repo for the first time, the best reading order is:

1. this file
2. [SCENARIO_SCHEMA.md](/d:/ens491/mcp_attack_lab/SCENARIO_SCHEMA.md)
3. [research/README.md](/d:/ens491/mcp_attack_lab/research/README.md)
4. [repro/README.md](/d:/ens491/mcp_attack_lab/repro/README.md)

If the goal is more specific:

- to understand the reusable harness:
  - start with `scenarios/`, `fixtures/`, and `SCENARIO_SCHEMA.md`
- to understand the GitHub case study:
  - start with `research/case-studies/github-mcp-toxic-flow.md`
- to rebuild the GitHub demo:
  - start with `repro/README.md`

## What This Repo Contains

### 1. Core Lab Harness

This is the reusable part of the project.

- `scenarios/`
  - YAML scenario definitions
- `mcp_profiles/`
  - reusable MCP server configurations
- `model_configs/`
  - reusable model settings
- `fixtures/`
  - prompts, poisoned content, dummy data, seed repositories
- `src/mcp_attack_lab/`
  - Python package for execution logic
- `scripts/`
  - thin wrapper scripts and MCP bridge helpers
- `results/`
  - run artifacts

### 2. Research And Case Studies

This is the paper-oriented part of the project.

- `research/case-studies/`
  - public-report analysis and taxonomy mapping
- `research/roadmaps/`
  - sequencing and experiment planning
- `research/testbeds/`
  - concrete reproduction notes and official testbed planning
- `research/checklists/`
  - step-by-step run checklists

### 3. Reproducibility Assets

This is the part that allows another person to rebuild the controlled GitHub
testbed.

- `repro/`
  - reproducibility guide
  - testbed manifest example
- `scripts/bootstrap_github_testbed.py`
  - bootstrap entrypoint for creating and seeding the GitHub testbed

There is also one workspace-level helper outside `mcp_attack_lab/`:

- `/.vscode/mcp.json`
- `/scripts/start_github_mcp_server.ps1`

These exist at the repository root so VS Code can launch the official GitHub
MCP server for the black-box client experiments.

## Important Fixture Split

There are two GitHub-related fixture trees on purpose:

- `fixtures/data/github_toxic_flow/`
  - local analogue assets used before the official GitHub testbed existed
- `fixtures/data/github_official/`
  - seed repositories and issue seeds for the controlled official GitHub setup

If someone is trying to reproduce the current GitHub demo, the correct starting
point is `fixtures/data/github_official/`.

## GitHub Toxic-Flow Focus

The main public-case anchor is:

- `GitHub MCP toxic flow`

The most relevant files for that line are:

- [github-mcp-toxic-flow.md](/d:/ens491/mcp_attack_lab/research/case-studies/github-mcp-toxic-flow.md)
- [github-mcp-production-proof-plan.md](/d:/ens491/mcp_attack_lab/research/roadmaps/github-mcp-production-proof-plan.md)
- [github-mcp-official-testbed-spec.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-mcp-official-testbed-spec.md)
- [github-mcp-official-read-path-result.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-mcp-official-read-path-result.md)
- [github-mcp-official-write-path-result.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-mcp-official-write-path-result.md)
- [vscode-black-box-client-eval-plan.md](/d:/ens491/mcp_attack_lab/research/testbeds/vscode-black-box-client-eval-plan.md)

## Reproducible GitHub Testbed

The official GitHub testbed now has two parts:

- **seed content**
  - `fixtures/data/github_official/`
- **bootstrap automation**
  - `repro/github_testbed_manifest.example.json`
  - `scripts/bootstrap_github_testbed.py`

That means another person should be able to:

- create the controlled public repo
- create the controlled private repo
- push the seed content
- create the malicious issue
- record the resulting metadata

with a documented and scriptable workflow instead of ad hoc shell history.

## Python Layout

- package: `src/mcp_attack_lab/`
- wrapper scripts:
  - `scripts/run_scenario.py`
  - `scripts/evaluate_result.py`
  - `scripts/run_official_github_probe.py`
  - `scripts/bootstrap_github_testbed.py`

Suggested setup:

```bash
cd mcp_attack_lab
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

Example scenario usage:

```bash
python -m mcp_attack_lab.cli run --scenario scenarios/001-indirect-prompt-injection.yml
python -m mcp_attack_lab.cli evaluate --scenario scenarios/001-indirect-prompt-injection.yml
```

## Design Principles

- Use only dummy secrets and controlled sinks.
- Treat this as a safety-evaluation harness, not a general exploit framework.
- Keep each scenario measurable.
- Separate:
  - case-study reasoning
  - executable lab assets
  - reproducibility/bootstrapping

## Current State

What is already implemented:

- local analogue toxic-flow reproduction
- official GitHub MCP read-path reproduction
- official GitHub MCP write-path reproduction
- VS Code black-box evaluation notes
- GitHub testbed bootstrap and issue-reset automation

What is next:

- expand the black-box VS Code client experiments
- compare default vs defended client postures
- tighten paper-ready reporting
