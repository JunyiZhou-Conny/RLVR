#!/usr/bin/env python3
"""Create GitHub Issues from docs/roadmap/issues_manifest.yaml using the gh CLI.

Usage:
  gh auth status
  python3 scripts/create_github_issues.py           # create missing issues
  python3 scripts/create_github_issues.py --dry-run

This cloud agent environment may be read-only for `gh` writes; run this on your
laptop or Harvard RC after cloning, with a token that can open issues.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "roadmap" / "issues_manifest.yaml"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def existing_titles() -> set[str]:
    proc = run(["gh", "issue", "list", "--limit", "200", "--state", "all", "--json", "title"])
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(
            "Could not list issues via gh. Authenticate with `gh auth login` "
            "and ensure you have access to this repo."
        )
    return {item["title"] for item in json.loads(proc.stdout or "[]")}


def ensure_labels(labels: list[str]) -> None:
    known = run(["gh", "label", "list", "--limit", "200", "--json", "name"])
    existing = set()
    if known.returncode == 0:
        existing = {x["name"] for x in json.loads(known.stdout or "[]")}
    colors = {
        "learning": "0E8A16",
        "literature": "1D76DB",
        "rewards": "D93F0B",
        "data": "FBCA04",
        "compute": "5319E7",
        "experiments": "BFDADC",
        "paper": "C5DEF5",
        "docs": "CFE2CE",
    }
    for lab in labels:
        if lab in existing:
            continue
        color = colors.get(lab, "CCCCCC")
        proc = run(["gh", "label", "create", lab, "--color", color, "--force"])
        if proc.returncode != 0:
            # --force may not exist on older gh; try without
            run(["gh", "label", "create", lab, "--color", color])


def create_issue(title: str, body: str, labels: list[str], dry_run: bool) -> None:
    if dry_run:
        print(f"WOULD CREATE: {title} labels={labels}")
        return
    ensure_labels(labels)
    cmd = ["gh", "issue", "create", "--title", title, "--body", body]
    for lab in labels:
        cmd.extend(["--label", lab])
    proc = run(cmd)
    if proc.returncode != 0:
        print(f"FAIL {title}: {proc.stderr}", file=sys.stderr)
    else:
        print(f"CREATED {proc.stdout.strip()} — {title}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force-all", action="store_true", help="Create even if title exists")
    args = parser.parse_args()

    data = yaml.safe_load(args.manifest.read_text())
    issues = data.get("issues", [])
    print(f"Manifest issues: {len(issues)}")

    if args.dry_run:
        existing = set()
    else:
        existing = existing_titles()
        print(f"Existing issues on repo: {len(existing)}")

    created = 0
    skipped = 0
    for issue in issues:
        title = issue["title"]
        if not args.force_all and title in existing:
            print(f"SKIP exists: {title}")
            skipped += 1
            continue
        create_issue(title, issue.get("body", ""), issue.get("labels", []), args.dry_run)
        created += 1

    print(f"Done. created/planned={created} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
