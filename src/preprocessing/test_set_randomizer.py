# -*- coding: utf-8 -*-
"""
Randomly chooses words for the test sets.
Chooses words which exists both in the w2v vocabulary and
in the Hebrew WN.
"""
import random

from gensim.models import Word2Vec
from nltk.corpus import wordnet

from utilities.transliteration import HebrewString


def write_random_words_to_file(number_of_words, pos, lang,
                               w2v_vector_file_path, out_dir_path):

    weight_matrix = Word2Vec.load_word2vec_format(w2v_vector_file_path,
                                                  binary=True)
    w2v_heb_words = {HebrewString(word).heb_ltrs()
                     for word in weight_matrix.vocab}

    wn_heb_words = set(wordnet.all_lemma_names  # @UndefinedVariable
                       (pos=pos, lang=lang))

    possible_heb_words = w2v_heb_words & wn_heb_words

    sampled_heb_words = random.sample(possible_heb_words, number_of_words)
    out_path = out_dir_path + "{}_{}_{}.words".format(lang, pos,
                                                      number_of_words)
    with open(out_path, 'w', newline="\n", encoding="utf8") as out_file:
        for noun in sampled_heb_words:
            out_file.write(noun + "\n")
    return out_path


def pos_to_wordnets(argument):
    return {
        1: wordnet.ADJ,
        2: wordnet.ADJ_SAT,
        3: wordnet.ADV,
        4: wordnet.NOUN,
        5: wordnet.VERB,
    }.get(int(argument), None)


if __name__ == '__main__':
    # w2v_vector_file_path = "../../data/vectors-y.bin"
    # out_dir_path = "../../exps/"
    w2v_vector_file_path = input("Please enter vector file path\n")
    out_dir_path = input("\nPlease enter destination directory\n")
    numb_of_words = int(input("\nPlease enter the number of random words\n"))

    print("\nPlease enter the number of the POS:")
    pos = input("[ADJ, ADJ_SAT, ADV, NOUN, VERB]: [1,2,3,4,5]\n")
    pos = pos_to_wordnets(pos)

    lang = input("\nPlease enter required language (heb for Hebrew)\n")

    try:
        write_random_words_to_file(numb_of_words, pos,
                                   lang, w2v_vector_file_path,
                                   out_dir_path)
    except:
        print("One of the inputs is incorrect, please try again")
