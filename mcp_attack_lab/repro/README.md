# Reproducibility Guide

This folder is for rebuilding the controlled GitHub testbed from scratch.

The goal is not only to document what was done once, but to allow another
researcher to create the same style of environment again.

## What Is Here

- [github_testbed_manifest.example.json](/d:/ens491/mcp_attack_lab/repro/github_testbed_manifest.example.json)
  - example manifest describing the public repo, private repo, and issue seed
- [../scripts/bootstrap_github_testbed.py](/d:/ens491/mcp_attack_lab/scripts/bootstrap_github_testbed.py)
  - bootstrap entrypoint

## What The Bootstrap Script Does

Given a manifest and a GitHub token, the bootstrap flow can:

- create the public repository
- create the private repository
- copy the seed repository contents
- initialize local clones
- push the first commit to GitHub
- create the malicious issue from a seed file
- write metadata describing the created assets

## Typical Usage

1. Copy the example manifest and adjust:
   - GitHub owner
   - local workspace path
   - repo names if needed
2. Ensure `GITHUB_PERSONAL_ACCESS_TOKEN` is available or stored in Git
   Credential Manager.
3. Run:

```bash
cd mcp_attack_lab
python scripts/bootstrap_github_testbed.py --manifest repro/github_testbed_manifest.example.json
```

## Output

The bootstrap writes a metadata artifact under `results/` that records:

- repository names
- repository URLs
- issue number and URL
- local workspace paths
- manifest used

## Scope

This automation is designed for:

- user-owned repositories
- harmless lab canaries
- controlled security evaluation

It is not intended for third-party targets or unsanctioned testing.
