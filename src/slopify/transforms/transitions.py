from __future__ import annotations

import random

from slopify.transforms._sentences import lowercase_first, split_sentences
from slopify.transforms.base import Transform

_TRANSITIONS = ["Additionally, ", "Moreover, ", "Furthermore, ", "Notably, ", "Consequently, "]


class TransitionTransform(Transform):
    """Prepends formulaic transition words to sentence starts."""

    name = "transitions"

    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        sentences = split_sentences(text)
        out = []
        for i, sentence in enumerate(sentences):
            if i > 0 and rng.random() < weight:
                sentence = rng.choice(_TRANSITIONS) + lowercase_first(sentence)
            out.append(sentence)
        return " ".join(out)
