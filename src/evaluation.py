# -*- coding: utf-8 -*-

from src.synset_graph_comparison import SynsetGraphComarison
from src.synset_graph_extension import SynsetGraphExtension as SGE


class Evaluation:
    def __init__(self, wnUtilities):
        self.wnUtilities = wnUtilities

    def evaluate(self, number_of_synsets, word_to_decoded_graph_dict):
        word_to_comparison_dict = dict()
        category_results = dict()

        for word, decoded_graph in word_to_decoded_graph_dict.items():

            baseline_graph = SGE.build_baseline_graph()
            baseline_graph.dump_to_file("{}-{}.txt".format(word, "baseline"))

            gold_graph = SGE.build_gold_graph(word, self.wnUtilities)
            baseline_graph.dump_to_file("{}-{}.txt".format(word, "gold"))

            comparison = SynsetGraphComarison(baseline_graph, decoded_graph,
                                              gold_graph)
            comparison.compare_using_all_methods()
            comparison.dump_to_file("{}-{}.txt".format(word,
                                                       number_of_synsets))
            word_to_comparison_dict[word] = comparison

            for category, result in comparison.results.items():
                if category not in category_results:
                    category_results[category] = 0
                category_results[category] += result

        with open("categories-{}.txt".format(number_of_synsets), 'w') as category_results_file:
            for category, result in category_results.items():
                category_results[category] = result / len(word_to_decoded_graph_dict)
                category_results_file.write("{}: {}".format(category, result))

        return word_to_comparison_dict, category_results
