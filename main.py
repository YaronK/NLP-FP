# -*- coding: utf-8 -*-

from get_english_synsets import EnglishSynsets
from synset_graph import SynsetGraph
from create_gold_tree import GoldTree


def main():
    print("Please write an Hebrew word")
    # word = input()
    print("Enter number of wanted Synsets")
    # synsets_number = input()
    word = "חתול"
    synsets_number = "10"

    es = EnglishSynsets(word, synsets_number)
    all_synets = es.get_english_synsets()

    test_graph = SynsetGraph(all_synets)
    gold_graph = GoldTree(word).get_gold_tree()

    print("")
    print("len(node.hypernym_nodes) > 1:")
    for node in test_graph.synset_nodes.values():
        if len(node.hypernym_nodes) > 1:
            print(node)

    print("")
    print("len(node.hyponym_nodes) > 1:")
    for node in test_graph.synset_nodes.values():
        if len(node.hyponym_nodes) > 1:
            print(node)

    print("")
    test_graph.print_tree()
    gold_graph.print_tree()

if __name__ == '__main__':
    main()
