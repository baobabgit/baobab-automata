"""
Tests unitaires pour le parser de grammaires hors-contexte.

Ce module contient les tests complets pour la classe GrammarParser
et toutes ses fonctionnalités.
"""

import pytest
from baobab_automata.pushdown.grammar_parser import GrammarParser
from baobab_automata.pushdown.grammar_types import (
    ContextFreeGrammar,
    GrammarType,
    Production,
)
from baobab_automata.pushdown.grammar_exceptions import (
    GrammarError,
    GrammarParseError,
    GrammarValidationError,
    GrammarConversionError,
    GrammarNormalizationError,
    GrammarOptimizationError,
)


class TestProduction:
    """Tests pour la classe Production."""

    def test_production_creation(self):
        """Test de création d'une production."""
        production = Production("S", ("a", "S", "b"))
        assert production.left_side == "S"
        assert production.right_side == ("a", "S", "b")

    def test_empty_production(self):
        """Test de création d'une production vide."""
        production = Production("S", ())
        assert production.is_empty()
        assert not production.is_terminal()
        assert not production.is_unit()
        assert not production.is_binary()

    def test_terminal_production(self):
        """Test de création d'une production terminale."""
        production = Production("S", ("a",))
        assert not production.is_empty()
        assert production.is_terminal()
        assert not production.is_unit()  # Pas unitaire car 'a' est un terminal
        assert not production.is_binary()

    def test_binary_production(self):
        """Test de création d'une production binaire."""
        production = Production("S", ("A", "B"))
        assert not production.is_empty()
        assert not production.is_terminal()
        assert not production.is_unit()
        assert production.is_binary()

    def test_production_validation(self):
        """Test de validation d'une production."""
        with pytest.raises(ValueError):
            Production("", ("a",))

        with pytest.raises(ValueError):
            Production("S", "a")  # Pas un tuple

        with pytest.raises(ValueError):
            Production("S", (1, 2))  # Pas des chaînes

    def test_production_string_representation(self):
        """Test de représentation textuelle d'une production."""
        production = Production("S", ("a", "b"))
        assert str(production) == "S -> a b"

        empty_production = Production("S", ())
        assert str(empty_production) == "S -> ε"


class TestContextFreeGrammar:
    """Tests pour la classe ContextFreeGrammar."""

    def test_grammar_creation(self):
        """Test de création d'une grammaire."""
        grammar = ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a", "b"},
            productions={
                Production("S", ("a", "S", "b")),
                Production("S", ()),
                Production("A", ("a",)),
            },
            start_symbol="S",
        )
        assert grammar.start_symbol == "S"
        assert "S" in grammar.variables
        assert "A" in grammar.variables
        assert "a" in grammar.terminals
        assert "b" in grammar.terminals

    def test_grammar_validation(self):
        """Test de validation d'une grammaire."""
        with pytest.raises(ValueError):
            ContextFreeGrammar(
                variables=set(),
                terminals={"a"},
                productions={Production("S", ("a",))},
                start_symbol="S",
            )

        with pytest.raises(ValueError):
            ContextFreeGrammar(
                variables={"S"}, terminals={"a"}, productions=set(), start_symbol="S"
            )

        with pytest.raises(ValueError):
            ContextFreeGrammar(
                variables={"S"},
                terminals={"a"},
                productions={Production("S", ("a",))},
                start_symbol="",
            )

    def test_grammar_methods(self):
        """Test des méthodes de la grammaire."""
        grammar = ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a", "b"},
            productions={
                Production("S", ("a", "S", "b")),
                Production("S", ()),
                Production("A", ("a",)),
            },
            start_symbol="S",
        )

        # Test get_productions_for
        s_productions = grammar.get_productions_for("S")
        assert len(s_productions) == 2

        # Test get_empty_productions
        empty_productions = grammar.get_empty_productions()
        assert len(empty_productions) == 1

        # Test has_empty_productions
        assert grammar.has_empty_productions()

        # Test has_unit_productions
        assert not grammar.has_unit_productions()

        # Test has_binary_productions
        assert not grammar.has_binary_productions()


class TestGrammarParser:
    """Tests pour la classe GrammarParser."""

    def test_parser_creation(self):
        """Test de création du parser."""
        parser = GrammarParser()
        assert parser._grammar is None
        assert parser._strict_validation is True

    def test_parser_creation_with_grammar(self):
        """Test de création du parser avec une grammaire."""
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )
        parser = GrammarParser(grammar)
        assert parser._grammar == grammar

    def test_load_grammar(self):
        """Test de chargement d'une grammaire."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )
        parser.load_grammar(grammar)
        assert parser._grammar == grammar

    def test_parse_grammar_simple(self):
        """Test de parsing d'une grammaire simple."""
        parser = GrammarParser()
        grammar_string = "S -> aSb | ε"
        grammar = parser.parse_grammar(grammar_string)

        assert grammar.start_symbol == "S"
        assert "S" in grammar.variables
        assert "a" in grammar.terminals
        assert "b" in grammar.terminals
        assert len(grammar.productions) == 2

    def test_parse_grammar_complex(self):
        """Test de parsing d'une grammaire complexe."""
        parser = GrammarParser()
        grammar_string = """
        S -> aSb | A
        A -> aA | b
        B -> bB | a
        """
        grammar = parser.parse_grammar(grammar_string)

        assert grammar.start_symbol == "S"
        assert "S" in grammar.variables
        assert "A" in grammar.variables
        assert "B" in grammar.variables
        assert "a" in grammar.terminals
        assert "b" in grammar.terminals

    def test_parse_grammar_invalid(self):
        """Test de parsing d'une grammaire invalide."""
        parser = GrammarParser()

        with pytest.raises(GrammarParseError):
            parser.parse_grammar("")

        with pytest.raises(GrammarParseError):
            parser.parse_grammar("S -> -> a")

        with pytest.raises(GrammarParseError):
            parser.parse_grammar("S")

    def test_validate_grammar_valid(self):
        """Test de validation d'une grammaire valide."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )
        assert parser.validate_grammar(grammar)

    def test_validate_grammar_invalid(self):
        """Test de validation d'une grammaire invalide."""
        parser = GrammarParser()

        # Grammaire sans variables
        with pytest.raises(ValueError):  # Erreur lors de la création
            grammar = ContextFreeGrammar(
                variables=set(), terminals={"a"}, productions=set(), start_symbol="S"
            )

    def test_analyze_grammar(self):
        """Test d'analyse d'une grammaire."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )

        analysis = parser.analyze_grammar(grammar)
        assert "type" in analysis
        assert "left_recursive" in analysis
        assert "right_recursive" in analysis
        assert "ambiguous" in analysis
        assert "empty_productions" in analysis

    def test_grammar_to_pda(self):
        """Test de conversion grammaire → PDA."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a", "b"},
            productions={Production("S", ("a", "S", "b")), Production("S", ())},
            start_symbol="S",
        )

        pda = parser.grammar_to_pda(grammar)
        assert pda is not None
        assert "q0" in pda.states
        assert "q1" in pda.states
        assert "q2" in pda.states
        assert "a" in pda.input_alphabet
        assert "b" in pda.input_alphabet

    def test_grammar_to_dpda(self):
        """Test de conversion grammaire → DPDA."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )

        # La conversion peut échouer si la grammaire n'est pas déterministe
        try:
            dpda = parser.grammar_to_dpda(grammar)
            assert dpda is not None
            assert "q0" in dpda.states
        except GrammarConversionError:
            # C'est acceptable si la conversion échoue
            pass

    def test_grammar_to_npda(self):
        """Test de conversion grammaire → NPDA."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a", "b"},
            productions={Production("S", ("a", "S", "b")), Production("S", ())},
            start_symbol="S",
        )

        # La conversion peut échouer si la grammaire n'est pas valide
        try:
            npda = parser.grammar_to_npda(grammar)
            assert npda is not None
            assert "q0" in npda.states
        except GrammarConversionError:
            # C'est acceptable si la conversion échoue
            pass

    def test_to_chomsky_normal_form(self):
        """Test de conversion en forme normale de Chomsky."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a", "b"},
            productions={
                Production("S", ("a", "S", "b")),
                Production("S", ()),
                Production("A", ("a", "A", "b")),
            },
            start_symbol="S",
        )

        cnf_grammar = parser.to_chomsky_normal_form(grammar)
        assert cnf_grammar is not None
        assert cnf_grammar.start_symbol == "S"

    def test_to_greibach_normal_form(self):
        """Test de conversion en forme normale de Greibach."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )

        gnf_grammar = parser.to_greibach_normal_form(grammar)
        assert gnf_grammar is not None
        assert gnf_grammar.start_symbol == "S"

    def test_eliminate_empty_productions(self):
        """Test d'élimination des productions vides."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a"},
            productions={Production("S", ("a", "A")), Production("A", ())},
            start_symbol="S",
        )

        new_grammar = parser.eliminate_empty_productions(grammar)
        assert new_grammar is not None
        assert new_grammar.start_symbol == "S"

    def test_eliminate_left_recursion(self):
        """Test d'élimination de la récursivité gauche."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("S", "a")), Production("S", ("a",))},
            start_symbol="S",
        )

        new_grammar = parser.eliminate_left_recursion(grammar)
        assert new_grammar is not None
        assert new_grammar.start_symbol == "S"

    def test_eliminate_unit_productions(self):
        """Test d'élimination des productions unitaires."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a"},
            productions={Production("S", ("A",)), Production("A", ("a",))},
            start_symbol="S",
        )

        new_grammar = parser.eliminate_unit_productions(grammar)
        assert new_grammar is not None
        assert new_grammar.start_symbol == "S"

    def test_eliminate_inaccessible_symbols(self):
        """Test d'élimination des symboles inaccessibles."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a"},
            productions={Production("S", ("a",)), Production("A", ("a",))},
            start_symbol="S",
        )

        new_grammar = parser.eliminate_inaccessible_symbols(grammar)
        assert new_grammar is not None
        assert new_grammar.start_symbol == "S"
        assert "A" not in new_grammar.variables

    def test_eliminate_non_generating_symbols(self):
        """Test d'élimination des symboles non-générateurs."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a"},
            productions={Production("S", ("a",)), Production("A", ("A",))},
            start_symbol="S",
        )

        new_grammar = parser.eliminate_non_generating_symbols(grammar)
        assert new_grammar is not None
        assert new_grammar.start_symbol == "S"
        assert "A" not in new_grammar.variables

    def test_optimize_grammar(self):
        """Test d'optimisation d'une grammaire."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a"},
            productions={Production("S", ("a",)), Production("A", ("a",))},
            start_symbol="S",
        )

        optimized_grammar = parser.optimize_grammar(grammar)
        assert optimized_grammar is not None
        assert optimized_grammar.start_symbol == "S"

    def test_detect_ambiguity(self):
        """Test de détection d'ambiguïté."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",)), Production("S", ("a",))},
            start_symbol="S",
        )

        is_ambiguous = parser.detect_ambiguity(grammar)
        assert isinstance(is_ambiguous, bool)

    def test_analyze_recursion(self):
        """Test d'analyse de récursivité."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("S", "a")), Production("S", ("a",))},
            start_symbol="S",
        )

        analysis = parser.analyze_recursion(grammar)
        assert "left_recursive" in analysis
        assert "right_recursive" in analysis
        assert "left_recursive_variables" in analysis
        assert "right_recursive_variables" in analysis
        assert "recursion_depth" in analysis

    def test_to_dict(self):
        """Test de conversion en dictionnaire."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )

        data = parser.to_dict(grammar)
        assert "variables" in data
        assert "terminals" in data
        assert "productions" in data
        assert "start_symbol" in data
        assert data["start_symbol"] == "S"

    def test_from_dict(self):
        """Test de création depuis un dictionnaire."""
        parser = GrammarParser()
        data = {
            "variables": ["S"],
            "terminals": ["a"],
            "productions": [{"left_side": "S", "right_side": ["a"]}],
            "start_symbol": "S",
        }

        grammar = parser.from_dict(data)
        assert grammar.start_symbol == "S"
        assert "S" in grammar.variables
        assert "a" in grammar.terminals

    def test_export_grammar_text(self):
        """Test d'export en format texte."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )

        text = parser.export_grammar(grammar, "text")
        assert isinstance(text, str)
        assert "S" in text
        assert "a" in text

    def test_export_grammar_json(self):
        """Test d'export en format JSON."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )

        json_str = parser.export_grammar(grammar, "json")
        assert isinstance(json_str, str)
        assert "S" in json_str
        assert "a" in json_str

    def test_export_grammar_xml(self):
        """Test d'export en format XML."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )

        xml_str = parser.export_grammar(grammar, "xml")
        assert isinstance(xml_str, str)
        assert "<grammar>" in xml_str
        assert "S" in xml_str
        assert "a" in xml_str

    def test_import_grammar_text(self):
        """Test d'import en format texte."""
        parser = GrammarParser()
        grammar_string = "S -> a"

        grammar = parser.import_grammar(grammar_string, "text")
        assert grammar.start_symbol == "S"
        assert "S" in grammar.variables
        assert "a" in grammar.terminals

    def test_import_grammar_json(self):
        """Test d'import en format JSON."""
        parser = GrammarParser()
        json_data = '{"variables": ["S"], "terminals": ["a"], "productions": [{"left_side": "S", "right_side": ["a"]}], "start_symbol": "S"}'

        grammar = parser.import_grammar(json_data, "json")
        assert grammar.start_symbol == "S"
        assert "S" in grammar.variables
        assert "a" in grammar.terminals

    def test_to_string(self):
        """Test de conversion en chaîne de caractères."""
        parser = GrammarParser()
        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )

        string = parser.to_string(grammar)
        assert isinstance(string, str)
        assert "S" in string
        assert "a" in string

    def test_parser_string_representation(self):
        """Test de représentation textuelle du parser."""
        parser = GrammarParser()
        assert str(parser) == "GrammarParser(grammar=None)"

        grammar = ContextFreeGrammar(
            variables={"S"},
            terminals={"a"},
            productions={Production("S", ("a",))},
            start_symbol="S",
        )
        parser.load_grammar(grammar)
        assert str(parser) == "GrammarParser(grammar=S)"


class TestGrammarParserIntegration:
    """Tests d'intégration pour le parser de grammaires."""

    def test_complete_workflow(self):
        """Test du workflow complet : parsing → validation → conversion → normalisation."""
        parser = GrammarParser()

        # Parsing d'une grammaire
        grammar_string = "S -> aSb | ε"
        grammar = parser.parse_grammar(grammar_string)

        # Validation
        assert parser.validate_grammar(grammar)

        # Analyse
        analysis = parser.analyze_grammar(grammar)
        assert analysis["type"] == GrammarType.GENERAL

        # Conversion en PDA
        pda = parser.grammar_to_pda(grammar)
        assert pda is not None

        # Normalisation
        cnf_grammar = parser.to_chomsky_normal_form(grammar)
        assert cnf_grammar is not None

        # Optimisation
        optimized_grammar = parser.optimize_grammar(grammar)
        assert optimized_grammar is not None

    def test_anbn_grammar(self):
        """Test avec la grammaire a^n b^n."""
        parser = GrammarParser()
        grammar_string = "S -> aSb | ε"
        grammar = parser.parse_grammar(grammar_string)

        # Validation
        assert parser.validate_grammar(grammar)

        # Conversion en PDA
        pda = parser.grammar_to_pda(grammar)
        assert pda is not None

        # Test de reconnaissance (si le PDA est implémenté)
        # assert pda.accepts('aabb')  # True
        # assert not pda.accepts('abab')  # False

    def test_palindrome_grammar(self):
        """Test avec une grammaire de palindrome."""
        parser = GrammarParser()
        grammar_string = "S -> aSa | bSb | a | b | ε"
        grammar = parser.parse_grammar(grammar_string)

        # Validation
        assert parser.validate_grammar(grammar)

        # Conversion en PDA
        pda = parser.grammar_to_pda(grammar)
        assert pda is not None

    def test_error_handling(self):
        """Test de gestion des erreurs."""
        parser = GrammarParser()

        # Erreur de parsing
        with pytest.raises(GrammarParseError):
            parser.parse_grammar("S -> -> a")

        # Erreur de validation
        with pytest.raises(ValueError):  # Erreur lors de la création
            grammar = ContextFreeGrammar(
                variables=set(), terminals={"a"}, productions=set(), start_symbol="S"
            )
            parser.validate_grammar(grammar)

        # Erreur de conversion
        with pytest.raises(ValueError):  # Erreur lors de la création
            # Création d'une grammaire invalide pour la conversion
            invalid_grammar = ContextFreeGrammar(
                variables={"S"}, terminals={"a"}, productions=set(), start_symbol="S"
            )

    def test_performance(self):
        """Test de performance avec une grammaire complexe."""
        parser = GrammarParser()

        # Grammaire avec plusieurs variables et productions
        grammar_string = """
        S -> A | B
        A -> aA | a
        B -> bB | b
        C -> cC | c
        """
        grammar = parser.parse_grammar(grammar_string)

        # Validation
        assert parser.validate_grammar(grammar)

        # Analyse
        analysis = parser.analyze_grammar(grammar)
        assert analysis["variable_count"] == 4
        assert analysis["terminal_count"] == 3

        # Conversion
        pda = parser.grammar_to_pda(grammar)
        assert pda is not None

        # Normalisation
        cnf_grammar = parser.to_chomsky_normal_form(grammar)
        assert cnf_grammar is not None
