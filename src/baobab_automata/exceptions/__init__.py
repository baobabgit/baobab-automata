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
]
