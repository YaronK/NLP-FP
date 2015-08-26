# -*- coding: utf-8 -*-
"""
Modifies a tab file for our application's needs.

1. Removes punctuation (Niqqud), converting text to Ktiv Male.
2. Keeps only 'lemma' lines, since 'def' lines caused problems
for nltk and not necessary for our application.

Input: A Hebrew tab file path
Output: A modified Hebrew tab file
"""
from utilities.conversion import HebrewString
from utilities.word2vec import Word2VecUtilities


def _check_validity_letter(order):
    return order in range(1488, 1515) or order == 32 or order == 45


def _remove_puncutation(word):
    new_word = ""
    for letter in word:
        letter_order = ord(letter)

        if _check_validity_letter(letter_order):
            new_word += letter
    return new_word


def _add_letter(word, letter, i):
    return word[0:i] + letter + word[i+1:len(word)]


def _get_removal_apporval(word, word_2_vec, i, letter):
    if i != len(word) and word[i - 1] != letter and word[i+1] != letter:
        new_word = _add_letter(word, letter, i)
        new_word = _remove_puncutation(new_word)
        eng_letters = HebrewString(new_word)
        retriever = word_2_vec.build_retriever(eng_letters.eng_ltrs())

        return retriever.get(1) is not None


def _remove_punctuation(word, word_2_vec):
    hirik = "ִ"
    holam = "ֹ"
    koobotz = "ֻ"

    for i in range(len(word)):
        if word[i] == hirik:
            if _get_removal_apporval(word, word_2_vec, i, "י"):
                word = _add_letter(word, "י", i)
                i -= 1
        if word[i] == holam:
            if _get_removal_apporval(word, word_2_vec, i, "ו"):
                word = _add_letter(word, "ו", i)
                i -= 1
        if word[i] == koobotz:
            if _get_removal_apporval(word, word_2_vec, i, "ו"):
                word = _add_letter(word, "ו", i)
                i -= 1

    return _remove_puncutation(word)


def main():
    w2v_vectors_file_path = "../../data/vectors-y.bin"
    original_file_path = "../../data/wn-data-heb.tab.original_file"
    new_file_path = "../../data/wn-data-heb.tab"

    w2v_utilities = Word2VecUtilities()
    w2v_utilities.load_vectors_from(w2v_vectors_file_path)

    with open(original_file_path, encoding="utf8") as original_file:
        with open(new_file_path, 'w', encoding="utf8",
                  newline="\n") as new_file:
            for line in original_file:
                words = line.split()
                if words[1] == "lemma":
                    for word in words[2:len(words)]:
                        new_word = _remove_punctuation(word, w2v_utilities)
                        line = line.replace(word, new_word, 1)
                    new_file.write(line)

if __name__ == '__main__':
    main()
