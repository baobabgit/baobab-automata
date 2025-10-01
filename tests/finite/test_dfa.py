"""
Tests unitaires pour la classe DFA.

Ce module contient tous les tests unitaires pour valider le bon fonctionnement
de la classe DFA selon les spécifications détaillées.
"""

import unittest
from typing import Dict, Set, Tuple

from baobab_automata.finite.dfa import DFA
from baobab_automata.finite.dfa_exceptions import (
    DFAError,
    InvalidDFAError,
    InvalidStateError,
    InvalidTransitionError,
)


class TestDFA(unittest.TestCase):
    """Tests unitaires pour la classe DFA."""

    def test_dfa_construction_valid(self):
        """Test de construction d'un DFA valide."""
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {("q0", "a"): "q1", ("q1", "b"): "q2"}
        initial_state = "q0"
        final_states = {"q2"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)

        assert dfa.states == states
        assert dfa.alphabet == alphabet
        assert dfa.initial_state == initial_state
        assert dfa.final_states == final_states
        assert dfa.validate()

    def test_dfa_construction_invalid_initial_state(self):
        """Test de construction d'un DFA avec état initial invalide."""
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q2"  # État non existant
        final_states = {"q1"}

        with self.assertRaises(InvalidDFAError):
            DFA(states, alphabet, transitions, initial_state, final_states)

    def test_dfa_construction_invalid_final_states(self):
        """Test de construction d'un DFA avec états finaux invalides."""
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q2"}  # État non existant

        with self.assertRaises(InvalidDFAError):
            DFA(states, alphabet, transitions, initial_state, final_states)

    def test_dfa_construction_invalid_transitions(self):
        """Test de construction d'un DFA avec transitions invalides."""
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1", ("q2", "a"): "q1"}  # État source invalide
        initial_state = "q0"
        final_states = {"q1"}

        with self.assertRaises(InvalidDFAError):
            DFA(states, alphabet, transitions, initial_state, final_states)

    def test_accepts_word_accepted(self):
        """Test de reconnaissance d'un mot accepté."""
        dfa = self._create_simple_dfa()

        assert dfa.accepts("ab") == True
        # Le DFA simple ne peut accepter que 'ab', pas 'aab' ou 'aaab'

    def test_accepts_word_rejected(self):
        """Test de reconnaissance d'un mot rejeté."""
        dfa = self._create_simple_dfa()

        assert dfa.accepts("a") == False
        assert dfa.accepts("b") == False
        assert dfa.accepts("ba") == False
        assert dfa.accepts("") == False

    def test_accepts_word_invalid_symbol(self):
        """Test de reconnaissance d'un mot avec symbole invalide."""
        dfa = self._create_simple_dfa()

        assert dfa.accepts("ac") == False  # 'c' n'est pas dans l'alphabet
        assert dfa.accepts("abc") == False

    def test_get_transition_existing(self):
        """Test de récupération d'une transition existante."""
        dfa = self._create_simple_dfa()

        assert dfa.get_transition("q0", "a") == "q1"
        assert dfa.get_transition("q1", "b") == "q2"

    def test_get_transition_nonexistent(self):
        """Test de récupération d'une transition inexistante."""
        dfa = self._create_simple_dfa()

        assert dfa.get_transition("q0", "b") is None
        assert dfa.get_transition("q1", "a") is None
        assert dfa.get_transition("q2", "a") is None

    def test_is_final_state(self):
        """Test de vérification des états finaux."""
        dfa = self._create_simple_dfa()

        assert dfa.is_final_state("q2") == True
        assert dfa.is_final_state("q0") == False
        assert dfa.is_final_state("q1") == False

    def test_get_reachable_states(self):
        """Test de récupération des états accessibles."""
        dfa = self._create_simple_dfa()

        reachable = dfa.get_reachable_states()
        assert reachable == {"q0", "q1", "q2"}

    def test_get_reachable_states_with_unreachable(self):
        """Test de récupération des états accessibles avec états inaccessibles."""
        states = {"q0", "q1", "q2", "q3"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): "q1",
            ("q1", "b"): "q2",
            # q3 est inaccessible
        }
        initial_state = "q0"
        final_states = {"q2"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        reachable = dfa.get_reachable_states()

        assert reachable == {"q0", "q1", "q2"}
        assert "q3" not in reachable

    def test_validate_valid_dfa(self):
        """Test de validation d'un DFA valide."""
        dfa = self._create_simple_dfa()
        assert dfa.validate() == True

    def test_validate_invalid_dfa(self):
        """Test de validation d'un DFA invalide."""
        # Créer un DFA valide d'abord
        dfa = self._create_simple_dfa()

        # Modifier les attributs pour rendre le DFA invalide
        dfa._transitions = {("q0", "a"): "q3"}  # q3 n'existe pas
        assert dfa.validate() == False

    def test_minimize_already_minimal(self):
        """Test de minimisation d'un DFA déjà minimal."""
        dfa = self._create_simple_dfa()
        minimal_dfa = dfa.minimize()

        # Le DFA minimal devrait avoir le même nombre d'états
        assert len(minimal_dfa.states) == len(dfa.states)
        assert minimal_dfa.alphabet == dfa.alphabet
        # Les langages acceptés doivent être identiques
        test_words = ["ab", "a", "b", "ba", "aa", "bb"]
        for word in test_words:
            assert dfa.accepts(word) == minimal_dfa.accepts(word)

    def test_minimize_with_redundant_states(self):
        """Test de minimisation d'un DFA avec états redondants."""
        # DFA avec états équivalents
        states = {"q0", "q1", "q2", "q3"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q2",
            ("q1", "a"): "q1",
            ("q1", "b"): "q3",
            ("q2", "a"): "q1",
            ("q2", "b"): "q2",
            ("q3", "a"): "q1",
            ("q3", "b"): "q2",
        }
        initial_state = "q0"
        final_states = {"q3"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        minimal_dfa = dfa.minimize()

        # Le DFA minimal devrait avoir moins d'états
        assert len(minimal_dfa.states) <= len(dfa.states)
        # Les langages acceptés doivent être identiques
        test_words = ["ab", "aab", "ba", "bb", "aabb", "baba"]
        for word in test_words:
            assert dfa.accepts(word) == minimal_dfa.accepts(word)

    def test_remove_unreachable_states(self):
        """Test de suppression des états inaccessibles."""
        states = {"q0", "q1", "q2", "q3"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): "q1",
            ("q1", "b"): "q2",
            # q3 est inaccessible
        }
        initial_state = "q0"
        final_states = {"q2"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        cleaned_dfa = dfa.remove_unreachable_states()

        assert "q3" not in cleaned_dfa.states
        assert cleaned_dfa.states == {"q0", "q1", "q2"}
        # Le langage accepté doit rester identique
        test_words = ["ab", "aab", "ba", "bb"]
        for word in test_words:
            assert dfa.accepts(word) == cleaned_dfa.accepts(word)

    def test_union(self):
        """Test de l'union de deux DFA."""
        dfa1 = self._create_simple_dfa()
        dfa2 = self._create_another_dfa()

        # L'union n'est pas encore implémentée
        with self.assertRaises(NotImplementedError):
            dfa1.union(dfa2)

    def test_intersection(self):
        """Test de l'intersection de deux DFA."""
        dfa1 = self._create_simple_dfa()
        dfa2 = self._create_another_dfa()

        # L'intersection n'est pas encore implémentée
        with self.assertRaises(NotImplementedError):
            dfa1.intersection(dfa2)

    def test_complement(self):
        """Test du complément d'un DFA."""
        dfa = self._create_simple_dfa()

        # Le complément n'est pas encore implémenté
        with self.assertRaises(NotImplementedError):
            dfa.complement()

    def test_concatenation(self):
        """Test de la concaténation de deux DFA."""
        dfa1 = self._create_simple_dfa()
        dfa2 = self._create_another_dfa()

        # La concaténation n'est pas encore implémentée
        with self.assertRaises(NotImplementedError):
            dfa1.concatenation(dfa2)

    def test_kleene_star(self):
        """Test de l'étoile de Kleene d'un DFA."""
        dfa = self._create_simple_dfa()

        # L'étoile de Kleene n'est pas encore implémentée
        with self.assertRaises(NotImplementedError):
            dfa.kleene_star()

    def test_to_dict(self):
        """Test de sérialisation en dictionnaire."""
        dfa = self._create_simple_dfa()
        data = dfa.to_dict()

        assert "states" in data
        assert "alphabet" in data
        assert "transitions" in data
        assert "initial_state" in data
        assert "final_states" in data

        assert set(data["states"]) == dfa.states
        assert set(data["alphabet"]) == dfa.alphabet
        assert data["initial_state"] == dfa.initial_state
        assert set(data["final_states"]) == dfa.final_states

    def test_from_dict(self):
        """Test de désérialisation depuis un dictionnaire."""
        dfa = self._create_simple_dfa()
        data = dfa.to_dict()

        new_dfa = DFA.from_dict(data)

        assert new_dfa.states == dfa.states
        assert new_dfa.alphabet == dfa.alphabet
        assert new_dfa.initial_state == dfa.initial_state
        assert new_dfa.final_states == dfa.final_states

        # Vérifier que les transitions sont identiques
        for (source, symbol), target in dfa._transitions.items():
            assert new_dfa.get_transition(source, symbol) == target

    def test_str_representation(self):
        """Test de la représentation string."""
        dfa = self._create_simple_dfa()
        str_repr = str(dfa)

        assert "DFA" in str_repr
        assert "states=3" in str_repr
        assert "transitions=2" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        dfa = self._create_simple_dfa()
        repr_str = repr(dfa)

        assert "DFA(" in repr_str
        assert "states=" in repr_str
        assert "alphabet=" in repr_str
        assert "initial_state=" in repr_str
        assert "final_states=" in repr_str
        assert "transitions=" in repr_str

    def test_to_nfa_not_implemented(self):
        """Test que la conversion vers NFA n'est pas encore implémentée."""
        dfa = self._create_simple_dfa()

        with self.assertRaises(NotImplementedError):
            dfa.to_nfa()

    def _create_simple_dfa(self) -> DFA:
        """Crée un DFA simple pour les tests."""
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {("q0", "a"): "q1", ("q1", "b"): "q2"}
        initial_state = "q0"
        final_states = {"q2"}

        return DFA(states, alphabet, transitions, initial_state, final_states)

    def _create_another_dfa(self) -> DFA:
        """Crée un autre DFA pour les tests d'opérations."""
        states = {"p0", "p1", "p2"}
        alphabet = {"c", "d"}
        transitions = {("p0", "c"): "p1", ("p1", "d"): "p2"}
        initial_state = "p0"
        final_states = {"p2"}

        return DFA(states, alphabet, transitions, initial_state, final_states)


if __name__ == "__main__":
    unittest.main()
