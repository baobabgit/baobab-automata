"""
Opérations sur les langages réguliers.

Ce module implémente la classe LanguageOperations qui fournit toutes
les opérations de base et avancées sur les langages réguliers.
"""

from typing import Any, Dict, Optional

from .abstract_finite_automaton import AbstractFiniteAutomaton
from .dfa import DFA
from .language_operations_exceptions import (
    IncompatibleAutomataError,
    OperationValidationError,
)
from .mapping import Mapping
from .nfa import NFA
from .operation_stats import OperationStats


class LanguageOperations:
    """
    Classe principale pour les opérations sur les langages réguliers.

    Cette classe fournit toutes les opérations de base et avancées
    sur les langages réguliers, incluant l'union, l'intersection,
    la complémentation, la concaténation, l'étoile de Kleene,
    les homomorphismes et d'autres opérations spécialisées.

    :param optimization_enabled: Active les optimisations (défaut: True)
    :type optimization_enabled: bool
    :param max_states: Limite du nombre d'états pour les opérations (défaut: 1000)
    :type max_states: int
    """

    def __init__(
        self, optimization_enabled: bool = True, max_states: int = 1000
    ) -> None:
        """
        Initialise l'opérateur de langages.

        :param optimization_enabled: Active les optimisations
        :type optimization_enabled: bool
        :param max_states: Limite du nombre d'états pour les opérations
        :type max_states: int
        """
        self._cache: Dict[str, AbstractFiniteAutomaton] = {}
        self._optimization_enabled = optimization_enabled
        self._max_states = max_states
        self._stats = OperationStats()
        self._operation_timeout = 30.0  # 30 secondes par défaut

    # ==================== OPÉRATIONS DE BASE ====================

    @staticmethod
    def union(
        automaton1: AbstractFiniteAutomaton,
        automaton2: AbstractFiniteAutomaton,
    ) -> AbstractFiniteAutomaton:
        """
        Calcule l'union de deux langages réguliers.

        L'union L1 ∪ L2 accepte tous les mots acceptés par L1 ou L2.

        :param automaton1: Premier automate
        :type automaton1: AbstractFiniteAutomaton
        :param automaton2: Deuxième automate
        :type automaton2: AbstractFiniteAutomaton
        :return: Automate acceptant l'union des deux langages
        :rtype: AbstractFiniteAutomaton
        :raises IncompatibleAutomataError: Si les automates sont incompatibles
        """
        # Validation des paramètres
        if not isinstance(automaton1, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton1 must be an AbstractFiniteAutomaton"
            )
        if not isinstance(automaton2, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton2 must be an AbstractFiniteAutomaton"
            )

        # Vérification de la compatibilité des alphabets
        if automaton1.alphabet != automaton2.alphabet:
            raise IncompatibleAutomataError("Automata have different alphabets")

        # Création d'un nouvel état initial
        new_initial = "union_initial"

        # Union des états avec préfixes pour éviter les conflits
        states1 = {f"1_{state}" for state in automaton1.states}
        states2 = {f"2_{state}" for state in automaton2.states}
        all_states = {new_initial} | states1 | states2

        # Union des alphabets + epsilon pour les transitions epsilon
        alphabet = automaton1.alphabet | automaton2.alphabet | {"epsilon"}

        # Construction des transitions
        transitions = {}

        # Transitions epsilon depuis le nouvel état initial
        transitions[(new_initial, "epsilon")] = {
            f"1_{automaton1.initial_state}",
            f"2_{automaton2.initial_state}",
        }

        # Transitions du premier automate
        for state in automaton1.states:
            for symbol in automaton1.alphabet:
                dest = automaton1.get_transition(state, symbol)
                if dest:
                    transitions[(f"1_{state}", symbol)] = {f"1_{dest}"}

        # Transitions du deuxième automate
        for state in automaton2.states:
            for symbol in automaton2.alphabet:
                dest = automaton2.get_transition(state, symbol)
                if dest:
                    transitions[(f"2_{state}", symbol)] = {f"2_{dest}"}

        # États finaux
        final_states = set()
        for state in automaton1.final_states:
            final_states.add(f"1_{state}")
        for state in automaton2.final_states:
            final_states.add(f"2_{state}")

        return NFA(all_states, alphabet, transitions, new_initial, final_states)

    @staticmethod
    def intersection(
        automaton1: AbstractFiniteAutomaton,
        automaton2: AbstractFiniteAutomaton,
    ) -> AbstractFiniteAutomaton:
        """
        Calcule l'intersection de deux langages réguliers.

        L'intersection L1 ∩ L2 accepte tous les mots acceptés par L1 et L2.

        :param automaton1: Premier automate
        :type automaton1: AbstractFiniteAutomaton
        :param automaton2: Deuxième automate
        :type automaton2: AbstractFiniteAutomaton
        :return: Automate acceptant l'intersection des deux langages
        :rtype: AbstractFiniteAutomaton
        :raises IncompatibleAutomataError: Si les automates sont incompatibles
        """
        # Validation des paramètres
        if not isinstance(automaton1, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton1 must be an AbstractFiniteAutomaton"
            )
        if not isinstance(automaton2, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton2 must be an AbstractFiniteAutomaton"
            )

        # Vérification de la compatibilité des alphabets
        if automaton1.alphabet != automaton2.alphabet:
            raise IncompatibleAutomataError("Automata have different alphabets")

        # Création du produit cartésien des états
        product_states = set()
        for state1 in automaton1.states:
            for state2 in automaton2.states:
                product_states.add(f"({state1},{state2})")

        # Alphabet commun
        alphabet = automaton1.alphabet & automaton2.alphabet

        # État initial
        initial_state = f"({automaton1.initial_state},{automaton2.initial_state})"

        # Construction des transitions
        transitions = {}
        for state1 in automaton1.states:
            for state2 in automaton2.states:
                for symbol in alphabet:
                    dest1 = automaton1.get_transition(state1, symbol)
                    dest2 = automaton2.get_transition(state2, symbol)
                    if dest1 and dest2:
                        transitions[(f"({state1},{state2})", symbol)] = {
                            f"({dest1},{dest2})"
                        }

        # États finaux (intersection des états finaux)
        final_states = set()
        for state1 in automaton1.final_states:
            for state2 in automaton2.final_states:
                final_states.add(f"({state1},{state2})")

        return NFA(product_states, alphabet, transitions, initial_state, final_states)

    @staticmethod
    def complement(
        automaton: AbstractFiniteAutomaton,
    ) -> AbstractFiniteAutomaton:
        """
        Calcule le complément d'un langage régulier.

        Le complément L' accepte tous les mots non acceptés par L.

        :param automaton: Automate à complémenter
        :type automaton: AbstractFiniteAutomaton
        :return: Automate acceptant le complément du langage
        :rtype: AbstractFiniteAutomaton
        :raises OperationValidationError: Si l'automate n'est pas déterministe
        """
        # Validation des paramètres
        if not isinstance(automaton, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton must be an AbstractFiniteAutomaton"
            )

        # Conversion vers DFA si nécessaire
        if not isinstance(automaton, DFA):
            # Pour simplifier, on suppose que l'automate peut être converti en DFA
            # Dans une implémentation complète, on utiliserait les algorithmes de conversion
            raise OperationValidationError(
                "Automaton must be deterministic for complement"
            )

        # Création d'un état puits si nécessaire
        sink_state = "sink"
        all_states = automaton.states | {sink_state}

        # Alphabet complet
        alphabet = automaton.alphabet

        # Construction des transitions
        transitions = {}

        # Copie des transitions existantes
        for state in automaton.states:
            for symbol in alphabet:
                dest = automaton.get_transition(state, symbol)
                if dest:
                    transitions[(state, symbol)] = dest
                else:
                    transitions[(state, symbol)] = sink_state

        # Transitions de l'état puits vers lui-même
        for symbol in alphabet:
            transitions[(sink_state, symbol)] = sink_state

        # États finaux inversés
        final_states = set()
        for state in all_states:
            if state not in automaton.final_states:
                final_states.add(state)

        return DFA(
            all_states,
            alphabet,
            transitions,
            automaton.initial_state,
            final_states,
        )

    @staticmethod
    def concatenation(
        automaton1: AbstractFiniteAutomaton,
        automaton2: AbstractFiniteAutomaton,
    ) -> AbstractFiniteAutomaton:
        """
        Calcule la concaténation de deux langages réguliers.

        La concaténation L1 · L2 accepte tous les mots w1w2 où w1 ∈ L1 et w2 ∈ L2.

        :param automaton1: Premier automate
        :type automaton1: AbstractFiniteAutomaton
        :param automaton2: Deuxième automate
        :type automaton2: AbstractFiniteAutomaton
        :return: Automate acceptant la concaténation des deux langages
        :rtype: AbstractFiniteAutomaton
        :raises IncompatibleAutomataError: Si les automates sont incompatibles
        """
        # Validation des paramètres
        if not isinstance(automaton1, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton1 must be an AbstractFiniteAutomaton"
            )
        if not isinstance(automaton2, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton2 must be an AbstractFiniteAutomaton"
            )

        # Union des alphabets + epsilon pour les transitions epsilon
        alphabet = automaton1.alphabet | automaton2.alphabet | {"epsilon"}

        # États avec préfixes pour éviter les conflits
        states1 = {f"1_{state}" for state in automaton1.states}
        states2 = {f"2_{state}" for state in automaton2.states}
        all_states = states1 | states2

        # État initial
        initial_state = f"1_{automaton1.initial_state}"

        # Construction des transitions
        transitions = {}

        # Transitions du premier automate
        for state in automaton1.states:
            for symbol in automaton1.alphabet:
                dest = automaton1.get_transition(state, symbol)
                if dest:
                    transitions[(f"1_{state}", symbol)] = {f"1_{dest}"}

        # Transitions du deuxième automate
        for state in automaton2.states:
            for symbol in automaton2.alphabet:
                dest = automaton2.get_transition(state, symbol)
                if dest:
                    transitions[(f"2_{state}", symbol)] = {f"2_{dest}"}

        # Connexions epsilon des états finaux du premier vers l'état initial du second
        for final_state in automaton1.final_states:
            transitions[(f"1_{final_state}", "epsilon")] = {
                f"2_{automaton2.initial_state}"
            }

        # États finaux (seulement ceux du deuxième automate)
        final_states = {f"2_{state}" for state in automaton2.final_states}

        return NFA(all_states, alphabet, transitions, initial_state, final_states)

    @staticmethod
    def kleene_star(
        automaton: AbstractFiniteAutomaton,
    ) -> AbstractFiniteAutomaton:
        """
        Calcule l'étoile de Kleene d'un langage régulier.

        L'étoile de Kleene L* accepte zéro ou plusieurs concaténations de mots de L.

        :param automaton: Automate à transformer
        :type automaton: AbstractFiniteAutomaton
        :return: Automate acceptant l'étoile de Kleene du langage
        :rtype: AbstractFiniteAutomaton
        """
        # Validation des paramètres
        if not isinstance(automaton, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton must be an AbstractFiniteAutomaton"
            )

        # Nouvel état initial
        new_initial = "kleene_initial"

        # États avec préfixe pour éviter les conflits
        states = {f"k_{state}" for state in automaton.states}
        all_states = {new_initial} | states

        # Alphabet + epsilon pour les transitions epsilon
        alphabet = automaton.alphabet | {"epsilon"}

        # Construction des transitions
        transitions = {}

        # Transition epsilon du nouvel état initial vers l'ancien état initial
        transitions[(new_initial, "epsilon")] = {f"k_{automaton.initial_state}"}

        # Transitions de l'automate original
        for state in automaton.states:
            for symbol in automaton.alphabet:
                dest = automaton.get_transition(state, symbol)
                if dest:
                    transitions[(f"k_{state}", symbol)] = {f"k_{dest}"}

        # Transitions epsilon des états finaux vers l'ancien état initial
        for final_state in automaton.final_states:
            transitions[(f"k_{final_state}", "epsilon")] = {
                f"k_{automaton.initial_state}"
            }

        # États finaux (nouvel état initial + anciens états finaux)
        final_states = {new_initial}
        for state in automaton.final_states:
            final_states.add(f"k_{state}")

        return NFA(all_states, alphabet, transitions, new_initial, final_states)

    # ==================== MÉTHODES UTILITAIRES ====================

    def validate_operation(
        self,
        operation: str,
        automaton1: AbstractFiniteAutomaton,
        automaton2: Optional[AbstractFiniteAutomaton] = None,
    ) -> bool:
        """
        Valide une opération avant son exécution.

        :param operation: Nom de l'opération
        :type operation: str
        :param automaton1: Premier automate
        :type automaton1: AbstractFiniteAutomaton
        :param automaton2: Deuxième automate (optionnel)
        :type automaton2: Optional[AbstractFiniteAutomaton]
        :return: True si l'opération est valide, False sinon
        :rtype: bool
        """
        # Validation des paramètres de base
        if not isinstance(automaton1, AbstractFiniteAutomaton):
            return False

        if automaton2 is not None and not isinstance(
            automaton2, AbstractFiniteAutomaton
        ):
            return False

        # Validation spécifique par opération
        if operation in ["union", "intersection", "concatenation"]:
            if automaton2 is None:
                return False
            # Vérification de la compatibilité des alphabets
            if automaton1.alphabet != automaton2.alphabet:
                return False

        # Vérification des limites de performance
        total_states = len(automaton1.states)
        if automaton2 is not None:
            total_states += len(automaton2.states)

        if total_states > self._max_states:
            return False

        return True

    def get_operation_stats(
        self,
        operation: str,
        automaton1: AbstractFiniteAutomaton,
        automaton2: Optional[AbstractFiniteAutomaton] = None,
    ) -> Dict[str, Any]:
        """
        Récupère les statistiques d'une opération.

        :param operation: Nom de l'opération
        :type operation: str
        :param automaton1: Premier automate
        :type automaton1: AbstractFiniteAutomaton
        :param automaton2: Deuxième automate (optionnel)
        :type automaton2: Optional[AbstractFiniteAutomaton]
        :return: Dictionnaire contenant les statistiques
        :rtype: Dict[str, Any]
        """
        return {
            "operation": operation,
            "automaton1_states": len(automaton1.states),
            "automaton1_final_states": len(automaton1.final_states),
            "automaton2_states": len(automaton2.states) if automaton2 else 0,
            "automaton2_final_states": (
                len(automaton2.final_states) if automaton2 else 0
            ),
            "total_states": len(automaton1.states)
            + (len(automaton2.states) if automaton2 else 0),
            "optimization_enabled": self._optimization_enabled,
            "max_states": self._max_states,
        }

    def clear_cache(self) -> None:
        """
        Vide le cache des opérations.
        """
        self._cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques du cache.

        :return: Dictionnaire contenant les statistiques du cache
        :rtype: Dict[str, Any]
        """
        return {
            "cache_size": len(self._cache),
            "cache_keys": list(self._cache.keys()),
        }

    def set_cache_size(self, size: int) -> None:
        """
        Définit la taille maximale du cache.

        :param size: Taille maximale du cache
        :type size: int
        :raises ValueError: Si la taille est négative
        """
        if size < 0:
            raise ValueError("Cache size must be non-negative")

        # Si la nouvelle taille est plus petite, on supprime les entrées les plus anciennes
        if len(self._cache) > size:
            keys_to_remove = list(self._cache.keys())[: len(self._cache) - size]
            for key in keys_to_remove:
                del self._cache[key]

    def get_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques globales des opérations.

        :return: Dictionnaire contenant les statistiques globales
        :rtype: Dict[str, Any]
        """
        return self._stats.get_stats()

    def reset_stats(self) -> None:
        """
        Remet à zéro les statistiques des opérations.
        """
        self._stats.reset()

    # ==================== OPÉRATIONS AVANCÉES ====================

    @staticmethod
    def homomorphism(
        automaton: AbstractFiniteAutomaton, mapping: Mapping
    ) -> AbstractFiniteAutomaton:
        """
        Applique un homomorphisme à un automate.

        Un homomorphisme transforme l'alphabet de l'automate selon le mapping donné.

        :param automaton: Automate à transformer
        :type automaton: AbstractFiniteAutomaton
        :param mapping: Mapping des symboles
        :type mapping: Mapping
        :return: Automate avec l'alphabet transformé
        :rtype: AbstractFiniteAutomaton
        :raises OperationValidationError: Si le mapping n'est pas valide
        """
        # Validation des paramètres
        if not isinstance(automaton, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton must be an AbstractFiniteAutomaton"
            )
        if not isinstance(mapping, Mapping):
            raise OperationValidationError("mapping must be a Mapping instance")

        # Nouvel alphabet transformé
        new_alphabet = mapping.apply_to_set(automaton.alphabet)

        # Construction des nouvelles transitions
        new_transitions = {}

        for state in automaton.states:
            for symbol in automaton.alphabet:
                dest = automaton.get_transition(state, symbol)
                if dest:
                    # Appliquer le mapping au symbole
                    new_symbol = mapping.apply(symbol)
                    new_transitions[(state, new_symbol)] = {dest}

        # États finaux inchangés
        final_states = automaton.final_states.copy()

        return NFA(
            automaton.states,
            new_alphabet,
            new_transitions,
            automaton.initial_state,
            final_states,
        )

    @staticmethod
    def inverse_homomorphism(
        automaton: AbstractFiniteAutomaton, mapping: Mapping
    ) -> AbstractFiniteAutomaton:
        """
        Applique un homomorphisme inverse à un automate.

        Un homomorphisme inverse transforme l'alphabet de l'automate selon
        le mapping inverse donné.

        :param automaton: Automate à transformer
        :type automaton: AbstractFiniteAutomaton
        :param mapping: Mapping des symboles
        :type mapping: Mapping
        :return: Automate avec l'alphabet transformé
        :rtype: AbstractFiniteAutomaton
        :raises OperationValidationError: Si le mapping n'est pas valide
        """
        # Validation des paramètres
        if not isinstance(automaton, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton must be an AbstractFiniteAutomaton"
            )
        if not isinstance(mapping, Mapping):
            raise OperationValidationError("mapping must be a Mapping instance")

        # Nouvel alphabet (domaine du mapping)
        new_alphabet = mapping.get_domain()

        # Construction des nouvelles transitions
        new_transitions = {}

        for state in automaton.states:
            for symbol in automaton.alphabet:
                dest = automaton.get_transition(state, symbol)
                if dest:
                    # Trouver tous les symboles qui mappent vers ce symbole
                    inverse_symbols = mapping.get_inverse_symbols(symbol)
                    for inverse_symbol in inverse_symbols:
                        new_transitions[(state, inverse_symbol)] = {dest}

        # États finaux inchangés
        final_states = automaton.final_states.copy()

        return NFA(
            automaton.states,
            new_alphabet,
            new_transitions,
            automaton.initial_state,
            final_states,
        )

    @staticmethod
    def cartesian_product(
        automaton1: AbstractFiniteAutomaton,
        automaton2: AbstractFiniteAutomaton,
    ) -> AbstractFiniteAutomaton:
        """
        Calcule le produit cartésien de deux automates.

        Le produit cartésien crée un automate dont les états sont des paires
        d'états des deux automates originaux.

        :param automaton1: Premier automate
        :type automaton1: AbstractFiniteAutomaton
        :param automaton2: Deuxième automate
        :type automaton2: AbstractFiniteAutomaton
        :return: Automate produit cartésien
        :rtype: AbstractFiniteAutomaton
        :raises IncompatibleAutomataError: Si les automates sont incompatibles
        """
        # Validation des paramètres
        if not isinstance(automaton1, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton1 must be an AbstractFiniteAutomaton"
            )
        if not isinstance(automaton2, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton2 must be an AbstractFiniteAutomaton"
            )

        # Vérification de la compatibilité des alphabets
        if automaton1.alphabet != automaton2.alphabet:
            raise IncompatibleAutomataError("Automata have different alphabets")

        # Création du produit cartésien des états
        product_states = set()
        for state1 in automaton1.states:
            for state2 in automaton2.states:
                product_states.add(f"({state1},{state2})")

        # Alphabet commun
        alphabet = automaton1.alphabet & automaton2.alphabet

        # État initial
        initial_state = f"({automaton1.initial_state},{automaton2.initial_state})"

        # Construction des transitions
        transitions = {}
        for state1 in automaton1.states:
            for state2 in automaton2.states:
                for symbol in alphabet:
                    dest1 = automaton1.get_transition(state1, symbol)
                    dest2 = automaton2.get_transition(state2, symbol)
                    if dest1 and dest2:
                        transitions[(f"({state1},{state2})", symbol)] = {
                            f"({dest1},{dest2})"
                        }

        # États finaux (intersection des états finaux)
        final_states = set()
        for state1 in automaton1.final_states:
            for state2 in automaton2.final_states:
                final_states.add(f"({state1},{state2})")

        return NFA(product_states, alphabet, transitions, initial_state, final_states)

    # ==================== OPÉRATIONS SPÉCIALISÉES ====================

    @staticmethod
    def difference(
        automaton1: AbstractFiniteAutomaton,
        automaton2: AbstractFiniteAutomaton,
    ) -> AbstractFiniteAutomaton:
        """
        Calcule la différence de deux langages réguliers.

        La différence L1 - L2 accepte tous les mots de L1 qui ne sont pas dans L2.
        Équivalence: L1 - L2 = L1 ∩ L2'

        :param automaton1: Premier automate
        :type automaton1: AbstractFiniteAutomaton
        :param automaton2: Deuxième automate
        :type automaton2: AbstractFiniteAutomaton
        :return: Automate acceptant la différence des deux langages
        :rtype: AbstractFiniteAutomaton
        :raises IncompatibleAutomataError: Si les automates sont incompatibles
        """
        # Calculer le complément du deuxième automate
        complement2 = LanguageOperations.complement(automaton2)

        # Calculer l'intersection du premier avec le complément du second
        return LanguageOperations.intersection(automaton1, complement2)

    @staticmethod
    def symmetric_difference(
        automaton1: AbstractFiniteAutomaton,
        automaton2: AbstractFiniteAutomaton,
    ) -> AbstractFiniteAutomaton:
        """
        Calcule la différence symétrique de deux langages réguliers.

        La différence symétrique L1 Δ L2 accepte tous les mots qui sont dans
        L1 ou L2 mais pas dans les deux.
        Équivalence: L1 Δ L2 = (L1 ∪ L2) - (L1 ∩ L2)

        :param automaton1: Premier automate
        :type automaton1: AbstractFiniteAutomaton
        :param automaton2: Deuxième automate
        :type automaton2: AbstractFiniteAutomaton
        :return: Automate acceptant la différence symétrique des deux langages
        :rtype: AbstractFiniteAutomaton
        :raises IncompatibleAutomataError: Si les automates sont incompatibles
        """
        # Calculer l'union et l'intersection
        union_result = LanguageOperations.union(automaton1, automaton2)
        intersection_result = LanguageOperations.intersection(automaton1, automaton2)

        # Calculer la différence de l'union et de l'intersection
        return LanguageOperations.difference(union_result, intersection_result)

    @staticmethod
    def power(automaton: AbstractFiniteAutomaton, n: int) -> AbstractFiniteAutomaton:
        """
        Calcule la puissance n-ième d'un langage régulier.

        La puissance L^n accepte n concaténations consécutives de mots de L.

        :param automaton: Automate de base
        :type automaton: AbstractFiniteAutomaton
        :param n: Puissance (doit être >= 0)
        :type n: int
        :return: Automate acceptant la puissance n-ième du langage
        :rtype: AbstractFiniteAutomaton
        :raises OperationValidationError: Si n est négatif
        """
        # Validation des paramètres
        if not isinstance(automaton, AbstractFiniteAutomaton):
            raise OperationValidationError(
                "automaton must be an AbstractFiniteAutomaton"
            )
        if n < 0:
            raise OperationValidationError("Power must be non-negative")

        # Cas spéciaux
        if n == 0:
            # L^0 = {ε} (langage contenant seulement le mot vide)
            return NFA({"q0"}, set(), {}, "q0", {"q0"})

        if n == 1:
            # L^1 = L
            return automaton

        # Calculer L^n par concaténation répétée
        result = automaton
        for _ in range(n - 1):
            result = LanguageOperations.concatenation(result, automaton)

        return result
