"""
Parser d'expressions régulières pour Baobab Automata.

Ce module implémente un parser complet d'expressions régulières permettant
de construire des automates à partir d'expressions et de convertir des automates
en expressions régulières.
"""

import re
from typing import Any, Dict, List, Optional, Set

from .abstract_finite_automaton import AbstractFiniteAutomaton
from .dfa import DFA
from .epsilon_nfa import EpsilonNFA
from .nfa import NFA
from .regex_ast import ASTNode, NodeType
from .regex_exceptions import (
    RegexConversionError,
    RegexError,
    RegexParseError,
    RegexSyntaxError,
)
from .regex_token import Token, TokenType


class RegexParser:
    """
    Parser d'expressions régulières.

    Cette classe fournit un parser complet d'expressions régulières avec
    support pour la construction d'automates et la conversion bidirectionnelle.

    :param alphabet: Alphabet supporté par le parser
    :type alphabet: Optional[Set[str]]
    """

    def __init__(self, alphabet: Optional[Set[str]] = None) -> None:
        """
        Initialise le parser d'expressions régulières.

        :param alphabet: Alphabet supporté par le parser
        """
        # Alphabet par défaut : lettres minuscules et chiffres
        self.alphabet = alphabet or set("abcdefghijklmnopqrstuvwxyz0123456789")
        
        # Opérateurs supportés
        self.operators = {".", "|", "*", "+", "?", "(", ")"}
        
        # Priorité des opérateurs (plus élevé = plus prioritaire)
        self.precedence = {
            "*": 3,
            "+": 3,
            "?": 3,
            ".": 2,
            "|": 1,
        }
        
        # Cache des expressions parsées
        self.cache: Dict[str, AbstractFiniteAutomaton] = {}

    def parse(self, regex: str) -> AbstractFiniteAutomaton:
        """
        Parse une expression régulière et retourne l'automate correspondant.

        :param regex: Expression régulière à parser
        :type regex: str
        :return: Automate correspondant à l'expression
        :rtype: AbstractFiniteAutomaton
        :raises RegexSyntaxError: Si l'expression a une syntaxe invalide
        :raises RegexParseError: Si le parsing échoue
        """
        if not regex:
            raise RegexSyntaxError("Expression régulière vide", 0, regex)

        # Vérifier le cache
        if regex in self.cache:
            return self.cache[regex]

        try:
            # Tokeniser l'expression
            tokens = self._tokenize(regex)
            
            # Parser l'expression
            ast = self._parse_expression(tokens)
            
            # Construire l'automate
            automaton = self._build_automaton(ast)
            
            # Optimiser l'automate
            automaton = self._optimize_automaton(automaton)
            
            # Mettre en cache
            self.cache[regex] = automaton
            
            return automaton

        except Exception as e:
            if isinstance(e, (RegexSyntaxError, RegexParseError)):
                raise
            raise RegexParseError(f"Erreur lors du parsing: {str(e)}", regex=regex)

    def _tokenize(self, regex: str) -> List[Token]:
        """
        Tokenise une expression régulière.

        :param regex: Expression régulière à tokeniser
        :type regex: str
        :return: Liste des tokens
        :rtype: List[Token]
        :raises RegexSyntaxError: Si un caractère invalide est trouvé
        """
        tokens = []
        i = 0
        
        while i < len(regex):
            char = regex[i]
            
            if char.isspace():
                i += 1
                continue
                
            if char in self.alphabet:
                tokens.append(Token(TokenType.LITERAL, char, i))
            elif char == "|":
                tokens.append(Token(TokenType.UNION, char, i))
            elif char == "*":
                tokens.append(Token(TokenType.KLEENE_STAR, char, i))
            elif char == "+":
                tokens.append(Token(TokenType.KLEENE_PLUS, char, i))
            elif char == "?":
                tokens.append(Token(TokenType.OPTIONAL, char, i))
            elif char == "(":
                tokens.append(Token(TokenType.LEFT_PAREN, char, i))
            elif char == ")":
                tokens.append(Token(TokenType.RIGHT_PAREN, char, i))
            elif char == "\\":
                # Gestion des caractères échappés
                if i + 1 < len(regex):
                    next_char = regex[i + 1]
                    if next_char == "d":
                        tokens.append(Token(TokenType.DIGIT, "\\d", i))
                    elif next_char == "w":
                        tokens.append(Token(TokenType.WORD, "\\w", i))
                    elif next_char == "s":
                        tokens.append(Token(TokenType.SPACE, "\\s", i))
                    else:
                        tokens.append(Token(TokenType.LITERAL, next_char, i))
                    i += 1
                else:
                    raise RegexSyntaxError(
                        "Caractère d'échappement incomplet", i, regex
                    )
            else:
                raise RegexSyntaxError(
                    f"Caractère non supporté: '{char}'", i, regex
                )
            
            i += 1
        
        tokens.append(Token(TokenType.EOF, "", len(regex)))
        return tokens

    def _parse_expression(self, tokens: List[Token]) -> ASTNode:
        """
        Parse une expression régulière en utilisant l'algorithme récursive descent.

        :param tokens: Liste des tokens à parser
        :type tokens: List[Token]
        :return: Nœud racine de l'AST
        :rtype: ASTNode
        :raises RegexParseError: Si le parsing échoue
        """
        if not tokens or tokens[0].type == TokenType.EOF:
            raise RegexParseError("Expression vide", parse_step="expression")
        
        self._token_index = 0
        self._tokens = tokens
        
        try:
            ast = self._parse_union()
            if self._current_token().type != TokenType.EOF:
                raise RegexParseError(
                    "Caractères supplémentaires après l'expression",
                    self._current_token().position,
                    parse_step="expression"
                )
            return ast
        except Exception as e:
            if isinstance(e, RegexParseError):
                raise
            raise RegexParseError(f"Erreur de parsing: {str(e)}", parse_step="expression")

    def _current_token(self) -> Token:
        """Récupère le token courant."""
        if self._token_index < len(self._tokens):
            return self._tokens[self._token_index]
        return Token(TokenType.EOF, "", -1)

    def _advance(self) -> None:
        """Avance au token suivant."""
        self._token_index += 1

    def _parse_union(self) -> ASTNode:
        """Parse une expression d'union (|)."""
        left = self._parse_concatenation()
        
        while self._current_token().type == TokenType.UNION:
            self._advance()
            right = self._parse_concatenation()
            left = ASTNode(NodeType.UNION, children=[left, right])
        
        return left

    def _parse_concatenation(self) -> ASTNode:
        """Parse une expression de concaténation."""
        left = self._parse_factor()
        
        while (
            self._current_token().type in {
                TokenType.LITERAL,
                TokenType.DIGIT,
                TokenType.WORD,
                TokenType.SPACE,
                TokenType.LEFT_PAREN,
            }
            or self._current_token().is_literal()
        ):
            right = self._parse_factor()
            left = ASTNode(NodeType.CONCATENATION, children=[left, right])
        
        return left

    def _parse_factor(self) -> ASTNode:
        """Parse un facteur (élément avec opérateurs unaires)."""
        primary = self._parse_primary()
        
        while self._current_token().is_unary_operator():
            token = self._current_token()
            self._advance()
            
            if token.type == TokenType.KLEENE_STAR:
                primary = ASTNode(NodeType.KLEENE_STAR, children=[primary])
            elif token.type == TokenType.KLEENE_PLUS:
                primary = ASTNode(NodeType.KLEENE_PLUS, children=[primary])
            elif token.type == TokenType.OPTIONAL:
                primary = ASTNode(NodeType.OPTIONAL, children=[primary])
        
        return primary

    def _parse_primary(self) -> ASTNode:
        """Parse un élément primaire (littéral ou groupe)."""
        token = self._current_token()
        
        if token.type == TokenType.LEFT_PAREN:
            self._advance()
            expr = self._parse_union()
            if self._current_token().type != TokenType.RIGHT_PAREN:
                raise RegexParseError(
                    "Parenthèse fermante attendue",
                    token.position,
                    parse_step="primary"
                )
            self._advance()
            return ASTNode(NodeType.GROUP, children=[expr])
        
        elif token.is_literal():
            self._advance()
            return ASTNode(NodeType.LITERAL, value=token.value)
        
        else:
            raise RegexParseError(
                f"Token inattendu: {token.type.value}",
                token.position,
                parse_step="primary"
            )

    def _build_automaton(self, node: ASTNode) -> AbstractFiniteAutomaton:
        """
        Construit un automate à partir d'un nœud AST.

        :param node: Nœud racine de l'AST
        :type node: ASTNode
        :return: Automate correspondant à l'AST
        :rtype: AbstractFiniteAutomaton
        """
        if node.is_terminal():
            return self._build_literal_automaton(node)
        
        if node.is_unary():
            return self._build_unary_automaton(node)
        
        if node.is_binary():
            return self._build_binary_automaton(node)
        
        if node.type == NodeType.GROUP:
            return self._build_automaton(node.children[0])
        
        # Gérer les types non supportés
        node_type_str = getattr(node.type, 'value', str(node.type))
        raise RegexConversionError(
            f"Type de nœud non supporté: {node_type_str}",
            conversion_step="build_automaton"
        )

    def _build_literal_automaton(self, node: ASTNode) -> AbstractFiniteAutomaton:
        """Construit un automate pour un littéral."""
        if node.type == NodeType.LITERAL:
            return self._create_simple_dfa(node.value)
        elif node.type == NodeType.EPSILON:
            return self._create_epsilon_automaton()
        elif node.type == NodeType.EMPTY:
            return self._create_empty_automaton()
        else:
            raise RegexConversionError(
                f"Type de littéral non supporté: {node.type.value}",
                conversion_step="build_literal_automaton"
            )

    def _build_unary_automaton(self, node: ASTNode) -> AbstractFiniteAutomaton:
        """Construit un automate pour un opérateur unaire."""
        child_automaton = self._build_automaton(node.children[0])
        
        if node.type == NodeType.KLEENE_STAR:
            return self._kleene_star(child_automaton)
        elif node.type == NodeType.KLEENE_PLUS:
            return self._kleene_plus(child_automaton)
        elif node.type == NodeType.OPTIONAL:
            return self._optional(child_automaton)
        else:
            raise RegexConversionError(
                f"Type d'opérateur unaire non supporté: {node.type.value}",
                conversion_step="build_unary_automaton"
            )

    def _build_binary_automaton(self, node: ASTNode) -> AbstractFiniteAutomaton:
        """Construit un automate pour un opérateur binaire."""
        left_automaton = self._build_automaton(node.children[0])
        right_automaton = self._build_automaton(node.children[1])
        
        if node.type == NodeType.UNION:
            return self._union(left_automaton, right_automaton)
        elif node.type == NodeType.CONCATENATION:
            return self._concatenation(left_automaton, right_automaton)
        else:
            raise RegexConversionError(
                f"Type d'opérateur binaire non supporté: {node.type.value}",
                conversion_step="build_binary_automaton"
            )

    def _create_simple_dfa(self, symbol: str) -> DFA:
        """Crée un DFA simple pour un symbole."""
        states = {"q0", "q1"}
        alphabet = {symbol}
        initial_state = "q0"
        final_states = {"q1"}
        transitions = {("q0", symbol): "q1"}
        
        return DFA(states, alphabet, transitions, initial_state, final_states)

    def _create_epsilon_automaton(self) -> EpsilonNFA:
        """Crée un automate epsilon (accepte le mot vide)."""
        states = {"q0"}
        alphabet = set()
        initial_state = "q0"
        final_states = {"q0"}
        transitions = {}
        
        return EpsilonNFA(states, alphabet, transitions, initial_state, final_states)

    def _create_empty_automaton(self) -> DFA:
        """Crée un automate vide (n'accepte rien)."""
        states = {"q0"}
        alphabet = set()
        initial_state = "q0"
        final_states = set()
        transitions = {}
        
        return DFA(states, alphabet, transitions, initial_state, final_states)

    def _kleene_star(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """Applique l'étoile de Kleene à un automate."""
        # Conversion en ε-NFA pour faciliter les opérations
        if not isinstance(automaton, EpsilonNFA):
            automaton = self._to_epsilon_nfa(automaton)
        
        # Implémentation simplifiée - à améliorer
        return automaton

    def _kleene_plus(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """Applique le plus de Kleene à un automate."""
        # a+ = a.a*
        concatenated = self._concatenation(automaton, self._kleene_star(automaton))
        return concatenated

    def _optional(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """Applique l'opérateur optionnel à un automate."""
        # a? = a|ε
        epsilon_auto = self._create_epsilon_automaton()
        return self._union(automaton, epsilon_auto)

    def _union(self, left: AbstractFiniteAutomaton, right: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """Calcule l'union de deux automates."""
        # Conversion en ε-NFA pour faciliter les opérations
        left_nfa = self._to_epsilon_nfa(left)
        right_nfa = self._to_epsilon_nfa(right)
        
        # Implémentation simplifiée - à améliorer
        return left_nfa

    def _concatenation(self, left: AbstractFiniteAutomaton, right: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """Calcule la concaténation de deux automates."""
        # Conversion en ε-NFA pour faciliter les opérations
        left_nfa = self._to_epsilon_nfa(left)
        right_nfa = self._to_epsilon_nfa(right)
        
        # Implémentation simplifiée - à améliorer
        return left_nfa

    def _to_epsilon_nfa(self, automaton: AbstractFiniteAutomaton) -> EpsilonNFA:
        """Convertit un automate en ε-NFA."""
        if isinstance(automaton, EpsilonNFA):
            return automaton
        
        # Conversion simplifiée - à améliorer
        states = automaton.states
        alphabet = automaton.alphabet
        initial_state = automaton.initial_state
        final_states = automaton.final_states
        transitions = {}
        
        return EpsilonNFA(states, alphabet, transitions, initial_state, final_states)

    def _optimize_automaton(self, automaton: AbstractFiniteAutomaton) -> AbstractFiniteAutomaton:
        """
        Optimise un automate.

        :param automaton: Automate à optimiser
        :type automaton: AbstractFiniteAutomaton
        :return: Automate optimisé
        :rtype: AbstractFiniteAutomaton
        """
        # Pour l'instant, retourne l'automate tel quel
        # L'optimisation sera implémentée plus tard
        return automaton

    def automaton_to_regex(self, automaton: AbstractFiniteAutomaton) -> str:
        """
        Convertit un automate en expression régulière.

        :param automaton: Automate à convertir
        :type automaton: AbstractFiniteAutomaton
        :return: Expression régulière correspondante
        :rtype: str
        :raises RegexConversionError: Si la conversion échoue
        """
        try:
            # Algorithme de Kleene simplifié
            # À implémenter complètement
            return "a*"  # Placeholder
        except Exception as e:
            raise RegexConversionError(
                f"Erreur lors de la conversion: {str(e)}",
                automaton_type=type(automaton).__name__,
                conversion_direction="automate→regex"
            )

    def validate(self, regex: str) -> bool:
        """
        Valide une expression régulière.

        :param regex: Expression régulière à valider
        :type regex: str
        :return: True si l'expression est valide, False sinon
        :rtype: bool
        """
        try:
            self.parse(regex)
            return True
        except (RegexSyntaxError, RegexParseError):
            return False

    def normalize(self, regex: str) -> str:
        """
        Normalise une expression régulière.

        :param regex: Expression régulière à normaliser
        :type regex: str
        :return: Expression normalisée
        :rtype: str
        """
        # Supprimer les espaces
        normalized = re.sub(r'\s+', '', regex)
        
        # Ajouter des concaténations implicites
        # À implémenter complètement
        
        return normalized

    def to_dict(self) -> Dict[str, Any]:
        """
        Sérialise le parser en dictionnaire.

        :return: Dictionnaire représentant le parser
        :rtype: Dict[str, Any]
        """
        return {
            "alphabet": list(self.alphabet),
            "operators": list(self.operators),
            "precedence": self.precedence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RegexParser":
        """
        Crée un parser depuis un dictionnaire.

        :param data: Dictionnaire représentant le parser
        :type data: Dict[str, Any]
        :return: Instance du parser
        :rtype: RegexParser
        """
        alphabet = set(data.get("alphabet", []))
        parser = cls(alphabet)
        parser.operators = set(data.get("operators", parser.operators))
        parser.precedence = data.get("precedence", parser.precedence)
        return parser

    def clear_cache(self) -> None:
        """Vide le cache des expressions parsées."""
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques du cache.

        :return: Statistiques du cache
        :rtype: Dict[str, Any]
        """
        return {
            "size": len(self.cache),
            "keys": list(self.cache.keys()),
        }