from importlib import resources
from typing import Iterable, Tuple

import numpy as np
import pandas as pd

from ..lang import to_simplified


class ConceptNetEmbeddings:
    def __init__(self):
        with resources.path(__package__, "conceptnet.zh.h5") as h5_path:
            self._store: pd.DataFrame = pd.HDFStore(h5_path, mode="r")

    def get_word_vectors(self, words: Iterable[str]) -> Tuple[pd.DataFrame, np.array]:
        in_vocab = []
        word_vec_list = []
        out_of_vocab = []
        for word in words:
            vec = self.get_word_vector(word)
            if not vec.empty:
                in_vocab.append(word)
                word_vec_list.append(vec)
            else:
                out_of_vocab.append(word)

        word_vec = pd.concat(word_vec_list)
        word_vec.index = in_vocab
        return word_vec, np.array(out_of_vocab)

    def get_word_vector(self, word: str) -> pd.DataFrame:
        # TODO: OOV
        key = f"/c/zh/{to_simplified(word)}"
        return self._store.select("/zh", "index == key")


def create_zh_table(conceptnet_h5: str):
    full = pd.read_hdf(conceptnet_h5)
    zh = full.index.str.startswith("/c/zh")
    full[zh].to_hdf("conceptnet.zh.h5", "zh", format="table")
