# -*- coding: utf-8 -*-

from get_english_synsets import GetEnglishSynsets
from scorer import SynsetGraph

def main():
    es = GetEnglishSynsets()

    all_synets = es.get_english_synsets()

    graph = SynsetGraph(all_synets)

if __name__ == '__main__':
    main()
