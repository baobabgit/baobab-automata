"""
Machine de Turing de base.

Ce module implémente la classe TM qui représente une machine de Turing
de base pour la reconnaissance de langages récursivement énumérables.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from .tm_configuration import TMConfiguration
from ...core.interfaces.turing_machine import ITuringMachine, TapeDirection
from ...exceptions.tm_exceptions import (
    InvalidTMError,
    InvalidStateError,
    TMSimulationError,
)


class TM(ITuringMachine):
    """Machine de Turing de base pour la reconnaissance de langages récursivement énumérables.

    Cette classe implémente une machine de Turing avec une bande infinie,
    des états d'acceptation et de rejet, et une fonction de transition
    définissant le comportement de la machine.

    :param states: Ensemble des états de la machine
    :param alphabet: Alphabet d'entrée
    :param tape_alphabet: Alphabet de la bande (incluant le symbole blanc)
    :param transitions: Fonction de transition
    :param initial_state: État initial
    :param accept_states: États d'acceptation
    :param reject_states: États de rejet
    :param blank_symbol: Symbole blanc (par défaut "B")
    :param name: Nom optionnel de la machine
    :raises InvalidTMError: Si la machine n'est pas valide
    """

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        tape_alphabet: Set[str],
        transitions: Dict[Tuple[str, str], Tuple[str, str, TapeDirection]],
        initial_state: str,
        accept_states: Set[str],
        reject_states: Set[str],
        blank_symbol: str = "B",
        name: Optional[str] = None,
    ) -> None:
        """Initialise une machine de Turing.

        :param states: Ensemble des états
        :param alphabet: Alphabet d'entrée
        :param tape_alphabet: Alphabet de la bande
        :param transitions: Fonction de transition
        :param initial_state: État initial
        :param accept_states: États d'acceptation
        :param reject_states: États de rejet
        :param blank_symbol: Symbole blanc
        :param name: Nom optionnel de la machine
        :raises InvalidTMError: Si la machine n'est pas valide
        """
        # Validation des paramètres
        self._validate_parameters(
            states,
            alphabet,
            tape_alphabet,
            initial_state,
            accept_states,
            reject_states,
            blank_symbol,
        )

        # Attribution des attributs
        self._states = states.copy()
        self._alphabet = alphabet.copy()
        self._tape_alphabet = tape_alphabet.copy()
        self._transitions = transitions.copy()
        self._initial_state = initial_state
        self._accept_states = accept_states.copy()
        self._reject_states = reject_states.copy()
        self._blank_symbol = blank_symbol
        self._name = name or f"TM_{id(self)}"

        # Validation de la cohérence
        errors = self.validate()
        if errors:
            raise InvalidTMError(
                f"Invalid Turing Machine: {'; '.join(errors)}"
            )

    def _validate_parameters(
        self,
        states: Set[str],
        alphabet: Set[str],
        tape_alphabet: Set[str],
        initial_state: str,
        accept_states: Set[str],
        reject_states: Set[str],
        blank_symbol: str,
    ) -> None:
        """Valide les paramètres d'entrée.

        :param states: Ensemble des états
        :param alphabet: Alphabet d'entrée
        :param tape_alphabet: Alphabet de la bande
        :param initial_state: État initial
        :param accept_states: États d'acceptation
        :param reject_states: États de rejet
        :param blank_symbol: Symbole blanc
        :raises ValueError: Si un paramètre est invalide
        """
        if not states:
            raise ValueError("States cannot be empty")
        if not alphabet:
            raise ValueError("Alphabet cannot be empty")
        if not tape_alphabet:
            raise ValueError("Tape alphabet cannot be empty")
        if blank_symbol not in tape_alphabet:
            raise ValueError("Blank symbol must be in tape alphabet")
        if initial_state not in states:
            raise ValueError("Initial state must be in states")
        if not accept_states.issubset(states):
            raise ValueError("Accept states must be subset of states")
        if not reject_states.issubset(states):
            raise ValueError("Reject states must be subset of states")
        if accept_states & reject_states:
            raise ValueError("Accept and reject states cannot overlap")

    def simulate(
        self, input_string: str, max_steps: int = 10000
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Simule l'exécution de la machine sur une chaîne d'entrée.

        :param input_string: Chaîne d'entrée
        :param max_steps: Nombre maximum d'étapes
        :return: Tuple (accepté, trace_d_exécution)
        :raises TMSimulationError: En cas d'erreur de simulation
        """
        try:
            trace = []
            tape = input_string
            head_position = 0
            current_state = self._initial_state
            step_count = 0

            # Configuration initiale
            config = TMConfiguration(
                current_state, tape, head_position, step_count
            )
            trace.append(self._config_to_dict(config))

            while step_count < max_steps:
                # Lecture du symbole actuel
                current_symbol = self._get_tape_symbol(tape, head_position)

                # Recherche de la transition
                transition_key = (current_state, current_symbol)
                if transition_key not in self._transitions:
                    # Pas de transition définie - rejet
                    return False, trace

                # Application de la transition
                new_state, write_symbol, direction = self._transitions[
                    transition_key
                ]

                # Mise à jour de la bande
                tape = self._write_to_tape(tape, head_position, write_symbol)

                # Déplacement de la tête
                head_position = self._move_head(head_position, direction)

                # Mise à jour de l'état
                current_state = new_state
                step_count += 1

                # Enregistrement de la configuration
                config = TMConfiguration(
                    current_state, tape, head_position, step_count
                )
                trace.append(self._config_to_dict(config))

                # Vérification des états d'arrêt après la transition
                if current_state in self._accept_states:
                    return True, trace
                if current_state in self._reject_states:
                    return False, trace

            # Timeout - considéré comme rejet
            return False, trace

        except Exception as e:
            raise TMSimulationError(f"Simulation error: {e}") from e

    def _get_tape_symbol(self, tape: str, position: int) -> str:
        """Récupère le symbole à une position donnée sur la bande.

        :param tape: Contenu de la bande
        :param position: Position sur la bande
        :return: Symbole à la position donnée ou symbole blanc
        """
        if 0 <= position < len(tape):
            return tape[position]
        return self._blank_symbol

    def _write_to_tape(self, tape: str, position: int, symbol: str) -> str:
        """Écrit un symbole à une position donnée sur la bande.

        :param tape: Contenu actuel de la bande
        :param position: Position où écrire
        :param symbol: Symbole à écrire
        :return: Nouveau contenu de la bande
        """
        if 0 <= position < len(tape):
            return tape[:position] + symbol + tape[position + 1 :]
        if position == len(tape):
            return tape + symbol
        # Position négative - étendre la bande vers la gauche
        padding = self._blank_symbol * (-position)
        return padding + tape + symbol

    def _move_head(self, position: int, direction: TapeDirection) -> int:
        """Déplace la tête selon la direction.

        :param position: Position actuelle de la tête
        :param direction: Direction de déplacement
        :return: Nouvelle position de la tête
        """
        if direction == TapeDirection.LEFT:
            return position - 1
        if direction == TapeDirection.RIGHT:
            return position + 1
        # STAY
        return position

    def _config_to_dict(self, config: TMConfiguration) -> Dict[str, Any]:
        """Convertit une configuration en dictionnaire pour la trace.

        :param config: Configuration à convertir
        :return: Dictionnaire représentant la configuration
        """
        return {
            "state": config.state,
            "tape": config.tape,
            "head_position": config.head_position,
            "step_count": config.step_count,
            "current_symbol": self._get_tape_symbol(
                config.tape, config.head_position
            ),
        }

    def step(
        self, current_state: str, tape_symbol: str
    ) -> Optional[Tuple[str, str, TapeDirection]]:
        """Effectue une étape de calcul.

        :param current_state: État actuel
        :param tape_symbol: Symbole lu sur la bande
        :return: Transition (nouvel_état, symbole_écrit, direction) ou None
        :raises InvalidStateError: Si l'état n'existe pas
        """
        if current_state not in self._states:
            raise InvalidStateError(f"State '{current_state}' not in states")

        transition_key = (current_state, tape_symbol)
        return self._transitions.get(transition_key)

    def is_halting_state(self, state: str) -> bool:
        """Vérifie si un état est un état d'arrêt.

        :param state: Identifiant de l'état à vérifier
        :return: True si l'état est un état d'arrêt
        """
        return state in self._accept_states or state in self._reject_states

    def validate(self) -> List[str]:
        """Valide la cohérence de la machine.

        :return: Liste des erreurs de validation
        """
        errors = []

        # Validation des états
        if not self._states:
            errors.append("Machine must have at least one state")

        # Validation des alphabets
        if not self._alphabet:
            errors.append("Input alphabet cannot be empty")
        if not self._tape_alphabet:
            errors.append("Tape alphabet cannot be empty")

        # Validation de l'inclusion des alphabets
        if not self._alphabet.issubset(self._tape_alphabet):
            errors.append("Input alphabet must be subset of tape alphabet")

        # Validation des états d'arrêt
        if not self._accept_states and not self._reject_states:
            errors.append("Machine must have at least one halting state")

        # Validation des transitions
        for (state, symbol), (
            new_state,
            write_symbol,
            direction,
        ) in self._transitions.items():
            if state not in self._states:
                errors.append(f"Transition references unknown state '{state}'")
            if symbol not in self._tape_alphabet:
                errors.append(
                    f"Transition references unknown tape symbol '{symbol}'"
                )
            if new_state not in self._states:
                errors.append(
                    f"Transition references unknown target state '{new_state}'"
                )
            if write_symbol not in self._tape_alphabet:
                errors.append(
                    f"Transition writes unknown symbol '{write_symbol}'"
                )
            if not isinstance(direction, TapeDirection):
                errors.append(f"Invalid tape direction '{direction}'")

        return errors

    @property
    def states(self) -> Set[str]:
        """Ensemble des états de la machine.

        :return: Copie de l'ensemble des états
        """
        return self._states.copy()

    @property
    def alphabet(self) -> Set[str]:
        """Alphabet d'entrée.

        :return: Copie de l'alphabet d'entrée
        """
        return self._alphabet.copy()

    @property
    def tape_alphabet(self) -> Set[str]:
        """Alphabet de la bande.

        :return: Copie de l'alphabet de la bande
        """
        return self._tape_alphabet.copy()

    @property
    def transitions(
        self,
    ) -> Dict[Tuple[str, str], Tuple[str, str, TapeDirection]]:
        """Fonction de transition.

        :return: Copie de la fonction de transition
        """
        return self._transitions.copy()

    @property
    def initial_state(self) -> str:
        """État initial.

        :return: Identifiant de l'état initial
        """
        return self._initial_state

    @property
    def accept_states(self) -> Set[str]:
        """États d'acceptation.

        :return: Copie de l'ensemble des états d'acceptation
        """
        return self._accept_states.copy()

    @property
    def reject_states(self) -> Set[str]:
        """États de rejet.

        :return: Copie de l'ensemble des états de rejet
        """
        return self._reject_states.copy()

    @property
    def blank_symbol(self) -> str:
        """Symbole blanc.

        :return: Symbole blanc utilisé par la machine
        """
        return self._blank_symbol

    @property
    def name(self) -> str:
        """Nom de la machine.

        :return: Nom de la machine
        """
        return self._name

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la machine en dictionnaire.

        :return: Représentation dictionnaire de la machine
        """
        return {
            "type": "TM",
            "name": self._name,
            "states": list(self._states),
            "alphabet": list(self._alphabet),
            "tape_alphabet": list(self._tape_alphabet),
            "transitions": {
                f"{state},{symbol}": [new_state, write_symbol, direction.value]
                for (state, symbol), (
                    new_state,
                    write_symbol,
                    direction,
                ) in self._transitions.items()
            },
            "initial_state": self._initial_state,
            "accept_states": list(self._accept_states),
            "reject_states": list(self._reject_states),
            "blank_symbol": self._blank_symbol,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TM":
        """Crée une machine à partir d'un dictionnaire.

        :param data: Données de la machine
        :return: Instance de TM
        :raises InvalidTMError: Si les données sont invalides
        """
        try:
            transitions = {}
            for key, value in data["transitions"].items():
                state, symbol = key.split(",", 1)
                new_state, write_symbol, direction_str = value
                direction = TapeDirection(direction_str)
                transitions[(state, symbol)] = (
                    new_state,
                    write_symbol,
                    direction,
                )

            return cls(
                states=set(data["states"]),
                alphabet=set(data["alphabet"]),
                tape_alphabet=set(data["tape_alphabet"]),
                transitions=transitions,
                initial_state=data["initial_state"],
                accept_states=set(data["accept_states"]),
                reject_states=set(data["reject_states"]),
                blank_symbol=data["blank_symbol"],
                name=data.get("name"),
            )
        except (KeyError, ValueError, TypeError) as e:
            raise InvalidTMError(f"Invalid TM data: {e}") from e

    def __str__(self) -> str:
        """Représentation textuelle de la machine.

        :return: Représentation textuelle
        """
        return f"TM({self._name}) - States: {len(self._states)}, Transitions: {len(self._transitions)}"

    def __repr__(self) -> str:
        """Représentation technique de la machine.

        :return: Représentation technique
        """
        return (
            f"TM(name='{self._name}', states={len(self._states)}, "
            f"alphabet={len(self._alphabet)}, transitions={len(self._transitions)})"
        )
