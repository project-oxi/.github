#!/usr/bin/env python3
"""Sync labels.yml to all 5 org repos via the GitHub Labels REST API.

Faster than gh label clone: 1 list call per repo, then parallel PATCH/
POST/DELETE. oxicode keeps its oxi-only labels (provider:*, area: agent/
ai/extensions/security); the other 4 repos do not.

Idempotent — re-run after editing labels.yml.
"""
from __future__ import annotations
import concurrent.futures as cf
import json
import subprocess
import sys
from pathlib import Path

import yaml

ORG = "project-oxi"
REPOS = ["oxicode", "oxibrowser", "oxios", "oxinot", "oxipage", "oxiline"]
OXICODE_ONLY = {
    "area: agent", "area: ai", "area: extensions", "area: security",
    "provider: anthropic", "provider: google", "provider: openai", "provider: other",
}
# Deprecated names replaced by canonical ones (remove from every repo).
DEPRECATED = {
    "bug", "documentation", "enhancement", "duplicate", "wontfix",
    "type: breaking-change",
    # Legacy GitHub defaults that don't map to our taxonomy.
    "dependencies", "github_actions", "rust", "invalid", "question",
}

# Parallel cap — one in-flight per repo, up to 8 workers.
MAX_WORKERS = 8


def gh(*args: str) -> dict | list | str:
    """Run gh and parse JSON when the last arg ends with a flag that
    requests it, else return (rc, stdout, stderr)."""
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:6])}... failed: {r.stderr.strip()}")
    return r.stdout


def list_labels(repo: str) -> dict[str, dict]:
    """Return {name: {color, description}} for the given repo."""
    out = gh("api", f"repos/{ORG}/{repo}/labels?per_page=100",
             "--jq", ".[] | {name: .name, color: .color, description: .description}")
    # gh --jq with non-stream output returns one JSON object per line.
    result: dict[str, dict] = {}
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        result[obj["name"]] = {"color": obj["color"], "description": obj["description"]}
    return result


def create_label(repo: str, name: str, color: str, description: str) -> str:
    """Create label. Returns 'created' or 'exists'."""
    r = subprocess.run(
        ["gh", "api", f"repos/{ORG}/{repo}/labels",
         "-X", "POST",
         "-f", f"name={name}",
         "-f", f"color={color.lstrip('#')}",
         "-f", f"description={description}"],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        return "created"
    if "422" in r.stderr and "already_exists" in r.stderr:
        return "exists"
    raise RuntimeError(f"create {name} on {repo}: {r.stderr.strip()[:300]}")


def update_label(repo: str, name: str, color: str, description: str) -> str:
    """PATCH label. Returns 'updated' or 'unchanged'."""
    r = subprocess.run(
        ["gh", "api", f"repos/{ORG}/{repo}/labels/{name}",
         "-X", "PATCH",
         "-f", f"color={color.lstrip('#')}",
         "-f", f"description={description}"],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        return "updated"
    raise RuntimeError(f"update {name} on {repo}: {r.stderr.strip()[:300]}")


def delete_label(repo: str, name: str) -> str:
    """Delete label. Returns 'deleted' or 'missing'."""
    r = subprocess.run(
        ["gh", "api", f"repos/{ORG}/{repo}/labels/{name}",
         "-X", "DELETE", "--silent"],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        return "deleted"
    if "404" in r.stderr:
        return "missing"
    raise RuntimeError(f"delete {name} on {repo}: {r.stderr.strip()[:300]}")


def sync_repo(repo: str, canonical: dict[str, dict]) -> dict:
    """Sync one repo. Returns change counts."""
    existing = list_labels(repo)
    changes = {"created": 0, "updated": 0, "deleted": 0, "unchanged": 0, "errors": []}

    # Upsert canonical labels.
    for name, spec in canonical.items():
        color = spec["color"].lstrip("#")
        desc = spec["description"]
        if name not in existing:
            try:
                create_label(repo, name, color, desc)
                changes["created"] += 1
                print(f"  {repo}: + {name}")
            except RuntimeError as e:
                changes["errors"].append(str(e))
        elif existing[name]["color"].lower() != color.lower() or existing[name]["description"] != desc:
            try:
                update_label(repo, name, color, desc)
                changes["updated"] += 1
                print(f"  {repo}: ~ {name}")
            except RuntimeError as e:
                changes["errors"].append(str(e))
        else:
            changes["unchanged"] += 1

    # Delete deprecated aliases (all repos).
    for name in DEPRECATED:
        if name in existing:
            try:
                delete_label(repo, name)
                changes["deleted"] += 1
                print(f"  {repo}: - {name} (deprecated)")
            except RuntimeError as e:
                changes["errors"].append(str(e))

    # Delete oxi-only labels from non-template repos.
    if repo != "oxicode":
        for name in OXICODE_ONLY:
            if name in existing:
                try:
                    delete_label(repo, name)
                    changes["deleted"] += 1
                    print(f"  {repo}: - {name} (oxi-only)")
                except RuntimeError as e:
                    changes["errors"].append(str(e))

    return changes


def main() -> int:
    spec_path = Path(__file__).parent.parent / "labels.yml"
    spec_list = yaml.safe_load(spec_path.read_text())
    canonical = {lbl["name"]: lbl for lbl in spec_list}
    print(f"Loaded {len(canonical)} canonical labels from labels.yml\n")

    summary = {}
    with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(sync_repo, repo, canonical): repo for repo in REPOS}
        for fut in cf.as_completed(futures):
            repo = futures[fut]
            try:
                summary[repo] = fut.result()
            except Exception as e:
                summary[repo] = {"errors": [str(e)]}

    # Final state check.
    print("\n=== Final label counts ===")
    final: dict[str, int] = {}
    with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for repo, n in zip(REPOS, pool.map(list_labels, REPOS)):
            final[repo] = len(n)
            print(f"  {repo}: {final[repo]} labels")

    # Per-repo extras (labels on the repo not in canonical and not deleted).
    print("\n=== Residual labels not in labels.yml ===")
    for repo in REPOS:
        existing = list_labels(repo)
        extras = set(existing) - set(canonical)
        if extras:
            print(f"  {repo}: {sorted(extras)}")
        else:
            print(f"  {repo}: (none)")

    has_errors = any(s.get("errors") for s in summary.values())
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
