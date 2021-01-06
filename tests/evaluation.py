"""Batch execute search for evaluation."""
from contextlib import redirect_stdout
from itertools import combinations

from ezra import BibleSearchEngine
from hanziconv import HanziConv
from tqdm import tqdm
from word_embeddings.conceptnet_strategy import ConceptNetStrategy

strategy = ConceptNetStrategy()

ezra_engine = BibleSearchEngine(strategy)
keywords = open('keywords.txt').read().splitlines()
keywords_s = map(HanziConv.toSimplified, keywords)
kw_pairs = list(combinations(keywords_s, 2))

for kw1, kw2 in tqdm(kw_pairs):
    with open('evaluation.ans', 'a') as outfile:
        with redirect_stdout(outfile):
            try:
                ezra_engine.search(f'{kw1} {kw2}', top_k=5, verbose=True)
            except Exception as ex:
                if type(ex) is KeyboardInterrupt:
                    raise ex
                print(f'Error: {kw1} {kw2}')
                print()
