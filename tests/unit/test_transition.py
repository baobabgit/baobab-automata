"""Tests unitaires pour la classe Transition."""

import pytest
from baobab_automata.core.implementations.transition import Transition
from baobab_automata.core.implementations.state import State
from baobab_automata.core.interfaces.state import StateType
from baobab_automata.core.interfaces.transition import TransitionType


@pytest.mark.unit
class TestTransition:
    """Tests pour la classe Transition."""

    def test_transition_creation_basic(self):
        """Test la création basique d'une transition."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)
        assert transition.source_state == source
        assert transition.target_state == target
        assert transition.symbol == "a"
        assert transition.transition_type == TransitionType.SYMBOL

    def test_transition_creation_with_epsilon(self):
        """Test la création d'une transition epsilon."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, None, TransitionType.EPSILON)
        assert transition.source_state == source
        assert transition.target_state == target
        assert transition.symbol is None
        assert transition.transition_type == TransitionType.EPSILON

    def test_transition_equality_same(self):
        """Test l'égalité de deux transitions identiques."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition1 = Transition(source, target, "a", TransitionType.SYMBOL)
        transition2 = Transition(source, target, "a", TransitionType.SYMBOL)
        assert transition1 == transition2
        assert hash(transition1) == hash(transition2)

    def test_transition_equality_different(self):
        """Test l'égalité de deux transitions différentes."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition1 = Transition(source, target, "a", TransitionType.SYMBOL)
        transition2 = Transition(source, target, "b", TransitionType.SYMBOL)
        assert transition1 != transition2

    def test_transition_hash(self):
        """Test le hash d'une transition."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition1 = Transition(source, target, "a", TransitionType.SYMBOL)
        transition2 = Transition(source, target, "a", TransitionType.SYMBOL)
        assert hash(transition1) == hash(transition2)

    def test_transition_string_representation(self):
        """Test la représentation string d'une transition."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)
        str_repr = str(transition)
        assert "q0" in str_repr
        assert "q1" in str_repr
        assert "a" in str_repr

    def test_transition_epsilon_string_representation(self):
        """Test la représentation string d'une transition epsilon."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, None, TransitionType.EPSILON)
        str_repr = str(transition)
        assert "q0" in str_repr
        assert "q1" in str_repr
        assert "ε" in str_repr

    def test_transition_immutability(self):
        """Test l'immutabilité des propriétés de base."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)
        # Les propriétés ne doivent pas être modifiables
        with pytest.raises(AttributeError):
            transition.source_state = target
        with pytest.raises(AttributeError):
            transition.symbol = "b"

    def test_transition_copy(self):
        """Test la copie d'une transition."""
        import copy
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)
        copied_transition = copy.copy(transition)
        assert copied_transition == transition
        assert copied_transition is not transition

    def test_transition_serialization(self):
        """Test la sérialisation d'une transition."""
        import pickle
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)
        serialized = pickle.dumps(transition)
        deserialized = pickle.loads(serialized)
        assert deserialized == transition

    def test_transition_is_applicable(self):
        """Test la vérification d'applicabilité d'une transition."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)
        
        # Test avec le bon symbole
        assert transition.is_applicable("a", {}) is True
        # Test avec un mauvais symbole
        assert transition.is_applicable("b", {}) is False
        # Test avec None (pas de symbole)
        assert transition.is_applicable(None, {}) is False

    def test_transition_epsilon_is_applicable(self):
        """Test la vérification d'applicabilité d'une transition epsilon."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, None, TransitionType.EPSILON)
        
        # Test avec None (epsilon)
        assert transition.is_applicable(None, {}) is True
        # Test avec un symbole (pas epsilon)
        assert transition.is_applicable("a", {}) is False

    def test_transition_execute(self):
        """Test l'exécution d'une transition."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        actions = {"counter": 1, "visited": True}
        transition = Transition(source, target, "a", TransitionType.SYMBOL, {}, actions)
        
        context = {"initial": "value"}
        new_context = transition.execute(context)
        
        # Le contexte original ne doit pas être modifié
        assert context == {"initial": "value"}
        # Le nouveau contexte doit contenir les actions
        assert new_context["counter"] == 1
        assert new_context["visited"] is True
        assert new_context["initial"] == "value"

    def test_transition_conditions(self):
        """Test les conditions d'une transition."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        conditions = {"state": "ready", "count": 5}
        transition = Transition(source, target, "a", TransitionType.SYMBOL, conditions)
        
        # Test avec les bonnes conditions
        assert transition.is_applicable("a", {"state": "ready", "count": 5}) is True
        # Test avec de mauvaises conditions
        assert transition.is_applicable("a", {"state": "not_ready"}) is False
        assert transition.is_applicable("a", {"state": "ready", "count": 3}) is False

    def test_transition_equality_with_non_transition(self):
        """Test l'égalité avec un objet non-Transition."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)
        assert transition != "transition"
        assert transition != 123

    def test_transition_different_source(self):
        """Test l'égalité avec une transition ayant une source différente."""
        source1 = State("q0", StateType.INTERMEDIATE)
        source2 = State("q2", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition1 = Transition(source1, target, "a", TransitionType.SYMBOL)
        transition2 = Transition(source2, target, "a", TransitionType.SYMBOL)
        assert transition1 != transition2

    def test_transition_different_target(self):
        """Test l'égalité avec une transition ayant une cible différente."""
        source = State("q0", StateType.INTERMEDIATE)
        target1 = State("q1", StateType.INTERMEDIATE)
        target2 = State("q2", StateType.INTERMEDIATE)
        transition1 = Transition(source, target1, "a", TransitionType.SYMBOL)
        transition2 = Transition(source, target2, "a", TransitionType.SYMBOL)
        assert transition1 != transition2

    def test_transition_different_symbol(self):
        """Test l'égalité avec une transition ayant un symbole différent."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition1 = Transition(source, target, "a", TransitionType.SYMBOL)
        transition2 = Transition(source, target, "b", TransitionType.SYMBOL)
        assert transition1 != transition2

    def test_transition_different_type(self):
        """Test l'égalité avec une transition ayant un type différent."""
        source = State("q0", StateType.INTERMEDIATE)
        target = State("q1", StateType.INTERMEDIATE)
        transition1 = Transition(source, target, "a", TransitionType.SYMBOL)
        transition2 = Transition(source, target, "a", TransitionType.EPSILON)
        assert transition1 != transition2