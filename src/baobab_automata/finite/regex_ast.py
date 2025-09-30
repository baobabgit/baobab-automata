"""
Classes de support pour l'arbre syntaxique abstrait (AST) des expressions régulières.

Ce module définit les classes ASTNode et NodeType utilisées pour représenter
l'arbre syntaxique d'une expression régulière après parsing.
"""

from enum import Enum
from typing import Any, List, Optional


class NodeType(Enum):
    """
    Types de nœuds dans l'arbre syntaxique abstrait.

    Cette énumération définit tous les types de nœuds qui peuvent être
    présents dans l'AST d'une expression régulière.
    """

    # Nœuds terminaux
    LITERAL = "literal"
    """Nœud littéral (caractère)"""

    # Nœuds d'opérations
    UNION = "union"
    """Nœud d'union (|)"""

    CONCATENATION = "concatenation"
    """Nœud de concaténation (.)"""

    KLEENE_STAR = "kleene_star"
    """Nœud étoile de Kleene (*)"""

    KLEENE_PLUS = "kleene_plus"
    """Nœud plus de Kleene (+)"""

    OPTIONAL = "optional"
    """Nœud optionnel (?)"""

    # Nœuds de groupes
    GROUP = "group"
    """Nœud de groupe (parenthèses)"""

    # Nœuds spéciaux
    EMPTY = "empty"
    """Nœud vide (mot vide)"""

    EPSILON = "epsilon"
    """Nœud epsilon (transition vide)"""


class ASTNode:
    """
    Représente un nœud dans l'arbre syntaxique abstrait d'une expression régulière.

    Un nœud AST contient le type, la valeur et les enfants d'un élément
    de l'arbre syntaxique.

    :param node_type: Type du nœud
    :type node_type: NodeType
    :param value: Valeur du nœud (pour les nœuds terminaux)
    :type value: str, optional
    :param children: Enfants du nœud
    :type children: List[ASTNode], optional
    """

    def __init__(
        self,
        node_type: NodeType,
        value: Optional[str] = None,
        children: Optional[List["ASTNode"]] = None,
    ) -> None:
        """
        Initialise un nœud AST.

        :param node_type: Type du nœud
        :param value: Valeur du nœud (pour les nœuds terminaux)
        :param children: Enfants du nœud
        """
        self.type = node_type
        self.value = value
        self.children = children or []

    def __repr__(self) -> str:
        """
        Retourne la représentation string du nœud AST.

        :return: Représentation string du nœud AST
        :rtype: str
        """
        if self.value is not None:
            return f"ASTNode({self.type.value}, '{self.value}', {len(self.children)} children)"
        return f"ASTNode({self.type.value}, {len(self.children)} children)"

    def __eq__(self, other: Any) -> bool:
        """
        Compare deux nœuds AST pour l'égalité.

        :param other: Autre objet à comparer
        :type other: Any
        :return: True si les nœuds sont égaux, False sinon
        :rtype: bool
        """
        if not isinstance(other, ASTNode):
            return False
        return (
            self.type == other.type
            and self.value == other.value
            and self.children == other.children
        )

    def __hash__(self) -> int:
        """
        Retourne le hash du nœud AST.

        :return: Hash du nœud AST
        :rtype: int
        """
        return hash((self.type, self.value, tuple(self.children)))

    def is_leaf(self) -> bool:
        """
        Vérifie si le nœud est une feuille (n'a pas d'enfants).

        :return: True si le nœud est une feuille, False sinon
        :rtype: bool
        """
        return len(self.children) == 0

    def is_unary(self) -> bool:
        """
        Vérifie si le nœud est un opérateur unaire.

        :return: True si le nœud est un opérateur unaire, False sinon
        :rtype: bool
        """
        return self.type in {
            NodeType.KLEENE_STAR,
            NodeType.KLEENE_PLUS,
            NodeType.OPTIONAL,
        }

    def is_binary(self) -> bool:
        """
        Vérifie si le nœud est un opérateur binaire.

        :return: True si le nœud est un opérateur binaire, False sinon
        :rtype: bool
        """
        return self.type in {NodeType.UNION, NodeType.CONCATENATION}

    def is_terminal(self) -> bool:
        """
        Vérifie si le nœud est terminal (littéral ou epsilon).

        :return: True si le nœud est terminal, False sinon
        :rtype: bool
        """
        return self.type in {NodeType.LITERAL, NodeType.EPSILON, NodeType.EMPTY}

    def add_child(self, child: "ASTNode") -> None:
        """
        Ajoute un enfant au nœud.

        :param child: Nœud enfant à ajouter
        :type child: ASTNode
        """
        self.children.append(child)

    def get_child(self, index: int) -> Optional["ASTNode"]:
        """
        Récupère un enfant par index.

        :param index: Index de l'enfant
        :type index: int
        :return: Nœud enfant ou None si l'index est invalide
        :rtype: Optional[ASTNode]
        """
        if 0 <= index < len(self.children):
            return self.children[index]
        return None

    def to_string(self) -> str:
        """
        Convertit l'AST en expression régulière string.

        :return: Expression régulière représentée par l'AST
        :rtype: str
        """
        if self.is_terminal():
            if self.type == NodeType.LITERAL:
                return self.value or ""
            elif self.type == NodeType.EPSILON:
                return "ε"
            elif self.type == NodeType.EMPTY:
                return "∅"
            return ""

        if self.is_unary():
            if len(self.children) == 0:
                return ""
            child_str = self.children[0].to_string()
            if self.type == NodeType.KLEENE_STAR:
                return f"({child_str})*"
            elif self.type == NodeType.KLEENE_PLUS:
                return f"({child_str})+"
            elif self.type == NodeType.OPTIONAL:
                return f"({child_str})?"
            return child_str

        if self.is_binary():
            if len(self.children) < 2:
                return ""
            
            left_str = self.children[0].to_string()
            right_str = self.children[1].to_string()
            
            if self.type == NodeType.UNION:
                return f"({left_str}|{right_str})"
            elif self.type == NodeType.CONCATENATION:
                return f"{left_str}{right_str}"
            return f"{left_str}{right_str}"

        if self.type == NodeType.GROUP:
            if len(self.children) == 0:
                return ""
            return f"({self.children[0].to_string()})"

        return ""