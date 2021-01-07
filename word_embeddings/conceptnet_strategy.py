import itertools
import json
from importlib import resources
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from ezra import BibleSearchStrategy, Match
from sklearn.metrics.pairwise import cosine_similarity

from . import tokenize


class ConceptNetStrategy(BibleSearchStrategy):
    def __init__(self):
        with resources.path(__package__, 'mini.zh.h5') as hdf_file:
            self._embeddings: pd.DataFrame = pd.read_hdf(hdf_file)
        self._embeddings.index = self._embeddings.index.str.replace(
            '/c/zh/', '')
        verse_lines = resources.read_text(__package__, 'tokenized_verses.txt')\
                               .split('\n')[:-1]
        self._tokenized_verses = [verse.split() for verse in verse_lines]
        self._all_words = np.unique(
            [word for verse in self._tokenized_verses for word in verse])
        self._words_vec = self.get_word_vectors(self._all_words)
        self._words_no_vec = np.setdiff1d(
            self._all_words, self._words_vec.index)

    def search(self, keyword: str, top_k: int) -> List[Match]:
        keyword_tk = np.array(tokenize(keyword))
        kw_vec = self.get_word_vectors(keyword_tk)
        kw_no_vec = np.setdiff1d(keyword_tk, kw_vec.index)

        def compute_similarity() -> pd.DataFrame:
            similarity_cs = pd.DataFrame(
                cosine_similarity(self._words_vec, kw_vec),
                self._words_vec.index,
                kw_vec.index)
            similarity_kw_no_vec = pd.DataFrame.from_dict(
                {kw: np.where(self._words_vec.index == kw, 1, 0)
                 for kw in kw_no_vec}
            )  # .set_index(self._words_vec.index)
            similarity_no_vec = pd.DataFrame.from_dict(
                {kw: np.where(self._words_no_vec == kw, 1, 0)
                 for kw in keyword_tk}
            ).set_index(self._words_no_vec)
            similarity_all_kw = pd.concat(
                [similarity_cs, similarity_kw_no_vec], axis=1)
            return similarity_all_kw.append(similarity_no_vec)
        similarity = compute_similarity()

        verse_matches = []
        for i, tokens in enumerate(self._tokenized_verses):
            scores = similarity.loc[tokens]
            kw_scores = list(zip(scores.idxmax(), scores.max()))
            verse_matches.append(Match(i, kw_scores))

        sorted_matches = sorted(verse_matches, key=Match.score, reverse=True)
        return sorted_matches[:top_k]

    def get_word_vectors(self, words: np.ndarray) -> pd.DataFrame:
        in_vocab = words[np.isin(words, self._embeddings.index)]
        # TODO: OOV
        return self._embeddings.loc[in_vocab]
