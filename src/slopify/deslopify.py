from __future__ import annotations

from slopify.transformlog import TransformLog


def deslopify(text: str, log: TransformLog) -> str:
    """Exact inverse of a slopify run, using its recorded transform log.

    This only undoes text slopify itself produced. It is not a general
    "clean up any AI slop" tool -- that's a harder, separate problem (see
    project notes) since there's no log to replay against arbitrary text.
    """
    return log.reverse(text)
