"""
Configuration d'une machine de Turing.

Ce module définit la classe TMConfiguration qui représente l'état
d'une machine de Turing à un moment donné de son exécution.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TMConfiguration:
    """Configuration d'une machine de Turing.

    Une configuration représente l'état complet d'une machine de Turing
    à un moment donné, incluant l'état actuel, le contenu de la bande,
    la position de la tête de lecture/écriture et le nombre d'étapes
    effectuées.

    :param state: État actuel de la machine
    :param tape: Contenu actuel de la bande
    :param head_position: Position de la tête de lecture/écriture
    :param step_count: Nombre d'étapes d'exécution effectuées
    """

    state: str
    tape: str
    head_position: int
    step_count: int

    def __post_init__(self):
        """Validation de la configuration après initialisation.

        :raises ValueError: Si la position de la tête ou le nombre d'étapes est négatif
        """
        if self.head_position < 0:
            raise ValueError("Head position cannot be negative")
        if self.step_count < 0:
            raise ValueError("Step count cannot be negative")

    def __str__(self) -> str:
        """Représentation textuelle de la configuration.

        :return: Chaîne représentant la configuration
        """
        return f"({self.state}, {self.tape}, {self.head_position}, {self.step_count})"

    def __repr__(self) -> str:
        """Représentation technique de la configuration.

        :return: Représentation technique complète
        """
        return (
            f"TMConfiguration(state='{self.state}', tape='{self.tape}', "
            f"head_position={self.head_position}, step_count={self.step_count})"
        )
