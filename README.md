WeSAKE: Word Embeddings of Sake
====
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE.txt)
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
## Analogy example
- Change the type of rice
- [brand+name] - [rice] + [rice]
- "金鵄正宗_純米大吟醸_祝" - "山田錦" + "祝" = "松屋久兵衛"
- "松屋久兵衛" is a sake brewed by "金鵄正宗" that is the same brewery as "金鵄正宗_純米大吟醸_祝", but the rice is changed as "祝"
```python
import utils
import pprint
model = utils.load_sake_embedding()
api = utils.SearchAPI()

# Analogy: change the type of rice
result = model.most_similar(positive=['brand+name:金鵄正宗_純米大吟醸_祝', 'rice:山田錦'], negative=['rice:祝'], topn=3)
# result
# [('brand:松屋久兵衛', 0.45839840173721313), # most similar word
#  ('brand:切子', 0.4513291120529175),
#  ('brand+name:北洋_袋取り雫酒', 0.44058412313461304)]
 
# Search about 'brand:松屋久兵衛'
target = result[0][0]
results = api.and_search(target)
pprint.pprint(results[0], width=40)

# {'alcohol_rate': {'max': '16.00',
#                   'mean': '16.50',
#                   'min': '17.00'},
#  'amino_acid_content': {'max': '1.10',
#                         'mean': '1.10',
#                         'min': '1.10'},
#  'brand': '松屋久兵衛',
#  'brand+name': '松屋久兵衛 ',
#  'brewer': 'キンシ正宗',       # Same brewer as 'brand+name:金鵄正宗_純米大吟醸_祝'
#  'city': '京都市伏見区',
#  'dgree_of_sweetness/dryness': '0.11',
#  'method_for_making_sake': [],
#  'name': '',
#  'prefecture': '京都府',
#  'rice': ['山田錦'],          # Type of the rice is changed by the analogy
#  'rice_polishing_rate': '35',
#  'sake_class': '純米大吟醸',
#  'sake_meter_value': {'max': '1.00',
#                       'mean': '1.00',
#                       'min': '1.00'},
#  'titratable_acidity': {'max': '1.20',
#                         'mean': '1.20',
#                         'min': '1.20'},
#  'yeast': []}
```
