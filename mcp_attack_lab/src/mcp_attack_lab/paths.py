from __future__ import annotations

from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SCENARIOS_DIR = PACKAGE_ROOT / "scenarios"
MCP_PROFILES_DIR = PACKAGE_ROOT / "mcp_profiles"
MODEL_CONFIGS_DIR = PACKAGE_ROOT / "model_configs"
RESULTS_DIR = PACKAGE_ROOT / "results"


def ensure_results_dir() -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR
