# -*- coding: utf-8 -*-

from evaluation import Evaluation
from synset_graph import SynsetGraph
from synset_graph_extension import SynsetGraphExtension as SGE
from wordnet import WordnetUtilities
from word2vec import Word2VecUtilities
from decode_baseline import baseline_decoder


def decode(word, number_of_synsets, vector_file_path, baseline):
    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    if baseline:
        test_graph = baseline_decoder()
    else:
        word2vec_synsets = \
            wnUtilities.get_word2vec_similar_synsets(word, number_of_synsets)
        if word2vec_synsets is None:
            print ("No word2vec similar synsets for {}\n".format(word))
            return

        test_graph = SynsetGraph("Test", word2vec_synsets)
        test_graph.print_tree()
    return test_graph, wnUtilities


def main():
    # word = input("Enter a Hebrew word:")
    # synsets_number = int(input("Enter the number of synsets:"))
    # decode_baseline = (input("Use Baseline? (True/False:")

    word = "חתול"
    number_of_synsets = 3
    vector_file_path = "vectors-g.bin"
    baseline = True

    test_graph, wnUtilities = decode(word, number_of_synsets,
                                     vector_file_path, baseline)

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

    result = Evaluation.evaluate(test_graph, gold_graph,
                                 SGE.thin_out_graph_by_paths)
    print("Evaluate: {0:.3f}".format(result))

if __name__ == '__main__':
    main()
