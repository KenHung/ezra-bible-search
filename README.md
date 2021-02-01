# Ezra 聖經經文搜尋

應用自然語言處理技術的聖經經文搜尋器。

## 背景

傳統的經文搜尋均需要搜尋關鍵字和經文完全一樣才能找到經文，也稱作 Exact Match。
Ezra 經文搜尋就想做 Fuzzy Match 的效果，就是關鍵字和經文有少量不同，也能處理。

## 數據來源

和合本經文、人名和地名資料來自「信望愛信仰與聖經資源中心」，https://bible.fhl.net/public 。

在文字配對方面，主要使用了 ConceptNet Numberbatch 的中文詞彙數據。

## 版權相關

項目以 [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0) 發佈，基本上是自由使用、
分發和修改，但修改後發佈的話煩請列明改動。

由於 ConceptNet 使用 [CC BY SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) 
發佈，發佈修改了的版本時請表明出處。你可以表明使用了 Ezra 經文搜尋或只表明 ConceptNet 也可，
因為我不介意你表明使用了 Ezra 與否。

--------------------------------------------------

Ezra 聖經經文搜尋，應用自然語言處理技術的經文搜尋器。  
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
the Creative Commons Attribution-ShareAlike license (CC BY SA 3.0) from
http://conceptnet.io.

The included data was created by contributors to Commonsense Computing
projects, contributors to Wikimedia projects, DBPedia, OpenCyc, Games
with a Purpose, Princeton University's WordNet, Francis Bond's Open
Multilingual WordNet, and Jim Breen's JMDict.
