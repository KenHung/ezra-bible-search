from importlib import resources
from typing import List

import jieba
import jieba.posseg as pseg

_bible_terms_loaded: bool = False


def tokenize(verse: str, remove_punctuation: bool = True) -> List[str]:
    global _bible_terms_loaded
    if not _bible_terms_loaded:
        bible_terms = resources.open_text(__name__, 'bible_terms.txt')
        jieba.load_userdict(bible_terms)
        _bible_terms_loaded = True

    if remove_punctuation:
        def filter_cond(tk): return tk.flag != 'x'
    else:
        def filter_cond(_): return True
    return [tk.word for tk in pseg.lcut(verse) if filter_cond(tk)]
