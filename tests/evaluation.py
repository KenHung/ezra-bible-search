"""Batch execute search for evaluation."""
from contextlib import redirect_stdout
from itertools import combinations

from ezra import BibleSearchEngine
from ezra.conceptnet_strategy import ConceptNetStrategy
from tqdm import tqdm

strategy = ConceptNetStrategy.from_pickle()

ezra_engine = BibleSearchEngine(strategy)
keywords = open("word_tokens.txt").read().splitlines()
kw_pairs = list(combinations(keywords, 2))

with open("evaluation.ans", "w") as outfile:
    with redirect_stdout(outfile):
        for kw1, kw2 in tqdm(kw_pairs):
            try:
                ezra_engine.search(f"{kw1} {kw2}", top_k=5, verbose=True)
            except Exception as ex:
                if type(ex) is KeyboardInterrupt:
                    raise ex
                print(f"Error: {kw1} {kw2}")
                print()
