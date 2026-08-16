"""R_sep — instance separation / anti-merge reward.

Proposal definition
-------------------
Reward a 1:1 match between decomposed predicted instances and point markers.
Penalize a single predicted connected component that covers ≥2 markers
(the merged-nuclei failure mode). Non-differentiable.
"""

from __future__ import annotations

from typing import Any, Sequence


def separation_reward(
    pred_mask: Any,
    points: Sequence[tuple[float, float]],
    *,
    threshold: float = 0.5,
) -> float:
    """Return separation reward for predicted instances vs point markers.

    Parameters
    ----------
    pred_mask:
        Predicted probability map or binary mask (H, W).
    points:
        Sequence of (row, col) or (y, x) point annotations.
    threshold:
        Binarization threshold before CC labeling.

    Returns
    -------
    float
        Higher when each component owns at most one point and points are covered;
        lower when merges (one CC, many points) occur.

    Notes
    -----
    Exact scoring formula (soft vs hard penalties, uncovered points) to be fixed
    with Alexander before GRPO runs. Unit tests should cover the merge case first.
    """
    raise NotImplementedError(
        "R_sep not implemented yet — see docs/proposal/PROPOSAL_DIGEST.md and roadmap Weeks 9–11"
    )
