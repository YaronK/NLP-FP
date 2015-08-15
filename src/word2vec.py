# -*- coding: utf-8 -*-

from gensim.models import Word2Vec


class SimilarWordsRetriever:
    def __init__(self, to, weight_matrix):
        self.retrieved = 0
        self.to = to
        self.weight_matrix = weight_matrix

    def get(self, n):
        try:
            similar = self.weight_matrix.most_similar(self.to, topn=n)
            self.retrieved = n
            return similar
        except Exception:
            print("Word {0} doesn't exists in vocabulary".format(self.to))
            return None

    def get_more(self):
        similar = self.weight_matrix.\
            most_similar(self.to, topn=self.retrieved*2)[self.retrieved:]
        self.retrieved *= 2
        return similar


class Word2VecUtilities:
    def load_vectors_from(self, vector_file_path, binary=True):
        print("Loading vectors from {0}".format(vector_file_path))
        self.weight_matrix = Word2Vec.load_word2vec_format(vector_file_path,
                                                           binary=binary)

    def build_retriever(self, to):
        return SimilarWordsRetriever(to, self.weight_matrix)
