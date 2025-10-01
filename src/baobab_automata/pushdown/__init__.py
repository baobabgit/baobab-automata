"""
Module pushdown - Automates à pile.

Ce module implémente les automates à pile non-déterministes (PDA),
déterministes (DPDA) et non-déterministes (NPDA).
"""

from .abstract_pushdown_automaton import AbstractPushdownAutomaton
from .pda import PDA
from .pda_configuration import PDAConfiguration
from .pda_exceptions import (
    PDAError,
    InvalidPDAError,
    InvalidStateError,
    InvalidTransitionError,
    PDASimulationError,
    PDAStackError,
    PDAValidationError,
    PDAOperationError,
)
from .pda_operations import PDAOperations
from .dpda import DPDA
from .dpda_configuration import DPDAConfiguration
from .dpda_exceptions import (
    DPDAError,
    InvalidDPDAError,
    DeterminismError,
    ConflictError,
    ConversionError,
    DPDAOptimizationError,
)
from .npda import NPDA
from .npda_configuration import NPDAConfiguration
from .npda_exceptions import (
    NPDAError,
    InvalidNPDAError,
    NPDATimeoutError,
    NPDAMemoryError,
    NPDAConfigurationError,
    NPDAConversionError,
    NPDAOptimizationError,
    NPDAValidationError,
    NPDAComplexityError,
)
from .grammar_parser import GrammarParser
from .grammar_types import ContextFreeGrammar, GrammarType, Production
from .grammar_exceptions import (
    GrammarError,
    GrammarParseError,
    GrammarValidationError,
    GrammarConversionError,
    GrammarNormalizationError,
    GrammarOptimizationError,
    GrammarTimeoutError,
    GrammarMemoryError,
)
from .conversion_algorithms import PushdownConversionAlgorithms
from .conversion_exceptions import (
    ConversionError,
    ConversionTimeoutError,
    ConversionMemoryError,
    ConversionValidationError,
    ConversionOptimizationError,
    ConversionEquivalenceError,
    ConversionNotPossibleError,
    ConversionConfigurationError,
)
from .specialized_algorithms import SpecializedAlgorithms, ParseTree, AlgorithmStats
from .specialized_exceptions import (
    AlgorithmError,
    AlgorithmTimeoutError,
    AlgorithmMemoryError,
    AlgorithmValidationError,
    AlgorithmOptimizationError,
    CYKError,
    EarleyError,
    LeftRecursionError,
    EmptyProductionError,
    NormalizationError,
)

__all__ = [
    "AbstractPushdownAutomaton",
    "PDA",
    "PDAConfiguration",
    "PDAError",
    "InvalidPDAError",
    "InvalidStateError",
    "InvalidTransitionError",
    "PDASimulationError",
    "PDAStackError",
    "PDAValidationError",
    "PDAOperationError",
    "PDAOperations",
    "DPDA",
    "DPDAConfiguration",
    "DPDAError",
    "InvalidDPDAError",
    "DeterminismError",
    "ConflictError",
    "ConversionError",
    "DPDAOptimizationError",
    "NPDA",
    "NPDAConfiguration",
    "NPDAError",
    "InvalidNPDAError",
    "NPDATimeoutError",
    "NPDAMemoryError",
    "NPDAConfigurationError",
    "NPDAConversionError",
    "NPDAOptimizationError",
    "NPDAValidationError",
    "NPDAComplexityError",
    "GrammarParser",
    "ContextFreeGrammar",
    "GrammarType",
    "Production",
    "GrammarError",
    "GrammarParseError",
    "GrammarValidationError",
    "GrammarConversionError",
    "GrammarNormalizationError",
    "GrammarOptimizationError",
    "GrammarTimeoutError",
    "GrammarMemoryError",
    "PushdownConversionAlgorithms",
    "ConversionError",
    "ConversionTimeoutError",
    "ConversionMemoryError",
    "ConversionValidationError",
    "ConversionOptimizationError",
    "ConversionEquivalenceError",
    "ConversionNotPossibleError",
    "ConversionConfigurationError",
    "SpecializedAlgorithms",
    "ParseTree",
    "AlgorithmStats",
    "AlgorithmError",
    "AlgorithmTimeoutError",
    "AlgorithmMemoryError",
    "AlgorithmValidationError",
    "AlgorithmOptimizationError",
    "CYKError",
    "EarleyError",
    "LeftRecursionError",
    "EmptyProductionError",
    "NormalizationError",
]
