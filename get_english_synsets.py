# -*- coding: utf-8 -*-

import re

from nltk.corpus import wordnet as wn

from utilities import ConvertHebrewEnglish
from word2vec_utilities import Word2VecUtilities


class EnglishSynsets:
    def __init__(self, _word, _synsets_number):
        self.word = _word
        self.synsets_number = int(_synsets_number)

        self.all_synsets = {}
        self.vectors_path = "vectors-g.bin"
        self.top_n = 500

    def get_synsets(self, similar_words):
        for similar_word in similar_words:
            if self.synsets_number < 1:
                break
            heb_word = ConvertHebrewEnglish(similar_word[0])

            word_synsets = wn.synsets(heb_word,  # @UndefinedVariable
                                      lang='heb')

            # Add known synsets to the sets
            if len(word_synsets) > 0:
                self.synsets_number -= 1
                for synset in word_synsets:
                    self.all_synsets[synset] = similar_word[1]

    def get_english_synsets(self):
        # Case input is in English
        if not re.search('[a-zA-Z]', self.word):
            self.word = ConvertHebrewEnglish(self.word)

        # Get n most similar words
        w2cUtils = Word2VecUtilities()
        w2cUtils.load_vectors_from(self.vectors_path)
        similar_words = w2cUtils.most_similar_to(self.word, self.top_n)

        # Get and return all Synsets
        self.get_synsets(similar_words)

        return self.all_synsets
