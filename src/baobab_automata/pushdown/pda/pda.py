"""
Implémentation des automates à pile non-déterministes (PDA).

Ce module implémente la classe PDA pour la reconnaissance des langages hors-contexte.
Les PDA étendent les automates finis en ajoutant une pile qui permet de reconnaître
des langages plus complexes comme a^n b^n ou les palindromes.
"""

from collections import deque
from typing import Any, Dict, Optional, Set, Tuple

from ..abstract_pushdown_automaton import AbstractPushdownAutomaton
from .pda_configuration import PDAConfiguration
from .pda_exceptions import (
    InvalidPDAError,
    InvalidStateError,
    InvalidTransitionError,
    PDAError,
    PDAValidationError,
)
from .pda_operations import PDAOperations


class PDA(AbstractPushdownAutomaton):
    """Automate à pile non-déterministe pour la reconnaissance de langages hors-contexte.

    Un PDA est défini par un tuple (Q, Σ, Γ, δ, q0, Z0, F) où :
    - Q : ensemble fini d'états
    - Σ : alphabet d'entrée
    - Γ : alphabet de pile
    - δ : fonction de transition Q × (Σ ∪ {ε}) × Γ → P(Q × Γ*)
    - q0 : état initial
    - Z0 : symbole initial de pile
    - F : ensemble d'états finaux
    """

    def __init__(
        self,
        states: Set[str],
        input_alphabet: Set[str],
        stack_alphabet: Set[str],
        transitions: Dict[Tuple[str, str, str], Set[Tuple[str, str]]],
        initial_state: str,
        initial_stack_symbol: str,
        final_states: Set[str],
        name: Optional[str] = None,
    ) -> None:
        """Initialise un automate à pile non-déterministe.

        :param states: Ensemble des états
        :param input_alphabet: Alphabet d'entrée
        :param stack_alphabet: Alphabet de pile
        :param transitions: Fonction de transition
        :param initial_state: État initial
        :param initial_stack_symbol: Symbole initial de pile
        :param final_states: États finaux
        :param name: Nom optionnel de l'automate
        :raises InvalidPDAError: Si l'automate n'est pas valide
        """
        self._states = frozenset(states)
        self._input_alphabet = frozenset(input_alphabet)
        self._stack_alphabet = frozenset(stack_alphabet)
        self._transitions = transitions
        self._initial_state = initial_state
        self._initial_stack_symbol = initial_stack_symbol
        self._final_states = frozenset(final_states)
        self._name = name

        # Cache pour les optimisations
        self._epsilon_closure_cache: Dict[Tuple[str, str], Set[Tuple[str, str]]] = {}
        self._reachable_states_cache: Dict[str, Set[str]] = {}

        # Validation automatique
        if not self.validate():
            raise InvalidPDAError("L'automate à pile n'est pas valide")

    @property
    def states(self) -> Set[str]:
        """Retourne l'ensemble des états de l'automate.

        :return: Ensemble des états
        """
        return set(self._states)

    @property
    def input_alphabet(self) -> Set[str]:
        """Retourne l'alphabet d'entrée de l'automate.

        :return: Alphabet d'entrée
        """
        return set(self._input_alphabet)

    @property
    def stack_alphabet(self) -> Set[str]:
        """Retourne l'alphabet de pile de l'automate.

        :return: Alphabet de pile
        """
        return set(self._stack_alphabet)

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
        return set(self._final_states)

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
        :raises PDAError: En cas d'erreur de traitement
        """
        if not isinstance(word, str):
            raise PDAError(f"Le mot doit être une chaîne, reçu: {type(word)}")

        try:
            return self._simulate_word(word)
        except Exception as e:
            raise PDAError(f"Erreur lors de la simulation du mot '{word}': {e}")

    def get_transitions(
        self, state: str, input_symbol: str, stack_symbol: str
    ) -> Set[Tuple[str, str]]:
        """Récupère les transitions possibles depuis un état donné.

        :param state: État source
        :param input_symbol: Symbole d'entrée (peut être ε)
        :param stack_symbol: Symbole de pile
        :return: Ensemble des transitions possibles (état_destination, symboles_pile)
        :raises InvalidStateError: Si l'état n'existe pas
        """
        if state not in self._states:
            raise InvalidStateError(state)

        if not isinstance(input_symbol, str):
            raise InvalidTransitionError(
                (state, input_symbol, stack_symbol),
                "Le symbole d'entrée doit être une chaîne",
            )

        if not isinstance(stack_symbol, str):
            raise InvalidTransitionError(
                (state, input_symbol, stack_symbol),
                "Le symbole de pile doit être une chaîne",
            )

        # Recherche des transitions exactes
        exact_transitions = self._transitions.get(
            (state, input_symbol, stack_symbol), set()
        )

        return exact_transitions

    def is_final_state(self, state: str) -> bool:
        """Vérifie si un état est final.

        :param state: État à vérifier
        :return: True si l'état est final, False sinon
        :raises InvalidStateError: Si l'état n'existe pas
        """
        if state not in self._states:
            raise InvalidStateError(state)

        return state in self._final_states

    def get_reachable_states(self, from_state: str) -> Set[str]:
        """Récupère tous les états accessibles depuis un état donné.

        :param from_state: État de départ
        :return: Ensemble des états accessibles
        :raises InvalidStateError: Si l'état n'existe pas
        """
        if from_state not in self._states:
            raise InvalidStateError(from_state)

        # Vérification du cache
        if from_state in self._reachable_states_cache:
            return self._reachable_states_cache[from_state].copy()

        # Calcul des états accessibles
        reachable = set()
        to_visit = deque([from_state])

        while to_visit:
            current_state = to_visit.popleft()
            if current_state in reachable:
                continue

            reachable.add(current_state)

            # Exploration de toutes les transitions possibles
            for (
                source,
                input_sym,
                stack_sym,
            ), destinations in self._transitions.items():
                if source == current_state:
                    for dest_state, _ in destinations:
                        if dest_state not in reachable:
                            to_visit.append(dest_state)

        # Mise en cache
        self._reachable_states_cache[from_state] = reachable.copy()

        return reachable

    def validate(self) -> bool:
        """Valide la cohérence de l'automate.

        :return: True si l'automate est valide, False sinon
        :raises PDAValidationError: Si l'automate n'est pas valide
        """
        try:
            # Validation des états
            if not self._states:
                raise PDAValidationError(
                    "L'automate doit avoir au moins un état", "états"
                )

            if self._initial_state not in self._states:
                raise PDAValidationError(
                    f"L'état initial '{self._initial_state}' n'existe pas",
                    "état_initial",
                )

            if not self._final_states.issubset(self._states):
                invalid_finals = self._final_states - self._states
                raise PDAValidationError(
                    f"États finaux invalides: {invalid_finals}", "états_finaux"
                )

            # Validation des alphabets
            if not self._input_alphabet:
                raise PDAValidationError(
                    "L'alphabet d'entrée ne peut pas être vide", "alphabet_entrée"
                )

            if not self._stack_alphabet:
                raise PDAValidationError(
                    "L'alphabet de pile ne peut pas être vide", "alphabet_pile"
                )

            if self._initial_stack_symbol not in self._stack_alphabet:
                raise PDAValidationError(
                    f"Le symbole initial de pile '{self._initial_stack_symbol}' n'est pas dans l'alphabet de pile",
                    "symbole_pile_initial",
                )

            # Validation des transitions
            for (
                state,
                input_sym,
                stack_sym,
            ), destinations in self._transitions.items():
                if state not in self._states:
                    raise PDAValidationError(
                        f"État source invalide dans la transition: {state}",
                        "transitions",
                    )

                if input_sym != "" and input_sym not in self._input_alphabet:
                    raise PDAValidationError(
                        f"Symbole d'entrée invalide dans la transition: {input_sym}",
                        "transitions",
                    )

                if stack_sym != "" and stack_sym not in self._stack_alphabet:
                    raise PDAValidationError(
                        f"Symbole de pile invalide dans la transition: {stack_sym}",
                        "transitions",
                    )

                if not destinations:
                    raise PDAValidationError(
                        f"Transition sans destination: ({state}, {input_sym}, {stack_sym})",
                        "transitions",
                    )

                for dest_state, stack_symbols in destinations:
                    if dest_state not in self._states:
                        raise PDAValidationError(
                            f"État destination invalide: {dest_state}", "transitions"
                        )

                    if not isinstance(stack_symbols, str):
                        raise PDAValidationError(
                            f"Symboles de pile doivent être une chaîne: {stack_symbols}",
                            "transitions",
                        )

                    for symbol in stack_symbols:
                        if symbol not in self._stack_alphabet:
                            raise PDAValidationError(
                                f"Symbole de pile invalide dans la destination: {symbol}",
                                "transitions",
                            )

            return True

        except PDAValidationError:
            return False
        except Exception as e:
            raise PDAValidationError(
                f"Erreur inattendue lors de la validation: {e}", "validation_générale"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'automate en dictionnaire.

        :return: Représentation dictionnaire de l'automate
        """
        # Conversion des transitions en format sérialisable
        serializable_transitions = {}
        for (state, input_sym, stack_sym), destinations in self._transitions.items():
            key = (state, input_sym, stack_sym)
            serializable_transitions[key] = list(destinations)

        return {
            "type": "PDA",
            "states": list(self._states),
            "input_alphabet": list(self._input_alphabet),
            "stack_alphabet": list(self._stack_alphabet),
            "transitions": serializable_transitions,
            "initial_state": self._initial_state,
            "initial_stack_symbol": self._initial_stack_symbol,
            "final_states": list(self._final_states),
            "name": self._name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PDA":
        """Crée un automate à partir d'un dictionnaire.

        :param data: Données de l'automate
        :return: Instance de PDA
        :raises InvalidPDAError: Si les données sont invalides
        """
        try:
            # Validation du type
            if data.get("type") != "PDA":
                raise InvalidPDAError(f"Type d'automate invalide: {data.get('type')}")

            # Conversion des transitions
            transitions = {}
            for (state, input_sym, stack_sym), destinations in data[
                "transitions"
            ].items():
                key = (state, input_sym, stack_sym)
                transitions[key] = set(destinations)

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

        except KeyError as e:
            raise InvalidPDAError(
                f"Données d'automate incomplètes: clé manquante '{e}'"
            )
        except Exception as e:
            raise InvalidPDAError(f"Données d'automate invalides: {e}")

    def _simulate_word(self, word: str) -> bool:
        """Simule la reconnaissance d'un mot de manière non-déterministe.

        :param word: Mot à simuler
        :return: True si le mot est accepté, False sinon
        """
        # Configuration initiale
        initial_config = PDAConfiguration(
            state=self._initial_state,
            remaining_input=word,
            stack=self._initial_stack_symbol,
        )

        # File de priorité pour la simulation (BFS)
        config_queue = deque([initial_config])
        visited_configs = set()

        # Limitation de la profondeur pour éviter les boucles infinies
        max_iterations = len(word) * len(self._states) * 100
        iteration_count = 0

        while config_queue and iteration_count < max_iterations:
            iteration_count += 1
            current_config = config_queue.popleft()

            # Vérification de l'acceptation
            if current_config.remaining_input == "" and self.is_final_state(
                current_config.state
            ):
                return True

            # Éviter les configurations déjà visitées
            config_key = (
                current_config.state,
                current_config.remaining_input,
                current_config.stack,
            )
            if config_key in visited_configs:
                continue
            visited_configs.add(config_key)

            # Exploration des transitions possibles
            # Transition avec symbole d'entrée
            if current_config.remaining_input:
                input_symbol = current_config.remaining_input[0]
                transitions = self.get_transitions(
                    current_config.state, input_symbol, current_config.stack_top or ""
                )

                for next_state, stack_symbols in transitions:
                    new_config = self._apply_transition(
                        current_config, next_state, stack_symbols
                    )
                    if new_config is not None:
                        config_queue.append(new_config)

            # Transitions epsilon (sans consommer de symbole d'entrée)
            epsilon_transitions = self.get_transitions(
                current_config.state,
                "",  # Symbole epsilon
                current_config.stack_top or "",
            )

            for next_state, stack_symbols in epsilon_transitions:
                new_config = self._apply_epsilon_transition(
                    current_config, next_state, stack_symbols
                )
                if new_config is not None:
                    config_queue.append(new_config)

        return False

    def _apply_transition(
        self, config: PDAConfiguration, next_state: str, stack_symbols: str
    ) -> Optional[PDAConfiguration]:
        """Applique une transition à une configuration.

        :param config: Configuration actuelle
        :param next_state: État de destination
        :param stack_symbols: Symboles à empiler
        :return: Nouvelle configuration ou None si la transition n'est pas applicable
        """
        try:
            # Consommation du symbole d'entrée
            if config.remaining_input:
                new_config = config.consume_input(config.remaining_input[0])
            else:
                new_config = config

            # Changement d'état
            new_config = new_config.change_state(next_state)

            # Gestion de la pile
            if config.stack_top:
                # Retirer le symbole du sommet
                new_config = new_config.pop_symbol()

            # Empiler les nouveaux symboles
            if stack_symbols:
                new_config = new_config.push_symbols(stack_symbols)

            return new_config

        except ValueError:
            # Transition non applicable
            return None

    def _apply_epsilon_transition(
        self, config: PDAConfiguration, next_state: str, stack_symbols: str
    ) -> Optional[PDAConfiguration]:
        """Applique une transition epsilon à une configuration.

        :param config: Configuration actuelle
        :param next_state: État de destination
        :param stack_symbols: Symboles à empiler
        :return: Nouvelle configuration ou None si la transition n'est pas applicable
        """
        try:
            # Pas de consommation de symbole d'entrée pour les transitions epsilon
            new_config = config

            # Changement d'état
            new_config = new_config.change_state(next_state)

            # Gestion de la pile
            if config.stack_top:
                # Retirer le symbole du sommet
                new_config = new_config.pop_symbol()

            # Empiler les nouveaux symboles
            if stack_symbols:
                new_config = new_config.push_symbols(stack_symbols)

            return new_config

        except ValueError:
            # Transition non applicable
            return None

    def _epsilon_closure(self, state: str, stack_symbol: str) -> Set[Tuple[str, str]]:
        """Calcule la fermeture epsilon pour un état et un symbole de pile.

        :param state: État de départ
        :param stack_symbol: Symbole de pile
        :return: Ensemble des configurations accessibles par transitions epsilon
        """
        cache_key = (state, stack_symbol)
        if cache_key in self._epsilon_closure_cache:
            return self._epsilon_closure_cache[cache_key]

        closure = set()
        to_process = deque([(state, stack_symbol)])
        processed = set()

        while to_process:
            current_state, current_stack = to_process.popleft()

            if (current_state, current_stack) in processed:
                continue
            processed.add((current_state, current_stack))

            # Recherche des transitions epsilon
            epsilon_transitions = self._transitions.get(
                (current_state, "", current_stack), set()
            )

            for next_state, stack_symbols in epsilon_transitions:
                closure.add((next_state, stack_symbols))

                # Traitement de la pile
                if current_stack:
                    new_stack = current_stack[:-1] + stack_symbols
                else:
                    new_stack = stack_symbols

                if new_stack:
                    to_process.append((next_state, new_stack[-1]))
                else:
                    to_process.append((next_state, ""))

        self._epsilon_closure_cache[cache_key] = closure
        return closure

    def union(self, other: "PDA") -> "PDA":
        """Crée l'union de deux PDA.

        :param other: Autre PDA
        :return: PDA reconnaissant l'union des langages
        :raises PDAOperationError: Si les PDA ne sont pas compatibles
        """
        return PDAOperations.union(self, other)

    def concatenation(self, other: "PDA") -> "PDA":
        """Crée la concaténation de deux PDA.

        :param other: Autre PDA
        :return: PDA reconnaissant la concaténation des langages
        :raises PDAOperationError: Si les PDA ne sont pas compatibles
        """
        return PDAOperations.concatenation(self, other)

    def kleene_star(self) -> "PDA":
        """Crée l'étoile de Kleene d'un PDA.

        :return: PDA reconnaissant l'étoile de Kleene du langage
        :raises PDAOperationError: Si l'opération échoue
        """
        return PDAOperations.kleene_star(self)

    def __str__(self) -> str:
        """Retourne la représentation textuelle de l'automate.

        :return: Représentation textuelle
        """
        name_str = f" '{self._name}'" if self._name else ""
        return (
            f"PDA{name_str}("
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
            f"PDA("
            f"states={self._states}, "
            f"input_alphabet={self._input_alphabet}, "
            f"stack_alphabet={self._stack_alphabet}, "
            f"transitions={self._transitions}, "
            f"initial_state='{self._initial_state}', "
            f"initial_stack_symbol='{self._initial_stack_symbol}', "
            f"final_states={self._final_states}, "
            f"name='{self._name}')"
        )
