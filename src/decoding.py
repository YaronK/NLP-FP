# -*- coding: utf-8 -*-

from synset.graph_extension import SynsetGraphExtension as SGE
from utilities.word2vec import Word2VecUtilities
from utilities.wordnet import WordnetUtilities


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


def main():
    synsets_number = int(input("Enter the number of synsets:\n"))
    path = input("Please write the path to the wanted" +
                 "Hebrew words(../exps/heb_n_10.words):\n")

    vector_file_path = "../data/vectors-y.bin"

    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    decoding = Decoding(wnUtilities)
    word_to_decoded_graph_dict = decoding.decode(synsets_number, path)

    for word, decoded_graph in word_to_decoded_graph_dict.items():
        baseline_graph = SGE.build_baseline_graph(word)
        print("baseline for {}:\n{}".format(word, baseline_graph.display()))

        gold_graph = SGE.build_gold_graph(word, wnUtilities)
        print("gold_graph for {}:\n{}".format(word, gold_graph.display()))

        print("decoded for {}:\n{}".format(word, decoded_graph.display()))

    print(word_to_decoded_graph_dict)

    print("specific files can be found under 'exps' folder")

if __name__ == '__main__':
    try:
        main()
    except:
        print("At least one of the input parameters isn't correct")
