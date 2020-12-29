import itertools
import json
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import wordnet as wn
from sklearn.metrics.pairwise import cosine_similarity


def sentence_similarity(keywords_tokens, sentence_tokens):
    keywords = [tk.word for tk in remove_stopwords(keywords_tokens)]
    sentence_tokens = remove_stopwords(sentence_tokens)
    kw_score = {}
    for kw in keywords:
        word_score = {tk.word: similarity(kw, tk.word)
                      for tk in sentence_tokens}
        if word_score:
            match_word = max(word_score, key=word_score.get)
            kw_score[match_word] = word_score[match_word]
        else:
            kw_score[''] = 0
    return kw_score


def remove_stopwords(tokens) -> list:
    # TODO: return tk.word
    return [tk for tk in tokens if tk.flag != 'x']


@lru_cache(maxsize=None)
def similarity(word1: str, word2: str) -> float:
    if word1 == word2:
        return 1

    try:
        vec1 = _embeddings.loc[f'/c/zh/{word1}'].to_numpy()
        vec2 = _embeddings.loc[f'/c/zh/{word2}'].to_numpy()
        return cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
    except KeyError:
        # TODO: try to find related terms and compare
        return 0


_embeddings: pd.DataFrame = None


def load_word_embeddings(path: str) -> None:
    global _embeddings
    _embeddings = pd.read_hdf(path)
    _embeddings = _embeddings[_embeddings.index.str.startswith('/c/zh')]
