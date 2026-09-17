# Scripts

- `create_github_issues.py` — seed GitHub issues from the roadmap manifest.
- `download_pathology_datasets.py` — one-command fetch of the six public S-Seg-RLVR datasets.

```bash
python scripts/download_pathology_datasets.py --dry-run
python scripts/download_pathology_datasets.py --only pannuke,monuseg
python scripts/download_pathology_datasets.py --out data/pathology
```

Writes `<out>/{pannuke,consep,monuseg,lizard,glas,crag}/`. Default `--out` is `data/pathology` (gitignored). Existing files are skipped. Warwick-gated sets (CoNSeP, Lizard, GlaS, CRAG) read `WARWICK_USER` / `WARWICK_PASS` or print exact browser steps and exit non-zero — they never write a fake zip. PanNuke and MoNuSeg are CC BY-NC-SA 4.0. Optional `--max-bytes N` skips files larger than N (use this so a first run cannot pull the ~2 GB PanNuke folds).
