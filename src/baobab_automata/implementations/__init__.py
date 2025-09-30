"""
Implémentations concrètes des interfaces.

Ce module contient les implémentations concrètes des interfaces définies
dans le module interfaces.
"""

from .state import State
from .transition import Transition

__all__ = [
    "State",
    "Transition",
]
