from hanziconv import HanziConv
from word_embeddings import word_tokenize


def test_word_tokenize():
    keywords = open('tests/word_tokens.txt').read().splitlines()
    keywords_s = map(HanziConv.toSimplified, keywords)
    for keyword in keywords_s:
        keyword_tk = word_tokenize(keyword)
        assert len(keyword_tk) == 1
