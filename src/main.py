# -*- coding: utf-8 -*-

from src.evaluation import Evaluation
from src.synset_graph_extension import SynsetGraphExtension as SGE
from src.wordnet import WordnetUtilities
from src.word2vec import Word2VecUtilities


def main():
    # word = input("Enter a Hebrew word:")
    # synsets_number = int(input("Enter the number of synsets:"))
    # decode_baseline = (input("Use Baseline? (True/False:")
    # thinning_method = (input("Use thinning Method? (True/None:")

    word = "חתול"
    number_of_synsets = 3
    vector_file_path = "../data/vectors-g.bin"
    thinning_method = None  # SGE.thin_out_graph_by_paths
    # thinning_method = SGE.thin_out_graph_by_paths

    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    test_graph = SGE.build_word2vec_graph(word, number_of_synsets, wnUtilities)
    print_graph(test_graph)

    baseline_graph = SGE.build_baseline_graph()
    print_graph(baseline_graph)

    gold_graph = SGE.build_gold_graph(word, wnUtilities)
    print_graph(gold_graph)

    evaluate(baseline_graph, gold_graph, thinning_method)
    evaluate(test_graph, gold_graph, thinning_method)


def evaluate(decoded_graph, gold_graph, thinning_method):
    result = Evaluation.evaluate(decoded_graph, gold_graph,
                                 thinning_method)
    print("Evaluate: {0:.3f}".format(result))


def print_graph(graph):
    graph.print_tree()
    print ("-----------------------------")

if __name__ == '__main__':
    main()
