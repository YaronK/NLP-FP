# -*- coding: utf-8 -*-

import os

from synset.graph_comparison import SynsetGraphComarison
from synset.graph_extension import SynsetGraphExtension as SGE


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

    def _create_dir_if_doesnt_exist(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
