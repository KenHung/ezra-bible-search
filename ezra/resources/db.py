import atexit
from importlib import resources
from typing import Iterable

import numpy as np
import tables

from ..lang import to_simplified
from . import abbr


class Bible:
    def __init__(self, db: tables.File):
        self._unv = db.root.unv.table
        self._book = db.root.unv.meta.book.meta.table
        self.idx = np.arange(self._unv.nrows)

    def get_record(self, index: int):
        _, (chap, vers), book_index, text = self._unv[index]
        _, book = self._book[book_index]
        return {
            "book": book.decode(),
            "chap": int(chap),
            "vers": int(vers),
        }, text.decode()

    def exact_match(self, keyword: str) -> np.ndarray:
        cond = "&".join("contains(text, %r)" % kw.encode() for kw in keyword.split())
        return self._unv.read_where(cond, field="index")

    def book_idx(self, in_book: str) -> np.ndarray:
        books = np.char.encode(abbr.ranges.get(in_book, [in_book]))
        all_books = self._book.read(field="values")
        book_indices = np.argwhere(np.isin(all_books, books))
        book_col = self._unv.read(field="book")
        return np.argwhere(np.isin(book_col, book_indices))


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
    atexit.register(_db.close)
    bible = Bible(_db)
    ccn_embeddings = ConceptNetEmbeddings(_db)
