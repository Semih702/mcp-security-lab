# Scripts

These are thin Python wrapper scripts for the lab CLI.

Suggested responsibilities:

- `run_scenario.py`: loads a scenario YAML, resolves model and MCP profiles, prepares fixtures, then launches a controlled run.
- `evaluate_result.py`: checks logs, tool calls, and outputs against the scenario's success criteria.

For now, the wrappers are intentionally lightweight so the lab structure can evolve before full implementation starts.
