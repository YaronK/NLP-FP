# -*- coding: utf-8 -*-
'''
Created on 7 ביול 2015

@author: Gilad
'''

from nltk.corpus import wordnet as wn
from gensim.models import Word2Vec

import change_letters


class EnglishSynsets:
    def __init__(self, _word, _synsets_number):
        # Initialize
        self.word = _word
        self.synsets_number = int(_synsets_number)
        self.all_synsets = {}
        self.vectors_path = "vectors-g.bin"
        self.top_n = 500

    def get_synsets(self, similar_words):
        synsets_counter = 0
        for word in similar_words:
            if synsets_counter >= self.synsets_number:
                break
            heb_word = change_letters.GetLetters(word[0], False)

            # Get Synsets
            word_synsets = wn.synsets(heb_word, lang='heb')

            # Add known synsets to the sets
            if len(word_synsets) > 0:
                synsets_counter += 1
                for synset in word_synsets:
                    self.all_synsets[synset] = word[1]

    def word_2_vec(self, heb_word):
        # Get word2vec model
        print("Starting Word2Vec Learning...")
        model = Word2Vec.load_word2vec_format(self.vectors_path, binary=True)

        return model.most_similar(heb_word, topn=self.top_n)

    def get_english_synsets(self):
        heb_word = change_letters.GetLetters(self.word, True)

        # Get n most similar words
        self.synsets_number = self.synsets_number
        similar_words = self.word_2_vec(heb_word)

        # Get and return all Synsets
        self.get_synsets(similar_words)

        return self.all_synsets
