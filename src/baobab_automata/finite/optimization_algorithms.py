"""
Algorithmes d'optimisation pour les automates finis.

Ce module implémente les algorithmes d'optimisation pour les automates finis
dans la phase 2 du projet Baobab Automata. Ces algorithmes permettent de
minimiser, optimiser et améliorer les performances des automates.
"""

import random
import time
from typing import Any, Dict, List, Set

from .abstract_finite_automaton import AbstractFiniteAutomaton
from .conversion_algorithms import ConversionAlgorithms
from .dfa import DFA
from .epsilon_nfa import EpsilonNFA
from .nfa import NFA
from .optimization_exceptions import OptimizationError, OptimizationValidationError


class OptimizationAlgorithms:
    """
    Classe principale pour les algorithmes d'optimisation des automates finis.

    Cette classe fournit des méthodes pour minimiser, optimiser et améliorer
    les performances des automates finis (DFA, NFA, ε-NFA).

    :param optimization_level: Niveau d'optimisation (0-3)
    :type optimization_level: int
    :param max_iterations: Limite d'itérations pour les algorithmes
    :type max_iterations: int
    """

    def __init__(self, optimization_level: int = 2, max_iterations: int = 1000) -> None:
        """
        Initialise l'optimiseur d'automates.

        :param optimization_level: Niveau d'optimisation (0-3)
        :type optimization_level: int
        :param max_iterations: Limite d'itérations pour les algorithmes
        :type max_iterations: int
        :raises OptimizationError: Si le niveau d'optimisation est invalide
        """
        if not 0 <= optimization_level <= 3:
            raise OptimizationError(
                f"Niveau d'optimisation invalide: {optimization_level}"
            )

        self._cache: Dict[str, AbstractFiniteAutomaton] = {}
        self._optimization_level = optimization_level
        self._max_iterations = max_iterations
        self._stats = OptimizationStats()

    @property
    def cache(self) -> Dict[str, AbstractFiniteAutomaton]:
        """
        Cache des optimisations.

        :return: Dictionnaire des automates optimisés
        :rtype: Dict[str, AbstractFiniteAutomaton]
        """
        return self._cache

    @property
    def optimization_level(self) -> int:
        """
        Niveau d'optimisation actuel.

        :return: Niveau d'optimisation (0-3)
        :rtype: int
        """
        return self._optimization_level

    @property
    def max_iterations(self) -> int:
        """
        Limite d'itérations pour les algorithmes.

        :return: Nombre maximum d'itérations
        :rtype: int
        """
        return self._max_iterations

    def minimize_dfa(self, dfa: DFA) -> DFA:
        """
        Minimise un DFA en utilisant l'algorithme de Hopcroft.

        :param dfa: DFA à minimiser
        :type dfa: DFA
        :return: DFA minimal équivalent
        :rtype: DFA
        :raises OptimizationError: Si l'optimisation échoue
        """
        if not isinstance(dfa, DFA):
            raise OptimizationError("L'automate doit être un DFA")

        # Vérifier le cache
        cache_key = self._get_cache_key(dfa)
        if cache_key in self._cache:
            cached_result = self._cache[cache_key]
            if isinstance(cached_result, DFA):
                return cached_result

        try:
            # Éliminer les états inaccessibles d'abord
            clean_dfa = self.remove_unreachable_states(dfa)

            # Appliquer l'algorithme de Hopcroft
            minimal_dfa = self._hopcroft_minimization(clean_dfa)

            # Valider le résultat
            if not self.validate_optimization(dfa, minimal_dfa):
                raise OptimizationValidationError(
                    "La minimisation a produit un automate non équivalent"
                )

            # Mettre en cache
            self._cache[cache_key] = minimal_dfa

            # Enregistrer les statistiques
            improvement = (
                (len(dfa.states) - len(minimal_dfa.states)) / len(dfa.states) * 100
            )
            self._stats.add_optimization("minimize_dfa", 0.0, improvement)

            return minimal_dfa

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(f"Erreur lors de la minimisation DFA: {e}") from e

    def minimize_dfa_incremental(
        self, dfa: DFA, changes: List["TransitionChange"]  # pylint: disable=unused-argument
    ) -> DFA:
        """
        Minimise un DFA de manière incrémentale.

        :param dfa: DFA à minimiser
        :type dfa: DFA
        :param changes: Liste des changements de transitions
        :type changes: List[TransitionChange]
        :return: DFA minimal équivalent
        :rtype: DFA
        :raises OptimizationError: Si l'optimisation échoue
        """
        if not isinstance(dfa, DFA):
            raise OptimizationError("L'automate doit être un DFA")

        start_time = time.time()

        try:
            # Pour l'instant, utiliser la minimisation standard
            # L'implémentation incrémentale sera ajoutée plus tard
            minimal_dfa = self.minimize_dfa(dfa)

            # Enregistrer les statistiques
            improvement = (
                (len(dfa.states) - len(minimal_dfa.states)) / len(dfa.states) * 100
            )
            self._stats.add_optimization(
                "minimize_dfa_incremental", 0.0, improvement
            )

            return minimal_dfa

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de la minimisation incrémentale DFA: {e}"
            )

    def minimize_dfa_optimized(self, dfa: DFA) -> DFA:
        """
        Minimise un DFA avec des optimisations avancées.

        :param dfa: DFA à minimiser
        :type dfa: DFA
        :return: DFA minimal équivalent
        :rtype: DFA
        :raises OptimizationError: Si l'optimisation échoue
        """
        if not isinstance(dfa, DFA):
            raise OptimizationError("L'automate doit être un DFA")

        # Vérifier le cache
        cache_key = self._get_cache_key(dfa) + "_optimized"
        if cache_key in self._cache:
            cached_result = self._cache[cache_key]
            if isinstance(cached_result, DFA):
                return cached_result

        try:
            # Éliminer les états inaccessibles et cœurs
            clean_dfa = self.remove_unreachable_states(dfa)
            clean_dfa = self.remove_coaccessible_states(clean_dfa)

            # Appliquer l'algorithme de Hopcroft optimisé
            minimal_dfa = self._hopcroft_minimization_optimized(clean_dfa)

            # Optimiser les structures de données
            minimal_dfa = self.optimize_data_structures(minimal_dfa)

            # Valider le résultat
            if not self.validate_optimization(dfa, minimal_dfa):
                raise OptimizationValidationError(
                    "La minimisation optimisée a produit un automate non équivalent"
                )

            # Mettre en cache
            self._cache[cache_key] = minimal_dfa

            # Enregistrer les statistiques
            optimization_time = time.time() - start_time
            improvement = (
                (len(dfa.states) - len(minimal_dfa.states)) / len(dfa.states) * 100
            )
            self._stats.add_optimization(
                "minimize_dfa_optimized", optimization_time, improvement
            )

            return minimal_dfa

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de la minimisation DFA optimisée: {e}"
            ) from e

    def minimize_nfa(self, nfa: NFA) -> DFA:
        """
        Minimise un NFA en le convertissant d'abord en DFA.

        :param nfa: NFA à minimiser
        :type nfa: NFA
        :return: NFA minimal équivalent
        :rtype: NFA
        :raises OptimizationError: Si l'optimisation échoue
        """
        if not isinstance(nfa, NFA):
            raise OptimizationError("L'automate doit être un NFA")

        # Vérifier le cache
        cache_key = self._get_cache_key(nfa)
        if cache_key in self._cache:
            cached_result = self._cache[cache_key]
            if isinstance(cached_result, NFA):
                return cached_result

        start_time = time.time()

        try:
            # Convertir NFA -> DFA
            converter = ConversionAlgorithms()
            dfa = converter.nfa_to_dfa(nfa)

            # Minimiser le DFA
            minimal_dfa = self.minimize_dfa(dfa)

            # Pour l'instant, retourner le DFA minimal
            # La conversion DFA -> NFA sera implémentée plus tard
            minimal_nfa = minimal_dfa

            # Valider le résultat
            if not self.validate_optimization(nfa, minimal_dfa):
                raise OptimizationValidationError(
                    "La minimisation NFA a produit un automate non équivalent"
                )

            # Mettre en cache
            self._cache[cache_key] = minimal_dfa

            # Enregistrer les statistiques
            optimization_time = time.time() - start_time
            improvement = (
                (len(nfa.states) - len(minimal_dfa.states)) / len(nfa.states) * 100
            )
            self._stats.add_optimization("minimize_nfa", optimization_time, improvement)

            return minimal_dfa

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(f"Erreur lors de la minimisation NFA: {e}") from e

    def minimize_nfa_approximate(self, nfa: NFA, tolerance: float = 0.1) -> NFA:
        """
        Minimise un NFA de manière approximative.

        :param nfa: NFA à minimiser
        :type nfa: NFA
        :param tolerance: Tolérance pour la perte de précision
        :type tolerance: float
        :return: NFA optimisé
        :rtype: NFA
        :raises OptimizationError: Si l'optimisation échoue
        """
        if not isinstance(nfa, NFA):
            raise OptimizationError("L'automate doit être un NFA")

        if not 0 <= tolerance <= 1:
            raise OptimizationError("La tolérance doit être entre 0 et 1")

        try:
            # Appliquer des heuristiques d'optimisation
            optimized_nfa = self.minimize_nfa_heuristic(nfa)

            # Valider que la perte de précision est acceptable
            if not self._validate_approximation(nfa, optimized_nfa, tolerance):
                # Si la perte est trop importante, retourner l'original
                optimized_nfa = nfa

            # Enregistrer les statistiques
            optimization_time = time.time() - start_time
            improvement = (
                (len(nfa.states) - len(optimized_nfa.states)) / len(nfa.states) * 100
            )
            self._stats.add_optimization(
                "minimize_nfa_approximate", optimization_time, improvement
            )

            return optimized_nfa

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de la minimisation approximative NFA: {e}"
            ) from e

    def minimize_nfa_heuristic(self, nfa: NFA) -> NFA:
        """
        Minimise un NFA en utilisant des heuristiques.

        :param nfa: NFA à minimiser
        :type nfa: NFA
        :return: NFA optimisé
        :rtype: NFA
        :raises OptimizationError: Si l'optimisation échoue
        """
        if not isinstance(nfa, NFA):
            raise OptimizationError("L'automate doit être un NFA")

        try:
            # Éliminer les états inaccessibles
            clean_nfa = self.remove_unreachable_states(nfa)

            # Fusionner les transitions identiques
            clean_nfa = self.merge_identical_transitions(clean_nfa)

            # Optimiser les structures de données
            clean_nfa = self.optimize_data_structures(clean_nfa)

            # Valider le résultat
            if not self.validate_optimization(nfa, clean_nfa):
                raise OptimizationValidationError(
                    "La minimisation heuristique a produit un automate non équivalent"
                )

            # Enregistrer les statistiques
            optimization_time = time.time() - start_time
            improvement = (
                (len(nfa.states) - len(clean_nfa.states)) / len(nfa.states) * 100
            )
            self._stats.add_optimization(
                "minimize_nfa_heuristic", optimization_time, improvement
            )

            return clean_nfa

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de la minimisation heuristique NFA: {e}"
            ) from e

    def remove_unreachable_states(
        self, automaton: AbstractFiniteAutomaton
    ) -> AbstractFiniteAutomaton:
        """
        Élimine les états inaccessibles d'un automate.

        :param automaton: Automate à nettoyer
        :type automaton: AbstractFiniteAutomaton
        :return: Automate sans états inaccessibles
        :rtype: AbstractFiniteAutomaton
        :raises OptimizationError: Si l'optimisation échoue
        """
        try:
            # Obtenir les états accessibles
            reachable_states = automaton.get_reachable_states()

            # Si tous les états sont accessibles, retourner l'automate original
            if len(reachable_states) == len(automaton.states):
                return automaton

            # Créer un nouvel automate sans les états inaccessibles
            if isinstance(automaton, DFA):
                return self._remove_unreachable_states_dfa(automaton, reachable_states)
            elif isinstance(automaton, NFA):
                return self._remove_unreachable_states_nfa(automaton, reachable_states)
            elif isinstance(automaton, EpsilonNFA):
                return self._remove_unreachable_states_epsilon_nfa(
                    automaton, reachable_states
                )
            else:
                raise OptimizationError(
                    f"Type d'automate non supporté: {type(automaton)}"
                )

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de l'élimination des états inaccessibles: {e}"
            ) from e

    def remove_coaccessible_states(
        self, automaton: AbstractFiniteAutomaton
    ) -> AbstractFiniteAutomaton:
        """
        Élimine les états non-cœurs d'un automate.

        :param automaton: Automate à nettoyer
        :type automaton: AbstractFiniteAutomaton
        :return: Automate sans états non-cœurs
        :rtype: AbstractFiniteAutomaton
        :raises OptimizationError: Si l'optimisation échoue
        """
        try:
            # Obtenir les états cœurs (accessibles depuis les états finaux)
            coaccessible_states = self._get_coaccessible_states(automaton)

            # Si tous les états sont cœurs, retourner l'automate original
            if len(coaccessible_states) == len(automaton.states):
                return automaton

            # Créer un nouvel automate sans les états non-cœurs
            if isinstance(automaton, DFA):
                return self._remove_coaccessible_states_dfa(
                    automaton, coaccessible_states
                )
            elif isinstance(automaton, NFA):
                return self._remove_coaccessible_states_nfa(
                    automaton, coaccessible_states
                )
            elif isinstance(automaton, EpsilonNFA):
                return self._remove_coaccessible_states_epsilon_nfa(
                    automaton, coaccessible_states
                )
            else:
                raise OptimizationError(
                    f"Type d'automate non supporté: {type(automaton)}"
                )

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de l'élimination des états non-cœurs: {e}"
            ) from e

    def merge_identical_transitions(
        self, automaton: AbstractFiniteAutomaton
    ) -> AbstractFiniteAutomaton:
        """
        Fusionne les transitions identiques d'un automate.

        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate avec transitions fusionnées
        :rtype: AbstractFiniteAutomaton
        :raises OptimizationError: Si l'optimisation échoue
        """
        try:
            if isinstance(automaton, DFA):
                return self._merge_identical_transitions_dfa(automaton)
            elif isinstance(automaton, NFA):
                return self._merge_identical_transitions_nfa(automaton)
            elif isinstance(automaton, EpsilonNFA):
                return self._merge_identical_transitions_epsilon_nfa(automaton)
            else:
                raise OptimizationError(
                    f"Type d'automate non supporté: {type(automaton)}"
                )

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(f"Erreur lors de la fusion des transitions: {e}") from e

    def optimize_performance(
        self, automaton: AbstractFiniteAutomaton
    ) -> AbstractFiniteAutomaton:
        """
        Optimise les performances d'un automate.

        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate optimisé
        :rtype: AbstractFiniteAutomaton
        :raises OptimizationError: Si l'optimisation échoue
        """
        try:
            # Pour l'instant, retourner l'automate original
            # Cette méthode sera implémentée plus tard avec des optimisations spécifiques
            self._stats.add_optimization("optimize_performance", 0.0, 0.0)

            return automaton

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de l'optimisation des performances: {e}"
            ) from e

    def optimize_memory(
        self, automaton: AbstractFiniteAutomaton
    ) -> AbstractFiniteAutomaton:
        """
        Optimise l'utilisation mémoire d'un automate.

        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate optimisé
        :rtype: AbstractFiniteAutomaton
        :raises OptimizationError: Si l'optimisation échoue
        """
        try:
            # Pour l'instant, retourner l'automate original
            # Cette méthode sera implémentée plus tard avec des optimisations spécifiques
            self._stats.add_optimization("optimize_memory", 0.0, 0.0)

            return automaton

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(f"Erreur lors de l'optimisation de la mémoire: {e}") from e

    def optimize_for_conversion(
        self, automaton: AbstractFiniteAutomaton, target_type: str
    ) -> AbstractFiniteAutomaton:
        """
        Optimise un automate pour une conversion vers un type spécifique.

        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :param target_type: Type d'automate cible
        :type target_type: str
        :return: Automate optimisé
        :rtype: AbstractFiniteAutomaton
        :raises OptimizationError: Si l'optimisation échoue
        """
        try:
            # Pour l'instant, retourner l'automate original
            # Cette méthode sera implémentée plus tard avec des optimisations spécifiques
            self._stats.add_optimization(
                f"optimize_for_conversion_{target_type}", 0.0, 0.0
            )

            return automaton

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de l'optimisation pour conversion: {e}"
            ) from e

    def reduce_epsilon_transitions(self, epsilon_nfa: EpsilonNFA) -> EpsilonNFA:
        """
        Réduit les transitions epsilon d'un ε-NFA.

        :param epsilon_nfa: ε-NFA à optimiser
        :type epsilon_nfa: EpsilonNFA
        :return: ε-NFA optimisé
        :rtype: EpsilonNFA
        :raises OptimizationError: Si l'optimisation échoue
        """
        if not isinstance(epsilon_nfa, EpsilonNFA):
            raise OptimizationError("L'automate doit être un ε-NFA")

        try:
            # Pour l'instant, retourner l'automate original
            # Cette méthode sera implémentée plus tard avec des optimisations spécifiques
            self._stats.add_optimization(
                "reduce_epsilon_transitions", 0.0, 0.0
            )

            return epsilon_nfa

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de la réduction des transitions epsilon: {e}"
            ) from e

    def optimize_data_structures(
        self, automaton: AbstractFiniteAutomaton
    ) -> AbstractFiniteAutomaton:
        """
        Optimise les structures de données d'un automate.

        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate avec structures optimisées
        :rtype: AbstractFiniteAutomaton
        :raises OptimizationError: Si l'optimisation échoue
        """
        try:
            # Pour l'instant, retourner l'automate original
            # Cette méthode sera implémentée plus tard avec des optimisations spécifiques
            self._stats.add_optimization(
                "optimize_data_structures", 0.0, 0.0
            )

            return automaton

        except Exception as e:
            if isinstance(e, OptimizationError):
                raise
            raise OptimizationError(
                f"Erreur lors de l'optimisation des structures: {e}"
            ) from e

    def validate_optimization(
        self, original: AbstractFiniteAutomaton, optimized: AbstractFiniteAutomaton
    ) -> bool:
        """
        Valide qu'une optimisation préserve l'équivalence des automates.

        :param original: Automate original
        :type original: AbstractFiniteAutomaton
        :param optimized: Automate optimisé
        :type optimized: AbstractFiniteAutomaton
        :return: True si les automates sont équivalents
        :rtype: bool
        """
        try:
            # Test sur un échantillon de mots
            test_words = self._generate_test_words(original, 100)

            for word in test_words:
                if original.accepts(word) != optimized.accepts(word):
                    return False

            return True

        except Exception:
            return False

    def get_optimization_stats(
        self, original: AbstractFiniteAutomaton, optimized: AbstractFiniteAutomaton
    ) -> Dict[str, Any]:
        """
        Récupère les statistiques d'optimisation.

        :param original: Automate original
        :type original: AbstractFiniteAutomaton
        :param optimized: Automate optimisé
        :type optimized: AbstractFiniteAutomaton
        :return: Dictionnaire des statistiques
        :rtype: Dict[str, Any]
        """
        return {
            "original_states": len(original.states),
            "optimized_states": len(optimized.states),
            "state_reduction": len(original.states) - len(optimized.states),
            "state_reduction_percent": (len(original.states) - len(optimized.states))
            / len(original.states)
            * 100,
            "optimization_stats": self._stats.get_stats(),
        }

    def clear_cache(self) -> None:
        """Vide le cache des optimisations."""
        self._cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques du cache.

        :return: Dictionnaire des statistiques du cache
        :rtype: Dict[str, Any]
        """
        return {"cache_size": len(self._cache), "cache_keys": list(self._cache.keys())}

    def set_cache_size(self, size: int) -> None:
        """
        Définit la taille maximale du cache.

        :param size: Taille maximale du cache
        :type size: int
        :raises OptimizationError: Si la taille est invalide
        """
        if size < 0:
            raise OptimizationError("La taille du cache doit être positive")

        # Pour l'instant, on ne limite pas la taille du cache
        # Cette fonctionnalité sera implémentée plus tard

    # Méthodes privées

    def _get_cache_key(self, automaton: AbstractFiniteAutomaton) -> str:
        """Génère une clé de cache pour un automate."""
        return f"{type(automaton).__name__}_{hash(str(automaton.to_dict()))}"

    def _hopcroft_minimization(self, dfa: DFA) -> DFA:
        """Implémente l'algorithme de minimisation de Hopcroft."""
        # Partition initiale : états finaux vs non-finaux
        partition = [dfa.final_states, dfa.states - dfa.final_states]

        # Éliminer les partitions vides
        partition = [p for p in partition if p]

        # Raffiner la partition
        worklist = [dfa.final_states] if dfa.final_states else []

        while worklist:
            current_set = worklist.pop(0)

            for symbol in dfa.alphabet:
                # Trouver les états qui ont une transition vers current_set avec symbol
                states_with_transition = set()
                for state in dfa.states:
                    target = dfa.get_transition(state, symbol)
                    if target in current_set:
                        states_with_transition.add(state)

                # Diviser chaque partition
                new_partition = []
                for partition_set in partition:
                    intersection = partition_set & states_with_transition
                    difference = partition_set - states_with_transition

                    if intersection and difference:
                        new_partition.append(intersection)
                        new_partition.append(difference)

                        # Ajouter la plus petite partition à la worklist
                        if len(intersection) <= len(difference):
                            worklist.append(intersection)
                        else:
                            worklist.append(difference)
                    else:
                        new_partition.append(partition_set)

                partition = new_partition

        # Construire le DFA minimal
        return self._build_minimal_dfa(dfa, partition)

    def _hopcroft_minimization_optimized(self, dfa: DFA) -> DFA:
        """Version optimisée de l'algorithme de Hopcroft."""
        # Pour l'instant, utiliser la version de base
        return self._hopcroft_minimization(dfa)

    def _build_minimal_dfa(self, original_dfa: DFA, partition: List[Set[str]]) -> DFA:
        """Construit un DFA minimal à partir d'une partition."""
        # Créer un mapping des états originaux vers les nouveaux états
        state_mapping = {}
        for i, partition_set in enumerate(partition):
            for state in partition_set:
                state_mapping[state] = f"q{i}"

        # Trouver l'état initial
        initial_state = None
        for partition_set in partition:
            if original_dfa.initial_state in partition_set:
                initial_state = state_mapping[original_dfa.initial_state]
                break

        # Trouver les états finaux
        final_states = set()
        for partition_set in partition:
            if partition_set & original_dfa.final_states:
                final_states.add(state_mapping[next(iter(partition_set))])

        # Construire les transitions
        new_transitions = {}
        for partition_set in partition:
            representative = next(iter(partition_set))
            new_state = state_mapping[representative]

            for symbol in original_dfa.alphabet:
                target = original_dfa.get_transition(representative, symbol)
                if target:
                    # Trouver la partition contenant target
                    for target_partition in partition:
                        if target in target_partition:
                            new_target = state_mapping[next(iter(target_partition))]
                            new_transitions[(new_state, symbol)] = new_target
                            break

        return DFA(
            states=set(state_mapping.values()),
            alphabet=original_dfa.alphabet,
            transitions=new_transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

    def _get_coaccessible_states(self, automaton: AbstractFiniteAutomaton) -> Set[str]:
        """Récupère les états cœurs d'un automate."""
        coaccessible = set(automaton.final_states)
        worklist = list(automaton.final_states)

        while worklist:
            current = worklist.pop(0)

            # Trouver tous les états qui ont une transition vers current
            for state in automaton.states:
                if state not in coaccessible:
                    for symbol in automaton.alphabet:
                        target = automaton.get_transition(state, symbol)
                        if target == current:
                            coaccessible.add(state)
                            worklist.append(state)
                            break

        return coaccessible

    def _remove_unreachable_states_dfa(
        self, dfa: DFA, reachable_states: Set[str]
    ) -> DFA:
        """Élimine les états inaccessibles d'un DFA."""
        # Filtrer les transitions
        new_transitions = {
            (state, symbol): target
            for (state, symbol), target in dfa.transitions.items()
            if state in reachable_states and target in reachable_states
        }

        # Filtrer les états finaux
        new_final_states = dfa.final_states & reachable_states

        return DFA(
            states=reachable_states,
            alphabet=dfa.alphabet,
            transitions=new_transitions,
            initial_state=dfa.initial_state,
            final_states=new_final_states,
        )

    def _remove_unreachable_states_nfa(
        self, nfa: NFA, reachable_states: Set[str]
    ) -> NFA:
        """Élimine les états inaccessibles d'un NFA."""
        # Filtrer les transitions
        new_transitions = {}
        for (state, symbol), targets in nfa.transitions.items():
            if state in reachable_states:
                new_targets = targets & reachable_states
                if new_targets:
                    new_transitions[(state, symbol)] = new_targets

        # Filtrer les états finaux
        new_final_states = nfa.final_states & reachable_states

        return NFA(
            states=reachable_states,
            alphabet=nfa.alphabet,
            transitions=new_transitions,
            initial_state=nfa.initial_state,
            final_states=new_final_states,
        )

    def _remove_unreachable_states_epsilon_nfa(
        self, epsilon_nfa: EpsilonNFA, reachable_states: Set[str]
    ) -> EpsilonNFA:
        """Élimine les états inaccessibles d'un ε-NFA."""
        # Filtrer les transitions
        new_transitions = {}
        for (state, symbol), targets in epsilon_nfa.transitions.items():
            if state in reachable_states:
                new_targets = targets & reachable_states
                if new_targets:
                    new_transitions[(state, symbol)] = new_targets

        # Filtrer les états finaux
        new_final_states = epsilon_nfa.final_states & reachable_states

        return EpsilonNFA(
            states=reachable_states,
            alphabet=epsilon_nfa.alphabet,
            transitions=new_transitions,
            initial_state=epsilon_nfa.initial_state,
            final_states=new_final_states,
            epsilon_symbol=epsilon_nfa.epsilon_symbol,
        )

    def _remove_coaccessible_states_dfa(
        self, dfa: DFA, coaccessible_states: Set[str]
    ) -> DFA:
        """Élimine les états non-cœurs d'un DFA."""
        # Filtrer les transitions
        new_transitions = {
            (state, symbol): target
            for (state, symbol), target in dfa.transitions.items()
            if state in coaccessible_states and target in coaccessible_states
        }

        # Filtrer les états finaux
        new_final_states = dfa.final_states & coaccessible_states

        return DFA(
            states=coaccessible_states,
            alphabet=dfa.alphabet,
            transitions=new_transitions,
            initial_state=dfa.initial_state,
            final_states=new_final_states,
        )

    def _remove_coaccessible_states_nfa(
        self, nfa: NFA, coaccessible_states: Set[str]
    ) -> NFA:
        """Élimine les états non-cœurs d'un NFA."""
        # Filtrer les transitions
        new_transitions = {}
        for (state, symbol), targets in nfa.transitions.items():
            if state in coaccessible_states:
                new_targets = targets & coaccessible_states
                if new_targets:
                    new_transitions[(state, symbol)] = new_targets

        # Filtrer les états finaux
        new_final_states = nfa.final_states & coaccessible_states

        return NFA(
            states=coaccessible_states,
            alphabet=nfa.alphabet,
            transitions=new_transitions,
            initial_state=nfa.initial_state,
            final_states=new_final_states,
        )

    def _remove_coaccessible_states_epsilon_nfa(
        self, epsilon_nfa: EpsilonNFA, coaccessible_states: Set[str]
    ) -> EpsilonNFA:
        """Élimine les états non-cœurs d'un ε-NFA."""
        # Filtrer les transitions
        new_transitions = {}
        for (state, symbol), targets in epsilon_nfa.transitions.items():
            if state in coaccessible_states:
                new_targets = targets & coaccessible_states
                if new_targets:
                    new_transitions[(state, symbol)] = new_targets

        # Filtrer les états finaux
        new_final_states = epsilon_nfa.final_states & coaccessible_states

        return EpsilonNFA(
            states=coaccessible_states,
            alphabet=epsilon_nfa.alphabet,
            transitions=new_transitions,
            initial_state=epsilon_nfa.initial_state,
            final_states=new_final_states,
            epsilon_symbol=epsilon_nfa.epsilon_symbol,
        )

    def _merge_identical_transitions_dfa(self, dfa: DFA) -> DFA:
        """Fusionne les transitions identiques d'un DFA."""
        # Pour un DFA, les transitions sont déjà uniques par (état, symbole)
        return dfa

    def _merge_identical_transitions_nfa(self, nfa: NFA) -> NFA:
        """Fusionne les transitions identiques d'un NFA."""
        # Fusionner les transitions identiques
        merged_transitions = {}
        for (state, symbol), targets in nfa.transitions.items():
            key = (state, symbol)
            if key in merged_transitions:
                merged_transitions[key] |= targets
            else:
                merged_transitions[key] = targets

        return NFA(
            states=nfa.states,
            alphabet=nfa.alphabet,
            transitions=merged_transitions,
            initial_state=nfa.initial_state,
            final_states=nfa.final_states,
        )

    def _merge_identical_transitions_epsilon_nfa(
        self, epsilon_nfa: EpsilonNFA
    ) -> EpsilonNFA:
        """Fusionne les transitions identiques d'un ε-NFA."""
        # Fusionner les transitions identiques
        merged_transitions = {}
        for (state, symbol), targets in epsilon_nfa.transitions.items():
            key = (state, symbol)
            if key in merged_transitions:
                merged_transitions[key] |= targets
            else:
                merged_transitions[key] = targets

        return EpsilonNFA(
            states=epsilon_nfa.states,
            alphabet=epsilon_nfa.alphabet,
            transitions=merged_transitions,
            initial_state=epsilon_nfa.initial_state,
            final_states=epsilon_nfa.final_states,
            epsilon_symbol=epsilon_nfa.epsilon_symbol,
        )

    def _validate_approximation(
        self,
        original: AbstractFiniteAutomaton,
        optimized: AbstractFiniteAutomaton,
        tolerance: float,
    ) -> bool:
        """
        Valide qu'une approximation respecte la tolérance.

        :param original: Automate original
        :type original: AbstractFiniteAutomaton
        :param optimized: Automate optimisé
        :type optimized: AbstractFiniteAutomaton
        :param tolerance: Tolérance acceptée
        :type tolerance: float
        :return: True si l'approximation est acceptable
        :rtype: bool
        """
        try:
            # Test sur un échantillon de mots
            test_words = self._generate_test_words(original, 100)

            errors = 0
            for word in test_words:
                if original.accepts(word) != optimized.accepts(word):
                    errors += 1

            error_rate = errors / len(test_words)
            return error_rate <= tolerance

        except Exception:
            return False

    def _generate_test_words(
        self, automaton: AbstractFiniteAutomaton, count: int
    ) -> List[str]:
        """Génère des mots de test pour la validation."""
        words = []
        alphabet = list(automaton.alphabet)

        # Générer des mots de différentes longueurs
        for length in range(min(5, count // 10 + 1)):
            for _ in range(count // 5):
                word = "".join(random.choice(alphabet) for _ in range(length))
                words.append(word)

        # Ajouter des mots spécifiques
        words.extend(["", "a", "b", "aa", "bb", "ab", "ba"])

        return words[:count]


class OptimizationStats:
    """
    Classe pour collecter les statistiques d'optimisation.

    Cette classe permet de suivre les performances des algorithmes
    d'optimisation et de générer des rapports.
    """

    def __init__(self) -> None:
        """Initialise les statistiques d'optimisation."""
        self._optimizations: List[Dict[str, Any]] = []

    def add_optimization(
        self, optimization_type: str, time_taken: float, improvement: float
    ) -> None:
        """
        Ajoute une optimisation aux statistiques.

        :param optimization_type: Type d'optimisation
        :type optimization_type: str
        :param time_taken: Temps pris par l'optimisation
        :type time_taken: float
        :param improvement: Amélioration en pourcentage
        :type improvement: float
        """
        self._optimizations.append(
            {
                "type": optimization_type,
                "time": time_taken,
                "improvement": improvement,
                "timestamp": time.time(),
            }
        )

    def get_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques d'optimisation.

        :return: Dictionnaire des statistiques
        :rtype: Dict[str, Any]
        """
        if not self._optimizations:
            return {"total_optimizations": 0}

        total_time = sum(opt["time"] for opt in self._optimizations)
        avg_time = total_time / len(self._optimizations)
        avg_improvement = sum(opt["improvement"] for opt in self._optimizations) / len(
            self._optimizations
        )

        return {
            "total_optimizations": len(self._optimizations),
            "total_time": total_time,
            "average_time": avg_time,
            "average_improvement": avg_improvement,
            "optimizations_by_type": self._get_optimizations_by_type(),
        }

    def _get_optimizations_by_type(self) -> Dict[str, Dict[str, Any]]:
        """Récupère les statistiques par type d'optimisation."""
        by_type = {}
        for opt in self._optimizations:
            opt_type = opt["type"]
            if opt_type not in by_type:
                by_type[opt_type] = {
                    "count": 0,
                    "total_time": 0.0,
                    "total_improvement": 0.0,
                }

            by_type[opt_type]["count"] += 1
            by_type[opt_type]["total_time"] += opt["time"]
            by_type[opt_type]["total_improvement"] += opt["improvement"]

        # Calculer les moyennes
        for opt_type in by_type:
            count = by_type[opt_type]["count"]
            by_type[opt_type]["average_time"] = by_type[opt_type]["total_time"] / count
            by_type[opt_type]["average_improvement"] = (
                by_type[opt_type]["total_improvement"] / count
            )

        return by_type

    def reset(self) -> None:
        """Remet à zéro les statistiques."""
        self._optimizations.clear()


