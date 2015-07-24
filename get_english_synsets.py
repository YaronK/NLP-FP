# -*- coding: utf-8 -*-
'''
Created on 7 ביול 2015

@author: Gilad
'''

import re

from nltk.corpus import wordnet as wn
from gensim.models import Word2Vec

from change_letters import GetLetters


class EnglishSynsets:
    def __init__(self, _word, _synsets_number):
        # Initialize
        self.word = _word
        self.synsets_number = int(_synsets_number)

        self.all_synsets = {}
        self.vectors_path = "vectors-g.bin"
        self.top_n = 500

    def get_synsets(self, similar_words):
        for similar_word in similar_words:
            if self.synsets_number < 1:
                break
            heb_word = GetLetters(similar_word[0])

            # Get Synsets
            word_synsets = wn.synsets(heb_word, lang='heb')

            # Add known synsets to the sets
            if len(word_synsets) > 0:
                self.synsets_number -= 1
                for synset in word_synsets:
                    self.all_synsets[synset] = similar_word[1]

    def word_2_vec(self):
        # Get word2vec model
        print("Starting Word2Vec Learning...")
        model = Word2Vec.load_word2vec_format(self.vectors_path, binary=True)

        return model.most_similar(self.word, topn=self.top_n)

    def get_english_synsets(self):
        # Case input is in English
        if not re.search('[a-zA-Z]', self.word):
            self.word = GetLetters(self.word)

        # Get n most similar words
        similar_words = self.word_2_vec()

        # Get and return all Synsets
        self.get_synsets(similar_words)

        return self.all_synsets
