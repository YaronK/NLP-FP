# -*- coding: utf-8 -*-
from synset_graph_extension import SynsetGraphExtension as SGE


class Evaluation:
    @staticmethod
    def evaluate(test_graph, gold_graph, balance_grpahs):

        if balance_grpahs:
            (test_graph, gold_graph) = Evaluation._balance_graphs(test_graph,
                                                                  gold_graph)

        gold_node_set = set(gold_graph.get_synset_nodes())
        test_node_set = set(test_graph.get_synset_nodes())

        intersection_set = test_node_set & gold_node_set
        union_set = test_node_set | gold_node_set

        return float(len(intersection_set)) / len(union_set)

    @staticmethod
    def _balance_graphs(test_graph, gold_graph):
        number_of_gold_leaves = len(gold_graph.get_leaf_synsets())
        number_of_test_leaves = len(test_graph.get_leaf_synsets())
        if (number_of_gold_leaves > number_of_test_leaves):
            gold_graph = SGE.thin_out_graph(gold_graph,
                                            number_of_test_leaves)
        elif (number_of_test_leaves > number_of_gold_leaves):
            test_graph = SGE.thin_out_graph(test_graph,
                                            number_of_gold_leaves)
        return (test_graph, gold_graph)
