# -*- coding: utf-8 -*-
'''
Created on 7 ביול 2015

@author: Gilad
'''
import re

from nltk.corpus import wordnet as wn

from scorer import SynsetGraph
from change_letters import GetLetters


class GoldTree:
    def __init__(self, _word):
        self.word = _word
        self.synset_dict = {}
        self.synsets_number = 0

    def get_gold_tree(self):
        # Case input is in English
        if re.search('[a-zA-Z]', self.word):
            self.word = GetLetters(self.word)

        synsets = wn.synsets(self.word, lang='heb')
        self.synsets_number = len(synsets)
        prob = 1 / self.synsets_number

        for synset in synsets:
            self.synset_dict[synset] = prob
        return SynsetGraph(self.synset_dict)
