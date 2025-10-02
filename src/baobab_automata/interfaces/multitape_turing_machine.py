"""
Interface abstraite pour les machines de Turing multi-bandes.

Ce module définit l'interface IMultiTapeTuringMachine qui doit être implémentée
par toutes les classes de machines de Turing multi-bandes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Set, Tuple, TYPE_CHECKING
from enum import Enum

from .turing_machine import TapeDirection

if TYPE_CHECKING:
    from .turing_machine import ITuringMachine


class MultiTapeState(Enum):
    """États spécifiques aux machines de Turing multi-bandes."""

    RUNNING = "running"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    HALTED = "halted"
    TIMEOUT = "timeout"
    SYNCHRONIZING = "synchronizing"


class TapeHead:
    """Représentation d'une tête de lecture/écriture."""

    def __init__(self, tape_id: int, position: int = 0):
        """Initialise une tête de lecture/écriture.

        :param tape_id: Identifiant de la bande
        :param position: Position initiale de la tête
        """
        self.tape_id = tape_id
        self.position = position

    def move(self, direction: TapeDirection) -> None:
        """Déplace la tête selon la direction.

        :param direction: Direction de déplacement
        """
        if direction == TapeDirection.LEFT:
            self.position -= 1
        elif direction == TapeDirection.RIGHT:
            self.position += 1
        # STAY ne change pas la position

    def __eq__(self, other):
        """Test d'égalité entre deux têtes."""
        if not isinstance(other, TapeHead):
            return False
        return self.tape_id == other.tape_id and self.position == other.position

    def __hash__(self):
        """Hash de la tête pour utilisation dans des dictionnaires."""
        return hash((self.tape_id, self.position))

    def __repr__(self):
        """Représentation textuelle de la tête."""
        return f"TapeHead(tape_id={self.tape_id}, position={self.position})"


class IMultiTapeTuringMachine(ABC):
    """Interface abstraite pour les machines de Turing multi-bandes.

    Cette interface étend ITuringMachine avec des capacités spécifiques
    aux machines multi-bandes, incluant la gestion de plusieurs bandes,
    la synchronisation des têtes et les optimisations d'accès.
    """

    @property
    @abstractmethod
    def tape_count(self) -> int:
        """Nombre de bandes.

        :return: Nombre de bandes de la machine
        """

    @property
    @abstractmethod
    def tape_alphabets(self) -> List[Set[str]]:
        """Alphabets de chaque bande.

        :return: Liste des alphabets pour chaque bande
        """

    @abstractmethod
    def simulate_multi_tape(
        self, input_strings: List[str], max_steps: int = 10000
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Simule l'exécution multi-bande de la machine.

        :param input_strings: Chaînes d'entrée pour chaque bande
        :param max_steps: Nombre maximum d'étapes
        :return: Tuple (accepté, trace_d_exécution)
        :raises MultiTapeTMSimulationError: En cas d'erreur de simulation
        """

    @abstractmethod
    def get_tape_symbols(
        self, tape_configurations: List[str], head_positions: List[int]
    ) -> List[str]:
        """Récupère les symboles sous toutes les têtes.

        :param tape_configurations: Configurations des bandes
        :param head_positions: Positions des têtes
        :return: Liste des symboles sous chaque tête
        """

    @abstractmethod
    def synchronize_heads(self, heads: List[TapeHead]) -> List[TapeHead]:
        """Synchronise les positions des têtes.

        :param heads: Liste des têtes à synchroniser
        :return: Liste des têtes synchronisées
        """

    @abstractmethod
    def validate_multi_tape_consistency(self) -> List[str]:
        """Valide la cohérence multi-bande de la machine.

        :return: Liste des erreurs de validation
        """

    @abstractmethod
    def convert_to_single_tape(self) -> "ITuringMachine":
        """Convertit la machine multi-bande en machine à bande unique.

        :return: Machine de Turing à bande unique équivalente
        :raises MultiTapeTMConversionError: Si la conversion échoue
        """

    @abstractmethod
    def optimize_tape_access(self) -> "IMultiTapeTuringMachine":
        """Optimise l'accès aux bandes.

        :return: Nouvelle MultiTapeTM optimisée
        :raises MultiTapeTMOptimizationError: Si l'optimisation échoue
        """
