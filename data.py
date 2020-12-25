import numpy as np
import pandas as pd

types = {
    'book': 'string',
    'chap': np.int32,
    'vers': np.int32,
    'text': 'string'
}


def read_bible(path: str) -> pd.DataFrame:
    data = pd.read_csv(
        path,
        compression='gzip',
        sep='#',
        header=None,
        usecols=[1, 2, 3, 4],
        names=list(types.keys()))

    data.dropna(inplace=True)
    data = data.astype(types)
    data.sort_values(['book', 'chap', 'vers'], inplace=True)

    assert len(data.book.unique()) == 66
    assert data.groupby('book').chap.unique().apply(in_order).all()
    vers_by_book_chap = data.groupby(['book', 'chap']).vers
    assert vers_by_book_chap.apply(in_order).all()
    assert vers_by_book_chap.max().sum() == len(data) == 31103

    return data


def in_order(nums: np.ndarray):
    return np.array_equal(nums, range(1, nums.max() + 1))
