"""
Configuration des automates à pile déterministes (DPDA).

Ce module définit la classe DPDAConfiguration pour représenter
les configurations d'un DPDA lors de la simulation.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class DPDAConfiguration:
    """Configuration d'un DPDA (état, mot restant, pile).

    Une configuration représente l'état complet d'un DPDA à un moment
    donné de la simulation, incluant l'état courant, le mot d'entrée
    restant et l'état de la pile.

    :param state: État courant de l'automate
    :param remaining_input: Mot d'entrée restant à traiter
    :param stack: État de la pile (chaîne avec le sommet à gauche)
    """

    state: str
    remaining_input: str
    stack: str

    def __post_init__(self) -> None:
        """Valide la configuration après initialisation.

        :raises ValueError: Si la configuration est invalide
        """
        if not isinstance(self.state, str) or not self.state:
            raise ValueError("L'état doit être une chaîne non vide")

        if not isinstance(self.remaining_input, str):
            raise ValueError("Le mot restant doit être une chaîne")

        if not isinstance(self.stack, str):
            raise ValueError("La pile doit être une chaîne")

    @property
    def is_accepting(self) -> bool:
        """Vérifie si la configuration est dans un état acceptant.

        Une configuration est acceptante si le mot d'entrée est vide
        et que la pile ne contient que le symbole de fond.

        :return: True si la configuration est acceptante, False sinon
        """
        return self.remaining_input == ""

    @property
    def stack_top(self) -> Optional[str]:
        """Retourne le symbole au sommet de la pile.

        :return: Symbole au sommet de la pile ou None si la pile est vide
        """
        return self.stack[0] if self.stack else None

    @property
    def stack_bottom(self) -> Optional[str]:
        """Retourne le symbole au fond de la pile.

        :return: Symbole au fond de la pile ou None si la pile est vide
        """
        return self.stack[-1] if self.stack else None

    @property
    def stack_height(self) -> int:
        """Retourne la hauteur de la pile.

        :return: Nombre de symboles dans la pile
        """
        return len(self.stack)

    @property
    def is_empty_stack(self) -> bool:
        """Vérifie si la pile est vide.

        :return: True si la pile est vide, False sinon
        """
        return self.stack == ""

    def push_symbols(self, symbols: str) -> "DPDAConfiguration":
        """Crée une nouvelle configuration avec des symboles ajoutés à la pile.

        :param symbols: Symboles à ajouter au sommet de la pile
        :return: Nouvelle configuration avec les symboles ajoutés
        :raises ValueError: Si les symboles sont invalides
        """
        if not isinstance(symbols, str):
            raise ValueError("Les symboles doivent être une chaîne")

        new_stack = symbols + self.stack
        return DPDAConfiguration(
            state=self.state, remaining_input=self.remaining_input, stack=new_stack
        )

    def pop_symbols(self, count: int = 1) -> "DPDAConfiguration":
        """Crée une nouvelle configuration avec des symboles retirés de la pile.

        :param count: Nombre de symboles à retirer du sommet
        :return: Nouvelle configuration avec les symboles retirés
        :raises ValueError: Si le nombre de symboles est invalide
        :raises IndexError: Si on essaie de retirer plus de symboles qu'il n'y en a
        """
        if not isinstance(count, int) or count < 0:
            raise ValueError("Le nombre de symboles doit être un entier positif")

        if count > len(self.stack):
            raise IndexError(
                "Tentative de retirer plus de symboles qu'il n'y en a dans la pile"
            )

        new_stack = self.stack[count:]
        return DPDAConfiguration(
            state=self.state, remaining_input=self.remaining_input, stack=new_stack
        )

    def replace_stack_top(self, new_symbols: str) -> "DPDAConfiguration":
        """Crée une nouvelle configuration en remplaçant le sommet de la pile.

        :param new_symbols: Nouveaux symboles pour remplacer le sommet
        :return: Nouvelle configuration avec le sommet remplacé
        :raises ValueError: Si les nouveaux symboles sont invalides
        :raises IndexError: Si la pile est vide
        """
        if not isinstance(new_symbols, str):
            raise ValueError("Les nouveaux symboles doivent être une chaîne")

        if not self.stack:
            raise IndexError("Impossible de remplacer le sommet d'une pile vide")

        new_stack = new_symbols + self.stack[1:]
        return DPDAConfiguration(
            state=self.state, remaining_input=self.remaining_input, stack=new_stack
        )

    def consume_input(self, count: int = 1) -> "DPDAConfiguration":
        """Crée une nouvelle configuration en consommant des symboles d'entrée.

        :param count: Nombre de symboles d'entrée à consommer
        :return: Nouvelle configuration avec les symboles consommés
        :raises ValueError: Si le nombre de symboles est invalide
        :raises IndexError: Si on essaie de consommer plus de symboles qu'il n'y en a
        """
        if not isinstance(count, int) or count < 0:
            raise ValueError("Le nombre de symboles doit être un entier positif")

        if count > len(self.remaining_input):
            raise IndexError(
                "Tentative de consommer plus de symboles qu'il n'y en a dans le mot"
            )

        new_input = self.remaining_input[count:]
        return DPDAConfiguration(
            state=self.state, remaining_input=new_input, stack=self.stack
        )

    def change_state(self, new_state: str) -> "DPDAConfiguration":
        """Crée une nouvelle configuration avec un nouvel état.

        :param new_state: Nouvel état de l'automate
        :return: Nouvelle configuration avec le nouvel état
        :raises ValueError: Si le nouvel état est invalide
        """
        if not isinstance(new_state, str) or not new_state:
            raise ValueError("Le nouvel état doit être une chaîne non vide")

        return DPDAConfiguration(
            state=new_state, remaining_input=self.remaining_input, stack=self.stack
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la configuration en dictionnaire.

        :return: Représentation dictionnaire de la configuration
        """
        return {
            "state": self.state,
            "remaining_input": self.remaining_input,
            "stack": self.stack,
            "stack_height": self.stack_height,
            "is_accepting": self.is_accepting,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DPDAConfiguration":
        """Crée une configuration à partir d'un dictionnaire.

        :param data: Données de la configuration
        :return: Instance de DPDAConfiguration
        :raises ValueError: Si les données sont invalides
        """
        required_fields = {"state", "remaining_input", "stack"}
        if not all(field in data for field in required_fields):
            missing = required_fields - set(data.keys())
            raise ValueError(f"Champs manquants: {missing}")

        return cls(
            state=data["state"],
            remaining_input=data["remaining_input"],
            stack=data["stack"],
        )

    def __str__(self) -> str:
        """Retourne la représentation string de la configuration.

        :return: Représentation string de la configuration
        """
        return f"({self.state}, '{self.remaining_input}', '{self.stack}')"

    def __repr__(self) -> str:
        """Retourne la représentation détaillée de la configuration.

        :return: Représentation détaillée de la configuration
        """
        return (
            f"DPDAConfiguration(state='{self.state}', "
            f"remaining_input='{self.remaining_input}', "
            f"stack='{self.stack}')"
        )
