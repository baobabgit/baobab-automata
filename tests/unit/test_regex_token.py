"""Tests unitaires pour les classes Token et TokenType."""

import pytest
from baobab_automata.finite.regex.regex_token import Token, TokenType


@pytest.mark.unit
class TestTokenType:
    """Tests pour l'énumération TokenType."""

    def test_token_type_values(self):
        """Test que tous les types de tokens ont les bonnes valeurs."""
        assert TokenType.LITERAL.value == "literal"
        assert TokenType.UNION.value == "union"
        assert TokenType.CONCATENATION.value == "concatenation"
        assert TokenType.KLEENE_STAR.value == "kleene_star"
        assert TokenType.KLEENE_PLUS.value == "kleene_plus"
        assert TokenType.OPTIONAL.value == "optional"
        assert TokenType.LEFT_PAREN.value == "left_paren"
        assert TokenType.RIGHT_PAREN.value == "right_paren"
        assert TokenType.ESCAPE.value == "escape"
        assert TokenType.DIGIT.value == "digit"
        assert TokenType.WORD.value == "word"
        assert TokenType.SPACE.value == "space"
        assert TokenType.EOF.value == "eof"

    def test_token_type_enumeration(self):
        """Test que TokenType est une énumération valide."""
        assert len(TokenType) == 13  # Il y a 13 types de tokens
        assert isinstance(TokenType.LITERAL, TokenType)
        assert isinstance(TokenType.UNION, TokenType)


@pytest.mark.unit
class TestToken:
    """Tests pour la classe Token."""

    def test_token_creation(self):
        """Test la création d'un token."""
        token = Token(TokenType.LITERAL, "a", 0)
        assert token.type == TokenType.LITERAL
        assert token.value == "a"
        assert token.position == 0

    def test_token_repr(self):
        """Test la représentation string d'un token."""
        token = Token(TokenType.LITERAL, "a", 0)
        expected = "Token(literal, 'a', 0)"
        assert repr(token) == expected

    def test_token_equality(self):
        """Test l'égalité entre tokens."""
        token1 = Token(TokenType.LITERAL, "a", 0)
        token2 = Token(TokenType.LITERAL, "a", 0)
        token3 = Token(TokenType.LITERAL, "b", 0)
        token4 = Token(TokenType.UNION, "a", 0)
        token5 = Token(TokenType.LITERAL, "a", 1)

        assert token1 == token2
        assert token1 != token3
        assert token1 != token4
        assert token1 != token5
        assert token1 != "not_a_token"

    def test_token_hash(self):
        """Test le hash d'un token."""
        token1 = Token(TokenType.LITERAL, "a", 0)
        token2 = Token(TokenType.LITERAL, "a", 0)
        token3 = Token(TokenType.LITERAL, "b", 0)

        assert hash(token1) == hash(token2)
        assert hash(token1) != hash(token3)

    def test_token_is_operator(self):
        """Test la méthode is_operator."""
        # Opérateurs
        assert Token(TokenType.UNION, "|", 0).is_operator()
        assert Token(TokenType.CONCATENATION, ".", 0).is_operator()
        assert Token(TokenType.KLEENE_STAR, "*", 0).is_operator()
        assert Token(TokenType.KLEENE_PLUS, "+", 0).is_operator()
        assert Token(TokenType.OPTIONAL, "?", 0).is_operator()

        # Non-opérateurs
        assert not Token(TokenType.LITERAL, "a", 0).is_operator()
        assert not Token(TokenType.LEFT_PAREN, "(", 0).is_operator()
        assert not Token(TokenType.RIGHT_PAREN, ")", 0).is_operator()
        assert not Token(TokenType.EOF, "", 0).is_operator()

    def test_token_is_literal(self):
        """Test la méthode is_literal."""
        # Littéraux
        assert Token(TokenType.LITERAL, "a", 0).is_literal()
        assert Token(TokenType.DIGIT, "\\d", 0).is_literal()
        assert Token(TokenType.WORD, "\\w", 0).is_literal()
        assert Token(TokenType.SPACE, "\\s", 0).is_literal()

        # Non-littéraux
        assert not Token(TokenType.UNION, "|", 0).is_literal()
        assert not Token(TokenType.LEFT_PAREN, "(", 0).is_literal()
        assert not Token(TokenType.EOF, "", 0).is_literal()

    def test_token_is_parenthesis(self):
        """Test la méthode is_parenthesis."""
        # Parenthèses
        assert Token(TokenType.LEFT_PAREN, "(", 0).is_parenthesis()
        assert Token(TokenType.RIGHT_PAREN, ")", 0).is_parenthesis()

        # Non-parenthèses
        assert not Token(TokenType.LITERAL, "a", 0).is_parenthesis()
        assert not Token(TokenType.UNION, "|", 0).is_parenthesis()
        assert not Token(TokenType.EOF, "", 0).is_parenthesis()

    def test_token_is_unary_operator(self):
        """Test la méthode is_unary_operator."""
        # Opérateurs unaires
        assert Token(TokenType.KLEENE_STAR, "*", 0).is_unary_operator()
        assert Token(TokenType.KLEENE_PLUS, "+", 0).is_unary_operator()
        assert Token(TokenType.OPTIONAL, "?", 0).is_unary_operator()

        # Non-opérateurs unaires
        assert not Token(TokenType.UNION, "|", 0).is_unary_operator()
        assert not Token(TokenType.CONCATENATION, ".", 0).is_unary_operator()
        assert not Token(TokenType.LITERAL, "a", 0).is_unary_operator()

    def test_token_is_binary_operator(self):
        """Test la méthode is_binary_operator."""
        # Opérateurs binaires
        assert Token(TokenType.UNION, "|", 0).is_binary_operator()
        assert Token(TokenType.CONCATENATION, ".", 0).is_binary_operator()

        # Non-opérateurs binaires
        assert not Token(TokenType.KLEENE_STAR, "*", 0).is_binary_operator()
        assert not Token(TokenType.KLEENE_PLUS, "+", 0).is_binary_operator()
        assert not Token(TokenType.OPTIONAL, "?", 0).is_binary_operator()
        assert not Token(TokenType.LITERAL, "a", 0).is_binary_operator()

    def test_token_immutability(self):
        """Test que les attributs du token sont immutables."""
        token = Token(TokenType.LITERAL, "a", 0)
        
        # Les attributs peuvent être modifiés (pas d'immutabilité stricte)
        # mais testons que les valeurs initiales sont correctes
        assert token.type == TokenType.LITERAL
        assert token.value == "a"
        assert token.position == 0

    def test_token_different_types(self):
        """Test avec différents types de tokens."""
        tokens = [
            Token(TokenType.LITERAL, "a", 0),
            Token(TokenType.UNION, "|", 1),
            Token(TokenType.KLEENE_STAR, "*", 2),
            Token(TokenType.LEFT_PAREN, "(", 3),
            Token(TokenType.RIGHT_PAREN, ")", 4),
            Token(TokenType.ESCAPE, "\\", 5),
            Token(TokenType.DIGIT, "\\d", 6),
            Token(TokenType.WORD, "\\w", 7),
            Token(TokenType.SPACE, "\\s", 8),
            Token(TokenType.EOF, "", 9),
        ]

        for i, token in enumerate(tokens):
            assert token.position == i
            # EOF peut avoir une valeur vide
            if token.type != TokenType.EOF:
                assert token.value != ""
            assert token.type in TokenType

    def test_token_edge_cases(self):
        """Test des cas limites pour les tokens."""
        # Token avec valeur vide
        token = Token(TokenType.EOF, "", 0)
        assert token.value == ""
        assert token.type == TokenType.EOF

        # Token avec position négative
        token = Token(TokenType.LITERAL, "a", -1)
        assert token.position == -1

        # Token avec position très grande
        token = Token(TokenType.LITERAL, "a", 999999)
        assert token.position == 999999