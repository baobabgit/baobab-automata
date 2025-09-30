"""Tests unitaires pour les transitions d'automates."""
import pytest
from baobab_automata.interfaces.transition import TransitionType
from baobab_automata.implementations.state import State
from baobab_automata.implementations.transition import Transition
from baobab_automata.interfaces.state import StateType

@pytest.mark.unit
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
    
    def test_is_applicable_epsilon(self, sample_states):
        """Test la méthode is_applicable pour les transitions epsilon."""
        epsilon_transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        # Transition epsilon doit être applicable avec symbol=None
        assert epsilon_transition.is_applicable(None, {}) is True
        assert epsilon_transition.is_applicable("a", {}) is False
    
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
    
    def test_execute_empty_actions(self, sample_states):
        """Test la méthode execute avec des actions vides."""
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        context = {"original": "value"}
        new_context = transition.execute(context)
        
        assert new_context == context  # Contexte inchangé
    
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
    
    def test_different_transition_types(self, sample_states):
        """Test la création de transitions avec différents types."""
        symbol_transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        epsilon_transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        stack_push_transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.STACK_PUSH
        )
        
        assert symbol_transition.transition_type == TransitionType.SYMBOL
        assert epsilon_transition.transition_type == TransitionType.EPSILON
        assert stack_push_transition.transition_type == TransitionType.STACK_PUSH
    
    def test_immutability(self, sample_states):
        """Test l'immutabilité des transitions."""
        conditions = {"key": "value"}
        actions = {"action": "result"}
        
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=conditions,
            _actions=actions
        )
        
        # Modification des structures originales
        conditions["key"] = "modified"
        actions["action"] = "modified"
        
        # La transition ne doit pas être affectée
        assert transition.conditions["key"] == "value"
        assert transition.actions["action"] == "result"
    
    def test_conditions_and_actions_copy(self, sample_states):
        """Test que les conditions et actions sont copiées en profondeur."""
        conditions = {"nested": {"key": "value"}}
        actions = {"nested": {"action": "result"}}
        
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=conditions,
            _actions=actions
        )
        
        # Modification des structures originales
        conditions["nested"]["key"] = "modified"
        actions["nested"]["action"] = "modified"
        
        # La transition ne doit pas être affectée
        assert transition.conditions["nested"]["key"] == "value"
        assert transition.actions["nested"]["action"] == "result"
    
    def test_is_applicable_with_complex_conditions(self, sample_states):
        """Test is_applicable avec des conditions complexes."""
        conditions = {"stack_top": "A", "counter": 5, "flag": True}
        
        transition = Transition(
            _source_state=sample_states["initial"],
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=conditions
        )
        
        # Contexte qui satisfait toutes les conditions
        valid_context = {"stack_top": "A", "counter": 5, "flag": True}
        assert transition.is_applicable("a", valid_context) is True
        
        # Contexte qui ne satisfait pas toutes les conditions
        invalid_context = {"stack_top": "A", "counter": 5, "flag": False}
        assert transition.is_applicable("a", invalid_context) is False
        
        # Contexte partiel
        partial_context = {"stack_top": "A"}
        assert transition.is_applicable("a", partial_context) is False