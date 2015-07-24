# -*- coding: utf-8 -*-

from get_english_synsets import EnglishSynsets
from scorer import SynsetGraph


def main():
    print("Please write an Hebrew word")
    # word = input()
    print("Enter number of wanted Synsets")
    # synsets_number = input()
    word = "חתול"
    synsets_number = "3"

    es = EnglishSynsets(word, synsets_number)
    all_synets = es.get_english_synsets()

    graph = SynsetGraph(all_synets)

    graph.print_tree()

if __name__ == '__main__':
    main()
