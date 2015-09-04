# -*- coding: utf-8 -*-

import os

from synset.graph_comparison import SynsetGraphComarison
from synset.graph_extension import SynsetGraphExtension as SGE
from utilities.word2vec import Word2VecUtilities
from utilities.wordnet import WordnetUtilities
from decoding import Decoding
import sys


class Evaluation:
    def __init__(self, wnUtilities):
        self.wnUtilities = wnUtilities
        exps_dir_path = "../exps/"
        results_dir_path = "../results/"

        self._create_dir_if_doesnt_exist(exps_dir_path)
        self._create_dir_if_doesnt_exist(results_dir_path)

    def evaluate(self, number_of_synsets, word_to_decoded_graph_dict):
        word_to_comparison_dict = dict()
        category_results = dict()

        for word, decoded_graph in word_to_decoded_graph_dict.items():
            exps_dir_path = "../exps/{}-{}/".format(word, number_of_synsets)
            results_dir_path = "../results/{}-{}/".format(word,
                                                          number_of_synsets)
            self._create_dir_if_doesnt_exist(exps_dir_path)
            self._create_dir_if_doesnt_exist(results_dir_path)

            baseline_graph = SGE.build_baseline_graph(word)
            baseline_graph.dump_to_file(exps_dir_path + "baseline.txt")

            gold_graph = SGE.build_gold_graph(word, self.wnUtilities)
            baseline_graph.dump_to_file(exps_dir_path + "gold.txt")

            decoded_graph.dump_to_file(exps_dir_path + "decoded.txt")

            comparison = SynsetGraphComarison(baseline_graph, decoded_graph,
                                              gold_graph)
            comparison.compare_using_all_methods()
            comparison.dump_to_file(results_dir_path + "comparison.txt")
            word_to_comparison_dict[word] = comparison

            for category, result in comparison.results.items():
                if category not in category_results:
                    category_results[category] = 0
                category_results[category] += result

        with open("../results/final-{}.txt".format(number_of_synsets),
                  'w', encoding='utf8') as category_results_file:
            for category, result in category_results.items():
                category_results[category] = (result /
                                              len(word_to_decoded_graph_dict))
                category_results_file.write("{}: {}\n".
                                            format(category,
                                                   category_results[category]))

        return word_to_comparison_dict, category_results

    def _create_dir_if_doesnt_exist(self, words_path):
        if not os.path.exists(words_path):
            os.makedirs(words_path)


def main(synsets_number, vector_file_path, words_path):
    print("Evaluation illustration for: {}, {}, {}".format(number_of_synsets,
                                                           vector_file_path,
                                                           words_path))
    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    decoding = Decoding(wnUtilities)
    word_to_decoded_graph_dict = decoding.decode(synsets_number, words_path)

    evaluation = Evaluation(wnUtilities)
    evaluation.evaluate(synsets_number, word_to_decoded_graph_dict)

    print("\nEvaluation files can be found under 'results' folder")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Not enough arguments, using defaults")
        number_of_synsets = 3
        vector_file_path = "../data/vectors-y.bin"
        words_path = "../exps/heb_n_10.words"
    else:
        number_of_synsets = int(sys.argv[1])
        vector_file_path = sys.argv[2]
        words_path = sys.argv[3]
    try:
        main(number_of_synsets, vector_file_path, words_path)
    except:
        print("At least one of the input parameters isn't correct")
