from importlib import resources
from typing import Iterable

import numpy as np
import pandas as pd
import tables

from ..lang import to_simplified


class ConceptNetEmbeddings:
    def __init__(self):
        with resources.path(__package__, "conceptnet.zh.h5") as h5_path:
            h5f = tables.open_file(h5_path)
            self._tbl = h5f.root.zh.table

    def get_word_vectors(self, words: Iterable[str]) -> np.ndarray:
        vectors = list(map(self.get_word_vector, words))
        return np.vstack(vectors)

    def get_word_vector(self, word: str) -> np.ndarray:
        key = f"/c/zh/{to_simplified(word)}".encode()  # noqa: F841
        records = self._tbl.read_where("index == key")
        if len(records) > 0:
            word, vector = records[0]
            return vector
        else:
            return np.zeros(300, "i1")


def create_zh_table(conceptnet_h5: str):
    full = pd.read_hdf(conceptnet_h5)
    zh = full.index.str.startswith("/c/zh")
    full[zh].to_hdf("conceptnet.zh.h5", "zh", format="table")
