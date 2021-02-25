from gensim.models import KeyedVectors
import pprint
import json


def preprocessing(sake_data):
    return sake_data.strip().replace(' ', '_')
    

def fix_data(data):
    fixed_data = []
    for k, v in sorted(data.items(), key=lambda x:x[0]):
        if 'mean' in v:
            fixed_data.append('{}:{}'.format(k, v['mean']))
        elif type(v) == list:
            for _v in v:
                _v = preprocessing(_v)
                fixed_data.append('{}:{}'.format(k, _v))
        else:
            v = preprocessing(v)
            fixed_data.append('{}:{}'.format(k, v.strip()))
    return fixed_data


def load_dataset():
    with open('../data//sake_dataset/json/sake_dataset_v1.json') as f:
        dataset = json.load(f)
    return dataset


def load_sake_embedding():
    return KeyedVectors.load_word2vec_format('model.txt')


class SearchAPI():
    def __init__(self):
        self.dataset = load_dataset()['dataset']
        
    def and_search(self, *args):
        """ This function returns sake data that contain the queries
            Args: 
                queries
            Return: 
                data (list) that contain the queries
            Example:
            >>> api = SearchAPI()
            >>> results = api.and_search("brand:英勲", "rice:祝")
            >>> pprint.pprint(results[0], width=40)
            {'alcohol_rate': {'max': '15.00', 'mean': '15.00', 'min': '15.00'},
             'amino_acid_content': {'max': '', 'mean': '', 'min': ''},
             'brand': '英勲',
             ...
            }
        """
        result = self.dataset
        for query in args:
            result = self.filtering(query, result)
        return result
    
    def filtering(self, query, dataset):
        return [d for d in dataset if query in fix_data(d)]
    
    
