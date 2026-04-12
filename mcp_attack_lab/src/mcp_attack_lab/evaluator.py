from __future__ import annotations

from .scenario_loader import load_scenario


def evaluate_scenario_definition(scenario_ref: str) -> dict[str, object]:
    scenario_path, scenario = load_scenario(scenario_ref)
    return {
        "scenario_path": str(scenario_path),
        "scenario_id": scenario["id"],
        "status": "definition-valid",
        "pass_if": scenario["expected"].get("pass_if", []),
        "fail_if": scenario["expected"].get("fail_if", []),
        "observability": scenario.get("observability", {}),
    }

