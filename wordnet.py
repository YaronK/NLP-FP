# -*- coding: utf-8 -*-
import re
from conversion import ConvertHebrewEnglish
from word2vec import Word2VecUtilities
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
        if similar_words is None:
            return None
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

    @staticmethod
    def get_gold_synsets(word):
        # In case input is in English
        if re.search('[a-zA-Z]', word):
            word = ConvertHebrewEnglish(word)

        synsets = wn.synsets(word,  # @UndefinedVariable
                             lang='heb')
        synsets_number = len(synsets)
        if synsets_number == 0:
            print("No real synset has been found")
            return None
        else:
            prob = 1 / float(synsets_number)
            synset_dict = dict()
            for synset in synsets:
                synset_dict[synset] = prob
            return synset_dict
