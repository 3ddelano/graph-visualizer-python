import abc


class GraphInterface(abc.ABC):
    @abc.abstractmethod
    def add_node(self, node):
        pass

    @abc.abstractmethod
    def delete_node(self, node):
        pass

    @abc.abstractmethod
    def add_edge(self, edge):
        pass

    @abc.abstractmethod
    def delete_edge(self, edge):
        pass
