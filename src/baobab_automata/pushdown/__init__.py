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
]
