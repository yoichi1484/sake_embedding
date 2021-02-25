import json
import pprint
from gensim.models import word2vec
import utils


def main():
    dataset = utils.load_dataset()['dataset']
    
    # fix dataset for training
    train_data = [utils.fix_data(data) for data in dataset]
    print('data example')
    pprint.pprint(dataset[1150], width=40)

    # training sgns
    model = word2vec.Word2Vec(train_data, size=100, min_count=0, 
                              window=5, iter=100, sg=1, hs=0)
    
    # save
    model.wv.save_word2vec_format('model.txt')
    print('training done')
    
if __name__ == '__main__':
    main()