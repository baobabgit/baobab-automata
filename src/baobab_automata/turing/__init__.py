"""
Module turing - Machines de Turing.

Ce module implémente les machines de Turing déterministes (DTM),
non-déterministes (NTM) et multi-rubans.
"""

from .tm import TM
from .tm_configuration import TMConfiguration

__all__ = [
    "TM",
    "TMConfiguration",
]
