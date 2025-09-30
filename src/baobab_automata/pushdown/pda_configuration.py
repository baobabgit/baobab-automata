"""
Configuration d'un automate à pile non-déterministe (PDA).

Ce module définit la classe PDAConfiguration qui représente
l'état d'un PDA à un moment donné de la simulation.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class PDAConfiguration:
    """Configuration d'un PDA (état, mot restant, pile).

    Une configuration représente l'état complet d'un PDA à un moment donné :
    - L'état actuel de l'automate
    - Le mot d'entrée restant à traiter
    - L'état de la pile (représenté comme une chaîne de caractères)

    La classe est immuable (frozen=True) pour garantir la cohérence
    et permettre l'utilisation dans des structures de données comme les sets.
    """

    state: str
    """État actuel de l'automate."""

    remaining_input: str
    """Mot d'entrée restant à traiter."""

    stack: str
    """État de la pile (chaîne de caractères avec le sommet à droite)."""

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
    def is_empty_stack(self) -> bool:
        """Vérifie si la pile est vide.

        :return: True si la pile est vide, False sinon
        """
        return not self.stack

    @property
    def stack_top(self) -> Optional[str]:
        """Récupère le symbole au sommet de la pile.

        :return: Le symbole au sommet de la pile, ou None si la pile est vide
        """
        if self.is_empty_stack:
            return None
        return self.stack[0]  # Le sommet est à gauche, pas à droite

    def push_symbols(self, symbols: str) -> "PDAConfiguration":
        """Crée une nouvelle configuration avec des symboles ajoutés à la pile.

        :param symbols: Symboles à ajouter à la pile (ajoutés au sommet)
        :return: Nouvelle configuration avec les symboles ajoutés
        :raises ValueError: Si les symboles ne sont pas une chaîne
        """
        if not isinstance(symbols, str):
            raise ValueError("Les symboles doivent être une chaîne")

        return PDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input,
            stack=symbols + self.stack,  # Ajouter au début (sommet)
        )

    def pop_symbol(self) -> "PDAConfiguration":
        """Crée une nouvelle configuration avec le symbole du sommet retiré.

        :return: Nouvelle configuration avec le symbole du sommet retiré
        :raises ValueError: Si la pile est vide
        """
        if self.is_empty_stack:
            raise ValueError("Impossible de retirer un symbole d'une pile vide")

        return PDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input,
            stack=self.stack[1:],  # Retirer le premier caractère (sommet)
        )

    def replace_stack_top(self, new_symbols: str) -> "PDAConfiguration":
        """Crée une nouvelle configuration avec le sommet de la pile remplacé.

        :param new_symbols: Nouveaux symboles pour remplacer le sommet
        :return: Nouvelle configuration avec le sommet remplacé
        :raises ValueError: Si la pile est vide ou si les symboles ne sont pas une chaîne
        """
        if not isinstance(new_symbols, str):
            raise ValueError("Les nouveaux symboles doivent être une chaîne")

        if self.is_empty_stack:
            raise ValueError("Impossible de remplacer le sommet d'une pile vide")

        return PDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input,
            stack=new_symbols + self.stack[1:],  # Remplacer le premier caractère
        )

    def consume_input(self, symbol: str) -> "PDAConfiguration":
        """Crée une nouvelle configuration avec un symbole d'entrée consommé.

        :param symbol: Symbole d'entrée à consommer
        :return: Nouvelle configuration avec le symbole consommé
        :raises ValueError: Si le symbole ne correspond pas au début du mot restant
        """
        if not isinstance(symbol, str):
            raise ValueError("Le symbole doit être une chaîne")

        if not self.remaining_input.startswith(symbol):
            raise ValueError(
                f"Le symbole '{symbol}' ne correspond pas au début du mot restant '{self.remaining_input}'"
            )

        return PDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input[len(symbol) :],
            stack=self.stack,
        )

    def change_state(self, new_state: str) -> "PDAConfiguration":
        """Crée une nouvelle configuration avec un nouvel état.

        :param new_state: Nouvel état de l'automate
        :return: Nouvelle configuration avec le nouvel état
        :raises ValueError: Si le nouvel état n'est pas une chaîne valide
        """
        if not isinstance(new_state, str) or not new_state:
            raise ValueError("Le nouvel état doit être une chaîne non vide")

        return PDAConfiguration(
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
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PDAConfiguration":
        """Crée une configuration à partir d'un dictionnaire.

        :param data: Données de la configuration
        :return: Instance de PDAConfiguration
        :raises ValueError: Si les données sont invalides
        """
        try:
            return cls(
                state=data["state"],
                remaining_input=data["remaining_input"],
                stack=data["stack"],
            )
        except KeyError as e:
            raise ValueError(
                f"Données de configuration incomplètes: clé manquante '{e}'"
            )
        except Exception as e:
            raise ValueError(f"Données de configuration invalides: {e}")

    def __str__(self) -> str:
        """Retourne la représentation textuelle de la configuration.

        :return: Représentation textuelle formatée
        """
        return f"({self.state}, {self.remaining_input}, {self.stack})"

    def __repr__(self) -> str:
        """Retourne la représentation technique de la configuration.

        :return: Représentation technique pour le débogage
        """
        return f"PDAConfiguration(state='{self.state}', remaining_input='{self.remaining_input}', stack='{self.stack}')"
