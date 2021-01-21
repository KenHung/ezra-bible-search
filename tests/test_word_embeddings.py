from ezra import word_tokenize


def test_word_tokenize():
    keywords = open('tests/word_tokens.txt').read().splitlines()
    for keyword in keywords:
        keyword_tk = word_tokenize(keyword)
        assert next(keyword_tk) == keyword
