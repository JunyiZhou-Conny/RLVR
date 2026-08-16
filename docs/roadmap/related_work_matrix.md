# Related-work differentiation matrix (v0 skeleton)

Fill during Weeks 3–4. Goal: prove the gap for S-Seg-RLVR in one page.

| Work | Task | Reward / loss type | Dense instance masks? | Medical / pathology? | Non-diff structural verifier? | Notes / cite |
|------|------|--------------------|-----------------------|----------------------|-------------------------------|--------------|
| **S-Seg-RLVR (this work)** | Pathology nuclei/gland instance seg | GRPO: count, separation, topology, PQ, fmt + weak grounding | Yes | Yes (pathology) | **Yes** | Proposal |
| Seg-Zero | Natural-image reasoning seg | Cognitive / reasoning RL | Seg masks (natural) | No | No (not structural path priors) | [5] |
| Seg-R1 | Segmentation via RL | Simple RL rewards (overlap-style) | Yes (general) | No | No | [6] |
| LENS | Unified reinforced reasoning seg | RL reasoning | Yes | No | No | [7] |
| MedGround-R1 | Medical image grounding | Spatial-semantic GRPO | Grounding, not dense path instances | Medical | No | [9] |
| MedSAM-Agent | Interactive medical seg | Multi-turn agentic RL | Interactive | Medical | No | [10] |
| Med-R1 | Medical VLM reasoning | RL for reasoning | N/A / VQA-style | Medical | No | [11] |
| HoVer-Net | Nuclei instance seg | Supervised HV + classification | Yes | Pathology | No (supervised) | [16] |
| StarDist / Cellpose | Cell/nuclei instance | Supervised shape priors | Yes | Bio/path | No (differentiable training) | [17][18] |
| PH / clDice losses | Topology-aware seg | Differentiable surrogates | Often semantic/tubular | Often medical | **Surrogate**, not RL verifier | [24]–[28] |
| SC-Net / point nuclei | Weak nuclei seg | Self-sup / co-training | Yes | Pathology | No RL | [22][23] |
| RLogist / PEAN / Qaiser | WSI RL | Navigation / attention | No (not instance masks) | Pathology | N/A | [29]–[31] |
| Stateless AC instance + priors | Instance seg RL | Actor-critic + high-level priors | Yes | ? | Nearest prior art — detail carefully | [32] |

## Narrative gap (draft one paragraph)

TBD after reading Stage 1 + Stage 5.

## Mentor review

- Date:
- Feedback:
