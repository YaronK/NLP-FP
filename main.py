# -*- coding: utf-8 -*-

from evaluation import Evaluation
from synset_graph import SynsetGraph
from wordnet import WordnetUtilities
from word2vec import Word2VecUtilities


def main():
    # word = input("Enter a Hebrew word:")
    # synsets_number = int(input("Enter the number of synsets:"))

    word = "חתול"
    number_of_synsets = 3

    vector_file_path = "vectors-g.bin"

    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    word2vec_synsets = \
        wnUtilities.get_word2vec_similar_synsets(word, number_of_synsets)
    if word2vec_synsets is None:
        print ("No word2vec similar synsets were found for {}\n".format(word))
        return

    test_graph = SynsetGraph("Test", word2vec_synsets)
    test_graph.print_tree()
    print ("-----------------------------")

    evaluate(word, test_graph, wnUtilities)


def evaluate(word, test_graph, wnUtilities):
    gold_synsets = wnUtilities.get_gold_synsets(word)
    if gold_synsets is None:
        print ("No wordnet synsets were found for {}\n".format(word))
        return

    gold_graph = SynsetGraph("Gold", gold_synsets)
    gold_graph.print_tree()
    print ("-----------------------------")

    result = Evaluation.evaluate(test_graph, gold_graph, False)
    print("Evaluate: {0:.3f}".format(result))

if __name__ == '__main__':
    main()
