"""
Module finite - Automates finis.

Ce module implémente les automates finis déterministes (DFA),
non-déterministes (NFA) et epsilon-NFA.
"""

from .abstract_finite_automaton import AbstractFiniteAutomaton
from .conversion_algorithms import (
    ConversionAlgorithms,
    ConversionError,
    ConversionMemoryError,
    ConversionStats,
    ConversionTimeoutError,
    ConversionValidationError
)
from .dfa import DFA
from .dfa_exceptions import DFAError, InvalidDFAError, InvalidStateError, InvalidTransitionError
from .epsilon_nfa import EpsilonNFA
from .epsilon_nfa_exceptions import ConversionError as EpsilonConversionError, EpsilonNFAError, InvalidEpsilonNFAError, InvalidEpsilonTransitionError
from .nfa import NFA
from .nfa_exceptions import ConversionError as NFAConversionError, InvalidNFAError, InvalidTransitionError as NFAInvalidTransitionError, NFAError

__all__ = [
    'AbstractFiniteAutomaton',
    'ConversionAlgorithms',
    'ConversionError',
    'ConversionMemoryError',
    'ConversionStats',
    'ConversionTimeoutError',
    'ConversionValidationError',
    'DFA',
    'DFAError',
    'InvalidDFAError',
    'InvalidStateError',
    'InvalidTransitionError',
    'EpsilonNFA',
    'EpsilonNFAError',
    'InvalidEpsilonNFAError',
    'InvalidEpsilonTransitionError',
    'EpsilonConversionError',
    'NFA',
    'NFAError',
    'InvalidNFAError',
    'NFAInvalidTransitionError',
    'NFAConversionError'
]
