# -*- coding: utf-8 -*-
from nltk.corpus import wordnet as wn
from synset_graph import SynsetGraph


def main():
    synset = wn.synset('entity.n.01')   # @UndefinedVariable
    childs = synset.hyponyms()
    flag = True

    while(flag):
        synset = childs[0]
        childs = synset.hyponyms()
        if len(childs) != 0:
            synset = childs[0]
            childs = synset.hyponyms()
        else:
            flag = False

    gold_graph = SynsetGraph(synset)
    gold_graph.print_tree()

if __name__ == '__main__':
    main()
