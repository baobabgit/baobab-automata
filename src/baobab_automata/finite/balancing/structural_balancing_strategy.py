"""
Stratégie de balancing structurel pour les automates finis.

Ce module implémente une stratégie de balancing qui optimise
la structure des automates pour réduire la complexité.
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


class StructuralBalancingStrategy(IBalancingStrategy):
    """
    Stratégie de balancing structurel pour les automates finis.
    
    Cette stratégie optimise la structure des automates en :
    - Réorganisant les états pour équilibrer la charge
    - Optimisant la distribution des transitions
    - Réduisant la complexité structurelle
    
    :param max_iterations: Nombre maximum d'itérations
    :type max_iterations: int
    :param timeout_seconds: Timeout en secondes
    :type timeout_seconds: float
    :param balance_threshold: Seuil d'équilibrage (0.0 à 1.0)
    :type balance_threshold: float
    """
    
    def __init__(
        self,
        max_iterations: int = 100,
        timeout_seconds: float = 30.0,
        balance_threshold: float = 0.8
    ) -> None:
        """
        Initialise la stratégie de balancing structurel.
        
        :param max_iterations: Nombre maximum d'itérations
        :type max_iterations: int
        :param timeout_seconds: Timeout en secondes
        :type timeout_seconds: float
        :param balance_threshold: Seuil d'équilibrage
        :type balance_threshold: float
        :raises BalancingError: Si les paramètres sont invalides
        """
        if max_iterations <= 0:
            raise BalancingError(f"Nombre d'itérations invalide: {max_iterations}")
        
        if timeout_seconds <= 0:
            raise BalancingError(f"Timeout invalide: {timeout_seconds}")
        
        if not 0.0 <= balance_threshold <= 1.0:
            raise BalancingError(f"Seuil d'équilibrage invalide: {balance_threshold}")
        
        self._max_iterations = max_iterations
        self._timeout_seconds = timeout_seconds
        self._balance_threshold = balance_threshold
    
    @property
    def name(self) -> str:
        """
        Nom de la stratégie.
        
        :return: Nom de la stratégie
        :rtype: str
        """
        return "StructuralBalancing"
    
    @property
    def description(self) -> str:
        """
        Description de la stratégie.
        
        :return: Description de la stratégie
        :rtype: str
        """
        return (
            "Optimise la structure des automates en réorganisant les états "
            "et en équilibrant la distribution des transitions pour réduire "
            "la complexité structurelle."
        )
    
    def balance(self, automaton: AbstractFiniteAutomaton) -> BalancingResult:
        """
        Applique la stratégie de balancing structurel à un automate.
        
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
            
            # Vérification si l'automate est déjà équilibré
            if metrics_before.is_well_balanced:
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
            balanced_automaton = self._apply_structural_balancing(automaton)
            
            # Calcul des métriques après balancing
            metrics_after = self.get_metrics(balanced_automaton)
            
            # Calcul du ratio d'amélioration
            improvement_ratio = self._calculate_improvement_ratio(
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
            raise BalancingError(f"Erreur lors du balancing structurel: {e}") from e
    
    def get_metrics(self, automaton: AbstractFiniteAutomaton) -> BalancingMetrics:
        """
        Calcule les métriques de balancing structurel pour un automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Métriques de balancing structurel
        :rtype: BalancingMetrics
        """
        return BalancingMetrics.from_automaton(automaton)
    
    def is_balanced(self, automaton: AbstractFiniteAutomaton) -> bool:
        """
        Vérifie si un automate est équilibré selon cette stratégie.
        
        :param automaton: Automate à vérifier
        :type automaton: AbstractFiniteAutomaton
        :return: True si l'automate est équilibré, False sinon
        :rtype: bool
        """
        metrics = self.get_metrics(automaton)
        return metrics.balance_score >= self._balance_threshold
    
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
            len(automaton.states) > 1
        )
    
    def _apply_structural_balancing(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Applique l'algorithme de balancing structurel.
        
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
            
            # Vérification si l'automate est suffisamment équilibré
            if current_metrics.balance_score >= self._balance_threshold:
                break
            
            # Application des optimisations structurelles
            current_automaton = self._optimize_state_distribution(current_automaton)
            current_automaton = self._optimize_transition_distribution(current_automaton)
            current_automaton = self._reorganize_states(current_automaton)
        
        return current_automaton
    
    def _optimize_state_distribution(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Optimise la distribution des états.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate optimisé
        :rtype: AbstractFiniteAutomaton
        """
        # Analyse de la distribution des transitions par état
        transitions_per_state = self._analyze_transitions_per_state(automaton)
        
        # Identification des états déséquilibrés
        unbalanced_states = self._identify_unbalanced_states(transitions_per_state)
        
        # Réorganisation des états déséquilibrés
        return self._rebalance_states(automaton, unbalanced_states)
    
    def _optimize_transition_distribution(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Optimise la distribution des transitions.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate optimisé
        :rtype: AbstractFiniteAutomaton
        """
        # Analyse des transitions redondantes
        redundant_transitions = self._find_redundant_transitions(automaton)
        
        # Fusion des transitions redondantes
        return self._merge_redundant_transitions(automaton, redundant_transitions)
    
    def _reorganize_states(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Réorganise les états pour optimiser les performances.
        
        :param automaton: Automate à réorganiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate réorganisé
        :rtype: AbstractFiniteAutomaton
        """
        # Analyse de la fréquence d'accès aux états
        state_frequency = self._analyze_state_frequency(automaton)
        
        # Réorganisation des états par fréquence d'usage
        return self._reorganize_by_frequency(automaton, state_frequency)
    
    def _analyze_transitions_per_state(self, automaton: AbstractFiniteAutomaton) -> Dict[str, int]:
        """
        Analyse le nombre de transitions par état.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Dictionnaire état -> nombre de transitions
        :rtype: Dict[str, int]
        """
        transitions_per_state = {}
        
        for state in automaton.states:
            transition_count = 0
            for symbol in automaton.alphabet:
                if automaton.get_transition(state, symbol) is not None:
                    transition_count += 1
            transitions_per_state[state] = transition_count
        
        return transitions_per_state
    
    def _identify_unbalanced_states(self, transitions_per_state: Dict[str, int]) -> List[str]:
        """
        Identifie les états déséquilibrés.
        
        :param transitions_per_state: Nombre de transitions par état
        :type transitions_per_state: Dict[str, int]
        :return: Liste des états déséquilibrés
        :rtype: List[str]
        """
        if not transitions_per_state:
            return []
        
        values = list(transitions_per_state.values())
        avg_transitions = sum(values) / len(values)
        
        unbalanced_states = []
        for state, count in transitions_per_state.items():
            # Un état est déséquilibré s'il a beaucoup plus ou beaucoup moins de transitions
            if count > avg_transitions * 1.5 or count < avg_transitions * 0.5:
                unbalanced_states.append(state)
        
        return unbalanced_states
    
    def _rebalance_states(self, automaton: AbstractFiniteAutomaton, unbalanced_states: List[str]) -> AbstractFiniteAutomaton:
        """
        Rééquilibre les états déséquilibrés.
        
        :param automaton: Automate à rééquilibrer
        :type automaton: AbstractFiniteAutomaton
        :param unbalanced_states: États déséquilibrés
        :type unbalanced_states: List[str]
        :return: Automate rééquilibré
        :rtype: AbstractFiniteAutomaton
        """
        # Pour l'instant, retourner l'automate original
        # L'implémentation complète nécessiterait une logique plus complexe
        return automaton
    
    def _find_redundant_transitions(self, automaton: AbstractFiniteAutomaton) -> List[Tuple[str, str, str]]:
        """
        Trouve les transitions redondantes.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Liste des transitions redondantes
        :rtype: List[Tuple[str, str, str]]
        """
        # Pour l'instant, retourner une liste vide
        # L'implémentation complète nécessiterait une logique plus complexe
        return []
    
    def _merge_redundant_transitions(self, automaton: AbstractFiniteAutomaton, redundant_transitions: List[Tuple[str, str, str]]) -> AbstractFiniteAutomaton:
        """
        Fusionne les transitions redondantes.
        
        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :param redundant_transitions: Transitions redondantes
        :type redundant_transitions: List[Tuple[str, str, str]]
        :return: Automate optimisé
        :rtype: AbstractFiniteAutomaton
        """
        # Pour l'instant, retourner l'automate original
        # L'implémentation complète nécessiterait une logique plus complexe
        return automaton
    
    def _analyze_state_frequency(self, automaton: AbstractFiniteAutomaton) -> Dict[str, float]:
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
    
    def _reorganize_by_frequency(self, automaton: AbstractFiniteAutomaton, state_frequency: Dict[str, float]) -> AbstractFiniteAutomaton:
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
    
    def _calculate_improvement_ratio(self, metrics_before: BalancingMetrics, metrics_after: BalancingMetrics) -> float:
        """
        Calcule le ratio d'amélioration.
        
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