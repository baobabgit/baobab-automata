"""
Module turing - Machines de Turing.

Ce module implémente les machines de Turing déterministes (DTM),
non-déterministes (NTM) et multi-rubans.
"""

from .tm import TM
from .tm_configuration import TMConfiguration
from .dtm import DTM
from .dtm_configuration import DTMConfiguration

__all__ = [
    "TM",
    "TMConfiguration",
    "DTM",
    "DTMConfiguration",
]
