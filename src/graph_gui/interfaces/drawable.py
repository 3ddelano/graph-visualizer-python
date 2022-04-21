"""
File: drawable.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""

import abc


class Drawable(abc.ABC):
    @abc.abstractmethod
    def draw(self, tur, *args):
        pass
