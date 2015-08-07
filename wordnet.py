# -*- coding: utf-8 -*-

from conversion import HebrewString
from translation import Translator

from nltk.corpus import wordnet as wn


class WordnetUtilities:

    @staticmethod
    def get_word2vec_similar_synsets(heb_word,
                                     number_of_required_synsets,
                                     word2vec_utilities):
        heb_word = HebrewString(heb_word)
        translator = Translator()
        retriever = word2vec_utilities.build_retriever(heb_word.eng_ltrs())

        word2vec_suggestions = retriever.get(number_of_required_synsets)
        if word2vec_suggestions is None:
            return None

        similar_synsets = dict()

        def need_more_synsets():
            return len(similar_synsets) < number_of_required_synsets

        while need_more_synsets():
            if len(word2vec_suggestions) == 0:
                word2vec_suggestions = retriever.get_more()

            suggestion, similarity = word2vec_suggestions.pop(0)
            suggestion = HebrewString(suggestion)

            if heb_word.eng_ltrs() in suggestion.eng_ltrs():
                print("Passed over {0}".format(suggestion.heb_ltrs()))
                continue

            suggestion_synsets = wn.synsets(  # @UndefinedVariable
                suggestion.heb_ltrs(), lang='heb')

            if len(suggestion_synsets) != 0:
                print("Found {0} in Hebrew WN".format(suggestion.heb_ltrs()))
            else:
                print("Couldn't find {0} in Hebrew WN".
                      format(suggestion.heb_ltrs()))
                translated_text = translator.translate(suggestion.heb_ltrs())
                if translated_text is None:
                    continue

                suggestion_synsets = \
                    wn.synsets(translated_text)  # @UndefinedVariable
                if len(suggestion_synsets) != 0:
                    print("Found {0}({1}) in English WN".
                          format(suggestion.heb_ltrs(), translated_text))
                else:
                    print("Couldn't find {0}({1}) in English WN".
                          format(suggestion.heb_ltrs(), translated_text))

            number_of_suggestion_synsets = min(len(suggestion_synsets),
                                               (number_of_required_synsets -
                                                len(similar_synsets)))
            while need_more_synsets() and len(suggestion_synsets) > 0:
                synset = suggestion_synsets.pop(0)
                if synset not in similar_synsets:
                    similar_synsets[synset] = (similarity /
                                               number_of_suggestion_synsets)

        return similar_synsets

    @staticmethod
    def get_gold_synsets(heb_word):
        heb_word = HebrewString(heb_word)

        synsets = wn.synsets(heb_word.heb_ltrs(),  # @UndefinedVariable
                             lang='heb')
        synsets_number = len(synsets)
        # Case heb_word does not appear in Hebrew Wordnet
        if synsets_number == 0:
            ts = Translator()
            eng_word = ts.translate(heb_word)
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
