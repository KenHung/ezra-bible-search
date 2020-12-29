import jieba.posseg as pseg

import search


def test_search():
    kw = '欢乐 祈祷'
    vers = '亚当生塞特；塞特生以挪士；'
    kw_tk = pseg.lcut(kw)
    vers_tk = pseg.lcut(vers)
    search.load_word_embeddings('data/mini.h5')
    similarity = search.sentence_similarity(kw_tk, vers_tk)
    assert similarity is not None


def test_conceptnet_similarity():
    search.load_word_embeddings('data/mini.h5')
    assert search.similarity('欢乐', '欢欣') > 0
