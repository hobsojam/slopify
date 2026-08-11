from __future__ import annotations

import re

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_SPLIT.split(text) if s]


def lowercase_first(sentence: str) -> str:
    if sentence and sentence[0].isupper() and not sentence[:2].isupper():
        return sentence[0].lower() + sentence[1:]
    return sentence
