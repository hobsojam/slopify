import random

from slopify.transforms.hedging import HedgingTransform


def test_hedging_skips_questions():
    result = HedgingTransform().apply("What is the point?", weight=1.0, rng=random.Random(0))
    assert result == "What is the point?"


def test_hedging_applies_to_statements():
    result = HedgingTransform().apply("This is a statement.", weight=1.0, rng=random.Random(0))
    assert result != "This is a statement."
