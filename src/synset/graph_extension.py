# -*- coding: utf-8 -*-
from nltk.corpus import wordnet as WN

from synset.graph import SynsetGraph


class SynsetGraphExtension:
    @staticmethod
    def build_baseline_graph(word):
        entity_synset = WN.synset('entity.n.01')  # @UndefinedVariable
        return SynsetGraph("Baseline", {entity_synset: 1.0})

    @staticmethod
    def build_word2vec_graph(word, number_of_synsets, wnUtilities):
        word2vec_synsets = \
            wnUtilities.get_word2vec_similar_synsets(word, number_of_synsets)
        if word2vec_synsets is None:
            print ("No word2vec similar synsets for {}.\n".format(word))
            return
        return SynsetGraph("Word2Vec", word2vec_synsets)

    @staticmethod
    def build_gold_graph(word, wnUtilities):
        gold_synsets = wnUtilities.get_gold_synsets(word)
        if gold_synsets is None:
            print ("No WordNet synsets were found for {}.\n".format(word))
            return
        return SynsetGraph("Gold", gold_synsets)

    @staticmethod
    def no_thinning(graph, number_of_leaves):
        return graph

    @staticmethod
    def thin_by_leaf_probabilities(graph, number_of_leaves):
        leaf_synset_nodes = graph.get_leaf_synset_nodes()
        leaf_synset_nodes = sorted(leaf_synset_nodes,
                                   key=lambda n: n.get_synset().name())
        leaf_synset_nodes = sorted(leaf_synset_nodes,
                                   key=lambda n: int(n.total_probability() *
                                                     10000),
                                   reverse=True)[:number_of_leaves]
        synset_weights_dictionary = {node.get_synset(): node.total_weight()
                                     for node in leaf_synset_nodes}

        return SynsetGraph(graph.name, synset_weights_dictionary)

    @staticmethod
    def thin_by_probability_paths(graph, number_of_leaves):
        chosen_synsets = {}  # synset : weight

        synset_weights = graph.get_synset_weights_dictionary().copy()
        temp_grpah = graph
        for _ in range(number_of_leaves):
            root_node = temp_grpah.get_entity_node()
            temp_node = root_node
            while not temp_node.is_leaf():
                hyponym_nodes = sorted(temp_node.get_hyponym_nodes(),
                                       key=lambda n: n.get_synset().name())
                hyponym_nodes = sorted(hyponym_nodes,
                                       key=lambda n: int(n.total_probability()
                                                         * 10000))
                temp_node = hyponym_nodes[-1]
            temp_synset = temp_node.get_synset()
            chosen_synsets[temp_synset] = temp_node.total_weight()
            del synset_weights[temp_synset]
            temp_grpah = SynsetGraph("Temp", synset_weights)

        return SynsetGraph(graph.name, chosen_synsets)
