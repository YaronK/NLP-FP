# -*- coding: utf-8 -*-
from nltk.corpus import wordnet as wn
from synset_graph import SynsetGraph


def baseline_decoder():
    synset = wn.synset('entity.n.01')   # @UndefinedVariable

    dic = {synset: 1}
    name = "baseline"
    test_graph = SynsetGraph(name, dic)
    test_graph.print_tree()
    return test_graph

if __name__ == '__main__':
    baseline_decoder()
