"""
Baobab Automata - Bibliothèque Python pour la manipulation d'automates.

Ce package fournit des interfaces et implémentations pour différents types
d'automates finis, automates à pile et machines de Turing.
"""

__version__ = "0.1.0"
__author__ = "Baobab Automata Team"
__email__ = "team@baobab-automata.dev"

# Imports des fonctionnalités principales
from .convenience_functions import (
    regex_to_nfa,
    minimize_dfa,
    DFA,
    Match,
)

# Imports des automates finis
from .finite.dfa import DFA as DFA_Class
from .finite.nfa import NFA, EpsilonNFA
from .finite.regex import RegexParser

# Imports des automates à pile
from .pushdown.pda import PDA
from .pushdown.dpda import DPDA
from .pushdown.npda import NPDA
from .pushdown.grammar import GrammarParser

# Imports des machines de Turing
from .turing.tm import TM
from .turing.dtm import DTM
from .turing.ntm import NTM
from .turing.multitape import MultiTapeTM

# Imports des algorithmes
from .algorithms.finite import ConversionAlgorithms, OptimizationAlgorithms
from .algorithms.pushdown import PushdownConversionAlgorithms, PushdownOptimizationAlgorithms
from .algorithms.turing import ComplexityAnalyzer

__all__ = [
    # Fonctionnalités principales
    "regex_to_nfa",
    "minimize_dfa",
    "DFA",
    "Match",
    
    # Automates finis
    "DFA_Class",
    "NFA",
    "EpsilonNFA",
    "RegexParser",
    
    # Automates à pile
    "PDA",
    "DPDA", 
    "NPDA",
    "GrammarParser",
    
    # Machines de Turing
    "TM",
    "DTM",
    "NTM",
    "MultiTapeTM",
    
    # Algorithmes
    "ConversionAlgorithms",
    "OptimizationAlgorithms",
    "PushdownConversionAlgorithms",
    "PushdownOptimizationAlgorithms",
    "ComplexityAnalyzer",
]
