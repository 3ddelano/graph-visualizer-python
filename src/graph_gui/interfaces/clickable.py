"""
File: clickable.py
Author: Delano Lourenco
Repo: https://github.com/3ddelano/graph-visualizer-python
License: MIT
"""

import abc


class Clickable(abc.ABC):
    @abc.abstractmethod
    def is_clicked(self, x, y):
        pass
