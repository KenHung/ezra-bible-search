import itertools

import nltk
from nltk.corpus import wordnet as wn


def sentence_similarity(keywords, sentence):
    keywords = remove_stopwords(keywords)
    sentence = remove_stopwords(sentence)
    keywords_similarity = (max(similarity(kw, token)
                               for token in sentence) for kw in keywords)
    return sum(keywords_similarity) / len(keywords)


def remove_stopwords(tokens):
    return [(word, pos) for word, pos in tokens if pos != 'x' and word not in '。，；⋯⋯、']


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


def map_pos(pos: str) -> str:
    wn_pos = {
        'n': wn.NOUN,
        'v': wn.VERB,
        'a': wn.ADJ,
        'd': wn.ADV
    }
    return wn_pos.get(pos[0]) or pos
