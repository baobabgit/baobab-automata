"""Tests de performance pour les automates."""

import time
import pytest
from baobab_automata.automata.finite.dfa import DFA


@pytest.mark.performance
class TestPerformance:
    """Tests de performance."""

    def test_dfa_creation_performance(self):
        """Test la performance de création d'un DFA."""
        start_time = time.time()

        # Création d'un DFA avec 1000 états
        states = {f"q{i}" for i in range(1000)}
        alphabet = {"a", "b"}
        transitions = {}
        initial_state = "q0"
        final_states = {"q999"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)

        creation_time = time.time() - start_time
        assert creation_time < 1.0  # Doit être créé en moins d'une seconde
        assert len(dfa.states) == 1000

    def test_transition_lookup_performance(self):
        """Test la performance de recherche de transitions."""
        # Création d'un DFA avec beaucoup de transitions
        states = {f"q{i}" for i in range(100)}
        alphabet = {"a", "b", "c"}
        transitions = {}
        for i in range(99):
            for symbol in alphabet:
                transitions[(f"q{i}", symbol)] = f"q{i+1}"

        initial_state = "q0"
        final_states = {"q99"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)

        # Test de performance de recherche
        start_time = time.time()
        for _ in range(1000):
            dfa.get_transition("q50", "a")
        lookup_time = time.time() - start_time

        assert lookup_time < 0.1  # Doit être rapide
        assert dfa.get_transition("q50", "a") == "q51"

    @pytest.mark.slow
    def test_large_automaton_performance(self):
        """Test la performance avec un très gros automate."""
        # Création d'un automate avec 10000 états
        states = {f"q{i}" for i in range(10000)}
        alphabet = {"a", "b"}
        transitions = {}
        initial_state = "q0"
        final_states = {"q9999"}

        start_time = time.time()

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)

        creation_time = time.time() - start_time
        assert creation_time < 5.0  # Doit être créé en moins de 5 secondes
        assert len(dfa.states) == 10000

    def test_state_creation_performance(self):
        """Test la performance de création d'états."""
        start_time = time.time()

        # Création de 10000 états
        states = {f"q{i}" for i in range(10000)}

        creation_time = time.time() - start_time
        assert creation_time < 0.1  # Doit être très rapide
        assert len(states) == 10000

    def test_transition_creation_performance(self):
        """Test la performance de création de transitions."""
        start_time = time.time()

        # Création de 10000 transitions
        transitions = {}
        for i in range(10000):
            transitions[(f"q{i}", "a")] = f"q{i+1}"

        creation_time = time.time() - start_time
        assert creation_time < 0.1  # Doit être très rapide
        assert len(transitions) == 10000

    def test_dfa_validation_performance(self):
        """Test la performance de validation d'un DFA."""
        # Créer un DFA avec beaucoup d'états et de transitions
        states = {f"q{i}" for i in range(500)}
        alphabet = {"a", "b", "c", "d"}
        transitions = {}
        for i in range(499):
            for symbol in alphabet:
                transitions[(f"q{i}", symbol)] = f"q{i+1}"

        initial_state = "q0"
        final_states = {"q499"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)

        # Test de performance de validation
        start_time = time.time()
        for _ in range(100):
            dfa.validate()
        validation_time = time.time() - start_time

        assert validation_time < 1.0  # Doit être rapide
        assert dfa.validate()

    def test_dfa_serialization_performance(self):
        """Test la performance de sérialisation d'un DFA."""
        # Créer un DFA avec beaucoup d'états et de transitions
        states = {f"q{i}" for i in range(200)}
        alphabet = {"a", "b", "c"}
        transitions = {}
        for i in range(199):
            for symbol in alphabet:
                transitions[(f"q{i}", symbol)] = f"q{i+1}"

        initial_state = "q0"
        final_states = {"q199"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)

        # Test de performance de sérialisation
        start_time = time.time()
        for _ in range(100):
            dfa.to_dict()
        serialization_time = time.time() - start_time

        assert serialization_time < 1.0  # Doit être rapide

    def test_memory_usage_performance(self):
        """Test l'utilisation mémoire avec de gros automates."""
        import sys

        # Mesurer la mémoire avant
        initial_memory = sys.getsizeof([])

        # Créer un gros automate
        states = {f"q{i}" for i in range(1000)}
        alphabet = {"a", "b", "c", "d", "e"}
        transitions = {}
        for i in range(999):
            for symbol in alphabet:
                transitions[(f"q{i}", symbol)] = f"q{i+1}"

        initial_state = "q0"
        final_states = {"q999"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)

        # Mesurer la mémoire après
        final_memory = sys.getsizeof(dfa)

        # Vérifier que l'utilisation mémoire est raisonnable
        memory_usage = final_memory - initial_memory
        assert memory_usage < 1000000  # Moins de 1MB pour 1000 états