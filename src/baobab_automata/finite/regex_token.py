"""
Classes de support pour la tokenisation des expressions régulières.

Ce module définit les classes Token et TokenType utilisées pour représenter
les éléments lexicaux d'une expression régulière lors de la tokenisation.
"""

from enum import Enum
from typing import Any


class TokenType(Enum):
    """
    Types de tokens supportés par le parser d'expressions régulières.

    Cette énumération définit tous les types de tokens qui peuvent être
    générés lors de la tokenisation d'une expression régulière.
    """

    # Caractères littéraux
    LITERAL = "literal"
    """Caractère littéral (a, b, c, etc.)"""

    # Opérateurs
    UNION = "union"
    """Opérateur d'union (|)"""

    CONCATENATION = "concatenation"
    """Opérateur de concaténation (.)"""

    KLEENE_STAR = "kleene_star"
    """Étoile de Kleene (*)"""

    KLEENE_PLUS = "kleene_plus"
    """Plus de Kleene (+)"""

    OPTIONAL = "optional"
    """Opérateur optionnel (?)"""

    # Parenthèses
    LEFT_PAREN = "left_paren"
    """Parenthèse gauche ("""

    RIGHT_PAREN = "right_paren"
    """Parenthèse droite )"""

    # Caractères spéciaux
    ESCAPE = "escape"
    """Caractère d'échappement (\\)"""

    # Classes de caractères
    DIGIT = "digit"
    """Classe de caractères pour les chiffres (\\d)"""

    WORD = "word"
    """Classe de caractères pour les caractères alphanumériques (\\w)"""

    SPACE = "space"
    """Classe de caractères pour les espaces (\\s)"""

    # Fin de chaîne
    EOF = "eof"
    """Fin de chaîne"""


class Token:
    """
    Représente un token dans une expression régulière.

    Un token contient le type, la valeur et la position d'un élément
    lexical dans une expression régulière.

    :param token_type: Type du token
    :type token_type: TokenType
    :param value: Valeur du token
    :type value: str
    :param position: Position du token dans l'expression
    :type position: int
    """

    def __init__(self, token_type: TokenType, value: str, position: int) -> None:
        """
        Initialise un token.

        :param token_type: Type du token
        :param value: Valeur du token
        :param position: Position du token dans l'expression
        """
        self.type = token_type
        self.value = value
        self.position = position

    def __repr__(self) -> str:
        """
        Retourne la représentation string du token.

        :return: Représentation string du token
        :rtype: str
        """
        return f"Token({self.type.value}, '{self.value}', {self.position})"

    def __eq__(self, other: Any) -> bool:
        """
        Compare deux tokens pour l'égalité.

        :param other: Autre objet à comparer
        :type other: Any
        :return: True si les tokens sont égaux, False sinon
        :rtype: bool
        """
        if not isinstance(other, Token):
            return False
        return (
            self.type == other.type
            and self.value == other.value
            and self.position == other.position
        )

    def __hash__(self) -> int:
        """
        Retourne le hash du token.

        :return: Hash du token
        :rtype: int
        """
        return hash((self.type, self.value, self.position))

    def is_operator(self) -> bool:
        """
        Vérifie si le token est un opérateur.

        :return: True si le token est un opérateur, False sinon
        :rtype: bool
        """
        return self.type in {
            TokenType.UNION,
            TokenType.CONCATENATION,
            TokenType.KLEENE_STAR,
            TokenType.KLEENE_PLUS,
            TokenType.OPTIONAL,
        }

    def is_literal(self) -> bool:
        """
        Vérifie si le token est un littéral.

        :return: True si le token est un littéral, False sinon
        :rtype: bool
        """
        return self.type in {
            TokenType.LITERAL,
            TokenType.DIGIT,
            TokenType.WORD,
            TokenType.SPACE,
        }

    def is_parenthesis(self) -> bool:
        """
        Vérifie si le token est une parenthèse.

        :return: True si le token est une parenthèse, False sinon
        :rtype: bool
        """
        return self.type in {TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN}

    def is_unary_operator(self) -> bool:
        """
        Vérifie si le token est un opérateur unaire.

        :return: True si le token est un opérateur unaire, False sinon
        :rtype: bool
        """
        return self.type in {
            TokenType.KLEENE_STAR,
            TokenType.KLEENE_PLUS,
            TokenType.OPTIONAL,
        }

    def is_binary_operator(self) -> bool:
        """
        Vérifie si le token est un opérateur binaire.

        :return: True si le token est un opérateur binaire, False sinon
        :rtype: bool
        """
        return self.type in {TokenType.UNION, TokenType.CONCATENATION}
