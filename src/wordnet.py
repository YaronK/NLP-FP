# -*- coding: utf-8 -*-

from src.conversion import HebrewString
from src.translation import Translator

from nltk.corpus import wordnet


class WordnetUtilities:
    def __init__(self, word2vec_utilities):
        self.translator = Translator()
        self.word2vec = word2vec_utilities
        self.wordnet = wordnet

    def get_word2vec_similar_synsets(self, heb_word,
                                     number_of_required_synsets):
        heb_word = HebrewString(heb_word)
        retriever = self.word2vec.build_retriever(heb_word.eng_ltrs())

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

            suggestion_synsets = self._get_suggestion_synsets(suggestion)
            if len(suggestion_synsets) == 0:
                continue

            number_of_suggestion_synsets = min(len(suggestion_synsets),
                                               (number_of_required_synsets -
                                                len(similar_synsets)))
            while need_more_synsets() and len(suggestion_synsets) > 0:
                synset = suggestion_synsets.pop(0)
                if synset not in similar_synsets:
                    similar_synsets[synset] = (similarity /
                                               number_of_suggestion_synsets)

        return similar_synsets

    def _get_suggestion_synsets(self, suggestion):
        suggestion_synsets = self.wordnet.synsets(suggestion.heb_ltrs(),
                                                  lang='heb')
        if len(suggestion_synsets) != 0:
            print("Found {0} in Hebrew WN".format(suggestion.heb_ltrs()))
        else:
            print("Couldn't find {0} in Hebrew WN".
                  format(suggestion.heb_ltrs()))
            translated_text = \
                self.translator.translate(suggestion.heb_ltrs())
            if translated_text is None:
                print ("Couldn't translate {0}".format(suggestion.heb_ltrs()))
                return []
            print("Translated {0}".format(translated_text))
            suggestion_synsets = self.wordnet.synsets(translated_text)
            if len(suggestion_synsets) != 0:
                print("Found {0}({1}) in English WN".
                      format(suggestion.heb_ltrs(), translated_text))
            else:
                print("Couldn't find {0}({1}) in English WN".
                      format(suggestion.heb_ltrs(), translated_text))
        return suggestion_synsets

    def get_gold_synsets(self, heb_word):
        heb_word = HebrewString(heb_word)

        synsets = self.wordnet.synsets(heb_word.heb_ltrs(), lang='heb')
        synsets_number = len(synsets)
        # Case heb_word does not appear in Hebrew Wordnet
        if synsets_number == 0:
            ts = Translator()
            eng_word = ts.translate(heb_word)
            synsets = wordnet.synsets(eng_word)  # @UndefinedVariable
            synsets_number = len(synsets)
            if synsets_number == 0:
                print("No real Synset has been found")
                return None

        prob = 1 / float(synsets_number)
        synset_dict = dict()
        for synset in synsets:
            synset_dict[synset] = prob
        return synset_dict
