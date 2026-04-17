from __future__ import annotations

import argparse
import json

from mcp_attack_lab.official_github_probe import run_official_github_probe


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the official GitHub MCP toxic-flow read probe")
    parser.add_argument("--model-profile", default="openai-gpt-5-nano")
    parser.add_argument("--owner", default="Semih702")
    parser.add_argument("--public-repo", default="gh-toxic-flow-public-lab")
    parser.add_argument("--private-repo", default="gh-toxic-flow-private-lab")
    parser.add_argument("--issue-number", type=int, default=1)
    parser.add_argument("--private-path", default="notes/internal-fix-summary.md")
    parser.add_argument("--post-comment", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_official_github_probe(
        model_profile_ref=args.model_profile,
        owner=args.owner,
        public_repo=args.public_repo,
        private_repo=args.private_repo,
        issue_number=args.issue_number,
        private_path=args.private_path,
        post_comment=args.post_comment,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
