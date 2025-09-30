"""
Tests unitaires pour la classe EpsilonNFA.

Ce module contient tous les tests unitaires pour la classe EpsilonNFA
selon les spécifications détaillées.
"""

import pytest
from typing import Dict, Set, Tuple

from baobab_automata.finite.epsilon_nfa import EpsilonNFA
from baobab_automata.finite.epsilon_nfa_exceptions import (
    ConversionError,
    EpsilonNFAError,
    InvalidEpsilonNFAError,
    InvalidEpsilonTransitionError
)


class TestEpsilonNFA:
    """Tests pour la classe EpsilonNFA."""
    
    def test_construction_valid(self):
        """Test de construction d'un ε-NFA valide."""
        states = {'q0', 'q1', 'q2'}
        alphabet = {'a', 'b'}
        transitions = {
            ('q0', 'ε'): {'q1'},
            ('q0', 'a'): {'q2'},
            ('q1', 'b'): {'q2'}
        }
        initial_state = 'q0'
        final_states = {'q2'}
        
        epsilon_nfa = EpsilonNFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )
        
        assert epsilon_nfa.states == states
        assert epsilon_nfa.alphabet == alphabet
        assert epsilon_nfa.initial_state == initial_state
        assert epsilon_nfa.final_states == final_states
        assert epsilon_nfa.epsilon_symbol == 'ε'
    
    def test_construction_with_custom_epsilon_symbol(self):
        """Test de construction avec symbole epsilon personnalisé."""
        states = {'q0', 'q1'}
        alphabet = {'a'}
        transitions = {
            ('q0', 'eps'): {'q1'},
            ('q0', 'a'): {'q1'}
        }
        initial_state = 'q0'
        final_states = {'q1'}
        
        epsilon_nfa = EpsilonNFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
            epsilon_symbol='eps'
        )
        
        assert epsilon_nfa.epsilon_symbol == 'eps'
    
    def test_construction_invalid_initial_state(self):
        """Test de construction avec état initial invalide."""
        states = {'q0', 'q1'}
        alphabet = {'a'}
        transitions = {('q0', 'a'): {'q1'}}
        initial_state = 'q2'  # N'existe pas
        final_states = {'q1'}
        
        with pytest.raises(InvalidEpsilonNFAError):
            EpsilonNFA(
                states=states,
                alphabet=alphabet,
                transitions=transitions,
                initial_state=initial_state,
                final_states=final_states
            )
    
    def test_construction_invalid_final_states(self):
        """Test de construction avec états finaux invalides."""
        states = {'q0', 'q1'}
        alphabet = {'a'}
        transitions = {('q0', 'a'): {'q1'}}
        initial_state = 'q0'
        final_states = {'q2'}  # N'existe pas
        
        with pytest.raises(InvalidEpsilonNFAError):
            EpsilonNFA(
                states=states,
                alphabet=alphabet,
                transitions=transitions,
                initial_state=initial_state,
                final_states=final_states
            )
    
    def test_construction_epsilon_in_alphabet(self):
        """Test de construction avec epsilon dans l'alphabet."""
        states = {'q0', 'q1'}
        alphabet = {'a', 'ε'}  # Epsilon dans l'alphabet
        transitions = {('q0', 'a'): {'q1'}}
        initial_state = 'q0'
        final_states = {'q1'}
        
        with pytest.raises(InvalidEpsilonNFAError):
            EpsilonNFA(
                states=states,
                alphabet=alphabet,
                transitions=transitions,
                initial_state=initial_state,
                final_states=final_states
            )
    
    def test_accepts_simple_word(self):
        """Test de reconnaissance d'un mot simple."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        assert epsilon_nfa.accepts('ab') == True
        assert epsilon_nfa.accepts('a') == True  # Via epsilon
        assert epsilon_nfa.accepts('b') == False
        assert epsilon_nfa.accepts('') == False
    
    def test_accepts_complex_word(self):
        """Test de reconnaissance d'un mot complexe."""
        epsilon_nfa = self._create_complex_epsilon_nfa()
        
        assert epsilon_nfa.accepts('ab') == True
        assert epsilon_nfa.accepts('aab') == True
        assert epsilon_nfa.accepts('abb') == True
        assert epsilon_nfa.accepts('aabb') == True
        assert epsilon_nfa.accepts('b') == False
        assert epsilon_nfa.accepts('aa') == False
    
    def test_accepts_word_with_invalid_symbol(self):
        """Test de reconnaissance avec symbole invalide."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        assert epsilon_nfa.accepts('ac') == False  # 'c' n'est pas dans l'alphabet
        assert epsilon_nfa.accepts('ε') == False  # Epsilon n'est pas dans l'alphabet
    
    def test_epsilon_closure_simple(self):
        """Test de fermeture epsilon simple."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        closure = epsilon_nfa.epsilon_closure({'q0'})
        assert closure == {'q0', 'q1'}
        
        closure = epsilon_nfa.epsilon_closure({'q1'})
        assert closure == {'q1'}
    
    def test_epsilon_closure_complex(self):
        """Test de fermeture epsilon complexe."""
        epsilon_nfa = self._create_complex_epsilon_nfa()
        
        closure = epsilon_nfa.epsilon_closure({'q0'})
        assert closure == {'q0', 'q1', 'q2'}
        
        closure = epsilon_nfa.epsilon_closure({'q1'})
        assert closure == {'q1', 'q2'}
    
    def test_epsilon_closure_with_cycles(self):
        """Test de fermeture epsilon avec cycles."""
        states = {'q0', 'q1', 'q2'}
        alphabet = {'a'}
        transitions = {
            ('q0', 'ε'): {'q1'},
            ('q1', 'ε'): {'q2'},
            ('q2', 'ε'): {'q0'}  # Cycle
        }
        initial_state = 'q0'
        final_states = {'q2'}
        
        epsilon_nfa = EpsilonNFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )
        
        closure = epsilon_nfa.epsilon_closure({'q0'})
        assert closure == {'q0', 'q1', 'q2'}
    
    def test_get_transitions(self):
        """Test de récupération des transitions."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        assert epsilon_nfa.get_transitions('q0', 'ε') == {'q1'}
        assert epsilon_nfa.get_transitions('q0', 'a') == {'q2'}
        assert epsilon_nfa.get_transitions('q0', 'b') == set()
        assert epsilon_nfa.get_transitions('q1', 'b') == {'q2'}
    
    def test_is_final_state(self):
        """Test de vérification d'état final."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        assert epsilon_nfa.is_final_state('q2') == True
        assert epsilon_nfa.is_final_state('q0') == False
        assert epsilon_nfa.is_final_state('q1') == False
    
    def test_get_accessible_states(self):
        """Test de récupération des états accessibles."""
        epsilon_nfa = self._create_complex_epsilon_nfa()
        
        accessible = epsilon_nfa.get_accessible_states()
        assert accessible == {'q0', 'q1', 'q2', 'q3'}
    
    def test_get_coaccessible_states(self):
        """Test de récupération des états cœurs."""
        epsilon_nfa = self._create_complex_epsilon_nfa()
        
        coaccessible = epsilon_nfa.get_coaccessible_states()
        assert coaccessible == {'q2', 'q3', 'q0', 'q1'}
    
    def test_get_useful_states(self):
        """Test de récupération des états utiles."""
        epsilon_nfa = self._create_complex_epsilon_nfa()
        
        useful = epsilon_nfa.get_useful_states()
        assert useful == {'q0', 'q1', 'q2', 'q3'}
    
    def test_to_nfa_conversion(self):
        """Test de conversion vers NFA."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        nfa = epsilon_nfa.to_nfa()
        
        # Vérifier que le NFA accepte les mêmes mots
        assert nfa.accepts('ab') == True
        assert nfa.accepts('a') == True
        assert nfa.accepts('b') == False
    
    def test_to_dfa_conversion(self):
        """Test de conversion vers DFA."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        dfa = epsilon_nfa.to_dfa()
        
        # Vérifier que le DFA accepte les mêmes mots
        assert dfa.accepts('ab') == True
        assert dfa.accepts('a') == True
        assert dfa.accepts('b') == False
    
    def test_to_dfa_direct_conversion(self):
        """Test de conversion directe vers DFA."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        dfa = epsilon_nfa.to_dfa_direct()
        
        # Vérifier que le DFA accepte les mêmes mots
        assert dfa.accepts('ab') == True
        assert dfa.accepts('a') == True
        assert dfa.accepts('b') == False
    
    def test_union_operation(self):
        """Test de l'opération d'union."""
        epsilon_nfa1 = self._create_simple_epsilon_nfa()
        epsilon_nfa2 = self._create_another_epsilon_nfa()
        
        union_nfa = epsilon_nfa1.union(epsilon_nfa2)
        
        # Vérifier que l'union accepte les mots des deux automates
        assert union_nfa.accepts('ab') == True  # Du premier
        assert union_nfa.accepts('cd') == True  # Du second
        assert union_nfa.accepts('a') == True   # Du premier via epsilon
        assert union_nfa.accepts('c') == True   # Du second via epsilon
    
    def test_concatenation_operation(self):
        """Test de l'opération de concaténation."""
        epsilon_nfa1 = self._create_simple_epsilon_nfa()
        epsilon_nfa2 = self._create_another_epsilon_nfa()
        
        concat_nfa = epsilon_nfa1.concatenation(epsilon_nfa2)
        
        # Vérifier que la concaténation accepte les mots concaténés
        assert concat_nfa.accepts('abcd') == True
        assert concat_nfa.accepts('acd') == True  # Via epsilon du premier
        assert concat_nfa.accepts('abc') == True  # Via epsilon du second
        assert concat_nfa.accepts('ac') == True   # Via epsilon des deux
    
    def test_kleene_star_operation(self):
        """Test de l'opération étoile de Kleene."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        star_nfa = epsilon_nfa.kleene_star()
        
        # Vérifier que l'étoile accepte les répétitions
        assert star_nfa.accepts('') == True      # Mot vide
        assert star_nfa.accepts('ab') == True    # Une occurrence
        assert star_nfa.accepts('abab') == True  # Plusieurs occurrences
        assert star_nfa.accepts('a') == True     # Via epsilon
    
    def test_validate_valid_automaton(self):
        """Test de validation d'un automate valide."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        assert epsilon_nfa.validate() == True
    
    def test_validate_invalid_automaton(self):
        """Test de validation d'un automate invalide."""
        states = {'q0', 'q1'}
        alphabet = {'a'}
        transitions = {
            ('q0', 'a'): {'q2'}  # q2 n'existe pas
        }
        initial_state = 'q0'
        final_states = {'q1'}
        
        epsilon_nfa = EpsilonNFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )
        
        assert epsilon_nfa.validate() == False
    
    def test_to_dict_serialization(self):
        """Test de sérialisation en dictionnaire."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        data = epsilon_nfa.to_dict()
        
        assert 'states' in data
        assert 'alphabet' in data
        assert 'transitions' in data
        assert 'initial_state' in data
        assert 'final_states' in data
        assert 'epsilon_symbol' in data
        
        assert set(data['states']) == {'q0', 'q1', 'q2'}
        assert set(data['alphabet']) == {'a', 'b'}
        assert data['initial_state'] == 'q0'
        assert set(data['final_states']) == {'q2'}
        assert data['epsilon_symbol'] == 'ε'
    
    def test_from_dict_deserialization(self):
        """Test de désérialisation depuis dictionnaire."""
        data = {
            'states': ['q0', 'q1', 'q2'],
            'alphabet': ['a', 'b'],
            'transitions': {
                'q0,ε': ['q1'],
                'q0,a': ['q2'],
                'q1,b': ['q2']
            },
            'initial_state': 'q0',
            'final_states': ['q2'],
            'epsilon_symbol': 'ε'
        }
        
        epsilon_nfa = EpsilonNFA.from_dict(data)
        
        assert epsilon_nfa.states == {'q0', 'q1', 'q2'}
        assert epsilon_nfa.alphabet == {'a', 'b'}
        assert epsilon_nfa.initial_state == 'q0'
        assert epsilon_nfa.final_states == {'q2'}
        assert epsilon_nfa.epsilon_symbol == 'ε'
    
    def test_string_representation(self):
        """Test de représentation string."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        str_repr = str(epsilon_nfa)
        assert 'ε-NFA' in str_repr
        assert 'states=3' in str_repr
        assert 'transitions=3' in str_repr
    
    def test_repr_representation(self):
        """Test de représentation détaillée."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        repr_str = repr(epsilon_nfa)
        assert 'EpsilonNFA' in repr_str
        assert 'q0' in repr_str
        assert 'q1' in repr_str
        assert 'q2' in repr_str
    
    def test_epsilon_closure_cache(self):
        """Test de mise en cache des fermetures epsilon."""
        epsilon_nfa = self._create_simple_epsilon_nfa()
        
        # Premier appel
        closure1 = epsilon_nfa.epsilon_closure({'q0'})
        
        # Deuxième appel (devrait utiliser le cache)
        closure2 = epsilon_nfa.epsilon_closure({'q0'})
        
        assert closure1 == closure2
        assert len(epsilon_nfa._epsilon_closure_cache) == 1
    
    def test_performance_large_automaton(self):
        """Test de performance avec un automate plus grand."""
        # Créer un automate avec plus d'états
        states = {f'q{i}' for i in range(10)}
        alphabet = {'a', 'b'}
        transitions = {}
        
        # Ajouter des transitions
        for i in range(9):
            transitions[(f'q{i}', 'a')] = {f'q{i+1}'}
            transitions[(f'q{i}', 'ε')] = {f'q{i+1}'}
        
        initial_state = 'q0'
        final_states = {'q9'}
        
        epsilon_nfa = EpsilonNFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )
        
        # Test de reconnaissance
        assert epsilon_nfa.accepts('a' * 9) == True
        assert epsilon_nfa.accepts('a' * 5) == True  # Via epsilon
        assert epsilon_nfa.accepts('b' * 9) == False
    
    def _create_simple_epsilon_nfa(self) -> EpsilonNFA:
        """Crée un ε-NFA simple pour les tests."""
        states = {'q0', 'q1', 'q2'}
        alphabet = {'a', 'b'}
        transitions = {
            ('q0', 'ε'): {'q1'},
            ('q0', 'a'): {'q2'},
            ('q1', 'b'): {'q2'}
        }
        initial_state = 'q0'
        final_states = {'q2'}
        
        return EpsilonNFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )
    
    def _create_complex_epsilon_nfa(self) -> EpsilonNFA:
        """Crée un ε-NFA complexe pour les tests."""
        states = {'q0', 'q1', 'q2', 'q3'}
        alphabet = {'a', 'b'}
        transitions = {
            ('q0', 'ε'): {'q1'},
            ('q1', 'ε'): {'q2'},
            ('q0', 'a'): {'q1'},
            ('q1', 'a'): {'q2'},
            ('q2', 'b'): {'q3'}
        }
        initial_state = 'q0'
        final_states = {'q3'}
        
        return EpsilonNFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )
    
    def _create_another_epsilon_nfa(self) -> EpsilonNFA:
        """Crée un autre ε-NFA pour les tests d'opérations."""
        states = {'q0', 'q1', 'q2'}
        alphabet = {'c', 'd'}
        transitions = {
            ('q0', 'ε'): {'q1'},
            ('q0', 'c'): {'q2'},
            ('q1', 'd'): {'q2'}
        }
        initial_state = 'q0'
        final_states = {'q2'}
        
        return EpsilonNFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )