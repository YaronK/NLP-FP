# -*- coding: utf-8 -*-
from synset_node import SynsetNode


class SynsetGraph(object):
    def __init__(self, name, synset_weights_dictionary):
        super(SynsetGraph, self).__init__()

        self.name = name
        self.synset_weights_dictionary = synset_weights_dictionary
        leaf_synsets = set(synset_weights_dictionary.keys())

        self._init_nodes(leaf_synsets)
        self._init_edges(leaf_synsets)

        self._calculate_weights(leaf_synsets, synset_weights_dictionary)
        self._calculate_probabilities()

    def _init_nodes(self, leaf_synsets):
        hypernym_paths = [hypernym_path
                          for synset in leaf_synsets
                          for hypernym_path in synset.hypernym_paths()]
        synsets = {synset
                   for hypernym_path in hypernym_paths
                   for synset in hypernym_path}
        self.synset_to_synset_node_dictionary = {synset: SynsetNode(synset)
                                                 for synset in synsets}
        self.leaf_synsets = leaf_synsets
        self.leaf_synset_nodes = {self.get_synset_node(s)
                                  for s in self.leaf_synsets}

    def _init_edges(self, leaf_synsets):
        for leaf in leaf_synsets:
            for hypernym_path in leaf.hypernym_paths():
                for i in range(1, len(hypernym_path)):

                    hyponym_node = self.get_synset_node(hypernym_path[i])
                    hypernym_node = self.get_synset_node(hypernym_path[i - 1])

                    hyponym_node.add_hypernym(hypernym_node)
                    hypernym_node.add_hyponym(hyponym_node)

    def _calculate_weights(self, leaf_synsets, synset_weights_dictionary):
        for leaf in leaf_synsets:
            leaf_node = self.get_synset_node(leaf)
            leaf_node.add_weight(synset_weights_dictionary[leaf])

    def _calculate_probabilities(self):
        self.get_entity_node().add_probability(1)

    def get_entity_node(self):
        entity_synset = [synset
                         for synset in self.get_synsets()
                         if synset.name() == "entity.n.01"][0]
        # TODO: find the root in a better way
        return self.get_synset_node(entity_synset)

    def get_leaf_synsets(self):
        return self.leaf_synsets

    def get_leaf_synset_nodes(self):
        return self.leaf_synset_nodes

    def get_synsets(self):
        return self.synset_to_synset_node_dictionary.keys()

    def get_synset_node(self, synset):
        return self.synset_to_synset_node_dictionary[synset]

    def get_synset_nodes(self):
        return self.synset_to_synset_node_dictionary.values()

    def get_synset_weights_dictionary(self):
        return self.synset_weights_dictionary

    def print_tree(self):
        print ("{0}:".format(self.name))
        self._print_node(self.get_entity_node(), 0)

    def _print_node(self, node, indentation):
        print("|   " * indentation + node.synset.name(), end="")
        while(len(node.hyponym_nodes) == 1):
            node = list(node.hyponym_nodes.keys())[0]
            print(" > " + node.synset.name(), end="")
        print("({0:.3f})".format(node.total_probability()))
        for hyponym_node in node.hyponym_nodes:
            self._print_node(hyponym_node, indentation + 1)
