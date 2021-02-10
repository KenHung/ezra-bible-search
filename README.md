# Ezra 聖經語意搜尋

應用語意模型的聖經經文搜尋器。

## 背景

傳統的經文搜尋均需要搜尋關鍵字和經文完全一樣才能找到經文，所以，字詞相似的經文就被忽略。
Ezra 就使用語意搜尋的技術，通過了解字詞的意思來進行搜尋，所以搜尋的結果會出現近義詞。

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
