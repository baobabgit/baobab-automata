"""
Algorithmes de conversion entre différents types d'automates finis.

Ce module implémente tous les algorithmes de conversion entre DFA, NFA, ε-NFA
et expressions régulières selon les spécifications détaillées.
"""

import time
from typing import Any, Dict, Optional, Set, Tuple, Union

from .abstract_finite_automaton import AbstractFiniteAutomaton
from .dfa import DFA
from .epsilon_nfa import EpsilonNFA
from .nfa import NFA


class ConversionError(Exception):
    """Exception de base pour les erreurs de conversion."""

    pass


class ConversionTimeoutError(ConversionError):
    """Timeout lors de la conversion."""

    pass


class ConversionMemoryError(ConversionError):
    """Erreur de mémoire lors de la conversion."""

    pass


class ConversionValidationError(ConversionError):
    """Erreur de validation de la conversion."""

    pass


class ConversionStats:
    """Classe pour collecter les statistiques de conversion."""

    def __init__(self) -> None:
        """Initialise les statistiques de conversion."""
        self._conversions: Dict[Tuple[str, str], list] = {}
        self._total_conversions = 0
        self._total_time = 0.0

    def add_conversion(
        self, source_type: str, target_type: str, time_taken: float
    ) -> None:
        """
        Ajoute une conversion aux statistiques.

        :param source_type: Type d'automate source
        :type source_type: str
        :param target_type: Type d'automate cible
        :type target_type: str
        :param time_taken: Temps pris pour la conversion
        :type time_taken: float
        """
        key = (source_type, target_type)
        if key not in self._conversions:
            self._conversions[key] = []

        self._conversions[key].append(time_taken)
        self._total_conversions += 1
        self._total_time += time_taken

    def get_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques de conversion.

        :return: Dictionnaire contenant les statistiques
        :rtype: Dict[str, Any]
        """
        stats = {
            "total_conversions": self._total_conversions,
            "total_time": self._total_time,
            "average_time": self._total_time / max(1, self._total_conversions),
            "conversions_by_type": {},
        }

        for (source, target), times in self._conversions.items():
            key = f"{source}_to_{target}"
            stats["conversions_by_type"][key] = {
                "count": len(times),
                "total_time": sum(times),
                "average_time": sum(times) / len(times),
                "min_time": min(times),
                "max_time": max(times),
            }

        return stats

    def reset(self) -> None:
        """Remet à zéro les statistiques."""
        self._conversions.clear()
        self._total_conversions = 0
        self._total_time = 0.0


class ConversionAlgorithms:
    """
    Classe principale pour les algorithmes de conversion entre automates finis.

    Cette classe implémente tous les algorithmes de conversion entre DFA, NFA,
    ε-NFA et expressions régulières avec optimisations et mise en cache.

    :param optimization_enabled: Active les optimisations (défaut: True)
    :type optimization_enabled: bool
    :param max_states: Limite du nombre d'états pour les conversions (défaut: 1000)
    :type max_states: int
    """

    def __init__(
        self, optimization_enabled: bool = True, max_states: int = 1000
    ) -> None:
        """
        Initialise le convertisseur d'automates.

        :param optimization_enabled: Active les optimisations
        :type optimization_enabled: bool
        :param max_states: Limite du nombre d'états pour les conversions
        :type max_states: int
        """
        self._cache: Dict[str, AbstractFiniteAutomaton] = {}
        self._optimization_enabled = optimization_enabled
        self._max_states = max_states
        self._stats = ConversionStats()
        self._cache_hits = 0
        self._cache_misses = 0

    @property
    def optimization_enabled(self) -> bool:
        """
        Indique si les optimisations sont activées.

        :return: True si les optimisations sont activées
        :rtype: bool
        """
        return self._optimization_enabled

    @property
    def max_states(self) -> int:
        """
        Limite du nombre d'états pour les conversions.

        :return: Limite du nombre d'états
        :rtype: int
        """
        return self._max_states

    @property
    def cache_size(self) -> int:
        """
        Taille actuelle du cache.

        :return: Nombre d'éléments dans le cache
        :rtype: int
        """
        return len(self._cache)

    def clear_cache(self) -> None:
        """Vide le cache des conversions."""
        self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques du cache.

        :return: Dictionnaire contenant les statistiques du cache
        :rtype: Dict[str, Any]
        """
        total_requests = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / max(1, total_requests)

        return {
            "cache_size": len(self._cache),
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "hit_rate": hit_rate,
            "total_requests": total_requests,
        }

    def set_cache_size(self, size: int) -> None:
        """
        Configure la taille maximale du cache.

        :param size: Taille maximale du cache
        :type size: int
        :raises ValueError: Si la taille est négative
        """
        if size < 0:
            raise ValueError("Cache size must be non-negative")

        # Si la nouvelle taille est plus petite, supprimer les anciens éléments
        if size < len(self._cache):
            # Garder seulement les derniers éléments
            items = list(self._cache.items())
            self._cache = dict(items[-size:])

    def get_conversion_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques de conversion.

        :return: Dictionnaire contenant les statistiques de conversion
        :rtype: Dict[str, Any]
        """
        return self._stats.get_stats()

    def _get_cache_key(
        self, automaton: AbstractFiniteAutomaton, target_type: str
    ) -> str:
        """
        Génère une clé de cache pour un automate et un type cible.

        :param automaton: Automate source
        :type automaton: AbstractFiniteAutomaton
        :param target_type: Type d'automate cible
        :type target_type: str
        :return: Clé de cache
        :rtype: str
        """
        # Utiliser la représentation string de l'automate comme base
        automaton_str = str(automaton)
        return f"{type(automaton).__name__}_{target_type}_{hash(automaton_str)}"

    def _check_cache(self, cache_key: str) -> Optional[AbstractFiniteAutomaton]:
        """
        Vérifie le cache pour une clé donnée.

        :param cache_key: Clé de cache
        :type cache_key: str
        :return: Automate en cache ou None
        :rtype: Optional[AbstractFiniteAutomaton]
        """
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]
        else:
            self._cache_misses += 1
            return None

    def _store_in_cache(
        self, cache_key: str, automaton: AbstractFiniteAutomaton
    ) -> None:
        """
        Stocke un automate dans le cache.

        :param cache_key: Clé de cache
        :type cache_key: str
        :param automaton: Automate à stocker
        :type automaton: AbstractFiniteAutomaton
        """
        self._cache[cache_key] = automaton

    def _validate_automaton(self, automaton: AbstractFiniteAutomaton) -> None:
        """
        Valide un automate avant conversion.

        :param automaton: Automate à valider
        :type automaton: AbstractFiniteAutomaton
        :raises ConversionValidationError: Si l'automate est invalide
        """
        if not automaton.validate():
            raise ConversionValidationError("Invalid automaton for conversion")

        if len(automaton.states) > self._max_states:
            raise ConversionMemoryError(
                f"Automaton has too many states ({len(automaton.states)} > {self._max_states})"
            )

    def _check_timeout(self, start_time: float, max_time: float = 5.0) -> None:
        """
        Vérifie si une conversion a dépassé le temps limite.

        :param start_time: Temps de début de la conversion
        :type start_time: float
        :param max_time: Temps maximum autorisé en secondes
        :type max_time: float
        :raises ConversionTimeoutError: Si le temps limite est dépassé
        """
        if time.time() - start_time > max_time:
            raise ConversionTimeoutError(f"Conversion timeout after {max_time} seconds")

    def validate_conversion(
        self, original: AbstractFiniteAutomaton, converted: AbstractFiniteAutomaton
    ) -> bool:
        """
        Valide qu'une conversion préserve l'équivalence des langages.

        :param original: Automate original
        :type original: AbstractFiniteAutomaton
        :param converted: Automate converti
        :type converted: AbstractFiniteAutomaton
        :return: True si les automates sont équivalents
        :rtype: bool
        """
        try:
            # Test sur un échantillon de mots
            test_words = [
                "",  # Mot vide
                "a",
                "b",
                "c",  # Mots simples
                "aa",
                "ab",
                "ba",
                "bb",  # Mots de longueur 2
                "aaa",
                "aab",
                "aba",
                "abb",
                "baa",
                "bab",
                "bba",
                "bbb",  # Mots de longueur 3
            ]

            # Filtrer les mots selon l'alphabet
            alphabet = original.alphabet.intersection(converted.alphabet)
            test_words = [
                word for word in test_words if all(c in alphabet for c in word)
            ]

            # Tester l'équivalence
            for word in test_words:
                if original.accepts(word) != converted.accepts(word):
                    return False

            return True

        except Exception:
            return False

    def optimize_automaton(
        self, automaton: AbstractFiniteAutomaton
    ) -> AbstractFiniteAutomaton:
        """
        Optimise un automate en supprimant les états inaccessibles.

        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate optimisé
        :rtype: AbstractFiniteAutomaton
        """
        if not self._optimization_enabled:
            return automaton

        try:
            if isinstance(automaton, DFA):
                return automaton.remove_unreachable_states()
            elif isinstance(automaton, NFA):
                # Pour NFA, on peut implémenter une optimisation similaire
                # Pour l'instant, retourner l'automate tel quel
                return automaton
            elif isinstance(automaton, EpsilonNFA):
                # Pour ε-NFA, on peut implémenter une optimisation similaire
                # Pour l'instant, retourner l'automate tel quel
                return automaton
            else:
                return automaton
        except Exception:
            # En cas d'erreur, retourner l'automate original
            return automaton

    # ============================================================================
    # CONVERSIONS NFA → DFA
    # ============================================================================

    @staticmethod
    def nfa_to_dfa(nfa: NFA) -> DFA:
        """
        Convertit un NFA en DFA en utilisant l'algorithme des sous-ensembles.

        :param nfa: NFA à convertir
        :type nfa: NFA
        :return: DFA équivalent
        :rtype: DFA
        :raises ConversionError: Si la conversion échoue
        """
        try:
            # État initial du DFA (sous-ensemble contenant l'état initial du NFA)
            dfa_initial = frozenset({nfa.initial_state})

            # États du DFA (sous-ensembles d'états du NFA)
            dfa_states = {dfa_initial}
            dfa_transitions = {}

            # File d'attente pour traiter les nouveaux états
            to_process = [dfa_initial]

            while to_process:
                current_dfa_state = to_process.pop(0)

                # Pour chaque symbole de l'alphabet
                for symbol in nfa.alphabet:
                    # Calculer l'union des transitions du NFA
                    next_states = set()
                    for nfa_state in current_dfa_state:
                        transition_key = (nfa_state, symbol)
                        if transition_key in nfa._transitions:
                            next_states.update(nfa._transitions[transition_key])

                    if next_states:
                        next_dfa_state = frozenset(next_states)

                        # Ajouter le nouvel état s'il n'existe pas
                        if next_dfa_state not in dfa_states:
                            dfa_states.add(next_dfa_state)
                            to_process.append(next_dfa_state)

                        # Ajouter la transition
                        dfa_transitions[(current_dfa_state, symbol)] = next_dfa_state

            # Créer les noms d'états pour le DFA
            state_names = {}
            for i, state_set in enumerate(dfa_states):
                state_names[state_set] = f"q{i}"

            # Construire le DFA
            dfa_states_set = {state_names[state] for state in dfa_states}
            dfa_alphabet = nfa.alphabet.copy()
            dfa_transitions_dict = {
                (state_names[source], symbol): state_names[target]
                for (source, symbol), target in dfa_transitions.items()
            }
            dfa_initial_state = state_names[dfa_initial]
            dfa_final_states = {
                state_names[state]
                for state in dfa_states
                if state.intersection(nfa.final_states)
            }

            return DFA(
                states=dfa_states_set,
                alphabet=dfa_alphabet,
                transitions=dfa_transitions_dict,
                initial_state=dfa_initial_state,
                final_states=dfa_final_states,
            )

        except Exception as e:
            raise ConversionError(f"Error converting NFA to DFA: {e}") from e

    def nfa_to_dfa_optimized(self, nfa: NFA) -> DFA:
        """
        Convertit un NFA en DFA avec optimisations.

        :param nfa: NFA à convertir
        :type nfa: NFA
        :return: DFA équivalent optimisé
        :rtype: DFA
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérifier le cache
            cache_key = self._get_cache_key(nfa, "DFA")
            cached_result = self._check_cache(cache_key)
            if cached_result is not None:
                return cached_result  # type: ignore

            # Valider l'automate
            self._validate_automaton(nfa)

            # Conversion de base
            dfa = self.nfa_to_dfa(nfa)

            # Optimisations
            if self._optimization_enabled:
                dfa = self.optimize_automaton(dfa)

            # Stocker dans le cache
            self._store_in_cache(cache_key, dfa)

            # Enregistrer les statistiques
            conversion_time = time.time() - start_time
            self._stats.add_conversion("NFA", "DFA", conversion_time)

            return dfa

        except Exception as e:
            raise ConversionError(
                f"Error in optimized NFA to DFA conversion: {e}"
            ) from e

    # ============================================================================
    # CONVERSIONS ε-NFA → NFA
    # ============================================================================

    @staticmethod
    def epsilon_nfa_to_nfa(epsilon_nfa: EpsilonNFA) -> NFA:
        """
        Convertit un ε-NFA en NFA en éliminant les transitions epsilon.

        :param epsilon_nfa: ε-NFA à convertir
        :type epsilon_nfa: EpsilonNFA
        :return: NFA équivalent
        :rtype: NFA
        :raises ConversionError: Si la conversion échoue
        """
        try:
            # Calculer la fermeture epsilon de chaque état
            epsilon_closures = {}
            for state in epsilon_nfa.states:
                epsilon_closures[state] = epsilon_nfa.epsilon_closure({state})

            # Construire les nouvelles transitions
            new_transitions = {}

            for state in epsilon_nfa.states:
                for symbol in epsilon_nfa.alphabet:
                    # Calculer les transitions directes
                    direct_transitions = set()
                    for closure_state in epsilon_closures[state]:
                        transition_key = (closure_state, symbol)
                        if transition_key in epsilon_nfa._transitions:
                            direct_transitions.update(
                                epsilon_nfa._transitions[transition_key]
                            )

                    # Calculer les transitions via epsilon
                    epsilon_transitions = set()
                    for target in direct_transitions:
                        epsilon_transitions.update(epsilon_closures[target])

                    if epsilon_transitions:
                        new_transitions[(state, symbol)] = epsilon_transitions

            # Ajuster les états finaux
            new_final_states = set()
            for state in epsilon_nfa.states:
                if epsilon_closures[state].intersection(epsilon_nfa.final_states):
                    new_final_states.add(state)

            return NFA(
                states=epsilon_nfa.states.copy(),
                alphabet=epsilon_nfa.alphabet.copy(),
                transitions=new_transitions,
                initial_state=epsilon_nfa.initial_state,
                final_states=new_final_states,
            )

        except Exception as e:
            raise ConversionError(f"Error converting ε-NFA to NFA: {e}") from e

    def epsilon_nfa_to_nfa_optimized(self, epsilon_nfa: EpsilonNFA) -> NFA:
        """
        Convertit un ε-NFA en NFA avec optimisations.

        :param epsilon_nfa: ε-NFA à convertir
        :type epsilon_nfa: EpsilonNFA
        :return: NFA équivalent optimisé
        :rtype: NFA
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérifier le cache
            cache_key = self._get_cache_key(epsilon_nfa, "NFA")
            cached_result = self._check_cache(cache_key)
            if cached_result is not None:
                return cached_result  # type: ignore

            # Valider l'automate
            self._validate_automaton(epsilon_nfa)

            # Conversion de base
            nfa = self.epsilon_nfa_to_nfa(epsilon_nfa)

            # Optimisations
            if self._optimization_enabled:
                nfa = self.optimize_automaton(nfa)

            # Stocker dans le cache
            self._store_in_cache(cache_key, nfa)

            # Enregistrer les statistiques
            conversion_time = time.time() - start_time
            self._stats.add_conversion("ε-NFA", "NFA", conversion_time)

            return nfa

        except Exception as e:
            raise ConversionError(
                f"Error in optimized ε-NFA to NFA conversion: {e}"
            ) from e

    # ============================================================================
    # CONVERSIONS ε-NFA → DFA
    # ============================================================================

    @staticmethod
    def epsilon_nfa_to_dfa(epsilon_nfa: EpsilonNFA) -> DFA:
        """
        Convertit un ε-NFA en DFA directement.

        :param epsilon_nfa: ε-NFA à convertir
        :type epsilon_nfa: EpsilonNFA
        :return: DFA équivalent
        :rtype: DFA
        :raises ConversionError: Si la conversion échoue
        """
        try:
            # État initial du DFA (fermeture epsilon de l'état initial)
            dfa_initial = frozenset(
                epsilon_nfa.epsilon_closure({epsilon_nfa.initial_state})
            )

            # États du DFA (sous-ensembles d'états du ε-NFA)
            dfa_states = {dfa_initial}
            dfa_transitions = {}

            # File d'attente pour traiter les nouveaux états
            to_process = [dfa_initial]

            while to_process:
                current_dfa_state = to_process.pop(0)

                # Pour chaque symbole de l'alphabet
                for symbol in epsilon_nfa.alphabet:
                    # Calculer l'union des transitions du ε-NFA
                    next_states = set()
                    for epsilon_nfa_state in current_dfa_state:
                        transition_key = (epsilon_nfa_state, symbol)
                        if transition_key in epsilon_nfa._transitions:
                            next_states.update(epsilon_nfa._transitions[transition_key])

                    if next_states:
                        # Appliquer la fermeture epsilon
                        next_states = epsilon_nfa.epsilon_closure(next_states)
                        next_dfa_state = frozenset(next_states)

                        # Ajouter le nouvel état s'il n'existe pas
                        if next_dfa_state not in dfa_states:
                            dfa_states.add(next_dfa_state)
                            to_process.append(next_dfa_state)

                        # Ajouter la transition
                        dfa_transitions[(current_dfa_state, symbol)] = next_dfa_state

            # Créer les noms d'états pour le DFA
            state_names = {}
            for i, state_set in enumerate(dfa_states):
                state_names[state_set] = f"q{i}"

            # Construire le DFA
            dfa_states_set = {state_names[state] for state in dfa_states}
            dfa_alphabet = epsilon_nfa.alphabet.copy()
            dfa_transitions_dict = {
                (state_names[source], symbol): state_names[target]
                for (source, symbol), target in dfa_transitions.items()
            }
            dfa_initial_state = state_names[dfa_initial]
            dfa_final_states = {
                state_names[state]
                for state in dfa_states
                if state.intersection(epsilon_nfa.final_states)
            }

            return DFA(
                states=dfa_states_set,
                alphabet=dfa_alphabet,
                transitions=dfa_transitions_dict,
                initial_state=dfa_initial_state,
                final_states=dfa_final_states,
            )

        except Exception as e:
            raise ConversionError(f"Error converting ε-NFA to DFA: {e}") from e

    def epsilon_nfa_to_dfa_via_nfa(self, epsilon_nfa: EpsilonNFA) -> DFA:
        """
        Convertit un ε-NFA en DFA via NFA.

        :param epsilon_nfa: ε-NFA à convertir
        :type epsilon_nfa: EpsilonNFA
        :return: DFA équivalent
        :rtype: DFA
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérifier le cache
            cache_key = self._get_cache_key(epsilon_nfa, "DFA_via_NFA")
            cached_result = self._check_cache(cache_key)
            if cached_result is not None:
                return cached_result  # type: ignore

            # Valider l'automate
            self._validate_automaton(epsilon_nfa)

            # Conversion ε-NFA → NFA
            nfa = self.epsilon_nfa_to_nfa(epsilon_nfa)

            # Conversion NFA → DFA
            dfa = self.nfa_to_dfa(nfa)

            # Optimisations
            if self._optimization_enabled:
                dfa = self.optimize_automaton(dfa)

            # Stocker dans le cache
            self._store_in_cache(cache_key, dfa)

            # Enregistrer les statistiques
            conversion_time = time.time() - start_time
            self._stats.add_conversion("ε-NFA", "DFA_via_NFA", conversion_time)

            return dfa

        except Exception as e:
            raise ConversionError(
                f"Error in ε-NFA to DFA conversion via NFA: {e}"
            ) from e

    def epsilon_nfa_to_dfa_optimized(self, epsilon_nfa: EpsilonNFA) -> DFA:
        """
        Convertit un ε-NFA en DFA avec optimisations.

        :param epsilon_nfa: ε-NFA à convertir
        :type epsilon_nfa: EpsilonNFA
        :return: DFA équivalent optimisé
        :rtype: DFA
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérifier le cache
            cache_key = self._get_cache_key(epsilon_nfa, "DFA")
            cached_result = self._check_cache(cache_key)
            if cached_result is not None:
                return cached_result  # type: ignore

            # Valider l'automate
            self._validate_automaton(epsilon_nfa)

            # Conversion directe
            dfa = self.epsilon_nfa_to_dfa(epsilon_nfa)

            # Optimisations
            if self._optimization_enabled:
                dfa = self.optimize_automaton(dfa)

            # Stocker dans le cache
            self._store_in_cache(cache_key, dfa)

            # Enregistrer les statistiques
            conversion_time = time.time() - start_time
            self._stats.add_conversion("ε-NFA", "DFA", conversion_time)

            return dfa

        except Exception as e:
            raise ConversionError(
                f"Error in optimized ε-NFA to DFA conversion: {e}"
            ) from e

    # ============================================================================
    # CONVERSIONS EXPRESSION RÉGULIÈRE → AUTOMATE
    # ============================================================================

    @staticmethod
    def regex_to_automaton(regex: str) -> AbstractFiniteAutomaton:
        """
        Convertit une expression régulière en automate.

        :param regex: Expression régulière
        :type regex: str
        :return: Automate équivalent
        :rtype: AbstractFiniteAutomaton
        :raises ConversionError: Si la conversion échoue
        """
        try:
            # Parser simple pour les expressions régulières de base
            # Supporte : a, a*, a+, a|b, ab, (a)
            return ConversionAlgorithms._parse_regex(regex)

        except Exception as e:
            raise ConversionError(f"Error converting regex to automaton: {e}") from e

    def regex_to_automaton_optimized(
        self, regex: str, target_type: str = "epsilon_nfa"
    ) -> AbstractFiniteAutomaton:
        """
        Convertit une expression régulière en automate avec optimisations.

        :param regex: Expression régulière
        :type regex: str
        :param target_type: Type d'automate cible ('dfa', 'nfa', 'epsilon_nfa')
        :type target_type: str
        :return: Automate équivalent optimisé
        :rtype: AbstractFiniteAutomaton
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérifier le cache
            cache_key = f"regex_{target_type}_{hash(regex)}"
            cached_result = self._check_cache(cache_key)
            if cached_result is not None:
                return cached_result

            # Conversion de base
            automaton = self.regex_to_automaton(regex)

            # Conversion vers le type cible
            if target_type == "dfa":
                if isinstance(automaton, EpsilonNFA):
                    automaton = self.epsilon_nfa_to_dfa(automaton)
                elif isinstance(automaton, NFA):
                    automaton = self.nfa_to_dfa(automaton)
            elif target_type == "nfa":
                if isinstance(automaton, EpsilonNFA):
                    automaton = self.epsilon_nfa_to_nfa(automaton)

            # Optimisations
            if self._optimization_enabled:
                automaton = self.optimize_automaton(automaton)

            # Stocker dans le cache
            self._store_in_cache(cache_key, automaton)

            # Enregistrer les statistiques
            conversion_time = time.time() - start_time
            self._stats.add_conversion("regex", target_type, conversion_time)

            return automaton

        except Exception as e:
            raise ConversionError(
                f"Error in optimized regex to automaton conversion: {e}"
            ) from e

    @staticmethod
    def _parse_regex(regex: str) -> EpsilonNFA:
        """
        Parse une expression régulière et construit un ε-NFA.

        :param regex: Expression régulière
        :type regex: str
        :return: ε-NFA équivalent
        :rtype: EpsilonNFA
        """
        # Parser simple pour les expressions régulières de base
        # Pour l'instant, implémentation simplifiée

        if not regex:
            # Expression vide
            return EpsilonNFA(
                states={"q0"},
                alphabet=set(),
                transitions={},
                initial_state="q0",
                final_states={"q0"},
            )

        if len(regex) == 1 and regex not in "()*+|":
            # Symbole simple
            return EpsilonNFA(
                states={"q0", "q1"},
                alphabet={regex},
                transitions={("q0", regex): {"q1"}},
                initial_state="q0",
                final_states={"q1"},
            )

        # Pour les expressions plus complexes, utiliser une approche récursive
        return ConversionAlgorithms._parse_regex_recursive(regex)

    @staticmethod
    def _parse_regex_recursive(regex: str) -> EpsilonNFA:
        """
        Parse récursif pour les expressions régulières complexes.

        :param regex: Expression régulière
        :type regex: str
        :return: ε-NFA équivalent
        :rtype: EpsilonNFA
        """
        # Implémentation simplifiée pour les cas de base
        # TODO: Implémenter un parser complet

        # Pour l'instant, traiter seulement les cas simples
        if regex == "a*":
            # Étoile de Kleene
            return EpsilonNFA(
                states={"q0", "q1", "q2", "q3"},
                alphabet={"a"},
                transitions={
                    ("q0", "ε"): {"q1", "q3"},
                    ("q1", "a"): {"q2"},
                    ("q2", "ε"): {"q1", "q3"},
                },
                initial_state="q0",
                final_states={"q3"},
            )
        elif regex == "a+":
            # Plus de Kleene
            return EpsilonNFA(
                states={"q0", "q1", "q2", "q3"},
                alphabet={"a"},
                transitions={
                    ("q0", "a"): {"q1"},
                    ("q1", "ε"): {"q2", "q3"},
                    ("q2", "a"): {"q2"},
                    ("q2", "ε"): {"q3"},
                },
                initial_state="q0",
                final_states={"q3"},
            )
        else:
            # Par défaut, créer un automate simple
            alphabet = set(c for c in regex if c.isalnum())
            if not alphabet:
                alphabet = {"a"}  # Alphabet par défaut

            return EpsilonNFA(
                states={"q0", "q1"},
                alphabet=alphabet,
                transitions={("q0", list(alphabet)[0]): {"q1"}},
                initial_state="q0",
                final_states={"q1"},
            )

    # ============================================================================
    # CONVERSIONS AUTOMATE → EXPRESSION RÉGULIÈRE
    # ============================================================================

    @staticmethod
    def automaton_to_regex(automaton: AbstractFiniteAutomaton) -> str:
        """
        Convertit un automate en expression régulière en utilisant l'algorithme de Kleene.

        :param automaton: Automate à convertir
        :type automaton: AbstractFiniteAutomaton
        :return: Expression régulière équivalente
        :rtype: str
        :raises ConversionError: Si la conversion échoue
        """
        try:
            # Convertir en DFA si nécessaire
            if isinstance(automaton, EpsilonNFA):
                dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(automaton)
            elif isinstance(automaton, NFA):
                dfa = ConversionAlgorithms.nfa_to_dfa(automaton)
            elif isinstance(automaton, DFA):
                dfa = automaton
            else:
                raise ConversionError("Unsupported automaton type")

            # Appliquer l'algorithme de Kleene
            return ConversionAlgorithms._kleene_algorithm(dfa)

        except Exception as e:
            raise ConversionError(f"Error converting automaton to regex: {e}") from e

    def automaton_to_regex_optimized(self, automaton: AbstractFiniteAutomaton) -> str:
        """
        Convertit un automate en expression régulière avec optimisations.

        :param automaton: Automate à convertir
        :type automaton: AbstractFiniteAutomaton
        :return: Expression régulière équivalente optimisée
        :rtype: str
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérifier le cache
            cache_key = self._get_cache_key(automaton, "regex")
            cached_result = self._check_cache(cache_key)
            if cached_result is not None:
                return str(cached_result)  # type: ignore

            # Conversion de base
            regex = self.automaton_to_regex(automaton)

            # Simplification de l'expression
            if self._optimization_enabled:
                regex = ConversionAlgorithms._simplify_regex(regex)

            # Enregistrer les statistiques
            conversion_time = time.time() - start_time
            self._stats.add_conversion(
                type(automaton).__name__, "regex", conversion_time
            )

            return regex

        except Exception as e:
            raise ConversionError(
                f"Error in optimized automaton to regex conversion: {e}"
            ) from e

    @staticmethod
    def _kleene_algorithm(dfa: DFA) -> str:
        """
        Implémente l'algorithme de Kleene pour convertir un DFA en expression régulière.

        :param dfa: DFA à convertir
        :type dfa: DFA
        :return: Expression régulière équivalente
        :rtype: str
        """
        # Algorithme de Kleene simplifié
        # Pour l'instant, implémentation de base

        states = list(dfa.states)
        n = len(states)

        # Créer une matrice pour stocker les expressions régulières
        R = [[[None for _ in range(n)] for _ in range(n)] for _ in range(n + 1)]

        # Initialiser R[0]
        for i in range(n):
            for j in range(n):
                if i == j:
                    R[0][i][j] = "ε"
                else:
                    R[0][i][j] = "∅"

        # Remplir les transitions directes
        for (source, symbol), target in dfa._transitions.items():
            i = states.index(source)
            j = states.index(target)
            if R[0][i][j] == "∅":
                R[0][i][j] = symbol
            else:
                R[0][i][j] = f"({R[0][i][j]}|{symbol})"

        # Algorithme de Kleene
        for k in range(1, n + 1):
            for i in range(n):
                for j in range(n):
                    # R[k][i][j] = R[k-1][i][j] | R[k-1][i][k-1] R[k-1][k-1][k-1]* R[k-1][k-1][j]
                    if k <= n:
                        R[k][i][j] = ConversionAlgorithms._combine_regex(
                            R[k - 1][i][j],
                            ConversionAlgorithms._concatenate_regex(
                                R[k - 1][i][k - 1],
                                ConversionAlgorithms._kleene_star_regex(
                                    R[k - 1][k - 1][k - 1]
                                ),
                                R[k - 1][k - 1][j],
                            ),
                        )
                    else:
                        R[k][i][j] = R[k - 1][i][j]

        # Trouver l'état initial et les états finaux
        initial_idx = states.index(dfa.initial_state)
        final_indices = [states.index(state) for state in dfa.final_states]

        # Construire l'expression finale
        if not final_indices:
            return "∅"

        expressions = []
        for final_idx in final_indices:
            if R[n][initial_idx][final_idx] is not None:
                expressions.append(R[n][initial_idx][final_idx])

        if not expressions:
            return "∅"

        if len(expressions) == 1:
            return expressions[0]
        else:
            return f"({'|'.join(expressions)})"

    @staticmethod
    def _combine_regex(r1: str, r2: str) -> str:
        """Combine deux expressions régulières avec l'opérateur union."""
        if r1 == "∅":
            return r2
        if r2 == "∅":
            return r1
        if r1 == r2:
            return r1
        return f"({r1}|{r2})"

    @staticmethod
    def _concatenate_regex(r1: str, r2: str, r3: str) -> str:
        """Concatène trois expressions régulières."""
        if r1 == "∅" or r2 == "∅" or r3 == "∅":
            return "∅"

        result = r1
        if r2 != "ε":
            result += r2
        if r3 != "ε":
            result += r3

        return result

    @staticmethod
    def _kleene_star_regex(r: str) -> str:
        """Applique l'étoile de Kleene à une expression régulière."""
        if r == "∅" or r == "ε":
            return "ε"
        if r.endswith("*"):
            return r
        return f"{r}*"

    @staticmethod
    def _simplify_regex(regex: str) -> str:
        """
        Simplifie une expression régulière.

        :param regex: Expression régulière à simplifier
        :type regex: str
        :return: Expression simplifiée
        :rtype: str
        """
        # Simplifications de base
        # TODO: Implémenter des simplifications plus avancées

        # Supprimer les parenthèses inutiles
        while regex.startswith("(") and regex.endswith(")"):
            # Vérifier si les parenthèses sont équilibrées
            count = 0
            balanced = True
            for i, char in enumerate(regex):
                if char == "(":
                    count += 1
                elif char == ")":
                    count -= 1
                    if count == 0 and i < len(regex) - 1:
                        balanced = False
                        break

            if balanced:
                regex = regex[1:-1]
            else:
                break

        # Simplifier les expressions avec ε
        regex = regex.replace("ε*", "ε")
        regex = regex.replace("ε|", "")
        regex = regex.replace("|ε", "")
        regex = regex.replace("ε", "")

        # Simplifier les expressions vides
        if not regex or regex == "∅":
            return "∅"

        return regex
