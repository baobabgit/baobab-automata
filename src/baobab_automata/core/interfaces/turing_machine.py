"""
Interface abstraite pour les machines de Turing.

Ce module définit l'interface ITuringMachine qui doit être implémentée
par toutes les classes de machines de Turing.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum


class TapeDirection(Enum):
    """Directions de déplacement sur la bande."""

    LEFT = "left"
    RIGHT = "right"
    STAY = "stay"


class TMState(Enum):
    """États possibles d'une machine de Turing."""

    RUNNING = "running"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    HALTED = "halted"


class ITuringMachine(ABC):
    """Interface abstraite pour les machines de Turing.

    Cette interface définit le contrat que doivent respecter toutes
    les implémentations de machines de Turing, qu'elles soient
    déterministes, non-déterministes ou multi-bandes.
    """

    @property
    @abstractmethod
    def states(self) -> Set[str]:
        """Ensemble des états de la machine.

        :return: Ensemble des identifiants d'états
        """

    @property
    @abstractmethod
    def alphabet(self) -> Set[str]:
        """Alphabet d'entrée de la machine.

        :return: Ensemble des symboles d'entrée
        """

    @property
    @abstractmethod
    def tape_alphabet(self) -> Set[str]:
        """Alphabet de la bande (incluant le symbole blanc).

        :return: Ensemble des symboles utilisables sur la bande
        """

    @property
    @abstractmethod
    def transitions(
        self,
    ) -> Dict[Tuple[str, str], Tuple[str, str, TapeDirection]]:
        """Fonction de transition de la machine.

        :return: Dictionnaire des transitions (état, symbole) -> (nouvel_état, symbole_écrit, direction)
        """

    @property
    @abstractmethod
    def initial_state(self) -> str:
        """État initial de la machine.

        :return: Identifiant de l'état initial
        """

    @property
    @abstractmethod
    def accept_states(self) -> Set[str]:
        """États d'acceptation de la machine.

        :return: Ensemble des identifiants d'états d'acceptation
        """

    @property
    @abstractmethod
    def reject_states(self) -> Set[str]:
        """États de rejet de la machine.

        :return: Ensemble des identifiants d'états de rejet
        """

    @abstractmethod
    def simulate(
        self, input_string: str, max_steps: int = 10000
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Simule l'exécution de la machine sur une chaîne d'entrée.

        :param input_string: Chaîne d'entrée à traiter
        :param max_steps: Nombre maximum d'étapes d'exécution
        :return: Tuple (accepté, trace_d_exécution)
        :raises TMSimulationError: En cas d'erreur de simulation
        """

    @abstractmethod
    def step(
        self, current_state: str, tape_symbol: str
    ) -> Optional[Tuple[str, str, TapeDirection]]:
        """Effectue une étape de calcul.

        :param current_state: État actuel de la machine
        :param tape_symbol: Symbole lu sur la bande
        :return: Transition (nouvel_état, symbole_écrit, direction) ou None si pas de transition
        :raises InvalidStateError: Si l'état n'existe pas
        """

    @abstractmethod
    def is_halting_state(self, state: str) -> bool:
        """Vérifie si un état est un état d'arrêt.

        :param state: Identifiant de l'état à vérifier
        :return: True si l'état est un état d'arrêt (acceptation ou rejet)
        """

    @abstractmethod
    def validate(self) -> List[str]:
        """Valide la cohérence de la machine.

        :return: Liste des erreurs de validation (vide si valide)
        """
