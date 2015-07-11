# -*- coding: utf-8 -*-

from get_english_synsets import GetEnglishSynsets

def main():
    es = GetEnglishSynsets()

    heb_word = input("Please Write an Hebrew word, In Hebrew characters\n")

    all_synets = es.get_english_synsets(heb_word)

if __name__ == '__main__':
    main()