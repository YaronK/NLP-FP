# -*- coding: utf-8 -*-
'''
Created on 7 ביול 2015

@author: Gilad
'''


def Get_Letters(word, lang):
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

        if lang == "heb":
            for letter in word:
                word = word.replace(letter, heb_eng_dict[letter])
        else:
            for letter in word[:-1]:
                word = word.replace(letter, eng_heb_dict[letter])
            fin_letter = word[len(word)-1]
            try:
                word = word.replace(fin_letter, eng_heb_dict_fin[fin_letter])
            except Exception:
                # Word not in dictionary
                return word

        return word
