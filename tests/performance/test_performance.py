"""Tests de performance pour Baobab Automata."""

import pytest
import time
from baobab_automata.finite.dfa import DFA
from baobab_automata.interfaces.state import StateType
from baobab_automata.interfaces.transition import TransitionType
from baobab_automata.implementations.state import State
from baobab_automata.implementations.transition import Transition


@pytest.mark.performance
class TestPerformance:
    """Tests de performance."""

    def test_dfa_creation_performance(self):
        """Test la performance de création d'un DFA."""
        start_time = time.time()

        # Création d'un DFA avec 1000 états
        states = {State(f"q{i}", StateType.INTERMEDIATE) for i in range(1000)}
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q999", StateType.FINAL)}
        alphabet = {"a", "b"}
        transitions = set()

        dfa = DFA(states, initial_states, final_states, alphabet, transitions)

        end_time = time.time()
        creation_time = end_time - start_time

        # Vérification que la création prend moins de 1 seconde
        assert creation_time < 1.0
        assert len(dfa.states) == 1000

    def test_transition_lookup_performance(self):
        """Test la performance de recherche de transitions."""
        # Création d'un DFA avec beaucoup de transitions
        states = {State(f"q{i}", StateType.INTERMEDIATE) for i in range(100)}
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q99", StateType.FINAL)}
        alphabet = {"a", "b", "c"}

        transitions = set()
        for i in range(99):
            for symbol in alphabet:
                transitions.add(
                    Transition(
                        _source_state=State(f"q{i}", StateType.INTERMEDIATE),
                        _target_state=State(f"q{i+1}", StateType.INTERMEDIATE),
                        _symbol=symbol,
                        _transition_type=TransitionType.SYMBOL,
                    )
                )

        dfa = DFA(states, initial_states, final_states, alphabet, transitions)

        # Test de performance de recherche
        start_time = time.time()

        for _ in range(1000):
            dfa.get_transitions(State("q0", StateType.INTERMEDIATE), "a")

        end_time = time.time()
        lookup_time = end_time - start_time

        # Vérification que la recherche prend moins de 1 seconde
        assert lookup_time < 1.0

    @pytest.mark.slow
    def test_large_automaton_performance(self):
        """Test la performance avec un très gros automate."""
        # Création d'un automate avec 10000 états
        states = {State(f"q{i}", StateType.INTERMEDIATE) for i in range(10000)}
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q9999", StateType.FINAL)}
        alphabet = {"a", "b"}
        transitions = set()

        start_time = time.time()

        dfa = DFA(states, initial_states, final_states, alphabet, transitions)

        end_time = time.time()
        creation_time = end_time - start_time

        # Vérification que la création prend moins de 5 secondes
        assert creation_time < 5.0
        assert len(dfa.states) == 10000

    def test_state_creation_performance(self):
        """Test la performance de création d'états."""
        start_time = time.time()

        # Création de 10000 états
        states = []
        for i in range(10000):
            states.append(State(f"q{i}", StateType.INTERMEDIATE))

        end_time = time.time()
        creation_time = end_time - start_time

        # Vérification que la création prend moins de 0.5 seconde
        assert creation_time < 0.5
        assert len(states) == 10000

    def test_transition_creation_performance(self):
        """Test la performance de création de transitions."""
        # Créer des états pour les transitions
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(1000)]

        start_time = time.time()

        # Création de 5000 transitions
        transitions = []
        for i in range(5000):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transitions.append(
                Transition(
                    _source_state=source,
                    _target_state=target,
                    _symbol="a",
                    _transition_type=TransitionType.SYMBOL,
                )
            )

        end_time = time.time()
        creation_time = end_time - start_time

        # Vérification que la création prend moins de 1 seconde
        assert creation_time < 1.0
        assert len(transitions) == 5000

    def test_dfa_validation_performance(self):
        """Test la performance de validation d'un DFA."""
        # Créer un DFA avec beaucoup d'états et de transitions
        states = {State(f"q{i}", StateType.INTERMEDIATE) for i in range(500)}
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q499", StateType.FINAL)}
        alphabet = {"a", "b", "c", "d"}

        transitions = set()
        for i in range(499):
            for symbol in alphabet:
                transitions.add(
                    Transition(
                        _source_state=State(f"q{i}", StateType.INTERMEDIATE),
                        _target_state=State(f"q{i+1}", StateType.INTERMEDIATE),
                        _symbol=symbol,
                        _transition_type=TransitionType.SYMBOL,
                    )
                )

        dfa = DFA(states, initial_states, final_states, alphabet, transitions)

        start_time = time.time()

        # Validation multiple
        for _ in range(100):
            dfa.is_valid()

        end_time = time.time()
        validation_time = end_time - start_time

        # Vérification que la validation prend moins de 2 secondes
        assert validation_time < 2.0

    def test_dfa_serialization_performance(self):
        """Test la performance de sérialisation d'un DFA."""
        # Créer un DFA avec beaucoup d'états et de transitions
        states = {State(f"q{i}", StateType.INTERMEDIATE) for i in range(200)}
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q199", StateType.FINAL)}
        alphabet = {"a", "b", "c"}

        transitions = set()
        for i in range(199):
            for symbol in alphabet:
                transitions.add(
                    Transition(
                        _source_state=State(f"q{i}", StateType.INTERMEDIATE),
                        _target_state=State(f"q{i+1}", StateType.INTERMEDIATE),
                        _symbol=symbol,
                        _transition_type=TransitionType.SYMBOL,
                    )
                )

        dfa = DFA(states, initial_states, final_states, alphabet, transitions)

        start_time = time.time()

        # Sérialisation multiple
        for _ in range(50):
            data = dfa.to_dict()

        end_time = time.time()
        serialization_time = end_time - start_time

        # Vérification que la sérialisation prend moins de 1 seconde
        assert serialization_time < 1.0
        assert isinstance(data, dict)

    def test_memory_usage_performance(self):
        """Test l'utilisation mémoire avec de gros automates."""
        import sys

        # Mesurer la mémoire avant
        initial_memory = sys.getsizeof([])

        # Créer un gros automate
        states = {State(f"q{i}", StateType.INTERMEDIATE) for i in range(1000)}
        initial_states = {State("q0", StateType.INITIAL)}
        final_states = {State("q999", StateType.FINAL)}
        alphabet = {"a", "b", "c", "d", "e"}

        transitions = set()
        for i in range(999):
            for symbol in alphabet:
                transitions.add(
                    Transition(
                        _source_state=State(f"q{i}", StateType.INTERMEDIATE),
                        _target_state=State(f"q{i+1}", StateType.INTERMEDIATE),
                        _symbol=symbol,
                        _transition_type=TransitionType.SYMBOL,
                    )
                )

        dfa = DFA(states, initial_states, final_states, alphabet, transitions)

        # Mesurer la mémoire après
        final_memory = sys.getsizeof(dfa)
        memory_usage = final_memory - initial_memory

        # Vérifier que l'utilisation mémoire est raisonnable (moins de 10MB)
        assert memory_usage < 10 * 1024 * 1024  # 10MB en bytes
