import re
from typing import List

import numpy as np
import pandas as pd
from opencc import OpenCC

from word_embeddings import word_tokenize


def read_bible(path: str) -> pd.DataFrame:
    types = {
        'index': np.int32,
        'book': 'string',
        'chap': np.int32,
        'vers': np.int32,
        'text': 'string'
    }
    data = pd.read_csv(
        path,
        sep='#',
        header=None,
        index_col=0,
        usecols=[0, 1, 2, 3, 4],
        names=list(types.keys()),
        dtype=types
    )
    data.sort_values('index', inplace=True)
    data.reset_index(drop=True, inplace=True)

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


def find_pos(def_lines: List[str]) -> str:
    for line in def_lines:
        match = re.search(';\s*(\S*(?:詞|地名))', line)
        if match:
            return match.group(1)
    return None


def jieba_pos(defs: str) -> str:
    people_keywords = ['人名', '父親', '兒子', '後裔', '一位', '一名', '家族', '的人']
    if '地名' in defs:
        return 'ns'
    elif any(kw in defs for kw in people_keywords):
        return 'nr'
    elif '動詞' in defs:
        return 'v'
    elif '形容詞' in defs:
        return 'a'
    elif '副詞' in defs:
        return 'd'
    else:
        return 'nz'


def create_name_dict(cbol_dict: pd.DataFrame) -> pd.DataFrame:
    # extract vocabs from 'XXX = "XXX"' pattern
    vocabs_eq = extract_vocabs(cbol_dict.def_lines)

    # extract vocabs from the following pattern:
    # [vocab]
    # 1) [definition]
    missing = cbol_dict.defs.str.contains(
        '(?:專有|人名|地名)') & ~cbol_dict.defs.str.contains('=')
    names_over_def = cbol_dict[missing].def_lines.transform(find_name_over_def)
    vocabs_over_def = extract_vocabs(names_over_def, r'([^ ：＝的是]*)[ ：＝的]?(.*)')

    # extract left over vocabs manually
    left_over = cbol_dict[missing][names_over_def.isna()]
    left_over_lines = left_over.def_lines.explode()
    left_over_names = ['拉伯撒利 或 拉撒利', '馬利', '古厄', '利乏音', '阿拉伯', '罷特', '何賽', '伊基拉', '撒但',
                       '亞利伊勒', '亞罷拿河', '以得臺', '施恩座', '石獾', '哈基多琳', '賽耳底', '撒旦', '以土買', '亞比烏市', '奮銳黨']
    left_over_vocabs = extract_vocabs(left_over.def_lines,
                                      f'({"|".join(left_over_names)})').drop_duplicates()

    all_vocabs = pd.concat([vocabs_eq, vocabs_over_def, left_over_vocabs])
    vocabs = all_vocabs.merge(cbol_dict[['strong', 'pos', 'jieba_pos']],
                              left_index=True, right_index=True)
    vocabs['name'] = clean_vocab_names(vocabs[0])
    invalid = vocabs.name.str.contains(r'[\(\)a-z]')
    return vocabs[~invalid][['strong', 'name', 1, 'pos', 'jieba_pos']]


def extract_vocabs(cbol_def_lines: pd.Series, pattern: str = r'(.*?)=(.*)') -> pd.DataFrame:
    vocab_defs = cbol_def_lines.explode()\
                               .str.extract(pattern)\
                               .dropna()
    return vocab_defs


def clean_vocab_names(names: pd.Series) -> pd.Series:
    return names.str.replace(r'\(.*\)', '')\
                .str.replace(r'（.*）', '')\
                .str.replace(r'\[.*\]', '')\
                .str.replace('參看 04182 摩利設迦特', '')\
                .str.replace(r'[ "]', '')\
                .str.replace(r'[•‧．・\-]', '・')


def find_name_over_def(lines):
    first_def = next((n for n, line in enumerate(lines)
                      if line.startswith('1)')), None)
    term = lines[first_def - 1] if first_def else np.nan
    return term if term and '詞' not in term else np.nan


def in_order(nums: np.ndarray):
    return np.array_equal(nums, range(1, nums.max() + 1))


if __name__ == "__main__":
    unv = read_bible('data/dnstrunv')
    dots = r'[•‧．・\-]'
    t2s = OpenCC('t2s.json')
    verses_s = unv.text.apply(t2s.convert)\
                       .str.replace(dots, '')
    tokenized = verses_s.apply(lambda v: ' '.join(word_tokenize(v)))
    tokenized.to_csv('word_embeddings/word_tokenized_verses.txt',
                     index=False, header=None)
