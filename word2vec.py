# -*- coding: utf-8 -*-

from gensim.models import Word2Vec


class Word2VecUtilities:
    def load_vectors_from(self, vector_file_path, binary=True):
        print("Loading vectors from {0}".format(vector_file_path))
        self.weight_matrix = Word2Vec.load_word2vec_format(vector_file_path,
                                                           binary=binary)

    def most_similar_to(self, to, topn):
        try:
            return self.weight_matrix.most_similar(to, topn=topn)
        except Exception:
            print("Word {0} doesn't exists in vocabulary".format(to))
            return None
