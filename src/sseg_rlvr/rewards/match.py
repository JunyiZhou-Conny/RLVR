"""R_match — panoptic-style instance matching reward on the anchor set.

Proposal definition
-------------------
Hungarian matching between predicted and ground-truth instances, then
Panoptic Quality (PQ) as a scalar reward. Non-differentiable (assignment problem).
Only available on the small fully annotated anchor set.
"""

from __future__ import annotations

from typing import Any


def match_reward(
    pred_instances: Any,
    gt_instances: Any,
    *,
    iou_threshold: float = 0.5,
) -> float:
    """Return PQ-like matching reward on fully labeled anchors.

    Parameters
    ----------
    pred_instances:
        Predicted instance label map or list of masks.
    gt_instances:
        Ground-truth instance label map or list of masks.
    iou_threshold:
        Match threshold used in PQ-style matching.

    Returns
    -------
    float
        Panoptic Quality or a monotone transform suitable as a reward.
    """
    raise NotImplementedError(
        "R_match not implemented yet — see docs/proposal/PROPOSAL_DIGEST.md and Kirillov PQ [21]"
    )
