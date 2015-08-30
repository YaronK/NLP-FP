# -*- coding: utf-8 -*-
import os.path
import pickle

import requests

from utilities.transliteration import HebrewString
import xml.etree.ElementTree as ET


class Translator:
    key = ("trnsl.1.1.20150725T135336Z.2f8c117c58a19f6" +
           "b.083ef7509a10f15ab51d34fe1fc912dd43978374")
    local_dictionary_file_name = "local_dictionary.bin"

    def __init__(self):
        if (os.path.isfile(Translator.local_dictionary_file_name)):
            with open(Translator.local_dictionary_file_name, 'rb') as file:
                self.local_dictionary = pickle.load(file, encoding='utf-8')
        else:
            self.local_dictionary = {}

    def __del__(self):
        with open(Translator.local_dictionary_file_name, 'wb') as file:
            pickle.dump(self.local_dictionary, file)

    def translate(self, heb_word):
        if heb_word in self.local_dictionary:
            return self.local_dictionary[heb_word]
        self.url = ("https://translate.yandex.net/api/v1.5/tr/translate?" +
                    "key={0}&lang=he-en&text={1}".format(Translator.key,
                                                         heb_word))
        try:
            response = requests.get(self.url)
        except Exception as exception:
            print(exception)
            raise

        tree = ET.fromstring(response.text)
        translation = tree.find("text").text

        if HebrewString(translation).heb_ltrs() == translation:
            return None
        if heb_word not in self.local_dictionary:
            self.local_dictionary[heb_word] = translation
        return translation
