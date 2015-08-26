# -*- coding: utf-8 -*-

from synset.graph_extension import SynsetGraphExtension as SGE


class Decoding:
    def __init__(self, wnUtilities):
        self.wnUtilities = wnUtilities

    def decode(self, number_of_synsets, words_file_path):
        with open(words_file_path, encoding='utf8') as words_file:
            words = [line[:-1] for line in words_file.readlines()]
        word_to_decoded_graph = dict()
        for word in words:
            print("Decoding: " + word)
            decoded_graph = SGE.build_word2vec_graph(word, number_of_synsets,
                                                     self.wnUtilities)

            word_to_decoded_graph[word] = decoded_graph
        return word_to_decoded_graph
