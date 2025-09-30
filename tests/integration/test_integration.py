"""Tests d'intégration pour les workflows complets."""
import pytest
from baobab_automata.finite.dfa import DFA
from baobab_automata.interfaces.state import StateType
from baobab_automata.interfaces.transition import TransitionType
from baobab_automata.interfaces.automaton import AutomatonType
from baobab_automata.implementations.state import State
from baobab_automata.implementations.transition import Transition

@pytest.mark.integration
class TestIntegration:
    """Tests d'intégration."""
    
    def test_automaton_creation_workflow(self, sample_alphabet):
        """Test le workflow complet de création d'un automate."""
        # Création des états
        initial_state = State("q0", StateType.INITIAL)
        intermediate_state = State("q1", StateType.INTERMEDIATE)
        final_state = State("q2", StateType.FINAL)
        
        states = {initial_state, intermediate_state, final_state}
        initial_states = {initial_state}
        final_states = {final_state}
        
        # Création des transitions
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
        
        transitions = {transition1, transition2}
        
        # Création de l'automate
        dfa = DFA(states, initial_states, final_states, sample_alphabet, transitions)
        
        # Vérifications
        assert dfa.automaton_type == AutomatonType.DFA
        assert dfa.is_valid()
        assert len(dfa.states) == 3
        assert len(dfa.transitions) == 2
        
        # Vérification des transitions
        transitions_from_q0 = dfa.get_transitions_from(initial_state)
        assert len(transitions_from_q0) == 1
        assert transition1 in transitions_from_q0
        
        transitions_to_q2 = dfa.get_transitions_to(final_state)
        assert len(transitions_to_q2) == 1
        assert transition2 in transitions_to_q2
    
    def test_automaton_modification_workflow(self, sample_alphabet):
        """Test le workflow de modification d'un automate."""
        # Création initiale
        initial_state = State("q0", StateType.INITIAL)
        final_state = State("q1", StateType.FINAL)
        
        dfa = DFA(
            states={initial_state, final_state},
            initial_states={initial_state},
            final_states={final_state},
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        # Ajout d'un état intermédiaire
        intermediate_state = State("q2", StateType.INTERMEDIATE)
        dfa.add_state(intermediate_state)
        
        # Ajout de transitions
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
        
        dfa.add_transition(transition1)
        dfa.add_transition(transition2)
        
        # Vérifications
        assert len(dfa.states) == 3
        assert len(dfa.transitions) == 2
        assert dfa.is_valid()
        
        # Suppression d'un état et de ses transitions
        dfa.remove_state(intermediate_state)
        assert len(dfa.states) == 2
        assert len(dfa.transitions) == 0  # Les transitions sont supprimées
    
    def test_automaton_serialization_workflow(self, sample_alphabet):
        """Test le workflow de sérialisation/désérialisation."""
        # Création d'un automate
        initial_state = State("q0", StateType.INITIAL)
        final_state = State("q1", StateType.FINAL)
        
        transition = Transition(
            _source_state=initial_state,
            _target_state=final_state,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        dfa = DFA(
            states={initial_state, final_state},
            initial_states={initial_state},
            final_states={final_state},
            alphabet=sample_alphabet,
            transitions={transition}
        )
        
        # Sérialisation
        data = dfa.to_dict()
        
        # Vérification de la structure des données
        assert data["automaton_type"] == "dfa"
        assert len(data["states"]) == 2
        assert len(data["transitions"]) == 1
        assert data["alphabet"] == list(sample_alphabet)
        
        # Vérification des détails des états
        state_identifiers = [state["identifier"] for state in data["states"]]
        assert "q0" in state_identifiers
        assert "q1" in state_identifiers
        
        # Vérification des détails des transitions
        transition_data = data["transitions"][0]
        assert transition_data["source_state"] == "q0"
        assert transition_data["target_state"] == "q1"
        assert transition_data["symbol"] == "a"
        assert transition_data["transition_type"] == "symbol"
    
    def test_validation_workflow(self, sample_alphabet):
        """Test le workflow de validation."""
        # Création d'un automate valide
        initial_state = State("q0", StateType.INITIAL)
        final_state = State("q1", StateType.FINAL)
        
        dfa = DFA(
            states={initial_state, final_state},
            initial_states={initial_state},
            final_states={final_state},
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        # Validation
        errors = dfa.validate()
        assert len(errors) == 0
        assert dfa.is_valid()
        
        # Test avec un automate invalide
        invalid_dfa = DFA(
            states={initial_state, final_state},
            initial_states=set(),  # Pas d'état initial
            final_states={final_state},
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        errors = invalid_dfa.validate()
        assert len(errors) > 0
        assert not invalid_dfa.is_valid()
        assert any("initial state" in error.lower() for error in errors)
    
    def test_complex_automaton_workflow(self, sample_alphabet):
        """Test le workflow avec un automate complexe."""
        # Création d'un automate avec plusieurs états et transitions
        states = {
            State("q0", StateType.INITIAL),
            State("q1", StateType.INTERMEDIATE),
            State("q2", StateType.INTERMEDIATE),
            State("q3", StateType.FINAL),
        }
        
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q3", StateType.FINAL)}
        
        # Création de transitions complexes
        transitions = set()
        for i, symbol in enumerate(["a", "b", "c"]):
            source = State(f"q{i}", StateType.INTERMEDIATE if i > 0 else StateType.INITIAL)
            target = State(f"q{i+1}", StateType.FINAL if i == 2 else StateType.INTERMEDIATE)
            
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol=symbol,
                _transition_type=TransitionType.SYMBOL
            )
            transitions.add(transition)
        
        # Création de l'automate
        dfa = DFA(states, initial_states, final_states, sample_alphabet, transitions)
        
        # Vérifications
        assert dfa.is_valid()
        assert len(dfa.states) == 4
        assert len(dfa.transitions) == 3
        
        # Test des opérations de recherche
        q0 = State("q0", StateType.INITIAL)
        q1 = State("q1", StateType.INTERMEDIATE)
        
        transitions_from_q0 = dfa.get_transitions_from(q0)
        assert len(transitions_from_q0) == 1
        
        transitions_to_q1 = dfa.get_transitions_to(q1)
        assert len(transitions_to_q1) == 1
        
        transitions_a = dfa.get_transitions(q0, "a")
        assert len(transitions_a) == 1
    
    def test_epsilon_transition_workflow(self, sample_alphabet):
        """Test le workflow avec des transitions epsilon."""
        # Création d'un automate avec transition epsilon
        initial_state = State("q0", StateType.INITIAL)
        intermediate_state = State("q1", StateType.INTERMEDIATE)
        final_state = State("q2", StateType.FINAL)
        
        states = {initial_state, intermediate_state, final_state}
        initial_states = {initial_state}
        final_states = {final_state}
        
        # Transition symbolique
        symbol_transition = Transition(
            _source_state=initial_state,
            _target_state=intermediate_state,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        # Transition epsilon
        epsilon_transition = Transition(
            _source_state=intermediate_state,
            _target_state=final_state,
            _symbol=None,
            _transition_type=TransitionType.EPSILON
        )
        
        transitions = {symbol_transition, epsilon_transition}
        
        # Création de l'automate
        dfa = DFA(states, initial_states, final_states, sample_alphabet, transitions)
        
        # Vérifications
        assert dfa.is_valid()
        assert len(dfa.transitions) == 2
        
        # Test des transitions epsilon
        epsilon_transitions = dfa.get_transitions(intermediate_state, None)
        assert len(epsilon_transitions) == 1
        assert epsilon_transition in epsilon_transitions
    
    def test_automaton_with_metadata_workflow(self, sample_alphabet):
        """Test le workflow avec des métadonnées."""
        # Création d'états avec métadonnées
        initial_state = State("q0", StateType.INITIAL, {"description": "Start state"})
        final_state = State("q1", StateType.FINAL, {"description": "Accept state"})
        
        # Création d'une transition avec conditions et actions
        transition = Transition(
            _source_state=initial_state,
            _target_state=final_state,
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
            _conditions={"stack_top": "A"},
            _actions={"stack_push": "B"}
        )
        
        dfa = DFA(
            states={initial_state, final_state},
            initial_states={initial_state},
            final_states={final_state},
            alphabet=sample_alphabet,
            transitions={transition}
        )
        
        # Vérifications
        assert dfa.is_valid()
        
        # Test de la transition avec conditions
        assert transition.is_applicable("a", {"stack_top": "A"})
        assert not transition.is_applicable("a", {"stack_top": "B"})
        
        # Test de l'exécution de la transition
        context = {"original": "value"}
        new_context = transition.execute(context)
        assert new_context["stack_push"] == "B"
        assert new_context["original"] == "value"
    
    def test_error_handling_workflow(self, sample_alphabet):
        """Test le workflow de gestion d'erreurs."""
        # Test avec des états invalides
        invalid_state = State("invalid", StateType.INTERMEDIATE)
        
        dfa = DFA(
            states={State("q0", StateType.INITIAL)},
            initial_states={invalid_state},  # État initial invalide
            final_states={State("q1", StateType.FINAL)},  # État final invalide
            alphabet=sample_alphabet,
            transitions=set()
        )
        
        # Validation doit détecter les erreurs
        errors = dfa.validate()
        assert len(errors) > 0
        assert not dfa.is_valid()
        
        # Test avec des transitions invalides
        invalid_transition = Transition(
            _source_state=invalid_state,
            _target_state=State("q1", StateType.FINAL),
            _symbol="a",
            _transition_type=TransitionType.SYMBOL
        )
        
        dfa.add_transition(invalid_transition)
        errors = dfa.validate()
        assert len(errors) > 0