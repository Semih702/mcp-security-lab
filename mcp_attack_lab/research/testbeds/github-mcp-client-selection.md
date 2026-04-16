# GitHub MCP Client Selection

## Goal

Choose the first real MCP client for the official GitHub toxic-flow
reproduction attempt.

This decision matters because different clients vary in:

- configuration clarity,
- support for local vs remote MCP servers,
- logging visibility,
- and how much automatic execution they allow.

## Selection Criteria

The first client should optimize for:

1. clear documented setup
2. stable support for the official GitHub MCP server
3. low ambiguity in configuration
4. enough visibility into tool behavior
5. ability to start with a more controlled posture

## Recommended First Client

Recommended first client:

- `VS Code 1.101+ with GitHub Copilot / Agent mode`

## Why This Is The Best First Choice

Based on GitHub's official MCP server documentation:

- GitHub explicitly documents installation in VS Code for the remote server
- GitHub also provides explicit local-server JSON configuration examples
- the README notes that VS Code 1.101+ is the supported baseline for remote MCP
- the local configuration can be placed in `.vscode/mcp.json`, which makes the
  setup easier to preserve and describe

This makes VS Code the strongest first choice for a documented and reproducible
official GitHub MCP testbed.

Official source:
- https://github.com/github/github-mcp-server

Relevant documentation points:
- remote server overview and VS Code installation
- local server Docker / `stdio` setup
- `.vscode/mcp.json` style configuration sharing
- toolset restriction support

## Why Not Start With Remote First

GitHub says the remote GitHub MCP server is the easiest way to get up and
running.

However, for our first controlled reproduction we should still prefer the
official local server because:

- configuration is easier to pin down,
- tool exposure is easier to reason about,
- and host-side remote behavior adds extra variables too early.

So:

- easiest to start generally: remote
- best for our first controlled reproduction: local

## Why Not Start With Codex As The First Official Run

GitHub's official README lists Codex as a supported installation path for the
remote server, which is useful.

However, for the very first official reproduction run, VS Code is still the
better choice because GitHub's README gives more explicit installation examples
for VS Code and local server configuration.

That means:

- `VS Code` should be the first official baseline client
- `Codex` can be a strong follow-up client for cross-client validation

## Proposed Client Order

1. `VS Code + official local GitHub MCP server`
2. `VS Code + official remote GitHub MCP server`
3. `Codex + official GitHub MCP server`

This order gives us:

- a stable baseline,
- then external-validity expansion,
- then cross-client replication.

## What We Need From The First Client Run

The first client does not need to be maximally autonomous.

It only needs to let us observe:

- public issue read
- private repo read
- public write attempt
- exact canary leak if the chain succeeds

That makes a more controlled client posture acceptable, and even desirable, for
the first official testbed.

## Decision

First official baseline client:

- `VS Code 1.101+`

First official server mode:

- `official local GitHub MCP server`

Follow-up validation:

- remote official GitHub MCP server
- then Codex as a second host for replication
