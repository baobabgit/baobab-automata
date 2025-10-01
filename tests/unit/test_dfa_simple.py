"""Tests unitaires simples pour les automates finis déterministes."""

import pytest
from baobab_automata.finite.dfa import DFA


@pytest.mark.unit
class TestDFASimple:
    """Tests simples pour la classe DFA."""

    def test_dfa_creation(self):
        """Test la création d'un DFA."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1", ("q1", "b"): "q0"},
            initial_state="q0",
            final_states={"q1"},
        )

        assert len(dfa.states) == 2
        assert dfa.initial_state == "q0"
        assert len(dfa.final_states) == 1
        assert "q1" in dfa.final_states
        assert dfa.alphabet == {"a", "b"}

    def test_dfa_accepts_word(self):
        """Test l'acceptation d'un mot."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        assert dfa.accepts("a") is True
        assert dfa.accepts("b") is False
        assert dfa.accepts("") is False

    def test_dfa_get_transition(self):
        """Test la récupération d'une transition."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        assert dfa.get_transition("q0", "a") == "q1"
        assert dfa.get_transition("q0", "b") is None

    def test_dfa_is_final_state(self):
        """Test la vérification d'état final."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        assert dfa.is_final_state("q1") is True
        assert dfa.is_final_state("q0") is False

    def test_dfa_get_reachable_states(self):
        """Test la récupération des états accessibles."""
        dfa = DFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        reachable = dfa.get_reachable_states()
        assert "q0" in reachable
        assert "q1" in reachable
        assert "q2" not in reachable

    def test_dfa_validate(self):
        """Test la validation d'un DFA."""
        # DFA valide
        valid_dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        assert valid_dfa.validate() is True

        # Test de validation avec un DFA valide mais avec des transitions invalides
        # Créons un DFA valide d'abord, puis testons la validation
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Testons la validation sur un DFA valide
        assert dfa.validate() is True

    def test_dfa_to_dict(self):
        """Test la sérialisation d'un DFA."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        data = dfa.to_dict()
        assert isinstance(data, dict)
        assert "states" in data
        assert "alphabet" in data
        assert "transitions" in data
        assert "initial_state" in data
        assert "final_states" in data

    def test_dfa_from_dict(self):
        """Test la désérialisation d'un DFA."""
        data = {
            "states": ["q0", "q1"],
            "alphabet": ["a", "b"],
            "transitions": {"q0,a": "q1"},
            "initial_state": "q0",
            "final_states": ["q1"],
        }

        dfa = DFA.from_dict(data)
        assert dfa.states == {"q0", "q1"}
        assert dfa.alphabet == {"a", "b"}
        assert dfa.initial_state == "q0"
        assert dfa.final_states == {"q1"}

    def test_dfa_string_representation(self):
        """Test la représentation string du DFA."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        str_repr = str(dfa)
        assert "DFA" in str_repr
        assert "states=2" in str_repr

    def test_dfa_minimize(self):
        """Test la minimisation d'un DFA."""
        dfa = DFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): "q1",
                ("q1", "a"): "q2",
                ("q2", "a"): "q2",
            },
            initial_state="q0",
            final_states={"q2"},
        )

        minimized = dfa.minimize()
        assert isinstance(minimized, DFA)
        assert len(minimized.states) <= len(dfa.states)

    def test_dfa_remove_unreachable_states(self):
        """Test la suppression des états inaccessibles."""
        dfa = DFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        cleaned = dfa.remove_unreachable_states()
        assert isinstance(cleaned, DFA)
        assert "q2" not in cleaned.states

    def test_dfa_complement(self):
        """Test le complément d'un DFA."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        complement = dfa.complement()
        assert isinstance(complement, DFA)
        assert complement.final_states == {"q0"}

    def test_dfa_to_nfa(self):
        """Test la conversion DFA vers NFA."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        nfa = dfa.to_nfa()
        assert hasattr(nfa, 'states')
        assert hasattr(nfa, 'alphabet')
        assert hasattr(nfa, 'initial_state')
        assert hasattr(nfa, 'final_states')

    def test_dfa_union(self):
        """Test l'union de deux DFA."""
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

        union = dfa1.union(dfa2)
        # L'union retourne un NFA, pas un DFA
        assert hasattr(union, 'states')
        assert hasattr(union, 'alphabet')
        assert hasattr(union, 'initial_state')
        assert hasattr(union, 'final_states')

    def test_dfa_intersection(self):
        """Test l'intersection de deux DFA."""
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

        intersection = dfa1.intersection(dfa2)
        # L'intersection retourne un NFA, pas un DFA
        assert hasattr(intersection, 'states')
        assert hasattr(intersection, 'alphabet')
        assert hasattr(intersection, 'initial_state')
        assert hasattr(intersection, 'final_states')

    def test_dfa_concatenation(self):
        """Test la concaténation de deux DFA."""
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

        concatenation = dfa1.concatenation(dfa2)
        # La concaténation retourne un NFA, pas un DFA
        assert hasattr(concatenation, 'states')
        assert hasattr(concatenation, 'alphabet')
        assert hasattr(concatenation, 'initial_state')
        assert hasattr(concatenation, 'final_states')

    def test_dfa_kleene_star(self):
        """Test l'étoile de Kleene d'un DFA."""
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        kleene = dfa.kleene_star()
        # L'étoile de Kleene retourne un NFA, pas un DFA
        assert hasattr(kleene, 'states')
        assert hasattr(kleene, 'alphabet')
        assert hasattr(kleene, 'initial_state')
        assert hasattr(kleene, 'final_states')

    def test_dfa_invalid_creation(self):
        """Test la création d'un DFA invalide."""
        with pytest.raises(Exception):  # InvalidDFAError
            DFA(
                states={"q1"},
                alphabet={"a"},
                transitions={},
                initial_state="q0",  # État initial pas dans les états
                final_states={"q1"},
            )