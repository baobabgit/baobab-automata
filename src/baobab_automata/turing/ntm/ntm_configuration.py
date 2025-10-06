"""
Configuration d'une machine de Turing non-déterministe.

Ce module définit la classe NTMConfiguration qui représente l'état
d'une machine de Turing non-déterministe à un moment donné de son exécution.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class NTMConfiguration:
    """Configuration d'une machine de Turing non-déterministe.

    Une configuration représente l'état complet d'une machine de Turing
    non-déterministe à un moment donné, incluant l'état actuel, le contenu
    de la bande, la position de la tête de lecture/écriture, le nombre
    d'étapes effectuées, et des informations spécifiques au
    non-déterminisme comme l'identifiant de branche et le poids de la
    configuration.

    :param state: État actuel de la machine
    :param tape: Contenu actuel de la bande
    :param head_position: Position de la tête de lecture/écriture
    :param step_count: Nombre d'étapes d'exécution effectuées
    :param branch_id: Identifiant unique de la branche de calcul
    :param is_accepting: Indique si cette configuration est dans un état
        d'acceptation
    :param is_rejecting: Indique si cette configuration est dans un état de
        rejet
    :param weight: Poids probabiliste de cette configuration
    """

    state: str
    tape: str
    head_position: int
    step_count: int
    branch_id: int = 0
    is_accepting: bool = False
    is_rejecting: bool = False
    weight: float = 1.0

    def __post_init__(self):
        """Validation de la configuration après initialisation.

        :raises ValueError: Si les paramètres ne respectent pas les contraintes
        """
        if self.head_position < 0:
            raise ValueError("Head position cannot be negative")
        if self.step_count < 0:
            raise ValueError("Step count cannot be negative")
        if self.weight <= 0:
            raise ValueError("Weight must be positive")
        if self.is_accepting and self.is_rejecting:
            raise ValueError(
                "Configuration cannot be both accepting and rejecting"
            )

    def __str__(self) -> str:
        """Représentation textuelle de la configuration.

        :return: Chaîne représentant la configuration
        """
        status = ""
        if self.is_accepting:
            status = " [ACCEPT]"
        elif self.is_rejecting:
            status = " [REJECT]"

        return (
            f"({self.state}, {self.tape}, {self.head_position}, "
            f"{self.step_count}, branch={self.branch_id}, "
            f"weight={self.weight:.3f}){status}"
        )

    def __repr__(self) -> str:
        """Représentation technique de la configuration.

        :return: Représentation technique complète
        """
        return (
            f"NTMConfiguration(state='{self.state}', tape='{self.tape}', "
            f"head_position={self.head_position}, "
            f"step_count={self.step_count}, "
            f"branch_id={self.branch_id}, "
            f"is_accepting={self.is_accepting}, "
            f"is_rejecting={self.is_rejecting}, weight={self.weight})"
        )

    def is_halting(self) -> bool:
        """Vérifie si la configuration est dans un état d'arrêt.

        :return: True si la configuration est dans un état d'arrêt
        """
        return self.is_accepting or self.is_rejecting

    def get_tape_symbol_at_head(self) -> str:
        """Récupère le symbole à la position de la tête.

        :return: Symbole à la position de la tête
        """
        if 0 <= self.head_position < len(self.tape):
            return self.tape[self.head_position]
        return "B"  # Symbole blanc par défaut

    def get_configuration_key(self) -> tuple:
        """Génère une clé unique pour cette configuration.

        Cette clé est utilisée pour détecter les boucles infinies
        dans la simulation non-déterministe.

        :return: Tuple représentant la clé de configuration
        """
        return (self.state, self.tape, self.head_position)
