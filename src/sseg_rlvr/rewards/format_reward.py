"""R_fmt — mask validity / format reward.

Proposal definition
-------------------
Reward well-formed, non-degenerate masks (e.g. non-empty, finite, within bounds,
not pathological speckles). Exact checks to be specified with mentor.
"""

from __future__ import annotations

from typing import Any


def format_reward(pred_mask: Any) -> float:
    """Return validity reward for a predicted mask.

    Returns
    -------
    float
        Typically 0 for valid masks and a negative penalty for degenerate outputs.
    """
    raise NotImplementedError(
        "R_fmt not implemented yet — see docs/proposal/PROPOSAL_DIGEST.md"
    )
