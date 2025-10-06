"""
Module turing - Machines de Turing.

Ce module implémente les machines de Turing déterministes (DTM),
non-déterministes (NTM) et multi-rubans, ainsi que les algorithmes
de conversion entre ces différents types.
"""

from .tm import TM
from .dtm import DTM
from .ntm import NTM
from .multitape import MultiTapeTM

# Imports des algorithmes
from ..algorithms.turing import ComplexityAnalyzer

__all__ = [
    "TM",
    "DTM",
    "NTM",
    "MultiTapeTM",
    "ComplexityAnalyzer",
]
