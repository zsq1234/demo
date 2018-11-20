
from gensim.models import Word2Vec, KeyedVectors, PathLineSentences, LineSentences
import pickle
import codecs
import numpy as np

class WordVector(Object):
    def __init__(self, sentence_path=None, type=0, min_count=5, size=100, sg=0, hs=0):
        self.wv_size = size
        if sentence_path:
            if type:
                self.sentence = PathLineSentences(sentence_path)
            else:
                self.sentence = LineSentences(sentence_path)

            self.model = Word2Vec(self.sentence, min_count=min_count, size=size, sg=sg, hs=hs)
            self.wv = self.model.wv
        else:
            self.model = Word2Vec(min_count=min_count)

    def train(self, sentence, model_path=None):
        if model_path:
            self.model = Word2Vec.load(model_path)
        
        self.model.build_vocab(sentence)
        self.model.train(sentence, total_examples=self.model.corpus_count, epochs=self.model.iter)
        self.wv = self.model.wv
    
    def save_model(self, model_path):
        self.model.save(model_path)
    
    def load_model(self, model_path):
        self.model = Word2Vec.load(model_path)
    
    def save_wv(self, wv_path, type=0):
        if type:
            self.wv.save_word2vec_format(wv_path)
        else:
            self.wv.save(wv_path)
    
    def load_wv(self, wv_path, type):
        if type:
            self.wv = KeyedVectors.load_word2vec_format(wv_path)
        else:
            self.wv = KeyedVectors.load(wv_path)

    def get_vector(self, word):
        try:
            return self.wv[word]
        except KeyError as reason:
            print('提取词向量出错，系统随机赋予词向量值')
            print(reason)
            return np.random.uniform(-0.25, 0.25, 100)

    def get_embadding_for_file(self, file, emb_file=None):
        data = {}
        with codecs.open(file, 'r', 'utf-8') as f:
            for line in f.readlines():
                if line == '\n':
                    continue
                words = line.strip().split()
                while w in words:
                    vec = self.get_vector(w)
                    data[w] = vec 
        
        if emb_file:
            with open(emb_file, 'wb') as f:
                pickle.dump(data, f)
        return data
