"""
Métriques de balancing pour les automates finis.

Ce module définit les métriques utilisées pour évaluer l'équilibrage
et les performances des automates finis.
"""

import statistics
from dataclasses import dataclass, field
from typing import Dict, Set

from ..abstract_finite_automaton import AbstractFiniteAutomaton


@dataclass(frozen=True)
class BalancingMetrics:
    """
    Métriques de balancing d'un automate.
    
    Cette classe encapsule toutes les métriques nécessaires pour évaluer
    l'équilibrage et les performances d'un automate fini.
    
    :param state_count: Nombre d'états dans l'automate
    :type state_count: int
    :param transition_count: Nombre de transitions dans l'automate
    :type transition_count: int
    :param average_transitions_per_state: Moyenne des transitions par état
    :type average_transitions_per_state: float
    :param max_transitions_per_state: Nombre maximum de transitions par état
    :type max_transitions_per_state: int
    :param min_transitions_per_state: Nombre minimum de transitions par état
    :type min_transitions_per_state: int
    :param transition_variance: Variance des transitions par état
    :type transition_variance: float
    :param state_access_frequency: Fréquence d'accès aux états
    :type state_access_frequency: Dict[str, float]
    :param transition_usage_frequency: Fréquence d'usage des transitions
    :type transition_usage_frequency: Dict[str, float]
    :param memory_usage: Utilisation mémoire en octets
    :type memory_usage: int
    :param recognition_complexity: Complexité de reconnaissance
    :type recognition_complexity: float
    :param balance_score: Score d'équilibrage (0.0 à 1.0)
    :type balance_score: float
    """
    
    state_count: int
    transition_count: int
    average_transitions_per_state: float
    max_transitions_per_state: int
    min_transitions_per_state: int
    transition_variance: float
    state_access_frequency: Dict[str, float] = field(default_factory=dict)
    transition_usage_frequency: Dict[str, float] = field(default_factory=dict)
    memory_usage: int = 0
    recognition_complexity: float = 0.0
    balance_score: float = 0.0
    
    def __post_init__(self) -> None:
        """
        Valide les métriques après initialisation.
        
        :raises ValueError: Si les métriques sont invalides
        """
        if self.state_count < 0:
            raise ValueError(f"Nombre d'états invalide: {self.state_count}")
        
        if self.transition_count < 0:
            raise ValueError(f"Nombre de transitions invalide: {self.transition_count}")
        
        if self.max_transitions_per_state < self.min_transitions_per_state:
            raise ValueError(
                f"Max transitions ({self.max_transitions_per_state}) < "
                f"Min transitions ({self.min_transitions_per_state})"
            )
        
        if not 0.0 <= self.balance_score <= 1.0:
            raise ValueError(f"Score d'équilibrage invalide: {self.balance_score}")
    
    @property
    def transition_balance_ratio(self) -> float:
        """
        Calcule le ratio d'équilibrage des transitions.
        
        :return: Ratio d'équilibrage (0.0 = parfaitement déséquilibré, 1.0 = parfaitement équilibré)
        :rtype: float
        """
        if self.max_transitions_per_state == 0:
            return 1.0
        
        return self.min_transitions_per_state / self.max_transitions_per_state
    
    @property
    def state_utilization(self) -> float:
        """
        Calcule le taux d'utilisation des états.
        
        :return: Taux d'utilisation des états (0.0 à 1.0)
        :rtype: float
        """
        if not self.state_access_frequency:
            return 0.0
        
        total_frequency = sum(self.state_access_frequency.values())
        if total_frequency == 0:
            return 0.0
        
        # Calcul de l'entropie pour mesurer la distribution
        probabilities = [
            freq / total_frequency 
            for freq in self.state_access_frequency.values()
        ]
        
        entropy = -sum(p * (p.bit_length() - 1) if p > 0 else 0 for p in probabilities)
        max_entropy = len(probabilities) * (1.0 / len(probabilities)) * (1.0 / len(probabilities)).bit_length()
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    @property
    def is_well_balanced(self) -> bool:
        """
        Indique si l'automate est bien équilibré.
        
        :return: True si bien équilibré, False sinon
        :rtype: bool
        """
        return (
            self.balance_score >= 0.7 and
            self.transition_balance_ratio >= 0.5 and
            self.state_utilization >= 0.6
        )
    
    @property
    def complexity_score(self) -> float:
        """
        Calcule un score de complexité global.
        
        :return: Score de complexité (0.0 = simple, 1.0 = complexe)
        :rtype: float
        """
        # Normalisation des métriques
        state_complexity = min(self.state_count / 100.0, 1.0)
        transition_complexity = min(self.transition_count / 500.0, 1.0)
        variance_complexity = min(self.transition_variance / 10.0, 1.0)
        
        return (state_complexity + transition_complexity + variance_complexity) / 3.0
    
    def to_dict(self) -> dict:
        """
        Sérialise les métriques en dictionnaire.
        
        :return: Dictionnaire représentant les métriques
        :rtype: dict
        """
        return {
            "state_count": self.state_count,
            "transition_count": self.transition_count,
            "average_transitions_per_state": self.average_transitions_per_state,
            "max_transitions_per_state": self.max_transitions_per_state,
            "min_transitions_per_state": self.min_transitions_per_state,
            "transition_variance": self.transition_variance,
            "state_access_frequency": self.state_access_frequency,
            "transition_usage_frequency": self.transition_usage_frequency,
            "memory_usage": self.memory_usage,
            "recognition_complexity": self.recognition_complexity,
            "balance_score": self.balance_score,
            "transition_balance_ratio": self.transition_balance_ratio,
            "state_utilization": self.state_utilization,
            "is_well_balanced": self.is_well_balanced,
            "complexity_score": self.complexity_score,
        }
    
    @classmethod
    def from_automaton(cls, automaton: AbstractFiniteAutomaton) -> "BalancingMetrics":
        """
        Calcule les métriques de balancing pour un automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Métriques de balancing
        :rtype: BalancingMetrics
        """
        states = automaton.states
        alphabet = automaton.alphabet
        
        # Calcul des transitions par état
        transitions_per_state = {}
        total_transitions = 0
        
        for state in states:
            state_transitions = 0
            for symbol in alphabet:
                if automaton.get_transition(state, symbol) is not None:
                    state_transitions += 1
            transitions_per_state[state] = state_transitions
            total_transitions += state_transitions
        
        # Calcul des statistiques
        transition_counts = list(transitions_per_state.values())
        
        if not transition_counts:
            return cls(
                state_count=len(states),
                transition_count=0,
                average_transitions_per_state=0.0,
                max_transitions_per_state=0,
                min_transitions_per_state=0,
                transition_variance=0.0,
                balance_score=1.0,
            )
        
        avg_transitions = statistics.mean(transition_counts)
        max_transitions = max(transition_counts)
        min_transitions = min(transition_counts)
        variance = statistics.variance(transition_counts) if len(transition_counts) > 1 else 0.0
        
        # Calcul du score d'équilibrage
        balance_score = cls._calculate_balance_score(
            avg_transitions, max_transitions, min_transitions, variance
        )
        
        return cls(
            state_count=len(states),
            transition_count=total_transitions,
            average_transitions_per_state=avg_transitions,
            max_transitions_per_state=max_transitions,
            min_transitions_per_state=min_transitions,
            transition_variance=variance,
            balance_score=balance_score,
        )
    
    @staticmethod
    def _calculate_balance_score(
        avg_transitions: float,
        max_transitions: int,
        min_transitions: int,
        variance: float
    ) -> float:
        """
        Calcule le score d'équilibrage.
        
        :param avg_transitions: Moyenne des transitions par état
        :type avg_transitions: float
        :param max_transitions: Maximum des transitions par état
        :type max_transitions: int
        :param min_transitions: Minimum des transitions par état
        :type min_transitions: int
        :param variance: Variance des transitions par état
        :type variance: float
        :return: Score d'équilibrage (0.0 à 1.0)
        :rtype: float
        """
        if max_transitions == 0:
            return 1.0
        
        # Score basé sur la variance (plus la variance est faible, plus c'est équilibré)
        variance_score = max(0.0, 1.0 - (variance / (avg_transitions + 1)))
        
        # Score basé sur l'écart entre min et max
        range_score = min_transitions / max_transitions
        
        # Score combiné
        return (variance_score + range_score) / 2.0