WeSAKE: Word Embeddings of Sake
====
# Setup
- Download  **sake dataset** from [here](https://github.com/yoichi1484/sake_dataset)
```
$ cd data
$ git clone https://github.com/yoichi1484/sake_dataset
$ cp sake_dataset/json/sake_dataset_v1.json ./
```
# Usage
## Training sake embeddings with gensim
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
