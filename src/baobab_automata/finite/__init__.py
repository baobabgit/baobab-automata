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
from .regex_ast import ASTNode, NodeType
from .regex_exceptions import RegexConversionError, RegexError, RegexParseError, RegexSyntaxError
from .regex_parser import RegexParser
from .regex_token import Token, TokenType

__all__ = [
    'AbstractFiniteAutomaton',
    'ASTNode',
    'ConversionAlgorithms',
    'ConversionError',
    'ConversionMemoryError',
    'ConversionStats',
    'ConversionTimeoutError',
    'ConversionValidationError',
    'DFA',
    'DFAError',
    'EpsilonConversionError',
    'EpsilonNFA',
    'EpsilonNFAError',
    'InvalidDFAError',
    'InvalidEpsilonNFAError',
    'InvalidEpsilonTransitionError',
    'InvalidNFAError',
    'InvalidStateError',
    'InvalidTransitionError',
    'NFAConversionError',
    'NFAError',
    'NFAInvalidTransitionError',
    'NodeType',
    'RegexConversionError',
    'RegexError',
    'RegexParseError',
    'RegexParser',
    'RegexSyntaxError',
    'Token',
    'TokenType'
]
