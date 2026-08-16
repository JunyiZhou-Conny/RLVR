"""Dataset helpers: point simulation from instance masks, loaders.

No raw pathology data lives in this repo. Implement simulators on synthetic
or externally downloaded data under a local `data/` directory (gitignored).
"""

from __future__ import annotations

from typing import Any


def instance_masks_to_points(instance_mask: Any) -> list[tuple[float, float]]:
    """Degrade an instance label map to centroids (one point per instance).

    Planned for the weak-label simulation pipeline (Week 12+).
    """
    raise NotImplementedError("instance_masks_to_points — Week 12+")
