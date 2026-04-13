from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import ensure_results_dir


def write_result_artifact(scenario_id: str, payload: dict[str, Any]) -> Path:
    results_dir = ensure_results_dir()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = results_dir / f"{scenario_id.lower()}-{timestamp}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path

