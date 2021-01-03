import numpy as np
import pandas as pd
from hanziconv import HanziConv

from word_embeddings import tokenize


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
        'strong': 'string',
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
        .str.replace('（.*）', '')\
        .str.replace('[帶冠詞]', '', regex=False)\
        .str.replace(' 參看 04182 ', ' ')
    return term.mask(term.str.contains('[a-zA-Z\)\(]'))


def in_order(nums: np.ndarray):
    return np.array_equal(nums, range(1, nums.max() + 1))


if __name__ == "__main__":
    unv = read_bible('data/dnstrunv.tgz')
    verses_s = unv.text.apply(HanziConv.toSimplified)
    tokenized = verses_s.apply(
        lambda v: ' '.join(tokenize(v, remove_punctuation=False)))
    tokenized.to_csv('data/tokenized_verses.txt', index=False, header=None)
