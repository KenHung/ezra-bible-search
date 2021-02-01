import pickle
from importlib import resources
from typing import List

import numpy as np

from .resources import bible, ccn_embeddings
from .search import BibleSearchStrategy, Match
from .word_tokenizer import word_tokenize


class ConceptNetStrategy(BibleSearchStrategy):
    def __init__(self):
        print("Word tokenizing verses...")
        dots = r'[•‧．・\-]'
        verses = bible.text.str.replace(dots, '', regex=True)
        word_tokenized_verses = verses.transform(
            lambda v: list(word_tokenize(v)))

        print("Getting word vectors...")
        all_words = np.unique(
            [word for verse in word_tokenized_verses for word in verse])
        self._words_vec, self._words_no_vec = ccn_embeddings.get_word_vectors(
            all_words)

        print("Tokenizing verses...")
        tokenized_verses = [list(set(map(self._tokenize, verse)))
                            for verse in word_tokenized_verses]
        max_length = max(map(len, tokenized_verses))
        self._tokenized_verses = np.array([v + [0]*(max_length-len(v))
                                           for v in tokenized_verses])

    def to_pickle(self):
        with open('conceptnet_strategy.pickle', 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def from_pickle(cls):
        with resources.open_binary('ezra.resources', 'conceptnet_strategy.pickle') as f:
            return pickle.load(f)

    def search(self, keyword: str, top_k: int) -> List[Match]:
        keyword_tk = np.array(list(word_tokenize(keyword)))
        kw_vec, kw_no_vec = ccn_embeddings.get_word_vectors(keyword_tk)

        def compute_similarity() -> np.ndarray:
            reserved_tokens = np.zeros((keyword_tk.size, 1))
            in_vocab = pairwise_consine_similarity(kw_vec, self._words_vec)
            if len(kw_no_vec) > 0:
                kw_oov = self._similarity_oov(kw_no_vec, self._words_vec.index)
                all_kw = np.vstack((in_vocab,  kw_oov))
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
        except IndexError:
            index -= len(self._words_vec)
            return self._words_no_vec[index]


# to reduce load time of Sci-Kit Learn, consine similarity calculation was implemented
# the result should be the same as using `sklearn.metrics.pairwise.cosine_similarity()`
def pairwise_consine_similarity(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    return np.dot(normalize(X),
                  normalize(Y).T)


def normalize(X: np.ndarray) -> np.ndarray:
    X = X.astype(float)
    l2_norms = np.einsum('ij,ij->i', X, X)
    np.sqrt(l2_norms, l2_norms)
    l2_norms[l2_norms == 0.0] = 1.0
    X /= l2_norms[:, np.newaxis]
    return X
