# -*- coding: utf-8 -*-
import urllib.request


class Translator:
    def __init__(self, _word):
        self.key = ("trnsl.1.1.20150725T135336Z.2f8c11" +
                    "7c58a19f6b.083ef7509a10f15ab51d34fe1fc912dd43978374")
        self.word = _word

        self.web = ("https://translate.yandex.net/api/v1.5/tr/translate?" +
                    "key={0}&lang=he-en&text={1}".format(self.word, self.key))

    def translate(self):
        print(self.web)
        request = urllib.request.urlopen(self.web).read()
        print(request)

if __name__ == '__main__':
    ts = Translator("ניסיון")
    ts.translate()
