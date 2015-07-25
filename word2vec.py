# -*- coding: utf-8 -*-

from gensim.models import Word2Vec


class Word2VecUtilities:
    def load_vectors_from(self, vector_file_path, binary=True):
        print("Starting Word2Vec Learning...")
        self.weight_matrix = Word2Vec.load_word2vec_format(vector_file_path,
                                                           binary=binary)

    def most_similar_to(self, to, topn):
        return self.weight_matrix.most_similar(to, topn=topn)
