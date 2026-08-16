"""Composite reward R = R_seg + λ_cnt R_cnt + … + R_fmt."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence


@dataclass
class RewardWeights:
    lambda_cnt: float = 1.0
    lambda_sep: float = 1.0
    lambda_topo: float = 0.0
    lambda_match: float = 0.0
    # R_seg and R_fmt are unweighted in the proposal sketch; keep explicit hooks.
    lambda_seg: float = 1.0
    lambda_fmt: float = 1.0


class CompositeReward:
    """Weighted sum of structural verifiers + grounding term.

    R_seg is provided by the caller (Dice/overlap on sparse or anchor labels)
    because it depends on the supervision regime.
    """

    def __init__(self, weights: RewardWeights | None = None) -> None:
        self.weights = weights or RewardWeights()

    def __call__(
        self,
        *,
        r_seg: float,
        pred_mask: Any,
        point_count: int | None = None,
        points: Sequence[tuple[float, float]] | None = None,
        gt_instances: Any | None = None,
        target_beta0: int | None = None,
        target_beta1: int | None = None,
    ) -> dict[str, float]:
        """Return dict with total and components.

        Raises NotImplementedError until individual verifiers are implemented.
        """
        raise NotImplementedError(
            "CompositeReward wiring lands after R_cnt/R_sep/… implementations "
            "(roadmap Weeks 9–11)."
        )
