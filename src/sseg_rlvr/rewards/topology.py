"""R_topo — topological correctness vs biological prior.

Proposal definition
-------------------
Score Betti-number / Euler-characteristic match on the binarized mask:

- β0 ≈ number of instances (nuclei / glands as components)
- β1 ≈ number of lumina (glands as rings)

Non-differentiable. Primary target datasets: GlaS, CRAG.
"""

from __future__ import annotations

from typing import Any


def topology_reward(
    pred_mask: Any,
    *,
    target_beta0: int | None = None,
    target_beta1: int | None = None,
    threshold: float = 0.5,
) -> float:
    """Return topology match reward.

    Parameters
    ----------
    pred_mask:
        Predicted probability map or binary mask.
    target_beta0, target_beta1:
        Target Betti numbers from annotation / prior. Either may be None if unused.
    threshold:
        Binarization threshold.

    Returns
    -------
    float
        Agreement score (formula TBD: negative L1 on Betti, or indicator match).
    """
    raise NotImplementedError(
        "R_topo not implemented yet — see docs/proposal/PROPOSAL_DIGEST.md and roadmap Weeks 9–11"
    )
