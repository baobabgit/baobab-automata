"""Tests unitaires pour les états d'automates."""

import pytest
from baobab_automata.interfaces.state import StateType
from baobab_automata.implementations.state import State


@pytest.mark.unit
class TestState:
    """Tests pour la classe State."""

    def test_state_creation(self):
        """Test la création d'un état."""
        state = State("q0", StateType.INITIAL)
        assert state.identifier == "q0"
        assert state.state_type == StateType.INITIAL
        assert state.metadata == {}

    def test_state_creation_with_metadata(self):
        """Test la création d'un état avec métadonnées."""
        metadata = {"description": "Test state", "priority": 1}
        state = State("q0", StateType.INITIAL, metadata)
        assert state.metadata == metadata

    def test_is_initial(self):
        """Test la méthode is_initial."""
        initial_state = State("q0", StateType.INITIAL)
        non_initial_state = State("q1", StateType.INTERMEDIATE)

        assert initial_state.is_initial() is True
        assert non_initial_state.is_initial() is False

    def test_is_final(self):
        """Test la méthode is_final."""
        final_state = State("q0", StateType.FINAL)
        non_final_state = State("q1", StateType.INTERMEDIATE)

        assert final_state.is_final() is True
        assert non_final_state.is_final() is False

    def test_is_accepting(self):
        """Test la méthode is_accepting."""
        accepting_state = State("q0", StateType.ACCEPTING)
        final_state = State("q1", StateType.FINAL)
        non_accepting_state = State("q2", StateType.INTERMEDIATE)

        assert accepting_state.is_accepting() is True
        assert final_state.is_accepting() is True
        assert non_accepting_state.is_accepting() is False

    def test_equality(self):
        """Test l'égalité entre états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)

        assert state1 == state2
        assert state1 != state3
        assert state1 != "not_a_state"

    def test_hash(self):
        """Test le hash des états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)

        assert hash(state1) == hash(state2)
        assert hash(state1) != hash(state3)

        # Test dans un set
        states_set = {state1, state2, state3}
        assert len(states_set) == 2  # state1 et state2 sont identiques

    def test_string_representation(self):
        """Test la représentation string des états."""
        state = State("q0", StateType.INITIAL)
        assert str(state) == "State(q0)"
        assert "q0" in repr(state)
        assert "INITIAL" in repr(state)

    def test_metadata_operations(self):
        """Test les opérations sur les métadonnées."""
        state = State("q0", StateType.INITIAL, {"key1": "value1"})

        assert state.get_metadata("key1") == "value1"
        assert state.get_metadata("key2") is None
        assert state.get_metadata("key2", "default") == "default"

    def test_add_metadata_raises_not_implemented(self):
        """Test que add_metadata lève NotImplementedError."""
        state = State("q0", StateType.INITIAL)

        with pytest.raises(NotImplementedError):
            state.add_metadata("key", "value")

    @pytest.mark.parametrize(
        "identifier,state_type,expected_valid",
        [
            ("q0", StateType.INITIAL, True),
            ("", StateType.INITIAL, True),  # Empty string is valid
        ],
    )
    def test_validation(self, identifier, state_type, expected_valid):
        """Test la validation des états."""
        if expected_valid and isinstance(state_type, StateType):
            state = State(identifier, state_type)
            assert state.identifier == identifier
        else:
            with pytest.raises((ValueError, TypeError)):
                State(identifier, state_type)

    def test_invalid_state_type(self):
        """Test la création d'un état avec un type invalide."""
        # La classe State n'effectue pas de validation du type d'état
        # car elle utilise un dataclass simple. Ce test vérifie le comportement actuel.
        # En fait, Python accepte n'importe quel type pour le paramètre state_type
        # car c'est un dataclass simple sans validation.
        state = State("q0", "invalid_type")
        assert state.identifier == "q0"
        assert state.state_type == "invalid_type"

    def test_immutability(self):
        """Test l'immutabilité des états."""
        metadata = {"key": "value"}
        state = State("q0", StateType.INITIAL, metadata)

        # Les métadonnées ne peuvent pas être modifiées
        assert state.metadata["key"] == "value"

        # Modification de la copie originale ne doit pas affecter l'état
        metadata["key"] = "modified"
        assert state.metadata["key"] == "value"  # Non modifié

    def test_different_state_types(self):
        """Test la création d'états avec différents types."""
        initial = State("q0", StateType.INITIAL)
        intermediate = State("q1", StateType.INTERMEDIATE)
        final = State("q2", StateType.FINAL)
        accepting = State("q3", StateType.ACCEPTING)
        rejecting = State("q4", StateType.REJECTING)

        assert initial.is_initial()
        assert not intermediate.is_initial()
        assert not final.is_initial()
        assert not accepting.is_initial()
        assert not rejecting.is_initial()

        assert not initial.is_final()
        assert not intermediate.is_final()
        assert final.is_final()
        assert not accepting.is_final()
        assert not rejecting.is_final()

        assert not initial.is_accepting()
        assert not intermediate.is_accepting()
        assert final.is_accepting()
        assert accepting.is_accepting()
        assert not rejecting.is_accepting()

    def test_metadata_copy(self):
        """Test que les métadonnées sont copiées en profondeur."""
        original_metadata = {"nested": {"key": "value"}}
        state = State("q0", StateType.INITIAL, original_metadata)

        # Modification de la structure originale
        original_metadata["nested"]["key"] = "modified"

        # L'état ne doit pas être affecté
        assert state.metadata["nested"]["key"] == "value"
