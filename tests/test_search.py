import ezra


def test_search_zh_hk():
    result = ezra.search("喜樂 事奉", zh_cn=False, verbose=True)
    assert "事奉" in result[0].verse


def test_search_zh_cn():
    result = ezra.search("喜乐 事奉", zh_cn=True, verbose=True)
    assert "事奉" in result[0].verse


def test_search_oov():
    result = ezra.search("苦害 銅匠", zh_cn=False, verbose=True)
    assert "苦害" in result[0].verse


def test_search_exact():
    result = ezra.search("聰明俊美", zh_cn=False, verbose=True, top_k=25)
    assert "聰明俊美" in result[0].verse
    assert "聰明" in result[1].verse
    assert "俊美" in result[1].verse
    assert len(result) == 25


def test_search_range():
    result = ezra.search("福音", zh_cn=False, in_book="letters", verbose=True)
    assert result[0].ref["book"] == "rom"


def test_related_keywords():
    result = ezra.related_keywords("喜樂 事奉")
    assert result[0] != "喜樂 事奉"
    assert "事奉" in result[0]
