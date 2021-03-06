import json
import pprint
import argparse
from gensim.models import word2vec
import utils


def main(size, min_count, iter):
    dataset = utils.load_dataset()['dataset']
    
    # fix dataset for training
    train_data = [utils.fix_data(data) for data in dataset]
    print('data example')
    pprint.pprint(dataset[1150], width=40)

    # training sgns
    model = word2vec.Word2Vec(train_data, size=size, min_count=min_count, 
                              window=5, iter=iter, sg=1, hs=0)
    
    # save
    model.wv.save_word2vec_format('model.txt')
    print('training done')
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', '-s', default=100, type=int, 
                        help='Dimention of the embedding space. (default = 100)')
    parser.add_argument('--min_count', '-m', default=0, type=int, 
                        help=' Ignores all words with total frequency lower than this. (default = 0)')
    parser.add_argument('--iter', '-i', default=100, type=int, 
                        help='Number of iteration (default = 0)')
    args = parser.parse_args()
    main(args.size, args.min_count, args.iter)
