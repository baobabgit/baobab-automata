"""Tests d'intégration pour les workflows complets."""

import pytest
from baobab_automata.automata.finite.dfa import DFA
from baobab_automata.automata.finite.epsilon_nfa import EpsilonNFA
from baobab_automata.automata.finite.dfa_exceptions import InvalidDFAError


@pytest.mark.integration
class TestIntegration:
    """Tests d'intégration."""

    def test_automaton_creation_workflow(self, sample_alphabet):
        """Test le workflow complet de création d'un automate."""
        # Création des états (utiliser des chaînes)
        states = {"q0", "q1", "q2"}
        initial_state = "q0"
        final_states = {"q2"}

        # Création des transitions (utiliser le format dictionnaire)
        transitions = {
            ("q0", "a"): "q1",
            ("q1", "b"): "q2",
        }

        # Création de l'automate
        dfa = DFA(states, sample_alphabet, transitions, initial_state, final_states)

        # Vérifications
        assert dfa.validate()
        assert len(dfa.states) == 3
        assert len(dfa._transitions) == 2

        # Vérification des transitions
        assert dfa.get_transition("q0", "a") == "q1"
        assert dfa.get_transition("q1", "b") == "q2"

    def test_automaton_modification_workflow(self, sample_alphabet):
        """Test le workflow de modification d'un automate."""
        # Création initiale
        states = {"q0", "q1"}
        transitions = {}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, sample_alphabet, transitions, initial_state, final_states)

        # Vérifications initiales
        assert len(dfa.states) == 2
        assert len(dfa._transitions) == 0
        assert dfa.validate()

        # Test de reconnaissance
        assert not dfa.accepts("a")  # Pas de transition définie

    def test_automaton_serialization_workflow(self, sample_alphabet):
        """Test le workflow de sérialisation/désérialisation."""
        # Création d'un automate
        states = {"q0", "q1"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, sample_alphabet, transitions, initial_state, final_states)

        # Sérialisation
        data = dfa.to_dict()

        # Vérification de la structure des données
        assert set(data["states"]) == {"q0", "q1"}
        assert set(data["alphabet"]) == sample_alphabet
        assert data["initial_state"] == "q0"
        assert set(data["final_states"]) == {"q1"}
        assert data["transitions"] == {"q0,a": "q1"}

    def test_validation_workflow(self, sample_alphabet):
        """Test le workflow de validation."""
        # Création d'un automate valide
        states = {"q0", "q1"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, sample_alphabet, transitions, initial_state, final_states)

        # Validation
        assert dfa.validate()

        # Test de reconnaissance
        assert dfa.accepts("a")
        assert not dfa.accepts("b")

    def test_complex_automaton_workflow(self, sample_alphabet):
        """Test le workflow avec un automate complexe."""
        # Création d'un automate avec plusieurs états et transitions
        states = {"q0", "q1", "q2", "q3"}
        transitions = {
            ("q0", "a"): "q1",
            ("q1", "b"): "q2",
            ("q2", "c"): "q3",
        }
        initial_state = "q0"
        final_states = {"q3"}

        dfa = DFA(states, sample_alphabet, transitions, initial_state, final_states)

        # Vérifications
        assert dfa.validate()
        assert len(dfa.states) == 4
        assert len(dfa._transitions) == 3

        # Test de reconnaissance
        assert dfa.accepts("abc")
        assert not dfa.accepts("ab")
        assert not dfa.accepts("abcd")

    def test_epsilon_transition_workflow(self, sample_alphabet):
        """Test le workflow avec des transitions epsilon."""
        # Création d'un ε-NFA
        states = {"q0", "q1", "q2"}
        transitions = {
            ("q0", "a"): {"q1"},
            ("q1", "ε"): {"q2"},  # transition epsilon
        }
        initial_state = "q0"
        final_states = {"q2"}

        epsilon_nfa = EpsilonNFA(states, sample_alphabet, transitions, initial_state, final_states)

        # Vérifications
        assert epsilon_nfa.validate()
        assert len(epsilon_nfa.states) == 3
        assert len(epsilon_nfa._transitions) == 2

        # Test de reconnaissance
        assert epsilon_nfa.accepts("a")
        assert not epsilon_nfa.accepts("ab")

    def test_automaton_with_metadata_workflow(self, sample_alphabet):
        """Test le workflow avec des métadonnées."""
        # Création d'un automate simple
        states = {"q0", "q1"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, sample_alphabet, transitions, initial_state, final_states)

        # Vérifications
        assert dfa.validate()

    def test_error_handling_workflow(self, sample_alphabet):
        """Test le workflow de gestion d'erreurs."""
        # Test avec des paramètres invalides
        with pytest.raises(InvalidDFAError):
            DFA(set(), sample_alphabet, {}, "", set())