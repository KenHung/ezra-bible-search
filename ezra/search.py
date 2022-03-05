from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np

from .lang import to_simplified


class Match:
    def __init__(self, index: int, kw_scores: List[Tuple[str, float]]):
        self.index = index
        self.kw_scores = kw_scores
        self.verse = ""
        self.ref = None

    def verse_hightlight(self) -> str:
        return self._highlight_occurrences(self.verse)

    def score(self) -> float:
        return sum(sc for _, sc in self.kw_scores)

    def to_dict(self) -> dict:
        return {
            "text": self.verse,
            "ref": self.ref,
            "score": self.score(),
            "kw_scores": dict(self.kw_scores),
        }

    def _highlight_occurrences(self, text: str) -> str:
        for i, kw in enumerate(self.kw_scores):
            text = text.replace(kw[0], self._highlight(f"{kw[0]}({kw[1]:.2f})", i))
        return text

    def _highlight(self, text: str, color_code: int) -> str:
        return f"\x1b[6;30;4{color_code + 1}m{text}\x1b[0m"


class BibleSearchStrategy(ABC):
    @abstractmethod
    def search(self, keyword: str, top_k: int, range: np.ndarray = None) -> List[Match]:
        return NotImplemented

    @abstractmethod
    def related_keywords(self, keyword: str, top_k: int) -> List[str]:
        return NotImplemented


class BibleSearchEngine:
    def __init__(self, strategy: BibleSearchStrategy):
        self.strategy = strategy

    def search(
        self,
        keyword: str,
        zh_cn: bool = False,
        in_book: str = None,
        top_k: int = 10,
        verbose: bool = False,
    ) -> List[Match]:
        """
        Search for verses that match the keyword
        """
        from .resources.db import bible

        exact_idx = bible.exact_match(keyword)
        if not in_book:
            search_range = (
                np.setdiff1d(bible.idx, exact_idx) if len(exact_idx) > 0 else None
            )
        else:
            book_range = bible.book_idx(in_book)
            exact_idx = np.intersect1d(exact_idx, book_range)
            search_range = np.setdiff1d(book_range, exact_idx)
        kw_scores_exact = [(kw, 1.0) for kw in keyword.split()]
        exact_matches = [Match(index, kw_scores_exact) for index in exact_idx]
        if len(exact_idx) < top_k:
            fuzzy_matches = self.strategy.search(
                keyword, top_k - len(exact_idx), search_range
            )
            results = exact_matches + fuzzy_matches
        else:
            results = exact_matches[:top_k]

        for match in results:
            match.ref, bible_text = bible.get_record(match.index)
            if zh_cn:
                match.verse = to_simplified(bible_text)
                match.kw_scores = [
                    (to_simplified(kw), score) for kw, score in match.kw_scores
                ]
            else:
                match.verse = bible_text

        if verbose:
            print(f"Searches for {keyword}:")
            for match in results:
                print(f"Score: {match.score():.2f} {match.verse_hightlight()}")
            print()
        return results

    def related_keywords(self, keyword: str, top_k: int = 5) -> List[str]:
        return self.strategy.related_keywords(keyword, top_k)
