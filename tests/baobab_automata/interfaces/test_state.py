"""
Tests unitaires pour l'interface IState et l'énumération StateType.

Ce module teste l'interface IState et l'énumération StateType.
"""

import pytest

from baobab_automata.interfaces.state import IState, StateType
from baobab_automata.implementations.state import State


class TestStateType:
    """Tests pour l'énumération StateType."""

    def test_state_type_values(self):
        """Test que tous les types d'états sont définis."""
        assert StateType.INITIAL.value == "initial"
        assert StateType.FINAL.value == "final"
        assert StateType.INTERMEDIATE.value == "intermediate"
        assert StateType.ACCEPTING.value == "accepting"
        assert StateType.REJECTING.value == "rejecting"

    def test_state_type_enumeration(self):
        """Test que l'énumération contient tous les types attendus."""
        expected_types = {
            "initial",
            "final",
            "intermediate",
            "accepting",
            "rejecting",
        }
        actual_types = {state_type.value for state_type in StateType}
        assert actual_types == expected_types


class TestIStateInterface:
    """Tests pour l'interface IState."""

    def test_interface_has_required_methods(self):
        """Test que l'interface IState a toutes les méthodes requises."""
        required_methods = [
            "identifier",
            "state_type",
            "metadata",
            "is_initial",
            "is_final",
            "is_accepting",
            "add_metadata",
            "get_metadata",
            "__eq__",
            "__hash__",
            "__str__",
            "__repr__",
        ]

        for method_name in required_methods:
            assert hasattr(
                IState, method_name
            ), f"Method {method_name} missing from IState"

    def test_interface_methods_are_abstract(self):
        """Test que les méthodes de l'interface sont abstraites."""
        # Vérifier que l'interface ne peut pas être instanciée directement
        with pytest.raises(TypeError):
            IState()

    def test_interface_properties_are_abstract(self):
        """Test que les propriétés de l'interface sont abstraites."""
        # Vérifier que les propriétés sont définies comme @property @abstractmethod
        assert hasattr(IState, "identifier")
        assert hasattr(IState, "state_type")
        assert hasattr(IState, "metadata")


class TestStateImplementation:
    """Tests pour l'implémentation State de IState."""

    def test_state_implements_interface(self):
        """Test que State implémente l'interface IState."""
        state = State("q0", StateType.INITIAL)
        assert isinstance(state, IState)

    def test_state_initialization(self):
        """Test de l'initialisation d'un état."""
        state = State(
            "q0", StateType.INITIAL, {"description": "Initial state"}
        )
        assert state.identifier == "q0"
        assert state.state_type == StateType.INITIAL
        assert state.metadata == {"description": "Initial state"}

    def test_state_initialization_default_metadata(self):
        """Test de l'initialisation avec métadonnées par défaut."""
        state = State("q0", StateType.INITIAL)
        assert state.identifier == "q0"
        assert state.state_type == StateType.INITIAL
        assert state.metadata == {}

    def test_is_initial(self):
        """Test de la méthode is_initial."""
        initial_state = State("q0", StateType.INITIAL)
        final_state = State("q1", StateType.FINAL)

        assert initial_state.is_initial() is True
        assert final_state.is_initial() is False

    def test_is_final(self):
        """Test de la méthode is_final."""
        initial_state = State("q0", StateType.INITIAL)
        final_state = State("q1", StateType.FINAL)

        assert initial_state.is_final() is False
        assert final_state.is_final() is True

    def test_is_accepting(self):
        """Test de la méthode is_accepting."""
        initial_state = State("q0", StateType.INITIAL)
        final_state = State("q1", StateType.FINAL)
        accepting_state = State("q2", StateType.ACCEPTING)
        intermediate_state = State("q3", StateType.INTERMEDIATE)

        assert initial_state.is_accepting() is False
        assert final_state.is_accepting() is True
        assert accepting_state.is_accepting() is True
        assert intermediate_state.is_accepting() is False

    def test_add_metadata_raises_not_implemented(self):
        """Test que add_metadata lève NotImplementedError."""
        state = State("q0", StateType.INITIAL)
        with pytest.raises(NotImplementedError):
            state.add_metadata("key", "value")

    def test_get_metadata(self):
        """Test de la méthode get_metadata."""
        state = State("q0", StateType.INITIAL, {"key1": "value1", "key2": 42})

        assert state.get_metadata("key1") == "value1"
        assert state.get_metadata("key2") == 42
        assert state.get_metadata("nonexistent") is None
        assert state.get_metadata("nonexistent", "default") == "default"

    def test_equality(self):
        """Test de l'égalité entre états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)

        assert state1 == state2
        assert state1 != state3
        assert state1 != "not_a_state"

    def test_hash(self):
        """Test du hachage des états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)

        assert hash(state1) == hash(state2)
        assert hash(state1) != hash(state3)

    def test_str_representation(self):
        """Test de la représentation string."""
        state = State("q0", StateType.INITIAL)
        assert str(state) == "State(q0)"

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        state = State("q0", StateType.INITIAL)
        expected = "State(identifier='q0', type=StateType.INITIAL)"
        assert repr(state) == expected

    def test_state_immutability(self):
        """Test que l'état est immuable."""
        state = State("q0", StateType.INITIAL)

        # Vérifier que l'état est hashable (nécessaire pour l'immutabilité)
        state_set = {state}
        assert state in state_set

        # Vérifier que l'état ne peut pas être modifié
        with pytest.raises(AttributeError):
            state.identifier = "q1"
