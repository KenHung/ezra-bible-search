import sys

from hanziconv import HanziConv
from sklearn.model_selection import train_test_split

sys.path.append('..')

from build_data import read_bible


def save_data(data, out_file):
    text_s = data.text.apply(HanziConv.toSimplified)
    data.text.append(text_s).to_csv(
        f'../data/{out_file}.txt', header=None, index=False)


unv = read_bible('../data/dnstrunv')
unv = unv[unv.text.str.len() > 4]
train, test = train_test_split(unv, test_size=0.1, random_state=0,
                               stratify=unv.book + unv.chap.astype(str))
save_data(train, 'unv_train')
save_data(test, 'unv_test')
