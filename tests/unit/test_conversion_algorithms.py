"""Tests unitaires pour la classe ConversionAlgorithms."""

import pytest
from baobab_automata.algorithms.finite.conversion_algorithms import ConversionAlgorithms
from baobab_automata.finite.dfa import DFA
from baobab_automata.finite.nfa import NFA
from baobab_automata.finite.epsilon_nfa import EpsilonNFA


@pytest.mark.unit
class TestConversionAlgorithms:
    """Tests pour la classe ConversionAlgorithms."""

    def test_class_initialization(self):
        """Test l'initialisation de la classe."""
        # La classe est statique, on peut l'instancier
        converter = ConversionAlgorithms()
        assert converter is not None

    def test_nfa_to_dfa_simple(self):
        """Test la conversion NFA vers DFA simple."""
        # Créer un NFA simple
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "b"): {"q0"},
            },
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == nfa.alphabet

    def test_nfa_to_dfa_minimal(self):
        """Test la conversion NFA vers DFA minimal."""
        # Créer un NFA minimal
        nfa = NFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states=set(),
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == nfa.alphabet

    def test_nfa_to_dfa_single_state(self):
        """Test la conversion NFA vers DFA avec un seul état."""
        # Créer un NFA avec un seul état
        nfa = NFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == nfa.alphabet

    def test_nfa_to_dfa_no_transitions(self):
        """Test la conversion NFA vers DFA sans transitions."""
        # Créer un NFA sans transitions
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={},
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == nfa.alphabet

    def test_nfa_to_dfa_large_alphabet(self):
        """Test la conversion NFA vers DFA avec un grand alphabet."""
        # Créer un NFA avec un grand alphabet
        large_alphabet = {chr(i) for i in range(ord('a'), ord('z') + 1)}
        nfa = NFA(
            states={"q0", "q1"},
            alphabet=large_alphabet,
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "z"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == nfa.alphabet

    def test_nfa_to_dfa_multiple_final_states(self):
        """Test la conversion NFA vers DFA avec plusieurs états finaux."""
        # Créer un NFA avec plusieurs états finaux
        nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "b"): {"q2"},
            },
            initial_state="q0",
            final_states={"q1", "q2"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == nfa.alphabet

    def test_nfa_to_dfa_self_loops(self):
        """Test la conversion NFA vers DFA avec des boucles sur soi."""
        # Créer un NFA avec des boucles sur soi
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q0", "q1"},
                ("q1", "b"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == nfa.alphabet

    def test_nfa_to_dfa_cycle(self):
        """Test la conversion NFA vers DFA avec un cycle."""
        # Créer un NFA avec un cycle
        nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "a"): {"q0"},
            },
            initial_state="q0",
            final_states={"q2"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == nfa.alphabet

    def test_nfa_to_dfa_complex_cycle(self):
        """Test la conversion NFA vers DFA avec un cycle complexe."""
        # Créer un NFA avec un cycle complexe
        nfa = NFA(
            states={"q0", "q1", "q2", "q3", "q4"},
            alphabet={"a", "b", "c"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "c"): {"q3"},
                ("q3", "a"): {"q4"},
                ("q4", "b"): {"q0"},
            },
            initial_state="q0",
            final_states={"q4"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == nfa.alphabet

    def test_epsilon_nfa_to_nfa_simple(self):
        """Test la conversion Epsilon-NFA vers NFA simple."""
        # Créer un Epsilon-NFA simple
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_with_epsilon_transitions(self):
        """Test la conversion Epsilon-NFA vers NFA avec transitions epsilon."""
        # Créer un Epsilon-NFA avec transitions epsilon
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "ε"): {"q3"},
            },
            initial_state="q0",
            final_states={"q3"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_complex(self):
        """Test la conversion Epsilon-NFA vers NFA complexe."""
        # Créer un Epsilon-NFA complexe
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3", "q4"},
            alphabet={"a", "b", "c"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "ε"): {"q3"},
                ("q3", "c"): {"q4"},
                ("q4", "ε"): {"q0"},
            },
            initial_state="q0",
            final_states={"q4"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_minimal(self):
        """Test la conversion Epsilon-NFA vers NFA minimal."""
        # Créer un Epsilon-NFA minimal
        epsilon_nfa = EpsilonNFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states=set(),
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_single_state(self):
        """Test la conversion Epsilon-NFA vers NFA avec un seul état."""
        # Créer un Epsilon-NFA avec un seul état
        epsilon_nfa = EpsilonNFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_no_transitions(self):
        """Test la conversion Epsilon-NFA vers NFA sans transitions."""
        # Créer un Epsilon-NFA sans transitions
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={},
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_large_alphabet(self):
        """Test la conversion Epsilon-NFA vers NFA avec un grand alphabet."""
        # Créer un Epsilon-NFA avec un grand alphabet
        large_alphabet = {chr(i) for i in range(ord('a'), ord('z') + 1)}
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet=large_alphabet,
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "z"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_multiple_final_states(self):
        """Test la conversion Epsilon-NFA vers NFA avec plusieurs états finaux."""
        # Créer un Epsilon-NFA avec plusieurs états finaux
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "b"): {"q2"},
            },
            initial_state="q0",
            final_states={"q1", "q2"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_self_loops(self):
        """Test la conversion Epsilon-NFA vers NFA avec des boucles sur soi."""
        # Créer un Epsilon-NFA avec des boucles sur soi
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q0", "q1"},
                ("q1", "b"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_cycle(self):
        """Test la conversion Epsilon-NFA vers NFA avec un cycle."""
        # Créer un Epsilon-NFA avec un cycle
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "a"): {"q0"},
            },
            initial_state="q0",
            final_states={"q2"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_nfa_complex_cycle(self):
        """Test la conversion Epsilon-NFA vers NFA avec un cycle complexe."""
        # Créer un Epsilon-NFA avec un cycle complexe
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3", "q4"},
            alphabet={"a", "b", "c"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "c"): {"q3"},
                ("q3", "a"): {"q4"},
                ("q4", "b"): {"q0"},
            },
            initial_state="q0",
            final_states={"q4"},
        )
        
        # Convertir en NFA
        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)
        
        assert isinstance(nfa, NFA)
        assert nfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_direct(self):
        """Test la conversion directe Epsilon-NFA vers DFA."""
        # Créer un Epsilon-NFA
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )
        
        # Convertir directement en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_with_epsilon_transitions(self):
        """Test la conversion Epsilon-NFA vers DFA avec transitions epsilon."""
        # Créer un Epsilon-NFA avec transitions epsilon
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "ε"): {"q3"},
            },
            initial_state="q0",
            final_states={"q3"},
        )
        
        # Convertir directement en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_complex(self):
        """Test la conversion Epsilon-NFA vers DFA complexe."""
        # Créer un Epsilon-NFA complexe
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3", "q4"},
            alphabet={"a", "b", "c"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "ε"): {"q3"},
                ("q3", "c"): {"q4"},
                ("q4", "ε"): {"q0"},
            },
            initial_state="q0",
            final_states={"q4"},
        )
        
        # Convertir directement en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_minimal(self):
        """Test la conversion Epsilon-NFA vers DFA minimal."""
        # Créer un Epsilon-NFA minimal
        epsilon_nfa = EpsilonNFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states=set(),
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_single_state(self):
        """Test la conversion Epsilon-NFA vers DFA avec un seul état."""
        # Créer un Epsilon-NFA avec un seul état
        epsilon_nfa = EpsilonNFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_no_transitions(self):
        """Test la conversion Epsilon-NFA vers DFA sans transitions."""
        # Créer un Epsilon-NFA sans transitions
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={},
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_large_alphabet(self):
        """Test la conversion Epsilon-NFA vers DFA avec un grand alphabet."""
        # Créer un Epsilon-NFA avec un grand alphabet
        large_alphabet = {chr(i) for i in range(ord('a'), ord('z') + 1)}
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet=large_alphabet,
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "z"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_multiple_final_states(self):
        """Test la conversion Epsilon-NFA vers DFA avec plusieurs états finaux."""
        # Créer un Epsilon-NFA avec plusieurs états finaux
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "b"): {"q2"},
            },
            initial_state="q0",
            final_states={"q1", "q2"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_self_loops(self):
        """Test la conversion Epsilon-NFA vers DFA avec des boucles sur soi."""
        # Créer un Epsilon-NFA avec des boucles sur soi
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q0", "q1"},
                ("q1", "b"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_cycle(self):
        """Test la conversion Epsilon-NFA vers DFA avec un cycle."""
        # Créer un Epsilon-NFA avec un cycle
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "a"): {"q0"},
            },
            initial_state="q0",
            final_states={"q2"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet

    def test_epsilon_nfa_to_dfa_complex_cycle(self):
        """Test la conversion Epsilon-NFA vers DFA avec un cycle complexe."""
        # Créer un Epsilon-NFA avec un cycle complexe
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3", "q4"},
            alphabet={"a", "b", "c"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "b"): {"q2"},
                ("q2", "c"): {"q3"},
                ("q3", "a"): {"q4"},
                ("q4", "b"): {"q0"},
            },
            initial_state="q0",
            final_states={"q4"},
        )
        
        # Convertir en DFA
        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)
        
        assert isinstance(dfa, DFA)
        assert dfa.alphabet == epsilon_nfa.alphabet