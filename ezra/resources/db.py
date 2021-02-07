from importlib import resources
from typing import Iterable

import numpy as np
import tables

from ..lang import to_simplified


class Bible:
    def __init__(self, db: tables.File):
        self._unv = db.root.unv.table
        self._book = db.root.unv.meta.book.meta.table

    def get_record(self, index: int):
        _, (chap, vers), book_index, text = self._unv[index]
        _, book = self._book[book_index]
        return {
            "book": book.decode(),
            "chap": int(chap),
            "vers": int(vers),
        }, text.decode()

    def exact_match(self, keyword: str) -> np.ndarray:
        cond = "&".join(["contains(text, %r)" % kw.encode() for kw in keyword.split()])
        return self._unv.read_where(cond, field="index")

    def book_ranges(self, in_book: str) -> np.ndarray:
        book_index = self._book.read_where("values == in_book")  # noqa: F841
        return self._unv.read_where("book == book_index", field="index")


class ConceptNetEmbeddings:
    def __init__(self, db: tables.File):
        self._emb = db.root.zh.table

    def get_word_vectors(self, words: Iterable[str]) -> np.ndarray:
        vectors = list(map(self.get_word_vector, words))
        return np.vstack(vectors)

    def get_word_vector(self, word: str) -> np.ndarray:
        key = f"/c/zh/{to_simplified(word)}".encode()  # noqa: F841
        records = self._emb.read_where("index == key")
        if len(records) > 0:
            word, vector = records[0]
            return vector
        else:
            return np.zeros(300, "i1")


with resources.path(__package__, "db.h5") as h5_path:
    _db = tables.open_file(h5_path)
    bible = Bible(_db)
    ccn_embeddings = ConceptNetEmbeddings(_db)
