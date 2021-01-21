import os
from abc import ABC, abstractmethod
from typing import Iterable, List, Tuple

import pandas as pd
from opencc import OpenCC

from .resources import bible


class Match:
    def __init__(self, index: int, kw_scores: List[Tuple[str, float]]):
        self.index = index
        self.kw_scores = kw_scores
        self.verse = ''

    def verse_hightlight(self) -> str:
        return self._highlight_occurrences(self.verse)

    def score(self) -> float:
        return sum(sc for _, sc in self.kw_scores)

    def _highlight_occurrences(self, text: str) -> str:
        for i, kw in enumerate(self.kw_scores):
            text = text.replace(kw[0],
                                self._highlight(f'{kw[0]}({kw[1]:.2f})', i))
        return text

    def _highlight(self, text: str, color_code: int) -> str:
        return f'\x1b[6;30;4{color_code + 1}m{text}\x1b[0m'


class BibleSearchStrategy(ABC):
    @abstractmethod
    def search(self, keyword: str, top_k: int) -> List[Match]:
        return NotImplemented


class BibleSearchEngine:
    def __init__(self, strategy: BibleSearchStrategy, bible_path: str = None):
        if bible_path is None:
            file_dir = os.path.dirname(__file__)
            bible_path = os.path.join(file_dir, 'data/dnstrunv')
        self.strategy = strategy
        self._t2s = OpenCC('t2s.json')

    def search(self, keyword: str, zh_cn: bool, top_k: int = 10,
               verbose: bool = False) -> List[Match]:
        """
        Search for verses that match the keyword
        """
        if not zh_cn:
            keyword = self._t2s.convert(keyword)
        results = self.strategy.search(keyword, top_k)

        for match in results:
            bible_text = bible.text[match.index]
            if zh_cn:
                match.verse = self._t2s.convert(bible_text)
                match.kw_scores = [(self._t2s.convert(kw), score)
                                   for kw, score in match.kw_scores]
            else:
                match.verse = bible_text

        if verbose:
            print(f'Searches for {keyword}:')
            for match in results:
                print(f'Score: {match.score():.2f} {match.verse_hightlight()}')
            print()
        return results
