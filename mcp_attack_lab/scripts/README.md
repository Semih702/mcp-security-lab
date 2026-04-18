# Scripts

These are operational entrypoints and helper bridges for the lab.

They are intentionally small, but they are no longer just placeholders.

## Main Entry Points

- `run_scenario.py`
  - run a scenario from the reusable YAML-based harness
- `evaluate_result.py`
  - evaluate a recorded scenario result
- `run_official_github_probe.py`
  - run the official GitHub MCP probe flow used in the GitHub toxic-flow work
- `bootstrap_github_testbed.py`
  - create and seed the controlled public/private GitHub repositories
- `reset_github_issue.py`
  - reset the reusable demo issue from a selected seed file

## MCP Bridge Helpers

- `mcp_filesystem_bridge.mjs`
  - bridge used for local filesystem MCP experiments
- `mcp_github_bridge.mjs`
  - bridge used for the official GitHub MCP experiments

## How To Read This Folder

If you only want the reusable harness, focus on:

- `run_scenario.py`
- `evaluate_result.py`

If you only want the GitHub demo/reproduction path, focus on:

- `bootstrap_github_testbed.py`
- `reset_github_issue.py`
- `run_official_github_probe.py`
