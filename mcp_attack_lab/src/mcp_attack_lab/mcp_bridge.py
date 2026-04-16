from __future__ import annotations

from pathlib import Path
from typing import Any

import json
import subprocess

from .paths import PACKAGE_ROOT


def call_filesystem_tool(
    *,
    allowed_root: Path,
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    bridge_script = (PACKAGE_ROOT / "scripts" / "mcp_filesystem_bridge.mjs").resolve()

    command = [
        "node",
        str(bridge_script),
        str(allowed_root),
        tool_name,
        json.dumps(arguments),
    ]
    completed = subprocess.run(
        command,
        cwd=str(PACKAGE_ROOT.parent),
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
    )

    if not completed.stdout.strip():
        raise RuntimeError(
            "MCP bridge did not return JSON output."
            f" stderr={completed.stderr.strip()}"
        )

    payload = json.loads(completed.stdout)
    payload["bridge_exit_code"] = completed.returncode
    payload["bridge_stderr"] = completed.stderr
    return payload
