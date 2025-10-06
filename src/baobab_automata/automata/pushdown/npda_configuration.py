"""
Configuration pour les automates à pile non-déterministes (NPDA).

Ce module définit la classe NPDAConfiguration pour représenter
les configurations d'un NPDA avec support des capacités parallèles.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True, order=True)
class NPDAConfiguration:
    """Configuration d'un NPDA (état, mot restant, pile, priorité).

    Cette classe représente une configuration d'un automate à pile
    non-déterministe avec des informations supplémentaires pour
    la gestion des calculs parallèles.

    Attributes:
        state: État actuel de l'automate
        remaining_input: Mot restant à traiter
        stack: Représentation de la pile comme une chaîne (sommet à gauche)
        priority: Priorité pour l'ordre de traitement (plus élevé = plus prioritaire)
        branch_id: Identifiant unique de la branche de calcul
        depth: Profondeur de la configuration dans l'arbre de calcul
        parent_id: Identifiant de la configuration parente (pour le suivi)
    """

    state: str
    remaining_input: str
    stack: str  # Représentation de la pile comme une chaîne
    priority: int = 0  # Priorité pour l'ordre de traitement
    branch_id: int = 0  # Identifiant de la branche
    depth: int = 0  # Profondeur dans l'arbre de calcul
    parent_id: Optional[int] = None  # ID de la configuration parente

    def __post_init__(self) -> None:
        """Valide la configuration après initialisation.

        :raises ValueError: Si la configuration est invalide
        """
        if not self.state:
            raise ValueError("L'état ne peut pas être vide")
        if not isinstance(self.remaining_input, str):
            raise ValueError("Le mot restant doit être une chaîne")
        if not isinstance(self.stack, str):
            raise ValueError("La pile doit être une chaîne")
        if self.priority < 0:
            raise ValueError("La priorité ne peut pas être négative")
        if self.branch_id < 0:
            raise ValueError("L'ID de branche ne peut pas être négatif")
        if self.depth < 0:
            raise ValueError("La profondeur ne peut pas être négative")

    @property
    def is_accepting(self) -> bool:
        """Vérifie si la configuration est acceptante.

        Une configuration est acceptante si :
        - Le mot restant est vide

        :return: True si la configuration est acceptante, False sinon
        """
        return self.remaining_input == ""

    @property
    def is_final(self) -> bool:
        """Vérifie si la configuration est finale.

        Une configuration est finale si le mot restant est vide.

        :return: True si la configuration est finale, False sinon
        """
        return self.remaining_input == ""

    @property
    def stack_top(self) -> str:
        """Retourne le symbole au sommet de la pile.

        :return: Symbole au sommet de la pile ou chaîne vide si la pile est vide
        """
        return self.stack[0] if self.stack else ""

    @property
    def stack_bottom(self) -> str:
        """Retourne le symbole au fond de la pile.

        :return: Symbole au fond de la pile ou chaîne vide si la pile est vide
        """
        return self.stack[-1] if self.stack else ""

    @property
    def stack_size(self) -> int:
        """Retourne la taille de la pile.

        :return: Nombre de symboles dans la pile
        """
        return len(self.stack)

    @property
    def input_length(self) -> int:
        """Retourne la longueur du mot restant.

        :return: Nombre de caractères restants à traiter
        """
        return len(self.remaining_input)

    def push_symbol(self, symbol: str) -> "NPDAConfiguration":
        """Crée une nouvelle configuration avec un symbole empilé.

        :param symbol: Symbole à empiler
        :return: Nouvelle configuration avec le symbole empilé
        :raises ValueError: Si le symbole est vide
        """
        if not symbol:
            raise ValueError("Le symbole à empiler ne peut pas être vide")

        return NPDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input,
            stack=symbol + self.stack,  # Empilage au début (sommet à gauche)
            priority=self.priority,
            branch_id=self.branch_id,
            depth=self.depth + 1,
            parent_id=self.branch_id,
        )

    def push_symbols(self, symbols: str) -> "NPDAConfiguration":
        """Crée une nouvelle configuration avec plusieurs symboles empilés.

        :param symbols: Chaîne de symboles à empiler
        :return: Nouvelle configuration avec les symboles empilés
        :raises ValueError: Si la chaîne de symboles est vide
        """
        if not symbols:
            raise ValueError("La chaîne de symboles ne peut pas être vide")

        return NPDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input,
            stack=symbols + self.stack,  # Empilage au début (sommet à gauche)
            priority=self.priority,
            branch_id=self.branch_id,
            depth=self.depth + 1,
            parent_id=self.branch_id,
        )

    def pop_symbol(self) -> "NPDAConfiguration":
        """Crée une nouvelle configuration avec un symbole dépilé.

        :return: Nouvelle configuration avec le symbole dépilé
        :raises ValueError: Si la pile est vide
        """
        if not self.stack:
            raise ValueError("Impossible de dépiler : la pile est vide")

        return NPDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input,
            stack=self.stack[1:],  # Dépilage du premier caractère
            priority=self.priority,
            branch_id=self.branch_id,
            depth=self.depth + 1,
            parent_id=self.branch_id,
        )

    def consume_input(self, length: int = 1) -> "NPDAConfiguration":
        """Crée une nouvelle configuration avec des caractères d'entrée consommés.

        :param length: Nombre de caractères à consommer
        :return: Nouvelle configuration avec les caractères consommés
        :raises ValueError: Si la longueur est invalide
        """
        if length < 0:
            raise ValueError("La longueur ne peut pas être négative")
        if length > len(self.remaining_input):
            raise ValueError(
                "Impossible de consommer plus de caractères que disponibles"
            )

        return NPDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input[length:],
            stack=self.stack,
            priority=self.priority,
            branch_id=self.branch_id,
            depth=self.depth + 1,
            parent_id=self.branch_id,
        )

    def change_state(self, new_state: str) -> "NPDAConfiguration":
        """Crée une nouvelle configuration avec un nouvel état.

        :param new_state: Nouvel état
        :return: Nouvelle configuration avec le nouvel état
        :raises ValueError: Si le nouvel état est vide
        """
        if not new_state:
            raise ValueError("Le nouvel état ne peut pas être vide")

        return NPDAConfiguration(
            state=new_state,
            remaining_input=self.remaining_input,
            stack=self.stack,
            priority=self.priority,
            branch_id=self.branch_id,
            depth=self.depth + 1,
            parent_id=self.branch_id,
        )

    def with_priority(self, new_priority: int) -> "NPDAConfiguration":
        """Crée une nouvelle configuration avec une nouvelle priorité.

        :param new_priority: Nouvelle priorité
        :return: Nouvelle configuration avec la nouvelle priorité
        :raises ValueError: Si la priorité est négative
        """
        if new_priority < 0:
            raise ValueError("La priorité ne peut pas être négative")

        return NPDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input,
            stack=self.stack,
            priority=new_priority,
            branch_id=self.branch_id,
            depth=self.depth,
            parent_id=self.parent_id,
        )

    def with_branch_id(self, new_branch_id: int) -> "NPDAConfiguration":
        """Crée une nouvelle configuration avec un nouvel ID de branche.

        :param new_branch_id: Nouvel ID de branche
        :return: Nouvelle configuration avec le nouvel ID de branche
        :raises ValueError: Si l'ID de branche est négatif
        """
        if new_branch_id < 0:
            raise ValueError("L'ID de branche ne peut pas être négatif")

        return NPDAConfiguration(
            state=self.state,
            remaining_input=self.remaining_input,
            stack=self.stack,
            priority=self.priority,
            branch_id=new_branch_id,
            depth=self.depth,
            parent_id=self.parent_id,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la configuration en dictionnaire.

        :return: Dictionnaire représentant la configuration
        """
        return {
            "state": self.state,
            "remaining_input": self.remaining_input,
            "stack": self.stack,
            "priority": self.priority,
            "branch_id": self.branch_id,
            "depth": self.depth,
            "parent_id": self.parent_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NPDAConfiguration":
        """Crée une configuration à partir d'un dictionnaire.

        :param data: Dictionnaire contenant les données de la configuration
        :return: Instance de NPDAConfiguration
        :raises ValueError: Si les données sont invalides
        """
        try:
            return cls(
                state=data["state"],
                remaining_input=data["remaining_input"],
                stack=data["stack"],
                priority=data.get("priority", 0),
                branch_id=data.get("branch_id", 0),
                depth=data.get("depth", 0),
                parent_id=data.get("parent_id"),
            )
        except KeyError as e:
            raise ValueError(f"Données de configuration invalides : clé manquante {e}")

    def __str__(self) -> str:
        """Retourne la représentation string de la configuration.

        :return: Représentation string de la configuration
        """
        return (
            f"NPDAConfiguration(state='{self.state}', "
            f"remaining_input='{self.remaining_input}', "
            f"stack='{self.stack}', "
            f"priority={self.priority}, "
            f"branch_id={self.branch_id}, "
            f"depth={self.depth})"
        )

    def __repr__(self) -> str:
        """Retourne la représentation détaillée de la configuration.

        :return: Représentation détaillée de la configuration
        """
        return self.__str__()
