# -*- coding: utf-8 -*-

from synset_graph import SynsetGraph
from wordnet import WordnetUtilities as WNUtils


def main():
    print("Please write an Hebrew word")
    # word = input()
    print("Enter number of wanted Synsets")
    # synsets_number = int(input())
    word = "כלב"
    number_of_synsets = 20

    # word2vec definitions
    vector_file_path = "vectors-g.bin"
    topn = 500

    word2vec_synsets = WNUtils.get_word2vec_similar_synsets(word,
                                                            number_of_synsets,
                                                            vector_file_path,
                                                            topn)
    if word2vec_synsets is None:
        return None
    test_graph = SynsetGraph(word2vec_synsets)

    gold_synsets = WNUtils.get_gold_synsets(word)
    if not gold_synsets:
        return None
    gold_graph = SynsetGraph(gold_synsets)

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
