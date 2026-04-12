from __future__ import annotations

import argparse
import json

from .evaluator import evaluate_scenario_definition
from .runner import run_scenario


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MCP Attack Lab CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Load a scenario and print the resolved run plan")
    run_parser.add_argument("--scenario", required=True, help="Scenario file path or file name")

    eval_parser = subparsers.add_parser(
        "evaluate",
        help="Load a scenario and print the evaluation definition summary",
    )
    eval_parser.add_argument("--scenario", required=True, help="Scenario file path or file name")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        result = run_scenario(args.scenario)
    elif args.command == "evaluate":
        result = evaluate_scenario_definition(args.scenario)
    else:
        parser.error(f"Unsupported command: {args.command}")
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

