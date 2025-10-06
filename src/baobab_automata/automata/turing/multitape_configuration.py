"""
Configuration d'une machine de Turing multi-bandes.

Ce module implémente la classe MultiTapeConfiguration qui représente
l'état complet d'une machine de Turing multi-bandes à un moment donné.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MultiTapeConfiguration:
    """Configuration d'une machine de Turing multi-bandes.

    Cette classe représente l'état complet d'une machine de Turing
    multi-bandes à un moment donné, incluant l'état de la machine,
    les contenus de toutes les bandes, les positions des têtes
    et les métadonnées d'exécution.

    :param state: État actuel de la machine
    :param tapes: Contenu de chaque bande
    :param head_positions: Position de la tête sur chaque bande
    :param step_count: Nombre d'étapes effectuées
    :param is_accepting: Indique si la configuration est acceptante
    :param is_rejecting: Indique si la configuration est rejetante
    :raises ValueError: Si la configuration n'est pas valide
    """

    state: str
    tapes: List[str]
    head_positions: List[int]
    step_count: int
    is_accepting: bool = False
    is_rejecting: bool = False

    def __post_init__(self):
        """Validation de la configuration après initialisation.

        :raises ValueError: Si la configuration n'est pas valide
        """
        # Vérifier la cohérence du nombre de bandes et de positions
        if len(self.tapes) != len(self.head_positions):
            raise ValueError(
                f"Number of tapes ({len(self.tapes)}) must match "
                f"number of head positions ({len(self.head_positions)})"
            )

        # Vérifier que les positions ne sont pas négatives
        if any(pos < 0 for pos in self.head_positions):
            raise ValueError("Head positions cannot be negative")

        # Vérifier que le nombre d'étapes n'est pas négatif
        if self.step_count < 0:
            raise ValueError("Step count cannot be negative")

        # Vérifier qu'une configuration ne peut pas être à la fois acceptante et rejetante
        if self.is_accepting and self.is_rejecting:
            raise ValueError("Configuration cannot be both accepting and rejecting")

    @property
    def tape_count(self) -> int:
        """Nombre de bandes dans cette configuration.

        :return: Nombre de bandes
        """
        return len(self.tapes)

    @property
    def is_halting(self) -> bool:
        """Indique si la configuration est un état d'arrêt.

        :return: True si la configuration est acceptante ou rejetante
        """
        return self.is_accepting or self.is_rejecting

    def get_tape_symbol_at_head(self, tape_index: int) -> str:
        """Récupère le symbole sous la tête d'une bande spécifique.

        :param tape_index: Index de la bande
        :return: Symbole sous la tête ou symbole blanc si position invalide
        :raises IndexError: Si l'index de bande est invalide
        """
        if not 0 <= tape_index < len(self.tapes):
            raise IndexError(f"Invalid tape index: {tape_index}")

        tape = self.tapes[tape_index]
        position = self.head_positions[tape_index]

        if 0 <= position < len(tape):
            return tape[position]
        # Position invalide - retourner symbole blanc
        return "B"

    def get_all_tape_symbols_at_heads(self) -> List[str]:
        """Récupère les symboles sous toutes les têtes.

        :return: Liste des symboles sous chaque tête
        """
        return [self.get_tape_symbol_at_head(i) for i in range(len(self.tapes))]

    def to_dict(self) -> dict:
        """Convertit la configuration en dictionnaire.

        :return: Dictionnaire représentant la configuration
        """
        return {
            "state": self.state,
            "tapes": self.tapes.copy(),
            "head_positions": self.head_positions.copy(),
            "step_count": self.step_count,
            "is_accepting": self.is_accepting,
            "is_rejecting": self.is_rejecting,
            "tape_count": self.tape_count,
            "is_halting": self.is_halting,
        }

    def __str__(self) -> str:
        """Représentation textuelle de la configuration."""
        tape_info = ", ".join(
            f"Tape{i}: '{tape}' (head at {pos})"
            for i, (tape, pos) in enumerate(zip(self.tapes, self.head_positions))
        )
        status = (
            "ACCEPTING"
            if self.is_accepting
            else "REJECTING" if self.is_rejecting else "RUNNING"
        )
        return f"MultiTapeConfig(state={self.state}, {tape_info}, step={self.step_count}, status={status})"

    def __repr__(self) -> str:
        """Représentation détaillée de la configuration."""
        return (
            f"MultiTapeConfiguration("
            f"state='{self.state}', "
            f"tapes={self.tapes}, "
            f"head_positions={self.head_positions}, "
            f"step_count={self.step_count}, "
            f"is_accepting={self.is_accepting}, "
            f"is_rejecting={self.is_rejecting})"
        )

