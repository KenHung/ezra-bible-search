import os
from abc import ABC, abstractmethod
from typing import Iterable, List, Tuple

import pandas as pd

from .lang import to_simplified
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

    def to_dict(self) -> dict:
        return {
            'verse': self.verse,
            'score': self.score(),
            'kw_scores': {kw: score for kw, score in self.kw_scores}
        }

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
    def __init__(self, strategy: BibleSearchStrategy):
        self.strategy = strategy

    def search(self, keyword: str, zh_cn: bool, top_k: int = 10,
               verbose: bool = False) -> List[Match]:
        """
        Search for verses that match the keyword
        """
        if not zh_cn:
            keyword = to_simplified(keyword)
        results = self.strategy.search(keyword, top_k)

        for match in results:
            bible_text = bible.text[match.index]
            if zh_cn:
                match.verse = to_simplified(bible_text)
                match.kw_scores = [(to_simplified(kw), score)
                                   for kw, score in match.kw_scores]
            else:
                match.verse = bible_text

        if verbose:
            print(f'Searches for {keyword}:')
            for match in results:
                print(f'Score: {match.score():.2f} {match.verse_hightlight()}')
            print()
        return results