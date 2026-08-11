from slopify.config import SlopifyConfig
from slopify.deslopify import deslopify
from slopify.pipeline import Pipeline

SAMPLE = "I use this tool to explore ideas and write faster. It is an important part of my process."

MULTI_PARAGRAPH = (
    "First paragraph, one sentence.\n\n"
    "Second paragraph, also one sentence."
)


def test_pipeline_runs_at_zero_intensity_unchanged():
    result = Pipeline(SlopifyConfig(intensity=0)).run(SAMPLE)
    assert result.text == SAMPLE
    assert result.log.entries == []


def test_pipeline_changes_text_at_full_intensity():
    result = Pipeline(SlopifyConfig(intensity=100, seed=1)).run(SAMPLE)
    assert result.text != SAMPLE


def test_pipeline_preserves_paragraph_breaks():
    result = Pipeline(SlopifyConfig(intensity=100, seed=1)).run(MULTI_PARAGRAPH)
    assert "\n\n" in result.text
    assert result.text.count("\n\n") == 1


def test_deslopify_reverses_slopify_exactly():
    result = Pipeline(SlopifyConfig(intensity=100, seed=1)).run(SAMPLE)
    restored = deslopify(result.text, result.log)
    assert restored == SAMPLE


def test_deslopify_rejects_diverged_text():
    result = Pipeline(SlopifyConfig(intensity=100, seed=1)).run(SAMPLE)
    if not result.log.entries:
        return
    try:
        deslopify(result.text + " extra", result.log)
        assert False, "expected ValueError"
    except ValueError:
        pass
