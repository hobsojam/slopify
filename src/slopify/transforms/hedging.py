from __future__ import annotations

import random

from slopify.transforms._sentences import lowercase_first, split_sentences
from slopify.transforms.base import Transform

_HEDGES = [
    "It's important to note that ",
    "Generally speaking, ",
    "To some extent, ",
    "In many cases, ",
]


class HedgingTransform(Transform):
    """Prepends cautious hedging phrases to sentence starts."""

    name = "hedging"

    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        sentences = split_sentences(text)
        out = []
        for sentence in sentences:
            if rng.random() < weight:
                sentence = rng.choice(_HEDGES) + lowercase_first(sentence)
            out.append(sentence)
        return " ".join(out)
