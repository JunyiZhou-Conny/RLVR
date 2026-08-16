# Contribution tracks

Who owns what over the next four months. Adjust with Alexander as the project evolves.

## Student-owned (Junyi) — high paper value without deep RL first

| Track | Artifacts | Weeks |
|-------|-----------|-------|
| Literature & related work | Notes in `literature/notes/`; differentiation matrix | 1–8 |
| Verifier / reward library | `src/sseg_rlvr/rewards/` + tests | 9–11 |
| Metrics | PQ, count error, merge/split rates in `src/sseg_rlvr/metrics/` | 9–12 |
| Data prep (once access exists) | Point simulation, dataset cards — **not** raw binaries in git | 12–13 |
| Experiment hygiene | Experiment cards under `experiments/` | 12–16 |
| Paper assets | Failure-mode figures, method diagram drafts, related-work prose | ongoing |

## Mentor-heavy (Alexander) — coordinate closely

| Track | Why |
|-------|-----|
| SAM / SAM2 policy wiring | Architecture + training recipe choices |
| GRPO training stability | Hyperparameters, group size, KL, reward scaling |
| Go / no-go vs soft surrogates | Scientific claim honesty |
| Venue strategy & authorship | MICCAI / ISBI / MIDL |
| Dataset access / IRB / licenses if any | Institutional |

## Shared

| Track | Notes |
|-------|-------|
| Weekly sync | Bring one artifact (note, matrix row, test output), not only status talk |
| Task board | GitHub Issues from `issues_manifest.yaml` |
| Compute | Harvard RC now; Dana-Farber later — document commands in experiment cards |

## What “done” looks like for the capstone

You can point to: (1) a related-work matrix that proves the gap, (2) a tested structural reward library, (3) at least Rung 0–1 experimental evidence, (4) a paper outline you co-wrote.
