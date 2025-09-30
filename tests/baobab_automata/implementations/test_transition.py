"""
Tests unitaires pour l'implémentation Transition.

Ce module contient les tests unitaires pour la classe Transition
qui implémente l'interface ITransition.
"""

import pytest
from baobab_automata.interfaces.state import StateType
from baobab_automata.interfaces.transition import TransitionType
from baobab_automata.implementations.state import State
from baobab_automata.implementations.transition import Transition


class TestTransitionImplementation:
    """Tests pour l'implémentation Transition."""
    
    def test_transition_creation_basic(self):
        """Test la création basique d'une transition."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        assert transition.source_state == source
        assert transition.target_state == target
        assert transition.symbol == "a"
        assert transition.transition_type == TransitionType.SYMBOL
        assert transition.conditions == {}
        assert transition.actions == {}
    
    def test_transition_creation_with_conditions_and_actions(self):
        """Test la création d'une transition avec conditions et actions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        conditions = {"stack_top": "A", "counter": 5}
        actions = {"stack_push": "B", "counter_increment": 1}
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=conditions,
            _actions=actions
        )
        
        assert transition.conditions == conditions
        assert transition.actions == actions
    
    def test_epsilon_transition(self):
        """Test la création d'une transition epsilon."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        assert transition.symbol is None
        assert transition.transition_type == TransitionType.EPSILON
    
    def test_transition_immutability(self):
        """Test l'immutabilité de la transition."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        conditions = {"key": "value"}
        actions = {"action": "value"}
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
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
    
    def test_transition_conditions_and_actions_immutability(self):
        """Test l'immutabilité des conditions et actions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        conditions = {"key": "value"}
        actions = {"action": "value"}
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
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
    
    def test_transition_is_applicable(self):
        """Test la méthode is_applicable."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        # Transition simple
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        # Test avec symbole correct
        assert transition.is_applicable("a", {}) is True
        
        # Test avec symbole incorrect
        assert transition.is_applicable("b", {}) is False
        
        # Test avec symbole None
        assert transition.is_applicable(None, {}) is False
    
    def test_transition_is_applicable_with_conditions(self):
        """Test is_applicable avec des conditions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        # Transition avec conditions
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions={"stack_top": "A", "counter": 5}
        )
        
        # Contexte qui satisfait toutes les conditions
        valid_context = {"stack_top": "A", "counter": 5}
        assert transition.is_applicable("a", valid_context) is True
        
        # Contexte qui ne satisfait pas toutes les conditions
        invalid_contexts = [
            {"stack_top": "B", "counter": 5},  # Mauvaise pile
            {"stack_top": "A", "counter": 4},  # Mauvais compteur
            {"stack_top": "A"},  # Manque counter
            {"counter": 5},  # Manque stack_top
            {},  # Contexte vide
        ]
        
        for invalid_context in invalid_contexts:
            assert transition.is_applicable("a", invalid_context) is False
    
    def test_transition_is_applicable_epsilon(self):
        """Test is_applicable pour les transitions epsilon."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        # Transition epsilon
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        # Test avec symbole None
        assert transition.is_applicable(None, {}) is True
        
        # Test avec symbole non-None
        assert transition.is_applicable("a", {}) is False
    
    def test_transition_execute(self):
        """Test la méthode execute."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        actions = {"stack_push": "B", "counter": 1}
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _actions=actions
        )
        
        context = {"stack": ["A"]}
        new_context = transition.execute(context)
        
        # Vérifier que les actions ont été appliquées
        assert new_context["stack_push"] == "B"
        assert new_context["counter"] == 1
        
        # Vérifier que le contexte original est préservé
        assert new_context["stack"] == ["A"]
    
    def test_transition_execute_with_complex_actions(self):
        """Test execute avec des actions complexes."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        actions = {
            "stack_push": "B",
            "counter_increment": 1,
            "new_flag": True,
            "nested": {"key": "value"},
        }
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
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
    
    def test_transition_equality(self):
        """Test l'égalité entre transitions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        # Transitions identiques
        transition1 = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        transition2 = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        assert transition1 == transition2
        assert hash(transition1) == hash(transition2)
        
        # Transitions différentes par symbole
        transition3 = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="b",
            _transition_type=TransitionType.SYMBOL
        )
        
        assert transition1 != transition3
        assert hash(transition1) != hash(transition3)
        
        # Transitions différentes par type
        transition4 = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.EPSILON
        )
        
        assert transition1 != transition4
        assert hash(transition1) != hash(transition4)
        
        # Comparaison avec un objet non-transition
        assert transition1 != "not_a_transition"
        assert transition1 != 42
        assert transition1 != None
    
    def test_transition_hash(self):
        """Test le hash des transitions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        transition1 = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        transition2 = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        transition3 = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="b",
            _transition_type=TransitionType.SYMBOL
        )
        
        # Transitions identiques ont le même hash
        assert hash(transition1) == hash(transition2)
        
        # Transitions différentes ont des hash différents
        assert hash(transition1) != hash(transition3)
        
        # Test dans un set
        transitions_set = {transition1, transition2, transition3}
        assert len(transitions_set) == 2  # transition1 et transition2 sont identiques
    
    def test_transition_string_representation(self):
        """Test la représentation string des transitions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        # Transition symbolique
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        str_repr = str(transition)
        assert "q0" in str_repr
        assert "q1" in str_repr
        assert "a" in str_repr
        
        # Transition epsilon
        epsilon_transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        epsilon_str = str(epsilon_transition)
        assert "q0" in epsilon_str
        assert "q1" in epsilon_str
        assert "ε" in epsilon_str
    
    def test_transition_all_types(self):
        """Test tous les types de transitions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
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
            symbol = "a" if transition_type == TransitionType.SYMBOL else None
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol=symbol,
                _transition_type=transition_type
            )
            assert transition.transition_type == transition_type
            assert transition.symbol == symbol
    
    def test_transition_deep_copy_conditions_and_actions(self):
        """Test que les conditions et actions sont copiées en profondeur."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        original_conditions = {
            "nested": {"key": "value"},
            "list": [1, 2, 3],
        }
        original_actions = {
            "nested": {"action": "value"},
            "list": [4, 5, 6],
        }
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=original_conditions,
            _actions=original_actions
        )
        
        # Modification des dictionnaires originaux
        original_conditions["nested"]["key"] = "modified"
        original_conditions["list"].append(4)
        original_actions["nested"]["action"] = "modified"
        original_actions["list"].append(7)
        
        # La transition ne doit pas être affectée
        assert transition.conditions["nested"] == {"key": "value"}
        assert transition.conditions["list"] == [1, 2, 3]
        assert transition.actions["nested"] == {"action": "value"}
        assert transition.actions["list"] == [4, 5, 6]
    
    def test_transition_edge_cases(self):
        """Test les cas limites des transitions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        # Transition avec conditions et actions vides
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions={},
            _actions={}
        )
        
        assert transition.conditions == {}
        assert transition.actions == {}
        assert transition.is_applicable("a", {}) is True
        
        # Transition avec conditions et actions None
        transition_none = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions=None,
            _actions=None
        )
        
        assert transition_none.conditions == {}
        assert transition_none.actions == {}
    
    def test_transition_consistency(self):
        """Test la cohérence de la transition."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions={"key": "value"},
            _actions={"action": "value"}
        )
        
        # Les propriétés ne doivent pas changer
        assert transition.source_state == source
        assert transition.target_state == target
        assert transition.symbol == "a"
        assert transition.transition_type == TransitionType.SYMBOL
        assert transition.conditions == {"key": "value"}
        assert transition.actions == {"action": "value"}
        
        # Les méthodes doivent être cohérentes
        assert transition.is_applicable("a", {"key": "value"}) is True
        assert transition.is_applicable("b", {"key": "value"}) is False
        assert transition.is_applicable("a", {"key": "wrong"}) is False
    
    def test_transition_serialization(self):
        """Test la sérialisation de la transition."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        transition = Transition(
            _source_state=source,
            _target_state=target,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        # Test que la transition peut être utilisée dans des structures de données
        transitions_list = [transition]
        transitions_dict = {transition: "value"}
        transitions_set = {transition}
        
        assert transition in transitions_list
        assert transition in transitions_dict
        assert transition in transitions_set
        
        # Test que la transition peut être utilisée comme clé de dictionnaire
        transition_map = {transition: "mapped_value"}
        assert transition_map[transition] == "mapped_value"