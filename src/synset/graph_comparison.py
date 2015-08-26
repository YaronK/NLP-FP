# -*- coding: utf-8 -*-
from synset.graph_extension import SynsetGraphExtension as SGE


class SynsetGraphComarison():
    def __init__(self, baseline_graph, decoded_graph, gold_graph):
        self.baseline_graph = baseline_graph
        self.decoded_graph = decoded_graph
        self.gold_graph = gold_graph

        self.results = {}

    def compare_using_all_methods(self):
        baseline_graph = self.baseline_graph
        decoded_graph = self.decoded_graph
        gold_graph = self.gold_graph
        compare_single = self.compare_using_a_single_method

        compare_single(baseline_graph, gold_graph, SGE.no_thinning)
        compare_single(decoded_graph, gold_graph, SGE.no_thinning)
        compare_single(decoded_graph, gold_graph, SGE.thin_out_graph_by_leaves)
        compare_single(decoded_graph, gold_graph, SGE.thin_out_graph_by_paths)

    def compare_using_a_single_method(self, decoded_graph, gold_graph,
                                      thinning_method):
        if (decoded_graph, gold_graph, thinning_method) in self.results:
            return self.results[(decoded_graph, gold_graph, thinning_method)]

        number_of_gold_leaves = len(gold_graph.get_leaf_synsets())
        number_of_test_leaves = len(decoded_graph.get_leaf_synsets())

        if ((thinning_method is not None) and (number_of_test_leaves >
                                               number_of_gold_leaves)):
            decoded_graph = thinning_method(decoded_graph,
                                            number_of_gold_leaves)

        gold_node_set = set(gold_graph.get_synset_nodes())
        test_node_set = set(decoded_graph.get_synset_nodes())

        intersection_set = test_node_set & gold_node_set
        union_set = test_node_set | gold_node_set

        result = float(len(intersection_set)) / len(union_set)

        self.results[(str(decoded_graph), str(gold_graph),
                      thinning_method.__name__)] = result

        print ("{0} <-> {1}. Thinning: {2}. Result: {3:.3f}".
               format(str(decoded_graph), str(gold_graph),
                      thinning_method.__name__, result))
        return result

    def dump_to_file(self, path):
        line_format = "{0} <-> {1}. Thinning: {2}. Result: {3:.3f}\n"

        results = []
        for (decoded_graph, gold_graph, thinning_method) in self.results:
            result = self.results[(decoded_graph, gold_graph, thinning_method)]
            results.append(line_format.format(str(decoded_graph),
                                              str(gold_graph),
                                              thinning_method,
                                              result))
        results = sorted(results)
        with open("../results/" + path, 'w') as file:
            for result in results:
                file.write(result)
