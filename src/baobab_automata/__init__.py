"""
Baobab Automata - Bibliothèque Python pour la manipulation d'automates.

Ce package fournit des interfaces et implémentations pour différents types
d'automates finis et de machines de Turing.
"""

__version__ = "0.1.0"
__author__ = "Baobab Automata Team"
__email__ = "team@baobab-automata.dev"

# Imports des interfaces principales
from .core.interfaces.state import IState, StateType
from .core.interfaces.transition import ITransition, TransitionType
from .core.interfaces.automaton import IAutomaton, AutomatonType
from .core.interfaces.recognizer import IRecognizer
from .core.interfaces.converter import IConverter

# Imports des implémentations concrètes
from .core.implementations.state import State
from .core.implementations.transition import Transition

# Imports des exceptions
from .exceptions import (
    BaobabAutomataError,
    InvalidAutomatonError,
    InvalidStateError,
    InvalidTransitionError,
    ConversionError,
    RecognitionError,
)

__all__ = [
    # Interfaces
    "IState",
    "StateType",
    "ITransition",
    "TransitionType",
    "IAutomaton",
    "AutomatonType",
    "IRecognizer",
    "IConverter",
    # Implémentations
    "State",
    "Transition",
    # Exceptions
    "BaobabAutomataError",
    "InvalidAutomatonError",
    "InvalidStateError",
    "InvalidTransitionError",
    "ConversionError",
    "RecognitionError",
]
