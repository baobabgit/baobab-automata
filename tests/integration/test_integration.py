"""
Tests d'intégration pour Baobab Automata.

Ce module contient les tests d'intégration pour vérifier que les
différents composants fonctionnent correctement ensemble.
"""

import pytest
from baobab_automata.implementations.state import State
from baobab_automata.implementations.transition import Transition
from baobab_automata.interfaces.state import StateType
from baobab_automata.interfaces.transition import TransitionType


class TestIntegration:
    """Tests d'intégration."""
    
    def test_state_transition_workflow(self):
        """Test le workflow complet état-transition."""
        # Création d'états
        initial_state = State("q0", StateType.INITIAL)
        intermediate_state = State("q1", StateType.INTERMEDIATE)
        final_state = State("q2", StateType.FINAL)
        
        # Création de transitions
        transition1 = Transition(
            _source_state=initial_state,
            _target_state=intermediate_state,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        transition2 = Transition(
            _source_state=intermediate_state,
            _target_state=final_state,
            _symbol="b",
            _transition_type=TransitionType.SYMBOL
        )
        
        # Test du workflow
        assert transition1.source_state == initial_state
        assert transition1.target_state == intermediate_state
        assert transition2.source_state == intermediate_state
        assert transition2.target_state == final_state
        
        # Test de l'applicabilité
        assert transition1.is_applicable("a", {}) is True
        assert transition1.is_applicable("b", {}) is False
        assert transition2.is_applicable("b", {}) is True
        assert transition2.is_applicable("a", {}) is False
    
    def test_complex_automaton_workflow(self):
        """Test un workflow d'automate complexe."""
        # Création d'un automate simple avec plusieurs états et transitions
        states = {
            "q0": State("q0", StateType.INITIAL),
            "q1": State("q1", StateType.INTERMEDIATE),
            "q2": State("q2", StateType.INTERMEDIATE),
            "q3": State("q3", StateType.FINAL),
        }
        
        transitions = [
            Transition(
                _source_state=states["q0"],
                _target_state=states["q1"],
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            ),
            Transition(
                _source_state=states["q1"],
                _target_state=states["q2"],
                _symbol="b",
                _transition_type=TransitionType.SYMBOL
            ),
            Transition(
                _source_state=states["q2"],
                _target_state=states["q3"],
                _symbol="c",
                _transition_type=TransitionType.SYMBOL
            ),
            # Transition epsilon
            Transition(
                _source_state=states["q1"],
                _target_state=states["q3"],
                _symbol=None,
                _transition_type=TransitionType.EPSILON
            ),
        ]
        
        # Test de la structure
        assert len(states) == 4
        assert len(transitions) == 4
        
        # Test des propriétés des états
        assert states["q0"].is_initial() is True
        assert states["q3"].is_final() is True
        assert states["q1"].is_accepting() is False
        assert states["q2"].is_accepting() is False
        
        # Test des transitions
        symbol_transitions = [t for t in transitions if t.symbol is not None]
        epsilon_transitions = [t for t in transitions if t.symbol is None]
        
        assert len(symbol_transitions) == 3
        assert len(epsilon_transitions) == 1
        
        # Test de l'applicabilité des transitions
        for transition in symbol_transitions:
            assert transition.is_applicable(transition.symbol, {}) is True
        
        for transition in epsilon_transitions:
            assert transition.is_applicable(None, {}) is True
    
    def test_metadata_workflow(self):
        """Test le workflow de gestion des métadonnées."""
        # Création d'états avec métadonnées
        state_with_metadata = State(
            "q0",
            StateType.INTERMEDIATE,
            {"description": "Test state", "priority": 1}
        )
        
        # Test de récupération des métadonnées
        assert state_with_metadata.get_metadata("description") == "Test state"
        assert state_with_metadata.get_metadata("priority") == 1
        assert state_with_metadata.get_metadata("nonexistent") is None
        assert state_with_metadata.get_metadata("nonexistent", "default") == "default"
        
        # Test de l'immutabilité des métadonnées
        metadata = state_with_metadata.metadata
        with pytest.raises(TypeError):
            metadata["new_key"] = "new_value"
    
    def test_conditions_and_actions_workflow(self):
        """Test le workflow de conditions et actions."""
        # Création d'une transition avec conditions et actions
        source_state = State("q0", StateType.INITIAL)
        target_state = State("q1", StateType.FINAL)
        
        transition = Transition(
            _source_state=source_state,
            _target_state=target_state,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions={"stack_top": "A", "counter": 5},
            _actions={"stack_push": "B", "counter_increment": 1}
        )
        
        # Test des conditions
        valid_context = {"stack_top": "A", "counter": 5}
        invalid_context = {"stack_top": "B", "counter": 5}
        
        assert transition.is_applicable("a", valid_context) is True
        assert transition.is_applicable("a", invalid_context) is False
        
        # Test des actions
        initial_context = {"existing": "value"}
        new_context = transition.execute(initial_context)
        
        assert new_context["stack_push"] == "B"
        assert new_context["counter_increment"] == 1
        assert new_context["existing"] == "value"  # Contexte original préservé
    
    def test_epsilon_transition_workflow(self):
        """Test le workflow des transitions epsilon."""
        # Création d'états
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q1", StateType.INTERMEDIATE)
        state3 = State("q2", StateType.FINAL)
        
        # Création de transitions epsilon
        epsilon_transition1 = Transition(
            _source_state=state1,
            _target_state=state2,
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        epsilon_transition2 = Transition(
            _source_state=state2,
            _target_state=state3,
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        # Test de l'applicabilité
        assert epsilon_transition1.is_applicable(None, {}) is True
        assert epsilon_transition2.is_applicable(None, {}) is True
        
        # Test de l'exécution
        context1 = {"step": 1}
        context2 = epsilon_transition1.execute(context1)
        context3 = epsilon_transition2.execute(context2)
        
        assert context3["step"] == 1  # Contexte préservé
    
    def test_state_equality_workflow(self):
        """Test le workflow de comparaison d'états."""
        # Création d'états identiques
        state1 = State("q0", StateType.INITIAL)
        state2 = State("q0", StateType.INITIAL)
        state3 = State("q1", StateType.INITIAL)
        
        # Test d'égalité
        assert state1 == state2
        assert state1 != state3
        assert state1 != "not_a_state"
        
        # Test dans un set
        states_set = {state1, state2, state3}
        assert len(states_set) == 2  # state1 et state2 sont identiques
    
    def test_transition_equality_workflow(self):
        """Test le workflow de comparaison de transitions."""
        # Création d'états
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        
        # Création de transitions identiques
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
        
        # Test d'égalité
        assert transition1 == transition2
        assert transition1 != transition3
        assert transition1 != "not_a_transition"
        
        # Test dans un set
        transitions_set = {transition1, transition2, transition3}
        assert len(transitions_set) == 2  # transition1 et transition2 sont identiques
    
    def test_string_representation_workflow(self):
        """Test le workflow de représentation string."""
        # Création d'états et transitions
        state = State("q0", StateType.INITIAL)
        transition = Transition(
            _source_state=state,
            _target_state=State("q1", StateType.FINAL),
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        # Test des représentations string
        state_str = str(state)
        state_repr = repr(state)
        transition_str = str(transition)
        
        assert "q0" in state_str
        assert "INITIAL" in state_repr
        assert "q0" in transition_str
        assert "q1" in transition_str
        assert "a" in transition_str
    
    def test_complex_metadata_workflow(self):
        """Test le workflow avec des métadonnées complexes."""
        # Création d'un état avec des métadonnées complexes
        complex_metadata = {
            "description": "Complex state",
            "nested": {"key": "value", "number": 42},
            "list": [1, 2, 3, {"nested": "item"}],
            "boolean": True,
            "number": 3.14,
        }
        
        state = State("q0", StateType.INTERMEDIATE, complex_metadata)
        
        # Test de récupération des métadonnées complexes
        assert state.get_metadata("description") == "Complex state"
        assert state.get_metadata("nested") == {"key": "value", "number": 42}
        assert state.get_metadata("list") == [1, 2, 3, {"nested": "item"}]
        assert state.get_metadata("boolean") is True
        assert state.get_metadata("number") == 3.14
        
        # Test de l'immutabilité
        metadata = state.metadata
        with pytest.raises(TypeError):
            metadata["new_key"] = "new_value"
    
    def test_error_handling_workflow(self):
        """Test le workflow de gestion d'erreurs."""
        # Test d'ajout de métadonnées sur un état immuable
        state = State("q0", StateType.INITIAL)
        
        with pytest.raises(NotImplementedError):
            state.add_metadata("key", "value")
        
        # Test de modification des métadonnées
        metadata = state.metadata
        with pytest.raises(TypeError):
            metadata["key"] = "value"
    
    def test_performance_integration(self):
        """Test d'intégration de performance."""
        # Création d'un grand nombre d'objets
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(100)]
        transitions = []
        
        for i in range(100):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            )
            transitions.append(transition)
        
        # Test des opérations de base
        for state in states:
            assert state.identifier.startswith("q")
            assert state.state_type == StateType.INTERMEDIATE
            assert not state.is_initial()
            assert not state.is_final()
            assert not state.is_accepting()
        
        for transition in transitions:
            assert transition.symbol == "a"
            assert transition.transition_type == TransitionType.SYMBOL
            assert transition.is_applicable("a", {}) is True
            assert transition.is_applicable("b", {}) is False