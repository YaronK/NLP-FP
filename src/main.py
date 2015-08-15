# -*- coding: utf-8 -*-

from src.evaluation import SynsetGraphComarison
from src.synset_graph_extension import SynsetGraphExtension as SGE
from src.wordnet import WordnetUtilities
from src.word2vec import Word2VecUtilities
from src.preprocessing.choose_random_words import choose_random_words


def main():
    # word = input("Enter a Hebrew word:")
    # synsets_number = int(input("Enter the number of synsets:"))
    # decode_baseline = (input("Use Baseline? (True/False:")
    # thinning_method = (input("Use thinning Method? (True/None:")

    # chosen_words = choose_random_words(10, "../data/wn-data-heb-BliNikud.tab")
    chosen_words = ["אוביקט"]
    number_of_synsets = 20
    vector_file_path = "../data/vectors-g.bin"

    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    for word in chosen_words:
        print(word)
        decoded_graph = SGE.build_word2vec_graph(word, number_of_synsets,
                                                 wnUtilities)

        decoded_graph.dump_to_file("{}-{}-{}.txt".format(word, "decoded",
                                                         number_of_synsets))

        baseline_graph = SGE.build_baseline_graph()
        baseline_graph.dump_to_file("{}-{}.txt".format(word, "baseline"))

        gold_graph = SGE.build_gold_graph(word, wnUtilities)
        baseline_graph.dump_to_file("{}-{}.txt".format(word, "gold"))

        comparison = SynsetGraphComarison(baseline_graph, decoded_graph,
                                          gold_graph)
        comparison.compare_using_all_methods()
        comparison.dump_to_file("{}-{}.txt".format(word, number_of_synsets))


if __name__ == '__main__':
    main()
