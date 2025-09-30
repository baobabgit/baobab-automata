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
]
