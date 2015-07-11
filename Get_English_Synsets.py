# -*- coding: utf-8 -*-
'''
Created on 7 ביול 2015

@author: Gilad
'''
from nltk.corpus import wordnet as wn
from gensim.models import Word2Vec
import Change_Hebrew_Letters


def get_English_synsets(similar_words):
    all_synsets = set()

    for word in similar_words:
        heb_word = Change_Hebrew_Letters.Get_Letters(word[0], "eng")
        word_synsets = wn.synsets(heb_word, lang='heb')

        print(word[0] + "({0}), Is {1:.3f} similar.".format(heb_word, word[1]))
        print("Synsets: {0}".format(word_synsets))

        if len(word_synsets) > 0:
            for synset in word_synsets:
                all_synsets.add(synset)
    return all_synsets


def read_corpus_from_file(path):
    with open(path) as f:
        lines = map(lambda line: line.replace("\n", ""), f.readlines())
    return list(lines)


def word_2_vec(heb_word):
    corpus_path = "vectors-g.bin"

    print("Starting Word2Vec Learning...")
    model = Word2Vec.load_word2vec_format(corpus_path, binary=True)

    return get_similar_word(model, heb_word)


def get_similar_word(model, heb_word):
    top_n = int(input("Please Enter number of wanted similar words\n"))

    print("Computing {0} most similar words for: {1}".format(top_n, heb_word))
    similar_words = model.most_similar(heb_word, topn=top_n)

    return similar_words

if __name__ == '__main__':
    heb_word = input("Please Write an Hebrew word, In Hebrew characters\n")
    heb_word = Change_Hebrew_Letters.Get_Letters(heb_word, "heb")

    similar_words = word_2_vec(heb_word)

    all_synsets = set()
    all_synsets = get_English_synsets(similar_words)

    print("All possible sysnets are: {0}".format(all_synsets))
