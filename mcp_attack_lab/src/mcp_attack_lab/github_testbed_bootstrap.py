from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .env_loader import load_dotenv_file
from .github_mcp_bridge import ensure_github_pat
from .paths import PACKAGE_ROOT, ensure_results_dir


def _setdefault_env() -> None:
    env_path = PACKAGE_ROOT / ".env.local"
    for key, value in load_dotenv_file(env_path).items():
        os.environ.setdefault(key, value)


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def _github_request(token: str, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url=f"https://api.github.com{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "mcp-attack-lab-bootstrap",
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API request failed: {method} {path} status={exc.code} body={body}") from exc


def ensure_repository(token: str, owner: str, name: str, private: bool) -> dict[str, Any]:
    try:
        return _github_request(token, "GET", f"/repos/{owner}/{name}")
    except RuntimeError as exc:
        if "status=404" not in str(exc):
            raise

    return _github_request(
        token,
        "POST",
        "/user/repos",
        {
            "name": name,
            "private": private,
            "has_issues": True,
            "auto_init": False,
        },
    )


def _copy_seed_tree(seed_dir: Path, destination: Path) -> None:
    if destination.exists():
        if any(destination.iterdir()):
            raise RuntimeError(
                f"Destination already exists and is not empty: {destination}. "
                "Choose a new workspace path or clean it manually."
            )
    destination.mkdir(parents=True, exist_ok=True)
    for item in seed_dir.iterdir():
        target = destination / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def _run_git(args: list[str], cwd: Path) -> None:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Git command failed in {cwd}: git {' '.join(args)}\n"
            f"stdout={completed.stdout}\n"
            f"stderr={completed.stderr}"
        )


def seed_repository(local_repo_dir: Path, seed_dir: Path, remote_url: str) -> str:
    _copy_seed_tree(seed_dir, local_repo_dir)
    _run_git(["init"], local_repo_dir)
    _run_git(["checkout", "-b", "main"], local_repo_dir)
    _run_git(["add", "."], local_repo_dir)
    _run_git(["commit", "-m", "Initial controlled testbed seed"], local_repo_dir)
    _run_git(["remote", "add", "origin", remote_url], local_repo_dir)
    _run_git(["push", "-u", "origin", "main"], local_repo_dir)

    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(local_repo_dir),
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(f"Could not resolve commit SHA for {local_repo_dir}")
    return completed.stdout.strip()


def _parse_issue_seed(seed_path: Path) -> tuple[str, str]:
    text = seed_path.read_text(encoding="utf-8")
    if not text.startswith("Title:"):
        raise ValueError(f"Issue seed does not start with Title: {seed_path}")

    lines = text.splitlines()
    title = lines[0].split("Title:", 1)[1].strip()
    marker = "Body:"
    try:
        body_index = lines.index(marker)
    except ValueError as exc:
        raise ValueError(f"Issue seed is missing Body: marker: {seed_path}") from exc
    body = "\n".join(lines[body_index + 1 :]).lstrip()
    return title, body


def create_issue_from_seed(token: str, owner: str, repo: str, seed_path: Path) -> dict[str, Any]:
    title, body = _parse_issue_seed(seed_path)
    return _github_request(
        token,
        "POST",
        f"/repos/{owner}/{repo}/issues",
        {
            "title": title,
            "body": body,
        },
    )


def write_bootstrap_metadata(payload: dict[str, Any]) -> Path:
    results_dir = ensure_results_dir()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = results_dir / f"github-testbed-bootstrap-{timestamp}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def bootstrap_github_testbed(
    *,
    manifest_path: Path,
    owner_override: str | None = None,
) -> dict[str, Any]:
    _setdefault_env()
    token = ensure_github_pat()
    manifest = load_manifest(manifest_path)
    owner = owner_override or manifest["owner"]
    local_workspace = (manifest_path.parent / manifest["local_workspace"]).resolve()
    local_workspace.mkdir(parents=True, exist_ok=True)

    repo_metadata: dict[str, Any] = {}
    for repo_key, repo_config in manifest["repos"].items():
        repo_name = repo_config["name"]
        repo_info = ensure_repository(
            token=token,
            owner=owner,
            name=repo_name,
            private=bool(repo_config["private"]),
        )
        seed_dir = (PACKAGE_ROOT / repo_config["seed_dir"]).resolve()
        local_repo_dir = (local_workspace / repo_name).resolve()
        commit_sha = seed_repository(
            local_repo_dir=local_repo_dir,
            seed_dir=seed_dir,
            remote_url=repo_info["clone_url"],
        )
        repo_metadata[repo_key] = {
            "name": repo_name,
            "private": bool(repo_config["private"]),
            "html_url": repo_info["html_url"],
            "clone_url": repo_info["clone_url"],
            "local_path": str(local_repo_dir),
            "commit_sha": commit_sha,
        }

    issue_config = manifest["issue"]
    target_repo_key = issue_config["target_repo"]
    target_repo_name = manifest["repos"][target_repo_key]["name"]
    issue_seed_path = (PACKAGE_ROOT / issue_config["seed_file"]).resolve()
    issue_info = create_issue_from_seed(
        token=token,
        owner=owner,
        repo=target_repo_name,
        seed_path=issue_seed_path,
    )

    metadata = {
        "owner": owner,
        "manifest_path": str(manifest_path.resolve()),
        "local_workspace": str(local_workspace),
        "repos": repo_metadata,
        "issue": {
            "target_repo": target_repo_name,
            "number": issue_info["number"],
            "html_url": issue_info["html_url"],
            "seed_file": str(issue_seed_path),
        },
    }
    metadata_path = write_bootstrap_metadata(metadata)
    metadata["metadata_path"] = str(metadata_path)
    return metadata
