# -*- coding: utf-8 -*-

from get_english_synsets import GetEnglishSynsets


def main():
    es = GetEnglishSynsets()

    all_synets = es.get_english_synsets()

if __name__ == '__main__':
    main()
