from __future__ import annotations

import argparse
import json

from mcp_attack_lab.github_testbed_reset import reset_issue_from_seed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reset an existing controlled GitHub issue from a seed file")
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--seed-file", required=True)
    parser.add_argument(
        "--keep-comments",
        action="store_true",
        help="Do not delete existing comments before updating the issue body",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = reset_issue_from_seed(
        owner=args.owner,
        repo=args.repo,
        issue_number=args.issue_number,
        seed_file=args.seed_file,
        delete_existing_comments=not args.keep_comments,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
