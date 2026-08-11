import random

from slopify.transforms.em_dash import EmDashTransform


def test_em_dash_replaces_conjunction_at_full_weight():
    result = EmDashTransform().apply("It works and it scales.", weight=1.0, rng=random.Random(0))
    assert "—" in result


def test_em_dash_leaves_text_untouched_at_zero_weight():
    text = "It works and it scales."
    result = EmDashTransform().apply(text, weight=0.0, rng=random.Random(0))
    assert result == text
