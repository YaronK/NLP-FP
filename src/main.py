# -*- coding: utf-8 -*-

from decoding import Decoding
from evaluation import Evaluation
from synset.graph_extension import SynsetGraphExtension as SGE
from utilities.word2vec import Word2VecUtilities
from utilities.wordnet import WordnetUtilities
import sys


def main(word, number_of_synsets, vector_file_path):
    print("Demo illustration for: {}, {}, {}".format(word, number_of_synsets,
                                                     vector_file_path))
    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    decoding = Decoding(wnUtilities)
    word_to_decoded_graph_dict = dict()
    print("Decoding: " + word)
    decoded_graph = SGE.build_word2vec_graph(word, number_of_synsets,
                                             decoding.wnUtilities)
    word_to_decoded_graph_dict[word] = decoded_graph

    evaluation = Evaluation(wnUtilities)
    _, category_results = \
        evaluation.evaluate(number_of_synsets, word_to_decoded_graph_dict)

    print(category_results)

    print("\nDecoding files for {} are under 'exps' folder".format(word))
    print("Evaluation files for {} are under 'results' folder".format(word))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Not enough arguments, using defaults")
        word = "חתול"
        number_of_synsets = 3
        vector_file_path = "../data/vectors-y.bin"
    else:
        word = sys.argv[1]
        number_of_synsets = int(sys.argv[2])
        vector_file_path = sys.argv[3]
    try:
        main(word, number_of_synsets, vector_file_path)
    except:
        print("At least one of the input parameters isn't correct")
