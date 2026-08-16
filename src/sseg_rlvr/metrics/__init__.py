"""Evaluation metrics for S-Seg-RLVR (PQ, count error, merge/split rates).

Implement alongside rewards in Weeks 9–12.
"""

from __future__ import annotations

from typing import Any


def count_absolute_error(pred_count: int, true_count: int) -> float:
    """|pred_count - true_count|."""
    return float(abs(pred_count - true_count))


def merge_rate(pred_mask: Any, points: Any) -> float:
    """Fraction of predicted components that cover ≥2 point markers.

    NotImplemented until separation utilities exist.
    """
    raise NotImplementedError("merge_rate — Weeks 9–12")
