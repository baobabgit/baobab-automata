"""
Tests unitaires pour les transitions d'automates.

Ce module contient les tests unitaires pour l'interface ITransition et
l'implémentation Transition.
"""

import pytest
from baobab_automata.interfaces.state import StateType
from baobab_automata.interfaces.transition import TransitionType
from baobab_automata.implementations.state import State
from baobab_automata.implementations.transition import Transition


class TestTransition:
    """Tests pour la classe Transition."""
    
    def test_transition_creation(self, sample_states):
        """Test la création d'une transition."""
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        assert transition.source_state == sample_states["initial"]
        assert transition.target_state == sample_states["final"]
        assert transition.symbol == "a"
        assert transition.transition_type == TransitionType.SYMBOL
    
    def test_epsilon_transition(self, sample_states):
        """Test la création d'une transition epsilon."""
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        assert transition.symbol is None
        assert transition.transition_type == TransitionType.EPSILON
    
    def test_transition_with_conditions_and_actions(self, sample_states):
        """Test la création d'une transition avec conditions et actions."""
        conditions = {"stack_top": "A"}
        actions = {"stack_push": "B"}
        
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=conditions,
            _actions=actions
        )
        
        assert transition.conditions == conditions
        assert transition.actions == actions
    
    def test_is_applicable(self, sample_states):
        """Test la méthode is_applicable."""
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        # Test avec symbole correct
        assert transition.is_applicable("a", {}) is True
        
        # Test avec symbole incorrect
        assert transition.is_applicable("b", {}) is False
        
        # Test avec conditions
        transition_with_conditions = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions={"stack_top": "A"}
        )
        
        assert transition_with_conditions.is_applicable("a", {"stack_top": "A"}) is True
        assert transition_with_conditions.is_applicable("a", {"stack_top": "B"}) is False
    
    def test_execute(self, sample_states):
        """Test la méthode execute."""
        actions = {"stack_push": "B", "counter": 1}
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _actions=actions
        )
        
        context = {"stack": ["A"]}
        new_context = transition.execute(context)
        
        assert new_context["stack_push"] == "B"
        assert new_context["counter"] == 1
        assert "stack" in new_context  # Contexte original préservé
    
    def test_equality(self, sample_states):
        """Test l'égalité entre transitions."""
        transition1 = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        transition2 = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        transition3 = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="b",
            _transition_type=TransitionType.SYMBOL
        )
        
        assert transition1 == transition2
        assert transition1 != transition3
        assert transition1 != "not_a_transition"
    
    def test_hash(self, sample_states):
        """Test le hash des transitions."""
        transition1 = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        transition2 = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        transition3 = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="b",
            _transition_type=TransitionType.SYMBOL
        )
        
        assert hash(transition1) == hash(transition2)
        assert hash(transition1) != hash(transition3)
        
        # Test dans un set
        transitions_set = {transition1, transition2, transition3}
        assert len(transitions_set) == 2  # transition1 et transition2 sont identiques
    
    def test_string_representation(self, sample_states):
        """Test la représentation string des transitions."""
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        assert "q0" in str(transition)
        assert "q2" in str(transition)
        assert "a" in str(transition)
        
        # Test transition epsilon
        epsilon_transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        assert "ε" in str(epsilon_transition)
    
    def test_immutability(self, sample_states):
        """Test l'immutabilité de la transition."""
        conditions = {"key": "value"}
        actions = {"action": "value"}
        
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=conditions,
            _actions=actions
        )
        
        # Modification des dictionnaires originaux ne doit pas affecter la transition
        conditions["key"] = "new_value"
        actions["action"] = "new_value"
        
        assert transition.conditions["key"] == "value"
        assert transition.actions["action"] == "value"
        
        # La transition ne doit pas être modifiable
        with pytest.raises(AttributeError):
            transition._symbol = "b"
    
    def test_conditions_and_actions_immutability(self, sample_states):
        """Test l'immutabilité des conditions et actions."""
        conditions = {"key": "value"}
        actions = {"action": "value"}
        
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=conditions,
            _actions=actions
        )
        
        # Les conditions et actions retournées doivent être immuables
        returned_conditions = transition.conditions
        returned_actions = transition.actions
        
        with pytest.raises(TypeError):
            returned_conditions["new_key"] = "new_value"
        
        with pytest.raises(TypeError):
            returned_actions["new_action"] = "new_value"
    
    def test_all_transition_types(self, sample_states):
        """Test tous les types de transitions."""
        transition_types = [
            TransitionType.SYMBOL,
            TransitionType.EPSILON,
            TransitionType.STACK_PUSH,
            TransitionType.STACK_POP,
            TransitionType.STACK_READ,
            TransitionType.TAPE_READ,
            TransitionType.TAPE_WRITE,
            TransitionType.TAPE_MOVE,
        ]
        
        for transition_type in transition_types:
            transition = Transition(
                _source_state=sample_states["initial"],
                _target_state=sample_states["final"],
                _symbol="a" if transition_type == TransitionType.SYMBOL else None,
                _transition_type=transition_type
            )
            assert transition.transition_type == transition_type
    
    def test_complex_conditions_and_actions(self, sample_states):
        """Test des conditions et actions complexes."""
        complex_conditions = {
            "stack_top": "A",
            "counter": 5,
            "nested": {"key": "value"},
            "list": [1, 2, 3],
        }
        
        complex_actions = {
            "stack_push": "B",
            "counter_increment": 1,
            "nested_action": {"result": "success"},
            "list_append": 4,
        }
        
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=complex_conditions,
            _actions=complex_actions
        )
        
        assert transition.conditions == complex_conditions
        assert transition.actions == complex_actions
    
    def test_is_applicable_with_complex_conditions(self, sample_states):
        """Test is_applicable avec des conditions complexes."""
        conditions = {
            "stack_top": "A",
            "counter": 5,
            "flag": True,
        }
        
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=conditions
        )
        
        # Contexte qui satisfait toutes les conditions
        valid_context = {
            "stack_top": "A",
            "counter": 5,
            "flag": True,
        }
        assert transition.is_applicable("a", valid_context) is True
        
        # Contexte qui ne satisfait pas toutes les conditions
        invalid_contexts = [
            {"stack_top": "B", "counter": 5, "flag": True},
            {"stack_top": "A", "counter": 4, "flag": True},
            {"stack_top": "A", "counter": 5, "flag": False},
            {"stack_top": "A", "counter": 5},  # Manque 'flag'
        ]
        
        for invalid_context in invalid_contexts:
            assert transition.is_applicable("a", invalid_context) is False
    
    def test_execute_with_complex_actions(self, sample_states):
        """Test execute avec des actions complexes."""
        actions = {
            "stack_push": "B",
            "counter_increment": 1,
            "new_flag": True,
            "nested": {"key": "value"},
        }
        
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _actions=actions
        )
        
        context = {"existing": "value"}
        new_context = transition.execute(context)
        
        # Vérifier que les actions ont été appliquées
        assert new_context["stack_push"] == "B"
        assert new_context["counter_increment"] == 1
        assert new_context["new_flag"] is True
        assert new_context["nested"] == {"key": "value"}
        
        # Vérifier que le contexte original est préservé
        assert new_context["existing"] == "value"