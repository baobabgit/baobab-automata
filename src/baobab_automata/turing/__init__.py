"""
Module turing - Machines de Turing.

Ce module implémente les machines de Turing déterministes (DTM),
non-déterministes (NTM) et multi-rubans, ainsi que les algorithmes
de conversion entre ces différents types.
"""

from .tm import TM
from .tm_configuration import TMConfiguration
from .dtm import DTM
from .dtm_configuration import DTMConfiguration
from .ntm import NTM
from .ntm_configuration import NTMConfiguration
from .multitape_tm import MultiTapeTM
from .multitape_configuration import MultiTapeConfiguration

# Import des éléments de conversion
from .conversion import (
    ConversionType,
    ConversionResult,
    IConversionAlgorithm,
    ConversionEngine,
    NTMToDTMConverter,
    MultiTapeToSingleConverter,
    StateReductionConverter,
    SymbolMinimizationConverter,
    DTMToTMConverter,
    TMToDTMConverter,
    ConversionError,
    InvalidConversionEngineError,
    ConversionTimeoutError,
    EquivalenceVerificationError,
    OptimizationError,
)

__all__ = [
    "TM",
    "TMConfiguration",
    "DTM",
    "DTMConfiguration",
    "NTM",
    "NTMConfiguration",
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
]
