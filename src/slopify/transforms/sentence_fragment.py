from __future__ import annotations

import random
import re

from slopify.transforms._sentences import map_sentences
from slopify.transforms.base import Transform

_SPLIT_POINT = re.compile(r"\s+(and|but)\s+")


class SentenceFragmentTransform(Transform):
    """Breaks conjunction clauses into short, punchy fragments.

    e.g. "It rewrites the text and keeps the meaning." ->
         "It rewrites the text. And keeps the meaning."

    This is a mechanical split, not a real subject-drop rewrite (that
    needs POS tagging to know what to drop) -- it just capitalizes the
    conjunction and starts a new sentence, which is enough to read as
    the short-fragment AI-slop cadence.
    """

    name = "sentence_fragment"

    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        def transform(sentences: list[str]) -> list[str]:
            out = []
            for sentence in sentences:
                match = _SPLIT_POINT.search(sentence)
                if match and rng.random() < weight:
                    head = sentence[: match.start()].rstrip()
                    conjunction = match.group(1)
                    tail = sentence[match.end() :]
                    if not head.endswith((".", "!", "?")):
                        head += "."
                    out.append(head)
                    out.append(f"{conjunction.capitalize()} {tail}")
                else:
                    out.append(sentence)
            return out

        return map_sentences(text, transform)
