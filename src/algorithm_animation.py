import abc


class AlgorithmAnimation(abc.ABC):
    @abc.abstractmethod
    def one_step(self):
        pass

    @abc.abstractmethod
    def is_ended(self):
        pass

    @abc.abstractmethod
    def get_drawn_nodes(self):
        pass

    @abc.abstractmethod
    def get_drawn_edges(self):
        pass
