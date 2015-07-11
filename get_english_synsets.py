# -*- coding: utf-8 -*-
'''
Created on 7 ביול 2015

@author: Gilad
'''
from nltk.corpus import wordnet as wn
from gensim.models import Word2Vec

import change_letters


def get_synsets(similar_words, top_n):
    # Initialize
    all_synsets = {}
    synsets_counter = 0

    for word in similar_words:
        if synsets_counter <= top_n:
            try:
                heb_word = change_letters.Get_Letters(word[0], "eng")
            except Exception:
                # Probably an English word in the corpora
                continue
            # Get synsets
            word_synsets = wn.synsets(heb_word, lang='heb')

            # Add known synsets to the sets
            if len(word_synsets) > 0:
                synsets_counter += 1
                for synset in word_synsets:
                    all_synsets[synset] = word[1]
                print("{0} ({1}), Is {2:.3f} similar. Synsets are: {3}"
                      .format(word[0], heb_word, word[1], word_synsets))

    return all_synsets


def word_2_vec(heb_word):
    vectors_path = "vectors-g.bin"

    # Get word2vec model
    print("Starting Word2Vec Learning...")
    model = Word2Vec.load_word2vec_format(vectors_path, binary=True)

    return get_similar_word(model, heb_word)


def get_similar_word(model, heb_word):
    top_n = int(input("Please Enter number of wanted synsets\n"))

    print("Computing {0} most similar synsets".format(top_n, heb_word))

    # Get 500 most similar words for given input
    similar_words = model.most_similar(heb_word, topn=500)

    return similar_words, top_n


def main():
    heb_word = input("Please Write an Hebrew word, In Hebrew characters\n")
    heb_word = change_letters.Get_Letters(heb_word, "heb")

    similar_words, top_n = word_2_vec(heb_word)

    all_synsets = get_synsets(similar_words, top_n)
    # TODO: Call Yarons Method


if __name__ == '__main__':
    main()
