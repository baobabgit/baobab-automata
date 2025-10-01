"""
Implémentation d'un automate fini déterministe (DFA).

Ce module contient la classe DFA qui implémente l'interface AbstractFiniteAutomaton
pour les automates finis déterministes selon les spécifications détaillées.
"""

from typing import Any, Dict, Optional, Set, Tuple

from .abstract_finite_automaton import AbstractFiniteAutomaton
from .language_operations import LanguageOperations
from .nfa import NFA

from .dfa_exceptions import InvalidDFAError


class DFA(AbstractFiniteAutomaton):
    """
    Implémentation d'un automate fini déterministe (DFA).

    Un DFA est un automate fini où pour chaque état et chaque symbole,
    il existe exactement une transition possible.

    :param states: Ensemble des états de l'automate
    :type states: Set[str]
    :param alphabet: Alphabet de l'automate
    :type alphabet: Set[str]
    :param transitions: Fonction de transition (état, symbole) vers un état
    :type transitions: Dict[Tuple[str, str], str]
    :param initial_state: État initial
    :type initial_state: str
    :param final_states: Ensemble des états finaux
    :type final_states: Set[str]
    """

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[Tuple[str, str], str],
        initial_state: str,
        final_states: Set[str],
    ) -> None:
        """
        Initialise un DFA.

        :param states: Ensemble des états de l'automate
        :type states: Set[str]
        :param alphabet: Alphabet de l'automate
        :type alphabet: Set[str]
        :param transitions: Fonction de transition (état, symbole) vers un état
        :type transitions: Dict[Tuple[str, str], str]
        :param initial_state: État initial
        :type initial_state: str
        :param final_states: Ensemble des états finaux
        :type final_states: Set[str]
        :raises InvalidDFAError: Si le DFA est invalide
        :raises InvalidStateError: Si un état est invalide
        :raises InvalidTransitionError: Si une transition est invalide
        """
        self._states = states.copy()
        self._alphabet = alphabet.copy()
        self._transitions = transitions.copy()
        self._initial_state = initial_state
        self._final_states = final_states.copy()

        # Validation du DFA
        if not self.validate():
            raise InvalidDFAError("Invalid DFA configuration")

    @property
    def states(self) -> Set[str]:
        """
        Ensemble des états de l'automate.

        :return: Ensemble des identifiants des états
        :rtype: Set[str]
        """
        return self._states.copy()

    @property
    def alphabet(self) -> Set[str]:
        """
        Alphabet de l'automate.

        :return: Ensemble des symboles de l'alphabet
        :rtype: Set[str]
        """
        return self._alphabet.copy()

    @property
    def initial_state(self) -> str:
        """
        État initial de l'automate.

        :return: Identifiant de l'état initial
        :rtype: str
        """
        return self._initial_state

    @property
    def final_states(self) -> Set[str]:
        """
        Ensemble des états finaux.

        :return: Ensemble des identifiants des états finaux
        :rtype: Set[str]
        """
        return self._final_states.copy()

    def accepts(self, word: str) -> bool:
        """
        Vérifie si l'automate accepte un mot donné.

        :param word: Mot à tester
        :type word: str
        :return: True si le mot est accepté, False sinon
        :rtype: bool
        """
        current_state = self._initial_state

        for symbol in word:
            if symbol not in self._alphabet:
                return False

            transition_key = (current_state, symbol)
            if transition_key not in self._transitions:
                return False

            current_state = self._transitions[transition_key]

        return current_state in self._final_states

    def get_transition(self, state: str, symbol: str) -> Optional[str]:
        """
        Récupère l'état de destination pour une transition donnée.

        :param state: État source
        :type state: str
        :param symbol: Symbole de la transition
        :type symbol: str
        :return: État de destination ou None si la transition n'existe pas
        :rtype: Optional[str]
        """
        transition_key = (state, symbol)
        return self._transitions.get(transition_key)

    def is_final_state(self, state: str) -> bool:
        """
        Vérifie si un état est final.

        :param state: Identifiant de l'état
        :type state: str
        :return: True si l'état est final, False sinon
        :rtype: bool
        """
        return state in self._final_states

    def get_reachable_states(self) -> Set[str]:
        """
        Récupère tous les états accessibles depuis l'état initial.

        :return: Ensemble des états accessibles
        :rtype: Set[str]
        """
        reachable = set()
        to_visit = {self._initial_state}

        while to_visit:
            current = to_visit.pop()
            if current in reachable:
                continue

            reachable.add(current)

            # Ajouter tous les états accessibles depuis l'état actuel
            for symbol in self._alphabet:
                transition_key = (current, symbol)
                if transition_key in self._transitions:
                    next_state = self._transitions[transition_key]
                    if next_state not in reachable:
                        to_visit.add(next_state)

        return reachable

    def validate(self) -> bool:
        """
        Valide la cohérence de l'automate.

        :return: True si l'automate est valide, False sinon
        :rtype: bool
        """
        try:
            # Vérifier que l'état initial est dans l'ensemble des états
            if self._initial_state not in self._states:
                return False

            # Vérifier que tous les états finaux sont dans l'ensemble des états
            if not self._final_states.issubset(self._states):
                return False

            # Vérifier que toutes les transitions sont valides
            for (source, symbol), target in self._transitions.items():
                if source not in self._states:
                    return False
                if target not in self._states:
                    return False
                if symbol not in self._alphabet:
                    return False

            return True
        except (AttributeError, TypeError, ValueError, KeyError):
            # Capturer les erreurs spécifiques qui peuvent survenir
            # lors de la validation de l'automate
            return False

    def minimize(self) -> "DFA":
        """
        Minimise le DFA en utilisant l'algorithme de Hopcroft.

        :return: DFA minimal équivalent
        :rtype: DFA
        """
        # Algorithme de Hopcroft pour la minimisation
        # Partition initiale : états finaux vs non-finaux
        partition = [self._final_states, self._states - self._final_states]

        # Éliminer les ensembles vides
        partition = [p for p in partition if p]

        # Raffiner la partition
        changed = True
        while changed:
            changed = False
            new_partition = []

            for group in partition:
                # Diviser le groupe selon les transitions
                subgroups = {}
                for state in group:
                    key = tuple(
                        self._get_group_for_state(state, symbol, partition)
                        for symbol in self._alphabet
                    )
                    if key not in subgroups:
                        subgroups[key] = set()
                    subgroups[key].add(state)

                # Ajouter les sous-groupes non vides
                for subgroup in subgroups.values():
                    if subgroup:
                        new_partition.append(subgroup)

                if len(subgroups) > 1:
                    changed = True

            partition = new_partition

        # Construire le DFA minimal
        state_mapping = {}
        for i, group in enumerate(partition):
            for state in group:
                state_mapping[state] = f"q{i}"

        # Nouveaux états
        new_states = {state_mapping[state] for state in self._states}

        # Nouvel alphabet (identique)
        new_alphabet = self._alphabet.copy()

        # Nouvelles transitions
        new_transitions = {}
        for (source, symbol), target in self._transitions.items():
            new_source = state_mapping[source]
            new_target = state_mapping[target]
            new_transitions[(new_source, symbol)] = new_target

        # Nouvel état initial
        new_initial = state_mapping[self._initial_state]

        # Nouveaux états finaux
        new_final = {state_mapping[state] for state in self._final_states}

        return DFA(
            states=new_states,
            alphabet=new_alphabet,
            transitions=new_transitions,
            initial_state=new_initial,
            final_states=new_final,
        )

    def _get_group_for_state(self, state: str, symbol: str, partition: list) -> int:
        """Trouve l'index du groupe contenant l'état de destination."""
        transition_key = (state, symbol)
        if transition_key in self._transitions:
            target = self._transitions[transition_key]
            for i, group in enumerate(partition):
                if target in group:
                    return i
        return -1

    def remove_unreachable_states(self) -> "DFA":
        """
        Supprime les états inaccessibles du DFA.

        :return: DFA sans états inaccessibles
        :rtype: DFA
        """
        reachable = self.get_reachable_states()

        # Nouveaux états (seulement les accessibles)
        new_states = reachable

        # Nouvel alphabet (identique)
        new_alphabet = self._alphabet.copy()

        # Nouvelles transitions (seulement celles entre états accessibles)
        new_transitions = {
            (source, symbol): target
            for (source, symbol), target in self._transitions.items()
            if source in reachable and target in reachable
        }

        # Nouvel état initial (identique)
        new_initial = self._initial_state

        # Nouveaux états finaux (seulement ceux accessibles)
        new_final = self._final_states.intersection(reachable)

        return DFA(
            states=new_states,
            alphabet=new_alphabet,
            transitions=new_transitions,
            initial_state=new_initial,
            final_states=new_final,
        )

    def union(self, other: "DFA") -> "DFA":
        """
        Calcule l'union de deux DFA.

        :param other: Autre DFA
        :type other: DFA
        :return: DFA acceptant l'union des langages
        :rtype: DFA
        """
        operations = LanguageOperations()
        result = operations.union(self, other)
        assert isinstance(result, DFA), "Union of DFA should return DFA"
        return result

    def intersection(self, other: "DFA") -> "DFA":
        """
        Calcule l'intersection de deux DFA.

        :param other: Autre DFA
        :type other: DFA
        :return: DFA acceptant l'intersection des langages
        :rtype: DFA
        """
        operations = LanguageOperations()
        result = operations.intersection(self, other)
        assert isinstance(result, DFA), "Intersection of DFA should return DFA"
        return result

    def complement(self) -> "DFA":
        """
        Calcule le complément du DFA (optimisé).

        :return: DFA acceptant le complément du langage
        :rtype: DFA
        """
        # Optimisation directe pour DFA : inverser les états finaux
        new_final_states = self._states - self._final_states
        return DFA(
            states=self._states,
            alphabet=self._alphabet,
            transitions=self._transitions,
            initial_state=self._initial_state,
            final_states=new_final_states
        )

    def concatenation(self, other: "DFA") -> "DFA":
        """
        Calcule la concaténation de deux DFA.

        :param other: Autre DFA
        :type other: DFA
        :return: DFA acceptant la concaténation des langages
        :rtype: DFA
        """
        operations = LanguageOperations()
        result = operations.concatenation(self, other)
        assert isinstance(result, DFA), "Concatenation of DFA should return DFA"
        return result

    def kleene_star(self) -> "DFA":
        """
        Calcule l'étoile de Kleene du DFA.

        :return: DFA acceptant l'étoile de Kleene du langage
        :rtype: DFA
        """
        operations = LanguageOperations()
        result = operations.kleene_star(self)
        assert isinstance(result, DFA), "Kleene star of DFA should return DFA"
        return result

    def to_nfa(self) -> "NFA":
        """
        Convertit le DFA en NFA.

        :return: NFA équivalent
        :rtype: NFA
        """
        # Un DFA est un cas particulier de NFA
        # Conversion directe : chaque transition DFA devient une transition NFA
        nfa_transitions = {}
        for (source, symbol), target in self._transitions.items():
            nfa_transitions[(source, symbol)] = {target}

        return NFA(
            states=self._states,
            alphabet=self._alphabet,
            transitions=nfa_transitions,
            initial_state=self._initial_state,
            final_states=self._final_states
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Sérialise l'automate en dictionnaire.

        :return: Dictionnaire représentant l'automate
        :rtype: Dict[str, Any]
        """
        return {
            "states": list(self._states),
            "alphabet": list(self._alphabet),
            "transitions": {
                f"{source},{symbol}": target
                for (source, symbol), target in self._transitions.items()
            },
            "initial_state": self._initial_state,
            "final_states": list(self._final_states),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DFA":
        """
        Crée un DFA depuis un dictionnaire.

        :param data: Dictionnaire représentant l'automate
        :type data: Dict[str, Any]
        :return: Instance du DFA
        :rtype: DFA
        """
        states = set(data["states"])
        alphabet = set(data["alphabet"])
        transitions = {
            (key.split(",")[0], key.split(",")[1]): target
            for key, target in data["transitions"].items()
        }
        initial_state = data["initial_state"]
        final_states = set(data["final_states"])

        return cls(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

    def __str__(self) -> str:
        """
        Représentation string de l'automate.

        :return: Représentation string de l'automate
        :rtype: str
        """
        return f"DFA(states={len(self._states)}, transitions={len(self._transitions)})"

    def __repr__(self) -> str:
        """
        Représentation détaillée de l'automate.

        :return: Représentation détaillée de l'automate
        :rtype: str
        """
        return (
            f"DFA(states={self._states}, alphabet={self._alphabet}, "
            f"initial_state='{self._initial_state}', final_states={self._final_states}, "
            f"transitions={self._transitions})"
        )
