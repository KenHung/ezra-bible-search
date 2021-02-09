from importlib import resources

import numpy as np
import pandas as pd


def in_order(nums: np.array):
    return np.array_equal(nums, range(1, nums.max() + 1))


def read_bible(bible_file) -> pd.DataFrame:
    types = {
        "index": np.int16,
        "book": str,
        "chap": np.uint8,
        "vers": np.uint8,
        "text": str,
    }
    bible = pd.read_table(
        bible_file,
        sep="#",
        header=None,
        index_col=0,
        usecols=[0, 1, 2, 3, 4],
        names=list(types.keys()),
        dtype=types,
    )
    bible["book"] = bible.book.str.replace(" ", "").str.lower().astype("category")
    bible.sort_values("index", inplace=True)
    bible.reset_index(drop=True, inplace=True)

    assert len(bible.book.unique()) == 66
    assert bible.groupby("book").chap.unique().apply(in_order).all()
    vers_by_book_chap = bible.groupby(["book", "chap"]).vers
    assert vers_by_book_chap.apply(in_order).all()
    assert vers_by_book_chap.max().sum() == len(bible) == 31103

    return bible


with resources.path(__package__, "fhl_unv.dsv") as f:
    df: pd.DataFrame = read_bible(f)
    text: pd.Series = df.text
