from __future__ import annotations

import random

from slopify.transforms.base import Transform


class TripletTransform(Transform):
    """Rule-of-three restatement: "fast, reliable, and thorough" for one idea.

    Stubbed out. Unlike the other transforms here, this one needs a real
    paraphrase of content the pipeline doesn't understand (near-synonyms
    for whatever the sentence is actually about) -- regex can't generate
    that. Fill in with a WordNet/thesaurus lookup or a small LLM call;
    see the slopify/deslopify design discussion on hybrid architecture.
    """

    name = "triplets"

    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        return text
