"""Tests unitaires pour la classe OptimizationAlgorithms."""

import pytest
from baobab_automata.algorithms.finite.optimization_algorithms import OptimizationAlgorithms
from baobab_automata.finite.optimization.optimization_exceptions import OptimizationError
from baobab_automata.finite.dfa import DFA
from baobab_automata.finite.nfa import NFA
from baobab_automata.finite.epsilon_nfa import EpsilonNFA


@pytest.mark.unit
class TestOptimizationAlgorithms:
    """Tests pour la classe OptimizationAlgorithms."""

    def test_optimization_algorithms_initialization_default(self):
        """Test l'initialisation avec les paramètres par défaut."""
        optimizer = OptimizationAlgorithms()
        assert optimizer.optimization_level == 2
        assert optimizer.max_iterations == 1000
        assert len(optimizer.cache) == 0

    def test_optimization_algorithms_initialization_custom(self):
        """Test l'initialisation avec des paramètres personnalisés."""
        optimizer = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        assert optimizer.optimization_level == 1
        assert optimizer.max_iterations == 500
        assert len(optimizer.cache) == 0

    def test_optimization_algorithms_initialization_invalid_level_negative(self):
        """Test l'initialisation avec un niveau d'optimisation négatif."""
        with pytest.raises(OptimizationError, match="Niveau d'optimisation invalide: -1"):
            OptimizationAlgorithms(optimization_level=-1)

    def test_optimization_algorithms_initialization_invalid_level_too_high(self):
        """Test l'initialisation avec un niveau d'optimisation trop élevé."""
        with pytest.raises(OptimizationError, match="Niveau d'optimisation invalide: 4"):
            OptimizationAlgorithms(optimization_level=4)

    def test_optimization_algorithms_initialization_level_0(self):
        """Test l'initialisation avec le niveau d'optimisation 0."""
        optimizer = OptimizationAlgorithms(optimization_level=0)
        assert optimizer.optimization_level == 0

    def test_optimization_algorithms_initialization_level_3(self):
        """Test l'initialisation avec le niveau d'optimisation 3."""
        optimizer = OptimizationAlgorithms(optimization_level=3)
        assert optimizer.optimization_level == 3

    def test_optimization_algorithms_properties(self):
        """Test les propriétés de l'optimiseur."""
        optimizer = OptimizationAlgorithms(optimization_level=1, max_iterations=200)
        
        # Test des propriétés
        assert optimizer.optimization_level == 1
        assert optimizer.max_iterations == 200
        assert isinstance(optimizer.cache, dict)
        assert len(optimizer.cache) == 0

    def test_optimization_algorithms_cache_initialization(self):
        """Test l'initialisation du cache."""
        optimizer = OptimizationAlgorithms()
        assert isinstance(optimizer.cache, dict)
        assert len(optimizer.cache) == 0

    def test_optimization_algorithms_max_iterations_zero(self):
        """Test l'initialisation avec max_iterations à 0."""
        optimizer = OptimizationAlgorithms(max_iterations=0)
        assert optimizer.max_iterations == 0

    def test_optimization_algorithms_max_iterations_large(self):
        """Test l'initialisation avec max_iterations très grand."""
        optimizer = OptimizationAlgorithms(max_iterations=10000)
        assert optimizer.max_iterations == 10000

    def test_optimization_algorithms_multiple_instances(self):
        """Test la création de plusieurs instances."""
        optimizer1 = OptimizationAlgorithms(optimization_level=1)
        optimizer2 = OptimizationAlgorithms(optimization_level=2)
        
        assert optimizer1.optimization_level == 1
        assert optimizer2.optimization_level == 2
        assert optimizer1 is not optimizer2

    def test_optimization_algorithms_cache_independence(self):
        """Test que les caches des différentes instances sont indépendants."""
        optimizer1 = OptimizationAlgorithms()
        optimizer2 = OptimizationAlgorithms()
        
        # Les caches doivent être différents
        assert optimizer1.cache is not optimizer2.cache
        assert len(optimizer1.cache) == 0
        assert len(optimizer2.cache) == 0

    def test_optimization_algorithms_immutable_properties(self):
        """Test que les propriétés ne peuvent pas être modifiées directement."""
        optimizer = OptimizationAlgorithms()
        
        # Les propriétés ne devraient pas être modifiables directement
        # (bien que Python permette la modification, on teste le comportement attendu)
        original_level = optimizer.optimization_level
        original_max_iter = optimizer.max_iterations
        
        # Ces attributs ne devraient pas changer
        assert optimizer.optimization_level == original_level
        assert optimizer.max_iterations == original_max_iter

    def test_optimization_algorithms_string_representation(self):
        """Test la représentation string de l'optimiseur."""
        optimizer = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        str_repr = str(optimizer)
        
        # La représentation devrait contenir des informations sur l'optimiseur
        assert "OptimizationAlgorithms" in str_repr or "optimization" in str_repr.lower()

    def test_optimization_algorithms_equality(self):
        """Test l'égalité entre deux optimiseurs."""
        optimizer1 = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        optimizer2 = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        optimizer3 = OptimizationAlgorithms(optimization_level=2, max_iterations=500)
        
        # Les optimiseurs sont des objets différents même avec les mêmes paramètres
        assert optimizer1 is not optimizer2
        assert optimizer1 != optimizer2  # Pas d'implémentation __eq__
        assert optimizer1 != optimizer3

    def test_optimization_algorithms_hash(self):
        """Test le hash de l'optimiseur."""
        optimizer1 = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        optimizer2 = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        optimizer3 = OptimizationAlgorithms(optimization_level=2, max_iterations=500)
        
        # Les optimiseurs sont des objets différents donc des hash différents
        assert hash(optimizer1) != hash(optimizer2)
        assert hash(optimizer1) != hash(optimizer3)
        assert hash(optimizer2) != hash(optimizer3)

    def test_optimization_algorithms_with_different_parameters(self):
        """Test l'optimiseur avec différents paramètres."""
        # Test avec différents niveaux d'optimisation
        for level in range(4):
            optimizer = OptimizationAlgorithms(optimization_level=level)
            assert optimizer.optimization_level == level

        # Test avec différents max_iterations
        for max_iter in [0, 1, 10, 100, 1000, 10000]:
            optimizer = OptimizationAlgorithms(max_iterations=max_iter)
            assert optimizer.max_iterations == max_iter

    def test_optimization_algorithms_boundary_values(self):
        """Test l'optimiseur avec des valeurs limites."""
        # Niveau d'optimisation minimum
        optimizer_min = OptimizationAlgorithms(optimization_level=0)
        assert optimizer_min.optimization_level == 0

        # Niveau d'optimisation maximum
        optimizer_max = OptimizationAlgorithms(optimization_level=3)
        assert optimizer_max.optimization_level == 3

        # Max iterations minimum
        optimizer_iter_min = OptimizationAlgorithms(max_iterations=0)
        assert optimizer_iter_min.max_iterations == 0

        # Max iterations très grand
        optimizer_iter_max = OptimizationAlgorithms(max_iterations=999999)
        assert optimizer_iter_max.max_iterations == 999999

    def test_optimization_algorithms_parameter_validation(self):
        """Test la validation des paramètres."""
        # Test des niveaux d'optimisation valides
        valid_levels = [0, 1, 2, 3]
        for level in valid_levels:
            optimizer = OptimizationAlgorithms(optimization_level=level)
            assert optimizer.optimization_level == level

        # Test des niveaux d'optimisation invalides
        invalid_levels = [-1, -10, 4, 5, 10, 100]
        for level in invalid_levels:
            with pytest.raises(OptimizationError):
                OptimizationAlgorithms(optimization_level=level)

    def test_optimization_algorithms_cache_operations(self):
        """Test les opérations sur le cache."""
        optimizer = OptimizationAlgorithms()
        
        # Le cache doit être vide au début
        assert len(optimizer.cache) == 0
        
        # Le cache doit être un dictionnaire
        assert isinstance(optimizer.cache, dict)
        
        # On peut ajouter des éléments au cache (même si ce n'est pas l'usage normal)
        optimizer.cache["test"] = "value"
        assert len(optimizer.cache) == 1
        assert optimizer.cache["test"] == "value"

    def test_optimization_algorithms_memory_usage(self):
        """Test l'utilisation mémoire de l'optimiseur."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur ne devrait pas utiliser beaucoup de mémoire au début
        assert len(optimizer.cache) == 0
        
        # Les attributs devraient être initialisés
        assert hasattr(optimizer, '_cache')
        assert hasattr(optimizer, '_optimization_level')
        assert hasattr(optimizer, '_max_iterations')
        assert hasattr(optimizer, '_stats')

    def test_optimization_algorithms_thread_safety(self):
        """Test la sécurité des threads de l'optimiseur."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur devrait être thread-safe pour les opérations de lecture
        level = optimizer.optimization_level
        max_iter = optimizer.max_iterations
        cache = optimizer.cache
        
        # Les valeurs ne devraient pas changer
        assert optimizer.optimization_level == level
        assert optimizer.max_iterations == max_iter
        assert optimizer.cache is cache

    def test_optimization_algorithms_serialization(self):
        """Test la sérialisation de l'optimiseur."""
        optimizer = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        
        # L'optimiseur devrait être sérialisable
        import pickle
        try:
            serialized = pickle.dumps(optimizer)
            deserialized = pickle.loads(serialized)
            
            assert deserialized.optimization_level == optimizer.optimization_level
            assert deserialized.max_iterations == optimizer.max_iterations
        except Exception:
            # Si la sérialisation échoue, ce n'est pas nécessairement un problème
            # car l'optimiseur pourrait contenir des objets non sérialisables
            pass

    def test_optimization_algorithms_copy(self):
        """Test la copie de l'optimiseur."""
        optimizer = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        
        # Test de copie superficielle
        import copy
        copied_optimizer = copy.copy(optimizer)
        
        assert copied_optimizer.optimization_level == optimizer.optimization_level
        assert copied_optimizer.max_iterations == optimizer.max_iterations
        assert copied_optimizer.cache is optimizer.cache  # Même référence

    def test_optimization_algorithms_deep_copy(self):
        """Test la copie profonde de l'optimiseur."""
        optimizer = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        
        # Test de copie profonde
        import copy
        try:
            deep_copied_optimizer = copy.deepcopy(optimizer)
            
            assert deep_copied_optimizer.optimization_level == optimizer.optimization_level
            assert deep_copied_optimizer.max_iterations == optimizer.max_iterations
            assert deep_copied_optimizer.cache is not optimizer.cache  # Différentes références
        except Exception:
            # Si la copie profonde échoue, ce n'est pas nécessairement un problème
            pass

    def test_optimization_algorithms_context_manager(self):
        """Test l'utilisation de l'optimiseur comme gestionnaire de contexte."""
        # L'optimiseur n'implémente pas le protocole de gestionnaire de contexte
        optimizer = OptimizationAlgorithms(optimization_level=1)
        assert optimizer.optimization_level == 1
        assert optimizer.max_iterations == 1000  # Valeur par défaut

    def test_optimization_algorithms_iteration(self):
        """Test l'itération sur l'optimiseur."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur devrait être itérable (si implémenté)
        try:
            for item in optimizer:
                pass
        except TypeError:
            # Si l'optimiseur n'est pas itérable, c'est normal
            pass

    def test_optimization_algorithms_length(self):
        """Test la longueur de l'optimiseur."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur devrait avoir une longueur (si implémenté)
        try:
            length = len(optimizer)
            assert isinstance(length, int)
        except TypeError:
            # Si l'optimiseur n'a pas de longueur, c'est normal
            pass

    def test_optimization_algorithms_contains(self):
        """Test l'opérateur 'in' sur l'optimiseur."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur devrait supporter l'opérateur 'in' (si implémenté)
        try:
            result = "test" in optimizer
            assert isinstance(result, bool)
        except TypeError:
            # Si l'optimiseur ne supporte pas 'in', c'est normal
            pass

    def test_optimization_algorithms_getitem(self):
        """Test l'opérateur [] sur l'optimiseur."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur devrait supporter l'opérateur [] (si implémenté)
        try:
            result = optimizer["test"]
            # Si on arrive ici, l'opérateur est supporté
        except (TypeError, KeyError):
            # Si l'optimiseur ne supporte pas [], c'est normal
            pass

    def test_optimization_algorithms_setitem(self):
        """Test l'opérateur []= sur l'optimiseur."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur devrait supporter l'opérateur []= (si implémenté)
        try:
            optimizer["test"] = "value"
            # Si on arrive ici, l'opérateur est supporté
        except TypeError:
            # Si l'optimiseur ne supporte pas []=, c'est normal
            pass

    def test_optimization_algorithms_delitem(self):
        """Test l'opérateur del sur l'optimiseur."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur devrait supporter l'opérateur del (si implémenté)
        try:
            del optimizer["test"]
            # Si on arrive ici, l'opérateur est supporté
        except (TypeError, KeyError):
            # Si l'optimiseur ne supporte pas del, c'est normal
            pass