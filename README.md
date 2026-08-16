# Structure-Verified RLVR for Label-Efficient Pathology Instance Segmentation

Working title: **S-Seg-RLVR**

Collaboration between a Health Data Science capstone (Junyi Zhou) and mentor **Alexander Chowdhury**, aimed at a research paper (target **MICCAI 2027**; fallback ISBI / MIDL 2027).

> Pixel-overlap losses (Dice/IoU) miss clinically catastrophic merge errors in pathology instance segmentation. This project treats **non-differentiable structural criteria** — instance count, separation, and topology — as **verifiable rewards** for GRPO, enabling learning from point/count supervision plus a small fully labeled anchor set.

## Where to start

| Doc | Purpose |
|-----|---------|
| [Proposal digest](docs/proposal/PROPOSAL_DIGEST.md) | Hypothesis, method, rewards, ablations (15-minute read) |
| [Full proposal PDF](docs/proposal/structural_rlvr_pathology_segmentation_proposal.pdf) | Source document |
| [16-week roadmap](docs/roadmap/LEARNING_ROADMAP.md) | Learning + deliverables |
| [Contribution tracks](docs/roadmap/CONTRIBUTION_TRACKS.md) | Student vs mentor ownership |
| [Related-work matrix](docs/roadmap/related_work_matrix.md) | Gap table (fill in Weeks 3–4) |
| [Literature library](literature/README.md) | Papers, PDFs, notes |
| [AI collaboration guide](docs/guides/AI_COLLABORATION.md) | How to use AI without losing understanding |

## Repo layout

```text
docs/           Proposal, roadmap, guides
literature/     papers.yaml, papers.bib, pdfs/, notes/
src/sseg_rlvr/  Future package (reward stubs now)
experiments/    Experiment cards (no heavy checkpoints)
notebooks/      Exploratory notebooks
scripts/        Issue seeding helper
```

## Literature PDFs

arXiv PDFs for proposal references are committed under `literature/pdfs/` (30 papers). Paywalled-only works are linked by DOI in `literature/papers.yaml`.

```bash
pip install pyyaml
python3 literature/scripts/download_arxiv.py --dry-run
python3 literature/scripts/export_bib.py
```

## Create the GitHub task board

Issues are defined in [`docs/roadmap/issues_manifest.yaml`](docs/roadmap/issues_manifest.yaml). From a machine where `gh` can write issues:

```bash
gh auth login
python3 scripts/create_github_issues.py --dry-run
python3 scripts/create_github_issues.py              # creates issues; label names go in the body
python3 scripts/create_github_issues.py --apply-labels  # optional, needs permission to create labels
```

If an accidental `test` issue exists from bootstrap, close it in the GitHub UI (the bootstrap token may lack close permission).

## Compute

| Resource | Status |
|----------|--------|
| Harvard Research Computing (RC) | GPUs available **now** |
| Dana-Farber Institute | GPUs available **later** |

Early milestones (reading, related-work matrix, reward unit tests on synthetic masks) do **not** need GPUs.

## Data

No pathology datasets are in this repository yet. When access is arranged, keep raw data outside git (see `.gitignore`) and document download steps in a dataset card.

## Hugging Face RL course (short version)

Do Units **1, 4, 8** (fundamentals, policy gradients, PPO), then read GRPO. Skip Q-learning / DQN / Unity / multi-agent deep dives. Details in the [learning roadmap](docs/roadmap/LEARNING_ROADMAP.md).

## Status

Bootstrap phase: proposal ingested, literature library + PDFs, roadmap, issue manifest, reward **stubs**. Training code and datasets come later.
