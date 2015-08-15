# -*- coding: utf-8 -*-

from src.evaluation import SynsetGraphComarison
from src.synset_graph_extension import SynsetGraphExtension as SGE
from src.wordnet import WordnetUtilities
from src.word2vec import Word2VecUtilities
from src.preprocessing.choose_random_words import main as cs


def main():
    # word = input("Enter a Hebrew word:")
    # synsets_number = int(input("Enter the number of synsets:"))
    # decode_baseline = (input("Use Baseline? (True/False:")
    # thinning_method = (input("Use thinning Method? (True/None:")

    # chosen_words = cs()
    chosen_words = ["חתול", "כלב"]
    number_of_synsets = 20
    vector_file_path = "../data/vectors-g.bin"

    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    for word in chosen_words:
        test_graph = SGE.build_word2vec_graph(word, number_of_synsets,
                                              wnUtilities)
        # print (test_graph.display())

        baseline_graph = SGE.build_baseline_graph()
        # print (baseline_graph.display())

        gold_graph = SGE.build_gold_graph(word, wnUtilities)
        # print (gold_graph.display())

        comparison = SynsetGraphComarison(baseline_graph, test_graph,
                                          gold_graph)
        comparison.compare_using_all_methods()
        comparison.dump_to_file("{}-{}.txt".format(word, number_of_synsets))


if __name__ == '__main__':
    main()
