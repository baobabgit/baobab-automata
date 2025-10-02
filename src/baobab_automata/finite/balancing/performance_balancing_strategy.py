"""
Stratégie de balancing de performance pour les automates finis.

Ce module implémente une stratégie de balancing qui optimise
les performances de reconnaissance des automates.
"""

import copy
import time
from typing import Dict, List, Set, Tuple

from .balancing_exceptions import BalancingError, BalancingTimeoutError
from .balancing_metrics import BalancingMetrics
from .balancing_result import BalancingResult
from .balancing_strategy import IBalancingStrategy
from ..abstract_finite_automaton import AbstractFiniteAutomaton
from ..dfa import DFA
from ..epsilon_nfa import EpsilonNFA
from ..nfa import NFA


class PerformanceBalancingStrategy(IBalancingStrategy):
    """
    Stratégie de balancing de performance pour les automates finis.
    
    Cette stratégie optimise les performances de reconnaissance en :
    - Réorganisant les états par fréquence d'usage
    - Optimisant le cache de reconnaissance
    - Pré-calculant les chemins fréquents
    
    :param max_iterations: Nombre maximum d'itérations
    :type max_iterations: int
    :param timeout_seconds: Timeout en secondes
    :type timeout_seconds: float
    :param performance_threshold: Seuil de performance (0.0 à 1.0)
    :type performance_threshold: float
    :param cache_size: Taille du cache de reconnaissance
    :type cache_size: int
    """
    
    def __init__(
        self,
        max_iterations: int = 50,
        timeout_seconds: float = 20.0,
        performance_threshold: float = 0.8,
        cache_size: int = 1000
    ) -> None:
        """
        Initialise la stratégie de balancing de performance.
        
        :param max_iterations: Nombre maximum d'itérations
        :type max_iterations: int
        :param timeout_seconds: Timeout en secondes
        :type timeout_seconds: float
        :param performance_threshold: Seuil de performance
        :type performance_threshold: float
        :param cache_size: Taille du cache de reconnaissance
        :type cache_size: int
        :raises BalancingError: Si les paramètres sont invalides
        """
        if max_iterations <= 0:
            raise BalancingError(f"Nombre d'itérations invalide: {max_iterations}")
        
        if timeout_seconds <= 0:
            raise BalancingError(f"Timeout invalide: {timeout_seconds}")
        
        if not 0.0 <= performance_threshold <= 1.0:
            raise BalancingError(f"Seuil de performance invalide: {performance_threshold}")
        
        if cache_size <= 0:
            raise BalancingError(f"Taille de cache invalide: {cache_size}")
        
        self._max_iterations = max_iterations
        self._timeout_seconds = timeout_seconds
        self._performance_threshold = performance_threshold
        self._cache_size = cache_size
    
    @property
    def name(self) -> str:
        """
        Nom de la stratégie.
        
        :return: Nom de la stratégie
        :rtype: str
        """
        return "PerformanceBalancing"
    
    @property
    def description(self) -> str:
        """
        Description de la stratégie.
        
        :return: Description de la stratégie
        :rtype: str
        """
        return (
            "Optimise les performances de reconnaissance en réorganisant "
            "les états par fréquence d'usage et en implémentant un système "
            "de cache intelligent pour améliorer la vitesse de reconnaissance."
        )
    
    def balance(self, automaton: AbstractFiniteAutomaton) -> BalancingResult:
        """
        Applique la stratégie de balancing de performance à un automate.
        
        :param automaton: Automate à équilibrer
        :type automaton: AbstractFiniteAutomaton
        :return: Résultat de l'opération de balancing
        :rtype: BalancingResult
        :raises BalancingError: Si l'opération échoue
        :raises BalancingTimeoutError: Si l'opération dépasse le timeout
        """
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            # Calcul des métriques avant balancing
            metrics_before = self.get_metrics(automaton)
            
            # Vérification si l'automate a déjà de bonnes performances
            if self._is_performance_optimal(metrics_before):
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
            balanced_automaton = self._apply_performance_balancing(automaton)
            
            # Calcul des métriques après balancing
            metrics_after = self.get_metrics(balanced_automaton)
            
            # Calcul du ratio d'amélioration
            improvement_ratio = self._calculate_performance_improvement(
                metrics_before, metrics_after
            )
            
            execution_time = time.time() - start_time
            memory_usage = self._get_memory_usage() - start_memory
            
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
            raise BalancingError(f"Erreur lors du balancing de performance: {e}") from e
    
    def get_metrics(self, automaton: AbstractFiniteAutomaton) -> BalancingMetrics:
        """
        Calcule les métriques de balancing de performance pour un automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Métriques de balancing de performance
        :rtype: BalancingMetrics
        """
        base_metrics = BalancingMetrics.from_automaton(automaton)
        
        # Calcul des métriques spécifiques à la performance
        performance_metrics = self._calculate_performance_metrics(automaton)
        
        # Mise à jour des métriques avec les données de performance
        return BalancingMetrics(
            state_count=base_metrics.state_count,
            transition_count=base_metrics.transition_count,
            average_transitions_per_state=base_metrics.average_transitions_per_state,
            max_transitions_per_state=base_metrics.max_transitions_per_state,
            min_transitions_per_state=base_metrics.min_transitions_per_state,
            transition_variance=base_metrics.transition_variance,
            state_access_frequency=performance_metrics["state_frequency"],
            transition_usage_frequency=performance_metrics["transition_frequency"],
            memory_usage=base_metrics.memory_usage,
            recognition_complexity=performance_metrics["recognition_complexity"],
            balance_score=performance_metrics["performance_score"],
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
        return self._is_performance_optimal(metrics)
    
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
            len(automaton.states) > 1 and
            len(automaton.alphabet) > 0
        )
    
    def _apply_performance_balancing(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Applique l'algorithme de balancing de performance.
        
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
            
            # Calcul des métriques actuelles
            current_metrics = self.get_metrics(current_automaton)
            
            # Vérification si l'automate a de bonnes performances
            if self._is_performance_optimal(current_metrics):
                break
            
            # Application des optimisations de performance
            current_automaton = self._optimize_state_access_pattern(current_automaton)
            current_automaton = self._implement_intelligent_cache(current_automaton)
            current_automaton = self._precompute_frequent_paths(current_automaton)
        
        return current_automaton
    
    def _optimize_state_access_pattern(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Optimise le pattern d'accès aux états.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate optimisé
        :rtype: AbstractFiniteAutomaton
        """
        # Analyse de la fréquence d'accès aux états
        state_frequency = self._analyze_state_access_frequency(automaton)
        
        # Réorganisation des états par fréquence d'usage
        return self._reorganize_states_by_frequency(automaton, state_frequency)
    
    def _implement_intelligent_cache(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Implémente un système de cache intelligent.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate avec cache intelligent
        :rtype: AbstractFiniteAutomaton
        """
        # Analyse des chemins fréquents
        frequent_paths = self._analyze_frequent_paths(automaton)
        
        # Implémentation du cache pour les chemins fréquents
        return self._add_intelligent_cache(automaton, frequent_paths)
    
    def _precompute_frequent_paths(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Pré-calcule les chemins fréquents.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate avec chemins pré-calculés
        :rtype: AbstractFiniteAutomaton
        """
        # Identification des chemins fréquents
        frequent_paths = self._identify_frequent_paths(automaton)
        
        # Pré-calcul des résultats pour les chemins fréquents
        return self._precompute_path_results(automaton, frequent_paths)
    
    def _calculate_performance_metrics(self, automaton: AbstractFiniteAutomaton) -> Dict[str, any]:
        """
        Calcule les métriques spécifiques à la performance.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Métriques de performance
        :rtype: Dict[str, any]
        """
        # Analyse de la fréquence d'accès aux états
        state_frequency = self._analyze_state_access_frequency(automaton)
        
        # Analyse de la fréquence d'usage des transitions
        transition_frequency = self._analyze_transition_usage_frequency(automaton)
        
        # Calcul de la complexité de reconnaissance
        recognition_complexity = self._calculate_recognition_complexity(automaton)
        
        # Calcul du score de performance
        performance_score = self._calculate_performance_score(
            state_frequency, transition_frequency, recognition_complexity
        )
        
        return {
            "state_frequency": state_frequency,
            "transition_frequency": transition_frequency,
            "recognition_complexity": recognition_complexity,
            "performance_score": performance_score,
        }
    
    def _analyze_state_access_frequency(self, automaton: AbstractFiniteAutomaton) -> Dict[str, float]:
        """
        Analyse la fréquence d'accès aux états.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Dictionnaire état -> fréquence d'accès
        :rtype: Dict[str, float]
        """
        # Pour l'instant, retourner des fréquences égales
        # L'implémentation complète nécessiterait une analyse plus complexe
        states = automaton.states
        frequency = 1.0 / len(states) if states else 0.0
        return {state: frequency for state in states}
    
    def _analyze_transition_usage_frequency(self, automaton: AbstractFiniteAutomaton) -> Dict[str, float]:
        """
        Analyse la fréquence d'usage des transitions.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Dictionnaire transition -> fréquence d'usage
        :rtype: Dict[str, float]
        """
        # Pour l'instant, retourner des fréquences égales
        # L'implémentation complète nécessiterait une analyse plus complexe
        transitions = []
        for state in automaton.states:
            for symbol in automaton.alphabet:
                if automaton.get_transition(state, symbol) is not None:
                    transitions.append(f"{state}:{symbol}")
        
        frequency = 1.0 / len(transitions) if transitions else 0.0
        return {transition: frequency for transition in transitions}
    
    def _calculate_recognition_complexity(self, automaton: AbstractFiniteAutomaton) -> float:
        """
        Calcule la complexité de reconnaissance.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Complexité de reconnaissance
        :rtype: float
        """
        # Complexité basée sur le nombre d'états et de transitions
        state_complexity = len(automaton.states) / 100.0
        transition_complexity = len(automaton.alphabet) / 50.0
        
        return min(1.0, state_complexity + transition_complexity)
    
    def _calculate_performance_score(self, state_frequency: Dict[str, float], transition_frequency: Dict[str, float], recognition_complexity: float) -> float:
        """
        Calcule le score de performance.
        
        :param state_frequency: Fréquence d'accès aux états
        :type state_frequency: Dict[str, float]
        :param transition_frequency: Fréquence d'usage des transitions
        :type transition_frequency: Dict[str, float]
        :param recognition_complexity: Complexité de reconnaissance
        :type recognition_complexity: float
        :return: Score de performance (0.0 à 1.0)
        :rtype: float
        """
        # Score basé sur la distribution des fréquences
        state_distribution_score = self._calculate_distribution_score(state_frequency)
        transition_distribution_score = self._calculate_distribution_score(transition_frequency)
        
        # Score combiné
        return (state_distribution_score + transition_distribution_score + (1.0 - recognition_complexity)) / 3.0
    
    def _calculate_distribution_score(self, frequency_dict: Dict[str, float]) -> float:
        """
        Calcule le score de distribution des fréquences.
        
        :param frequency_dict: Dictionnaire des fréquences
        :type frequency_dict: Dict[str, float]
        :return: Score de distribution (0.0 à 1.0)
        :rtype: float
        """
        if not frequency_dict:
            return 0.0
        
        values = list(frequency_dict.values())
        if not values:
            return 0.0
        
        # Score basé sur l'entropie de la distribution
        total = sum(values)
        if total == 0:
            return 0.0
        
        probabilities = [v / total for v in values]
        entropy = -sum(p * (p.bit_length() - 1) if p > 0 else 0 for p in probabilities)
        max_entropy = len(probabilities) * (1.0 / len(probabilities)) * (1.0 / len(probabilities)).bit_length()
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _is_performance_optimal(self, metrics: BalancingMetrics) -> bool:
        """
        Vérifie si les performances sont optimales.
        
        :param metrics: Métriques de performance
        :type metrics: BalancingMetrics
        :return: True si les performances sont optimales, False sinon
        :rtype: bool
        """
        return (
            metrics.balance_score >= self._performance_threshold and
            metrics.recognition_complexity <= 0.5 and
            metrics.state_utilization >= 0.7
        )
    
    def _analyze_frequent_paths(self, automaton: AbstractFiniteAutomaton) -> List[List[str]]:
        """
        Analyse les chemins fréquents dans l'automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Liste des chemins fréquents
        :rtype: List[List[str]]
        """
        # Pour l'instant, retourner une liste vide
        # L'implémentation complète nécessiterait une analyse plus complexe
        return []
    
    def _add_intelligent_cache(self, automaton: AbstractFiniteAutomaton, frequent_paths: List[List[str]]) -> AbstractFiniteAutomaton:
        """
        Ajoute un cache intelligent à l'automate.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :param frequent_paths: Chemins fréquents
        :type frequent_paths: List[List[str]]
        :return: Automate avec cache intelligent
        :rtype: AbstractFiniteAutomaton
        """
        # Pour l'instant, retourner l'automate original
        # L'implémentation complète nécessiterait une logique plus complexe
        return automaton
    
    def _identify_frequent_paths(self, automaton: AbstractFiniteAutomaton) -> List[List[str]]:
        """
        Identifie les chemins fréquents dans l'automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Liste des chemins fréquents
        :rtype: List[List[str]]
        """
        # Pour l'instant, retourner une liste vide
        # L'implémentation complète nécessiterait une logique plus complexe
        return []
    
    def _precompute_path_results(self, automaton: AbstractFiniteAutomaton, frequent_paths: List[List[str]]) -> AbstractFiniteAutomaton:
        """
        Pré-calcule les résultats pour les chemins fréquents.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :param frequent_paths: Chemins fréquents
        :type frequent_paths: List[List[str]]
        :return: Automate avec résultats pré-calculés
        :rtype: AbstractFiniteAutomaton
        """
        # Pour l'instant, retourner l'automate original
        # L'implémentation complète nécessiterait une logique plus complexe
        return automaton
    
    def _reorganize_states_by_frequency(self, automaton: AbstractFiniteAutomaton, state_frequency: Dict[str, float]) -> AbstractFiniteAutomaton:
        """
        Réorganise les états par fréquence d'usage.
        
        :param automaton: Automate à réorganiser
        :type automaton: AbstractFiniteAutomaton
        :param state_frequency: Fréquence d'accès aux états
        :type state_frequency: Dict[str, float]
        :return: Automate réorganisé
        :rtype: AbstractFiniteAutomaton
        """
        # Pour l'instant, retourner l'automate original
        # L'implémentation complète nécessiterait une logique plus complexe
        return automaton
    
    def _calculate_performance_improvement(self, metrics_before: BalancingMetrics, metrics_after: BalancingMetrics) -> float:
        """
        Calcule l'amélioration de performance.
        
        :param metrics_before: Métriques avant balancing
        :type metrics_before: BalancingMetrics
        :param metrics_after: Métriques après balancing
        :type metrics_after: BalancingMetrics
        :return: Ratio d'amélioration (0.0 à 1.0)
        :rtype: float
        """
        if metrics_before.balance_score == 0:
            return 0.0
        
        improvement = (metrics_after.balance_score - metrics_before.balance_score) / metrics_before.balance_score
        return max(0.0, min(1.0, improvement))
    
    def _get_memory_usage(self) -> int:
        """
        Obtient l'utilisation mémoire actuelle.
        
        :return: Utilisation mémoire en octets
        :rtype: int
        """
        # Pour l'instant, retourner 0
        # L'implémentation complète nécessiterait une mesure réelle
        return 0