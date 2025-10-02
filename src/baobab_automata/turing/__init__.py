"""
Module turing - Machines de Turing.

Ce module implémente les machines de Turing déterministes (DTM),
non-déterministes (NTM) et multi-rubans.
"""

from .tm import TM
from .tm_configuration import TMConfiguration
from .dtm import DTM
from .dtm_configuration import DTMConfiguration
from .ntm import NTM
from .ntm_configuration import NTMConfiguration
from .multitape_tm import MultiTapeTM
from .multitape_configuration import MultiTapeConfiguration

__all__ = [
    "TM",
    "TMConfiguration",
    "DTM",
    "DTMConfiguration",
    "NTM",
    "NTMConfiguration",
<<<<<<< Current (Your changes)
=======
    "MultiTapeTM",
    "MultiTapeConfiguration",
    "ConversionType",
    "ConversionResult",
    "IConversionAlgorithm",
    "ConversionEngine",
    "NTMToDTMConverter",
    "MultiTapeToSingleConverter",
    "StateReductionConverter",
    "SymbolMinimizationConverter",
    "DTMToTMConverter",
    "TMToDTMConverter",
    "ConversionError",
    "InvalidConversionEngineError",
    "ConversionTimeoutError",
    "EquivalenceVerificationError",
    "OptimizationError",
>>>>>>> Incoming (Background Agent changes)
]
