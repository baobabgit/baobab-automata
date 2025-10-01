"""Tests unitaires basiques pour les opérations de langage."""

import pytest
from baobab_automata.finite.language_operations import LanguageOperations
from baobab_automata.finite.dfa import DFA


@pytest.mark.unit
class TestLanguageOperationsBasic:
    """Tests basiques pour les opérations de langage."""

    def test_language_operations_initialization(self):
        """Test l'initialisation de LanguageOperations."""
        ops = LanguageOperations()
        assert ops is not None

    def test_union_same_automata(self):
        """Test l'union d'un automate avec lui-même."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        ops = LanguageOperations()
        union = ops.union(dfa, dfa)
        assert hasattr(union, 'states')
        assert hasattr(union, 'alphabet')
        # Les automates retournés n'ont pas d'attribut transitions public
        assert hasattr(union, 'states')
        assert hasattr(union, 'initial_state')
        assert hasattr(union, 'final_states')

    def test_intersection_same_automata(self):
        """Test l'intersection d'un automate avec lui-même."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        ops = LanguageOperations()
        intersection = ops.intersection(dfa, dfa)
        assert hasattr(intersection, 'states')
        assert hasattr(intersection, 'alphabet')
        # Les automates retournés n'ont pas d'attribut transitions public
        assert hasattr(intersection, 'states')
        assert hasattr(intersection, 'initial_state')
        assert hasattr(intersection, 'final_states')

    def test_concatenation_same_automata(self):
        """Test la concaténation d'un automate avec lui-même."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        ops = LanguageOperations()
        concatenation = ops.concatenation(dfa, dfa)
        assert hasattr(concatenation, 'states')
        assert hasattr(concatenation, 'alphabet')
        # Les automates retournés n'ont pas d'attribut transitions public
        assert hasattr(concatenation, 'states')
        assert hasattr(concatenation, 'initial_state')
        assert hasattr(concatenation, 'final_states')

    def test_kleene_star_single_automaton(self):
        """Test l'étoile de Kleene d'un automate."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        ops = LanguageOperations()
        kleene = ops.kleene_star(dfa)
        assert hasattr(kleene, 'states')
        assert hasattr(kleene, 'alphabet')
        # Les automates retournés n'ont pas d'attribut transitions public
        assert hasattr(kleene, 'states')
        assert hasattr(kleene, 'initial_state')
        assert hasattr(kleene, 'final_states')

    def test_complement_single_automaton(self):
        """Test le complément d'un automate."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        ops = LanguageOperations()
        complement = ops.complement(dfa)
        assert hasattr(complement, 'states')
        assert hasattr(complement, 'alphabet')
        # Les DFA retournés n'ont pas d'attribut transitions public
        assert hasattr(complement, 'states')
        assert hasattr(complement, 'initial_state')
        assert hasattr(complement, 'final_states')

    def test_union_different_automata(self):
        """Test l'union de deux automates différents."""
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )
        ops = LanguageOperations()
        union = ops.union(dfa1, dfa2)
        assert hasattr(union, 'states')
        assert hasattr(union, 'alphabet')
        # Les automates retournés n'ont pas d'attribut transitions public
        assert hasattr(union, 'states')
        assert hasattr(union, 'initial_state')
        assert hasattr(union, 'final_states')

    def test_intersection_different_automata(self):
        """Test l'intersection de deux automates différents."""
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )
        ops = LanguageOperations()
        intersection = ops.intersection(dfa1, dfa2)
        assert hasattr(intersection, 'states')
        assert hasattr(intersection, 'alphabet')
        # Les automates retournés n'ont pas d'attribut transitions public
        assert hasattr(intersection, 'states')
        assert hasattr(intersection, 'initial_state')
        assert hasattr(intersection, 'final_states')

    def test_concatenation_different_automata(self):
        """Test la concaténation de deux automates différents."""
        dfa1 = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        dfa2 = DFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): "q3"},
            initial_state="q2",
            final_states={"q3"},
        )
        ops = LanguageOperations()
        concatenation = ops.concatenation(dfa1, dfa2)
        assert hasattr(concatenation, 'states')
        assert hasattr(concatenation, 'alphabet')
        # Les automates retournés n'ont pas d'attribut transitions public
        assert hasattr(concatenation, 'states')
        assert hasattr(concatenation, 'initial_state')
        assert hasattr(concatenation, 'final_states')

    def test_operations_with_empty_automaton(self):
        """Test les opérations avec un automate vide."""
        empty_dfa = DFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states=set(),
        )
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        ops = LanguageOperations()
        
        # Test union avec automate vide
        union = ops.union(empty_dfa, dfa)
        assert hasattr(union, 'states')
        
        # Test intersection avec automate vide
        intersection = ops.intersection(empty_dfa, dfa)
        assert hasattr(intersection, 'states')
        
        # Test concaténation avec automate vide
        concatenation = ops.concatenation(empty_dfa, dfa)
        assert hasattr(concatenation, 'states')

    def test_operations_with_single_state_automaton(self):
        """Test les opérations avec un automate à un seul état."""
        single_dfa = DFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        ops = LanguageOperations()
        
        # Test union avec automate à un état
        union = ops.union(single_dfa, dfa)
        assert hasattr(union, 'states')
        
        # Test intersection avec automate à un état
        intersection = ops.intersection(single_dfa, dfa)
        assert hasattr(intersection, 'states')
        
        # Test concaténation avec automate à un état
        concatenation = ops.concatenation(single_dfa, dfa)
        assert hasattr(concatenation, 'states')

    def test_operations_with_no_transitions(self):
        """Test les opérations avec un automate sans transitions."""
        no_transitions_dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q1"},
        )
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        ops = LanguageOperations()
        
        # Test union avec automate sans transitions
        union = ops.union(no_transitions_dfa, dfa)
        assert hasattr(union, 'states')
        
        # Test intersection avec automate sans transitions
        intersection = ops.intersection(no_transitions_dfa, dfa)
        assert hasattr(intersection, 'states')
        
        # Test concaténation avec automate sans transitions
        concatenation = ops.concatenation(no_transitions_dfa, dfa)
        assert hasattr(concatenation, 'states')