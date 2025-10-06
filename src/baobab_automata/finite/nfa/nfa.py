"""
Implémentation d'un automate fini non-déterministe (NFA).

Ce module contient la classe NFA qui implémente l'interface AbstractFiniteAutomaton
pour les automates finis non-déterministes selon les spécifications détaillées.
"""

from typing import Any, Dict, FrozenSet, Optional, Set, Tuple

from ..abstract_finite_automaton import AbstractFiniteAutomaton
from .nfa_exceptions import (
    ConversionError,
    InvalidNFAError,
    InvalidTransitionError,
    NFAError,
)


class NFA(AbstractFiniteAutomaton):
    """
    Implémentation d'un automate fini non-déterministe (NFA).

    Un NFA est un automate fini où pour chaque état et chaque symbole,
    il peut y avoir zéro, une ou plusieurs transitions possibles.

    :param states: Ensemble des états de l'automate
    :type states: Set[str]
    :param alphabet: Alphabet de l'automate
    :type alphabet: Set[str]
    :param transitions: Fonction de transition (état, symbole) -> ensemble d'états
    :type transitions: Dict[Tuple[str, str], Set[str]]
    :param initial_state: État initial
    :type initial_state: str
    :param final_states: Ensemble des états finaux
    :type final_states: Set[str]
    """

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[Tuple[str, str], Set[str]],
        initial_state: str,
        final_states: Set[str],
    ) -> None:
        """
        Initialise un NFA.

        :param states: Ensemble des états de l'automate
        :type states: Set[str]
        :param alphabet: Alphabet de l'automate
        :type alphabet: Set[str]
        :param transitions: Fonction de transition (état, symbole) -> ensemble d'états
        :type transitions: Dict[Tuple[str, str], Set[str]]
        :param initial_state: État initial
        :type initial_state: str
        :param final_states: Ensemble des états finaux
        :type final_states: Set[str]
        :raises InvalidNFAError: Si le NFA est invalide
        :raises InvalidTransitionError: Si une transition est invalide
        """
        self._states = states.copy()
        self._alphabet = alphabet.copy()
        self._transitions = {k: v.copy() for k, v in transitions.items()}
        self._initial_state = initial_state
        self._final_states = final_states.copy()

        # Validation du NFA
        if not self.validate():
            raise InvalidNFAError("Invalid NFA configuration")

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

        Utilise l'algorithme de simulation non-déterministe pour tester
        toutes les branches possibles de l'automate.

        :param word: Mot à tester
        :type word: str
        :return: True si le mot est accepté, False sinon
        :rtype: bool
        """
        return self._simulate_nfa(word)

    def get_transition(self, state: str, symbol: str) -> Optional[str]:
        """
        Récupère l'état de destination pour une transition donnée.

        Pour un NFA, cette méthode retourne le premier état de destination
        trouvé ou None si aucune transition n'existe.

        :param state: État source
        :type state: str
        :param symbol: Symbole de la transition
        :type symbol: str
        :return: Premier état de destination ou None si la transition n'existe pas
        :rtype: Optional[str]
        """
        transition_key = (state, symbol)
        destinations = self._transitions.get(transition_key, set())
        return next(iter(destinations)) if destinations else None

    def get_transitions(self, state: str, symbol: str) -> Set[str]:
        """
        Récupère l'ensemble des états de destination pour une transition donnée.

        :param state: État source
        :type state: str
        :param symbol: Symbole de la transition
        :type symbol: str
        :return: Ensemble des états de destination
        :rtype: Set[str]
        """
        transition_key = (state, symbol)
        return self._transitions.get(transition_key, set()).copy()

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
        return self.get_accessible_states()

    def _simulate_nfa(self, word: str) -> bool:
        """
        Simule l'exécution du NFA sur un mot donné.

        :param word: Mot à tester
        :type word: str
        :return: True si le mot est accepté, False sinon
        :rtype: bool
        """
        # Ensemble des états courants (commence par l'état initial)
        current_states = {self._initial_state}

        # Appliquer les fermetures epsilon au début
        current_states = self._epsilon_closure(current_states)

        # Pour chaque symbole du mot
        for symbol in word:
            if symbol not in self._alphabet:
                return False

            # Calculer les nouveaux états possibles
            next_states = set()
            for state in current_states:
                transition_key = (state, symbol)
                if transition_key in self._transitions:
                    next_states.update(self._transitions[transition_key])

            # Appliquer les fermetures epsilon après chaque transition
            current_states = self._epsilon_closure(next_states)

            # Si aucun état n'est possible, le mot est rejeté
            if not current_states:
                return False

        # Vérifier si au moins un état final est atteint
        return bool(current_states.intersection(self._final_states))

    def _epsilon_closure(self, states: Set[str]) -> Set[str]:
        """
        Calcule la fermeture epsilon d'un ensemble d'états.

        :param states: Ensemble d'états
        :type states: Set[str]
        :return: Fermeture epsilon des états
        :rtype: Set[str]
        """
        closure = set(states)
        to_process = list(states)

        while to_process:
            current = to_process.pop(0)

            # Chercher les transitions epsilon depuis l'état actuel
            epsilon_key = (current, "epsilon")
            if epsilon_key in self._transitions:
                for target in self._transitions[epsilon_key]:
                    if target not in closure:
                        closure.add(target)
                        to_process.append(target)

        return closure

    def get_accessible_states(self) -> Set[str]:
        """
        Récupère tous les états accessibles depuis l'état initial.

        :return: Ensemble des états accessibles
        :rtype: Set[str]
        """
        accessible = set()
        to_visit = {self._initial_state}

        while to_visit:
            current = to_visit.pop()
            if current in accessible:
                continue

            accessible.add(current)

            # Ajouter tous les états accessibles depuis l'état actuel
            for symbol in self._alphabet:
                transition_key = (current, symbol)
                if transition_key in self._transitions:
                    for next_state in self._transitions[transition_key]:
                        if next_state not in accessible:
                            to_visit.add(next_state)

        return accessible

    def get_coaccessible_states(self) -> Set[str]:
        """
        Récupère tous les états cœurs (pouvant atteindre un état final).

        :return: Ensemble des états cœurs
        :rtype: Set[str]
        """
        coaccessible = set()
        to_visit = set(self._final_states)

        while to_visit:
            current = to_visit.pop()
            if current in coaccessible:
                continue

            coaccessible.add(current)

            # Trouver tous les états qui peuvent atteindre l'état actuel
            for state in self._states:
                for symbol in self._alphabet:
                    transition_key = (state, symbol)
                    if transition_key in self._transitions:
                        if current in self._transitions[transition_key]:
                            if state not in coaccessible:
                                to_visit.add(state)

        return coaccessible

    def get_useful_states(self) -> Set[str]:
        """
        Récupère tous les états utiles (accessibles et cœurs).

        :return: Ensemble des états utiles
        :rtype: Set[str]
        """
        accessible = self.get_accessible_states()
        coaccessible = self.get_coaccessible_states()
        return accessible.intersection(coaccessible)

    def to_dfa(self) -> "DFA":
        """
        Convertit le NFA en DFA en utilisant l'algorithme des sous-ensembles.

        :return: DFA équivalent
        :rtype: DFA
        """
        try:
            # Import local pour éviter les dépendances circulaires
            from ..dfa import DFA

            # État initial du DFA (sous-ensemble contenant l'état initial du NFA)
            dfa_initial = frozenset({self._initial_state})

            # États du DFA (sous-ensembles d'états du NFA)
            dfa_states = {dfa_initial}
            dfa_transitions = {}

            # File d'attente pour traiter les nouveaux états
            to_process = [dfa_initial]

            while to_process:
                current_dfa_state = to_process.pop(0)

                # Pour chaque symbole de l'alphabet
                for symbol in self._alphabet:
                    # Calculer l'union des transitions du NFA
                    next_states = set()
                    for nfa_state in current_dfa_state:
                        transition_key = (nfa_state, symbol)
                        if transition_key in self._transitions:
                            next_states.update(self._transitions[transition_key])

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
            dfa_alphabet = self._alphabet.copy()
            dfa_transitions_dict = {
                (state_names[source], symbol): state_names[target]
                for (source, symbol), target in dfa_transitions.items()
            }
            dfa_initial_state = state_names[dfa_initial]
            dfa_final_states = {
                state_names[state]
                for state in dfa_states
                if state.intersection(self._final_states)
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

    def union(self, other: "NFA") -> "NFA":
        """
        Calcule l'union de deux NFA.

        :param other: Autre NFA
        :type other: NFA
        :return: NFA acceptant l'union des langages
        :rtype: NFA
        """
        # Créer un nouvel état initial
        new_initial = "q0_union"

        # Combiner les états (avec préfixes pour éviter les conflits)
        new_states = {new_initial}
        new_states.update(f"nfa1_{state}" for state in self._states)
        new_states.update(f"nfa2_{state}" for state in other._states)

        # Combiner les alphabets
        new_alphabet = self._alphabet.union(other._alphabet)

        # Combiner les transitions
        new_transitions = {}

        # Transitions du premier NFA
        for (source, symbol), targets in self._transitions.items():
            new_source = f"nfa1_{source}"
            new_targets = {f"nfa1_{target}" for target in targets}
            new_transitions[(new_source, symbol)] = new_targets

        # Transitions du second NFA
        for (source, symbol), targets in other._transitions.items():
            new_source = f"nfa2_{source}"
            new_targets = {f"nfa2_{target}" for target in targets}
            new_transitions[(new_source, symbol)] = new_targets

        # Ajouter les transitions depuis le nouvel état initial
        new_transitions[(new_initial, "epsilon")] = {
            f"nfa1_{self._initial_state}",
            f"nfa2_{other._initial_state}",
        }

        # Combiner les états finaux
        new_final_states = {f"nfa1_{state}" for state in self._final_states}
        new_final_states.update(f"nfa2_{state}" for state in other._final_states)

        return NFA(
            states=new_states,
            alphabet=new_alphabet,
            transitions=new_transitions,
            initial_state=new_initial,
            final_states=new_final_states,
        )

    def concatenation(self, other: "NFA") -> "NFA":
        """
        Calcule la concaténation de deux NFA.

        :param other: Autre NFA
        :type other: NFA
        :return: NFA acceptant la concaténation des langages
        :rtype: NFA
        """
        # Combiner les états (avec préfixes pour éviter les conflits)
        new_states = {f"nfa1_{state}" for state in self._states}
        new_states.update(f"nfa2_{state}" for state in other._states)

        # Combiner les alphabets
        new_alphabet = self._alphabet.union(other._alphabet)

        # Combiner les transitions
        new_transitions = {}

        # Transitions du premier NFA
        for (source, symbol), targets in self._transitions.items():
            new_source = f"nfa1_{source}"
            new_targets = {f"nfa1_{target}" for target in targets}
            new_transitions[(new_source, symbol)] = new_targets

        # Transitions du second NFA
        for (source, symbol), targets in other._transitions.items():
            new_source = f"nfa2_{source}"
            new_targets = {f"nfa2_{target}" for target in targets}
            new_transitions[(new_source, symbol)] = new_targets

        # Connecter les états finaux du premier NFA à l'état initial du second
        for final_state in self._final_states:
            transition_key = (f"nfa1_{final_state}", "epsilon")
            if transition_key not in new_transitions:
                new_transitions[transition_key] = set()
            new_transitions[transition_key].add(f"nfa2_{other._initial_state}")

        # Nouvel état initial (celui du premier NFA)
        new_initial = f"nfa1_{self._initial_state}"

        # Nouveaux états finaux (ceux du second NFA)
        new_final_states = {f"nfa2_{state}" for state in other._final_states}

        return NFA(
            states=new_states,
            alphabet=new_alphabet,
            transitions=new_transitions,
            initial_state=new_initial,
            final_states=new_final_states,
        )

    def kleene_star(self) -> "NFA":
        """
        Calcule l'étoile de Kleene du NFA.

        :return: NFA acceptant l'étoile de Kleene du langage
        :rtype: NFA
        """
        # Créer un nouvel état initial
        new_initial = "q0_star"

        # Ajouter le nouvel état initial aux états
        new_states = {new_initial}
        new_states.update(self._states)

        # Alphabet identique
        new_alphabet = self._alphabet.copy()

        # Copier les transitions existantes
        new_transitions = {k: v.copy() for k, v in self._transitions.items()}

        # Ajouter les transitions depuis le nouvel état initial
        new_transitions[(new_initial, "epsilon")] = {self._initial_state}

        # Connecter les états finaux à l'état initial
        for final_state in self._final_states:
            transition_key = (final_state, "epsilon")
            if transition_key not in new_transitions:
                new_transitions[transition_key] = set()
            new_transitions[transition_key].add(self._initial_state)

        # Nouveaux états finaux (ancien état initial + anciens états finaux)
        new_final_states = {new_initial}
        new_final_states.update(self._final_states)

        return NFA(
            states=new_states,
            alphabet=new_alphabet,
            transitions=new_transitions,
            initial_state=new_initial,
            final_states=new_final_states,
        )

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
            for (source, symbol), targets in self._transitions.items():
                if source not in self._states:
                    return False
                if not targets.issubset(self._states):
                    return False
                if (
                    symbol not in self._alphabet and symbol != "epsilon"
                ):  # 'epsilon' pour les transitions epsilon
                    return False

            return True
        except Exception:
            return False

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
                f"{source},{symbol}": list(targets)
                for (source, symbol), targets in self._transitions.items()
            },
            "initial_state": self._initial_state,
            "final_states": list(self._final_states),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NFA":
        """
        Crée un NFA depuis un dictionnaire.

        :param data: Dictionnaire représentant l'automate
        :type data: Dict[str, Any]
        :return: Instance du NFA
        :rtype: NFA
        """
        states = set(data["states"])
        alphabet = set(data["alphabet"])
        transitions = {
            tuple(key.split(",")): set(targets)
            for key, targets in data["transitions"].items()
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
        return f"NFA(states={len(self._states)}, transitions={len(self._transitions)})"

    def __repr__(self) -> str:
        """
        Représentation détaillée de l'automate.

        :return: Représentation détaillée de l'automate
        :rtype: str
        """
        return (
            f"NFA(states={self._states}, alphabet={self._alphabet}, "
            f"initial_state='{self._initial_state}', final_states={self._final_states}, "
            f"transitions={self._transitions})"
        )
