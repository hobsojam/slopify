from __future__ import annotations

import random
from abc import ABC, abstractmethod


class Transform(ABC):
    """One slopification technique (em dashes, vocabulary swaps, etc.).

    `weight` is 0-1 (already resolved from SlopifyConfig.weight_for) and
    should be read as "probability of touching any given eligible spot",
    not "how many times to run".
    """

    name: str

    @abstractmethod
    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        raise NotImplementedError
