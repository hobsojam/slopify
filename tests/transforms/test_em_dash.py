import random

from slopify.transforms.em_dash import EmDashTransform


def test_em_dash_replaces_conjunction_at_full_weight():
    result = EmDashTransform().apply("It works and it scales.", weight=1.0, rng=random.Random(0))
    assert result == "It works — it scales."


def test_em_dash_drops_conjunction_so_fragment_cant_rematch_it():
    from slopify.transforms.sentence_fragment import SentenceFragmentTransform

    text = "It rewrites the text and it scales."
    after_em_dash = EmDashTransform().apply(text, weight=1.0, rng=random.Random(0))
    after_fragment = SentenceFragmentTransform().apply(after_em_dash, weight=1.0, rng=random.Random(0))
    assert "—." not in after_fragment
    assert after_fragment == after_em_dash


def test_em_dash_leaves_text_untouched_at_zero_weight():
    text = "It works and it scales."
    result = EmDashTransform().apply(text, weight=0.0, rng=random.Random(0))
    assert result == text


def test_em_dash_replaces_comma_before_participle():
    result = EmDashTransform().apply(
        "It rewrites the text, revealing the trick.", weight=1.0, rng=random.Random(0)
    )
    assert result == "It rewrites the text — revealing the trick."


def test_em_dash_replaces_parenthetical():
    result = EmDashTransform().apply(
        "The tool (which is free) helps.", weight=1.0, rng=random.Random(0)
    )
    assert result == "The tool — which is free — helps."
