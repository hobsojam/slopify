from __future__ import annotations

import random

from slopify.transforms._sentences import split_sentences
from slopify.transforms.base import Transform

# Generic closers, not tied to the sentence's actual content. Good enough
# to trip a slop detector; a higher-fidelity version would extract the
# sentence's subject and reference it directly, which needs light NLP.
_CLOSERS = [
    "It plays a vital role in this space.",
    "It serves as a testament to what's possible.",
    "Its impact cannot be overstated.",
    "It leaves a lasting impression.",
]


class GrandioseTransform(Transform):
    """Appends inflated-significance closer sentences."""

    name = "grandiose"

    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        sentences = split_sentences(text)
        out = []
        for sentence in sentences:
            out.append(sentence)
            if rng.random() < weight:
                out.append(rng.choice(_CLOSERS))
        return " ".join(out)
