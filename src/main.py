# -*- coding: utf-8 -*-

from decoding import Decoding
from evaluation import Evaluation
from utilities.word2vec import Word2VecUtilities
from utilities.wordnet import WordnetUtilities


def main():
    # word = input("Enter a Hebrew word:")
    # synsets_number = int(input("Enter the number of synsets:"))
    # decode_baseline = (input("Use Baseline? (True/False:")
    # thinning_method = (input("Use thinning Method? (True/None:")

    # chosen_words = choose_random_words(10, "../data/wn-data-heb-BliNikud.tab")
    number_of_synsets = 5
    vector_file_path = "../data/vectors-y.bin"

    w2vUtilities = Word2VecUtilities()
    w2vUtilities.load_vectors_from(vector_file_path)
    wnUtilities = WordnetUtilities(w2vUtilities)

    decoding = Decoding(wnUtilities)
    word_to_decoded_graph_dict = decoding.decode(number_of_synsets,
                                                 "../exps/heb_n_10.words")
    evaluation = Evaluation(wnUtilities)
    _, category_results = \
        evaluation.evaluate(number_of_synsets, word_to_decoded_graph_dict)

    print(category_results)


if __name__ == '__main__':
    main()
