"""
Module conversion - Algorithmes de conversion des machines de Turing.

Ce module implémente les algorithmes de conversion entre différents types
de machines de Turing (TM, DTM, NTM, MultiTapeTM) avec validation d'équivalence
et optimisations.
"""

from .conversion_types import (
    ConversionType,
    ConversionResult,
    IConversionAlgorithm,
)
from .conversion_engine import ConversionEngine
from .converters import (
    NTMToDTMConverter,
    MultiTapeToSingleConverter,
    StateReductionConverter,
    SymbolMinimizationConverter,
    DTMToTMConverter,
    TMToDTMConverter,
)
from .exceptions import (
    ConversionError,
    InvalidConversionEngineError,
    ConversionTimeoutError,
    EquivalenceVerificationError,
    OptimizationError,
)

__all__ = [
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
