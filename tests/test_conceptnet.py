from ezra import BibleSearchEngine
from word_embeddings.conceptnet_strategy import ConceptNetStrategy


def test_search():
    strategy = ConceptNetStrategy()
    ezra_engine = BibleSearchEngine(strategy)
    result = ezra_engine.search('喜乐 事奉', verbose=True)
    assert result is not None
