# Dataset acquisition log — S-Seg-RLVR pathology datasets

Status as of 2026-09-27. Raw data is never committed (`/data/` is gitignored);
this file records **where each file actually came from** so the acquisition
is reproducible and citable in the eventual paper's data section.

## Why this file exists

The official Warwick TIA Centre pages for 4 of the 6 datasets
(CoNSeP, Lizard, GlaS, CRAG) currently redirect through Warwick's
`websignon.warwick.ac.uk` SSO (Entra ID) regardless of URL, including old
`www2.warwick.ac.uk` links cited in older papers/repos. This is a known,
multi-year, community-wide outage (see e.g.
[hover_net#267](https://github.com/vqdang/hover_net/issues/267),
open since 2023, unresolved as of late 2025) — not specific to any
institution. `scripts/download_pathology_datasets.py` correctly refuses to
fake these downloads and exits non-zero with manual steps.

Where a legitimate community mirror exists, we used it. **These mirrors are
not the datasets' original hosts** — cite the original papers regardless of
which mirror the bytes came from.

## Status table

| Dataset | Official source | Status | Actual source used | Verified |
|---|---|---|---|---|
| PanNuke | `warwick.ac.uk/.../pannuke` | ✅ Open | Official URL (3 fold zips) | Downloaded via script |
| MoNuSeg | Grand Challenge Data page | ✅ Open | Official Google Drive links | Downloaded via script |
| GlaS | `warwick.ac.uk/.../glascontest` | 🔴 SSO wall | [Academic Torrents](https://academictorrents.com/details/208814dd113c2b0a242e74e832ccac28fcff74e5) — `warwick_qu_dataset_released_2016_07_08.zip` | ✅ 172 MB, unzipped, `.bmp` images + `Grade.csv` match documented 165-image structure |
| CoNSeP | `warwick.ac.uk/TIA/data/hovernet/` | 🔴 SSO wall | [HyperAI mirror](https://hyper.ai/en/datasets/18936) (torrent id 21960, via `orion.hyper.ai/tracker/download?torrent=21960`) | ✅ 146 MB, unzipped, `Test/Images/*.png` match documented 41-tile HoVer-Net structure |
| Lizard | `warwick.ac.uk/.../lizard` | 🔴 SSO wall | **Partial substitute only**: [`MedOtter/CoNIC2022`](https://huggingface.co/datasets/MedOtter/CoNIC2022) (Hugging Face, public, ungated) | ✅ 705 MB downloaded, but this is the **CoNIC 2022 challenge re-tiled subset** (4,981 of the full ~495K-nuclei Lizard set), not the full Lizard annotation set. Fine for early prototyping only. |
| CRAG | `warwick.ac.uk/.../mildnet` | 🔴 SSO wall | **None found.** A GitHub repo (`XiaoyuZHK/CRAG-Dataset_Aug_ToCOCO`) references the dataset but appears to hold only augmentation/COCO-conversion scripts, not raw data — unverified, do not rely on it. | ❌ Blocked |

## Still needed: CRAG (and full Lizard)

No working mirror found for CRAG. No mirror found for the *full* Lizard
annotation set (only the CoNIC re-tiled subset). Next step: email
`tia@warwick.ac.uk` directly (per the script's own printed instructions),
ideally with mentor (Alexander Chowdhury) in the loop — this is a
cross-institution data-hosting problem, not something fixable by requesting
"Harvard access."

## License reminders

- PanNuke, MoNuSeg: **CC BY-NC-SA 4.0** — research/non-commercial only, share-alike.
- GlaS: dataset license not explicitly stated by Warwick; the challenge paper is for research use.
- CoNSeP: some third-party mirrors state Apache 2.0; verify against the original HoVer-Net paper before relying on this for the write-up.
- CoNIC2022 (Lizard subset): CC BY-NC-SA 4.0.

## Suitability for RLVR training — explicitly not evaluated yet

Everything above only confirms: **the files are real, non-corrupt, and match
the documented dataset structure.** It does *not* confirm these are the
right datasets, right format, or right preprocessing for the
structure-verified reward pipeline (point/count supervision, degraded
instance masks, topology rewards) described in the proposal. That
evaluation comes after the data-loading/preprocessing code exists.
