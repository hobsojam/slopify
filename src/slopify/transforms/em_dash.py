from __future__ import annotations

import random
import re

from slopify.transforms.base import Transform

# Conjunctions/commas that AI writing loves to replace with an em dash.
_TARGETS = re.compile(r"(?:,\s+| )(and|but|so|which)\s+")


class EmDashTransform(Transform):
    name = "em_dash"

    def apply(self, text: str, weight: float, rng: random.Random) -> str:
        def replace(match: re.Match) -> str:
            if rng.random() > weight:
                return match.group(0)
            return f" — {match.group(1)} "

        return _TARGETS.sub(replace, text)
