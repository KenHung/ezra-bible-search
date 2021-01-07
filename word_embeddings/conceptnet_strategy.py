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
        tokenized_verses = [verse.split() for verse in verse_lines]
        all_words = np.unique(
            [word for verse in tokenized_verses for word in verse])
        self._words_vec = self.get_word_vectors(all_words)
        self._words_no_vec = np.setdiff1d(all_words, self._words_vec.index)

        def to_num_tk(word: str) -> int:
            try:
                return self._words_vec.index.get_loc(word)
            except KeyError:
                return np.where(self._words_no_vec == word)[0][0] + len(self._words_vec)
        self._num_tk_verses = [np.unique(list(map(to_num_tk, verse)))
                               for verse in tokenized_verses]

    def search(self, keyword: str, top_k: int) -> List[Match]:
        keyword_tk = np.array(tokenize(keyword))
        kw_vec = self.get_word_vectors(keyword_tk)
        kw_no_vec = np.setdiff1d(keyword_tk, kw_vec.index)

        def compute_similarity() -> pd.DataFrame:
            similarity_cs = cosine_similarity(kw_vec, self._words_vec)
            similarity_kw_no_vec = pd.DataFrame.from_dict(
                {kw: np.where(self._words_vec.index == kw, 1, 0)
                 for kw in kw_no_vec}
            )  # .set_index(self._words_vec.index)
            similarity_no_vec = np.stack([np.where(self._words_no_vec == kw, 1, 0)
                                          for kw in keyword_tk])
            # similarity_all_kw = pd.concat(
            #    [similarity_cs, similarity_kw_no_vec], axis=1)
            return np.hstack((similarity_cs, similarity_no_vec))
        similarity = compute_similarity()

        verse_matches = []
        for i, tokens in enumerate(self._num_tk_verses):
            kw_scores = []
            for kw in range(len(keyword_tk)):
                scores = similarity[kw][tokens]
                max_word = np.argmax(scores)
                kw_scores.append((tokens[max_word], scores[max_word]))
            verse_matches.append(Match(i, kw_scores))

        top_matches = sorted(
            verse_matches, key=Match.score, reverse=True)[:top_k]
        for m in top_matches:
            m.kw_scores = [(self._words_vec.index[kw], score)
                           for kw, score in m.kw_scores]
        return top_matches

    def get_word_vectors(self, words: np.ndarray) -> pd.DataFrame:
        in_vocab = words[np.isin(words, self._embeddings.index)]
        # TODO: OOV
        return self._embeddings.loc[in_vocab]
