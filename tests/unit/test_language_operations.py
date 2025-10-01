"""Tests unitaires pour la classe LanguageOperations."""

import pytest
from baobab_automata.finite.language_operations import LanguageOperations
from baobab_automata.finite.dfa import DFA
from baobab_automata.finite.nfa import NFA
from baobab_automata.finite.language_operations_exceptions import (
    IncompatibleAutomataError,
    OperationValidationError,
)


@pytest.mark.unit
class TestLanguageOperations:
    """Tests pour la classe LanguageOperations."""

    def test_initialization(self):
        """Test l'initialisation de LanguageOperations."""
        ops = LanguageOperations()
        assert ops._optimization_enabled is True
        assert ops._max_states == 1000
        assert ops._operation_timeout == 30.0
        assert isinstance(ops._stats, type(ops._stats))

    def test_initialization_with_params(self):
        """Test l'initialisation avec paramètres personnalisés."""
        ops = LanguageOperations(optimization_enabled=False, max_states=500)
        assert ops._optimization_enabled is False
        assert ops._max_states == 500

    def test_union_basic(self):
        """Test l'union de base de deux DFA."""
        # DFA acceptant "a"
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        # DFA acceptant "b"
        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"b"},
            transitions={("q2", "b"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )

        result = LanguageOperations.union(dfa1, dfa2)
        assert isinstance(result, NFA)
        assert "union_initial" in result.states
        assert "1_q0" in result.states
        assert "2_q2" in result.states

    def test_union_incompatible_alphabets(self):
        """Test l'union avec des alphabets incompatibles."""
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"b"},
            transitions={("q2", "b"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )

        with pytest.raises(IncompatibleAutomataError):
            LanguageOperations.union(dfa1, dfa2)

    def test_union_invalid_automaton1(self):
        """Test l'union avec un automate invalide."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        with pytest.raises(OperationValidationError):
            LanguageOperations.union("not_an_automaton", dfa)

    def test_union_invalid_automaton2(self):
        """Test l'union avec un automate invalide."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        with pytest.raises(OperationValidationError):
            LanguageOperations.union(dfa, "not_an_automaton")

    def test_intersection_basic(self):
        """Test l'intersection de base de deux DFA."""
        # DFA acceptant "a"
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        # DFA acceptant "a" aussi
        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )

        result = LanguageOperations.intersection(dfa1, dfa2)
        assert isinstance(result, NFA)
        assert "(q0,q2)" in result.states
        assert "(q1,q3)" in result.states

    def test_intersection_incompatible_alphabets(self):
        """Test l'intersection avec des alphabets incompatibles."""
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"b"},
            transitions={("q2", "b"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )

        with pytest.raises(IncompatibleAutomataError):
            LanguageOperations.intersection(dfa1, dfa2)

    def test_intersection_invalid_automaton1(self):
        """Test l'intersection avec un automate invalide."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        with pytest.raises(OperationValidationError):
            LanguageOperations.intersection("not_an_automaton", dfa)

    def test_intersection_invalid_automaton2(self):
        """Test l'intersection avec un automate invalide."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        with pytest.raises(OperationValidationError):
            LanguageOperations.intersection(dfa, "not_an_automaton")

    def test_complement_basic(self):
        """Test le complément de base d'un DFA."""
        # DFA acceptant "a"
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        result = LanguageOperations.complement(dfa)
        assert isinstance(result, DFA)
        assert result.states == dfa.states
        assert result.alphabet == dfa.alphabet
        assert result.initial_state == dfa.initial_state

    def test_complement_invalid_automaton(self):
        """Test le complément avec un automate invalide."""
        with pytest.raises(OperationValidationError):
            LanguageOperations.complement("not_an_automaton")

    def test_concatenation_basic(self):
        """Test la concaténation de base de deux DFA."""
        # DFA acceptant "a"
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        # DFA acceptant "b"
        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"b"},
            transitions={("q2", "b"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )

        result = LanguageOperations.concatenation(dfa1, dfa2)
        assert isinstance(result, NFA)
        assert "concat_initial" in result.states
        assert "1_q0" in result.states
        assert "2_q2" in result.states

    def test_concatenation_incompatible_alphabets(self):
        """Test la concaténation avec des alphabets incompatibles."""
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"b"},
            transitions={("q2", "b"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )

        with pytest.raises(IncompatibleAutomataError):
            LanguageOperations.concatenation(dfa1, dfa2)

    def test_concatenation_invalid_automaton1(self):
        """Test la concaténation avec un automate invalide."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        with pytest.raises(OperationValidationError):
            LanguageOperations.concatenation("not_an_automaton", dfa)

    def test_concatenation_invalid_automaton2(self):
        """Test la concaténation avec un automate invalide."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        with pytest.raises(OperationValidationError):
            LanguageOperations.concatenation(dfa, "not_an_automaton")

    def test_kleene_star_basic(self):
        """Test l'étoile de Kleene de base d'un DFA."""
        # DFA acceptant "a"
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        result = LanguageOperations.kleene_star(dfa)
        assert isinstance(result, NFA)
        assert "kleene_initial" in result.states
        assert "1_q0" in result.states

    def test_kleene_star_invalid_automaton(self):
        """Test l'étoile de Kleene avec un automate invalide."""
        with pytest.raises(OperationValidationError):
            LanguageOperations.kleene_star("not_an_automaton")

    def test_operations_with_same_automaton(self):
        """Test les opérations avec le même automate."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        # Union avec lui-même
        union_result = LanguageOperations.union(dfa, dfa)
        assert isinstance(union_result, NFA)

        # Intersection avec lui-même
        intersection_result = LanguageOperations.intersection(dfa, dfa)
        assert isinstance(intersection_result, NFA)

        # Concaténation avec lui-même
        concat_result = LanguageOperations.concatenation(dfa, dfa)
        assert isinstance(concat_result, NFA)

    def test_operations_with_empty_automaton(self):
        """Test les opérations avec un automate vide."""
        # DFA vide (pas d'états finaux)
        empty_dfa = DFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states=set(),
        )

        # DFA acceptant "a"
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        # Union avec automate vide
        union_result = LanguageOperations.union(empty_dfa, dfa)
        assert isinstance(union_result, NFA)

        # Intersection avec automate vide
        intersection_result = LanguageOperations.intersection(empty_dfa, dfa)
        assert isinstance(intersection_result, NFA)

    def test_operations_with_single_state_automaton(self):
        """Test les opérations avec un automate à un seul état."""
        # DFA avec un seul état (état initial et final)
        single_dfa = DFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )

        # DFA acceptant "a"
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        # Union
        union_result = LanguageOperations.union(single_dfa, dfa)
        assert isinstance(union_result, NFA)

        # Intersection
        intersection_result = LanguageOperations.intersection(single_dfa, dfa)
        assert isinstance(intersection_result, NFA)

    def test_operations_with_complex_automaton(self):
        """Test les opérations avec des automates complexes."""
        # DFA acceptant "ab"
        dfa1 = DFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): "q1",
                ("q1", "b"): "q2",
            },
            initial_state="q0",
            final_states={"q2"},
        )

        # DFA acceptant "ba"
        dfa2 = DFA(
            states={"q3", "q4", "q5"},
            alphabet={"a", "b"},
            transitions={
                ("q3", "b"): "q4",
                ("q4", "a"): "q5",
            },
            initial_state="q3",
            final_states={"q5"},
        )

        # Union
        union_result = LanguageOperations.union(dfa1, dfa2)
        assert isinstance(union_result, NFA)
        assert len(union_result.states) > len(dfa1.states) + len(dfa2.states)

        # Intersection
        intersection_result = LanguageOperations.intersection(dfa1, dfa2)
        assert isinstance(intersection_result, NFA)

        # Concaténation
        concat_result = LanguageOperations.concatenation(dfa1, dfa2)
        assert isinstance(concat_result, NFA)

    def test_operations_with_different_alphabets(self):
        """Test les opérations avec des alphabets différents."""
        # DFA avec alphabet {"a", "b"}
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        # DFA avec alphabet {"c", "d"}
        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"c", "d"},
            transitions={("q2", "c"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )

        # Ces opérations devraient échouer à cause des alphabets différents
        with pytest.raises(IncompatibleAutomataError):
            LanguageOperations.union(dfa1, dfa2)

        with pytest.raises(IncompatibleAutomataError):
            LanguageOperations.intersection(dfa1, dfa2)

        with pytest.raises(IncompatibleAutomataError):
            LanguageOperations.concatenation(dfa1, dfa2)

    def test_operations_with_epsilon_transitions(self):
        """Test les opérations avec des transitions epsilon."""
        # NFA avec transitions epsilon
        nfa1 = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "epsilon"},
            transitions={
                ("q0", "epsilon"): {"q1"},
                ("q1", "a"): {"q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        nfa2 = NFA(
            states={"q3", "q4", "q5"},
            alphabet={"b", "epsilon"},
            transitions={
                ("q3", "epsilon"): {"q4"},
                ("q4", "b"): {"q5"},
            },
            initial_state="q3",
            final_states={"q5"},
        )

        # Union avec transitions epsilon
        union_result = LanguageOperations.union(nfa1, nfa2)
        assert isinstance(union_result, NFA)
        assert "epsilon" in union_result.alphabet

    def test_operations_error_handling(self):
        """Test la gestion d'erreurs des opérations."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        # Test avec None
        with pytest.raises(OperationValidationError):
            LanguageOperations.union(None, dfa)

        with pytest.raises(OperationValidationError):
            LanguageOperations.union(dfa, None)

        # Test avec des types invalides
        with pytest.raises(OperationValidationError):
            LanguageOperations.union(123, dfa)

        with pytest.raises(OperationValidationError):
            LanguageOperations.union(dfa, [])

    def test_operations_with_minimal_automata(self):
        """Test les opérations avec des automates minimaux."""
        # DFA minimal acceptant le mot vide
        empty_dfa = DFA(
            states={"q0"},
            alphabet=set(),
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )

        # DFA minimal acceptant "a"
        a_dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        # Union avec automate vide
        union_result = LanguageOperations.union(empty_dfa, a_dfa)
        assert isinstance(union_result, NFA)

        # Complément de l'automate vide
        complement_result = LanguageOperations.complement(empty_dfa)
        assert isinstance(complement_result, DFA)

        # Étoile de Kleene de l'automate vide
        kleene_result = LanguageOperations.kleene_star(empty_dfa)
        assert isinstance(kleene_result, NFA)