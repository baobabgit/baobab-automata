"""
Module finite - Automates finis.

Ce module implémente les automates finis déterministes (DFA),
non-déterministes (NFA) et epsilon-NFA.
"""

from .abstract_finite_automaton import AbstractFiniteAutomaton
from .dfa import DFA
from .dfa_exceptions import DFAError, InvalidDFAError, InvalidStateError, InvalidTransitionError
from .nfa import NFA
from .nfa_exceptions import ConversionError, InvalidNFAError, InvalidTransitionError as NFAInvalidTransitionError, NFAError

__all__ = [
    'AbstractFiniteAutomaton',
    'DFA',
    'DFAError',
    'InvalidDFAError',
    'InvalidStateError',
    'InvalidTransitionError',
    'NFA',
    'NFAError',
    'InvalidNFAError',
    'NFAInvalidTransitionError',
    'ConversionError'
]
