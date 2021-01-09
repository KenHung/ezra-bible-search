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
        self._words_vec, self._words_no_vec = self._get_word_vectors(all_words)

        num_tk_verses = [np.unique(list(map(self._num_tokenize, verse)))
                         for verse in tokenized_verses]
        max_length = max(map(len, num_tk_verses))
        self._num_tk_verses = np.stack([np.append(v, np.zeros(max_length - v.size, int))
                                        for v in num_tk_verses])

    _reserved_token_length = 1

    def _num_tokenize(self, word: str) -> int:
        try:
            index_by_vocab = self._words_vec.index.get_loc(word)
        except KeyError:
            no_vec_index = np.where(self._words_no_vec == word)[0][0]
            index_by_vocab = no_vec_index + len(self._words_vec)
        return ConceptNetStrategy._reserved_token_length + index_by_vocab

    def _num_detokenize(self, token: int) -> str:
        index = token - ConceptNetStrategy._reserved_token_length
        try:
            return self._words_vec.index[index]
        except KeyError:
            index -= len(self._words_vec)
            return self._words_no_vec[index]

    def search(self, keyword: str, top_k: int) -> List[Match]:
        keyword_tk = np.array(tokenize(keyword))
        kw_vec, kw_no_vec = self._get_word_vectors(keyword_tk)

        def compute_similarity() -> pd.DataFrame:
            reserved_tokens = np.zeros((keyword_tk.size, 1))
            in_vocab = cosine_similarity(kw_vec, self._words_vec)
            if len(kw_no_vec) > 0:
                kw_oov = self._similarity_oov(kw_no_vec, self._words_vec.index)
                all_kw = np.stack((in_vocab,  kw_oov))
            else:
                all_kw = in_vocab
            verse_oov = self._similarity_oov(keyword_tk, self._words_no_vec)
            return np.hstack((reserved_tokens, all_kw, verse_oov))
        similarity = compute_similarity()

        all_match_scores = similarity[:, self._num_tk_verses]
        kw_verse_scores = np.amax(all_match_scores, axis=2)
        verse_scores = kw_verse_scores.sum(axis=0)
        top_matches = np.argsort(verse_scores)[-1:-top_k-1:-1]

        def find_match(kw, tokens):
            scores = similarity[kw, tokens]
            match_word = np.argmax(scores)
            return self._num_detokenize(tokens[match_word]), scores[match_word]
        top_matches_info = []
        for index in top_matches:
            tokens = self._num_tk_verses[index]
            kw_scores = [find_match(kw, tokens)
                         for kw in range(len(keyword_tk))]
            top_matches_info.append(Match(index, kw_scores))
        return top_matches_info

    def _similarity_oov(self, xs: np.array, ys: np.array) -> np.ndarray:
        return np.stack([np.where(ys == x, 1, 0) for x in xs])

    def _get_word_vectors(self, words: np.ndarray) -> Tuple[pd.DataFrame, np.array]:
        in_vocab = [word for word in words if self._in_vocab(word)]
        out_of_vocab = np.setdiff1d(words, in_vocab)
        return self._embeddings.loc[in_vocab], out_of_vocab

    def _in_vocab(self, word: str) -> bool:
        # TODO: OOV
        return word in self._embeddings.index
