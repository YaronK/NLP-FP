# -*- coding: utf-8 -*-
import re
from conversion import ConvertHebrewEnglish
from word2vec import Word2VecUtilities
from translation import Translator

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
                for synset in word_synsets:
                    number_of_synsets -= 1
                    all_synsets[synset] = similar_word[1]
                    if number_of_synsets < 1:
                        break
            # Case Hebrew word not appear in Wordnet
            else:
                ts = Translator()
                eng_word = ts.translate(heb_word)
                word_synsets = wn.synsets(eng_word)  # @UndefinedVariable
                if len(word_synsets) > 0:
                    for synset in word_synsets:
                        number_of_synsets -= 1
                        all_synsets[synset] = similar_word[1]
                        if number_of_synsets < 1:
                            break

        return all_synsets

    @staticmethod
    def get_gold_synsets(word):
        # In case input is in English
        if re.search('[a-zA-Z]', word):
            word = ConvertHebrewEnglish(word)

        synsets = wn.synsets(word,  # @UndefinedVariable
                             lang='heb')
        synsets_number = len(synsets)
        # Case word does not appear in Hebrew Wordnet
        if synsets_number == 0:
            ts = Translator()
            eng_word = ts.translate(word)
            synsets = wn.synsets(eng_word)  # @UndefinedVariable
            synsets_number = len(synsets)
            if synsets_number == 0:
                print("No real Synset has been found")
                return None

        prob = 1 / float(synsets_number)
        synset_dict = dict()
        for synset in synsets:
            synset_dict[synset] = prob
        return synset_dict
