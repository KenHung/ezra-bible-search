from importlib import resources
from typing import Iterable

import jieba
import jieba.posseg as pseg
from opencc import OpenCC

_bible_tokens_loaded: bool = False
_t2s = OpenCC('t2s.json')


def word_tokenize(sentence: str) -> Iterable[str]:
    global _bible_tokens_loaded
    if not _bible_tokens_loaded:
        for token_file in ['classics.txt', 'names.txt']:
            tokens = resources.open_text(f'{__name__}.word_tokens', token_file)
            jieba.load_userdict(tokens)
        _bible_tokens_loaded = True

    sentence_s = _t2s.convert(sentence)
    assert len(sentence) == len(sentence_s)
    total = 0
    for tk in pseg.cut(sentence_s):
        tk.word = sentence[total:total+len(tk.word)]
        total += len(tk.word)
        if tk.flag != 'x':
            yield tk.word
