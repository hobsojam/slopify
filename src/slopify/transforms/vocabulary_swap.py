from __future__ import annotations

import json
import random
import re
from importlib import resources

from slopify.transforms.base import Transform


def _load_vocabulary() -> dict[str, str]:
    raw = resources.files("slopify.data").joinpath("ai_vocabulary.json").read_text(encoding="utf-8")
    return json.loads(raw)


class VocabularySwapTransform(Transform):
    name = "vocabulary_swap"

    def __init__(self) -> None:
        self._vocabulary = _load_vocabulary()
        # Longest phrase first so "important part" wins over the bare "important".
        terms = sorted(self._vocabulary, key=len, reverse=True)
        pattern = "|".join(re.escape(term) for term in terms)
        # Optionally capture a leading "a"/"an" so we can fix its agreement
        # with the replacement -- "an important part" must become "a vital
        # role", not "an vital role".
        self._pattern = re.compile(rf"\b(?:(a|an)\s+)?({pattern})\b", re.IGNORECASE)

    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        def replace(match: re.Match) -> str:
            if rng.random() > weight:
                return match.group(0)
            article, original = match.group(1), match.group(2)
            replacement = self._vocabulary[original.lower()]
            if article:
                correct_article = "an" if replacement[0].lower() in "aeiou" else "a"
                if article[0].isupper():
                    correct_article = correct_article.capitalize()
                return f"{correct_article} {replacement}"
            if original[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            return replacement

        return self._pattern.sub(replace, text)
