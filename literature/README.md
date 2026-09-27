# Literature library

Curated references from the S-Seg-RLVR proposal (Alexander Chowdhury), organized by the mentor reading roadmap.

| Resource | Path |
|----------|------|
| Machine-readable index | [`papers.yaml`](./papers.yaml) |
| BibTeX | [`papers.bib`](./papers.bib) |
| PDFs (arXiv) | [`pdfs/`](./pdfs/) |
| Reading notes | [`notes/`](./notes/) |
| Download script | [`scripts/download_arxiv.py`](./scripts/download_arxiv.py) |
| Bib export | [`scripts/export_bib.py`](./scripts/export_bib.py) |

**Policy:** arXiv PDFs are committed here for offline reading. Paywalled journal PDFs are **not** scraped — use the DOI links in `papers.yaml`. Incomplete citations are marked `status: unresolved` for mentor follow-up.

Refresh PDFs:

```bash
pip install pyyaml
python3 literature/scripts/download_arxiv.py          # skip existing
python3 literature/scripts/download_arxiv.py --force  # re-download
python3 literature/scripts/download_arxiv.py --dry-run
```

---

## Stage 0 — RL & policy optimization

| # | Paper | Priority | PDF |
|---|-------|----------|-----|
| 1 | PPO (Schulman et al.) | must | yes |
| 2 | DeepSeekMath / GRPO (Shao et al.) | must | yes |
| 3 | DeepSeek-R1 (Guo et al.) | must | yes |
| 4 | DAPO (Yu et al.) | should | yes |

## Stage 1 — Segmentation-as-RLVR

| # | Paper | Priority | PDF |
|---|-------|----------|-----|
| 5 | Seg-Zero | must | yes |
| 6 | Seg-R1 | must | yes |
| 7 | LENS | should | yes |
| 8 | SAM-R1 | optional | yes |
| 9 | MedGround-R1 | should | yes |
| 10 | MedSAM-Agent | should | yes |
| 11 | Med-R1 | should | yes |
| 38 | MedReasoner (body-only name) | should | yes |

**Differentiation line:** these mostly do grounding / interactive clicking with overlap rewards; none use non-differentiable **structural** verifiers for dense pathology instance masks.

## Stage 2 — Segmentation backbones & SAM

| # | Paper | Priority | PDF |
|---|-------|----------|-----|
| 12 | U-Net | should | yes |
| 13 | nnU-Net | should | yes (arXiv preprint of Nat Methods) |
| 14 | SAM | must | yes |
| 15 | SAM 2 | must | yes |

## Stage 3 — Nuclei & gland instance segmentation (+ datasets)

| # | Paper | Priority | PDF |
|---|-------|----------|-----|
| 16 | HoVer-Net | must | yes |
| 17 | StarDist | should | yes |
| 18 | Cellpose | should | yes |
| 19 | Distance-map regression (Naylor) | should | DOI only |
| 20 | DCAN (glands) | should | yes |
| 21 | Panoptic Quality | must | yes |
| 33–37 | MoNuSeg, PanNuke, GlaS, CRAG/MILD-Net, Lizard | should | mixed |
| 39 | CoNSeP dataset (body-only name) | should | yes (HoVer-Net [16] PDF) |

## Stage 4 — Weak / point supervision

| # | Paper | Priority | PDF |
|---|-------|----------|-----|
| 22 | SC-Net | must | yes |
| 23 | Qu et al. point nuclei | should | yes |

## Stage 5 — Topological & structural objectives

| # | Paper | Priority | PDF |
|---|-------|----------|-----|
| 24 | Hu et al. topology-preserving | must | yes |
| 25 | Clough et al. PH loss | must | yes |
| 26 | clDice | must | yes |
| 27 | Stucki et al. barcodes | should | yes |
| 28 | Berger et al. multi-class topo | should | yes |

## Stage 6 — RL in pathology / WSI (optional / fast)

| # | Paper | Priority | PDF |
|---|-------|----------|-----|
| 29 | Qaiser & Rajpoot | optional | yes |
| 30 | RLogist | optional | yes |
| 31 | PEAN | optional | yes (Nat Comms OA) |
| 32 | Stateless actor-critic instance seg | should | yes |

---

## Body-only extras (not numbered in the proposal)

| # | Paper / dataset | Priority | PDF |
|---|-----------------|----------|-----|
| 38 | MedReasoner | should | yes |
| 39 | CoNSeP dataset | should | yes (same PDF as HoVer-Net [16]; not duplicated) |

## Remaining paywalled (no legal open preprint found)

1. **Naylor** distance-map TMI 2019 — DOI only. HAL `hal-01984033` is a notice without a file.
2. **MoNuSeg / Kumar** TMI 2017 — DOI only. No arXiv. The 2019 challenge writeup is a different paper (not substituted).

---

## Note-taking

Copy [`../docs/guides/READING_NOTES_TEMPLATE.md`](../docs/guides/READING_NOTES_TEMPLATE.md) into `notes/` for each paper you read. Seeded note shells exist for **must-read** papers.
