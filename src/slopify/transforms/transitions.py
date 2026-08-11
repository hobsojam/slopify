from __future__ import annotations

import random

from slopify.transforms._sentences import lowercase_first, map_sentences
from slopify.transforms.base import Transform

_TRANSITIONS = ["Additionally, ", "Moreover, ", "Furthermore, ", "Notably, ", "Consequently, "]


class TransitionTransform(Transform):
    """Prepends formulaic transition words to sentence starts."""

    name = "transitions"

    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        def transform(sentences: list[str]) -> list[str]:
            out = []
            for i, sentence in enumerate(sentences):
                if i > 0 and rng.random() < weight:
                    sentence = rng.choice(_TRANSITIONS) + lowercase_first(sentence)
                out.append(sentence)
            return out

        return map_sentences(text, transform)
