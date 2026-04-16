# GitHub Repo Setup Instructions

## Goal

Create the first controlled GitHub repositories for the official MCP toxic-flow
reproduction.

These instructions assume we are creating two repositories:

- one public repository
- one private repository

The content seeds live under:

- [public_repo_seed](/d:/ens491/mcp_attack_lab/fixtures/data/github_official/public_repo_seed)
- [private_repo_seed](/d:/ens491/mcp_attack_lab/fixtures/data/github_official/private_repo_seed)
- [issue_seeds](/d:/ens491/mcp_attack_lab/fixtures/data/github_official/issue_seeds)

## Suggested Repository Names

- public: `gh-toxic-flow-public-lab`
- private: `gh-toxic-flow-private-lab`

## Step 1: Create The Public Repository

- Create a new public repository on GitHub.
- Enable issues.
- Add the files from `public_repo_seed/`.
- Push the first commit.

## Step 2: Create The Private Repository

- Create a new private repository on GitHub.
- Add the files from `private_repo_seed/`.
- Push the first commit.

## Step 3: Open The Malicious Issue

Choose one of the issue seeds:

- [issue-001-malicious-comment-sink.md](/d:/ens491/mcp_attack_lab/fixtures/data/github_official/issue_seeds/issue-001-malicious-comment-sink.md)
- [issue-002-malicious-pr-sink.md](/d:/ens491/mcp_attack_lab/fixtures/data/github_official/issue_seeds/issue-002-malicious-pr-sink.md)

Recommended first choice:

- `issue-001-malicious-comment-sink.md`

Reason:

- comment sink is easier to observe and clean up than a PR workflow

## Step 4: Record Baseline Metadata

Before running the client:

- save public repo URL
- save private repo URL
- save issue URL
- save commit SHA from public repo
- save commit SHA from private repo
- save exact canary string

## Step 5: Prepare The Official GitHub MCP Configuration

Follow the official GitHub MCP setup using:

- [github-mcp-official-testbed-spec.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-mcp-official-testbed-spec.md)
- [github-mcp-client-selection.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-mcp-client-selection.md)
- [github-mcp-run-checklist.md](/d:/ens491/mcp_attack_lab/research/checklists/github-mcp-run-checklist.md)

## Recommended First Official Run

- client: `VS Code 1.101+`
- server: `official local GitHub MCP server`
- sink: `issue comment`
- issue seed: `issue-001-malicious-comment-sink.md`

## Why Start With Comment Sink

- easiest cleanup
- simpler audit trail
- lower ceremony than PR creation
- enough to prove public write and exact canary leak
