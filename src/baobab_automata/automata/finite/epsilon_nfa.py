"""
Implémentation d'un automate fini non-déterministe avec transitions epsilon (ε-NFA).

Ce module contient la classe EpsilonNFA qui implémente l'interface AbstractFiniteAutomaton
pour les automates finis non-déterministes avec transitions epsilon selon les spécifications détaillées.
"""

from typing import Any, Dict, FrozenSet, Optional, Set, Tuple, TYPE_CHECKING

from .abstract_finite_automaton import AbstractFiniteAutomaton
from .epsilon_nfa_exceptions import (
    ConversionError,
    InvalidEpsilonNFAError,
)

if TYPE_CHECKING:
    from .nfa import NFA
    from .dfa import DFA


class EpsilonNFA(AbstractFiniteAutomaton):
    """
    Implémentation d'un automate fini non-déterministe avec transitions epsilon (ε-NFA).

    Un ε-NFA est un automate fini où pour chaque état et chaque symbole,
    il peut y avoir zéro, une ou plusieurs transitions possibles, y compris
    des transitions epsilon (transitions vides).

    :param states: Ensemble des états de l'automate
    :type states: Set[str]
    :param alphabet: Alphabet de l'automate (sans epsilon)
    :type alphabet: Set[str]
    :param transitions: Fonction de transition (état, symbole) vers un ensemble d'états
    :type transitions: Dict[Tuple[str, str], Set[str]]
    :param initial_state: État initial
    :type initial_state: str
    :param final_states: Ensemble des états finaux
    :type final_states: Set[str]
    :param epsilon_symbol: Symbole epsilon (par défaut 'ε')
    :type epsilon_symbol: str
    """

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[Tuple[str, str], Set[str]],
        initial_state: str,
        final_states: Set[str],
        epsilon_symbol: str = "ε",
    ) -> None:
        """
        Initialise un ε-NFA.

        :param states: Ensemble des états de l'automate
        :type states: Set[str]
        :param alphabet: Alphabet de l'automate (sans epsilon)
        :type alphabet: Set[str]
        :param transitions: Fonction de transition (état, symbole) vers un ensemble d'états
        :type transitions: Dict[Tuple[str, str], Set[str]]
        :param initial_state: État initial
        :type initial_state: str
        :param final_states: Ensemble des états finaux
        :type final_states: Set[str]
        :param epsilon_symbol: Symbole epsilon (par défaut 'ε')
        :type epsilon_symbol: str
        :raises InvalidEpsilonNFAError: Si le ε-NFA est invalide
        :raises InvalidEpsilonTransitionError: Si une transition est invalide
        """
        self._states = states.copy()
        self._alphabet = alphabet.copy()
        self._transitions = {k: v.copy() for k, v in transitions.items()}
        self._initial_state = initial_state
        self._final_states = final_states.copy()
        self._epsilon_symbol = epsilon_symbol

        # Cache pour les fermetures epsilon
        self._epsilon_closure_cache: Dict[FrozenSet[str], Set[str]] = {}

        # Validation du ε-NFA
        if not self.validate():
            raise InvalidEpsilonNFAError("Invalid ε-NFA configuration")

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

    @property
    def epsilon_symbol(self) -> str:
        """
        Symbole epsilon de l'automate.

        :return: Symbole epsilon
        :rtype: str
        """
        return self._epsilon_symbol

    def accepts(self, word: str) -> bool:
        """
        Vérifie si l'automate accepte un mot donné.

        Utilise l'algorithme de simulation avec fermeture epsilon pour tester
        toutes les branches possibles de l'automate.

        :param word: Mot à tester
        :type word: str
        :return: True si le mot est accepté, False sinon
        :rtype: bool
        """
        return self._simulate_epsilon_nfa(word)

    def get_transition(self, state: str, symbol: str) -> Optional[str]:
        """
        Récupère l'état de destination pour une transition donnée.

        Pour un ε-NFA, cette méthode retourne le premier état de destination
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

    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        """
        Calcule la fermeture epsilon d'un ensemble d'états.

        :param states: Ensemble d'états
        :type states: Set[str]
        :return: Fermeture epsilon des états
        :rtype: Set[str]
        """
        return self._cached_epsilon_closure(states)

    def _simulate_epsilon_nfa(self, word: str) -> bool:
        """
        Simule l'exécution du ε-NFA sur un mot donné.

        :param word: Mot à tester
        :type word: str
        :return: True si le mot est accepté, False sinon
        :rtype: bool
        """
        # Ensemble des états courants (commence par l'état initial)
        current_states = {self._initial_state}

        # Appliquer les fermetures epsilon au début
        current_states = self.epsilon_closure(current_states)

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
            current_states = self.epsilon_closure(next_states)

            # Si aucun état n'est possible, le mot est rejeté
            if not current_states:
                return False

        # Vérifier si au moins un état final est atteint
        return bool(current_states.intersection(self._final_states))

    def _cached_epsilon_closure(self, states: Set[str]) -> Set[str]:
        """
        Calcule la fermeture epsilon avec mise en cache.

        :param states: Ensemble d'états
        :type states: Set[str]
        :return: Fermeture epsilon des états
        :rtype: Set[str]
        """
        # Créer une clé de cache
        states_frozen = frozenset(states)

        # Vérifier le cache
        if states_frozen in self._epsilon_closure_cache:
            return self._epsilon_closure_cache[states_frozen].copy()

        # Calculer la fermeture epsilon
        closure = self._compute_epsilon_closure(states)

        # Mettre en cache
        self._epsilon_closure_cache[states_frozen] = closure.copy()

        return closure

    def _compute_epsilon_closure(self, states: Set[str]) -> Set[str]:
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
            epsilon_key = (current, self._epsilon_symbol)
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
            for symbol in self._alphabet.union({self._epsilon_symbol}):
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
                for symbol in self._alphabet.union({self._epsilon_symbol}):
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

    def to_nfa(self) -> "NFA":
        """
        Convertit le ε-NFA en NFA en éliminant les transitions epsilon.

        :return: NFA équivalent
        :rtype: NFA
        """
        try:
            # Import local pour éviter les dépendances circulaires
            from .nfa import NFA

            # Calculer la fermeture epsilon de chaque état
            epsilon_closures = {}
            for state in self._states:
                epsilon_closures[state] = self.epsilon_closure({state})

            # Construire les nouvelles transitions
            new_transitions = {}

            for state in self._states:
                for symbol in self._alphabet:
                    # Calculer les transitions directes
                    direct_transitions = set()
                    for closure_state in epsilon_closures[state]:
                        transition_key = (closure_state, symbol)
                        if transition_key in self._transitions:
                            direct_transitions.update(self._transitions[transition_key])

                    # Calculer les transitions via epsilon
                    epsilon_transitions = set()
                    for target in direct_transitions:
                        epsilon_transitions.update(epsilon_closures[target])

                    if epsilon_transitions:
                        new_transitions[(state, symbol)] = epsilon_transitions

            # Ajuster les états finaux
            new_final_states = set()
            for state in self._states:
                if epsilon_closures[state].intersection(self._final_states):
                    new_final_states.add(state)

            return NFA(
                states=self._states.copy(),
                alphabet=self._alphabet.copy(),
                transitions=new_transitions,
                initial_state=self._initial_state,
                final_states=new_final_states,
            )

        except Exception as e:
            raise ConversionError(f"Error converting ε-NFA to NFA: {e}") from e

    def to_dfa(self) -> "DFA":
        """
        Convertit le ε-NFA en DFA via NFA.

        :return: DFA équivalent
        :rtype: DFA
        """
        try:
            # Convertir vers NFA d'abord
            nfa = self.to_nfa()
            # Puis convertir vers DFA
            return nfa.to_dfa()

        except Exception as e:
            raise ConversionError(f"Error converting ε-NFA to DFA: {e}") from e

    def to_dfa_direct(self) -> "DFA":
        """
        Convertit le ε-NFA en DFA directement.

        :return: DFA équivalent
        :rtype: DFA
        """
        try:
            # Import local pour éviter les dépendances circulaires
            from .dfa import DFA

            # État initial du DFA (fermeture epsilon de l'état initial)
            dfa_initial = frozenset(self.epsilon_closure({self._initial_state}))

            # États du DFA (sous-ensembles d'états du ε-NFA)
            dfa_states = {dfa_initial}
            dfa_transitions = {}

            # File d'attente pour traiter les nouveaux états
            to_process = [dfa_initial]

            while to_process:
                current_dfa_state = to_process.pop(0)

                # Pour chaque symbole de l'alphabet
                for symbol in self._alphabet:
                    # Calculer l'union des transitions du ε-NFA
                    next_states = set()
                    for epsilon_nfa_state in current_dfa_state:
                        transition_key = (epsilon_nfa_state, symbol)
                        if transition_key in self._transitions:
                            next_states.update(self._transitions[transition_key])

                    if next_states:
                        # Appliquer la fermeture epsilon
                        next_states = self.epsilon_closure(next_states)
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
            raise ConversionError(f"Error converting ε-NFA to DFA directly: {e}") from e

    def union(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """
        Calcule l'union de deux ε-NFA.

        :param other: Autre ε-NFA
        :type other: EpsilonNFA
        :return: ε-NFA acceptant l'union des langages
        :rtype: EpsilonNFA
        """
        # Créer un nouvel état initial
        new_initial = "q0_union"

        # Combiner les états (avec préfixes pour éviter les conflits)
        new_states = {new_initial}
        new_states.update(f"enfa1_{state}" for state in self.states)
        new_states.update(f"enfa2_{state}" for state in other.states)

        # Combiner les alphabets
        new_alphabet = self.alphabet.union(other.alphabet)

        # Combiner les transitions
        new_transitions = {}

        # Transitions du premier ε-NFA
        for source in self.states:
            for symbol in self.alphabet.union({self._epsilon_symbol}):
                targets = self.get_transitions(source, symbol)
                if targets:
                    new_source = f"enfa1_{source}"
                    new_targets = {f"enfa1_{target}" for target in targets}
                    new_transitions[(new_source, symbol)] = new_targets

        # Transitions du second ε-NFA
        for source in other.states:
            for symbol in other.alphabet.union({other.epsilon_symbol}):
                targets = other.get_transitions(source, symbol)
                if targets:
                    new_source = f"enfa2_{source}"
                    new_targets = {f"enfa2_{target}" for target in targets}
                    new_transitions[(new_source, symbol)] = new_targets

        # Ajouter les transitions depuis le nouvel état initial
        new_transitions[(new_initial, self._epsilon_symbol)] = {
            f"enfa1_{self.initial_state}",
            f"enfa2_{other.initial_state}",
        }

        # Combiner les états finaux
        new_final_states = {f"enfa1_{state}" for state in self.final_states}
        new_final_states.update(f"enfa2_{state}" for state in other.final_states)

        return EpsilonNFA(
            states=new_states,
            alphabet=new_alphabet,
            transitions=new_transitions,
            initial_state=new_initial,
            final_states=new_final_states,
            epsilon_symbol=self._epsilon_symbol,
        )

    def concatenation(self, other: "EpsilonNFA") -> "EpsilonNFA":
        """
        Calcule la concaténation de deux ε-NFA.

        :param other: Autre ε-NFA
        :type other: EpsilonNFA
        :return: ε-NFA acceptant la concaténation des langages
        :rtype: EpsilonNFA
        """
        # Combiner les états (avec préfixes pour éviter les conflits)
        new_states = {f"enfa1_{state}" for state in self.states}
        new_states.update(f"enfa2_{state}" for state in other.states)

        # Combiner les alphabets
        new_alphabet = self.alphabet.union(other.alphabet)

        # Combiner les transitions
        new_transitions = {}

        # Transitions du premier ε-NFA
        for source in self.states:
            for symbol in self.alphabet.union({self._epsilon_symbol}):
                targets = self.get_transitions(source, symbol)
                if targets:
                    new_source = f"enfa1_{source}"
                    new_targets = {f"enfa1_{target}" for target in targets}
                    new_transitions[(new_source, symbol)] = new_targets

        # Transitions du second ε-NFA
        for source in other.states:
            for symbol in other.alphabet.union({other.epsilon_symbol}):
                targets = other.get_transitions(source, symbol)
                if targets:
                    new_source = f"enfa2_{source}"
                    new_targets = {f"enfa2_{target}" for target in targets}
                    new_transitions[(new_source, symbol)] = new_targets

        # Connecter les états finaux du premier ε-NFA à l'état initial du second
        for final_state in self.final_states:
            transition_key = (f"enfa1_{final_state}", self._epsilon_symbol)
            if transition_key not in new_transitions:
                new_transitions[transition_key] = set()
            new_transitions[transition_key].add(f"enfa2_{other.initial_state}")

        # Nouvel état initial (celui du premier ε-NFA)
        new_initial = f"enfa1_{self.initial_state}"

        # Nouveaux états finaux (ceux du second ε-NFA)
        new_final_states = {f"enfa2_{state}" for state in other.final_states}

        return EpsilonNFA(
            states=new_states,
            alphabet=new_alphabet,
            transitions=new_transitions,
            initial_state=new_initial,
            final_states=new_final_states,
            epsilon_symbol=self._epsilon_symbol,
        )

    def kleene_star(self) -> "EpsilonNFA":
        """
        Calcule l'étoile de Kleene du ε-NFA.

        :return: ε-NFA acceptant l'étoile de Kleene du langage
        :rtype: EpsilonNFA
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
        new_transitions[(new_initial, self._epsilon_symbol)] = {self._initial_state}

        # Connecter les états finaux à l'état initial
        for final_state in self._final_states:
            transition_key = (final_state, self._epsilon_symbol)
            if transition_key not in new_transitions:
                new_transitions[transition_key] = set()
            new_transitions[transition_key].add(self._initial_state)

        # Nouveaux états finaux (ancien état initial + anciens états finaux)
        new_final_states = {new_initial}
        new_final_states.update(self._final_states)

        return EpsilonNFA(
            states=new_states,
            alphabet=new_alphabet,
            transitions=new_transitions,
            initial_state=new_initial,
            final_states=new_final_states,
            epsilon_symbol=self._epsilon_symbol,
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

            # Vérifier que l'epsilon_symbol n'est pas dans l'alphabet
            if self._epsilon_symbol in self._alphabet:
                return False

            # Vérifier que toutes les transitions sont valides
            for (source, symbol), targets in self._transitions.items():
                if source not in self._states:
                    return False
                if not targets.issubset(self._states):
                    return False
                if symbol not in self._alphabet and symbol != self._epsilon_symbol:
                    return False

            return True
        except (AttributeError, TypeError, ValueError, KeyError):
            # Capturer les erreurs spécifiques qui peuvent survenir
            # lors de la validation de l'automate
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
            "epsilon_symbol": self._epsilon_symbol,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EpsilonNFA":
        """
        Crée un ε-NFA depuis un dictionnaire.

        :param data: Dictionnaire représentant l'automate
        :type data: Dict[str, Any]
        :return: Instance du ε-NFA
        :rtype: EpsilonNFA
        """
        states = set(data["states"])
        alphabet = set(data["alphabet"])
        transitions = {
            tuple(key.split(",")): set(targets)
            for key, targets in data["transitions"].items()
        }
        initial_state = data["initial_state"]
        final_states = set(data["final_states"])
        epsilon_symbol = data.get("epsilon_symbol", "ε")

        return cls(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
            epsilon_symbol=epsilon_symbol,
        )

    def __str__(self) -> str:
        """
        Représentation string de l'automate.

        :return: Représentation string de l'automate
        :rtype: str
        """
        return (
            f"ε-NFA(states={len(self._states)}, transitions={len(self._transitions)})"
        )

    def __repr__(self) -> str:
        """
        Représentation détaillée de l'automate.

        :return: Représentation détaillée de l'automate
        :rtype: str
        """
        return (
            f"EpsilonNFA(states={self._states}, alphabet={self._alphabet}, "
            f"initial_state='{self._initial_state}', final_states={self._final_states}, "
            f"transitions={self._transitions}, epsilon_symbol='{self._epsilon_symbol}')"
        )
