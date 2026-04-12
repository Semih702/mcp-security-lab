from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .paths import PACKAGE_ROOT, SCENARIOS_DIR


REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "id",
    "name",
    "attack",
    "profiles",
    "execution",
    "expected",
}


def resolve_scenario_path(value: str | Path) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    scenario_path = (SCENARIOS_DIR / candidate).resolve()
    if scenario_path.exists():
        return scenario_path
    return (PACKAGE_ROOT / candidate).resolve()


def load_yaml_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping at the top level: {path}")
    return data


def validate_scenario(data: dict[str, Any], path: Path) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL_KEYS - data.keys())
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Scenario is missing required keys ({joined}): {path}")

    profiles = data.get("profiles", {})
    if not isinstance(profiles, dict) or "mcp_profile" not in profiles or "model_profile" not in profiles:
        raise ValueError(f"Scenario must define profiles.mcp_profile and profiles.model_profile: {path}")

    execution = data.get("execution", {})
    if not isinstance(execution, dict) or "runner" not in execution or "evaluator" not in execution:
        raise ValueError(f"Scenario must define execution.runner and execution.evaluator: {path}")

    expected = data.get("expected", {})
    if not isinstance(expected, dict) or "pass_if" not in expected or "fail_if" not in expected:
        raise ValueError(f"Scenario must define expected.pass_if and expected.fail_if: {path}")


def load_scenario(value: str | Path) -> tuple[Path, dict[str, Any]]:
    path = resolve_scenario_path(value)
    if not path.exists():
        raise FileNotFoundError(f"Scenario file does not exist: {path}")
    data = load_yaml_file(path)
    validate_scenario(data, path)
    return path, data


def load_profile(directory: Path, profile_id: str) -> tuple[Path, dict[str, Any]]:
    profile_path = directory / f"{profile_id}.yml"
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {profile_path}")
    return profile_path, load_yaml_file(profile_path)

