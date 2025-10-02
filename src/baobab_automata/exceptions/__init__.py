"""
Exceptions personnalisées pour Baobab Automata.

Ce module contient toutes les exceptions personnalisées utilisées dans
la bibliothèque.
"""

from .base import (
    BaobabAutomataError,
    InvalidAutomatonError,
    InvalidStateError,
    InvalidTransitionError,
    ConversionError,
    RecognitionError,
)
from .tm_exceptions import (
    TMError,
    InvalidTMError,
    TMSimulationError,
    TMTimeoutError,
)
from .dtm_exceptions import (
    DTMError,
    InvalidDTMError,
    DTMDeterminismError,
    DTMSimulationError,
    DTMOptimizationError,
    DTMCacheError,
)

__all__ = [
    "BaobabAutomataError",
    "InvalidAutomatonError",
    "InvalidStateError",
    "InvalidTransitionError",
    "ConversionError",
    "RecognitionError",
    "TMError",
    "InvalidTMError",
    "TMSimulationError",
    "TMTimeoutError",
    "DTMError",
    "InvalidDTMError",
    "DTMDeterminismError",
    "DTMSimulationError",
    "DTMOptimizationError",
    "DTMCacheError",
]
