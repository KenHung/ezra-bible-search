import os
from abc import ABC, abstractmethod
from typing import List, Tuple

import pandas as pd

from build_data import read_bible


class BibleSearchEngine:
    def __init__(self, strategy=None, bible_path: str = None):
        if bible_path is None:
            file_dir = os.path.dirname(__file__)
            bible_path = os.path.join(file_dir, 'data/dnstrunv')
        self.bible = read_bible(bible_path)
        self.strategy = strategy

    def search(self, keyword: str, top_k: int = 10,
               verbose: bool = False) -> List[Tuple[str, float]]:
        """
        Search for verses that match the keyword
        """
        results = self.strategy.search(keyword, top_k)
        verse_results = [(self.bible.text[index], score)
                         for index, score in results]
        if verbose:
            print(f'Searches for {keyword}:')
            for verse, score in verse_results:
                print(f'Score: {score:7.4f} {verse}')
            print()
        return verse_results


class BibleSearchStrategy(ABC):
    @abstractmethod
    def search(self, keyword: str, top_k: int) -> List[Tuple[int, float]]:
        return NotImplemented
