# -*- coding: utf-8 -*-

from evaluation import Evaluation
from synset_graph import SynsetGraph
from wordnet import WordnetUtilities as WNUtils
from word2vec import Word2VecUtilities


def main():
    # word = input("Enter a Hebrew word:")
    # synsets_number = int(input("Enter the number of synsets:"))

    word = "כלב"
    number_of_synsets = 3

    # word2vec definitions
    vector_file_path = "vectors-g.bin"
    topn = 500

    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    word2vec_synsets = WNUtils.get_word2vec_similar_synsets(word,
                                                            number_of_synsets,
                                                            w2vUtilities,
                                                            topn)
    if word2vec_synsets is None:
        return

    test_graph = SynsetGraph(word2vec_synsets)

    gold_synsets = WNUtils.get_gold_synsets(word)
    if gold_synsets is not None:
        gold_graph = SynsetGraph(gold_synsets)
        result = Evaluation.evaluate(test_graph, gold_graph)
        print("Evaluate: {0:.3f}".format(result))
        print("")
        gold_graph.print_tree()

    print("")
    test_graph.print_tree()


if __name__ == '__main__':
    main()
