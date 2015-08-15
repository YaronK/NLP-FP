from synset_graph import SynsetGraph


class SynsetGraphExtension:
    @staticmethod
    def thin_out_graph_by_leaves(graph, number_of_leaves):
        leaf_synset_nodes = sorted(graph.get_leaf_synset_nodes(),
                                   key=lambda n: n.total_weight(),
                                   reverse=True)[:number_of_leaves]
        synset_weights_dictionary = {node.get_synset(): node.total_weight()
                                     for node in leaf_synset_nodes}

        return SynsetGraph("Thinner" + graph.name, synset_weights_dictionary)

    @staticmethod
    def thin_out_graph_by_paths(graph, number_of_leaves):
        chosen_synsets = {}  # synset : weight

        synset_weights = graph.get_synset_weights_dictionary().copy()
        temp_grpah = graph
        for _ in range(number_of_leaves):
            root_node = temp_grpah.get_entity_node()
            temp_node = root_node
            while not temp_node.is_leaf():
                temp_node = max(temp_node.get_hyponym_nodes(),
                                key=lambda n: n.total_probability())
            temp_synset = temp_node.get_synset()
            chosen_synsets[temp_synset] = temp_node.total_weight()
            del synset_weights[temp_synset]
            temp_grpah = SynsetGraph("Temp", synset_weights)

        return SynsetGraph("Thinner" + graph.name, chosen_synsets)
