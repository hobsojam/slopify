from __future__ import annotations

import random

from slopify.transforms._sentences import lowercase_first, map_sentences
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
        def transform(sentences: list[str]) -> list[str]:
            out = []
            for sentence in sentences:
                # These hedges all read as a declarative lead-in ("It's
                # important to note that ...") -- grafted onto a question
                # they produce something ungrammatical like "It's important
                # to note that what is the point?".
                is_question = sentence.rstrip().endswith("?")
                if not is_question and rng.random() < weight:
                    sentence = rng.choice(_HEDGES) + lowercase_first(sentence)
                out.append(sentence)
            return out

        return map_sentences(text, transform)
