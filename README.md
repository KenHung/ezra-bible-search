# Ezra 聖經語意搜尋 - Semantic Search Engine for Chinese Bible

應用語意搜尋技術的聖經經文搜尋器，通過新型的自然語言處理技術，了解字詞的意思來進行搜尋。即使經文內詞彙的字眼不一樣，只要意思相近，也有機會被搜尋出來。

Semantic search engine for Chinese Bible, applying state-of-the-art natural
language processing techniques, which is able to search for relevant biblical text
by the meaning of search keywords.

## 安裝

系統需求：

* [Python 3.8](https://www.python.org/downloads/) 或以上（較低版本或許也可以，但沒有詳細測試）

安裝步驟：

1. 安裝所需要的 Python packages

   ```sh
   pip install -r requirements.txt
   ```

2. 下載所需的原始數據，放到 `/data` 中。
   * [信望愛和合本](https://bible.fhl.net/public/dnstrunv.tgz)
   * [ConceptNet Numberbatch 詞向量](http://conceptnet.s3.amazonaws.com/precomputed-data/2016/numberbatch/19.08/mini.h5)

   也可以使用 `make` 下載所需檔案，如果沒有 `make`，就需要手動下載到 `/data` 中。

   ```sh
   make data
   ```

3. 預備運行需用的數據檔案，`db.h5` 內含是經文和詞向量數據。  
   `conceptnet_strategy.pickle` 是一些預先計算的數據，作用是減低程序初始化時間。  
   製作數據檔案時需要 `pandas` 但運行程序時就不需要。

   ```sh
   pip install pandas
   ```

   可以用 `make` 製作數據檔。沒有 `make` 的話，可以手動執行 `Makefile` 內相關的指令。

   ```sh
   make ezra/resources/db.h5
   make ezra/resources/conceptnet_strategy.pickle
   ```

## 用法

一般開發可以使用 `flask`：
```
FLASK_APP=ezra FLASK_ENV=development flask run --without-threads
```

伺服器上使用可以使用 `gunicorn`，目前不支援 multiprocessing/multithreading：
```
gunicorn main:app --workers 1 --threads 1
```

## 數據來源

和合本經文、人名和地名資料來自「信望愛信仰與聖經資源中心」：https://bible.fhl.net/public 。

語意模型採用了 [ConceptNet Numberbatch](https://github.com/commonsense/conceptnet-numberbatch)
 的中文詞彙部分，由 [Luminoso Technologies, Inc.](https://www.luminoso.com/) 以
 [CC-By-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 條款授權。

## 版權相關

項目以 [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0) 條款授權，
基本上是自由使用、分發和修改，但修改後發佈的話煩請列明改動。

--------------------------------------------------

Ezra 聖經語意搜尋，應用語意模型的聖經經文搜尋器。  
Copyright (C) 2021 Ken Hung

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

--------------------------------------------------

This work includes data from ConceptNet 5, which was compiled by the
Commonsense Computing Initiative. ConceptNet 5 is freely available under
the Creative Commons Attribution-ShareAlike license (CC-By-SA 4.0) from
http://conceptnet.io.

The included data was created by contributors to Commonsense Computing
projects, contributors to Wikimedia projects, Games with a Purpose,
Princeton University's WordNet, DBPedia, Unicode, Jim Breen, MDBG, and
Cycorp's OpenCyc.
