from ezra import BibleSearchEngine
from pytest import fixture
from ezra.conceptnet_strategy import ConceptNetStrategy


@fixture()
def ezra_engine():
    strategy = ConceptNetStrategy()
    return BibleSearchEngine(strategy)
