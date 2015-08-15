# -*- coding: utf-8 -*-
from src.synset_node import SynsetNode
import os

class SynsetGraph(object):
    def __init__(self, name, synset_weights_dictionary):
        super(SynsetGraph, self).__init__()

        self.name = name
        self.synset_weights_dictionary = synset_weights_dictionary
        leaf_synsets = set(synset_weights_dictionary.keys())

        self._init_nodes(leaf_synsets)
        self._init_edges(leaf_synsets)
        self.root_node = self._find_root_node()

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

    def _find_root_node(self):
        synset = list(self.get_synsets())[0]
        while not self.get_synset_node(synset).is_root():
            hypernyms = synset.hypernyms()
            synset = hypernyms[0]
        return self.get_synset_node(synset)

    def get_entity_node(self):
        return self.root_node

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

    def display(self):
        return ("{0}:".format(self.name) + "\n" +
                self._display_node(self.get_entity_node(), 0))

    def _display_node(self, node, indentation):
        temp = "|   " * indentation + node.synset.name()
        while(len(node.hyponym_nodes) == 1):
            node = list(node.hyponym_nodes.keys())[0]
            temp += " > " + node.synset.name()
        temp += "({0:.3f})\n".format(node.total_probability())
        for hyponym_node in node.hyponym_nodes:
            temp += self._display_node(hyponym_node, indentation + 1)
        return temp

    def __str__(self):
        return self.name
