# -*- coding: utf-8 -*-
'''
Created on 7 ביול 2015

@author: Gilad
'''
from nltk.corpus import wordnet as wn
from gensim.models import Word2Vec

import change_letters


class get_english_synsets:
    def get_synsets(self, similar_words, synsets_number):
        # Initialize
        all_synsets = {}
        synsets_counter = 0

        for word in similar_words:
            if synsets_counter < synsets_number:
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

    def word_2_vec(self, heb_word, synsets_number):
        vectors_path = "vectors-g.bin"

        # Get word2vec model
        print("Starting Word2Vec Learning...")
        model = Word2Vec.load_word2vec_format(vectors_path, binary=True)

        return model.most_similar(heb_word, topn=500)


def main():
    es = get_english_synsets()

    heb_word = input("Please Write an Hebrew word, In Hebrew characters\n")
    eng_word = change_letters.Get_Letters(heb_word, "heb")

    synset_number = int(input("Please Enter number of wanted synsets\n"))
    similar_words = es.word_2_vec(eng_word, synset_number)

    print("Synsets for: {0}".format(heb_word))
    all_synsets = es.get_synsets(similar_words, synset_number)
    # TODO: Call Yarons Method


if __name__ == '__main__':
    main()