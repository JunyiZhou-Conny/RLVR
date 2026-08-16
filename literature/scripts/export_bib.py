#!/usr/bin/env python3
"""Export literature/papers.yaml to literature/papers.bib."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]


def bib_entry(paper: dict) -> str:
    key = paper["key"]
    title = paper["title"].replace("{", "").replace("}", "")
    authors = paper.get("authors", "Unknown")
    year = paper.get("year", "")
    fields = [
        f"  title = {{{title}}}",
        f"  author = {{{authors}}}",
        f"  year = {{{year}}}",
    ]
    if paper.get("arxiv"):
        fields.append(f"  eprint = {{{paper['arxiv']}}}")
        fields.append("  archivePrefix = {arXiv}")
        fields.append(f"  url = {{https://arxiv.org/abs/{paper['arxiv']}}}")
        entry_type = "article"
    elif paper.get("doi"):
        fields.append(f"  doi = {{{paper['doi']}}}")
        if paper.get("url"):
            fields.append(f"  url = {{{paper['url']}}}")
        entry_type = "article"
    else:
        fields.append("  note = {Citation incomplete — resolve with mentor}")
        entry_type = "misc"
    if paper.get("note") and not paper.get("arxiv"):
        fields.append(f"  note = {{{paper['note']}}}")
    body = ",\n".join(fields)
    return f"@{entry_type}{{{key},\n{body}\n}}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yaml", type=Path, default=ROOT / "literature" / "papers.yaml")
    parser.add_argument("--out", type=Path, default=ROOT / "literature" / "papers.bib")
    args = parser.parse_args()
    papers = yaml.safe_load(args.yaml.read_text())["papers"]
    text = "% Auto-generated from papers.yaml — re-run literature/scripts/export_bib.py\n\n"
    text += "\n\n".join(bib_entry(p) for p in papers) + "\n"
    args.out.write_text(text)
    print(f"Wrote {len(papers)} entries to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
