"""Tests pour les types de grammaire pushdown."""

import pytest
from baobab_automata.automata.pushdown.grammar_types import GrammarType


@pytest.mark.unit
class TestPushdownGrammarTypes:
    """Tests pour les types de grammaire pushdown."""

    def test_grammar_type_enumeration(self):
        """Test l'énumération des types de grammaire."""
        assert hasattr(GrammarType, 'GENERAL')
        assert hasattr(GrammarType, 'CHOMSKY_NORMAL_FORM')
        assert hasattr(GrammarType, 'GREIBACH_NORMAL_FORM')
        assert hasattr(GrammarType, 'LEFT_RECURSIVE')
        assert hasattr(GrammarType, 'RIGHT_RECURSIVE')
        assert hasattr(GrammarType, 'AMBIGUOUS')

    def test_grammar_type_values(self):
        """Test les valeurs des types de grammaire."""
        assert GrammarType.GENERAL.value == "general"
        assert GrammarType.CHOMSKY_NORMAL_FORM.value == "chomsky_normal_form"
        assert GrammarType.GREIBACH_NORMAL_FORM.value == "greibach_normal_form"
        assert GrammarType.LEFT_RECURSIVE.value == "left_recursive"
        assert GrammarType.RIGHT_RECURSIVE.value == "right_recursive"
        assert GrammarType.AMBIGUOUS.value == "ambiguous"

    def test_grammar_type_count(self):
        """Test le nombre de types de grammaire."""
        assert len(GrammarType) == 6

    def test_grammar_type_iteration(self):
        """Test l'itération sur les types de grammaire."""
        types = list(GrammarType)
        assert len(types) == 6
        assert GrammarType.GENERAL in types
        assert GrammarType.CHOMSKY_NORMAL_FORM in types
        assert GrammarType.GREIBACH_NORMAL_FORM in types
        assert GrammarType.LEFT_RECURSIVE in types
        assert GrammarType.RIGHT_RECURSIVE in types
        assert GrammarType.AMBIGUOUS in types

    def test_grammar_type_membership(self):
        """Test l'appartenance aux types de grammaire."""
        assert "general" in GrammarType
        assert "chomsky_normal_form" in GrammarType
        assert "greibach_normal_form" in GrammarType
        assert "left_recursive" in GrammarType
        assert "right_recursive" in GrammarType
        assert "ambiguous" in GrammarType
        assert "invalid_type" not in GrammarType

    def test_grammar_type_string_representation(self):
        """Test la représentation string des types de grammaire."""
        assert str(GrammarType.GENERAL) == "GrammarType.GENERAL"
        assert str(GrammarType.CHOMSKY_NORMAL_FORM) == "GrammarType.CHOMSKY_NORMAL_FORM"
        assert str(GrammarType.GREIBACH_NORMAL_FORM) == "GrammarType.GREIBACH_NORMAL_FORM"
        assert str(GrammarType.LEFT_RECURSIVE) == "GrammarType.LEFT_RECURSIVE"
        assert str(GrammarType.RIGHT_RECURSIVE) == "GrammarType.RIGHT_RECURSIVE"
        assert str(GrammarType.AMBIGUOUS) == "GrammarType.AMBIGUOUS"

    def test_grammar_type_repr(self):
        """Test la représentation repr des types de grammaire."""
        assert repr(GrammarType.GENERAL) == "<GrammarType.GENERAL: 'general'>"
        assert repr(GrammarType.CHOMSKY_NORMAL_FORM) == "<GrammarType.CHOMSKY_NORMAL_FORM: 'chomsky_normal_form'>"
        assert repr(GrammarType.GREIBACH_NORMAL_FORM) == "<GrammarType.GREIBACH_NORMAL_FORM: 'greibach_normal_form'>"
        assert repr(GrammarType.LEFT_RECURSIVE) == "<GrammarType.LEFT_RECURSIVE: 'left_recursive'>"
        assert repr(GrammarType.RIGHT_RECURSIVE) == "<GrammarType.RIGHT_RECURSIVE: 'right_recursive'>"
        assert repr(GrammarType.AMBIGUOUS) == "<GrammarType.AMBIGUOUS: 'ambiguous'>"

    def test_grammar_type_equality(self):
        """Test l'égalité des types de grammaire."""
        assert GrammarType.GENERAL == GrammarType.GENERAL
        assert GrammarType.GENERAL != GrammarType.CHOMSKY_NORMAL_FORM
        assert GrammarType.LEFT_RECURSIVE != GrammarType.RIGHT_RECURSIVE
        assert GrammarType.AMBIGUOUS != GrammarType.GENERAL

    def test_grammar_type_hash(self):
        """Test le hash des types de grammaire."""
        assert hash(GrammarType.GENERAL) == hash(GrammarType.GENERAL)
        assert hash(GrammarType.GENERAL) != hash(GrammarType.CHOMSKY_NORMAL_FORM)
        assert hash(GrammarType.LEFT_RECURSIVE) != hash(GrammarType.RIGHT_RECURSIVE)

    def test_grammar_type_comparison_operators(self):
        """Test les opérateurs de comparaison des types de grammaire."""
        # Les énumérations n'ont pas d'ordre défini
        with pytest.raises(TypeError):
            assert GrammarType.GENERAL < GrammarType.CHOMSKY_NORMAL_FORM
        with pytest.raises(TypeError):
            assert GrammarType.GENERAL > GrammarType.CHOMSKY_NORMAL_FORM
        with pytest.raises(TypeError):
            assert GrammarType.GENERAL <= GrammarType.CHOMSKY_NORMAL_FORM
        with pytest.raises(TypeError):
            assert GrammarType.GENERAL >= GrammarType.CHOMSKY_NORMAL_FORM

    def test_grammar_type_boolean_conversion(self):
        """Test la conversion booléenne des types de grammaire."""
        assert bool(GrammarType.GENERAL) is True
        assert bool(GrammarType.CHOMSKY_NORMAL_FORM) is True
        assert bool(GrammarType.GREIBACH_NORMAL_FORM) is True
        assert bool(GrammarType.LEFT_RECURSIVE) is True
        assert bool(GrammarType.RIGHT_RECURSIVE) is True
        assert bool(GrammarType.AMBIGUOUS) is True

    def test_grammar_type_arithmetic_operations(self):
        """Test les opérations arithmétiques sur les types de grammaire."""
        with pytest.raises(TypeError):
            _ = GrammarType.GENERAL + "1"
        with pytest.raises(TypeError):
            _ = GrammarType.GENERAL - 1
        with pytest.raises(TypeError):
            _ = GrammarType.GENERAL * 2
        with pytest.raises(TypeError):
            _ = GrammarType.GENERAL / 2

    def test_grammar_type_immutability(self):
        """Test l'immutabilité des types de grammaire."""
        with pytest.raises(AttributeError):
            GrammarType.GENERAL = "new_value"
        with pytest.raises(AttributeError):
            del GrammarType.GENERAL

    def test_grammar_type_copy(self):
        """Test la copie des types de grammaire."""
        import copy
        copied_type = copy.copy(GrammarType.GENERAL)
        assert copied_type == GrammarType.GENERAL
        assert copied_type is GrammarType.GENERAL  # Les énumérations sont des singletons

    def test_grammar_type_deep_copy(self):
        """Test la copie profonde des types de grammaire."""
        import copy
        deep_copied_type = copy.deepcopy(GrammarType.GENERAL)
        assert deep_copied_type == GrammarType.GENERAL
        assert deep_copied_type is GrammarType.GENERAL  # Les énumérations sont des singletons

    def test_grammar_type_serialization(self):
        """Test la sérialisation des types de grammaire."""
        import pickle
        serialized = pickle.dumps(GrammarType.GENERAL)
        deserialized = pickle.loads(serialized)
        assert deserialized == GrammarType.GENERAL
        assert deserialized is GrammarType.GENERAL

    def test_grammar_type_edge_cases(self):
        """Test les cas limites des types de grammaire."""
        # Test avec des valeurs vides
        assert GrammarType.GENERAL != ""
        assert GrammarType.GENERAL != None
        assert GrammarType.GENERAL != 0
        assert GrammarType.GENERAL != False

    def test_grammar_type_attributes(self):
        """Test les attributs des types de grammaire."""
        assert hasattr(GrammarType.GENERAL, 'name')
        assert hasattr(GrammarType.GENERAL, 'value')
        assert GrammarType.GENERAL.name == "GENERAL"
        assert GrammarType.GENERAL.value == "general"

    def test_grammar_type_contains(self):
        """Test l'opérateur in pour les types de grammaire."""
        assert "general" in GrammarType
        assert "chomsky_normal_form" in GrammarType
        assert "greibach_normal_form" in GrammarType
        assert "left_recursive" in GrammarType
        assert "right_recursive" in GrammarType
        assert "ambiguous" in GrammarType
        assert "invalid" not in GrammarType

    def test_grammar_type_getitem(self):
        """Test l'accès par index aux types de grammaire."""
        # Les enums Python lèvent KeyError pour les index numériques
        with pytest.raises(KeyError):
            _ = GrammarType[0]
        with pytest.raises(KeyError):
            _ = GrammarType["INVALID"]

    def test_grammar_type_setitem(self):
        """Test la modification par index des types de grammaire."""
        with pytest.raises(TypeError):
            GrammarType[0] = "new_value"
        with pytest.raises(TypeError):
            GrammarType["GENERAL"] = "new_value"

    def test_grammar_type_delitem(self):
        """Test la suppression par index des types de grammaire."""
        with pytest.raises(TypeError):
            del GrammarType[0]
        with pytest.raises(TypeError):
            del GrammarType["GENERAL"]

    def test_grammar_type_len(self):
        """Test la longueur des types de grammaire."""
        assert len(GrammarType) == 6

    def test_grammar_type_iter(self):
        """Test l'itérateur des types de grammaire."""
        types = list(iter(GrammarType))
        assert len(types) == 6
        assert all(isinstance(t, GrammarType) for t in types)

    def test_grammar_type_reversed(self):
        """Test l'itérateur inversé des types de grammaire."""
        types = list(reversed(GrammarType))
        assert len(types) == 6
        assert all(isinstance(t, GrammarType) for t in types)

    def test_grammar_type_members(self):
        """Test l'attribut members des types de grammaire."""
        assert hasattr(GrammarType, '__members__')
        members = GrammarType.__members__
        assert len(members) == 6
        assert "GENERAL" in members
        assert "CHOMSKY_NORMAL_FORM" in members
        assert "GREIBACH_NORMAL_FORM" in members
        assert "LEFT_RECURSIVE" in members
        assert "RIGHT_RECURSIVE" in members
        assert "AMBIGUOUS" in members

    def test_grammar_type_values_method(self):
        """Test la méthode values des types de grammaire."""
        values = list(GrammarType.__members__.values())
        assert len(values) == 6
        assert GrammarType.GENERAL in values
        assert GrammarType.CHOMSKY_NORMAL_FORM in values
        assert GrammarType.GREIBACH_NORMAL_FORM in values
        assert GrammarType.LEFT_RECURSIVE in values
        assert GrammarType.RIGHT_RECURSIVE in values
        assert GrammarType.AMBIGUOUS in values