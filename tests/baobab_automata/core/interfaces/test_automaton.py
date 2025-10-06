"""
Tests unitaires pour les automates.

Ce module contient les tests unitaires pour l'interface IAutomaton
et les implémentations d'automates.
"""

import pytest
from unittest.mock import Mock
from baobab_automata.core.interfaces.automaton import AutomatonType
from baobab_automata.core.interfaces.state import StateType
from baobab_automata.core.interfaces.transition import TransitionType
from baobab_automata.core.implementations.state import State
from baobab_automata.core.implementations.transition import Transition


class TestAutomatonInterface:
    """Tests pour l'interface IAutomaton."""

    def test_automaton_type_enum(self):
        """Test l'énumération AutomatonType."""
        assert AutomatonType.DFA.value == "dfa"
        assert AutomatonType.NFA.value == "nfa"
        assert AutomatonType.EPSILON_NFA.value == "epsilon_nfa"
        assert AutomatonType.PDA.value == "pda"
        assert AutomatonType.DPDA.value == "dpda"
        assert AutomatonType.NPDA.value == "npda"
        assert AutomatonType.TM.value == "tm"
        assert AutomatonType.DTM.value == "dtm"
        assert AutomatonType.NTM.value == "ntm"
        assert AutomatonType.MULTI_TAPE_TM.value == "multi_tape_tm"

    def test_automaton_interface_properties(self, mock_automaton):
        """Test les propriétés de l'interface IAutomaton."""
        assert hasattr(mock_automaton, "automaton_type")
        assert hasattr(mock_automaton, "states")
        assert hasattr(mock_automaton, "initial_states")
        assert hasattr(mock_automaton, "final_states")
        assert hasattr(mock_automaton, "alphabet")
        assert hasattr(mock_automaton, "transitions")

    def test_automaton_interface_methods(self, mock_automaton):
        """Test les méthodes de l'interface IAutomaton."""
        # Test des méthodes d'ajout/suppression
        assert hasattr(mock_automaton, "add_state")
        assert hasattr(mock_automaton, "remove_state")
        assert hasattr(mock_automaton, "add_transition")
        assert hasattr(mock_automaton, "remove_transition")

        # Test des méthodes de récupération
        assert hasattr(mock_automaton, "get_transitions_from")
        assert hasattr(mock_automaton, "get_transitions_to")
        assert hasattr(mock_automaton, "get_transitions")

        # Test des méthodes de validation
        assert hasattr(mock_automaton, "is_valid")
        assert hasattr(mock_automaton, "validate")

        # Test des méthodes de sérialisation
        assert hasattr(mock_automaton, "to_dict")
        assert hasattr(mock_automaton, "from_dict")

        # Test des méthodes de représentation
        assert hasattr(mock_automaton, "__str__")
        assert hasattr(mock_automaton, "__repr__")


class TestAutomatonWorkflow:
    """Tests de workflow pour les automates."""

    def test_automaton_creation_workflow(
        self, sample_states, sample_alphabet, sample_transitions
    ):
        """Test le workflow de création d'un automate."""
        # Création d'un mock d'automate
        mock_automaton = Mock()
        mock_automaton.automaton_type = AutomatonType.DFA
        mock_automaton.states = {sample_states["initial"], sample_states["final"]}
        mock_automaton.initial_states = {sample_states["initial"]}
        mock_automaton.final_states = {sample_states["final"]}
        mock_automaton.alphabet = sample_alphabet
        mock_automaton.transitions = {sample_transitions["symbol"]}

        # Vérification des propriétés
        assert mock_automaton.automaton_type == AutomatonType.DFA
        assert len(mock_automaton.states) == 2
        assert len(mock_automaton.initial_states) == 1
        assert len(mock_automaton.final_states) == 1
        assert mock_automaton.alphabet == sample_alphabet
        assert len(mock_automaton.transitions) == 1

    def test_automaton_state_management_workflow(self, sample_states, mock_automaton):
        """Test le workflow de gestion des états."""
        # Configuration du mock
        mock_automaton.add_state.return_value = None
        mock_automaton.remove_state.return_value = None

        # Test d'ajout d'état
        mock_automaton.add_state(sample_states["initial"])
        mock_automaton.add_state.assert_called_once_with(sample_states["initial"])

        # Test de suppression d'état
        mock_automaton.remove_state(sample_states["initial"])
        mock_automaton.remove_state.assert_called_with(sample_states["initial"])

    def test_automaton_transition_management_workflow(
        self, sample_transitions, mock_automaton
    ):
        """Test le workflow de gestion des transitions."""
        # Configuration du mock
        mock_automaton.add_transition.return_value = None
        mock_automaton.remove_transition.return_value = None

        # Test d'ajout de transition
        mock_automaton.add_transition(sample_transitions["symbol"])
        mock_automaton.add_transition.assert_called_once_with(
            sample_transitions["symbol"]
        )

        # Test de suppression de transition
        mock_automaton.remove_transition(sample_transitions["symbol"])
        mock_automaton.remove_transition.assert_called_with(
            sample_transitions["symbol"]
        )

    def test_automaton_transition_queries_workflow(
        self, sample_states, sample_transitions, mock_automaton
    ):
        """Test le workflow de requêtes de transitions."""
        # Configuration du mock
        mock_automaton.get_transitions_from.return_value = {
            sample_transitions["symbol"]
        }
        mock_automaton.get_transitions_to.return_value = {sample_transitions["symbol"]}
        mock_automaton.get_transitions.return_value = {sample_transitions["symbol"]}

        # Test de récupération des transitions partant d'un état
        transitions_from = mock_automaton.get_transitions_from(sample_states["initial"])
        mock_automaton.get_transitions_from.assert_called_once_with(
            sample_states["initial"]
        )
        assert transitions_from == {sample_transitions["symbol"]}

        # Test de récupération des transitions arrivant à un état
        transitions_to = mock_automaton.get_transitions_to(sample_states["final"])
        mock_automaton.get_transitions_to.assert_called_once_with(
            sample_states["final"]
        )
        assert transitions_to == {sample_transitions["symbol"]}

        # Test de récupération des transitions pour un état et un symbole
        transitions = mock_automaton.get_transitions(sample_states["initial"], "a")
        mock_automaton.get_transitions.assert_called_once_with(
            sample_states["initial"], "a"
        )
        assert transitions == {sample_transitions["symbol"]}

    def test_automaton_validation_workflow(self, mock_automaton):
        """Test le workflow de validation d'un automate."""
        # Configuration du mock
        mock_automaton.is_valid.return_value = True
        mock_automaton.validate.return_value = []

        # Test de validation simple
        is_valid = mock_automaton.is_valid()
        assert is_valid is True

        # Test de validation détaillée
        errors = mock_automaton.validate()
        assert errors == []

    def test_automaton_serialization_workflow(self, mock_automaton):
        """Test le workflow de sérialisation d'un automate."""
        # Configuration du mock
        mock_data = {
            "automaton_type": "dfa",
            "states": [],
            "transitions": [],
            "alphabet": [],
            "initial_states": [],
            "final_states": [],
        }
        mock_automaton.to_dict.return_value = mock_data
        mock_automaton.from_dict.return_value = None

        # Test de sérialisation
        data = mock_automaton.to_dict()
        assert data == mock_data

        # Test de désérialisation
        mock_automaton.from_dict(mock_data)
        mock_automaton.from_dict.assert_called_once_with(mock_data)

    def test_automaton_representation_workflow(self, mock_automaton):
        """Test le workflow de représentation d'un automate."""
        # Configuration du mock
        mock_automaton.__str__ = Mock(return_value="DFA(states=2, transitions=1)")
        mock_automaton.__repr__ = Mock(
            return_value="DFA(automaton_type='dfa', states=2)"
        )

        # Test de représentation string
        str_repr = str(mock_automaton)
        assert str_repr == "DFA(states=2, transitions=1)"

        # Test de représentation détaillée
        repr_str = repr(mock_automaton)
        assert repr_str == "DFA(automaton_type='dfa', states=2)"


class TestAutomatonTypes:
    """Tests pour les différents types d'automates."""

    def test_finite_automaton_types(self):
        """Test les types d'automates finis."""
        finite_types = [
            AutomatonType.DFA,
            AutomatonType.NFA,
            AutomatonType.EPSILON_NFA,
        ]

        for automaton_type in finite_types:
            assert automaton_type in AutomatonType
            assert isinstance(automaton_type.value, str)

    def test_pushdown_automaton_types(self):
        """Test les types d'automates à pile."""
        pushdown_types = [
            AutomatonType.PDA,
            AutomatonType.DPDA,
            AutomatonType.NPDA,
        ]

        for automaton_type in pushdown_types:
            assert automaton_type in AutomatonType
            assert isinstance(automaton_type.value, str)

    def test_turing_machine_types(self):
        """Test les types de machines de Turing."""
        turing_types = [
            AutomatonType.TM,
            AutomatonType.DTM,
            AutomatonType.NTM,
            AutomatonType.MULTI_TAPE_TM,
        ]

        for automaton_type in turing_types:
            assert automaton_type in AutomatonType
            assert isinstance(automaton_type.value, str)


class TestAutomatonIntegration:
    """Tests d'intégration pour les automates."""

    def test_complete_automaton_workflow(
        self, sample_states, sample_alphabet, sample_transitions
    ):
        """Test un workflow complet d'automate."""
        # Création d'un automate complet
        mock_automaton = Mock()
        mock_automaton.automaton_type = AutomatonType.DFA
        mock_automaton.states = {sample_states["initial"], sample_states["final"]}
        mock_automaton.initial_states = {sample_states["initial"]}
        mock_automaton.final_states = {sample_states["final"]}
        mock_automaton.alphabet = sample_alphabet
        mock_automaton.transitions = {sample_transitions["symbol"]}

        # Configuration des méthodes
        mock_automaton.is_valid.return_value = True
        mock_automaton.validate.return_value = []
        mock_automaton.get_transitions.return_value = {sample_transitions["symbol"]}

        # Test de validation
        assert mock_automaton.is_valid() is True
        assert mock_automaton.validate() == []

        # Test de récupération de transitions
        transitions = mock_automaton.get_transitions(sample_states["initial"], "a")
        assert transitions == {sample_transitions["symbol"]}

        # Test de la structure
        assert len(mock_automaton.states) == 2
        assert len(mock_automaton.initial_states) == 1
        assert len(mock_automaton.final_states) == 1
        assert len(mock_automaton.transitions) == 1
        assert mock_automaton.alphabet == sample_alphabet

    def test_automaton_error_handling_workflow(self, mock_automaton):
        """Test le workflow de gestion d'erreurs d'un automate."""
        # Configuration du mock pour simuler des erreurs
        mock_automaton.is_valid.return_value = False
        mock_automaton.validate.return_value = [
            "No initial states",
            "Invalid transition",
        ]

        # Test de validation avec erreurs
        assert mock_automaton.is_valid() is False
        errors = mock_automaton.validate()
        assert len(errors) == 2
        assert "No initial states" in errors
        assert "Invalid transition" in errors
