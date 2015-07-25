# -*- coding: utf-8 -*-
import re
from utilities import ConvertHebrewEnglish
from word2vec_utilities import Word2VecUtilities
from nltk.corpus import wordnet as wn


class WordnetUtilities:
    @staticmethod
    def get_word2vec_similar_synsets(word, number_of_synsets,
                                     vector_file_path, topn):
        # In case input is in English
        if not re.search('[a-zA-Z]', word):
            word = ConvertHebrewEnglish(word)

        w2cUtils = Word2VecUtilities()
        w2cUtils.load_vectors_from(vector_file_path)
        similar_words = w2cUtils.most_similar_to(word, topn=topn)

        all_synsets = dict()
        for similar_word in similar_words:
            if number_of_synsets < 1:
                break
            heb_word = ConvertHebrewEnglish(similar_word[0])

            word_synsets = wn.synsets(heb_word,  # @UndefinedVariable
                                      lang='heb')

            # Add known synsets to the sets
            if len(word_synsets) > 0:
                number_of_synsets -= 1
                for synset in word_synsets:
                    all_synsets[synset] = similar_word[1]
        return all_synsets