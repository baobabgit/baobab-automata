"""
Tests unitaires pour les états d'automates.

Ce module contient les tests unitaires pour l'interface IState et
l'implémentation State.
"""

import pytest
from baobab_automata.interfaces.state import StateType
from baobab_automata.implementations.state import State


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
    
    def test_add_metadata_raises_error(self):
        """Test que add_metadata lève une erreur sur un état immuable."""
        state = State("q0", StateType.INITIAL)
        
        with pytest.raises(NotImplementedError):
            state.add_metadata("key", "value")
    
    @pytest.mark.parametrize("identifier,state_type,expected_valid", [
        ("q0", StateType.INITIAL, True),
        ("", StateType.INITIAL, True),  # Identifiant vide autorisé
    ])
    def test_validation(self, identifier, state_type, expected_valid):
        """Test la validation des états."""
        if expected_valid:
            state = State(identifier, state_type)
            assert state.identifier == identifier
    
    def test_immutability(self):
        """Test l'immutabilité de l'état."""
        metadata = {"key": "value"}
        state = State("q0", StateType.INITIAL, metadata)
        
        # Modification du dictionnaire original ne doit pas affecter l'état
        metadata["key"] = "new_value"
        assert state.get_metadata("key") == "value"
        
        # L'état ne doit pas être modifiable
        with pytest.raises(AttributeError):
            state._identifier = "q1"
    
    def test_metadata_immutability(self):
        """Test l'immutabilité des métadonnées."""
        metadata = {"key": "value"}
        state = State("q0", StateType.INITIAL, metadata)
        
        # Les métadonnées retournées doivent être immuables
        returned_metadata = state.metadata
        with pytest.raises(TypeError):
            returned_metadata["new_key"] = "new_value"
    
    def test_all_state_types(self):
        """Test tous les types d'états."""
        state_types = [
            StateType.INITIAL,
            StateType.FINAL,
            StateType.INTERMEDIATE,
            StateType.ACCEPTING,
            StateType.REJECTING,
        ]
        
        for state_type in state_types:
            state = State("q0", state_type)
            assert state.state_type == state_type
            assert state.identifier == "q0"
    
    def test_state_with_complex_metadata(self):
        """Test un état avec des métadonnées complexes."""
        complex_metadata = {
            "description": "Complex state",
            "nested": {"key": "value"},
            "list": [1, 2, 3],
            "number": 42,
            "boolean": True,
        }
        
        state = State("q0", StateType.INTERMEDIATE, complex_metadata)
        
        assert state.get_metadata("description") == "Complex state"
        assert state.get_metadata("nested") == {"key": "value"}
        assert state.get_metadata("list") == [1, 2, 3]
        assert state.get_metadata("number") == 42
        assert state.get_metadata("boolean") is True