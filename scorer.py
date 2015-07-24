# -*- coding: utf-8 -*-


class SynsetNode(object):
    def __init__(self, synset):
        super(SynsetNode, self).__init__()
        self.synset = synset

        self.hypernym_nodes = dict()  # hypernym_node : probability
        self.hyponym_nodes = dict()  # hyponym_node : weight

    def add_hypernym(self, hypernym_node):
        if hypernym_node not in self.hypernym_nodes:
            self.hypernym_nodes[hypernym_node] = 0

    def add_hyponym(self, hyponym_node):
        if hyponym_node not in self.hyponym_nodes:
            self.hyponym_nodes[hyponym_node] = 0

    def add_weight(self, weight, from_hyponym=None):
        if from_hyponym is None:
            self._total_weight = weight
        else:
            self.hyponym_nodes[from_hyponym] += weight

        weight_per_hypernym = (0 if (len(self.hypernym_nodes) == 0) else
                               weight / float(len(self.hypernym_nodes)))
        for hypernym_node in self.hypernym_nodes:
            hypernym_node.add_weight(weight_per_hypernym, self)

    def add_probability(self, probability, from_hypernym=None):
        if from_hypernym is None:
            self._total_probability = probability
        else:
            self.hypernym_nodes[from_hypernym] += probability

        for hyponym_node in self.hyponym_nodes:
            hyponym_probability = ((self.hyponym_nodes[hyponym_node] /
                                    self.total_weight()) * probability)
            hyponym_node.add_probability(hyponym_probability, self)

    def total_weight(self):
        if not hasattr(self, "_total_weight"):
            self._total_weight = sum(self.hyponym_nodes.values())
        return self._total_weight

    def total_probability(self):
        if not hasattr(self, "_total_probability"):
            self._total_probability = sum(self.hypernym_nodes.values())
        return self._total_probability

    def __repr__(self):
        return str(self) + " ({0:.3f})".format(self.total_probability())

    def __str__(self):
        return self.synset.name()


class SynsetGraph(object):
    def __init__(self, synset_weight_dict):
        super(SynsetGraph, self).__init__()

        leaf_synsets = set(synset_weight_dict.keys())

        hypernym_paths = [hypernym_path
                          for synset in leaf_synsets
                          for hypernym_path in synset.hypernym_paths()]

        self.synsets = synsets = {synset
                                  for hypernym_path in hypernym_paths
                                  for synset in hypernym_path}
        self.synset_nodes = synset_nodes = {synset: SynsetNode(synset)
                                            for synset in synsets}
        self.leaf_nodes = {synset_nodes[synset] for synset in leaf_synsets}

        for leaf in leaf_synsets:
            for hypernym_path in leaf.hypernym_paths():
                for i in range(1, len(hypernym_path)):

                    hyponym_node = synset_nodes[hypernym_path[i]]
                    hypernym_node = synset_nodes[hypernym_path[i - 1]]

                    hyponym_node.add_hypernym(hypernym_node)
                    hypernym_node.add_hyponym(hyponym_node)

        for leaf in leaf_synsets:
            leaf_node = synset_nodes[leaf]
            leaf_node.add_weight(synset_weight_dict[leaf])

        self.get_entity_node().add_probability(1)

    def get_entity_node(self):
        entity_synset = [synset
                         for synset in self.synsets
                         if synset.name() == "entity.n.01"][0]
        return self.synset_nodes[entity_synset]

    def print_tree(self):
        self._print_node(self.get_entity_node(), 0)

    def _print_node(self, node, indentation):
        print("|   " * indentation + repr(node))
        for hyponym_node in node.hyponym_nodes:
            self._print_node(hyponym_node, indentation + 1)
