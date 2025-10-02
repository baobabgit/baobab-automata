"""
Interfaces abstraites pour les automates.

Ce module contient toutes les interfaces abstraites définissant les contrats
pour les différents composants d'un automate.
"""

from .state import IState, StateType
from .transition import ITransition, TransitionType
from .automaton import IAutomaton, AutomatonType
from .recognizer import IRecognizer
from .converter import IConverter
from .turing_machine import ITuringMachine, TapeDirection, TMState
from .deterministic_turing_machine import IDeterministicTuringMachine, DTMState
from .non_deterministic_turing_machine import (
    INonDeterministicTuringMachine,
    NTMState,
    NTMTransition,
)

__all__ = [
    "IState",
    "StateType",
    "ITransition",
    "TransitionType",
    "IAutomaton",
    "AutomatonType",
    "IRecognizer",
    "IConverter",
    "ITuringMachine",
    "TapeDirection",
    "TMState",
    "IDeterministicTuringMachine",
    "DTMState",
    "INonDeterministicTuringMachine",
    "NTMState",
    "NTMTransition",
]
