"""Tests unitaires pour la classe State."""

import pytest
from baobab_automata.implementations.state import State
from baobab_automata.interfaces.state import StateType


@pytest.mark.unit
class TestState:
    """Tests pour la classe State."""

    def test_state_creation_basic(self):
        """Test la création basique d'un état."""
        state = State("q0", StateType.INTERMEDIATE)
        assert state.identifier == "q0"
        assert state.state_type == StateType.INTERMEDIATE
        assert not state.is_initial()
        assert not state.is_final()

    def test_state_creation_with_initial(self):
        """Test la création d'un état initial."""
        state = State("q0", StateType.INITIAL)
        assert state.identifier == "q0"
        assert state.is_initial()
        assert not state.is_final()

    def test_state_creation_with_final(self):
        """Test la création d'un état final."""
        state = State("q0", StateType.FINAL)
        assert state.identifier == "q0"
        assert not state.is_initial()
        assert state.is_final()

    def test_state_creation_with_accepting(self):
        """Test la création d'un état acceptant."""
        state = State("q0", StateType.ACCEPTING)
        assert state.identifier == "q0"
        assert not state.is_initial()
        assert not state.is_final()
        assert state.is_accepting()

    def test_state_creation_empty_name(self):
        """Test la création d'un état avec un nom vide."""
        state = State("", StateType.INTERMEDIATE)
        assert state.identifier == ""
        assert not state.is_initial()
        assert not state.is_final()

    def test_state_creation_numeric_name(self):
        """Test la création d'un état avec un nom numérique."""
        state = State("123", StateType.INTERMEDIATE)
        assert state.identifier == "123"
        assert not state.is_initial()
        assert not state.is_final()

    def test_state_creation_special_characters(self):
        """Test la création d'un état avec des caractères spéciaux."""
        state = State("q0_$#@", StateType.INTERMEDIATE)
        assert state.identifier == "q0_$#@"
        assert not state.is_initial()
        assert not state.is_final()

    def test_state_creation_unicode_name(self):
        """Test la création d'un état avec un nom Unicode."""
        state = State("état_αβγ", StateType.INTERMEDIATE)
        assert state.identifier == "état_αβγ"
        assert not state.is_initial()
        assert not state.is_final()

    def test_state_equality_same(self):
        """Test l'égalité de deux états identiques."""
        state1 = State("q0", StateType.INTERMEDIATE)
        state2 = State("q0", StateType.INTERMEDIATE)
        assert state1 == state2
        assert hash(state1) == hash(state2)

    def test_state_equality_different_name(self):
        """Test l'égalité de deux états avec des noms différents."""
        state1 = State("q0", StateType.INTERMEDIATE)
        state2 = State("q1", StateType.INTERMEDIATE)
        assert state1 != state2

    def test_state_equality_different_type(self):
        """Test l'égalité de deux états avec des types différents."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.FINAL)
        assert state1 != state2

    def test_state_equality_with_non_state(self):
        """Test l'égalité avec un objet non-State."""
        state = State("q0", StateType.INTERMEDIATE)
        assert state != "q0"
        assert state != 123

    def test_state_hash(self):
        """Test le hash d'un état."""
        state1 = State("q0", StateType.INTERMEDIATE)
        state2 = State("q0", StateType.INTERMEDIATE)
        assert hash(state1) == hash(state2)

    def test_state_hash_with_different_types(self):
        """Test le hash d'un état avec des types différents."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.FINAL)
        assert hash(state1) != hash(state2)

    def test_state_string_representation(self):
        """Test la représentation string d'un état."""
        state = State("q0", StateType.INTERMEDIATE)
        str_repr = str(state)
        assert "q0" in str_repr
        assert "State" in str_repr

    def test_state_repr(self):
        """Test la représentation repr d'un état."""
        state = State("q0", StateType.INITIAL)
        repr_str = repr(state)
        assert "q0" in repr_str
        assert "State" in repr_str
        assert "INITIAL" in repr_str

    def test_state_metadata(self):
        """Test les métadonnées d'un état."""
        metadata = {"color": "red", "weight": 1.5}
        state = State("q0", StateType.INTERMEDIATE, metadata)
        assert state.metadata["color"] == "red"
        assert state.metadata["weight"] == 1.5

    def test_state_get_metadata(self):
        """Test la récupération de métadonnées."""
        metadata = {"color": "red"}
        state = State("q0", StateType.INTERMEDIATE, metadata)
        assert state.get_metadata("color") == "red"
        assert state.get_metadata("nonexistent") is None
        assert state.get_metadata("nonexistent", "default") == "default"

    def test_state_add_metadata_not_implemented(self):
        """Test que l'ajout de métadonnées lève NotImplementedError."""
        state = State("q0", StateType.INTERMEDIATE)
        with pytest.raises(NotImplementedError):
            state.add_metadata("key", "value")

    def test_state_copy(self):
        """Test la copie d'un état."""
        import copy
        state = State("q0", StateType.INITIAL)
        copied_state = copy.copy(state)
        assert copied_state == state
        assert copied_state is not state

    def test_state_deep_copy(self):
        """Test la copie profonde d'un état."""
        import copy
        state = State("q0", StateType.INITIAL)
        deep_copied_state = copy.deepcopy(state)
        assert deep_copied_state == state
        assert deep_copied_state is not state

    def test_state_serialization(self):
        """Test la sérialisation d'un état."""
        import pickle
        state = State("q0", StateType.INITIAL)
        serialized = pickle.dumps(state)
        deserialized = pickle.loads(serialized)
        assert deserialized == state

    def test_state_comparison_operators(self):
        """Test les opérateurs de comparaison."""
        state1 = State("q0", StateType.INTERMEDIATE)
        state2 = State("q1", StateType.INTERMEDIATE)
        state3 = State("q0", StateType.INTERMEDIATE)

        # Test de l'égalité
        assert state1 == state3
        assert state1 != state2

        # Test des opérateurs de comparaison (si implémentés)
        # Note: Les opérateurs <, >, <=, >= ne sont pas implémentés par défaut
        # mais on peut tester qu'ils lèvent une exception appropriée
        with pytest.raises(TypeError):
            state1 < state2
        with pytest.raises(TypeError):
            state1 > state2
        with pytest.raises(TypeError):
            state1 <= state2
        with pytest.raises(TypeError):
            state1 >= state2

    def test_state_boolean_conversion(self):
        """Test la conversion booléenne d'un état."""
        state = State("q0", StateType.INTERMEDIATE)
        # La conversion booléenne retourne toujours True pour les objets non-vides
        assert bool(state) is True

    def test_state_arithmetic_operations(self):
        """Test les opérations arithmétiques sur un état."""
        state = State("q0", StateType.INTERMEDIATE)
        # Les opérations arithmétiques ne sont pas implémentées par défaut
        # mais on peut tester qu'elles lèvent une exception appropriée
        with pytest.raises(TypeError):
            state + "1"
        with pytest.raises(TypeError):
            state - "1"

    def test_state_multiplication(self):
        """Test la multiplication d'un état."""
        state = State("q0", StateType.INTERMEDIATE)
        # La multiplication n'est pas implémentée par défaut pour les objets State
        # mais on peut tester qu'elle lève une exception appropriée
        with pytest.raises(TypeError):
            state * 2