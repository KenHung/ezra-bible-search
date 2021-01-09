from importlib import resources
from typing import List

import jieba
import jieba.posseg as pseg

_bible_tokens_loaded: bool = False


def word_tokenize(verse: str, remove_punctuation: bool = True) -> List[str]:
    global _bible_tokens_loaded
    if not _bible_tokens_loaded:
        for token_file in ['classics.txt', 'names.txt']:
            tokens = resources.open_text(f'{__name__}.word_tokens', token_file)
            jieba.load_userdict(tokens)
        _bible_tokens_loaded = True

    if remove_punctuation:
        def filter_cond(tk): return tk.flag != 'x'
    else:
        def filter_cond(_): return True
    return [tk.word for tk in pseg.lcut(verse) if filter_cond(tk)]
