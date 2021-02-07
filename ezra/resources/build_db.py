import sys

import pandas as pd
from ezra.resources import bible


def create_zh_table(conceptnet_h5: str, db_file):
    full = pd.read_hdf(conceptnet_h5)
    zh = full.index.str.startswith("/c/zh")
    full[zh].to_hdf(db_file, "zh", format="table")


def create_unv_table(db_file):
    bible.df.to_hdf(db_file, "unv", format="table", data_columns=["book", "text"])


if __name__ == "__main__":
    path = sys.argv[1]
    with pd.HDFStore(path, mode="w") as db_file:
        create_zh_table("data/mini.h5", db_file)
        create_unv_table(db_file)
