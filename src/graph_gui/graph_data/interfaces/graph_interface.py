"""
File: graph_interface.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""

import abc


class GraphInterface(abc.ABC):
    @abc.abstractmethod
    def add_node(self, node):
        pass

    @abc.abstractmethod
    def delete_node(self, node_or_id):
        pass

    @abc.abstractmethod
    def get_adjacent_nodes(self, node_or_id):
        pass

    @abc.abstractmethod
    def get_node_by_id(self, node_id):
        pass

    # ----------
    # Edge Methods
    # ----------

    @abc.abstractmethod
    def add_edge(self, edge):
        pass

    @abc.abstractmethod
    def update_edge_weight(self, edge_or_id, weight):
        pass

    @abc.abstractmethod
    def delete_edge(self, edge_or_id):
        pass

    @abc.abstractmethod
    def get_adjacent_edges(self, node_or_id):
        pass

    @abc.abstractmethod
    def get_edge_by_id(self, edge_id):
        pass

    @abc.abstractmethod
    def get_edge_between_nodes(self, nodeA_or_id, nodeB_or_id):
        pass

    # ----------
    # Misc Methods
    # ----------

    @abc.abstractmethod
    def save_to_files(self, nodelist_path, edgelist_path):
        pass

    @abc.abstractmethod
    def load_from_files(self, nodelist_path, edgelist_path):
        pass
