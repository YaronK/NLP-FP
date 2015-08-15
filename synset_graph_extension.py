from synset_graph import SynsetGraph


class SynsetGraphExtension:
    @staticmethod
    def thin_out_graph(graph, number_of_leaves):
        leaf_synset_nodes = sorted(graph.get_leaf_synset_nodes(),
                                   key=lambda n: n.total_weight(),
                                   reverse=True)[:number_of_leaves]
        synset_weights_dictionary = {node.get_synset(): node.total_weight()
                                     for node in leaf_synset_nodes}

        return SynsetGraph("Thinner" + graph.name, synset_weights_dictionary)
