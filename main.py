# -*- coding: utf-8 -*-

from evaluation import Evaluation
from synset_graph import SynsetGraph
from wordnet import WordnetUtilities as WNUtils
from word2vec import Word2VecUtilities


def main():
    # word = input("Enter a Hebrew word:")
    # synsets_number = int(input("Enter the number of synsets:"))

    word = "חתול"
    number_of_synsets = 20

    vector_file_path = "vectors-g.bin"

    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    word2vec_synsets = WNUtils.get_word2vec_similar_synsets(word,
                                                            number_of_synsets,
                                                            w2vUtilities)
    if word2vec_synsets is None:
        print ("No word2vec similar synsets were found for {}\n".format(word))
        return

    test_graph = SynsetGraph(word2vec_synsets)
    print ("\nTEST:")
    test_graph.print_tree()
    print ("")

    gold_synsets = WNUtils.get_gold_synsets(word)
    if gold_synsets is None:
        print ("No wordnet synsets were found for {}\n".format(word))
        return

    gold_graph = SynsetGraph(gold_synsets)
    print ("\nGOLD:")
    gold_graph.print_tree()
    print ("")

    result = Evaluation.evaluate(test_graph, gold_graph, False)
    print("Evaluate: {0:.3f}".format(result))

if __name__ == '__main__':
    main()
