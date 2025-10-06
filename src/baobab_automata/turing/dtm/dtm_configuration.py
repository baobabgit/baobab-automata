"""
Configuration d'une machine de Turing déterministe.

Ce module définit la classe DTMConfiguration qui représente l'état
d'une machine de Turing déterministe à un moment donné de son exécution.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DTMConfiguration:
    """Configuration d'une machine de Turing déterministe.

    Une configuration représente l'état complet d'une machine de Turing
    déterministe à un moment donné, incluant l'état actuel, le contenu de la bande,
    la position de la tête de lecture/écriture, le nombre d'étapes effectuées
    et les informations sur l'acceptation/rejet.

    :param state: État actuel de la machine
    :param tape: Contenu actuel de la bande
    :param head_position: Position de la tête de lecture/écriture
    :param step_count: Nombre d'étapes d'exécution effectuées
    :param is_accepting: Indique si la configuration est dans un état d'acceptation
    :param is_rejecting: Indique si la configuration est dans un état de rejet
    """

    state: str
    tape: str
    head_position: int
    step_count: int
    is_accepting: bool = False
    is_rejecting: bool = False

    def __post_init__(self):
        """Validation de la configuration après initialisation.

        :raises ValueError: Si le nombre d'étapes est négatif,
                           ou si la configuration est à la fois acceptante et rejetante
        """
        # Note: head_position peut être négatif pour les machines de Turing
        # car la bande s'étend infiniment dans les deux directions
        if self.step_count < 0:
            raise ValueError("Step count cannot be negative")
        if self.is_accepting and self.is_rejecting:
            raise ValueError("Configuration cannot be both accepting and rejecting")

    def __str__(self) -> str:
        """Représentation textuelle de la configuration.

        :return: Chaîne représentant la configuration
        """
        status = ""
        if self.is_accepting:
            status = " (ACCEPTING)"
        elif self.is_rejecting:
            status = " (REJECTING)"

        return f"({self.state}, {self.tape}, {self.head_position}, {self.step_count}){status}"

    def __repr__(self) -> str:
        """Représentation technique de la configuration.

        :return: Représentation technique complète
        """
        return (
            f"DTMConfiguration(state='{self.state}', tape='{self.tape}', "
            f"head_position={self.head_position}, step_count={self.step_count}, "
            f"is_accepting={self.is_accepting}, is_rejecting={self.is_rejecting})"
        )
