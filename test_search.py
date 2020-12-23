import jieba
import jieba.posseg as pseg

from search import sentence_similarity

jieba.enable_paddle()


def test_search():
    kw = '信心 行事'
    vers = '我靠主大大地喜乐，因为你们思念我的心如今又发生；你们向来就思念我，只是没得机会。'
    kw_tk = pseg.lcut(kw, use_paddle=True)
    vers_tk = pseg.lcut(vers, use_paddle=True)
    similarity = sentence_similarity(kw_tk, vers_tk)
    assert similarity >= 0
