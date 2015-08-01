# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET


class Translator:
    def __init__(self):
        self.key = ("trnsl.1.1.20150725T135336Z.2f8c11" +
                    "7c58a19f6b.083ef7509a10f15ab51d34fe1fc912dd43978374")

    def translate(self, word):
        self.url = ("https://translate.yandex.net/api/v1.5/tr/translate?" +
                    "key={0}&lang=he-en&text={1}".format(self.key, word))
        try:
            response = requests.get(self.url)
        except Exception:
            print("No internet connection found")
            return ""
        tree = ET.fromstring(response.text)
        return tree.find("text").text
