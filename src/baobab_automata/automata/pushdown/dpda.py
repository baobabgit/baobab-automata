"""
Implémentation des automates à pile déterministes (DPDA).

Ce module implémente la classe DPDA pour la reconnaissance des langages
hors-contexte déterministes avec des algorithmes optimisés.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict

from .abstract_pushdown_automaton import AbstractPushdownAutomaton
from .dpda_configuration import DPDAConfiguration
from .dpda_exceptions import DPDAError, InvalidDPDAError


class DPDA(AbstractPushdownAutomaton):
    """Automate à pile déterministe pour la reconnaissance de langages hors-contexte déterministes.

    Un DPDA est un PDA avec des contraintes de déterminisme qui garantissent
    qu'il n'y a jamais plus d'une transition possible pour une configuration donnée.
    Cela permet des algorithmes de reconnaissance plus efficaces.

    :param states: Ensemble des états
    :param input_alphabet: Alphabet d'entrée
    :param stack_alphabet: Alphabet de pile
    :param transitions: Fonction de transition déterministe
    :param initial_state: État initial
    :param initial_stack_symbol: Symbole initial de pile
    :param final_states: États finaux
    :param name: Nom optionnel de l'automate
    :raises InvalidDPDAError: Si l'automate n'est pas valide ou non-déterministe
    """

    def __init__(
        self,
        states: Set[str],
        input_alphabet: Set[str],
        stack_alphabet: Set[str],
        transitions: Dict[Tuple[str, str, str], Tuple[str, str]],
        initial_state: str,
        initial_stack_symbol: str,
        final_states: Set[str],
        name: Optional[str] = None,
    ) -> None:
        """Initialise un automate à pile déterministe.

        :param states: Ensemble des états
        :param input_alphabet: Alphabet d'entrée
        :param stack_alphabet: Alphabet de pile
        :param transitions: Fonction de transition déterministe
        :param initial_state: État initial
        :param initial_stack_symbol: Symbole initial de pile
        :param final_states: États finaux
        :param name: Nom optionnel de l'automate
        :raises InvalidDPDAError: Si l'automate n'est pas valide ou non-déterministe
        """
        self._states = states
        self._input_alphabet = input_alphabet
        self._stack_alphabet = stack_alphabet
        self._transitions = transitions
        self._initial_state = initial_state
        self._initial_stack_symbol = initial_stack_symbol
        self._final_states = final_states
        self._name = name

        # Cache pour les optimisations
        self._epsilon_closure_cache: Dict[
            Tuple[str, str], Optional[Tuple[str, str]]
        ] = {}
        self._transition_cache: Dict[
            Tuple[str, str, str], Optional[Tuple[str, str]]
        ] = {}

        # Validation de l'automate
        self.validate()

    @property
    def states(self) -> Set[str]:
        """Retourne l'ensemble des états de l'automate.

        :return: Ensemble des états
        """
        return self._states

    @property
    def input_alphabet(self) -> Set[str]:
        """Retourne l'alphabet d'entrée de l'automate.

        :return: Alphabet d'entrée
        """
        return self._input_alphabet

    @property
    def stack_alphabet(self) -> Set[str]:
        """Retourne l'alphabet de pile de l'automate.

        :return: Alphabet de pile
        """
        return self._stack_alphabet

    @property
    def initial_state(self) -> str:
        """Retourne l'état initial de l'automate.

        :return: État initial
        """
        return self._initial_state

    @property
    def initial_stack_symbol(self) -> str:
        """Retourne le symbole initial de pile.

        :return: Symbole initial de pile
        """
        return self._initial_stack_symbol

    @property
    def final_states(self) -> Set[str]:
        """Retourne l'ensemble des états finaux.

        :return: États finaux
        """
        return self._final_states

    @property
    def name(self) -> Optional[str]:
        """Retourne le nom de l'automate.

        :return: Nom de l'automate ou None
        """
        return self._name

    def accepts(self, word: str) -> bool:
        """Vérifie si un mot est accepté par l'automate.

        :param word: Mot à tester
        :return: True si le mot est accepté, False sinon
        :raises DPDAError: En cas d'erreur de traitement
        """
        try:
            return self._simulate_word_deterministic(word)
        except Exception as e:
            raise DPDAError(
                f"Erreur lors de la reconnaissance du mot '{word}': {e}"
            ) from e

    def _simulate_word_deterministic(self, word: str) -> bool:
        """Simule la reconnaissance d'un mot de manière déterministe.

        :param word: Mot à simuler
        :return: True si le mot est accepté, False sinon
        """
        # Configuration initiale
        current_config = DPDAConfiguration(
            state=self._initial_state,
            remaining_input=word,
            stack=self._initial_stack_symbol,
        )

        # Simulation déterministe
        while True:
            # Vérification de l'acceptation
            if current_config.is_accepting and self.is_final_state(
                current_config.state
            ):
                return True

            # Récupération de la transition unique
            input_symbol = (
                current_config.remaining_input[0]
                if current_config.remaining_input
                else ""
            )
            stack_symbol = current_config.stack_top

            if stack_symbol is None:
                return False

            # Recherche de transition avec symbole d'entrée
            transition = self.get_transition(
                current_config.state, input_symbol, stack_symbol
            )

            # Si pas de transition avec symbole d'entrée, chercher transition epsilon
            if transition is None:
                transition = self.get_transition(current_config.state, "", stack_symbol)

            if transition is None:
                return False

            # Application de la transition
            new_state, stack_operation = transition

            # Mise à jour de la configuration
            if input_symbol and input_symbol != "":
                current_config = current_config.consume_input(1)
            current_config = current_config.change_state(new_state)

            # Gestion de la pile
            if stack_operation == "":
                # Dépilage
                current_config = current_config.pop_symbols(1)
            else:
                # Remplacement du sommet
                current_config = current_config.replace_stack_top(stack_operation)

    def get_transition(
        self, state: str, input_symbol: str, stack_symbol: str
    ) -> Optional[Tuple[str, str]]:
        """Récupère la transition unique depuis un état donné.

        :param state: État source
        :param input_symbol: Symbole d'entrée (peut être ε)
        :param stack_symbol: Symbole de pile
        :return: Transition unique ou None si aucune transition
        :raises InvalidDPDAError: Si l'état n'existe pas
        :raises DPDAError: Si plusieurs transitions sont possibles
        """
        if state not in self._states:
            raise InvalidDPDAError(f"État invalide: {state}")

        # Vérification du cache
        cache_key = (state, input_symbol, stack_symbol)
        if cache_key in self._transition_cache:
            return self._transition_cache[cache_key]

        # Recherche de la transition
        transition = self._transitions.get((state, input_symbol, stack_symbol))

        # Mise en cache
        self._transition_cache[cache_key] = transition

        return transition

    def get_transitions(
        self, state: str, input_symbol: str, stack_symbol: str
    ) -> Set[Tuple[str, str]]:
        """Récupère les transitions possibles depuis un état donné.

        Pour un DPDA, cette méthode retourne au plus une transition.

        :param state: État source
        :param input_symbol: Symbole d'entrée (peut être ε)
        :param stack_symbol: Symbole de pile
        :return: Ensemble des transitions possibles (au plus une)
        """
        transition = self.get_transition(state, input_symbol, stack_symbol)
        return {transition} if transition else set()

    def is_final_state(self, state: str) -> bool:
        """Vérifie si un état est final.

        :param state: État à vérifier
        :return: True si l'état est final, False sinon
        """
        return state in self._final_states

    def get_reachable_states(self, from_state: str) -> Set[str]:
        """Récupère tous les états accessibles depuis un état donné.

        :param from_state: État de départ
        :return: Ensemble des états accessibles
        """
        if from_state not in self._states:
            return set()

        visited = set()
        to_visit = {from_state}

        while to_visit:
            current_state = to_visit.pop()
            if current_state in visited:
                continue

            visited.add(current_state)

            # Recherche des états accessibles via les transitions
            for (state, input_symbol, stack_symbol), (
                next_state,
                _,
            ) in self._transitions.items():
                if state == current_state:
                    to_visit.add(next_state)

        return visited

    def validate(self) -> bool:
        """Valide la cohérence et le déterminisme de l'automate.

        :return: True si l'automate est valide, False sinon
        :raises InvalidDPDAError: Si l'automate n'est pas valide
        """
        errors = []

        # Validation de base
        if not self._states:
            errors.append("L'automate doit avoir au moins un état")

        if self._initial_state not in self._states:
            errors.append(f"L'état initial '{self._initial_state}' n'existe pas")

        if not self._final_states.issubset(self._states):
            invalid_finals = self._final_states - self._states
            errors.append(f"États finaux invalides: {invalid_finals}")

        if self._initial_stack_symbol not in self._stack_alphabet:
            errors.append(
                f"Le symbole initial de pile '{self._initial_stack_symbol}' n'est pas dans l'alphabet de pile"
            )

        # Validation des transitions
        for (state, _, stack_symbol), (
            next_state,
            stack_operation,
        ) in self._transitions.items():
            if state not in self._states:
                errors.append(f"Transition depuis un état invalide: {state}")

            if next_state not in self._states:
                errors.append(f"Transition vers un état invalide: {next_state}")

            # Note: input_symbol est ignoré car on utilise _ dans la boucle

            if stack_symbol not in self._stack_alphabet:
                errors.append(
                    f"Symbole de pile invalide dans la transition: {stack_symbol}"
                )

            # Validation de l'opération de pile
            for symbol in stack_operation:
                if symbol not in self._stack_alphabet:
                    errors.append(
                        f"Symbole de pile invalide dans l'opération: {symbol}"
                    )

        # Validation du déterminisme
        determinism_errors = self._validate_determinism()
        errors.extend(determinism_errors)

        if errors:
            raise InvalidDPDAError(
                "L'automate n'est pas valide", validation_errors=errors
            )

        return True

    def _validate_determinism(self) -> List[str]:
        """Valide que l'automate respecte les contraintes de déterminisme.

        :return: Liste des erreurs de déterminisme
        """
        errors = []

        # Vérification des conflits de transitions
        transition_keys = defaultdict(list)
        for (
            state,
            input_symbol,
            stack_symbol,
        ), transition in self._transitions.items():
            key = (state, input_symbol, stack_symbol)
            transition_keys[key].append(transition)

        for key, transitions in transition_keys.items():
            if len(transitions) > 1:
                errors.append(f"Conflit de déterminisme pour {key}: {transitions}")

        # Vérification des conflits epsilon/symbole
        epsilon_states = set()
        symbol_states = set()

        for state, input_symbol, stack_symbol in self._transitions.keys():
            if input_symbol == "":
                epsilon_states.add(state)
            else:
                symbol_states.add(state)

        conflicts = epsilon_states.intersection(symbol_states)
        if conflicts:
            errors.append(f"Conflits epsilon/symbole dans les états: {conflicts}")

        return errors

    def _detect_conflicts(self) -> List[str]:
        """Détecte les conflits de déterminisme dans l'automate.

        :return: Liste des descriptions des conflits détectés
        """
        conflicts = []

        # Détection des conflits de transitions
        transition_keys = defaultdict(list)
        for (
            state,
            input_symbol,
            stack_symbol,
        ), transition in self._transitions.items():
            key = (state, input_symbol, stack_symbol)
            transition_keys[key].append(transition)

        for key, transitions in transition_keys.items():
            if len(transitions) > 1:
                conflicts.append(f"Conflit de transitions pour {key}: {transitions}")

        # Détection des conflits epsilon/symbole
        epsilon_states = set()
        symbol_states = set()

        for state, input_symbol, stack_symbol in self._transitions.keys():
            if input_symbol == "":
                epsilon_states.add(state)
            else:
                symbol_states.add(state)

        conflicts_epsilon = epsilon_states.intersection(symbol_states)
        if conflicts_epsilon:
            conflicts.append(
                f"Conflits epsilon/symbole dans les états: {conflicts_epsilon}"
            )

        return conflicts

    def analyze_determinism(self) -> Dict[str, Any]:
        """Analyse le niveau de déterminisme de l'automate.

        :return: Dictionnaire avec les métriques de déterminisme
        """
        conflicts = self._detect_conflicts()
        total_transitions = len(self._transitions)

        # Calcul du pourcentage de transitions déterministes
        deterministic_transitions = 0
        for state, input_symbol, stack_symbol in self._transitions.keys():
            key = (state, input_symbol, stack_symbol)
            if len([t for t in self._transitions.keys() if t == key]) == 1:
                deterministic_transitions += 1

        determinism_percentage = (
            (deterministic_transitions / total_transitions * 100)
            if total_transitions > 0
            else 100
        )

        return {
            "total_transitions": total_transitions,
            "deterministic_transitions": deterministic_transitions,
            "determinism_percentage": determinism_percentage,
            "conflicts_detected": len(conflicts),
            "conflicts": conflicts,
            "is_deterministic": len(conflicts) == 0,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'automate en dictionnaire.

        :return: Représentation dictionnaire de l'automate
        """
        return {
            "type": "DPDA",
            "states": list(self._states),
            "input_alphabet": list(self._input_alphabet),
            "stack_alphabet": list(self._stack_alphabet),
            "transitions": {
                f"{state},{input_symbol},{stack_symbol}": f"{next_state},{stack_operation}"
                for (state, input_symbol, stack_symbol), (
                    next_state,
                    stack_operation,
                ) in self._transitions.items()
            },
            "initial_state": self._initial_state,
            "initial_stack_symbol": self._initial_stack_symbol,
            "final_states": list(self._final_states),
            "name": self._name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DPDA":
        """Crée un automate à partir d'un dictionnaire.

        :param data: Données de l'automate
        :return: Instance de DPDA
        :raises InvalidDPDAError: Si les données sont invalides
        """
        try:
            # Conversion des transitions
            transitions = {}
            for key, value in data["transitions"].items():
                state, input_symbol, stack_symbol = key.split(",")
                next_state, stack_operation = value.split(",")
                transitions[(state, input_symbol, stack_symbol)] = (
                    next_state,
                    stack_operation,
                )

            return cls(
                states=set(data["states"]),
                input_alphabet=set(data["input_alphabet"]),
                stack_alphabet=set(data["stack_alphabet"]),
                transitions=transitions,
                initial_state=data["initial_state"],
                initial_stack_symbol=data["initial_stack_symbol"],
                final_states=set(data["final_states"]),
                name=data.get("name"),
            )
        except (KeyError, ValueError) as e:
            raise InvalidDPDAError(f"Données invalides: {e}") from e

    def __str__(self) -> str:
        """Retourne la représentation textuelle de l'automate.

        :return: Représentation textuelle
        """
        return (
            f"DPDA("
            f"states={len(self._states)}, "
            f"input_alphabet={self._input_alphabet}, "
            f"stack_alphabet={self._stack_alphabet}, "
            f"initial_state='{self._initial_state}', "
            f"final_states={self._final_states})"
        )

    def __repr__(self) -> str:
        """Retourne la représentation technique de l'automate.

        :return: Représentation technique pour le débogage
        """
        return (
            f"DPDA("
            f"states={self._states}, "
            f"input_alphabet={self._input_alphabet}, "
            f"stack_alphabet={self._stack_alphabet}, "
            f"transitions=..., "
            f"initial_state='{self._initial_state}', "
            f"initial_stack_symbol='{self._initial_stack_symbol}', "
            f"final_states={self._final_states}, "
            f"name='{self._name}')"
        )
