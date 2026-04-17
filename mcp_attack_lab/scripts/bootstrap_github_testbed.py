from __future__ import annotations

import argparse
import json
from pathlib import Path

from mcp_attack_lab.github_testbed_bootstrap import bootstrap_github_testbed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bootstrap the controlled GitHub MCP toxic-flow testbed")
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to a GitHub testbed manifest JSON file",
    )
    parser.add_argument(
        "--owner",
        help="Optional GitHub owner override",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = bootstrap_github_testbed(
        manifest_path=Path(args.manifest),
        owner_override=args.owner,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
