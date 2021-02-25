WeSAKE: Word Embeddings of Sake
====
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE.txt)
# About
- This tool enables **"sake operation"**
  - The terms of sake are represented by a vector in an Euclidean space
  - The sake embedding supports 14 categories (see [here](https://github.com/yoichi1484/sake_dataset)).
  - Change an attribute of the sake such as type of rice, yeast, and rice polishing rate
- e.g., "金鵄正宗_純米大吟醸_祝" - "山田錦" + "祝" = "松屋久兵衛"
- e.g., "金鵄正宗_純米大吟醸_祝" - "精米歩合45%" + "精米歩合60%" = "金鵄正宗_特別純米"

# Setup
- Download  **sake dataset** from [here](https://github.com/yoichi1484/sake_dataset)
```
$ cd data
$ git clone https://github.com/yoichi1484/sake_dataset
$ cp sake_dataset/json/sake_dataset_v1.json ./
```
# Usage
## Training sake embeddings with [gensim](https://radimrehurek.com/gensim/)
```
python train.py
```
## Analogy of sake vectors
```python
import utils
model = utils.load_sake_embedding()
result = model.most_similar(positive=['brand:英勲', 'rice:山田錦'], negative=['rice:祝'], topn=1)
result[0] # ('brand+name:美丈夫_大吟醸_薫', 0.465287983417511)
```
## Search sake data with queries
```python
import pprint
api = utils.SearchAPI()
results = api.and_search("brand+name:美丈夫_大吟醸_薫", "dgree_of_sweetness/dryness:-0.08", "rice_polishing_rate:40")
pprint.pprint(results[0], width=40)
{'alcohol_rate': {'max': '',
                  'mean': '',
                  'min': ''},
 'amino_acid_content': {'max': '',
                        'mean': '',
                        'min': ''},
 'brand': '美丈夫',
 'brand+name': '美丈夫 大吟醸 薫',
 'brewer': '濵川商店',
 'city': '安芸郡田野町',
 'dgree_of_sweetness/dryness': '-0.08',
 ...
 }
```
# Examples of sake-analogy
- Input sake: "金鵄正宗_純米大吟醸_祝"
```python
# About "金鵄正宗_純米大吟醸_祝"

{'alcohol_rate': {'max': '16.00',
                  'mean': '16.50',
                  'min': '17.00'},
 'amino_acid_content': {'max': '1.10',
                        'mean': '1.10',
                        'min': '1.10'},
 'brand': '金鵄正宗',
 'brand+name': '金鵄正宗 純米大吟醸 祝',
 'brewer': 'キンシ正宗',
 'city': '京都市伏見区',
 'dgree_of_sweetness/dryness': '0.11',
 'method_for_making_sake': [],
 'name': '純米大吟醸 祝',
 'prefecture': '京都府',
 'rice': ['祝'],
 'rice_polishing_rate': '45',
 'sake_class': '純米大吟醸',
 'sake_meter_value': {'max': '1.00',
                      'mean': '1.00',
                      'min': '1.00'},
 'titratable_acidity': {'max': '1.20',
                        'mean': '1.20',
                        'min': '1.20'},
 'yeast': []}
```
## 1. Change rice
- ```[brand+name] - [rice A] + [rice B]```
- "金鵄正宗_純米大吟醸_祝" - "山田錦" + "祝" = "松屋久兵衛"
- "山田錦" -> "祝"
- "松屋久兵衛" is a sake brewed by "キンシ正宗", which is the same brewery as "金鵄正宗_純米大吟醸_祝", but the rice is changed as "祝"
```python
import utils
import pprint
model = utils.load_sake_embedding()
api = utils.SearchAPI()

# Analogy: change the type of rice
result = model.most_similar(positive=['brand+name:金鵄正宗_純米大吟醸_祝', 'rice:山田錦'], negative=['rice:祝'], topn=3)

[('brand:松屋久兵衛', 0.45839840173721313), # most similar word
 ('brand:切子', 0.4513291120529175),
 ('brand+name:北洋_袋取り雫酒', 0.44058412313461304)]
 
# Search about 'brand:松屋久兵衛'
target = 'brand:松屋久兵衛'
results = api.and_search(target)
pprint.pprint(results[0], width=40)

{'alcohol_rate': {'max': '16.00',
                 'mean': '16.50',
                 'min': '17.00'},
'amino_acid_content': {'max': '1.10',
                       'mean': '1.10',
                       'min': '1.10'},
'brand': '松屋久兵衛',
'brand+name': '松屋久兵衛 ',
'brewer': 'キンシ正宗',       # Same brewer as 'brand+name:金鵄正宗_純米大吟醸_祝'
'city': '京都市伏見区',
'dgree_of_sweetness/dryness': '0.11',
'method_for_making_sake': [],
'name': '',
'prefecture': '京都府',
'rice': ['山田錦'],          # Type of the rice is changed by the analogy
'rice_polishing_rate': '35',
'sake_class': '純米大吟醸',
'sake_meter_value': {'max': '1.00',
                     'mean': '1.00',
                     'min': '1.00'},
'titratable_acidity': {'max': '1.20',
                       'mean': '1.20',
                       'min': '1.20'},
'yeast': []}
```

## 2. Change rice polishing rate
- ```[brand+name] - [rice_polishing_rate A] + [rice_polishing_rate B]```
- 45% -> 60%
```python
import utils
import pprint
model = utils.load_sake_embedding()
api = utils.SearchAPI()

# Analogy: change the rice polishing rate
result = model.most_similar(positive=['brand+name:金鵄正宗_純米大吟醸_祝', 'rice_polishing_rate:60'], negative=['rice_polishing_rate:45'], topn=3)

[('brand+name:金鵄正宗_特別純米', 0.6118292808532715),
 ('brand+name:金閣_荒武者', 0.571118950843811),
 ('brand+name:松屋久兵衛', 0.566016674041748)]

# Search about 'brand+name:金鵄正宗_特別純米'
target = 'brand+name:金鵄正宗_特別純米'
results = api.and_search(target)
pprint.pprint(results[0], width=40)

{'alcohol_rate': {'max': '15.00',
                  'mean': '15.50',
                  'min': '16.00'},
 'amino_acid_content': {'max': '1.30',
                        'mean': '1.30',
                        'min': '1.30'},
 'brand': '金鵄正宗',
 'brand+name': '金鵄正宗 特別純米',
 'brewer': 'キンシ正宗',       # Same brewer as 'brand+name:金鵄正宗_純米大吟醸_祝'
 'city': '京都市伏見区',
 'dgree_of_sweetness/dryness': '-0.17',
 'method_for_making_sake': [],
 'name': '特別純米',
 'prefecture': '京都府',
 'rice': ['五百万石'],
 'rice_polishing_rate': '60', # The rice polishing rate is changed
 'sake_class': '特別純米',
 'sake_meter_value': {'max': '1.50',
                      'mean': '1.50',
                      'min': '1.50'},
 'titratable_acidity': {'max': '1.40',
                        'mean': '1.40',
                        'min': '1.40'},
 'yeast': []}
```
