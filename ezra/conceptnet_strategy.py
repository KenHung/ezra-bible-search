import pickle
from importlib import resources
from typing import List

import numpy as np

from .resources.db import ccn_embeddings
from .search import BibleSearchStrategy, Match
from .word_tokenizer import word_tokenize


class ConceptNetStrategy(BibleSearchStrategy):
    def __init__(self):
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
        keyword_tk = np.array(list(word_tokenize(keyword)))
        kw_vec = ccn_embeddings.get_word_vectors(keyword_tk)

        def compute_similarity() -> np.ndarray:
            reserved_tokens = np.zeros((keyword_tk.size, 1))
            exact = pairwise_equal(keyword_tk, self._all_words)
            cosine = pairwise_cosine_similarity(kw_vec, self._words_vec)
            concat = np.where(exact, 1, cosine)
            return np.hstack((reserved_tokens, concat))

        similarity = compute_similarity()

        verses_in_range = (
            self._tokenized_verses[in_range]
            if in_range is not None
            else self._tokenized_verses
        )
        # there are two parts of score: cosine similarity and count of good keywords
        all_match_scores = similarity[:, verses_in_range]
        kw_verse_scores = np.amax(all_match_scores, axis=2)
        verse_scores = np.core.records.fromarrays(
            [
                kw_verse_scores.sum(axis=0),
                np.where(kw_verse_scores >= 0.5, 1, 0).sum(axis=0),
            ],
            names="total,good_kw_counts",
        )
        top_matches = np.argsort(verse_scores, order=["good_kw_counts", "total"])[
            -1 : -top_k - 1 : -1
        ]

        def create_match(index: int) -> Match:
            tokens = verses_in_range[index]
            kw_scores = []
            for kw in range(len(keyword_tk)):
                scores = similarity[kw, tokens]
                match_word = np.argmax(scores)
                match_token = tokens[match_word]
                kw_scores.append((self._detokenize(match_token), scores[match_word]))
            return Match(in_range[index] if in_range is not None else index, kw_scores)

        return [create_match(i) for i in top_matches]

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


# to reduce load time of Sci-Kit Learn, cosine similarity calculation was implemented
# the result should be the same as using `sklearn.metrics.pairwise.cosine_similarity()`
def pairwise_cosine_similarity(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    return np.dot(normalize(X), normalize(Y).T)


def normalize(X: np.ndarray) -> np.ndarray:
    X = X.astype(float)
    l2_norms = np.einsum("ij,ij->i", X, X)
    np.sqrt(l2_norms, l2_norms)
    l2_norms[l2_norms == 0.0] = 1.0
    X /= l2_norms[:, np.newaxis]
    return X
