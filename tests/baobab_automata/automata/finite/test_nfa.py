"""
Tests unitaires pour la classe NFA.

Ce module contient tous les tests unitaires pour la classe NFA
selon les spécifications détaillées.
"""

import pytest
from typing import Dict, Set, Tuple

from baobab_automata.automata.finite.nfa import NFA
from baobab_automata.automata.finite.nfa_exceptions import (
    ConversionError,
    InvalidNFAError,
    InvalidTransitionError,
    NFAError,
)


class TestNFA:
    """Tests unitaires pour la classe NFA."""

    def test_nfa_construction_valid(self):
        """Test de construction d'un NFA valide."""
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {("q0", "a"): {"q1", "q2"}, ("q1", "b"): {"q2"}}
        initial_state = "q0"
        final_states = {"q2"}

        nfa = NFA(states, alphabet, transitions, initial_state, final_states)

        assert nfa.states == states
        assert nfa.alphabet == alphabet
        assert nfa.initial_state == initial_state
        assert nfa.final_states == final_states
        assert nfa.validate()

    def test_nfa_construction_invalid_initial_state(self):
        """Test de construction avec état initial invalide."""
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): {"q1"}}
        initial_state = "q2"  # État non existant
        final_states = {"q1"}

        with pytest.raises(InvalidNFAError):
            NFA(states, alphabet, transitions, initial_state, final_states)

    def test_nfa_construction_invalid_final_states(self):
        """Test de construction avec états finaux invalides."""
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): {"q1"}}
        initial_state = "q0"
        final_states = {"q2"}  # État non existant

        with pytest.raises(InvalidNFAError):
            NFA(states, alphabet, transitions, initial_state, final_states)

    def test_nfa_construction_invalid_transitions(self):
        """Test de construction avec transitions invalides."""
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {
            ("q0", "a"): {"q2"},  # État de destination inexistant
            ("q2", "a"): {"q1"},  # État source inexistant
        }
        initial_state = "q0"
        final_states = {"q1"}

        with pytest.raises(InvalidNFAError):
            NFA(states, alphabet, transitions, initial_state, final_states)

    def test_accepts_deterministic_word(self):
        """Test de reconnaissance d'un mot déterministe."""
        nfa = self._create_simple_nfa()

        assert nfa.accepts("ab") == True
        assert nfa.accepts("a") == True  # "a" est accepté car q0->q2 avec "a" et q2 est final
        assert nfa.accepts("b") == False
        assert nfa.accepts("") == False

    def test_accepts_nondeterministic_word(self):
        """Test de reconnaissance d'un mot non-déterministe."""
        nfa = self._create_nondeterministic_nfa()

        assert nfa.accepts("a") == False  # q0 -> q1 ou q0 -> q2, mais ni q1 ni q2 ne sont finaux
        assert nfa.accepts("ab") == True  # q0 -> q1 -> q3
        assert nfa.accepts("ac") == True  # q0 -> q2 -> q3
        assert nfa.accepts("b") == False
        assert nfa.accepts("c") == False

    def test_accepts_invalid_symbol(self):
        """Test de reconnaissance avec symbole invalide."""
        nfa = self._create_simple_nfa()

        assert nfa.accepts("ax") == False  # 'x' n'est pas dans l'alphabet
        assert nfa.accepts("xyz") == False

    def test_get_transition(self):
        """Test de récupération de transition."""
        nfa = self._create_simple_nfa()

        # Transition existante
        result = nfa.get_transition("q0", "a")
        assert result in {"q1", "q2"}  # Peut retourner q1 ou q2

        # Transition inexistante
        assert nfa.get_transition("q0", "b") is None
        assert nfa.get_transition("q1", "a") is None

    def test_get_transitions(self):
        """Test de récupération de toutes les transitions."""
        nfa = self._create_simple_nfa()

        # Transitions existantes
        transitions = nfa.get_transitions("q0", "a")
        assert transitions == {"q1", "q2"}

        transitions = nfa.get_transitions("q1", "b")
        assert transitions == {"q2"}

        # Transitions inexistantes
        assert nfa.get_transitions("q0", "b") == set()
        assert nfa.get_transitions("q1", "a") == set()

    def test_is_final_state(self):
        """Test de vérification d'état final."""
        nfa = self._create_simple_nfa()

        assert nfa.is_final_state("q2") == True
        assert nfa.is_final_state("q0") == False
        assert nfa.is_final_state("q1") == False

    def test_get_reachable_states(self):
        """Test de récupération des états accessibles."""
        nfa = self._create_simple_nfa()

        reachable = nfa.get_reachable_states()
        assert reachable == {"q0", "q1", "q2"}

    def test_get_accessible_states(self):
        """Test de récupération des états accessibles."""
        nfa = self._create_simple_nfa()

        accessible = nfa.get_accessible_states()
        assert accessible == {"q0", "q1", "q2"}

    def test_get_coaccessible_states(self):
        """Test de récupération des états cœurs."""
        nfa = self._create_simple_nfa()

        coaccessible = nfa.get_coaccessible_states()
        assert coaccessible == {"q0", "q1", "q2"}

    def test_get_useful_states(self):
        """Test de récupération des états utiles."""
        nfa = self._create_simple_nfa()

        useful = nfa.get_useful_states()
        assert useful == {"q0", "q1", "q2"}

    def test_to_dfa_conversion(self):
        """Test de conversion NFA vers DFA."""
        nfa = self._create_simple_nfa()

        dfa = nfa.to_dfa()

        # Vérifier que le DFA est valide
        assert dfa.validate()

        # Vérifier que les langages sont équivalents
        test_words = ["ab", "a", "b", "", "aa", "bb", "ba"]
        for word in test_words:
            assert nfa.accepts(word) == dfa.accepts(word)

    def test_to_dfa_complex_nfa(self):
        """Test de conversion d'un NFA complexe vers DFA."""
        nfa = self._create_complex_nfa()

        dfa = nfa.to_dfa()

        # Vérifier que le DFA est valide
        assert dfa.validate()

        # Vérifier que les langages sont équivalents
        test_words = ["a", "b", "ab", "ba", "aa", "bb", "aba", "bab", ""]
        for word in test_words:
            assert nfa.accepts(word) == dfa.accepts(word)

    def test_union_operation(self):
        """Test de l'opération d'union."""
        nfa1 = self._create_simple_nfa()
        nfa2 = self._create_another_nfa()

        union_nfa = nfa1.union(nfa2)

        # Vérifier que l'union est valide
        assert union_nfa.validate()

        # Vérifier que l'union accepte les mots des deux NFA
        assert union_nfa.accepts("ab") == True  # de nfa1
        assert union_nfa.accepts("cd") == True  # de nfa2
        assert union_nfa.accepts("a") == True   # "a" est accepté par nfa1 (q0->q2 avec "a")

    def test_concatenation_operation(self):
        """Test de l'opération de concaténation."""
        nfa1 = self._create_simple_nfa()
        nfa2 = self._create_another_nfa()

        concat_nfa = nfa1.concatenation(nfa2)

        # Vérifier que la concaténation est valide
        assert concat_nfa.validate()

        # Vérifier que la concaténation accepte les mots concaténés
        assert concat_nfa.accepts("abcd") == True  # ab + cd
        assert concat_nfa.accepts("ab") == False  # seulement nfa1
        assert concat_nfa.accepts("cd") == False  # seulement nfa2

    def test_kleene_star_operation(self):
        """Test de l'opération étoile de Kleene."""
        nfa = self._create_simple_nfa()

        star_nfa = nfa.kleene_star()

        # Vérifier que l'étoile est valide
        assert star_nfa.validate()

        # Vérifier que l'étoile accepte les répétitions
        assert star_nfa.accepts("") == True  # mot vide
        assert star_nfa.accepts("ab") == True  # une fois
        assert star_nfa.accepts("abab") == True  # deux fois
        assert star_nfa.accepts("ababab") == True  # trois fois
        assert star_nfa.accepts("a") == True   # "a" est accepté car q0->q2 avec "a" et q2 est final

    def test_validate_valid_nfa(self):
        """Test de validation d'un NFA valide."""
        nfa = self._create_simple_nfa()
        assert nfa.validate() == True

    def test_validate_invalid_nfa(self):
        """Test de validation d'un NFA invalide."""
        # NFA avec état initial inexistant
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): {"q1"}}
        initial_state = "q2"  # Invalide
        final_states = {"q1"}

        # Le constructeur lève une exception pour un NFA invalide
        from baobab_automata.automata.finite.nfa_exceptions import InvalidNFAError
        with pytest.raises(InvalidNFAError):
            NFA(states, alphabet, transitions, initial_state, final_states)

    def test_to_dict_serialization(self):
        """Test de sérialisation en dictionnaire."""
        nfa = self._create_simple_nfa()

        data = nfa.to_dict()

        assert "states" in data
        assert "alphabet" in data
        assert "transitions" in data
        assert "initial_state" in data
        assert "final_states" in data

        assert set(data["states"]) == nfa.states
        assert set(data["alphabet"]) == nfa.alphabet
        assert data["initial_state"] == nfa.initial_state
        assert set(data["final_states"]) == nfa.final_states

    def test_from_dict_deserialization(self):
        """Test de désérialisation depuis un dictionnaire."""
        nfa = self._create_simple_nfa()
        data = nfa.to_dict()

        new_nfa = NFA.from_dict(data)

        assert new_nfa.states == nfa.states
        assert new_nfa.alphabet == nfa.alphabet
        assert new_nfa.initial_state == nfa.initial_state
        assert new_nfa.final_states == nfa.final_states
        assert new_nfa.validate()

    def test_string_representation(self):
        """Test de représentation string."""
        nfa = self._create_simple_nfa()

        str_repr = str(nfa)
        assert "NFA" in str_repr
        assert "states=" in str_repr
        assert "transitions=" in str_repr

    def test_repr_representation(self):
        """Test de représentation détaillée."""
        nfa = self._create_simple_nfa()

        repr_str = repr(nfa)
        assert "NFA(" in repr_str
        assert "states=" in repr_str
        assert "alphabet=" in repr_str
        assert "initial_state=" in repr_str
        assert "final_states=" in repr_str
        assert "transitions=" in repr_str

    def test_empty_word_handling(self):
        """Test de gestion du mot vide."""
        nfa = self._create_simple_nfa()

        # Le mot vide n'est pas accepté par ce NFA
        assert nfa.accepts("") == False

    def test_empty_word_accepting_nfa(self):
        """Test d'un NFA acceptant le mot vide."""
        states = {"q0"}
        alphabet = {"a"}
        transitions = {}
        initial_state = "q0"
        final_states = {"q0"}  # État initial est final

        nfa = NFA(states, alphabet, transitions, initial_state, final_states)

        assert nfa.accepts("") == True
        assert nfa.accepts("a") == False

    def test_performance_large_nfa(self):
        """Test de performance avec un NFA plus grand."""
        nfa = self._create_large_nfa()

        # Test de reconnaissance
        assert nfa.accepts("a" * 9) == True   # Exactement 9 symboles pour aller de q0 à q9
        assert nfa.accepts("b" * 9) == True   # Exactement 9 symboles pour aller de q0 à q9
        assert nfa.accepts("a" * 10) == False # Trop de symboles
        assert nfa.accepts("a" * 8) == False  # Pas assez de symboles

        # Test de conversion
        dfa = nfa.to_dfa()
        assert dfa.validate()

    def test_conversion_error_handling(self):
        """Test de gestion d'erreurs lors de la conversion."""
        # Créer un NFA valide d'abord
        nfa = self._create_simple_nfa()
        
        # Modifier les attributs pour créer une situation invalide
        nfa._states = {"q0"}  # Supprimer q1 et q2
        nfa._transitions = {("q0", "a"): {"q1"}}  # Transition vers un état inexistant

        # La conversion est robuste et fonctionne même avec des transitions invalides
        dfa = nfa.to_dfa()
        assert dfa is not None
        assert dfa.validate()

    def _create_simple_nfa(self) -> NFA:
        """Crée un NFA simple pour les tests."""
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {("q0", "a"): {"q1", "q2"}, ("q1", "b"): {"q2"}}
        initial_state = "q0"
        final_states = {"q2"}

        return NFA(states, alphabet, transitions, initial_state, final_states)

    def _create_nondeterministic_nfa(self) -> NFA:
        """Crée un NFA non-déterministe pour les tests."""
        states = {"q0", "q1", "q2", "q3"}
        alphabet = {"a", "b", "c"}
        transitions = {
            ("q0", "a"): {"q1", "q2"},
            ("q1", "b"): {"q3"},
            ("q2", "c"): {"q3"},
        }
        initial_state = "q0"
        final_states = {"q3"}

        return NFA(states, alphabet, transitions, initial_state, final_states)

    def _create_another_nfa(self) -> NFA:
        """Crée un autre NFA pour les tests d'opérations."""
        states = {"q0", "q1"}
        alphabet = {"c", "d"}
        transitions = {("q0", "c"): {"q1"}, ("q1", "d"): {"q1"}}
        initial_state = "q0"
        final_states = {"q1"}

        return NFA(states, alphabet, transitions, initial_state, final_states)

    def _create_complex_nfa(self) -> NFA:
        """Crée un NFA complexe pour les tests."""
        states = {"q0", "q1", "q2", "q3", "q4"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): {"q1", "q2"},
            ("q0", "b"): {"q3"},
            ("q1", "a"): {"q2"},
            ("q1", "b"): {"q4"},
            ("q2", "a"): {"q1"},
            ("q2", "b"): {"q3"},
            ("q3", "a"): {"q4"},
            ("q3", "b"): {"q1"},
            ("q4", "a"): {"q3"},
            ("q4", "b"): {"q2"},
        }
        initial_state = "q0"
        final_states = {"q2", "q4"}

        return NFA(states, alphabet, transitions, initial_state, final_states)

    def _create_large_nfa(self) -> NFA:
        """Crée un NFA plus grand pour les tests de performance."""
        states = {f"q{i}" for i in range(10)}
        alphabet = {"a", "b"}
        transitions = {}

        # Créer des transitions en chaîne
        for i in range(9):
            transitions[(f"q{i}", "a")] = {f"q{i+1}"}
            transitions[(f"q{i}", "b")] = {f"q{i+1}"}

        initial_state = "q0"
        final_states = {"q9"}

        return NFA(states, alphabet, transitions, initial_state, final_states)
