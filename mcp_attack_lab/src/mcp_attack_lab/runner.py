from __future__ import annotations

from pathlib import Path
from typing import Any

from .paths import MCP_PROFILES_DIR, MODEL_CONFIGS_DIR
from .scenario_loader import load_profile, load_scenario


def build_run_summary(scenario_path: Path, scenario: dict[str, Any]) -> dict[str, Any]:
    mcp_profile_id = scenario["profiles"]["mcp_profile"]
    model_profile_id = scenario["profiles"]["model_profile"]

    mcp_profile_path, mcp_profile = load_profile(MCP_PROFILES_DIR, mcp_profile_id)
    model_profile_path, model_profile = load_profile(MODEL_CONFIGS_DIR, model_profile_id)

    return {
        "scenario_path": str(scenario_path),
        "scenario_id": scenario["id"],
        "scenario_name": scenario["name"],
        "attack_type": scenario["attack"]["type"],
        "mcp_profile_path": str(mcp_profile_path),
        "mcp_profile_id": mcp_profile.get("id", mcp_profile_id),
        "model_profile_path": str(model_profile_path),
        "model_profile_id": model_profile.get("id", model_profile_id),
        "runner": scenario["execution"].get("runner"),
        "evaluator": scenario["execution"].get("evaluator"),
        "timeout_seconds": scenario["execution"].get("timeout_seconds"),
        "pass_if": scenario["expected"].get("pass_if", []),
        "fail_if": scenario["expected"].get("fail_if", []),
    }


def run_scenario(scenario_ref: str) -> dict[str, Any]:
    scenario_path, scenario = load_scenario(scenario_ref)
    return build_run_summary(scenario_path, scenario)

