"""
Tests unitaires pour les optimisations AVL des automates finis.

Ce module teste les nouvelles fonctionnalités d'optimisation AVL
implémentées dans la classe OptimizationAlgorithms.
"""

import pytest
import time
from typing import Dict, List, Set

from baobab_automata.finite.avl_structures import (
    AVLCache,
    AVLPartitionTree,
    AutomatonFeatureExtractor,
    PerformanceModel,
)
from baobab_automata.finite.dfa import DFA
from baobab_automata.finite.nfa import NFA
from baobab_automata.finite.optimization_algorithms import OptimizationAlgorithms
from baobab_automata.finite.optimization_exceptions import OptimizationError


class TestAVLPartitionTree:
    """Tests pour la classe AVLPartitionTree."""
    
    def test_insert_and_find(self):
        """Test d'insertion et de recherche dans l'arbre AVL."""
        tree = AVLPartitionTree()
        
        # Insérer des partitions
        partition1 = {'q0', 'q1'}
        partition2 = {'q2', 'q3'}
        tree.insert_partition(partition1)
        tree.insert_partition(partition2)
        
        # Vérifier la recherche
        assert tree.find_partition('q0') == partition1
        assert tree.find_partition('q2') == partition2
        assert tree.find_partition('q4') is None
    
    def test_split_partition(self):
        """Test de division de partition."""
        tree = AVLPartitionTree()
        
        partition = {'q0', 'q1', 'q2', 'q3'}
        tree.insert_partition(partition)
        
        splitter = {'q0', 'q2'}
        part1, part2 = tree.split_partition(partition, splitter)
        
        assert part1 == {'q0', 'q2'}
        assert part2 == {'q1', 'q3'}
    
    def test_remove_partition(self):
        """Test de suppression de partition."""
        tree = AVLPartitionTree()
        
        partition = {'q0', 'q1'}
        tree.insert_partition(partition)
        
        assert tree.find_partition('q0') == partition
        
        tree.remove_partition(partition)
        assert tree.find_partition('q0') is None
    
    def test_get_all_partitions(self):
        """Test de récupération de toutes les partitions."""
        tree = AVLPartitionTree()
        
        partition1 = {'q0', 'q1'}
        partition2 = {'q2', 'q3'}
        tree.insert_partition(partition1)
        tree.insert_partition(partition2)
        
        all_partitions = tree.get_all_partitions()
        assert len(all_partitions) == 2
        assert partition1 in all_partitions
        assert partition2 in all_partitions
    
    def test_clear(self):
        """Test de vidage de l'arbre."""
        tree = AVLPartitionTree()
        
        partition = {'q0', 'q1'}
        tree.insert_partition(partition)
        
        assert tree.find_partition('q0') == partition
        
        tree.clear()
        assert tree.find_partition('q0') is None
        assert tree.get_all_partitions() == []
    
    def test_performance_large_tree(self):
        """Test de performance avec un grand arbre."""
        tree = AVLPartitionTree()
        
        # Insérer 100 partitions
        for i in range(100):
            partition = {f'q{j}' for j in range(i, i + 10)}
            tree.insert_partition(partition)
        
        # Rechercher dans l'arbre
        start_time = time.time()
        for i in range(50):
            tree.find_partition(f'q{i * 10}')
        end_time = time.time()
        
        # Vérifier que la recherche est rapide (O(log n))
        assert end_time - start_time < 0.1  # Moins de 100ms


class TestAVLCache:
    """Tests pour la classe AVLCache."""
    
    def test_put_and_get(self):
        """Test d'ajout et de récupération dans le cache."""
        cache = AVLCache(max_size=10)
        
        # Ajouter des données
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        
        # Récupérer les données
        assert cache.get("key1") == "value1"
        assert cache.get("key2") == "value2"
        assert cache.get("key3") is None
    
    def test_cache_size_limit(self):
        """Test de la limite de taille du cache."""
        cache = AVLCache(max_size=2)
        
        # Ajouter plus d'éléments que la limite
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        
        # Vérifier que le cache respecte la limite
        assert len(cache.cache_data) <= 2
    
    def test_access_tracking(self):
        """Test du suivi des accès."""
        cache = AVLCache()
        
        cache.put("key1", "value1")
        
        # Accéder plusieurs fois
        cache.get("key1")
        cache.get("key1")
        
        # Vérifier que les accès sont enregistrés
        assert "key1" in cache.access_history
        assert len(cache.access_history["key1"]) == 2
    
    def test_invalidate_pattern(self):
        """Test d'invalidation par pattern."""
        cache = AVLCache()
        
        cache.put("dfa_key1", "value1")
        cache.put("dfa_key2", "value2")
        cache.put("nfa_key1", "value3")
        
        # Invalider les clés contenant "dfa"
        cache.invalidate_pattern("dfa")
        
        # Vérifier que seules les clés DFA sont supprimées
        assert cache.get("dfa_key1") is None
        assert cache.get("dfa_key2") is None
        assert cache.get("nfa_key1") == "value3"
    
    def test_predict_next_access(self):
        """Test de prédiction d'accès futur."""
        cache = AVLCache()
        
        cache.put("key1", "value1")
        
        # Accéder plusieurs fois rapidement
        for _ in range(5):
            cache.get("key1")
        
        # Prédire l'accès futur
        probability = cache.predict_next_access("key1")
        assert 0.0 <= probability <= 1.0
    
    def test_cache_stats(self):
        """Test des statistiques du cache."""
        cache = AVLCache()
        
        cache.put("key1", "value1")
        cache.get("key1")
        
        stats = cache.get_cache_stats()
        assert "size" in stats
        assert "max_size" in stats
        assert "access_count" in stats
        assert "hit_rate" in stats


class TestAutomatonFeatureExtractor:
    """Tests pour la classe AutomatonFeatureExtractor."""
    
    def test_extract_dfa_features(self):
        """Test d'extraction de caractéristiques pour un DFA."""
        extractor = AutomatonFeatureExtractor()
        
        # Créer un DFA simple
        dfa = DFA(
            states={'q0', 'q1'},
            alphabet={'a', 'b'},
            transitions={('q0', 'a'): 'q1', ('q1', 'b'): 'q0'},
            initial_state='q0',
            final_states={'q1'}
        )
        
        features = extractor.extract(dfa)
        
        # Vérifier les caractéristiques de base
        assert features['num_states'] == 2
        assert features['num_transitions'] == 2
        assert features['alphabet_size'] == 2
        assert features['final_states_ratio'] == 0.5
        
        # Vérifier les caractéristiques calculées
        assert 'transition_density' in features
        assert 'connectivity' in features
        assert 'average_out_degree' in features
        assert 'regularity_score' in features
    
    def test_extract_nfa_features(self):
        """Test d'extraction de caractéristiques pour un NFA."""
        extractor = AutomatonFeatureExtractor()
        
        # Créer un NFA simple
        nfa = NFA(
            states={'q0', 'q1'},
            alphabet={'a', 'b'},
            transitions={('q0', 'a'): {'q1'}, ('q0', 'b'): {'q0', 'q1'}},
            initial_state='q0',
            final_states={'q1'}
        )
        
        features = extractor.extract(nfa)
        
        # Vérifier les caractéristiques
        assert features['num_states'] == 2
        assert features['alphabet_size'] == 2
        assert features['final_states_ratio'] == 0.5


class TestPerformanceModel:
    """Tests pour la classe PerformanceModel."""
    
    def test_predict_performance(self):
        """Test de prédiction de performance."""
        model = PerformanceModel()
        
        features = {
            'num_states': 10,
            'num_transitions': 20,
            'alphabet_size': 2
        }
        
        predictions = model.predict(features)
        
        # Vérifier la structure des prédictions
        assert 'time' in predictions
        assert 'memory' in predictions
        assert 'improvement' in predictions
        
        # Vérifier que les valeurs sont positives
        assert predictions['time'] >= 0
        assert predictions['memory'] >= 0
        assert 0 <= predictions['improvement'] <= 1
    
    def test_update_model(self):
        """Test de mise à jour du modèle."""
        model = PerformanceModel()
        
        features = {'num_states': 10}
        actual_performance = {'time': 0.1, 'memory': 1.0, 'improvement': 0.2}
        
        # Mettre à jour le modèle
        model.update(features, actual_performance)
        
        # Vérifier que les données sont enregistrées
        assert len(model.training_data) == 1
        assert model.training_data[0][0] == features
        assert model.training_data[0][1] == actual_performance


class TestOptimizationAlgorithmsAVL:
    """Tests pour les optimisations AVL dans OptimizationAlgorithms."""
    
    def test_minimize_dfa_avl_basic(self):
        """Test de base de la minimisation DFA AVL."""
        optimizer = OptimizationAlgorithms(enable_avl=True)
        
        # Créer un DFA non minimal
        dfa = DFA(
            states={'q0', 'q1', 'q2'},
            alphabet={'a', 'b'},
            transitions={
                ('q0', 'a'): 'q1',
                ('q0', 'b'): 'q2',
                ('q1', 'a'): 'q1',
                ('q1', 'b'): 'q1',
                ('q2', 'a'): 'q2',
                ('q2', 'b'): 'q2'
            },
            initial_state='q0',
            final_states={'q1', 'q2'}
        )
        
        # Minimiser avec AVL
        minimal_dfa = optimizer.minimize_dfa_avl(dfa)
        
        # Vérifier la minimisation
        assert len(minimal_dfa.states) <= len(dfa.states)
        assert self._are_equivalent(dfa, minimal_dfa)
    
    def test_minimize_dfa_avl_fallback(self):
        """Test du fallback vers la minimisation standard."""
        optimizer = OptimizationAlgorithms(enable_avl=False)
        
        dfa = self._create_simple_dfa()
        
        # Devrait utiliser la minimisation standard
        minimal_dfa = optimizer.minimize_dfa_avl(dfa)
        
        assert len(minimal_dfa.states) <= len(dfa.states)
        assert self._are_equivalent(dfa, minimal_dfa)
    
    def test_remove_unreachable_states_avl(self):
        """Test de l'élimination AVL des états inaccessibles."""
        optimizer = OptimizationAlgorithms(enable_avl=True)
        
        # Créer un DFA avec des états inaccessibles
        dfa = DFA(
            states={'q0', 'q1', 'q2'},
            alphabet={'a'},
            transitions={('q0', 'a'): 'q1'},
            initial_state='q0',
            final_states={'q1'}
        )
        
        # Éliminer les états inaccessibles avec AVL
        clean_dfa = optimizer.remove_unreachable_states_avl(dfa)
        
        # Vérifier que q2 est supprimé
        assert 'q2' not in clean_dfa.states
        assert 'q0' in clean_dfa.states
        assert 'q1' in clean_dfa.states
    
    def test_validate_optimization_avl(self):
        """Test de validation AVL des optimisations."""
        optimizer = OptimizationAlgorithms(enable_avl=True)
        
        dfa1 = self._create_simple_dfa()
        dfa2 = self._create_simple_dfa()
        
        # Devrait être équivalent
        assert optimizer.validate_optimization_avl(dfa1, dfa2)
        
        # Créer un DFA différent
        dfa3 = DFA(
            states={'q0'},
            alphabet={'a'},
            transitions={},
            initial_state='q0',
            final_states=set()
        )
        
        # Ne devrait pas être équivalent
        assert not optimizer.validate_optimization_avl(dfa1, dfa3)
    
    def test_cache_functionality(self):
        """Test de la fonctionnalité de cache AVL."""
        optimizer = OptimizationAlgorithms(enable_avl=True)
        
        dfa = self._create_simple_dfa()
        
        # Première minimisation
        minimal_dfa1 = optimizer.minimize_dfa_avl(dfa)
        
        # Deuxième minimisation (devrait utiliser le cache)
        minimal_dfa2 = optimizer.minimize_dfa_avl(dfa)
        
        # Vérifier que les résultats sont identiques
        assert minimal_dfa1.states == minimal_dfa2.states
        assert minimal_dfa1.transitions == minimal_dfa2.transitions
    
    def test_performance_comparison(self):
        """Test de comparaison de performance AVL vs standard."""
        optimizer_standard = OptimizationAlgorithms(enable_avl=False)
        optimizer_avl = OptimizationAlgorithms(enable_avl=True)
        
        # Créer un DFA de taille moyenne
        dfa = self._create_medium_dfa()
        
        # Mesurer le temps standard
        start_time = time.time()
        minimal_standard = optimizer_standard.minimize_dfa(dfa)
        standard_time = time.time() - start_time
        
        # Mesurer le temps AVL
        start_time = time.time()
        minimal_avl = optimizer_avl.minimize_dfa_avl(dfa)
        avl_time = time.time() - start_time
        
        # Vérifier l'équivalence
        assert self._are_equivalent(minimal_standard, minimal_avl)
        
        # Pour les petits automates, les performances peuvent être similaires
        # Mais AVL devrait être au moins aussi rapide
        assert avl_time <= standard_time + 0.01  # Tolérance de 10ms
    
    def test_error_handling(self):
        """Test de gestion d'erreurs."""
        optimizer = OptimizationAlgorithms(enable_avl=True)
        
        # Test avec un automate invalide
        with pytest.raises(OptimizationError):
            optimizer.minimize_dfa_avl(None)
        
        # Test avec un NFA (devrait lever une erreur)
        nfa = NFA(
            states={'q0'},
            alphabet={'a'},
            transitions={},
            initial_state='q0',
            final_states=set()
        )
        
        with pytest.raises(OptimizationError):
            optimizer.minimize_dfa_avl(nfa)
    
    def _create_simple_dfa(self) -> DFA:
        """Crée un DFA simple pour les tests."""
        return DFA(
            states={'q0', 'q1'},
            alphabet={'a', 'b'},
            transitions={
                ('q0', 'a'): 'q1',
                ('q0', 'b'): 'q0',
                ('q1', 'a'): 'q1',
                ('q1', 'b'): 'q0'
            },
            initial_state='q0',
            final_states={'q1'}
        )
    
    def _create_medium_dfa(self) -> DFA:
        """Crée un DFA de taille moyenne pour les tests."""
        states = {f'q{i}' for i in range(10)}
        alphabet = {'a', 'b', 'c'}
        transitions = {}
        
        # Créer des transitions aléatoires
        for state in states:
            for symbol in alphabet:
                target = f'q{(int(state[1:]) + 1) % 10}'
                transitions[(state, symbol)] = target
        
        return DFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state='q0',
            final_states={'q5', 'q9'}
        )
    
    def _are_equivalent(self, dfa1: DFA, dfa2: DFA) -> bool:
        """Vérifie si deux DFA sont équivalents."""
        # Test sur un échantillon de mots
        test_words = ['', 'a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba']
        
        for word in test_words:
            if dfa1.accepts(word) != dfa2.accepts(word):
                return False
        
        return True


class TestIntegrationAVL:
    """Tests d'intégration pour les optimisations AVL."""
    
    def test_full_optimization_pipeline(self):
        """Test du pipeline complet d'optimisation AVL."""
        optimizer = OptimizationAlgorithms(
            optimization_level=3,
            enable_avl=True,
            enable_learning=True
        )
        
        # Créer un automate complexe
        automaton = self._create_complex_automaton()
        
        # Optimiser avec le pipeline complet
        optimized_automaton = optimizer.minimize_dfa_avl(automaton)
        
        # Vérifier l'équivalence
        assert self._are_equivalent(automaton, optimized_automaton)
        
        # Vérifier l'amélioration
        stats = optimizer.get_optimization_stats(automaton, optimized_automaton)
        assert stats['state_reduction'] >= 0
    
    def test_cache_invalidation(self):
        """Test de l'invalidation du cache AVL."""
        optimizer = OptimizationAlgorithms(enable_avl=True)
        
        # Créer un automate et l'optimiser
        automaton1 = self._create_simple_automaton()
        optimized1 = optimizer.minimize_dfa_avl(automaton1)
        
        # Modifier l'automate légèrement
        automaton2 = self._create_simple_automaton()
        # Ajouter un état supplémentaire
        automaton2.states.add('q2')
        
        # Optimiser à nouveau
        optimized2 = optimizer.minimize_dfa_avl(automaton2)
        
        # Vérifier que les résultats sont différents
        assert optimized1.states != optimized2.states
    
    def _create_simple_automaton(self) -> DFA:
        """Crée un automate simple pour les tests."""
        return DFA(
            states={'q0', 'q1'},
            alphabet={'a'},
            transitions={('q0', 'a'): 'q1'},
            initial_state='q0',
            final_states={'q1'}
        )
    
    def _create_complex_automaton(self) -> DFA:
        """Crée un automate complexe pour les tests."""
        states = {f'q{i}' for i in range(20)}
        alphabet = {'a', 'b', 'c', 'd'}
        transitions = {}
        
        # Créer des transitions complexes
        for i, state in enumerate(states):
            for symbol in alphabet:
                target = f'q{(i + 1) % 20}'
                transitions[(state, symbol)] = target
        
        return DFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state='q0',
            final_states={f'q{i}' for i in range(5, 20, 3)}
        )
    
    def _are_equivalent(self, dfa1: DFA, dfa2: DFA) -> bool:
        """Vérifie si deux DFA sont équivalents."""
        # Test sur un échantillon de mots
        test_words = ['', 'a', 'b', 'aa', 'ab', 'ba', 'bb']
        
        for word in test_words:
            if dfa1.accepts(word) != dfa2.accepts(word):
                return False
        
        return True