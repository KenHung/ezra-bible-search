import pickle
from importlib import resources
from itertools import groupby, product
from typing import List

import numpy as np

from .resources.db import ccn_embeddings
from .search import BibleSearchStrategy, Match
from .word_tokenizer import word_tokenize


class ConceptNetStrategy(BibleSearchStrategy):
    def __init__(self):
        """
        Initialize search required data, it can be saved and re-loaded to skip
        initialization every time. It has 3 steps:
        1. Word tokenize the whole Bible (turn sentences into word pieces)
        2. Get word vectors of words exist in the Bible
        3. Tokenize each word in the Bible (use a unique number to repsent each word)
           for performance reason
        """
        from .resources import bible

        print("Word tokenizing verses...")
        dots = r"[•‧．・\-]"
        verses = bible.text.str.replace(dots, "", regex=True)
        word_tokenized_verses = verses.transform(lambda v: list(word_tokenize(v)))

        print("Getting word vectors...")
        self._all_words = np.unique(
            [word for verse in word_tokenized_verses for word in verse]
        )
        self._words_vec = ccn_embeddings.get_word_vectors(self._all_words)

        print("Tokenizing verses...")
        tokenized_verses = [
            list(set(map(self._tokenize, verse))) for verse in word_tokenized_verses
        ]
        max_length = max(map(len, tokenized_verses))
        self._tokenized_verses = np.array(
            [v + [0] * (max_length - len(v)) for v in tokenized_verses]
        )

    def to_pickle(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def from_pickle(cls):
        with resources.open_binary("ezra.resources", "conceptnet_strategy.pickle") as f:
            return pickle.load(f)

    def search(
        self, keyword: str, top_k: int, in_range: np.ndarray = None
    ) -> List[Match]:
        similarity = self.compute_similarity(keyword)

        verses_in_range = (
            self._tokenized_verses[in_range]
            if in_range is not None
            else self._tokenized_verses
        )
        # there are two parts of score: cosine similarity and count of good keywords
        all_match_scores = similarity[:, verses_in_range]
        match_kw_idx = all_match_scores.argmax(axis=2).T
        match_tokens = np.take_along_axis(verses_in_range, match_kw_idx, axis=1).T
        kw_verse_scores = np.take_along_axis(similarity, match_tokens, axis=1)
        verse_scores = np.core.records.fromarrays(
            [
                kw_verse_scores.sum(axis=0),
                np.where(kw_verse_scores >= 0.5, 1, 0).sum(axis=0),
            ],
            names="total,good_kw_counts",
        )
        verse_sorted_idx = np.flip(
            np.argsort(verse_scores, order=["good_kw_counts", "total"])
        )
        top_matches = verse_sorted_idx[:top_k]

        def create_match(index: int) -> Match:
            match_kw = map(self._detokenize, match_tokens.T[index])
            kw_scores = list(zip(match_kw, kw_verse_scores.T[index]))
            index_global = in_range[index] if in_range is not None else index
            return Match(index_global, kw_scores)

        return [create_match(i) for i in top_matches]

    def related_keywords(self, keyword: str, top_k: int = 5) -> List[str]:
        similarity = self.compute_similarity(keyword)
        relevant_tk = np.argwhere(similarity >= 0.5)
        tk_groups = []
        for _, g in groupby(relevant_tk, lambda r: r[0]):
            tk_groups.append(list(map(lambda r: r[1], g)))
        tk_combinations = np.array(list(product(*tk_groups)))
        if tk_combinations.size > 0:
            tk_scores = np.take_along_axis(similarity, tk_combinations.T, axis=1)
            total_scores = tk_scores.sum(axis=0)
            tk_idx = np.flip(np.argsort(total_scores))
            top_suggestions = tk_combinations[tk_idx]
            suggestions = [" ".join(s) for s in map(self._detokenize, top_suggestions)]
            return [s for s in suggestions if s != keyword][:top_k]
        else:
            return []

    def compute_similarity(self, keyword: str) -> np.ndarray:
        keyword_tk = np.array(list(word_tokenize(keyword)))
        kw_vec = ccn_embeddings.get_word_vectors(keyword_tk)

        reserved_tokens = np.zeros((keyword_tk.size, 1))
        exact = pairwise_equal(keyword_tk, self._all_words)
        cosine = self._pairwise_cosine_similarity_words_vec(kw_vec)
        concat = np.where(exact, 1, cosine)
        return np.hstack((reserved_tokens, concat))

    # to reduce load time of Sci-Kit Learn, cosine similarity was implemented
    # the result should be the same as `sklearn.metrics.pairwise.cosine_similarity()`
    def _pairwise_cosine_similarity_words_vec(self, kw_vec: np.ndarray) -> np.ndarray:
        if not hasattr(self, "_words_vec_normalized"):
            self._words_vec_normalized = normalize(self._words_vec).T
        return normalize(kw_vec).dot(self._words_vec_normalized)

    # reserve token for padding
    _reserved_token_length = 1

    def _tokenize(self, word: str) -> int:
        index = np.argmax(self._all_words == word)
        return ConceptNetStrategy._reserved_token_length + index

    def _detokenize(self, token: int) -> str:
        index = token - ConceptNetStrategy._reserved_token_length
        return self._all_words[index]


def pairwise_equal(xs: np.array, ys: np.array) -> np.ndarray:
    return np.stack([ys == x for x in xs])


def normalize(X: np.ndarray) -> np.ndarray:
    X = X.astype(float)
    l2_norms = np.einsum("ij,ij->i", X, X)
    np.sqrt(l2_norms, l2_norms)
    l2_norms[l2_norms == 0.0] = 1.0
    X /= l2_norms[:, np.newaxis]
    return X
