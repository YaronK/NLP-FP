# -*- coding: utf-8 -*-


class SynsetEdge(object):
    """docstring for SynsetEdge"""
    def __init__(self, hypernym_node, hyponym_node):
        super(SynsetEdge, self).__init__()

        self.hypernym_node = hypernym_node
        self.hyponym_node = hyponym_node

        self.weight = 0
        self.probability = 0

    def add_weight(self, weight):
        self.weight += weight
        self.hypernym_node.add_weight(weight)

    def set_probability(self, probability):
        self.probability = probability
        self.hyponym_node.add_probability(probability)

    def __str__(self):
        return "<{},{}>".format(str(self.hyponym_node),
                                str(self.hypernym_node))


class SynsetNode(object):
    """docstring for SynsetNode"""
    def __init__(self, synset):
        super(SynsetNode, self).__init__()
        self.synset = synset

        self.hypernym_edges = {}  # hypernym_synset_name => SynsetEdge
        self.hyponym_edges = {}  # hyponym_synset_name => SynsetEdge

        self.weight = 0
        self.probability = 0

    def add_weight(self, weight):
        self.weight += weight

        if len(self.hypernym_edges) != 0:
            weight_per_hypernym = weight / float(len(self.hypernym_edges))
            for hypernym_edge in self.hypernym_edges.values():
                hypernym_edge.add_weight(weight_per_hypernym)

    def add_probability(self, probability):
        self.probability += probability

        if len(self.hyponym_edges) != 0:
            for hyponym_edge in self.hyponym_edges.values():
                hyponym_probability = ((hyponym_edge.weight / self.weight) *
                                       self.probability)
                hyponym_edge.set_probability(hyponym_probability)

    def add_hypernym(self, hypernym_node):
        hypernym_name = hypernym_node.synset.name()

        if hypernym_name not in self.hypernym_edges:
            edge = SynsetEdge(hypernym_node, self)
            self.hypernym_edges[hypernym_name] = edge
            hypernym_node.hyponym_edges[self.synset.name()] = edge

    def __repr__(self):
        return str(self) + " (prob.: {0:.3f})".format(self.probability)

    def __str__(self):
        return self.synset.name()


class SynsetGraph(object):
    """docstring for SynsetGraph"""
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
        self.leaf_nodes = {self.synset_nodes[synset]
                           for synset in leaf_synsets}

        for leaf in leaf_synsets:
            leaf_node = synset_nodes[leaf]

            for hypernym_path in leaf.hypernym_paths():
                for i in range(1, len(hypernym_path)):

                    hyponym_node = synset_nodes[hypernym_path[i]]
                    hypernym_node = synset_nodes[hypernym_path[i - 1]]

                    hyponym_node.add_hypernym(hypernym_node)

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
        for hyponym_edge in node.hyponym_edges.values():
            self._print_node(hyponym_edge.hyponym_node, indentation + 1)
