"""Tests unitaires pour les automates finis déterministes."""

import pytest
from baobab_automata.finite.dfa import DFA
from baobab_automata.interfaces.state import StateType
from baobab_automata.interfaces.transition import TransitionType
from baobab_automata.interfaces.automaton import AutomatonType
from baobab_automata.implementations.state import State
from baobab_automata.implementations.transition import Transition


@pytest.mark.unit
class TestDFA:
    """Tests pour la classe DFA."""

    def test_dfa_creation(self, sample_states, sample_alphabet):
        """Test la création d'un DFA."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set(),
        )

        assert dfa.automaton_type == AutomatonType.DFA
        assert len(dfa.states) == 2
        assert len(dfa.initial_states) == 1
        assert len(dfa.final_states) == 1
        assert dfa.alphabet == sample_alphabet

    def test_add_state(self, sample_states, sample_alphabet):
        """Test l'ajout d'un état."""
        dfa = DFA(
            states=set(),
            initial_states=set(),
            final_states=set(),
            alphabet=sample_alphabet,
            transitions=set(),
        )

        dfa.add_state(sample_states["initial"])
        assert sample_states["initial"] in dfa.states

    def test_remove_state(self, sample_states, sample_alphabet):
        """Test la suppression d'un état."""
        dfa = DFA(
            states={sample_states["initial"]},
            initial_states={sample_states["initial"]},
            final_states=set(),
            alphabet=sample_alphabet,
            transitions=set(),
        )

        dfa.remove_state(sample_states["initial"])
        assert sample_states["initial"] not in dfa.states

    def test_add_transition(self, sample_states, sample_alphabet, sample_transitions):
        """Test l'ajout d'une transition."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set(),
        )

        dfa.add_transition(sample_transitions["symbol"])
        assert sample_transitions["symbol"] in dfa.transitions

    def test_get_transitions_from(
        self, sample_states, sample_alphabet, sample_transitions
    ):
        """Test la récupération des transitions partant d'un état."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions={sample_transitions["symbol"]},
        )

        transitions = dfa.get_transitions_from(sample_states["initial"])
        assert sample_transitions["symbol"] in transitions

    def test_get_transitions_to(
        self, sample_states, sample_alphabet, sample_transitions
    ):
        """Test la récupération des transitions arrivant à un état."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["intermediate"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["intermediate"]},
            alphabet=sample_alphabet,
            transitions={sample_transitions["symbol"]},
        )

        transitions = dfa.get_transitions_to(sample_states["intermediate"])
        assert sample_transitions["symbol"] in transitions

    def test_get_transitions(self, sample_states, sample_alphabet, sample_transitions):
        """Test la récupération des transitions pour un état et un symbole."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions={sample_transitions["symbol"]},
        )

        transitions = dfa.get_transitions(sample_states["initial"], "a")
        assert sample_transitions["symbol"] in transitions

        transitions = dfa.get_transitions(sample_states["initial"], "b")
        assert len(transitions) == 0

    def test_is_valid(self, sample_states, sample_alphabet):
        """Test la validation d'un DFA."""
        # DFA valide
        valid_dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set(),
        )
        assert valid_dfa.is_valid() is True

        # DFA invalide (pas d'état initial)
        invalid_dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states=set(),
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set(),
        )
        assert invalid_dfa.is_valid() is False

    def test_validate(self, sample_states, sample_alphabet):
        """Test la validation détaillée d'un DFA."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set(),
        )

        errors = dfa.validate()
        assert isinstance(errors, list)

    def test_validate_with_invalid_states(self, sample_states, sample_alphabet):
        """Test la validation avec des états invalides."""
        # Créer un état qui n'est pas dans l'ensemble des états
        invalid_state = State("invalid", StateType.INTERMEDIATE)

        dfa = DFA(
            states={sample_states["initial"]},
            initial_states={invalid_state},  # État initial invalide
            final_states={sample_states["final"]},  # État final invalide
            alphabet=sample_alphabet,
            transitions=set(),
        )

        errors = dfa.validate()
        assert len(errors) > 0
        assert any("Initial state" in error for error in errors)
        assert any("Final state" in error for error in errors)

    def test_validate_with_invalid_transitions(self, sample_states, sample_alphabet):
        """Test la validation avec des transitions invalides."""
        invalid_state = State("invalid", StateType.INTERMEDIATE)
        invalid_transition = Transition(
            _source_state=invalid_state,
            _target_state=sample_states["final"],
            _symbol="a",
            _transition_type=TransitionType.SYMBOL,
        )

        dfa = DFA(
            states={sample_states["initial"]},
            initial_states={sample_states["initial"]},
            final_states=set(),
            alphabet=sample_alphabet,
            transitions={invalid_transition},
        )

        errors = dfa.validate()
        assert len(errors) > 0
        assert any("source state" in error.lower() for error in errors)
        assert any("target state" in error.lower() for error in errors)

    def test_to_dict(self, sample_states, sample_alphabet):
        """Test la sérialisation d'un DFA."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set(),
        )

        data = dfa.to_dict()
        assert isinstance(data, dict)
        assert "states" in data
        assert "transitions" in data
        assert "alphabet" in data
        assert "automaton_type" in data
        assert data["automaton_type"] == "dfa"

    def test_to_dict_with_transitions(
        self, sample_states, sample_alphabet, sample_transitions
    ):
        """Test la sérialisation d'un DFA avec des transitions."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions={sample_transitions["symbol"]},
        )

        data = dfa.to_dict()
        assert len(data["transitions"]) == 1
        transition_data = data["transitions"][0]
        assert transition_data["source_state"] == "q0"
        assert transition_data["target_state"] == "q1"
        assert transition_data["symbol"] == "a"

    def test_from_dict_not_implemented(self, sample_states, sample_alphabet):
        """Test que from_dict lève NotImplementedError."""
        dfa = DFA(
            states={sample_states["initial"]},
            initial_states={sample_states["initial"]},
            final_states=set(),
            alphabet=sample_alphabet,
            transitions=set(),
        )

        with pytest.raises(NotImplementedError):
            dfa.from_dict({})

    def test_string_representation(self, sample_states, sample_alphabet):
        """Test la représentation string du DFA."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions=set(),
        )

        str_repr = str(dfa)
        assert "DFA" in str_repr
        assert "states=2" in str_repr
        assert "transitions=0" in str_repr

    def test_remove_state_removes_associated_transitions(
        self, sample_states, sample_alphabet, sample_transitions
    ):
        """Test que la suppression d'un état supprime les transitions associées."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions={sample_transitions["symbol"]},
        )

        # Supprimer l'état source de la transition
        dfa.remove_state(sample_states["initial"])

        # La transition doit être supprimée
        assert len(dfa.transitions) == 0
        assert sample_states["initial"] not in dfa.states
        assert sample_states["initial"] not in dfa.initial_states

    def test_remove_transition(
        self, sample_states, sample_alphabet, sample_transitions
    ):
        """Test la suppression d'une transition."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["final"]},
            initial_states={sample_states["initial"]},
            final_states={sample_states["final"]},
            alphabet=sample_alphabet,
            transitions={sample_transitions["symbol"]},
        )

        dfa.remove_transition(sample_transitions["symbol"])
        assert sample_transitions["symbol"] not in dfa.transitions

    def test_empty_dfa(self, sample_alphabet):
        """Test la création d'un DFA vide."""
        dfa = DFA(
            states=set(),
            initial_states=set(),
            final_states=set(),
            alphabet=sample_alphabet,
            transitions=set(),
        )

        assert len(dfa.states) == 0
        assert len(dfa.initial_states) == 0
        assert len(dfa.final_states) == 0
        assert len(dfa.transitions) == 0
        assert not dfa.is_valid()  # DFA vide n'est pas valide

    def test_dfa_with_multiple_initial_states(self, sample_states, sample_alphabet):
        """Test un DFA avec plusieurs états initiaux."""
        dfa = DFA(
            states={sample_states["initial"], sample_states["intermediate"]},
            initial_states={sample_states["initial"], sample_states["intermediate"]},
            final_states=set(),
            alphabet=sample_alphabet,
            transitions=set(),
        )

        assert len(dfa.initial_states) == 2
        assert dfa.is_valid() is True
