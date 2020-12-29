import jieba
import jieba.posseg as pseg

import search


def test_search():
    kw = '欢乐 祈祷'
    vers = '亚当生塞特；塞特生以挪士；'
    kw_tk = pseg.lcut(kw)
    vers_tk = pseg.lcut(vers)
    similarity = search.sentence_similarity(kw_tk, vers_tk)
    assert similarity is not None


def test_conceptnet_similarity():
    search.load_conceptnet_terms('data/conceptnet')
    assert search.similarity('喜乐', '欢喜') > 0
