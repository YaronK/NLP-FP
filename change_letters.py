# -*- coding: utf-8 -*-
'''
Created on 7 ביול 2015

@author: Gilad
'''
import re


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def GetLetters(word, input_word):
    eng_heb_dict = {"a": "א", "b": "ב", "g": "ג", "d": "ד",
                    "h": "ה", "w": "ו", "z": "ז", "x": "ח",
                    "v": "ט", "i": "י", "k": "כ", "l": "ל",
                    "m": "מ", "n": "נ", "s": "ס", "y": "ע",
                    "p": "פ", "c": "צ", "q": "ק", "r": "ר",
                    "e": "ש", "t": "ת"}

    eng_heb_dict_fin = {"a": "א", "b": "ב", "g": "ג", "d": "ד",
                        "h": "ה", "w": "ו", "z": "ז", "x": "ח",
                        "v": "ט", "i": "י", "l": "ל", "s": "ס",
                        "y": "ע", "q": "ק", "r": "ר", "e": "ש",
                        "t": "ת", "m": "ם", "n": "ן", "c": "ץ",
                        "k": "ך", "p": "ף"}

    heb_eng_dict = {"א": "a", "ב": "b", "ג": "g", "ד": "d",
                    "ה": "h", "ו": "w", "ז": "z", "ח": "x",
                    "ט": "v", "י": "i", "כ": "k", "ל": "l",
                    "מ": "m", "נ": "n", "ס": "s", "ע": "y",
                    "פ": "p", "צ": "c", "ק": "q", "ר": "r",
                    "ש": "e", "ת": "t", "ם": "m", "ן": "n",
                    "ץ": "c", "ך": "k", "ף": "p"}

    if re.search('[a-zA-Z]', word):
        # Case input word is already in English
        if input_word:
            return word
        # Handle final letter in Hebrew
        word_start = replace_all(word[:-1], eng_heb_dict)
        word_final = replace_all(word[len(word) - 1], eng_heb_dict_fin)
        word = word_start + word_final
    else:
        # Translate from Hebrew to "Jibrish"
        word = replace_all(word, heb_eng_dict)
    return word
