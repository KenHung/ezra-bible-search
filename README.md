# Ezra 聖經語意搜尋 - Semantic Search Engine for Chinese Bible

應用語意搜尋技術的聖經經文搜尋器，通過新型的自然語言處理技術，了解字詞的意思來進行搜尋。即使經文內詞彙的字眼不一樣，只要意思相近，也有機會被搜尋出來。

Semantic search engine for Chinese Bible, applying state-of-the-art natural
language processing techniques, which is able to search for relevant biblical text
by the meaning of search keywords.

搜尋「喜樂 事奉」的結果：
![Search example](example.png)

## 安裝

* 系統需求：[Python 3.8](https://www.python.org/downloads/) 或以上（較低版本或許也可以，但沒有詳細測試）
* 使用 `pip` 安裝：
```
pip install ezra-search
```
* 手動安裝：[詳細步驟](https://github.com/KenHung/ezra-bible-search/wiki/%E6%89%8B%E5%8B%95%E5%AE%89%E8%A3%9D%E6%AD%A5%E9%A9%9F)

## 用法

### Python module
```
>>> import ezra
>>> results = ezra.search("喜樂 事奉", top_k=3)
....
>>> for r in results:
...     print(r.to_dict())
... 
{'text': '所以，弟兄們，我以神的慈悲勸你們，將身體獻上，當作活祭，是聖潔的，是神所喜悅的；你們如此事奉乃是理所當然的。', 'ref': {'book': 'rom', 'chap': 12, 'vers': 1}, 'score': 1.7845185866114202, 'kw_scores': {'喜悅': 0.78451858661142, '事奉': 1.0}}
{'text': '「因為你富有的時候，不歡心樂意地事奉耶和華─你的神，', 'ref': {'book': 'deut', 'chap': 28, 'vers': 47}, 'score': 1.609989717447291, 'kw_scores': {'歡心': 0.609989717447291, '事奉': 1.0}}
{'text': '希該喜悅以斯帖，就恩待她，急忙給她需用的香品和她所當得的分，又派所當得的七個宮女服事她，使她和她的宮女搬入女院上好的房屋。', 'ref': {'book': 'esth', 'chap': 2, 'vers': 9}, 'score': 1.580993769747976, 'kw_scores': {'喜悅': 0.78451858661142, '服事': 0.7964751831365557}}
```

### Web App
自帶簡單的 Web 介面：
![UI](ui.png)

安裝後可以 `flask` 或 `gunicorn` 直接起動，但目前不支援 multiprocessing/multithreading
* `flask`
```
FLASK_APP=ezra flask run --without-threads
```
* `gunicorn`（需另行安裝）
```
gunicorn --workers=1 --threads=1 'ezra:create_app()'
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
