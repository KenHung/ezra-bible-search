from ezra import BibleSearchEngine
from pytest import fixture
from ezra.conceptnet_strategy import ConceptNetStrategy


@fixture(scope='module')
def ezra_engine():
    strategy = ConceptNetStrategy.from_pickle()
    return BibleSearchEngine(strategy)
