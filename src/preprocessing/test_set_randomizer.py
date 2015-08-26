# -*- coding: utf-8 -*-
"""
choose_random_words python script goes through the Hebrew wordnet,
and chooses random words to be evaluated

Input: Hebrew Wordnet
Output: x random words

"""
import random

from gensim.models import Word2Vec
from nltk.corpus import wordnet

from utilities.conversion import HebrewString


out_dir_path = "../../exps/"


def write_random_words_to_file(number_of_words, pos, lang):
    vector_file_path = "../../data/vectors-y.bin"
    weight_matrix = Word2Vec.load_word2vec_format(vector_file_path,
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

if __name__ == '__main__':
    write_random_words_to_file(10, wordnet.NOUN, "heb")
