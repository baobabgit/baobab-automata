"""
Tests unitaires pour l'implémentation State.

Ce module contient les tests unitaires pour la classe State
qui implémente l'interface IState.
"""

import pytest
from baobab_automata.interfaces.state import StateType
from baobab_automata.implementations.state import State


class TestStateImplementation:
    """Tests pour l'implémentation State."""

    def test_state_creation_basic(self):
        """Test la création basique d'un état."""
        state = State("q0", StateType.INITIAL)

        assert state.identifier == "q0"
        assert state.state_type == StateType.INITIAL
        assert state.metadata == {}

    def test_state_creation_with_metadata(self):
        """Test la création d'un état avec métadonnées."""
        metadata = {"description": "Test state", "priority": 1}
        state = State("q0", StateType.INITIAL, metadata)

        assert state.identifier == "q0"
        assert state.state_type == StateType.INITIAL
        assert state.metadata == metadata

    def test_state_immutability(self):
        """Test l'immutabilité de l'état."""
        metadata = {"key": "value"}
        state = State("q0", StateType.INITIAL, metadata)

        # Modification du dictionnaire original ne doit pas affecter l'état
        metadata["key"] = "new_value"
        assert state.get_metadata("key") == "value"

        # L'état ne doit pas être modifiable
        with pytest.raises(AttributeError):
            state._identifier = "q1"

    def test_state_metadata_immutability(self):
        """Test l'immutabilité des métadonnées."""
        metadata = {"key": "value"}
        state = State("q0", StateType.INITIAL, metadata)

        # Les métadonnées retournées doivent être immuables
        returned_metadata = state.metadata
        with pytest.raises(TypeError):
            returned_metadata["new_key"] = "new_value"

    def test_state_type_methods(self):
        """Test les méthodes de type d'état."""
        # Test état initial
        initial_state = State("q0", StateType.INITIAL)
        assert initial_state.is_initial() is True
        assert initial_state.is_final() is False
        assert initial_state.is_accepting() is False

        # Test état final
        final_state = State("q1", StateType.FINAL)
        assert final_state.is_initial() is False
        assert final_state.is_final() is True
        assert final_state.is_accepting() is True

        # Test état intermédiaire
        intermediate_state = State("q2", StateType.INTERMEDIATE)
        assert intermediate_state.is_initial() is False
        assert intermediate_state.is_final() is False
        assert intermediate_state.is_accepting() is False

        # Test état acceptant
        accepting_state = State("q3", StateType.ACCEPTING)
        assert accepting_state.is_initial() is False
        assert accepting_state.is_final() is False
        assert accepting_state.is_accepting() is True

        # Test état rejetant
        rejecting_state = State("q4", StateType.REJECTING)
        assert rejecting_state.is_initial() is False
        assert rejecting_state.is_final() is False
        assert rejecting_state.is_accepting() is False

    def test_state_equality(self):
        """Test l'égalité entre états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)
        state4 = State("q0", StateType.FINAL)

        # États identiques
        assert state1 == state2
        assert hash(state1) == hash(state2)

        # États différents par identifiant
        assert state1 != state3
        assert hash(state1) != hash(state3)

        # États différents par type
        assert state1 != state4
        assert hash(state1) != hash(state4)

        # Comparaison avec un objet non-état
        assert state1 != "not_a_state"
        assert state1 != 42
        assert state1 != None

    def test_state_hash(self):
        """Test le hash des états."""
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)

        # États identiques ont le même hash
        assert hash(state1) == hash(state2)

        # États différents ont des hash différents
        assert hash(state1) != hash(state3)

        # Test dans un set
        states_set = {state1, state2, state3}
        assert len(states_set) == 2  # state1 et state2 sont identiques

    def test_state_string_representation(self):
        """Test la représentation string des états."""
        state = State("q0", StateType.INITIAL)

        # Test str()
        assert str(state) == "State(q0)"

        # Test repr()
        repr_str = repr(state)
        assert "State" in repr_str
        assert "q0" in repr_str
        assert "INITIAL" in repr_str

    def test_state_metadata_operations(self):
        """Test les opérations sur les métadonnées."""
        metadata = {"key1": "value1", "key2": 42, "key3": [1, 2, 3]}
        state = State("q0", StateType.INITIAL, metadata)

        # Test get_metadata avec clé existante
        assert state.get_metadata("key1") == "value1"
        assert state.get_metadata("key2") == 42
        assert state.get_metadata("key3") == [1, 2, 3]

        # Test get_metadata avec clé inexistante
        assert state.get_metadata("nonexistent") is None

        # Test get_metadata avec valeur par défaut
        assert state.get_metadata("nonexistent", "default") == "default"
        assert state.get_metadata("nonexistent", 0) == 0

    def test_state_add_metadata_error(self):
        """Test que add_metadata lève une erreur sur un état immuable."""
        state = State("q0", StateType.INITIAL)

        with pytest.raises(NotImplementedError) as exc_info:
            state.add_metadata("key", "value")

        assert "Cannot modify frozen dataclass" in str(exc_info.value)
        assert "StateBuilder" in str(exc_info.value)

    def test_state_with_complex_metadata(self):
        """Test un état avec des métadonnées complexes."""
        complex_metadata = {
            "description": "Complex state",
            "nested": {"key": "value", "number": 42},
            "list": [1, 2, 3, {"nested": "item"}],
            "boolean": True,
            "number": 3.14,
            "none": None,
        }

        state = State("q0", StateType.INTERMEDIATE, complex_metadata)

        # Test de récupération des métadonnées complexes
        assert state.get_metadata("description") == "Complex state"
        assert state.get_metadata("nested") == {"key": "value", "number": 42}
        assert state.get_metadata("list") == [1, 2, 3, {"nested": "item"}]
        assert state.get_metadata("boolean") is True
        assert state.get_metadata("number") == 3.14
        assert state.get_metadata("none") is None

    def test_state_deep_copy_metadata(self):
        """Test que les métadonnées sont copiées en profondeur."""
        original_metadata = {
            "nested": {"key": "value"},
            "list": [1, 2, 3],
        }

        state = State("q0", StateType.INITIAL, original_metadata)

        # Modification du dictionnaire original
        original_metadata["nested"]["key"] = "modified"
        original_metadata["list"].append(4)

        # L'état ne doit pas être affecté
        assert state.get_metadata("nested") == {"key": "value"}
        assert state.get_metadata("list") == [1, 2, 3]

    def test_state_all_types(self):
        """Test tous les types d'états."""
        state_types = [
            StateType.INITIAL,
            StateType.FINAL,
            StateType.INTERMEDIATE,
            StateType.ACCEPTING,
            StateType.REJECTING,
        ]

        for i, state_type in enumerate(state_types):
            state = State(f"q{i}", state_type)
            assert state.identifier == f"q{i}"
            assert state.state_type == state_type
            assert state.metadata == {}

    def test_state_edge_cases(self):
        """Test les cas limites des états."""
        # Identifiant vide
        empty_id_state = State("", StateType.INITIAL)
        assert empty_id_state.identifier == ""

        # Identifiant avec caractères spéciaux
        special_id_state = State("q0-1_2", StateType.INITIAL)
        assert special_id_state.identifier == "q0-1_2"

        # Métadonnées vides
        empty_metadata_state = State("q0", StateType.INITIAL, {})
        assert empty_metadata_state.metadata == {}

        # Métadonnées None
        none_metadata_state = State("q0", StateType.INITIAL, None)
        assert none_metadata_state.metadata == {}

    def test_state_consistency(self):
        """Test la cohérence de l'état."""
        state = State("q0", StateType.INITIAL, {"key": "value"})

        # L'identifiant ne doit pas changer
        assert state.identifier == "q0"

        # Le type ne doit pas changer
        assert state.state_type == StateType.INITIAL

        # Les métadonnées ne doivent pas changer
        assert state.metadata == {"key": "value"}

        # Les méthodes de type doivent être cohérentes
        assert state.is_initial() is True
        assert state.is_final() is False
        assert state.is_accepting() is False

    def test_state_serialization(self):
        """Test la sérialisation de l'état."""
        state = State("q0", StateType.INITIAL, {"key": "value"})

        # Test que l'état peut être utilisé dans des structures de données
        states_list = [state]
        states_dict = {state: "value"}
        states_set = {state}

        assert state in states_list
        assert state in states_dict
        assert state in states_set

        # Test que l'état peut être utilisé comme clé de dictionnaire
        state_map = {state: "mapped_value"}
        assert state_map[state] == "mapped_value"
