"""Non-differentiable structural reward verifiers.

These modules implement the discrete reward terms from the S-Seg-RLVR proposal.
They are intentionally non-differentiable (thresholding, connected components,
Hungarian matching, Betti numbers). GRPO consumes their scalar outputs.

Status: stubs with docstrings — implement in Weeks 9–11.
"""

from sseg_rlvr.rewards.composite import CompositeReward, RewardWeights
from sseg_rlvr.rewards.count import count_reward
from sseg_rlvr.rewards.format_reward import format_reward
from sseg_rlvr.rewards.match import match_reward
from sseg_rlvr.rewards.separation import separation_reward
from sseg_rlvr.rewards.topology import topology_reward

__all__ = [
    "CompositeReward",
    "RewardWeights",
    "count_reward",
    "separation_reward",
    "topology_reward",
    "match_reward",
    "format_reward",
]
