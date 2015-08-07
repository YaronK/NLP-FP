# -*- coding: utf-8 -*-


class Evaluation:
    @staticmethod
    def evaluate(test_graph, gold_graph):
        gold_nodes = gold_graph.get_synset_nodes()
        test_nodes = test_graph.get_synset_nodes()

        total_gold = len(gold_nodes)
        total_test = len(test_nodes)

        total_nodes = total_gold + total_test

        test_correct = sum([1 for node in test_nodes
                           if node in gold_nodes])

        gold_correct = sum([1 for node in gold_nodes
                           if node in test_nodes])

        return ((test_correct + gold_correct) / total_nodes)

        # test_correct = sum([node.total_probability() for node in test_nodes
        #                     if node in gold_nodes])

        # test_wrong = sum([node.total_probability() for node in test_nodes
        #                   if node not in gold_nodes])
