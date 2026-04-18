from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .github_mcp_bridge import ensure_github_pat
from .github_testbed_bootstrap import (
    _setdefault_env,
    delete_issue_comment,
    list_issue_comments,
    update_issue_from_seed,
)
from .paths import PACKAGE_ROOT, ensure_results_dir


def write_reset_metadata(payload: dict[str, Any]) -> Path:
    results_dir = ensure_results_dir()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = results_dir / f"github-issue-reset-{timestamp}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def reset_issue_from_seed(
    *,
    owner: str,
    repo: str,
    issue_number: int,
    seed_file: str,
    delete_existing_comments: bool = True,
) -> dict[str, Any]:
    _setdefault_env()
    token = ensure_github_pat()
    seed_path = (PACKAGE_ROOT / seed_file).resolve()

    deleted_comments: list[dict[str, Any]] = []
    if delete_existing_comments:
        comments = list_issue_comments(token, owner, repo, issue_number)
        for comment in comments:
            comment_id = int(comment["id"])
            delete_issue_comment(token, owner, repo, comment_id)
            deleted_comments.append(
                {
                    "id": comment_id,
                    "html_url": comment.get("html_url"),
                    "user": (comment.get("user") or {}).get("login"),
                }
            )

    issue_info = update_issue_from_seed(
        token=token,
        owner=owner,
        repo=repo,
        issue_number=issue_number,
        seed_path=seed_path,
    )

    metadata = {
        "owner": owner,
        "repo": repo,
        "issue_number": issue_number,
        "seed_file": str(seed_path),
        "deleted_comments": deleted_comments,
        "issue": {
            "number": issue_info["number"],
            "html_url": issue_info["html_url"],
            "title": issue_info["title"],
            "state": issue_info["state"],
        },
    }
    metadata_path = write_reset_metadata(metadata)
    metadata["metadata_path"] = str(metadata_path)
    return metadata
