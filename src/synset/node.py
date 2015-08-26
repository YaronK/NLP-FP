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
        if from_hyponym is None:  # i.e. leaf
            self._total_weight = weight
        else:
            self.hyponym_nodes[from_hyponym] += weight

        number_of_hypernym_nodes = len(self.hypernym_nodes)
        weight_per_hypernym = (0 if (number_of_hypernym_nodes == 0) else
                               weight / float(number_of_hypernym_nodes))
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

    def is_leaf(self):
        return len(self.hyponym_nodes) == 0

    def is_root(self):
        return len(self.hypernym_nodes) == 0

    def get_hypernym_nodes(self):
        return list(self.hypernym_nodes.keys())

    def get_hyponym_nodes(self):
        return list(self.hyponym_nodes.keys())

    def get_synset(self):
        return self.synset

    def total_weight(self):
        #  Should be called only after weights have been calculated
        if not hasattr(self, "_total_weight"):
            self._total_weight = sum(self.hyponym_nodes.values())
        return self._total_weight

    def total_probability(self):
        #  Should be called only after probabilities have been calculated
        if not hasattr(self, "_total_probability"):
            self._total_probability = sum(self.hypernym_nodes.values())
        return self._total_probability

    def __repr__(self):
        return str(self) + " ({0:.3f})".format(self.total_probability())

    def __str__(self):
        return self.synset.name()

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and (self.synset ==
                                                       other.synset))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.synset.__hash__()
