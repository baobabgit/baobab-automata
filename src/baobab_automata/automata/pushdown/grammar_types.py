"""
Types et structures de données pour les grammaires hors-contexte.

Ce module définit les classes de base pour représenter les grammaires
hors-contexte (CFG) et leurs composants.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Set, Tuple


class GrammarType(Enum):
    """Types de grammaires supportés."""

    GENERAL = "general"
    CHOMSKY_NORMAL_FORM = "chomsky_normal_form"
    GREIBACH_NORMAL_FORM = "greibach_normal_form"
    LEFT_RECURSIVE = "left_recursive"
    RIGHT_RECURSIVE = "right_recursive"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class Production:
    """Représente une production d'une grammaire.

    Une production est une règle de réécriture de la forme A -> α où A est une
    variable (symbole non-terminal) et α est une séquence de symboles (terminaux
    et non-terminaux).

    Attributes:
        left_side: Variable de gauche (symbole non-terminal)
        right_side: Séquence de symboles de droite (terminaux et non-terminaux)

    Example:
        Production('S', ['a', 'S', 'b'])  # S -> aSb
        Production('A', [])               # A -> ε (production vide)
    """

    left_side: str
    right_side: Tuple[str, ...]

    def __post_init__(self) -> None:
        """Validation post-initialisation."""
        if not self.left_side:
            raise ValueError("La variable de gauche ne peut pas être vide")

        if not isinstance(self.right_side, tuple):
            raise ValueError("Le côté droit doit être un tuple")

        for symbol in self.right_side:
            if not isinstance(symbol, str):
                raise ValueError("Tous les symboles doivent être des chaînes")

    def is_empty(self) -> bool:
        """Vérifie si la production est vide (epsilon).

        :return: True si la production est vide
        """
        return len(self.right_side) == 0

    def is_terminal(self) -> bool:
        """Vérifie si la production génère uniquement des terminaux.

        :return: True si la production génère uniquement des terminaux
        """
        return len(self.right_side) == 1 and self.right_side[0] != self.left_side

    def is_unit(self) -> bool:
        """Vérifie si la production est unitaire (A -> B).

        :return: True si la production est unitaire
        """
        return (
            len(self.right_side) == 1
            and self.right_side[0] != self.left_side
            and self.right_side[0].isupper()
        )

    def is_binary(self) -> bool:
        """Vérifie si la production est binaire (A -> BC).

        :return: True si la production est binaire
        """
        return len(self.right_side) == 2

    def __str__(self) -> str:
        """Représentation textuelle de la production."""
        if not self.right_side:
            return f"{self.left_side} -> ε"
        return f"{self.left_side} -> {' '.join(self.right_side)}"

    def __repr__(self) -> str:
        """Représentation détaillée de la production."""
        return f"Production('{self.left_side}', {self.right_side})"


@dataclass(frozen=True)
class ContextFreeGrammar:
    """Représente une grammaire hors-contexte.

    Une grammaire hors-contexte (CFG) est définie par un quadruplet (V, T, P, S) où :
    - V est l'ensemble des variables (symboles non-terminaux)
    - T est l'ensemble des terminaux
    - P est l'ensemble des productions (règles de réécriture)
    - S est le symbole de départ

    Attributes:
        variables: Symboles non-terminaux
        terminals: Symboles terminaux
        productions: Règles de production
        start_symbol: Symbole de départ
        name: Nom optionnel de la grammaire

    Example:
        grammar = ContextFreeGrammar(
            variables={'S', 'A', 'B'},
            terminals={'a', 'b'},
            productions={
                Production('S', ['a', 'S', 'b']),
                Production('S', []),
                Production('A', ['a', 'A']),
                Production('A', ['b'])
            },
            start_symbol='S',
            name='anbn'
        )
    """

    variables: Set[str]
    terminals: Set[str]
    productions: Set[Production]
    start_symbol: str
    name: Optional[str] = None

    def __post_init__(self) -> None:
        """Validation post-initialisation."""
        if not self.variables:
            raise ValueError("L'ensemble des variables ne peut pas être vide")

        if not self.productions:
            raise ValueError("L'ensemble des productions ne peut pas être vide")

        if not self.start_symbol:
            raise ValueError("Le symbole de départ ne peut pas être vide")

        if self.start_symbol not in self.variables:
            raise ValueError("Le symbole de départ doit être une variable")

        # Vérification de la cohérence des productions
        for production in self.productions:
            if production.left_side not in self.variables:
                raise ValueError(f"Variable '{production.left_side}' non définie")

            for symbol in production.right_side:
                if symbol not in self.variables and symbol not in self.terminals:
                    raise ValueError(f"Symbole '{symbol}' non défini")

    def get_productions_for(self, variable: str) -> Set[Production]:
        """Obtient toutes les productions pour une variable donnée.

        :param variable: Variable pour laquelle récupérer les productions
        :return: Ensemble des productions pour la variable
        :raises ValueError: Si la variable n'existe pas
        """
        if variable not in self.variables:
            raise ValueError(f"Variable '{variable}' non définie")

        return {p for p in self.productions if p.left_side == variable}

    def get_empty_productions(self) -> Set[Production]:
        """Obtient toutes les productions vides.

        :return: Ensemble des productions vides
        """
        return {p for p in self.productions if p.is_empty()}

    def get_unit_productions(self) -> Set[Production]:
        """Obtient toutes les productions unitaires.

        :return: Ensemble des productions unitaires
        """
        return {p for p in self.productions if p.is_unit()}

    def get_binary_productions(self) -> Set[Production]:
        """Obtient toutes les productions binaires.

        :return: Ensemble des productions binaires
        """
        return {p for p in self.productions if p.is_binary()}

    def has_empty_productions(self) -> bool:
        """Vérifie si la grammaire a des productions vides.

        :return: True si la grammaire a des productions vides
        """
        return len(self.get_empty_productions()) > 0

    def has_unit_productions(self) -> bool:
        """Vérifie si la grammaire a des productions unitaires.

        :return: True si la grammaire a des productions unitaires
        """
        return len(self.get_unit_productions()) > 0

    def has_binary_productions(self) -> bool:
        """Vérifie si la grammaire a des productions binaires.

        :return: True si la grammaire a des productions binaires
        """
        return len(self.get_binary_productions()) > 0

    def get_variables_used_in_productions(self) -> Set[str]:
        """Obtient toutes les variables utilisées dans les productions.

        :return: Ensemble des variables utilisées
        """
        used_variables = set()
        for production in self.productions:
            used_variables.add(production.left_side)
            for symbol in production.right_side:
                if symbol in self.variables:
                    used_variables.add(symbol)
        return used_variables

    def get_terminals_used_in_productions(self) -> Set[str]:
        """Obtient tous les terminaux utilisés dans les productions.

        :return: Ensemble des terminaux utilisés
        """
        used_terminals = set()
        for production in self.productions:
            for symbol in production.right_side:
                if symbol in self.terminals:
                    used_terminals.add(symbol)
        return used_terminals

    def __str__(self) -> str:
        """Représentation textuelle de la grammaire."""
        lines = []
        if self.name:
            lines.append(f"# Grammaire : {self.name}")

        lines.append(f"# Variables : {', '.join(sorted(self.variables))}")
        lines.append(f"# Terminaux : {', '.join(sorted(self.terminals))}")
        lines.append(f"# Symbole de départ : {self.start_symbol}")
        lines.append("")

        # Groupement des productions par variable
        productions_by_var = {}
        for production in self.productions:
            if production.left_side not in productions_by_var:
                productions_by_var[production.left_side] = []
            productions_by_var[production.left_side].append(production)

        for variable in sorted(productions_by_var.keys()):
            productions = productions_by_var[variable]
            if len(productions) == 1:
                lines.append(str(productions[0]))
            else:
                # Production avec alternatives
                right_sides = []
                for prod in productions:
                    if prod.is_empty():
                        right_sides.append("ε")
                    else:
                        right_sides.append(" ".join(prod.right_side))
                lines.append(f"{variable} -> {' | '.join(right_sides)}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        """Représentation détaillée de la grammaire."""
        return (
            f"ContextFreeGrammar("
            f"variables={self.variables}, "
            f"terminals={self.terminals}, "
            f"productions={len(self.productions)} productions, "
            f"start_symbol='{self.start_symbol}')"
        )
