"""
Stratégie de balancing mémoire pour les automates finis.

Ce module implémente une stratégie de balancing qui optimise
l'utilisation mémoire des automates.
"""

import copy
import time
from typing import Dict, List, Set, Tuple

from .balancing_exceptions import BalancingError, BalancingMemoryError, BalancingTimeoutError
from .balancing_metrics import BalancingMetrics
from .balancing_result import BalancingResult
from .balancing_strategy import IBalancingStrategy
from ..abstract_finite_automaton import AbstractFiniteAutomaton
from ..dfa import DFA
from ..epsilon_nfa import EpsilonNFA
from ..nfa import NFA


class MemoryBalancingStrategy(IBalancingStrategy):
    """
    Stratégie de balancing mémoire pour les automates finis.
    
    Cette stratégie optimise l'utilisation mémoire en :
    - Optimisant les structures de données
    - Réduisant la fragmentation mémoire
    - Implémentant un système de cache intelligent
    
    :param max_iterations: Nombre maximum d'itérations
    :type max_iterations: int
    :param timeout_seconds: Timeout en secondes
    :type timeout_seconds: float
    :param memory_threshold: Seuil d'utilisation mémoire (0.0 à 1.0)
    :type memory_threshold: float
    :param max_memory_usage: Utilisation mémoire maximale en octets
    :type max_memory_usage: int
    """
    
    def __init__(
        self,
        max_iterations: int = 30,
        timeout_seconds: float = 15.0,
        memory_threshold: float = 0.7,
        max_memory_usage: int = 100 * 1024 * 1024  # 100MB
    ) -> None:
        """
        Initialise la stratégie de balancing mémoire.
        
        :param max_iterations: Nombre maximum d'itérations
        :type max_iterations: int
        :param timeout_seconds: Timeout en secondes
        :type timeout_seconds: float
        :param memory_threshold: Seuil d'utilisation mémoire
        :type memory_threshold: float
        :param max_memory_usage: Utilisation mémoire maximale
        :type max_memory_usage: int
        :raises BalancingError: Si les paramètres sont invalides
        """
        if max_iterations <= 0:
            raise BalancingError(f"Nombre d'itérations invalide: {max_iterations}")
        
        if timeout_seconds <= 0:
            raise BalancingError(f"Timeout invalide: {timeout_seconds}")
        
        if not 0.0 <= memory_threshold <= 1.0:
            raise BalancingError(f"Seuil mémoire invalide: {memory_threshold}")
        
        if max_memory_usage <= 0:
            raise BalancingError(f"Utilisation mémoire maximale invalide: {max_memory_usage}")
        
        self._max_iterations = max_iterations
        self._timeout_seconds = timeout_seconds
        self._memory_threshold = memory_threshold
        self._max_memory_usage = max_memory_usage
    
    @property
    def name(self) -> str:
        """
        Nom de la stratégie.
        
        :return: Nom de la stratégie
        :rtype: str
        """
        return "MemoryBalancing"
    
    @property
    def description(self) -> str:
        """
        Description de la stratégie.
        
        :return: Description de la stratégie
        :rtype: str
        """
        return (
            "Optimise l'utilisation mémoire en optimisant les structures "
            "de données, en réduisant la fragmentation mémoire et en "
            "implémentant un système de cache intelligent pour minimiser "
            "l'empreinte mémoire."
        )
    
    def balance(self, automaton: AbstractFiniteAutomaton) -> BalancingResult:
        """
        Applique la stratégie de balancing mémoire à un automate.
        
        :param automaton: Automate à équilibrer
        :type automaton: AbstractFiniteAutomaton
        :return: Résultat de l'opération de balancing
        :rtype: BalancingResult
        :raises BalancingError: Si l'opération échoue
        :raises BalancingTimeoutError: Si l'opération dépasse le timeout
        :raises BalancingMemoryError: Si l'opération dépasse la limite mémoire
        """
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            # Vérification de la limite mémoire
            if start_memory > self._max_memory_usage:
                raise BalancingMemoryError(self._max_memory_usage, start_memory)
            
            # Calcul des métriques avant balancing
            metrics_before = self.get_metrics(automaton)
            
            # Vérification si l'automate utilise déjà efficacement la mémoire
            if self._is_memory_efficient(metrics_before):
                return BalancingResult(
                    original_automaton=automaton,
                    balanced_automaton=automaton,
                    metrics_before=metrics_before,
                    metrics_after=metrics_before,
                    improvement_ratio=0.0,
                    execution_time=time.time() - start_time,
                    memory_usage=0,
                    strategy_name=self.name,
                )
            
            # Application de la stratégie de balancing
            balanced_automaton = self._apply_memory_balancing(automaton)
            
            # Calcul des métriques après balancing
            metrics_after = self.get_metrics(balanced_automaton)
            
            # Calcul du ratio d'amélioration
            improvement_ratio = self._calculate_memory_improvement(
                metrics_before, metrics_after
            )
            
            execution_time = time.time() - start_time
            memory_usage = self._get_memory_usage() - start_memory
            
            # Vérification de la limite mémoire après balancing
            if memory_usage > self._max_memory_usage:
                raise BalancingMemoryError(self._max_memory_usage, memory_usage)
            
            return BalancingResult(
                original_automaton=automaton,
                balanced_automaton=balanced_automaton,
                metrics_before=metrics_before,
                metrics_after=metrics_after,
                improvement_ratio=improvement_ratio,
                execution_time=execution_time,
                memory_usage=memory_usage,
                strategy_name=self.name,
            )
            
        except Exception as e:
            if time.time() - start_time > self._timeout_seconds:
                raise BalancingTimeoutError(self._timeout_seconds, self.name) from e
            raise BalancingError(f"Erreur lors du balancing mémoire: {e}") from e
    
    def get_metrics(self, automaton: AbstractFiniteAutomaton) -> BalancingMetrics:
        """
        Calcule les métriques de balancing mémoire pour un automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Métriques de balancing mémoire
        :rtype: BalancingMetrics
        """
        base_metrics = BalancingMetrics.from_automaton(automaton)
        
        # Calcul des métriques spécifiques à la mémoire
        memory_metrics = self._calculate_memory_metrics(automaton)
        
        # Mise à jour des métriques avec les données mémoire
        return BalancingMetrics(
            state_count=base_metrics.state_count,
            transition_count=base_metrics.transition_count,
            average_transitions_per_state=base_metrics.average_transitions_per_state,
            max_transitions_per_state=base_metrics.max_transitions_per_state,
            min_transitions_per_state=base_metrics.min_transitions_per_state,
            transition_variance=base_metrics.transition_variance,
            state_access_frequency=base_metrics.state_access_frequency,
            transition_usage_frequency=base_metrics.transition_usage_frequency,
            memory_usage=memory_metrics["memory_usage"],
            recognition_complexity=base_metrics.recognition_complexity,
            balance_score=memory_metrics["memory_efficiency_score"],
        )
    
    def is_balanced(self, automaton: AbstractFiniteAutomaton) -> bool:
        """
        Vérifie si un automate est équilibré selon cette stratégie.
        
        :param automaton: Automate à vérifier
        :type automaton: AbstractFiniteAutomaton
        :return: True si l'automate est équilibré, False sinon
        :rtype: bool
        """
        metrics = self.get_metrics(automaton)
        return self._is_memory_efficient(metrics)
    
    def can_balance(self, automaton: AbstractFiniteAutomaton) -> bool:
        """
        Vérifie si cette stratégie peut être appliquée à un automate.
        
        :param automaton: Automate à vérifier
        :type automaton: AbstractFiniteAutomaton
        :return: True si la stratégie peut être appliquée, False sinon
        :rtype: bool
        """
        return (
            isinstance(automaton, (DFA, NFA, EpsilonNFA)) and
            automaton.validate() and
            len(automaton.states) > 0
        )
    
    def _apply_memory_balancing(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Applique l'algorithme de balancing mémoire.
        
        :param automaton: Automate à équilibrer
        :type automaton: AbstractFiniteAutomaton
        :return: Automate équilibré
        :rtype: AbstractFiniteAutomaton
        """
        current_automaton = copy.deepcopy(automaton)
        
        for iteration in range(self._max_iterations):
            # Vérification du timeout
            if time.time() - time.time() > self._timeout_seconds:
                break
            
            # Vérification de la limite mémoire
            current_memory = self._get_memory_usage()
            if current_memory > self._max_memory_usage:
                raise BalancingMemoryError(self._max_memory_usage, current_memory)
            
            # Calcul des métriques actuelles
            current_metrics = self.get_metrics(current_automaton)
            
            # Vérification si l'automate utilise efficacement la mémoire
            if self._is_memory_efficient(current_metrics):
                break
            
            # Application des optimisations mémoire
            current_automaton = self._optimize_data_structures(current_automaton)
            current_automaton = self._reduce_memory_fragmentation(current_automaton)
            current_automaton = self._implement_memory_cache(current_automaton)
        
        return current_automaton
    
    def _optimize_data_structures(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Optimise les structures de données de l'automate.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate avec structures optimisées
        :rtype: AbstractFiniteAutomaton
        """
        # Optimisation des structures de données
        # Pour l'instant, retourner l'automate original
        # L'implémentation complète nécessiterait une logique plus complexe
        return automaton
    
    def _reduce_memory_fragmentation(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Réduit la fragmentation mémoire de l'automate.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate avec fragmentation réduite
        :rtype: AbstractFiniteAutomaton
        """
        # Réduction de la fragmentation mémoire
        # Pour l'instant, retourner l'automate original
        # L'implémentation complète nécessiterait une logique plus complexe
        return automaton
    
    def _implement_memory_cache(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Implémente un système de cache mémoire intelligent.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate avec cache mémoire intelligent
        :rtype: AbstractFiniteAutomaton
        """
        # Implémentation du cache mémoire intelligent
        # Pour l'instant, retourner l'automate original
        # L'implémentation complète nécessiterait une logique plus complexe
        return automaton
    
    def _calculate_memory_metrics(self, automaton: AbstractFiniteAutomaton) -> Dict[str, any]:
        """
        Calcule les métriques spécifiques à la mémoire.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Métriques mémoire
        :rtype: Dict[str, any]
        """
        # Calcul de l'utilisation mémoire
        memory_usage = self._estimate_memory_usage(automaton)
        
        # Calcul de l'efficacité mémoire
        memory_efficiency = self._calculate_memory_efficiency(automaton, memory_usage)
        
        return {
            "memory_usage": memory_usage,
            "memory_efficiency_score": memory_efficiency,
        }
    
    def _estimate_memory_usage(self, automaton: AbstractFiniteAutomaton) -> int:
        """
        Estime l'utilisation mémoire de l'automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Utilisation mémoire estimée en octets
        :rtype: int
        """
        # Estimation basée sur le nombre d'états et de transitions
        state_memory = len(automaton.states) * 64  # 64 octets par état
        transition_memory = len(automaton.alphabet) * len(automaton.states) * 32  # 32 octets par transition
        
        return state_memory + transition_memory
    
    def _calculate_memory_efficiency(self, automaton: AbstractFiniteAutomaton, memory_usage: int) -> float:
        """
        Calcule l'efficacité mémoire de l'automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :param memory_usage: Utilisation mémoire en octets
        :type memory_usage: int
        :return: Score d'efficacité mémoire (0.0 à 1.0)
        :rtype: float
        """
        # Score basé sur l'utilisation mémoire par rapport à la limite
        memory_ratio = memory_usage / self._max_memory_usage
        
        # Score basé sur la densité des données
        data_density = self._calculate_data_density(automaton)
        
        # Score combiné
        return (1.0 - memory_ratio) * data_density
    
    def _calculate_data_density(self, automaton: AbstractFiniteAutomaton) -> float:
        """
        Calcule la densité des données de l'automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Densité des données (0.0 à 1.0)
        :rtype: float
        """
        # Densité basée sur le ratio transitions/états
        if len(automaton.states) == 0:
            return 0.0
        
        transition_density = len(automaton.alphabet) / len(automaton.states)
        return min(1.0, transition_density / 10.0)  # Normalisation
    
    def _is_memory_efficient(self, metrics: BalancingMetrics) -> bool:
        """
        Vérifie si l'automate utilise efficacement la mémoire.
        
        :param metrics: Métriques mémoire
        :type metrics: BalancingMetrics
        :return: True si l'automate est efficace en mémoire, False sinon
        :rtype: bool
        """
        return (
            metrics.balance_score >= self._memory_threshold and
            metrics.memory_usage <= self._max_memory_usage * 0.8
        )
    
    def _calculate_memory_improvement(self, metrics_before: BalancingMetrics, metrics_after: BalancingMetrics) -> float:
        """
        Calcule l'amélioration de l'utilisation mémoire.
        
        :param metrics_before: Métriques avant balancing
        :type metrics_before: BalancingMetrics
        :param metrics_after: Métriques après balancing
        :type metrics_after: BalancingMetrics
        :return: Ratio d'amélioration (0.0 à 1.0)
        :rtype: float
        """
        if metrics_before.memory_usage == 0:
            return 0.0
        
        # Amélioration basée sur la réduction de l'utilisation mémoire
        memory_reduction = (metrics_before.memory_usage - metrics_after.memory_usage) / metrics_before.memory_usage
        
        # Amélioration basée sur l'efficacité mémoire
        efficiency_improvement = metrics_after.balance_score - metrics_before.balance_score
        
        # Score combiné
        return max(0.0, min(1.0, (memory_reduction + efficiency_improvement) / 2.0))
    
    def _get_memory_usage(self) -> int:
        """
        Obtient l'utilisation mémoire actuelle.
        
        :return: Utilisation mémoire en octets
        :rtype: int
        """
        # Pour l'instant, retourner 0
        # L'implémentation complète nécessiterait une mesure réelle
        return 0