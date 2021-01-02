import jieba
import jieba.posseg as pseg
import pandas as pd
from data import read_bible
from hanziconv import HanziConv

unv = read_bible('../data/dnstrunv.tgz')
text_s = unv.text.apply(HanziConv.toSimplified)

jieba.load_userdict('bible_terms.txt')
tokenized_verses = text_s.apply(pseg.lcut)
tokenized_verses.apply(lambda l: ' '.join(tk.word for tk in l))\
                .to_csv('tokenized_verses.txt', index=False, header=None)
