"""Tests unitaires pour la classe RegexParser."""

import pytest
from baobab_automata.automata.finite.regex_parser import RegexParser
from baobab_automata.automata.finite.regex_exceptions import (
    RegexSyntaxError,
    RegexParseError,
    RegexError,
)


@pytest.mark.unit
class TestRegexParser:
    """Tests pour la classe RegexParser."""

    def test_parser_initialization(self):
        """Test l'initialisation du parser."""
        parser = RegexParser()
        assert parser.alphabet is not None
        assert len(parser.alphabet) > 0
        assert parser.operators == {".", "|", "*", "+", "?", "(", ")"}
        assert parser.precedence["*"] == 3
        assert parser.precedence["."] == 2
        assert parser.precedence["|"] == 1

    def test_parser_initialization_with_custom_alphabet(self):
        """Test l'initialisation avec un alphabet personnalisé."""
        custom_alphabet = {"a", "b", "c"}
        parser = RegexParser(alphabet=custom_alphabet)
        assert parser.alphabet == custom_alphabet

    def test_parse_simple_literal(self):
        """Test le parsing d'un littéral simple."""
        parser = RegexParser()
        automaton = parser.parse("a")
        assert automaton is not None
        assert hasattr(automaton, 'states')
        assert hasattr(automaton, 'alphabet')
        assert hasattr(automaton, 'initial_state')
        assert hasattr(automaton, 'final_states')

    def test_parse_empty_string(self):
        """Test le parsing d'une chaîne vide."""
        parser = RegexParser()
        with pytest.raises(RegexSyntaxError):
            parser.parse("")

    def test_parse_simple_union(self):
        """Test le parsing d'une union simple."""
        parser = RegexParser()
        automaton = parser.parse("a|b")
        assert automaton is not None

    def test_parse_simple_concatenation(self):
        """Test le parsing d'une concaténation simple."""
        parser = RegexParser()
        automaton = parser.parse("ab")
        assert automaton is not None

    def test_parse_simple_kleene_star(self):
        """Test le parsing d'une étoile de Kleene simple."""
        parser = RegexParser()
        automaton = parser.parse("a*")
        assert automaton is not None

    def test_parse_simple_kleene_plus(self):
        """Test le parsing d'un plus de Kleene simple."""
        parser = RegexParser()
        automaton = parser.parse("a+")
        assert automaton is not None

    def test_parse_simple_optional(self):
        """Test le parsing d'un opérateur optionnel simple."""
        parser = RegexParser()
        automaton = parser.parse("a?")
        assert automaton is not None

    def test_parse_simple_parentheses(self):
        """Test le parsing avec des parenthèses simples."""
        parser = RegexParser()
        automaton = parser.parse("(a)")
        assert automaton is not None

    def test_parse_complex_expression(self):
        """Test le parsing d'une expression complexe."""
        parser = RegexParser()
        automaton = parser.parse("(a|b)*c")
        assert automaton is not None

    def test_parse_very_complex_expression(self):
        """Test le parsing d'une expression très complexe."""
        parser = RegexParser()
        automaton = parser.parse("((a|b)*c+)?")
        assert automaton is not None

    def test_parse_with_unknown_symbol(self):
        """Test le parsing avec un symbole inconnu."""
        parser = RegexParser(alphabet={"a", "b"})
        with pytest.raises(RegexSyntaxError):
            parser.parse("c")

    def test_parse_with_invalid_syntax(self):
        """Test le parsing avec une syntaxe invalide."""
        parser = RegexParser()
        with pytest.raises(RegexParseError):
            parser.parse("*")

    def test_parse_with_unmatched_parentheses(self):
        """Test le parsing avec des parenthèses non appariées."""
        parser = RegexParser()
        with pytest.raises(RegexParseError):
            parser.parse("(a")

    def test_parse_with_unmatched_parentheses_close(self):
        """Test le parsing avec des parenthèses fermantes non appariées."""
        parser = RegexParser()
        with pytest.raises(RegexParseError):
            parser.parse("a)")

    def test_parse_with_empty_parentheses(self):
        """Test le parsing avec des parenthèses vides."""
        parser = RegexParser()
        with pytest.raises(RegexParseError):
            parser.parse("()")

    def test_parse_with_consecutive_operators(self):
        """Test le parsing avec des opérateurs consécutifs."""
        parser = RegexParser()
        with pytest.raises(RegexParseError):
            parser.parse("a||b")

    def test_parse_with_operator_at_start(self):
        """Test le parsing avec un opérateur au début."""
        parser = RegexParser()
        with pytest.raises(RegexParseError):
            parser.parse("|a")

    def test_parse_with_operator_at_end(self):
        """Test le parsing avec un opérateur à la fin."""
        parser = RegexParser()
        with pytest.raises(RegexParseError):
            parser.parse("a|")

    def test_parse_with_multiple_kleene_stars(self):
        """Test le parsing avec plusieurs étoiles de Kleene."""
        parser = RegexParser()
        # Le parser accepte les opérateurs multiples
        automaton = parser.parse("a**")
        assert automaton is not None

    def test_parse_with_multiple_kleene_plus(self):
        """Test le parsing avec plusieurs plus de Kleene."""
        parser = RegexParser()
        # Le parser accepte les opérateurs multiples
        automaton = parser.parse("a++")
        assert automaton is not None

    def test_parse_with_multiple_optional(self):
        """Test le parsing avec plusieurs opérateurs optionnels."""
        parser = RegexParser()
        # Le parser accepte les opérateurs multiples
        automaton = parser.parse("a??")
        assert automaton is not None

    def test_parse_with_mixed_operators(self):
        """Test le parsing avec des opérateurs mixtes."""
        parser = RegexParser()
        # Le parser accepte les opérateurs mixtes
        automaton = parser.parse("a*+")
        assert automaton is not None

    def test_parse_with_nested_parentheses(self):
        """Test le parsing avec des parenthèses imbriquées."""
        parser = RegexParser()
        automaton = parser.parse("((a|b)|c)")
        assert automaton is not None

    def test_parse_with_deeply_nested_parentheses(self):
        """Test le parsing avec des parenthèses profondément imbriquées."""
        parser = RegexParser()
        automaton = parser.parse("(((a|b)|c)|d)")
        assert automaton is not None

    def test_parse_with_whitespace(self):
        """Test le parsing avec des espaces."""
        parser = RegexParser()
        # Le parser accepte les espaces (les ignore)
        automaton = parser.parse("a b")
        assert automaton is not None

    def test_parse_with_special_characters(self):
        """Test le parsing avec des caractères spéciaux."""
        parser = RegexParser()
        with pytest.raises(RegexSyntaxError):
            parser.parse("a@b")

    def test_parse_with_numbers(self):
        """Test le parsing avec des chiffres."""
        parser = RegexParser()
        automaton = parser.parse("123")
        assert automaton is not None

    def test_parse_with_mixed_alphanumeric(self):
        """Test le parsing avec des caractères alphanumériques mixtes."""
        parser = RegexParser()
        automaton = parser.parse("a1b2c3")
        assert automaton is not None

    def test_parse_with_epsilon_transitions(self):
        """Test le parsing avec des transitions epsilon."""
        parser = RegexParser()
        automaton = parser.parse("a*")
        assert automaton is not None

    def test_parse_with_complex_epsilon_transitions(self):
        """Test le parsing avec des transitions epsilon complexes."""
        parser = RegexParser()
        automaton = parser.parse("(a|b)*")
        assert automaton is not None

    def test_parse_caching(self):
        """Test la mise en cache des expressions parsées."""
        parser = RegexParser()
        
        # Première fois
        automaton1 = parser.parse("a")
        assert "a" in parser.cache
        
        # Deuxième fois (doit utiliser le cache)
        automaton2 = parser.parse("a")
        assert automaton1 is automaton2

    def test_parse_different_expressions(self):
        """Test le parsing d'expressions différentes."""
        parser = RegexParser()
        
        # Expressions différentes
        expr1 = "a"
        expr2 = "b"
        expr3 = "a|b"
        expr4 = "a*"
        expr5 = "ab"
        
        automaton1 = parser.parse(expr1)
        automaton2 = parser.parse(expr2)
        automaton3 = parser.parse(expr3)
        automaton4 = parser.parse(expr4)
        automaton5 = parser.parse(expr5)
        
        assert automaton1 is not None
        assert automaton2 is not None
        assert automaton3 is not None
        assert automaton4 is not None
        assert automaton5 is not None

    def test_parse_with_very_long_expression(self):
        """Test le parsing d'une expression très longue."""
        parser = RegexParser()
        long_expr = "a" * 100
        automaton = parser.parse(long_expr)
        assert automaton is not None

    def test_parse_with_repeated_patterns(self):
        """Test le parsing avec des motifs répétés."""
        parser = RegexParser()
        automaton = parser.parse("(ab)*")
        assert automaton is not None

    def test_parse_with_alternating_patterns(self):
        """Test le parsing avec des motifs alternés."""
        parser = RegexParser()
        automaton = parser.parse("(ab|cd)*")
        assert automaton is not None

    def test_parse_with_optional_patterns(self):
        """Test le parsing avec des motifs optionnels."""
        parser = RegexParser()
        automaton = parser.parse("(ab)?")
        assert automaton is not None

    def test_parse_with_plus_patterns(self):
        """Test le parsing avec des motifs plus."""
        parser = RegexParser()
        automaton = parser.parse("(ab)+")
        assert automaton is not None

    def test_parse_with_complex_nested_patterns(self):
        """Test le parsing avec des motifs imbriqués complexes."""
        parser = RegexParser()
        automaton = parser.parse("((ab|cd)*|(ef|gh)+)?")
        assert automaton is not None

    def test_parse_error_handling(self):
        """Test la gestion d'erreurs du parsing."""
        parser = RegexParser()
        
        # Test avec des erreurs de syntaxe
        with pytest.raises(RegexParseError):
            parser.parse("**")
        
        with pytest.raises(RegexParseError):
            parser.parse("++")
        
        with pytest.raises(RegexParseError):
            parser.parse("??")
        
        with pytest.raises(RegexParseError):
            parser.parse("|")
        
        with pytest.raises(RegexParseError):
            parser.parse("(")
        
        with pytest.raises(RegexParseError):
            parser.parse(")")

    def test_parse_with_invalid_characters(self):
        """Test le parsing avec des caractères invalides."""
        parser = RegexParser()
        
        # Test avec des caractères non supportés
        with pytest.raises(RegexSyntaxError):
            parser.parse("a@b")
        
        with pytest.raises(RegexSyntaxError):
            parser.parse("a#b")
        
        with pytest.raises(RegexSyntaxError):
            parser.parse("a$b")

    def test_parse_with_unicode_characters(self):
        """Test le parsing avec des caractères Unicode."""
        parser = RegexParser()
        
        # Test avec des caractères Unicode (devrait échouer avec l'alphabet par défaut)
        with pytest.raises(RegexSyntaxError):
            parser.parse("αβγ")

    def test_parse_with_custom_alphabet_unicode(self):
        """Test le parsing avec un alphabet Unicode personnalisé."""
        unicode_alphabet = {"α", "β", "γ", "δ", "ε"}
        parser = RegexParser(alphabet=unicode_alphabet)
        
        automaton = parser.parse("αβγ")
        assert automaton is not None

    def test_parse_with_very_simple_expressions(self):
        """Test le parsing d'expressions très simples."""
        parser = RegexParser()
        
        # Test avec des expressions d'un seul caractère
        for char in "abcdefghijklmnopqrstuvwxyz0123456789":
            automaton = parser.parse(char)
            assert automaton is not None

    def test_parse_with_operator_precedence(self):
        """Test le parsing avec la priorité des opérateurs."""
        parser = RegexParser()
        
        # Test que * a une priorité plus élevée que |
        automaton1 = parser.parse("a|b*")
        automaton2 = parser.parse("(a|b)*")
        
        assert automaton1 is not None
        assert automaton2 is not None
        # Les deux devraient être différents
        assert automaton1 != automaton2

    def test_parse_with_complex_operator_precedence(self):
        """Test le parsing avec une priorité d'opérateurs complexe."""
        parser = RegexParser()
        
        # Test avec des opérateurs de priorité différente
        automaton = parser.parse("a|b*c+d?")
        assert automaton is not None

    def test_parse_with_very_long_nested_expression(self):
        """Test le parsing d'une expression très longue et imbriquée."""
        parser = RegexParser()
        
        # Construction d'une expression très imbriquée
        expr = "a"
        for i in range(10):
            expr = f"({expr}|b{i})*"
        
        automaton = parser.parse(expr)
        assert automaton is not None

    def test_parse_with_edge_cases(self):
        """Test le parsing avec des cas limites."""
        parser = RegexParser()
        
        # Test avec des cas limites
        edge_cases = [
            "a*",      # Étoile de Kleene
            "a+",      # Plus de Kleene
            "a?",      # Optionnel
            "(a)",     # Parenthèses simples
            "a|b",     # Union simple
            "ab",      # Concaténation simple
        ]
        
        for case in edge_cases:
            automaton = parser.parse(case)
            assert automaton is not None

    def test_parse_with_invalid_operator_combinations(self):
        """Test le parsing avec des combinaisons d'opérateurs invalides."""
        parser = RegexParser()
        
        # Test avec des combinaisons invalides
        invalid_combinations = [
            "**",      # Double étoile
            "++",      # Double plus
            "??",      # Double optionnel
            "*+",      # Étoile et plus
            "*?",      # Étoile et optionnel
            "+?",      # Plus et optionnel
            "|*",      # Union et étoile
            "|+",      # Union et plus
            "|?",      # Union et optionnel
        ]
        
        for combination in invalid_combinations:
            with pytest.raises(RegexParseError):
                parser.parse(combination)

    def test_parse_with_valid_operator_combinations(self):
        """Test le parsing avec des combinaisons d'opérateurs valides."""
        parser = RegexParser()
        
        # Test avec des combinaisons valides
        valid_combinations = [
            "a*",      # Littéral et étoile
            "a+",      # Littéral et plus
            "a?",      # Littéral et optionnel
            "(a)*",    # Parenthèses et étoile
            "(a)+",    # Parenthèses et plus
            "(a)?",    # Parenthèses et optionnel
            "a|b",     # Union de littéraux
            "ab",      # Concaténation de littéraux
        ]
        
        for combination in valid_combinations:
            automaton = parser.parse(combination)
            assert automaton is not None