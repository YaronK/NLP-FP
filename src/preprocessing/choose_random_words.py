# coding: utf-8
"""
choose_random_words python script goes through the Hebrew wordnet,
and chooses random words to be evaluated

Input: Hebrew Wordnet
Output: x random words

"""
import random


def choose_random_words(number_of_words, wn_path):
    heb_wn = open(wn_path, 'r', encoding="utf8")
    chosen_words = list()

    for line in heb_wn:
        if number_of_words > 0:
            words = line.split()
            if words[1] == "lemma" and len(words) < 4:
                choice = random.choice([True, False])
                if choice:
                    number_of_words -= 1
                    try:
                        chosen_words.append(words[2])
                    except:
                        pass

    heb_wn.close()

    return chosen_words
    # print(chosen_words)


if __name__ == '__main__':
    choose_random_words()
