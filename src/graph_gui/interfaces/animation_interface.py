"""
File: animation_interface.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""

import abc


class AnimationInterface(abc.ABC):
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
