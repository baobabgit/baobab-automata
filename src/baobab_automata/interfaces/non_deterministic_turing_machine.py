"""
Interface abstraite pour les machines de Turing non-déterministes.

Ce module définit l'interface INonDeterministicTuringMachine qui doit être
implémentée par toutes les classes de machines de Turing non-déterministes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
from enum import Enum
from .turing_machine import TapeDirection


class NTMState(Enum):
    """États spécifiques aux machines de Turing non-déterministes."""

    RUNNING = "running"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    HALTED = "halted"
    TIMEOUT = "timeout"
    BRANCHING = "branching"


class NTMTransition:
    """Transition non-déterministe avec poids."""

    def __init__(
        self,
        new_state: str,
        write_symbol: str,
        direction: TapeDirection,
        weight: float = 1.0,
    ):
        """Initialise une transition non-déterministe.

        :param new_state: Nouvel état après la transition
        :param write_symbol: Symbole à écrire sur la bande
        :param direction: Direction de déplacement de la tête
        :param weight: Poids de la transition (probabilité relative)
        :raises ValueError: Si le poids n'est pas positif
        """
        if weight <= 0:
            raise ValueError("Transition weight must be positive")

        self.new_state = new_state
        self.write_symbol = write_symbol
        self.direction = direction
        self.weight = weight

    def __str__(self) -> str:
        """Représentation textuelle de la transition.

        :return: Chaîne représentant la transition
        """
        return (
            f"({self.new_state}, {self.write_symbol}, {self.direction.value}, "
            f"{self.weight})"
        )

    def __repr__(self) -> str:
        """Représentation technique de la transition.

        :return: Représentation technique complète
        """
        return (
            f"NTMTransition(new_state='{self.new_state}', "
            f"write_symbol='{self.write_symbol}', direction={self.direction}, "
            f"weight={self.weight})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare deux transitions pour l'égalité.

        :param other: Autre objet à comparer
        :return: True si les transitions sont égales
        """
        if not isinstance(other, NTMTransition):
            return False
        return (
            self.new_state == other.new_state
            and self.write_symbol == other.write_symbol
            and self.direction == other.direction
            and self.weight == other.weight
        )

    def __hash__(self) -> int:
        """Calcule le hash de la transition.

        :return: Hash de la transition
        """
        return hash(
            (self.new_state, self.write_symbol, self.direction, self.weight)
        )


class INonDeterministicTuringMachine(ABC):
    """Interface abstraite pour les machines de Turing non-déterministes.

    Cette interface étend ITuringMachine avec des capacités spécifiques
    au non-déterminisme, incluant la gestion des transitions multiples,
    la simulation parallèle et l'analyse des arbres de calcul.
    """

    @property
    @abstractmethod
    def is_non_deterministic(self) -> bool:
        """Vérifie si la machine est non-déterministe.

        :return: True si la machine présente du non-déterminisme
        """

    @abstractmethod
    def simulate_non_deterministic(
        self,
        input_string: str,
        max_steps: int = 10000,
        max_branches: int = 1000,
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Simule l'exécution non-déterministe de la machine.

        :param input_string: Chaîne d'entrée à traiter
        :param max_steps: Nombre maximum d'étapes par branche
        :param max_branches: Nombre maximum de branches simultanées
        :return: Tuple (accepté, trace_d_exécution)
        :raises NTMSimulationError: En cas d'erreur de simulation
        """

    @abstractmethod
    def get_all_transitions(
        self, current_state: str, tape_symbol: str
    ) -> List[NTMTransition]:
        """Récupère toutes les transitions possibles pour un état et symbole.

        :param current_state: État actuel de la machine
        :param tape_symbol: Symbole lu sur la bande
        :return: Liste des transitions possibles
        :raises InvalidStateError: Si l'état n'existe pas
        """

    @abstractmethod
    def validate_non_determinism(self) -> List[str]:
        """Valide la cohérence non-déterministe de la machine.

        :return: Liste des erreurs de validation
        """

    @abstractmethod
    def analyze_computation_tree(
        self, input_string: str, max_depth: int = 100
    ) -> Dict[str, Any]:
        """Analyse l'arbre de calcul pour une entrée donnée.

        :param input_string: Chaîne d'entrée à analyser
        :param max_depth: Profondeur maximale de l'arbre à explorer
        :return: Analyse détaillée de l'arbre de calcul
        """

    @abstractmethod
    def optimize_parallel_computation(
        self,
    ) -> "INonDeterministicTuringMachine":
        """Optimise les calculs parallèles.

        :return: Nouvelle machine optimisée
        :raises NTMOptimizationError: Si l'optimisation échoue
        """

    @abstractmethod
    def get_transition_probability(
        self,
        current_state: str,
        tape_symbol: str,
        target_state: str,
        write_symbol: str,
        direction: TapeDirection,
    ) -> float:
        """Calcule la probabilité d'une transition spécifique.

        :param current_state: État actuel
        :param tape_symbol: Symbole lu
        :param target_state: État cible
        :param write_symbol: Symbole à écrire
        :param direction: Direction de déplacement
        :return: Probabilité de la transition (0.0 si impossible)
        """
