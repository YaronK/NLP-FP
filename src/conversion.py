# -*- coding: utf-8 -*-


class HebrewString(str):
    heb_eng_dict = {"א": "a", "ב": "b", "ג": "g", "ד": "d",
                    "ה": "h", "ו": "w", "ז": "z", "ח": "x",
                    "ט": "v", "י": "i", "כ": "k", "ל": "l",
                    "מ": "m", "נ": "n", "ס": "s", "ע": "y",
                    "פ": "p", "צ": "c", "ק": "q", "ר": "r",
                    "ש": "e", "ת": "t", "ם": "m", "ן": "n",
                    "ץ": "c", "ך": "k", "ף": "p"}

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

    def eng_ltrs(self):
        if not hasattr(self, "_english_letters"):
            _english_letters = \
                HebrewString._replace_all(self, HebrewString.heb_eng_dict)
        return _english_letters

    def heb_ltrs(self):
        if not hasattr(self, "_english_letters"):
            start = HebrewString._replace_all(self[:-1],
                                              HebrewString.eng_heb_dict)
            end = HebrewString._replace_all(self[-1],
                                            HebrewString.eng_heb_dict_fin)
            _hebrew_letters = start + end
        return _hebrew_letters

    @staticmethod
    def _replace_all(word, dic):
        for i, j in dic.items():
            word = word.replace(i, j)
        return word
