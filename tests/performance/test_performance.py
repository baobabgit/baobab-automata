"""
Tests de performance pour Baobab Automata.

Ce module contient les tests de performance et de benchmark pour
vérifier que les implémentations respectent les contraintes de performance.
"""

import gc
import pytest
import time
from baobab_automata.implementations.state import State
from baobab_automata.implementations.transition import Transition
from baobab_automata.interfaces.state import StateType
from baobab_automata.interfaces.transition import TransitionType


class TestPerformance:
    """Tests de performance."""
    
    @pytest.mark.performance
    def test_state_creation_performance(self):
        """Test la performance de création d'états."""
        start_time = time.time()
        
        # Création de 10000 états
        states = []
        for i in range(10000):
            state = State(f"q{i}", StateType.INTERMEDIATE)
            states.append(state)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        # Vérification que la création prend moins de 1 seconde
        assert creation_time < 1.0
        assert len(states) == 10000
    
    @pytest.mark.performance
    def test_transition_creation_performance(self):
        """Test la performance de création de transitions."""
        # Création d'états de base
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(100)]
        
        start_time = time.time()
        
        # Création de 10000 transitions
        transitions = []
        for i in range(10000):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            )
            transitions.append(transition)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        # Vérification que la création prend moins de 1 seconde
        assert creation_time < 1.0
        assert len(transitions) == 10000
    
    @pytest.mark.performance
    def test_state_hash_performance(self):
        """Test la performance de hachage des états."""
        # Création d'états
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(1000)]
        
        start_time = time.time()
        
        # Test de hachage répété
        for _ in range(10000):
            for state in states:
                hash(state)
        
        end_time = time.time()
        hash_time = end_time - start_time
        
        # Vérification que le hachage prend moins de 25 secondes
        assert hash_time < 25.0
    
    @pytest.mark.performance
    def test_transition_hash_performance(self):
        """Test la performance de hachage des transitions."""
        # Création d'états et transitions
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(100)]
        transitions = []
        for i in range(1000):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            )
            transitions.append(transition)
        
        start_time = time.time()
        
        # Test de hachage répété
        for _ in range(1000):
            for transition in transitions:
                hash(transition)
        
        end_time = time.time()
        hash_time = end_time - start_time
        
        # Vérification que le hachage prend moins de 25 secondes
        assert hash_time < 25.0
    
    @pytest.mark.performance
    def test_state_equality_performance(self):
        """Test la performance de comparaison d'états."""
        # Création d'états
        states1 = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(100)]
        states2 = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(100)]
        
        start_time = time.time()
        
        # Test de comparaison répété
        for _ in range(1000):
            for state1, state2 in zip(states1, states2):
                state1 == state2
        
        end_time = time.time()
        comparison_time = end_time - start_time
        
        # Vérification que la comparaison prend moins de 0.3 seconde
        assert comparison_time < 0.3
    
    @pytest.mark.performance
    def test_transition_equality_performance(self):
        """Test la performance de comparaison de transitions."""
        # Création d'états et transitions
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(50)]
        transitions1 = []
        transitions2 = []
        
        for i in range(500):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transition1 = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            )
            transition2 = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            )
            transitions1.append(transition1)
            transitions2.append(transition2)
        
        start_time = time.time()
        
        # Test de comparaison répété
        for _ in range(100):
            for trans1, trans2 in zip(transitions1, transitions2):
                trans1 == trans2
        
        end_time = time.time()
        comparison_time = end_time - start_time
        
        # Vérification que la comparaison prend moins de 0.3 seconde
        assert comparison_time < 0.3
    
    @pytest.mark.performance
    def test_is_applicable_performance(self):
        """Test la performance de is_applicable."""
        # Création d'états et transitions
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(100)]
        transitions = []
        
        for i in range(1000):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            )
            transitions.append(transition)
        
        start_time = time.time()
        
        # Test de is_applicable répété
        for _ in range(100):
            for transition in transitions:
                transition.is_applicable("a", {})
        
        end_time = time.time()
        applicable_time = end_time - start_time
        
        # Vérification que is_applicable prend moins de 0.5 seconde
        assert applicable_time < 0.5
    
    @pytest.mark.performance
    def test_execute_performance(self):
        """Test la performance de execute."""
        # Création d'états et transitions
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(100)]
        transitions = []
        
        for i in range(1000):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL,
                _actions={"counter": i}
            )
            transitions.append(transition)
        
        start_time = time.time()
        
        # Test de execute répété
        context = {"initial": "value"}
        for _ in range(100):
            for transition in transitions:
                transition.execute(context)
        
        end_time = time.time()
        execute_time = end_time - start_time
        
        # Vérification que execute prend moins de 0.5 seconde
        assert execute_time < 0.5
    
    @pytest.mark.slow
    def test_large_scale_performance(self):
        """Test la performance à grande échelle."""
        # Création d'un grand nombre d'états et transitions
        start_time = time.time()
        
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(1000)]
        transitions = []
        
        for i in range(10000):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            )
            transitions.append(transition)
        
        # Test des opérations de base
        for state in states:
            hash(state)
            str(state)
            state.is_initial()
            state.is_final()
            state.is_accepting()
        
        for transition in transitions:
            hash(transition)
            str(transition)
            transition.is_applicable("a", {})
            transition.execute({})
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Vérification que l'ensemble prend moins de 5 secondes
        assert total_time < 5.0
        assert len(states) == 1000
        assert len(transitions) == 10000
    
    @pytest.mark.performance
    def test_memory_efficiency(self):
        """Test l'efficacité mémoire."""
        import sys
        
        # Mesure de la mémoire avant création
        initial_objects = len(gc.get_objects())
        
        # Création d'un grand nombre d'objets
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(1000)]
        transitions = []
        
        for i in range(1000):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            )
            transitions.append(transition)
        
        # Mesure de la mémoire après création
        final_objects = len(gc.get_objects())
        
        # Vérification que l'augmentation du nombre d'objets est raisonnable
        object_increase = final_objects - initial_objects
        assert object_increase < 5000  # Moins de 5000 nouveaux objets
    
    @pytest.mark.performance
    def test_string_representation_performance(self):
        """Test la performance de représentation string."""
        # Création d'objets
        states = [State(f"q{i}", StateType.INTERMEDIATE) for i in range(1000)]
        transitions = []
        
        for i in range(1000):
            source = states[i % len(states)]
            target = states[(i + 1) % len(states)]
            transition = Transition(
                _source_state=source,
                _target_state=target,
                _symbol="a",
                _transition_type=TransitionType.SYMBOL
            )
            transitions.append(transition)
        
        start_time = time.time()
        
        # Test de représentation string répété
        for _ in range(100):
            for state in states:
                str(state)
                repr(state)
            
            for transition in transitions:
                str(transition)
        
        end_time = time.time()
        string_time = end_time - start_time
        
        # Vérification que la représentation string prend moins de 1 seconde
        assert string_time < 1.0