# MCP Attack Lab Scaffold

This directory is a reusable skeleton for controlled MCP security scenario reproduction.

The idea is simple:

- Each attack scenario lives in a single YAML file under `scenarios/`.
- MCP server choices live in `mcp_profiles/`.
- Model choices live in `model_configs/`.
- Prompts, poisoned content, and dummy secrets live in `fixtures/`.
- Python CLI entrypoints and thin wrapper scripts live in `scripts/`.
- Results can be stored under `results/`.

Recommended flow:

1. Pick a scenario YAML.
2. Resolve the `mcp_profile` and `model_profile` it references.
3. Load any prompt and fixture files listed in the scenario.
4. Run the scenario in an isolated environment.
5. Record outcome, logs, and observations in `results/`.

## Python Layout

The lab is now Python-based.

- Main package: `src/mcp_attack_lab/`
- CLI entrypoint: `python -m mcp_attack_lab.cli`
- Wrapper scripts:
  - `scripts/run_scenario.py`
  - `scripts/evaluate_result.py`

Suggested setup:

```bash
cd mcp_attack_lab
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

Example usage:

```bash
python -m mcp_attack_lab.cli run --scenario scenarios/001-indirect-prompt-injection.yml
python -m mcp_attack_lab.cli evaluate --scenario scenarios/001-indirect-prompt-injection.yml
```

Suggested design principles:

- Use only dummy secrets and controlled sinks.
- Treat this as a safety evaluation harness, not a general exploit framework.
- Keep each scenario measurable: expected action, forbidden action, and success criteria should be explicit.
- Prefer outcome-based assertions such as "did the model call a forbidden tool?" over vague judgments.

Directory layout:

- `scenarios/`: attack definitions and templates
- `mcp_profiles/`: reusable MCP server configurations
- `model_configs/`: reusable model settings
- `fixtures/`: prompts, mock data, dummy files, poisoned content
- `scripts/`: Python wrapper scripts
- `src/mcp_attack_lab/`: core Python package
- `results/`: run outputs
