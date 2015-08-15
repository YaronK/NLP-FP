# -*- coding: utf-8 -*-


class Evaluation:
    @staticmethod
    def evaluate(test_graph, gold_graph, thinning_method=None):
        number_of_gold_leaves = len(gold_graph.get_leaf_synsets())
        number_of_test_leaves = len(test_graph.get_leaf_synsets())

        if ((thinning_method is not None) and (number_of_test_leaves >
                                               number_of_gold_leaves)):
            test_graph = thinning_method(test_graph, number_of_gold_leaves)

        gold_node_set = set(gold_graph.get_synset_nodes())
        test_node_set = set(test_graph.get_synset_nodes())

        intersection_set = test_node_set & gold_node_set
        union_set = test_node_set | gold_node_set

        return float(len(intersection_set)) / len(union_set)
