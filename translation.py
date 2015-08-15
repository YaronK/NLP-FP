# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
from conversion import HebrewString


class Translator:
    key = ("trnsl.1.1.20150725T135336Z.2f8c117c58a19f6" +
           "b.083ef7509a10f15ab51d34fe1fc912dd43978374")

    # TODO:  implement cache - which is saved/loaded from/to disk.

    def translate(self, heb_word):
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
        return translation
