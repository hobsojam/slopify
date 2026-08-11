from __future__ import annotations

import re
from typing import Callable

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_PARAGRAPH_SPLIT = re.compile(r"(\n\s*\n)")


def split_sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_SPLIT.split(text) if s]


def lowercase_first(sentence: str) -> str:
    if sentence and sentence[0].isupper() and not sentence[:2].isupper():
        return sentence[0].lower() + sentence[1:]
    return sentence


def map_sentences(text: str, fn: Callable[[list[str]], list[str]]) -> str:
    """Applies `fn` to the sentences within each paragraph independently.

    Paragraph breaks (blank lines) are captured and reinserted verbatim, so
    multi-paragraph input doesn't get flattened into a single line -- only
    the whitespace *within* a paragraph (single line breaks, wrapping) gets
    reflowed to a single space, same as before.
    """
    parts = _PARAGRAPH_SPLIT.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = " ".join(fn(split_sentences(parts[i])))
    return "".join(parts)
