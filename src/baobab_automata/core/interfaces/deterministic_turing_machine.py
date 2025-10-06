"""
Interface abstraite pour les machines de Turing déterministes.

Ce module définit l'interface IDeterministicTuringMachine qui doit être
implémentée par toutes les classes de machines de Turing déterministes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum

from .turing_machine import TapeDirection


class DTMState(Enum):
    """États spécifiques aux machines de Turing déterministes."""

    RUNNING = "running"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    HALTED = "halted"
    TIMEOUT = "timeout"


class IDeterministicTuringMachine(ABC):
    """Interface abstraite pour les machines de Turing déterministes.

    Cette interface étend ITuringMachine avec des méthodes spécifiques
    au déterminisme et aux optimisations de performance.
    """

    @property
    @abstractmethod
    def is_deterministic(self) -> bool:
        """Vérifie si la machine est déterministe.

        :return: True si la machine est déterministe, False sinon
        """
        pass

    @abstractmethod
    def simulate_deterministic(
        self, input_string: str, max_steps: int = 10000
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Simule l'exécution déterministe de la machine.

        :param input_string: Chaîne d'entrée à traiter
        :param max_steps: Nombre maximum d'étapes d'exécution
        :return: Tuple (accepté, trace_d_exécution)
        :raises DTMSimulationError: En cas d'erreur de simulation
        """
        pass

    @abstractmethod
    def get_next_configuration(
        self, current_state: str, tape_symbol: str
    ) -> Optional[Tuple[str, str, TapeDirection]]:
        """Récupère la prochaine configuration de manière déterministe.

        :param current_state: État actuel de la machine
        :param tape_symbol: Symbole lu sur la bande
        :return: Transition (nouvel_état, symbole_écrit, direction) ou None
        :raises InvalidStateError: Si l'état n'existe pas
        """
        pass

    @abstractmethod
    def validate_determinism(self) -> List[str]:
        """Valide le déterminisme de la machine.

        :return: Liste des erreurs de déterminisme (vide si déterministe)
        """
        pass

    @abstractmethod
    def optimize_transitions(self) -> "IDeterministicTuringMachine":
        """Optimise les transitions pour améliorer les performances.

        :return: Nouvelle machine de Turing déterministe optimisée
        :raises DTMOptimizationError: Si l'optimisation échoue
        """
        pass
