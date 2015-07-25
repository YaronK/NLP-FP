# -*- coding: utf-8 -*-
import re

from nltk.corpus import wordnet as wn

from synset_graph import SynsetGraph
from utilities import ConvertHebrewEnglish


class GoldTree:
    def __init__(self, _word):
        self.word = _word
        self.synset_dict = {}
        self.synsets_number = 0

    def get_gold_tree(self):
        # Case input is in English
        if re.search('[a-zA-Z]', self.word):
            self.word = ConvertHebrewEnglish(self.word)

        synsets = wn.synsets(self.word,  # @UndefinedVariable
                             lang='heb')
        self.synsets_number = len(synsets)
        if self.synsets_number == 0:
            print("No real synset has been found")
        else:
            prob = 1 / self.synsets_number

            for synset in synsets:
                self.synset_dict[synset] = prob
            return SynsetGraph(self.synset_dict)
