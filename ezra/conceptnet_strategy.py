import itertools
import json
from importlib import resources
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from ezra import BibleSearchStrategy, Match
from sklearn.metrics.pairwise import cosine_similarity

from . import word_tokenize, to_simplified


class ConceptNetStrategy(BibleSearchStrategy):
    def __init__(self):
        with resources.path('ezra.resources', 'conceptnet.zh.h5') as hdf_file:
            self._embeddings: pd.DataFrame = pd.read_hdf(hdf_file)
        self._embeddings.index = self._embeddings.index.str.replace(
            '/c/zh/', '')

        verse_lines = resources.read_text('ezra.resources', 'word_tokenized_verses.txt')\
                               .split('\n')[:-1]
        word_tokenized_verses = [verse.split() for verse in verse_lines]
        all_words = np.unique(
            [word for verse in word_tokenized_verses for word in verse])
        self._words_vec, self._words_no_vec = self._get_word_vectors(all_words)

        tokenized_verses = [np.unique(list(map(self._tokenize, verse)))
                            for verse in word_tokenized_verses]
        max_length = max(map(len, tokenized_verses))
        self._tokenized_verses = np.stack([np.append(v, np.zeros(max_length - v.size, int))
                                           for v in tokenized_verses])

    def search(self, keyword: str, top_k: int) -> List[Match]:
        keyword_tk = np.array(list(word_tokenize(keyword)))
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

        all_match_scores = similarity[:, self._tokenized_verses]
        kw_verse_scores = np.amax(all_match_scores, axis=2)
        verse_scores = kw_verse_scores.sum(axis=0)
        top_matches = np.argsort(verse_scores)[-1:-top_k-1:-1]

        def create_match(index: int) -> Match:
            tokens = self._tokenized_verses[index]
            kw_scores = []
            for kw in range(len(keyword_tk)):
                scores = similarity[kw, tokens]
                match_word = np.argmax(scores)
                match_token = tokens[match_word]
                kw_scores.append((self._detokenize(match_token),
                                  scores[match_word]))
            return Match(index, kw_scores)
        return [create_match(i) for i in top_matches]

    def _similarity_oov(self, xs: np.array, ys: np.array) -> np.ndarray:
        return np.stack([np.where(ys == x, 1, 0) for x in xs])

    def _get_word_vectors(self, words: np.array) -> Tuple[pd.DataFrame, np.array]:
        in_vocab = [word for word in words if self._in_vocab(to_simplified(word))]
        out_of_vocab = np.setdiff1d(words, in_vocab)
        word_vec = self._embeddings.loc[map(to_simplified, in_vocab)]
        word_vec.index = in_vocab
        return word_vec, out_of_vocab

    def _in_vocab(self, word: str) -> bool:
        # TODO: OOV
        return word in self._embeddings.index

    _reserved_token_length = 1

    def _tokenize(self, word: str) -> int:
        try:
            index_by_vocab = self._words_vec.index.get_loc(word)
        except KeyError:
            no_vec_index = np.where(self._words_no_vec == word)[0][0]
            index_by_vocab = no_vec_index + len(self._words_vec)
        return ConceptNetStrategy._reserved_token_length + index_by_vocab

    def _detokenize(self, token: int) -> str:
        index = token - ConceptNetStrategy._reserved_token_length
        try:
            return self._words_vec.index[index]
        except KeyError:
            index -= len(self._words_vec)
            return self._words_no_vec[index]
