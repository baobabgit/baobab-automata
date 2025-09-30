"""
Tests unitaires pour l'implémentation State.

Ce module teste l'implémentation concrète State de l'interface IState.
"""

import pytest

from baobab_automata.implementations.state import State
from baobab_automata.interfaces.state import StateType


class TestStateImplementation:
    """Tests pour l'implémentation State."""

    def test_state_creation_all_types(self):
        """Test de création d'états de tous les types."""
        states = [
            State("q0", StateType.INITIAL),
            State("q1", StateType.FINAL),
            State("q2", StateType.INTERMEDIATE),
            State("q3", StateType.ACCEPTING),
            State("q4", StateType.REJECTING),
        ]

        for state in states:
            assert isinstance(state, State)
            assert state.identifier.startswith("q")

    def test_state_with_metadata(self):
        """Test de création d'état avec métadonnées."""
        metadata = {
            "description": "Test state",
            "priority": 1,
            "color": "blue",
        }
        state = State("q0", StateType.INITIAL, metadata)

        assert state.metadata == metadata
        assert state.get_metadata("description") == "Test state"
        assert state.get_metadata("priority") == 1
        assert state.get_metadata("color") == "blue"

    def test_state_metadata_default_value(self):
        """Test de get_metadata avec valeur par défaut."""
        state = State("q0", StateType.INITIAL)

        assert state.get_metadata("nonexistent") is None
        assert state.get_metadata("nonexistent", "default") == "default"
        assert state.get_metadata("nonexistent", 42) == 42

    def test_state_type_checks(self):
        """Test des vérifications de type d'état."""
        # État initial
        initial_state = State("q0", StateType.INITIAL)
        assert initial_state.is_initial() is True
        assert initial_state.is_final() is False
        assert initial_state.is_accepting() is False

        # État final
        final_state = State("q1", StateType.FINAL)
        assert final_state.is_initial() is False
        assert final_state.is_final() is True
        assert final_state.is_accepting() is True

        # État acceptant
        accepting_state = State("q2", StateType.ACCEPTING)
        assert accepting_state.is_initial() is False
        assert accepting_state.is_final() is False
        assert accepting_state.is_accepting() is True

        # État intermédiaire
        intermediate_state = State("q3", StateType.INTERMEDIATE)
        assert intermediate_state.is_initial() is False
        assert intermediate_state.is_final() is False
        assert intermediate_state.is_accepting() is False

        # État rejetant
        rejecting_state = State("q4", StateType.REJECTING)
        assert rejecting_state.is_initial() is False
        assert rejecting_state.is_final() is False
        assert rejecting_state.is_accepting() is False

    def test_state_equality(self):
        """Test de l'égalité entre états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)
        state4 = State("q0", StateType.FINAL)

        # Même identifiant et type
        assert state1 == state2

        # Identifiants différents
        assert state1 != state3

        # Types différents mais même identifiant
        assert state1 != state4

        # Comparaison avec autre type
        assert state1 != "not_a_state"
        assert state1 != 42

    def test_state_hash(self):
        """Test du hachage des états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)

        # Même identifiant = même hash
        assert hash(state1) == hash(state2)

        # Identifiants différents = hash différents
        assert hash(state1) != hash(state3)

        # Hash stable
        assert hash(state1) == hash(state1)

    def test_state_in_sets(self):
        """Test d'utilisation des états dans des sets."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.FINAL)

        state_set = {state1, state2, state3}

        # Les états identiques ne doivent apparaître qu'une fois
        assert len(state_set) == 2
        assert state1 in state_set
        assert state2 in state_set
        assert state3 in state_set

    def test_state_string_representations(self):
        """Test des représentations string des états."""
        state = State("q0", StateType.INITIAL, {"description": "Test"})

        # Représentation simple
        assert str(state) == "State(q0)"

        # Représentation détaillée
        expected_repr = "State(identifier='q0', type=StateType.INITIAL)"
        assert repr(state) == expected_repr

    def test_state_immutability(self):
        """Test de l'immutabilité des états."""
        state = State("q0", StateType.INITIAL)

        # Vérifier que l'état est hashable
        assert hash(state) is not None

        # Vérifier que les attributs ne peuvent pas être modifiés
        with pytest.raises(AttributeError):
            state.identifier = "q1"

        with pytest.raises(AttributeError):
            state.state_type = StateType.FINAL

        with pytest.raises(AttributeError):
            state.metadata = {"new": "value"}

    def test_state_metadata_immutability(self):
        """Test de l'immutabilité des métadonnées."""
        metadata = {"key": "value"}
        state = State("q0", StateType.INITIAL, metadata)

        # Les métadonnées ne doivent pas pouvoir être modifiées
        with pytest.raises(TypeError):
            state.metadata["new_key"] = "new_value"

    def test_state_with_empty_metadata(self):
        """Test d'état avec métadonnées vides."""
        state = State("q0", StateType.INITIAL, {})

        assert state.metadata == {}
        assert state.get_metadata("any_key") is None
        assert state.get_metadata("any_key", "default") == "default"

    def test_state_with_none_metadata(self):
        """Test d'état avec métadonnées None."""
        state = State("q0", StateType.INITIAL, {"key": None})

        assert state.get_metadata("key") is None
        assert state.get_metadata("key", "default") is None
        assert state.get_metadata("nonexistent", "default") == "default"
