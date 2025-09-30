"""
Tests unitaires pour le parser d'expressions régulières.

Ce module contient tous les tests unitaires pour la classe RegexParser
et les classes de support associées.
"""

import pytest
from baobab_automata.finite import (
    ASTNode,
    DFA,
    EpsilonNFA,
    NodeType,
    RegexConversionError,
    RegexError,
    RegexParseError,
    RegexParser,
    RegexSyntaxError,
    Token,
    TokenType,
)


class TestToken:
    """Tests pour la classe Token."""

    def test_token_creation(self):
        """Test la création d'un token."""
        token = Token(TokenType.LITERAL, "a", 0)
        assert token.type == TokenType.LITERAL
        assert token.value == "a"
        assert token.position == 0

    def test_token_equality(self):
        """Test l'égalité de deux tokens."""
        token1 = Token(TokenType.LITERAL, "a", 0)
        token2 = Token(TokenType.LITERAL, "a", 0)
        token3 = Token(TokenType.LITERAL, "b", 0)
        
        assert token1 == token2
        assert token1 != token3

    def test_token_is_operator(self):
        """Test la détection d'opérateurs."""
        union_token = Token(TokenType.UNION, "|", 0)
        literal_token = Token(TokenType.LITERAL, "a", 0)
        
        assert union_token.is_operator()
        assert not literal_token.is_operator()

    def test_token_is_literal(self):
        """Test la détection de littéraux."""
        literal_token = Token(TokenType.LITERAL, "a", 0)
        union_token = Token(TokenType.UNION, "|", 0)
        
        assert literal_token.is_literal()
        assert not union_token.is_literal()

    def test_token_is_parenthesis(self):
        """Test la détection de parenthèses."""
        left_paren = Token(TokenType.LEFT_PAREN, "(", 0)
        literal_token = Token(TokenType.LITERAL, "a", 0)
        
        assert left_paren.is_parenthesis()
        assert not literal_token.is_parenthesis()


class TestASTNode:
    """Tests pour la classe ASTNode."""

    def test_ast_node_creation(self):
        """Test la création d'un nœud AST."""
        node = ASTNode(NodeType.LITERAL, "a")
        assert node.type == NodeType.LITERAL
        assert node.value == "a"
        assert node.children == []

    def test_ast_node_with_children(self):
        """Test la création d'un nœud AST avec enfants."""
        child1 = ASTNode(NodeType.LITERAL, "a")
        child2 = ASTNode(NodeType.LITERAL, "b")
        node = ASTNode(NodeType.UNION, children=[child1, child2])
        
        assert node.type == NodeType.UNION
        assert len(node.children) == 2
        assert node.children[0] == child1
        assert node.children[1] == child2

    def test_ast_node_is_leaf(self):
        """Test la détection de feuilles."""
        leaf = ASTNode(NodeType.LITERAL, "a")
        internal = ASTNode(NodeType.UNION, children=[leaf])
        
        assert leaf.is_leaf()
        assert not internal.is_leaf()

    def test_ast_node_is_unary(self):
        """Test la détection d'opérateurs unaires."""
        unary = ASTNode(NodeType.KLEENE_STAR)
        binary = ASTNode(NodeType.UNION)
        
        assert unary.is_unary()
        assert not binary.is_unary()

    def test_ast_node_is_binary(self):
        """Test la détection d'opérateurs binaires."""
        binary = ASTNode(NodeType.UNION)
        unary = ASTNode(NodeType.KLEENE_STAR)
        
        assert binary.is_binary()
        assert not unary.is_binary()

    def test_ast_node_to_string(self):
        """Test la conversion en string."""
        # Test littéral
        literal = ASTNode(NodeType.LITERAL, "a")
        assert literal.to_string() == "a"
        
        # Test union
        left = ASTNode(NodeType.LITERAL, "a")
        right = ASTNode(NodeType.LITERAL, "b")
        union = ASTNode(NodeType.UNION, children=[left, right])
        assert union.to_string() == "(a|b)"


class TestRegexParser:
    """Tests pour la classe RegexParser."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.parser = RegexParser()

    def test_parser_initialization(self):
        """Test l'initialisation du parser."""
        assert isinstance(self.parser.alphabet, set)
        assert "a" in self.parser.alphabet
        assert "0" in self.parser.alphabet
        assert isinstance(self.parser.operators, set)
        assert "*" in self.parser.operators
        assert isinstance(self.parser.precedence, dict)
        assert self.parser.precedence["*"] == 3

    def test_parser_with_custom_alphabet(self):
        """Test l'initialisation avec un alphabet personnalisé."""
        custom_alphabet = {"a", "b", "c"}
        parser = RegexParser(custom_alphabet)
        assert parser.alphabet == custom_alphabet

    def test_tokenize_simple_expression(self):
        """Test la tokenisation d'une expression simple."""
        tokens = self.parser._tokenize("a|b")
        assert len(tokens) == 4  # a, |, b, EOF
        assert tokens[0].type == TokenType.LITERAL
        assert tokens[0].value == "a"
        assert tokens[1].type == TokenType.UNION
        assert tokens[2].type == TokenType.LITERAL
        assert tokens[2].value == "b"
        assert tokens[3].type == TokenType.EOF

    def test_tokenize_with_parentheses(self):
        """Test la tokenisation avec parenthèses."""
        tokens = self.parser._tokenize("(a|b)*")
        assert len(tokens) == 7  # (, a, |, b, ), *, EOF
        assert tokens[0].type == TokenType.LEFT_PAREN
        assert tokens[4].type == TokenType.RIGHT_PAREN
        assert tokens[5].type == TokenType.KLEENE_STAR
        assert tokens[6].type == TokenType.EOF

    def test_tokenize_with_escape_sequences(self):
        """Test la tokenisation avec séquences d'échappement."""
        tokens = self.parser._tokenize("\\d+")
        assert len(tokens) == 3  # \d, +, EOF
        assert tokens[0].type == TokenType.DIGIT
        assert tokens[1].type == TokenType.KLEENE_PLUS

    def test_tokenize_invalid_character(self):
        """Test la tokenisation avec un caractère invalide."""
        with pytest.raises(RegexSyntaxError):
            self.parser._tokenize("a@b")

    def test_tokenize_incomplete_escape(self):
        """Test la tokenisation avec un échappement incomplet."""
        with pytest.raises(RegexSyntaxError):
            self.parser._tokenize("a\\")

    def test_parse_simple_literal(self):
        """Test le parsing d'un littéral simple."""
        tokens = self.parser._tokenize("a")
        ast = self.parser._parse_expression(tokens)
        assert ast.type == NodeType.LITERAL
        assert ast.value == "a"

    def test_parse_union(self):
        """Test le parsing d'une union."""
        tokens = self.parser._tokenize("a|b")
        ast = self.parser._parse_expression(tokens)
        assert ast.type == NodeType.UNION
        assert len(ast.children) == 2
        assert ast.children[0].type == NodeType.LITERAL
        assert ast.children[0].value == "a"
        assert ast.children[1].type == NodeType.LITERAL
        assert ast.children[1].value == "b"

    def test_parse_concatenation(self):
        """Test le parsing d'une concaténation."""
        tokens = self.parser._tokenize("ab")
        ast = self.parser._parse_expression(tokens)
        assert ast.type == NodeType.CONCATENATION
        assert len(ast.children) == 2

    def test_parse_kleene_star(self):
        """Test le parsing de l'étoile de Kleene."""
        tokens = self.parser._tokenize("a*")
        ast = self.parser._parse_expression(tokens)
        assert ast.type == NodeType.KLEENE_STAR
        assert len(ast.children) == 1
        assert ast.children[0].type == NodeType.LITERAL
        assert ast.children[0].value == "a"

    def test_parse_group(self):
        """Test le parsing d'un groupe."""
        tokens = self.parser._tokenize("(a|b)")
        ast = self.parser._parse_expression(tokens)
        assert ast.type == NodeType.GROUP
        assert len(ast.children) == 1
        assert ast.children[0].type == NodeType.UNION

    def test_parse_empty_expression(self):
        """Test le parsing d'une expression vide."""
        with pytest.raises(RegexSyntaxError):
            self.parser.parse("")

    def test_parse_unbalanced_parentheses(self):
        """Test le parsing avec parenthèses non équilibrées."""
        tokens = self.parser._tokenize("(a|b")
        with pytest.raises(RegexParseError):
            self.parser._parse_expression(tokens)

    def test_parse_complex_expression(self):
        """Test le parsing d'une expression complexe."""
        tokens = self.parser._tokenize("(a|b)*c+")
        ast = self.parser._parse_expression(tokens)
        assert ast.type == NodeType.CONCATENATION
        assert len(ast.children) == 2

    def test_validate_valid_expression(self):
        """Test la validation d'une expression valide."""
        assert self.parser.validate("a|b")
        assert self.parser.validate("(a|b)*")
        assert self.parser.validate("a+b*")

    def test_validate_invalid_expression(self):
        """Test la validation d'une expression invalide."""
        assert not self.parser.validate("a@b")
        assert not self.parser.validate("(a|b")
        assert not self.parser.validate("")

    def test_normalize_expression(self):
        """Test la normalisation d'une expression."""
        normalized = self.parser.normalize("a | b")
        assert normalized == "a|b"

    def test_serialization(self):
        """Test la sérialisation et désérialisation."""
        data = self.parser.to_dict()
        assert "alphabet" in data
        assert "operators" in data
        assert "precedence" in data
        
        new_parser = RegexParser.from_dict(data)
        assert new_parser.alphabet == self.parser.alphabet
        assert new_parser.operators == self.parser.operators
        assert new_parser.precedence == self.parser.precedence

    def test_cache_functionality(self):
        """Test le fonctionnement du cache."""
        # Premier parsing
        automaton1 = self.parser.parse("a|b")
        
        # Deuxième parsing (doit utiliser le cache)
        automaton2 = self.parser.parse("a|b")
        
        # Vérifier que le cache contient l'expression
        assert "a|b" in self.parser.cache
        
        # Vider le cache
        self.parser.clear_cache()
        assert len(self.parser.cache) == 0

    def test_cache_stats(self):
        """Test les statistiques du cache."""
        self.parser.parse("a|b")
        stats = self.parser.get_cache_stats()
        assert stats["size"] == 1
        assert "a|b" in stats["keys"]

    def test_parse_empty_string(self):
        """Test le parsing d'une chaîne vide."""
        with pytest.raises(RegexSyntaxError):
            self.parser.parse("")

    def test_parse_invalid_syntax(self):
        """Test le parsing avec une syntaxe invalide."""
        with pytest.raises(RegexSyntaxError):
            self.parser.parse("a@b")

    def test_parse_unbalanced_parentheses(self):
        """Test le parsing avec parenthèses non équilibrées."""
        with pytest.raises(RegexParseError):
            self.parser.parse("(a|b")

    def test_automaton_to_regex_placeholder(self):
        """Test la conversion automate vers regex (placeholder)."""
        # Pour l'instant, cette méthode retourne un placeholder
        automaton = self.parser.parse("a|b")
        regex = self.parser.automaton_to_regex(automaton)
        assert regex == "a*"  # Placeholder actuel

    def test_build_automaton_literal(self):
        """Test la construction d'automate pour un littéral."""
        node = ASTNode(NodeType.LITERAL, "a")
        automaton = self.parser._build_automaton(node)
        assert isinstance(automaton, DFA)

    def test_build_automaton_epsilon(self):
        """Test la construction d'automate pour epsilon."""
        node = ASTNode(NodeType.EPSILON)
        automaton = self.parser._build_automaton(node)
        assert isinstance(automaton, EpsilonNFA)

    def test_build_automaton_empty(self):
        """Test la construction d'automate pour vide."""
        node = ASTNode(NodeType.EMPTY)
        automaton = self.parser._build_automaton(node)
        assert isinstance(automaton, DFA)

    def test_build_automaton_unsupported_node(self):
        """Test la construction d'automate avec un nœud non supporté."""
        # Créer un nœud avec un type non supporté en utilisant un mock
        class UnsupportedNode:
            def __init__(self):
                self.type = "unsupported"
                self.value = "test"
                self.children = []
            
            def is_terminal(self):
                return False
            
            def is_unary(self):
                return False
            
            def is_binary(self):
                return False
        
        node = UnsupportedNode()
        
        with pytest.raises(RegexConversionError):
            self.parser._build_automaton(node)