# 16-week learning & research roadmap

Audience: Junyi Zhou (Conny), Health Data Science, mentored by **Alexander Chowdhury**.  
Venue target: MICCAI 2027 (fallback ISBI / MIDL 2027).

This roadmap pairs **learning** with **shippable artifacts**. Prefer finishing a small deliverable over finishing every paper.

---

## Compute & data reality

| Resource | Status |
|----------|--------|
| Harvard Research Computing (RC) GPUs | Available **now** — use for smoke tests when ready |
| Dana-Farber Institute GPUs | Available **later** |
| Pathology datasets | **None yet** — request/download with mentor before Weeks 12–13; never commit raw data |

Until data arrives: synthetic masks for reward unit tests + literature + related-work matrix.

---

## Hugging Face Deep RL course (triage)

Full course: https://huggingface.co/learn/deep-rl-course

| Unit | Action |
|------|--------|
| 1 Fundamentals | **Do** |
| 2 Q-Learning | Skim only |
| 3 Deep Q-Learning | **Skip** |
| 4 Policy gradients / REINFORCE | **Do fully** |
| 5 Unity ML-Agents | **Skip** |
| 6 Actor-Critic | Skim (GRPO has no critic) |
| 7 Multi-agent | **Skip** |
| 8 PPO | **Do fully**, then read GRPO [2] |

Time-box: ~1–1.5 weeks parallel with Stage 0–1 papers — not a month-long detour. Lunar Lander Q-learning is not the skill bottleneck for this paper.

---

## Weeks 1–2 — Orientation + RL vocabulary

**Read:** proposal digest thrice; PPO [1]; start GRPO [2]; HF Unit 1 + start Unit 4.

**Do:**
- Write a 1-page restatement of the project in your own words (mentor feedback).
- Start notes for [1], [2].

**Deliverable:** 1-page restatement + ≥3 paper notes started + related-work table skeleton.

**Issue labels:** `learning`, `literature`

---

## Weeks 3–4 — GRPO + Seg-RLVR prior art

**Read:** finish HF Unit 8; DeepSeek-R1 [3] conceptually; Seg-Zero [5], Seg-R1 [6]; skim LENS [7], MedGround-R1 [9].

**Do:** fill related-work matrix columns: task, reward type, dense mask?, medical?, structural verifier?

**Deliverable:** related-work matrix v1 (mentor-reviewable).

---

## Weeks 5–6 — Pathology instance segmentation literacy

**Read:** HoVer-Net [16] deeply (HV maps ↔ merge failures); skim StarDist [17], Cellpose [18], PQ [21]; SAM [14] / SAM2 [15] enough to know what the policy is.

**Deliverable:** one-page “clustered nuclei failure” note + figure sketch (high Dice, wrong count).

---

## Weeks 7–8 — Weak labels + topology surrogates

**Read:** SC-Net [22]; resolve Qu et al. [23] with mentor; Hu [24], Clough [25], clDice [26]; skim Stucki [27].

**Deliverable:** half-page: why Betti/count need surrogates under SGD, and why GRPO does not.

---

## Weeks 9–11 — Verifier library (core student contribution)

**Build** in `src/sseg_rlvr/rewards/` with unit tests on synthetic blobs:

1. `R_cnt`, `R_sep`, `R_fmt`
2. `R_match` (Hungarian → PQ-like)
3. `R_topo` (β0 / β1) on gland-like rings

**Deliverable:** tested reward package + equations/examples in package README.

**No GPU required.**

---

## Weeks 12–13 — Data acquisition + baselines

**With mentor:** pick first public nuclei dataset (likely MoNuSeg or PanNuke); document download for Harvard RC / later Dana-Farber.

**Do:** dataset card (license, splits, point simulation). Run one baseline path for failure-mode analysis once data exists.

**Deliverable:** dataset card + access runbook + baseline metric draft (or explicit blocked-on-data note).

---

## Weeks 14–16 — GRPO MVP + paper outline

**With mentor:** wire SAM policy + GRPO using open recipes **after** rewards are trustworthy.

**Do:** Rung 0–1 experiments; draft paper outline (gap figure, method diagram, related work from your matrix).

**Deliverable:** MVP training log + paper outline + open questions list.

Optional anytime: Stage 6 pathology-RL papers for positioning paragraphs only.

---

## Success checkpoints

| Checkpoint | Evidence |
|------------|----------|
| End of week 4 | Related-work matrix reviewed by Alexander |
| End of week 8 | You can explain the surrogate gap without notes |
| End of week 11 | `R_cnt` / `R_sep` unit tests green |
| End of week 16 | Rung 0–1 run + outline exists |

Task board: see [`issues_manifest.yaml`](./issues_manifest.yaml) and `scripts/create_github_issues.py`.
