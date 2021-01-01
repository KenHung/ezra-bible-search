"""Get phases got cut accidentally in tokenization."""
import sys
sys.path.append('..')

import jieba
import jieba.posseg as pseg
import pandas as pd
from data import read_bible
from hanziconv import HanziConv
from tqdm import tqdm


unv = read_bible('../data/dnstrunv.tgz')
unv['text_s'] = unv.text.apply(HanziConv.toSimplified)

jieba.load_userdict('bible_terms.txt')
tokenized = unv.text_s.apply(pseg.lcut)

conceptnet_vocabs = pd.read_hdf('mini.h5').index
chinese_vocabs = conceptnet_vocabs[
    conceptnet_vocabs.str.startswith('/c/zh')].str.replace('/c/zh/', '')

with open('phases_got_cut.txt', 'w') as phases_got_cut:
    for vocab in tqdm(chinese_vocabs):
        for verse_tokens in tokenized:
            for n in range(len(verse_tokens) - 1):
                possible_phase = verse_tokens[n].word + verse_tokens[n + 1].word
                if vocab == possible_phase:
                    phases_got_cut.write(vocab)
                    phases_got_cut.write('\n')
                    phases_got_cut.flush()
