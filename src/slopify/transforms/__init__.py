from slopify.transforms.base import Transform
from slopify.transforms.em_dash import EmDashTransform
from slopify.transforms.vocabulary_swap import VocabularySwapTransform
from slopify.transforms.triplets import TripletTransform
from slopify.transforms.sentence_fragment import SentenceFragmentTransform
from slopify.transforms.transitions import TransitionTransform
from slopify.transforms.hedging import HedgingTransform
from slopify.transforms.grandiose import GrandioseTransform

# Order matters: later transforms see the output of earlier ones.
# Vocabulary/transitions/hedging/grandiose run before structural
# transforms (fragmentation, triplets) so those see the swapped-in
# slop words too. EmDashTransform runs before SentenceFragmentTransform
# because both compete for the same "and"/"but" spots -- em dash is the
# more recognizable slop signal, so it gets first pick.
DEFAULT_PIPELINE_ORDER: list[type[Transform]] = [
    VocabularySwapTransform,
    TransitionTransform,
    HedgingTransform,
    GrandioseTransform,
    TripletTransform,
    EmDashTransform,
    SentenceFragmentTransform,
]

__all__ = [
    "Transform",
    "EmDashTransform",
    "VocabularySwapTransform",
    "TripletTransform",
    "SentenceFragmentTransform",
    "TransitionTransform",
    "HedgingTransform",
    "GrandioseTransform",
    "DEFAULT_PIPELINE_ORDER",
]
