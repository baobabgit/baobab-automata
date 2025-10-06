"""
Fonctions de convenance pour exposer les fonctionnalités principales de la bibliothèque.

Ce module fournit des fonctions simples et directes pour les opérations les plus courantes
sur les automates finis.
"""

from typing import Optional

from .finite.dfa.dfa import DFA, Match
from .finite.nfa.nfa import NFA
from .algorithms.finite.conversion_algorithms import ConversionAlgorithms
from .algorithms.finite.optimization_algorithms import OptimizationAlgorithms


def regex_to_nfa(regex: str) -> NFA:
    """
    Convertit une expression régulière en NFA (Non-deterministic Finite Automaton).

    :param regex: Expression régulière à convertir
    :type regex: str
    :return: NFA équivalent à l'expression régulière
    :rtype: NFA
    :raises Exception: Si la conversion échoue
    """
    converter = ConversionAlgorithms()
    # Utiliser la méthode regex_to_automaton_optimized et convertir en NFA
    automaton = converter.regex_to_automaton_optimized(regex, target_type="nfa")
    if isinstance(automaton, NFA):
        return automaton
    else:
        # Si ce n'est pas un NFA, le convertir
        return automaton.to_nfa()


# Note: La conversion NFA vers DFA est disponible via nfa.to_dfa()
# Pas besoin de fonction de convenance redondante


def minimize_dfa(dfa: DFA) -> DFA:
    """
    Minimise un DFA en utilisant l'algorithme de Hopcroft.

    :param dfa: DFA à minimiser
    :type dfa: DFA
    :return: DFA minimal équivalent
    :rtype: DFA
    :raises Exception: Si la minimisation échoue
    """
    optimizer = OptimizationAlgorithms()
    return optimizer.minimize_dfa(dfa)


# Exposer les fonctions de convenance
__all__ = [
    "regex_to_nfa",
    "minimize_dfa",
    "DFA",
    "Match"
]
