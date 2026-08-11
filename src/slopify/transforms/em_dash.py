from __future__ import annotations

import random
import re

from slopify.transforms.base import Transform

# Conjunctions/commas that AI writing loves to replace with an em dash.
_CONJUNCTIONS = re.compile(r"(?:,\s+| )(and|but|so|which)\s+")
# A comma before a participial clause ("...text, revealing the tell") is one
# of the single most common em-dash triggers in AI writing -- "including",
# "highlighting", "revealing", etc.
_COMMA_PARTICIPLE = re.compile(r",\s+(\w+ing\b)")
# Parenthetical asides get dashed instead of bracketed: "the tool (which is
# free)" -> "the tool — which is free —".
_PARENTHETICAL = re.compile(r"\s*\(([^()]{1,80})\)")


class EmDashTransform(Transform):
    name = "em_dash"

    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        def replace_conjunction(match: re.Match) -> str:
            if rng.random() > weight:
                return match.group(0)
            word = match.group(1)
            # "and"/"but"/"so" are pure conjunctions -- the dash can fully
            # replace them ("fast and reliable" -> "fast — reliable"), which
            # also matters mechanically: leaving the word in place meant
            # SentenceFragmentTransform, which runs right after, would match
            # that same "and"/"but" again and fragment it too, producing
            # "written —. And you want ...". "which" is a relative pronoun
            # the clause needs, so only the comma before it gets dashed.
            if word.lower() == "which":
                return f" — {word} "
            return " — "

        def replace_participle(match: re.Match) -> str:
            if rng.random() > weight:
                return match.group(0)
            return f" — {match.group(1)}"

        def replace_parenthetical(match: re.Match) -> str:
            if rng.random() > weight:
                return match.group(0)
            return f" — {match.group(1).strip()} —"

        text = _CONJUNCTIONS.sub(replace_conjunction, text)
        text = _COMMA_PARTICIPLE.sub(replace_participle, text)
        text = _PARENTHETICAL.sub(replace_parenthetical, text)
        return text
