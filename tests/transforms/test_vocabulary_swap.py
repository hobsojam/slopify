import random

from slopify.transforms.vocabulary_swap import VocabularySwapTransform


def test_article_agreement_fixed_for_consonant_replacement():
    result = VocabularySwapTransform().apply(
        "It is an important part of my process.", weight=1.0, rng=random.Random(0)
    )
    assert "a vital role" in result
    assert "an vital role" not in result


def test_article_agreement_fixed_for_vowel_replacement():
    result = VocabularySwapTransform().apply("It is a complex system.", weight=1.0, rng=random.Random(0))
    assert "an intricate system" in result
