from __future__ import annotations

import json
import os
import subprocess
from typing import Any

from .paths import PACKAGE_ROOT


def ensure_github_pat() -> str:
    existing = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if existing:
        return existing

    query = "protocol=https\nhost=github.com\nusername=Semih702\n\n"
    completed = subprocess.run(
        ["git", "credential", "fill"],
        input=query,
        text=True,
        capture_output=True,
        check=False,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Could not resolve GitHub credential with git credential fill. "
            f"stderr={completed.stderr.strip()}"
        )

    for line in completed.stdout.splitlines():
        if line.startswith("password="):
            token = line.split("=", 1)[1]
            if token:
                os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = token
                return token

    raise RuntimeError("GitHub credential lookup did not return a password/token.")


def call_github_tool(
    *,
    tool_name: str,
    arguments: dict[str, Any],
    read_only: bool = True,
    toolsets: str = "repos,issues,pull_requests",
    server_bin: str | None = None,
) -> dict[str, Any]:
    ensure_github_pat()

    bridge_script = (PACKAGE_ROOT / "scripts" / "mcp_github_bridge.mjs").resolve()
    options = {
        "readOnly": read_only,
        "toolsets": toolsets,
    }
    if server_bin:
        options["serverBin"] = server_bin

    command = [
        "node",
        str(bridge_script),
        tool_name,
        json.dumps(arguments),
        json.dumps(options),
    ]
    completed = subprocess.run(
        command,
        cwd=str(PACKAGE_ROOT.parent),
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
        env=os.environ.copy(),
    )

    if not completed.stdout.strip():
        raise RuntimeError(
            "GitHub MCP bridge did not return JSON output."
            f" stderr={completed.stderr.strip()}"
        )

    payload = json.loads(completed.stdout)
    payload["bridge_exit_code"] = completed.returncode
    payload["bridge_stderr"] = completed.stderr
    return payload
