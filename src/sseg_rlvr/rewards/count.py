"""R_cnt — instance-count agreement.

Proposal definition
-------------------
R_cnt = -|#connected_components(pred) - c|

where c is the point-annotation count (number of nuclei markers).
Requires binarization / labeling; not differentiable.
"""

from __future__ import annotations

from typing import Any


def count_reward(
    pred_mask: Any,
    point_count: int,
    *,
    threshold: float = 0.5,
) -> float:
    """Return count agreement reward.

    Parameters
    ----------
    pred_mask:
        Predicted probability map or binary mask (H, W).
    point_count:
        Number of point annotations / expected instances c.
    threshold:
        Binarization threshold before connected-component labeling.

    Returns
    -------
    float
        Negative absolute error between #CC and point_count.

    Notes
    -----
    Implementation planned Weeks 9–11 using skimage.measure.label (or equivalent).
    """
    raise NotImplementedError(
        "R_cnt not implemented yet — see docs/proposal/PROPOSAL_DIGEST.md and roadmap Weeks 9–11"
    )
