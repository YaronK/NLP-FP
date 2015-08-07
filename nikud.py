# -*- coding: utf-8 -*-
from word2vec import Word2VecUtilities
from conversion import HebrewString


def _remove_puncutation(word):
    new_word = ""
    for letter in word:
        o = ord(letter)
        if o in range(1488, 1515) or o == 32 or o == 45:
            new_word += letter
    return new_word


def add_letter(word, letter, i):
    return word[0:i] + letter + word[i+1:len(word)]


def _get_removal_apporval(word, word_2_vec, i, letter):
    if i != len(word) and word[i - 1] != letter and word[i+1] != letter:
        new_word = add_letter(word, letter, i)
        new_word = _remove_puncutation(new_word)
        eng_letters = HebrewString(new_word)
        retriever = word_2_vec.build_retriever(eng_letters.eng_ltrs())

        return retriever.get(1) is not None


def check_punctuation(word, word_2_vec):
    hirik = "ִ"
    holam = "ֹ"
    koobotz = "ֻ"

    for i in range(0, len(word)):
        if word[i] == hirik:
            if _get_removal_apporval(word, word_2_vec, i, "י"):
                word = add_letter(word, "י", i)
                i -= 1
        if word[i] == holam:
            if _get_removal_apporval(word, word_2_vec, i, "ו"):
                word = add_letter(word, "ו", i)
                i -= 1
        if word[i] == koobotz:
            if _get_removal_apporval(word, word_2_vec, i, "ו"):
                word = add_letter(word, "ו", i)
                i -= 1

    return _remove_puncutation(word)


def main():
    word_2_vec = Word2VecUtilities()
    word_2_vec.load_vectors_from("vectors-g.bin")

    f = open(r"wn-data-heb-Original.tab", 'r',  encoding="utf8")
    text = ""

    for line in f:
        words = line.split()
        if words[1] == "lemma":
            for word in words[2:len(words)]:
                new_word = check_punctuation(word, word_2_vec)
                line = line.replace(word, new_word)
                line = line.replace(r"\r\n", r"\n")
        text += line

    f = open(r"wn-data-heb-BliNikud.tab", 'w',  encoding="utf8")
    f.write(text)


if __name__ == '__main__':
    main()
