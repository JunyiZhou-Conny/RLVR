#!/usr/bin/env python3
"""Download arXiv PDFs listed in literature/papers.yaml into literature/pdfs/."""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_YAML = ROOT / "literature" / "papers.yaml"
DEFAULT_OUT = ROOT / "literature" / "pdfs"
ARXIV_PDF = "https://arxiv.org/pdf/{arxiv}.pdf"
USER_AGENT = "S-Seg-RLVR-literature-bot/0.1 (research; educational; contact via GitHub repo)"


def load_papers(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text())
    return data.get("papers", [])


def pdf_path(out_dir: Path, paper: dict) -> Path:
    arxiv = paper["arxiv"].replace("/", "_")
    return out_dir / f"{paper['id']:02d}_{paper['key']}_{arxiv}.pdf"


def download(arxiv_id: str, dest: Path, timeout: float = 60.0) -> None:
    url = ARXIV_PDF.format(arxiv=arxiv_id)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    if len(data) < 1000 or not data.startswith(b"%PDF"):
        raise RuntimeError(f"Unexpected response for {arxiv_id} ({len(data)} bytes)")
    dest.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yaml", type=Path, default=DEFAULT_YAML)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Re-download even if file exists")
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds between downloads")
    args = parser.parse_args()

    papers = load_papers(args.yaml)
    args.out.mkdir(parents=True, exist_ok=True)

    todo = [p for p in papers if p.get("arxiv")]
    skip = [p for p in papers if not p.get("arxiv")]

    print(f"Papers with arXiv IDs: {len(todo)}")
    print(f"Papers without arXiv (doi_only/unresolved): {len(skip)}")
    for p in skip:
        print(f"  SKIP [{p['id']:02d}] {p['key']} status={p.get('status')}")

    ok, fail, existed = 0, 0, 0
    for p in todo:
        dest = pdf_path(args.out, p)
        label = f"[{p['id']:02d}] {p['arxiv']} -> {dest.name}"
        if dest.exists() and not args.force:
            print(f"  EXISTS {label}")
            existed += 1
            continue
        if args.dry_run:
            print(f"  WOULD DOWNLOAD {label}")
            ok += 1
            continue
        try:
            print(f"  DOWNLOADING {label} ...", flush=True)
            download(p["arxiv"], dest)
            print(f"  OK {label} ({dest.stat().st_size} bytes)")
            ok += 1
            time.sleep(args.sleep)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError, OSError) as e:
            print(f"  FAIL {label}: {e}")
            fail += 1
            # Keep going; mark remaining

    print(f"\nSummary: downloaded/planned={ok} existed={existed} failed={fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
