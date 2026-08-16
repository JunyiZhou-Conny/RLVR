# S-Seg-RLVR — Proposal Digest

Plain-language digest of the working proposal from mentor **Alexander Chowdhury**.  
Source PDF: [`structural_rlvr_pathology_segmentation_proposal.pdf`](./structural_rlvr_pathology_segmentation_proposal.pdf)

| Field | Value |
|-------|-------|
| Working title | **S-Seg-RLVR** — Non-Differentiable Structural Verifiers as Rewards for Weakly-Supervised Nuclei and Gland Segmentation |
| Full title | Structure-Verified RLVR for Label-Efficient Pathology Instance Segmentation |
| Target venue | MICCAI 2027 (fallback: ISBI 2027 / MIDL 2027) |
| Student | Junyi Zhou (Conny), Health Data Science |
| Mentor | Alexander Chowdhury |

---

## Hypothesis

Pixel-overlap objectives (Dice / IoU) are the **wrong training signal** for pathology instance segmentation. The structural quantities pathologists care about — **instance count**, **instance separation**, and **object topology** — are the right inductive bias, but they have been unusable as losses because they are discrete and non-differentiable.

**Reinforcement learning with verifiable rewards (RLVR)** removes that constraint: GRPO scores a scalar reward per rollout and never differentiates it, so we can supervise with the **exact structural criterion**, derived from weak (point / count) annotation rather than dense masks.

---

## Motivation and gap

Two nearly-touching nuclei merged into one instance barely dents Dice but destroys the count — and downstream, the grade. Under-segmentation of clustered nuclei is the canonical clinically relevant failure.

The topology-aware literature spent a decade building **differentiable surrogates** (persistent-homology losses, soft-skeleton clDice, barcode matching) because Betti numbers and instance counts cannot be backpropagated. RLVR sidesteps that machinery: the discrete structural quantity **is** the reward.

### Positioning

| Line of work | What it does | Gap vs this project |
|--------------|--------------|---------------------|
| Seg-Zero, Seg-R1, LENS | Reasoning-RL for natural-image segmentation | Not pathology dense instance masks; not structural verifiers |
| MedGround-R1, MedSAM-Agent, Med-R1 | Medical GRPO for grounding / VQA / interactive clicking | Overlap / click rewards, not structural instance criteria |
| RLogist, PEAN, Qaiser & Rajpoot | RL in pathology for classification / navigation | Not dense instance segmentation |
| Prior nuclei RL | Threshold post-processing or superpixel merge/split | Narrow; not structural RLVR from weak labels |
| Distance maps, StarDist, shape penalties | Structural priors as **differentiable** losses | Never as non-differentiable RL verifiers |

**Claim:** biological / topological structure is the verifier for static pathology segmentation.

---

## Method

### Policy

Use a **SAM / SAM2** image-branch mask decoder as policy \(\pi_\theta\). Optimize with **GRPO** (group-relative advantages); **no critic**.

### Composite reward

\[
R = R_{\mathrm{seg}} + \lambda_{\mathrm{cnt}} R_{\mathrm{cnt}} + \lambda_{\mathrm{sep}} R_{\mathrm{sep}} + \lambda_{\mathrm{topo}} R_{\mathrm{topo}} + \lambda_{\mathrm{match}} R_{\mathrm{match}} + R_{\mathrm{fmt}}
\]

| Term | Meaning | Differentiable? |
|------|---------|-----------------|
| \(R_{\mathrm{seg}}\) | Grounding: overlap on sparsely labeled pixels, or Dice on a small fully annotated **anchor** set | Can be; keeps masks attached to evidence |
| \(R_{\mathrm{cnt}}\) | Instance-count agreement: \(-\lvert \#\mathrm{CC}(\mathrm{pred}) - c\rvert\) where \(c\) is the point-annotation count | **No** (threshold + connected components) |
| \(R_{\mathrm{sep}}\) | Separation: 1:1 match between instances and point markers; penalize one component covering ≥2 markers (merged-nuclei failure) | **No** |
| \(R_{\mathrm{topo}}\) | Topology vs prior: \(\beta_0=\#\)instances, \(\beta_1=\#\)lumina (glands); Betti / Euler match on binarized mask | **No** |
| \(R_{\mathrm{match}}\) | Panoptic-style Hungarian matching → Panoptic Quality on the anchor set | **No** (assignment) |
| \(R_{\mathrm{fmt}}\) | Validity: well-formed, non-degenerate masks | Mostly discrete checks |

### Label efficiency

\(R_{\mathrm{cnt}}\), \(R_{\mathrm{sep}}\), \(R_{\mathrm{topo}}\) come from **point annotations + a fixed biological prior**, not dense masks. Only a small anchor set carries full masks (for \(R_{\mathrm{seg}}\) / \(R_{\mathrm{match}}\)). Discrete verifiers convert cheap supervision into a usable signal that a pixel loss cannot.

---

## Datasets

| Task | Datasets | Notes |
|------|----------|-------|
| Nuclei (instance + class) | PanNuke, CoNSeP, MoNuSeg, Lizard | Degrade instance masks → centroids to simulate point annotation; counts are free |
| Gland (topology) | GlaS, CRAG | For \(R_{\mathrm{topo}}\) with \(\beta_1 = \#\)lumina |

**Status (student):** no datasets downloaded yet. Acquisition is a roadmap milestone. Do **not** commit raw dataset binaries to this repo.

---

## Baselines

1. Supervised Dice / CE on the same weak labels (lower bound).
2. Supervised on full masks (upper bound, reference only).
3. HoVer-Net / StarDist / CellPose at matched supervision (domain SOTA).
4. Differentiable soft-surrogate of the **same** structural objectives (soft-clDice + PH Betti term + soft density-count), trained as a loss on the same weak labels.

---

## Ablation plan (one variable per rung)

| Rung | Change | Question |
|------|--------|----------|
| 0 | Anchor-only supervised fine-tune | Grounding sanity check |
| 1 | + \(R_{\mathrm{cnt}}\) | Does count alone recover merged instances? |
| 2 | + \(R_{\mathrm{sep}}\) | Isolate clustered-nuclei failure |
| 3 | + \(R_{\mathrm{topo}}\) (glands) | Isolate lumen topology |
| 4 | + \(R_{\mathrm{match}}\) | Full reward |

**Go / no-go:** Rung 4 vs Baseline 4 at matched supervision.

- If discrete-reward policy **wins** → surrogate gap is real; RL closes it.
- If it only **matches** → honest finding: surrogates already capture the signal; contribution is label-efficiency, not non-differentiability.

---

## Compute notes

| Resource | When |
|----------|------|
| Harvard Research Computing (RC) GPUs | Available now |
| Dana-Farber Institute GPUs | Available later |

Early work (literature, verifiers, synthetic tests) does not require GPUs. SAM + GRPO training will.

---

## Reading roadmap (mentor stages)

See [`../../literature/README.md`](../../literature/README.md) and [`../roadmap/LEARNING_ROADMAP.md`](../roadmap/LEARNING_ROADMAP.md).

0. RL & policy optimization (PPO → GRPO → R1 → DAPO)  
1. Segmentation-as-RLVR prior art  
2. Segmentation backbones & SAM  
3. Nuclei / gland instance segmentation  
4. Weak / point supervision  
5. Topological & structural objectives  
6. RL in pathology / WSI (optional / fast)
