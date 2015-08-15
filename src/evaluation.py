# -*- coding: utf-8 -*-

from src.synset_graph_extension import SynsetGraphExtension as SGE


def compare_graph_pair(decoded_graph, gold_graph,
                       thinning_method=SGE.no_thinning):
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
    print ("Compared: {0} <-> {1}. Thinning: {2}. Result: {3:.3f}".
           format(str(decoded_graph), str(gold_graph),
                  thinning_method.__name__, result))
    return result
