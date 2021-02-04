def test_search_zh_hk(ezra_engine):
    result = ezra_engine.search("喜樂 事奉", zh_cn=False, verbose=True)
    assert "事奉" in result[0].verse


def test_search_zh_cn(ezra_engine):
    result = ezra_engine.search("喜乐 事奉", zh_cn=True, verbose=True)
    assert "事奉" in result[0].verse


def test_search_oov(ezra_engine):
    result = ezra_engine.search("苦害 銅匠", zh_cn=False, verbose=True)
    assert "苦害" in result[0].verse
