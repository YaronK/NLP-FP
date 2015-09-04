# -*- coding: utf-8 -*-

import sys

from decoding import Decoding
from synset.graph_extension import SynsetGraphExtension as SGE
from utilities.word2vec import Word2VecUtilities
from utilities.wordnet import WordnetUtilities


def main(word, number_of_synsets, vector_file_path):
    print(("Constructing graph for {} with {} leaf synsets using vectors " +
           "from {}").format(word, number_of_synsets, vector_file_path))
    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    decoding = Decoding(wnUtilities)
    decoded_graph = SGE.build_word2vec_graph(word, number_of_synsets,
                                             decoding.wnUtilities)
    print(decoded_graph.display())

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Not enough arguments, using defaults")
        word = "xtwl"
        number_of_synsets = 4
        vector_file_path = "../data/vectors-y.bin"
    else:
        word = sys.argv[1]
        number_of_synsets = int(sys.argv[2])
        vector_file_path = sys.argv[3]
    try:
        main(word, number_of_synsets, vector_file_path)
    except Exception as exception:
        print(exception)
