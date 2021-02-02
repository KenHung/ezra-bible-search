from importlib import resources
from typing import Iterable

import jieba
import jieba.posseg as pseg

from ..lang import to_simplified

_bible_tokens_loaded: bool = False


def word_tokenize(sentence: str) -> Iterable[str]:
    global _bible_tokens_loaded
    if not _bible_tokens_loaded:
        for token_file in ["classics.txt", "names.txt"]:
            tokens = resources.open_text(__package__, token_file)
            jieba.load_userdict(tokens)
        _bible_tokens_loaded = True

    sentence_s = to_simplified(sentence)
    assert len(sentence) == len(sentence_s)
    total = 0
    for tk in pseg.cut(sentence_s):
        tk.word = sentence[total : total + len(tk.word)]
        total += len(tk.word)
        if tk.flag != "x":
            yield tk.word
