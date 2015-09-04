# -*- coding: utf-8 -*-

from decoding import Decoding
from evaluation import Evaluation
from synset.graph_extension import SynsetGraphExtension as SGE
from utilities.word2vec import Word2VecUtilities
from utilities.wordnet import WordnetUtilities


def main():
    word = input("Enter a Hebrew word:\n")
    number_of_synsets = int(input("Enter the number of synsets:\n"))
    vector_file_path = "../data/vectors-y.bin"

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
    try:
        main()
    except:
        print("At least one of the input parameters isn't correct")
