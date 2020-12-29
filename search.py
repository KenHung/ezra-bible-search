import itertools
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import nltk
from nltk.corpus import wordnet as wn


def sentence_similarity(keywords_tokens, sentence_tokens):
    keywords = [tk.word for tk in remove_stopwords(keywords_tokens)]
    sentence_tokens = remove_stopwords(sentence_tokens)
    kw_score = {}
    for kw in keywords:
        word_score = {tk.word: similarity(kw, tk) for tk in sentence_tokens}
        if word_score:
            match_word = max(word_score, key=word_score.get)
            kw_score[match_word] = word_score[match_word]
        else:
            kw_score[''] = 0
    return kw_score


def remove_stopwords(tokens) -> list:
    return [tk for tk in tokens if tk.flag != 'x']


def similarity(token_a, token_b) -> float:
    word_a, pos_a = map_pos(token_a)
    word_b, pos_b = map_pos(token_b)

    if word_a == word_b:
        return 1

    ss_a = get_synsets(word_a, pos_a)
    ss_b = get_synsets(word_b, pos_b)
    if ss_a and ss_b:
        sims = map(lambda p: wn.path_similarity(*p) or 0,
                   itertools.product(ss_a, ss_b))
    elif ss_a:
        lemmas = (syn.lemma_names(lang='cmn') for syn in ss_a)
        sims = [(1 if word_b == lemma else 0) for lemma in lemmas]
    elif ss_b:
        lemmas = (syn.lemma_names(lang='cmn') for syn in ss_b)
        sims = [(1 if word_a == lemma else 0) for lemma in lemmas]
    else:
        sims = [0]
    return max(sims)


def get_synsets(word, pos):
    ss = wn.synsets(word, pos=pos, lang='cmn')
    if not ss:
        ccn_words = _conceptnet_terms.get(word)
        if ccn_words:
            all_ss = (wn.synsets(ccn_word, pos=pos) for ccn_word in ccn_words)
            ss = set(itertools.chain(*all_ss))
    return ss


def map_pos(token) -> Tuple[str, Optional[str]]:
    if type(token) is str:
        return token, None
    else:
        wn_pos = {
            'n': wn.NOUN,
            'v': wn.VERB,
            'a': wn.ADJ,
            'd': wn.ADV
        }
        pos = wn_pos.get(token.flag[0], token.flag)
        return token.word, pos


_conceptnet_terms: Dict[str, List[str]] = {}


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
