# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET


class Translator:
    key = ("trnsl.1.1.20150725T135336Z.2f8c117c58a19f6" +
           "b.083ef7509a10f15ab51d34fe1fc912dd43978374")

    # TODO:  implement cache - which is saved/loaded from/to disk.

    def translate(self, word):
        self.url = ("https://translate.yandex.net/api/v1.5/tr/translate?" +
                    "key={0}&lang=he-en&text={1}".format(Translator.key, word))
        try:
            response = requests.get(self.url)
        except Exception as exception:
            print(exception)
            raise
        # TODO:  handle case where word is not found in the dictionary
        #        separately
        tree = ET.fromstring(response.text)
        return tree.find("text").text
