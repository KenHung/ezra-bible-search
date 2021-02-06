from importlib import resources
from typing import Iterable

import numpy as np
import tables

from ..lang import to_simplified


class Bible:
    def __init__(self, db: tables.File):
        self._unv = db.root.unv.table

    def get_record(self, index: int):
        record = self._unv[index]
        _, (chap, vers), (book, text) = record
        return {
            "book": book.decode(),
            "chap": int(chap),
            "vers": int(vers),
        }, text.decode()


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
