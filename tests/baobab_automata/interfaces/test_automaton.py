"""
Tests unitaires pour l'interface IAutomaton et l'énumération AutomatonType.

Ce module teste l'interface IAutomaton et l'énumération AutomatonType.
"""

import pytest

from baobab_automata.interfaces.automaton import IAutomaton, AutomatonType


class TestAutomatonType:
    """Tests pour l'énumération AutomatonType."""

    def test_automaton_type_values(self):
        """Test que tous les types d'automates sont définis."""
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

    def test_automaton_type_enumeration(self):
        """Test que l'énumération contient tous les types attendus."""
        expected_types = {
            "dfa",
            "nfa",
            "epsilon_nfa",
            "pda",
            "dpda",
            "npda",
            "tm",
            "dtm",
            "ntm",
            "multi_tape_tm",
        }
        actual_types = {
            automaton_type.value for automaton_type in AutomatonType
        }
        assert actual_types == expected_types


class TestIAutomatonInterface:
    """Tests pour l'interface IAutomaton."""

    def test_interface_has_required_methods(self):
        """Test que l'interface IAutomaton a toutes les méthodes requises."""
        required_methods = [
            "automaton_type",
            "states",
            "initial_states",
            "final_states",
            "alphabet",
            "transitions",
            "add_state",
            "remove_state",
            "add_transition",
            "remove_transition",
            "get_transitions_from",
            "get_transitions_to",
            "get_transitions",
            "is_valid",
            "validate",
            "to_dict",
            "from_dict",
            "__str__",
            "__repr__",
        ]

        for method_name in required_methods:
            assert hasattr(
                IAutomaton, method_name
            ), f"Method {method_name} missing from IAutomaton"

    def test_interface_methods_are_abstract(self):
        """Test que les méthodes de l'interface sont abstraites."""
        # Vérifier que l'interface ne peut pas être instanciée directement
        with pytest.raises(TypeError):
            IAutomaton()

    def test_interface_properties_are_abstract(self):
        """Test que les propriétés de l'interface sont abstraites."""
        # Vérifier que les propriétés sont définies comme @property @abstractmethod
        assert hasattr(IAutomaton, "automaton_type")
        assert hasattr(IAutomaton, "states")
        assert hasattr(IAutomaton, "initial_states")
        assert hasattr(IAutomaton, "final_states")
        assert hasattr(IAutomaton, "alphabet")
        assert hasattr(IAutomaton, "transitions")
