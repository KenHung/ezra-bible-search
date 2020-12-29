import itertools
import json
import os
from pathlib import Path
from typing import List

import nltk
from nltk.corpus import wordnet as wn


def sentence_similarity(keywords_tokens, sentence_tokens):
    keywords_tokens = remove_stopwords(keywords_tokens)
    sentence_tokens = remove_stopwords(sentence_tokens)
    kw_score = {}
    for kw_tk in keywords_tokens:
        word_score = {word: similarity(kw_tk, (word, pos))
                      for word, pos in sentence_tokens}
        match_word = max(word_score, key=word_score.get)
        kw_score[match_word] = word_score[match_word]
    return kw_score


def remove_stopwords(tokens):
    return [(word, pos) for word, pos in tokens if word not in '。，；⋯⋯、 ']


def similarity(token_a, token_b) -> float:
    word_a, pos_a = token_a
    if type(token_b) is str:
        word_b = token_b
        pos_b = None
    else:
        word_b, pos_b = token_b
    if word_a == word_b:
        return 1

    if pos_a:
        pos_a = map_pos(pos_a)
    if pos_b:
        pos_b = map_pos(pos_b)

    asyns = wn.synsets(word_a, pos=pos_a, lang='cmn')
    bsyns = wn.synsets(word_b, pos=pos_b, lang='cmn')
    if asyns and bsyns:
        sims = map(lambda p: wn.path_similarity(*p) or 0,
                   itertools.product(asyns, bsyns))
    elif asyns:
        lemmas = (syn.lemma_names(lang='cmn') for syn in asyns)
        sims = [(1 if word_b == lemma else 0) for lemma in lemmas]
    elif bsyns:
        lemmas = (syn.lemma_names(lang='cmn') for syn in bsyns)
        sims = [(1 if word_a == lemma else 0) for lemma in lemmas]
    else:
        sims = [0]
    return max(sims)


_conceptnet_terms = {}


def load_conceptnet_terms(in_dir: str) -> None:
    global _conceptnet_terms
    for word_file in Path(in_dir).iterdir():
        with open(word_file) as f:
            ccn_resp = json.load(f)
            en_labels = extract_en_labels(ccn_resp)
            if en_labels:
                _conceptnet_terms[word_file.stem] = en_labels


def extract_en_labels(ccn_resp: dict) -> List[str]:
    edges = ccn_resp.get('edges', [])
    return [node['end']['label'] for node in edges if node['end'].get('language') == 'en']


def map_pos(pos: str) -> str:
    wn_pos = {
        'n': wn.NOUN,
        'v': wn.VERB,
        'a': wn.ADJ,
        'd': wn.ADV
    }
    return wn_pos.get(pos[0]) or pos
