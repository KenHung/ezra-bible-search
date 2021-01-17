from ezra import BibleSearchEngine
from pytest import fixture
from word_embeddings.conceptnet_strategy import ConceptNetStrategy


@fixture()
def ezra_engine():
    strategy = ConceptNetStrategy()
    return BibleSearchEngine(strategy)
