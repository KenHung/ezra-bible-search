import numpy as np
import pandas as pd


def read_bible(path: str) -> pd.DataFrame:
    types = {
        'book': 'string',
        'chap': np.int32,
        'vers': np.int32,
        'text': 'string'
    }
    data = pd.read_csv(
        path,
        compression='gzip',
        sep='#',
        header=None,
        usecols=[1, 2, 3, 4],
        names=list(types.keys())
    )
    data.dropna(inplace=True)
    data = data.astype(types)
    data.sort_values(['book', 'chap', 'vers'], inplace=True)

    assert len(data.book.unique()) == 66
    assert data.groupby('book').chap.unique().apply(in_order).all()
    vers_by_book_chap = data.groupby(['book', 'chap']).vers
    assert vers_by_book_chap.apply(in_order).all()
    assert vers_by_book_chap.max().sum() == len(data) == 31103

    return data


def read_cbol_dict(path: str) -> pd.DataFrame:
    types = {
        'strong': np.int32,
        'defs': 'string'
    }
    data = pd.read_csv(
        path,
        sep='^',
        names=list(types.keys()),
        usecols=[0, 1],
        dtype=types
    )
    return data


def extract_term(defs: pd.Series) -> pd.Series:
    term = defs\
        .str.extract('n([^n]*?) ?=', expand=False)\
        .str.replace('\(.*\)', '')\
        .str.replace('[帶冠詞]', 'X')\
        .str.replace(' 參看 04182 ', ' ')\
        .str.replace('[或,•‧\-、，="（）族人的]', ' ')
    term = term.mask(term.notna() & term.str.contains('[a-zA-Z\)]'))
    return term.str.split()


def in_order(nums: np.ndarray):
    return np.array_equal(nums, range(1, nums.max() + 1))
