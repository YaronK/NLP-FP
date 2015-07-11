# -*- coding: utf-8 -*-
from nltk.corpus import wordnet as wn


class SynsetEdge(object):
    """docstring for SynsetEdge"""
    def __init__(self, hypernym_node, hyponym_node):
        super(SynsetEdge, self).__init__()

        self.hypernym_node = hypernym_node
        self.hyponym_node = hyponym_node

        self.weight = 0
        self.probability = 0

    def set_weight(self, weight):
        self.weight = weight
        self.hypernym_node.add_weight(weight)

    def set_probability(self, probability):
        self.probability = probability
        self.hyponym_node.add_probability(probability)


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

        weight_per_hypernym = weight / float(len(self.hypernym_edges))
        for hypernym_edge in self.hypernym_edges:
            hypernym_edge.set_weight(weight_per_hypernym)

    def add_probability(self, probability):
        self.probability += probability

        probability_per_hyponym = probability / float(len(self.hyponym_edges))
        for hyponym_edge in self.hyponym_edges:
            hyponym_edge.set_probability(probability_per_hyponym)

    def add_hypernym(self, hypernym_node):
        hypernym_name = hypernym_node.synset.name()

        if hypernym_name not in self.hypernym_edges:
            edge = SynsetEdge(hypernym_node, self)
            self.hypernym_edges[hypernym_name] = edge
            hypernym_node.hyponym_edges[self.synset.name()] = edge


class SynsetGraph(object):
    """docstring for SynsetGraph"""
    def __init__(self, synset_weight_dict):
        super(SynsetGraph, self).__init__()

        leaf_synsets = set(synset_weight_dict.keys())

        hypernym_paths = {hypernym_path for hypernym_path in synset.hypernym_paths()
                                        for synset in leaf_synsets}
        synsets = {synset for synset in hypernym_path for hypernym_path in hypernym_paths}
        synset_nodes = {synset : SynsetNode(synset) for synset in synsets}

        for leaf in leaf_synsets:
            leaf_node = synset_nodes[leaf_node]
            
            for hypernym_path in leaf.hypernym_paths():
                for i in xrange(0,len(hypernym_path - 1)):
                    
                    hyponym_node = synset_nodes[hypernym_path[i]]
                    hypernym_node = synset_nodes[hypernym_path[i + 1]]

                    hyponym_node.add_hypernym(hypernym_node)

        for leaf in leaf_synsets:
            leaf_node = synset_nodes[leaf_node]
            leaf_node.add_weight(synset_weight_dict[leaf])

        entity_synset = [synset for synset in synsets if synset.name() == "entity"][0]
        entity_node = synset_nodes[entity_synset]

        entity_node.add_probability(1)

        self.synset_nodes = synset_nodes









class SynsetProperties(object):
    """docstring for SynsetProperties"""
    def __init__(self, synset):
        super(SynsetProperties, self).__init__()
        
        self.synset = synset
        self.reference_count = 0
        self.avg_depth = (self.synset.min_depth() + self.synset.max_depth()) / float(2)
    
    def increment_reference_count(self, synset_weight):
        self.reference_count += synset_weight

    #def __str__(self):
    #   return ("name: {}\n".format(self.synset.name()) +
    #           "reference_count: {}\n".format(self.reference_count) +
    #           "avg_depth: {}\n".format(self.avg_depth) +
    #           "definition: {}".format(self.synset.definition()))

    def __repr__(self):
        return self.synset.name()

class SynsetScorer(object):
    """docstring for SynsetScorer"""
    def __init__(self):
        super(SynsetScorer, self).__init__()
        
        self.synset_dict = {}

    def _add_hypernym_path_synsetss(self, hypernym_path, synset_weight):
        for synset in hypernym_path:
            if synset.name() not in self.synset_dict:
                self.synset_dict[synset.name()] = SynsetProperties(synset)
            self.synset_dict[synset.name()].increment_reference_count(synset_weight)

    def add_hypernym_paths(self, synset, synset_weight=1):
        for hypernym_path in synset.hypernym_paths():
            self._add_hypernym_path(hypernym_path, synset_weight)

    def sort_synsets_by(self, key_func, reverse=True, display=False):
        sorted_synsets = sorted(self.synset_dict.values(), key=key_func, reverse=reverse)
        
        if display:
            for sp in sorted_synsets:
                print(sp)
                print('\n')

        return sorted_synsets

def main():
   scorer = SynsetScorer()

   dog_synsets = wn.synsets("dog")
   cat_synsets = wn.synsets("cat")
   mouse_synsets = wn.synsets("mouse")
   horse_synsets = wn.synsets("horse")

   dog = dog_synsets[0]
   cat = cat_synsets[0]
   mouse = mouse_synsets[0]
   horse = horse_synsets[0]

   scorer.add_hypernym_paths(dog)
   scorer.add_hypernym_paths(cat)
   scorer.add_hypernym_paths(mouse)
   scorer.add_hypernym_paths(horse)

   print(scorer.sort_synsets_by(lambda sp: sp.reference_count * sp.avg_depth))