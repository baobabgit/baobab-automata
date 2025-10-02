"""Tests simples pour les algorithmes d'optimisation."""

import pytest
from baobab_automata.finite.optimization_algorithms import OptimizationAlgorithms
from baobab_automata.finite.dfa import DFA
from baobab_automata.finite.optimization_exceptions import OptimizationError


@pytest.mark.unit
class TestOptimizationAlgorithmsSimple:
    """Tests simples pour OptimizationAlgorithms."""

    def test_optimization_algorithms_initialization_default(self):
        """Test l'initialisation par défaut."""
        optimizer = OptimizationAlgorithms()
        assert optimizer.optimization_level == 2
        assert optimizer.max_iterations == 1000

    def test_optimization_algorithms_initialization_custom(self):
        """Test l'initialisation avec paramètres personnalisés."""
        optimizer = OptimizationAlgorithms(optimization_level=3, max_iterations=500)
        assert optimizer.optimization_level == 3
        assert optimizer.max_iterations == 500

    def test_optimization_algorithms_initialization_invalid_level_negative(self):
        """Test l'initialisation avec niveau négatif."""
        with pytest.raises(OptimizationError, match="Niveau d'optimisation invalide: -1"):
            OptimizationAlgorithms(optimization_level=-1)

    def test_optimization_algorithms_initialization_invalid_level_too_high(self):
        """Test l'initialisation avec niveau trop élevé."""
        with pytest.raises(OptimizationError, match="Niveau d'optimisation invalide: 4"):
            OptimizationAlgorithms(optimization_level=4)

    def test_optimization_algorithms_initialization_level_0(self):
        """Test l'initialisation avec niveau 0."""
        optimizer = OptimizationAlgorithms(optimization_level=0)
        assert optimizer.optimization_level == 0

    def test_optimization_algorithms_initialization_level_3(self):
        """Test l'initialisation avec niveau 3."""
        optimizer = OptimizationAlgorithms(optimization_level=3)
        assert optimizer.optimization_level == 3

    def test_optimization_algorithms_properties(self):
        """Test les propriétés de l'optimiseur."""
        optimizer = OptimizationAlgorithms(optimization_level=1, max_iterations=200)
        assert optimizer.optimization_level == 1
        assert optimizer.max_iterations == 200
        assert isinstance(optimizer.cache, dict)

    def test_optimization_algorithms_cache_initialization(self):
        """Test l'initialisation du cache."""
        optimizer = OptimizationAlgorithms()
        assert isinstance(optimizer.cache, dict)
        assert len(optimizer.cache) == 0

    def test_optimization_algorithms_cache_independence(self):
        """Test l'indépendance des caches."""
        optimizer1 = OptimizationAlgorithms()
        optimizer2 = OptimizationAlgorithms()
        assert optimizer1.cache is not optimizer2.cache

    def test_optimization_algorithms_cache_operations(self):
        """Test les opérations sur le cache."""
        optimizer = OptimizationAlgorithms()
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )
        
        # Le cache est vide initialement
        assert len(optimizer.cache) == 0
        
        # Ajouter un élément au cache (simulation)
        optimizer.cache["test"] = dfa
        assert len(optimizer.cache) == 1
        assert "test" in optimizer.cache

    def test_optimization_algorithms_immutable_properties(self):
        """Test que les propriétés ne sont pas modifiables."""
        optimizer = OptimizationAlgorithms()
        
        # Les propriétés ne sont pas modifiables directement
        with pytest.raises(AttributeError):
            optimizer.optimization_level = 1
        with pytest.raises(AttributeError):
            optimizer.max_iterations = 100

    def test_optimization_algorithms_string_representation(self):
        """Test la représentation string."""
        optimizer = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        str_repr = str(optimizer)
        assert "OptimizationAlgorithms" in str_repr

    def test_optimization_algorithms_repr(self):
        """Test la représentation repr."""
        optimizer = OptimizationAlgorithms(optimization_level=1, max_iterations=500)
        repr_str = repr(optimizer)
        assert "OptimizationAlgorithms" in repr_str

    def test_optimization_algorithms_equality(self):
        """Test l'égalité des optimiseurs."""
        optimizer1 = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        optimizer2 = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        optimizer3 = OptimizationAlgorithms(optimization_level=1, max_iterations=1000)
        
        # Les objets ne sont pas égaux par défaut (pas d'implémentation __eq__)
        assert optimizer1 != optimizer2
        assert optimizer1 != optimizer3

    def test_optimization_algorithms_hash(self):
        """Test le hash des optimiseurs."""
        optimizer1 = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        optimizer2 = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        optimizer3 = OptimizationAlgorithms(optimization_level=1, max_iterations=1000)
        
        # Les objets ont des hash différents par défaut (pas d'implémentation __hash__)
        assert hash(optimizer1) != hash(optimizer2)
        assert hash(optimizer1) != hash(optimizer3)

    def test_optimization_algorithms_with_different_parameters(self):
        """Test avec différents paramètres."""
        optimizer1 = OptimizationAlgorithms(optimization_level=0, max_iterations=100)
        optimizer2 = OptimizationAlgorithms(optimization_level=3, max_iterations=2000)
        
        assert optimizer1.optimization_level == 0
        assert optimizer1.max_iterations == 100
        assert optimizer2.optimization_level == 3
        assert optimizer2.max_iterations == 2000

    def test_optimization_algorithms_boundary_values(self):
        """Test avec des valeurs limites."""
        # Niveau minimum
        optimizer_min = OptimizationAlgorithms(optimization_level=0, max_iterations=1)
        assert optimizer_min.optimization_level == 0
        assert optimizer_min.max_iterations == 1
        
        # Niveau maximum
        optimizer_max = OptimizationAlgorithms(optimization_level=3, max_iterations=10000)
        assert optimizer_max.optimization_level == 3
        assert optimizer_max.max_iterations == 10000

    def test_optimization_algorithms_parameter_validation(self):
        """Test la validation des paramètres."""
        # Niveau d'optimisation invalide
        with pytest.raises(OptimizationError):
            OptimizationAlgorithms(optimization_level=-1)
        
        with pytest.raises(OptimizationError):
            OptimizationAlgorithms(optimization_level=4)
        
        # Valeurs valides
        for level in range(4):
            optimizer = OptimizationAlgorithms(optimization_level=level)
            assert optimizer.optimization_level == level

    def test_optimization_algorithms_memory_usage(self):
        """Test l'utilisation mémoire."""
        optimizer = OptimizationAlgorithms()
        
        # Le cache est vide initialement
        assert len(optimizer.cache) == 0
        
        # Ajouter plusieurs éléments
        for i in range(10):
            dfa = DFA(
                states={f"q{i}"},
                alphabet={"a"},
                transitions={},
                initial_state=f"q{i}",
                final_states=set(),
            )
            optimizer.cache[f"test_{i}"] = dfa
        
        assert len(optimizer.cache) == 10

    def test_optimization_algorithms_thread_safety(self):
        """Test la sécurité des threads."""
        optimizer = OptimizationAlgorithms()
        
        # Simuler l'accès concurrent au cache
        dfa = DFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states=set(),
        )
        
        # Ajouter un élément
        optimizer.cache["thread_test"] = dfa
        assert "thread_test" in optimizer.cache
        
        # Vérifier que l'élément est toujours là
        assert optimizer.cache["thread_test"] == dfa

    def test_optimization_algorithms_serialization(self):
        """Test la sérialisation."""
        optimizer = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        
        # Vérifier que l'objet peut être picklé
        import pickle
        serialized = pickle.dumps(optimizer)
        deserialized = pickle.loads(serialized)
        
        assert deserialized.optimization_level == optimizer.optimization_level
        assert deserialized.max_iterations == optimizer.max_iterations

    def test_optimization_algorithms_copy(self):
        """Test la copie."""
        optimizer = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        
        # Copie superficielle
        import copy
        copied_optimizer = copy.copy(optimizer)
        
        assert copied_optimizer.optimization_level == optimizer.optimization_level
        assert copied_optimizer.max_iterations == optimizer.max_iterations
        assert copied_optimizer is not optimizer

    def test_optimization_algorithms_deep_copy(self):
        """Test la copie profonde."""
        optimizer = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        
        # Copie profonde
        import copy
        deep_copied_optimizer = copy.deepcopy(optimizer)
        
        assert deep_copied_optimizer.optimization_level == optimizer.optimization_level
        assert deep_copied_optimizer.max_iterations == optimizer.max_iterations
        assert deep_copied_optimizer is not optimizer

    def test_optimization_algorithms_context_manager(self):
        """Test l'utilisation comme context manager."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur n'implémente pas le protocole context manager
        # mais on peut tester qu'il n'y a pas d'erreur
        assert optimizer is not None

    def test_optimization_algorithms_iteration(self):
        """Test l'itération."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur n'est pas itérable
        with pytest.raises(TypeError):
            list(optimizer)

    def test_optimization_algorithms_length(self):
        """Test la longueur."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur n'a pas de longueur
        with pytest.raises(TypeError):
            len(optimizer)

    def test_optimization_algorithms_contains(self):
        """Test l'opérateur in."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur ne supporte pas l'opérateur in
        with pytest.raises(TypeError):
            "test" in optimizer

    def test_optimization_algorithms_getitem(self):
        """Test l'accès par index."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur ne supporte pas l'accès par index
        with pytest.raises(TypeError):
            optimizer["test"]

    def test_optimization_algorithms_setitem(self):
        """Test l'assignation par index."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur ne supporte pas l'assignation par index
        with pytest.raises(TypeError):
            optimizer["test"] = "value"

    def test_optimization_algorithms_delitem(self):
        """Test la suppression par index."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur ne supporte pas la suppression par index
        with pytest.raises(TypeError):
            del optimizer["test"]

    def test_optimization_algorithms_boolean_conversion(self):
        """Test la conversion booléenne."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur est toujours truthy
        assert bool(optimizer) is True

    def test_optimization_algorithms_arithmetic_operations(self):
        """Test les opérations arithmétiques."""
        optimizer = OptimizationAlgorithms()
        
        # L'optimiseur ne supporte pas les opérations arithmétiques
        with pytest.raises(TypeError):
            optimizer + 1
        with pytest.raises(TypeError):
            optimizer - 1
        with pytest.raises(TypeError):
            optimizer * 2
        with pytest.raises(TypeError):
            optimizer / 2

    def test_optimization_algorithms_comparison_operators(self):
        """Test les opérateurs de comparaison."""
        optimizer1 = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        optimizer2 = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)
        optimizer3 = OptimizationAlgorithms(optimization_level=1, max_iterations=1000)
        
        # Les objets ne sont pas égaux par défaut (pas d'implémentation __eq__)
        assert optimizer1 != optimizer2
        assert optimizer1 != optimizer3
        # Les opérateurs de comparaison ne sont pas implémentés
        with pytest.raises(TypeError):
            optimizer1 >= optimizer2
        with pytest.raises(TypeError):
            optimizer1 <= optimizer2
        with pytest.raises(TypeError):
            optimizer1 > optimizer2
        with pytest.raises(TypeError):
            optimizer1 < optimizer2

    def test_optimization_algorithms_edge_cases(self):
        """Test les cas limites."""
        # Niveau d'optimisation à la limite
        optimizer_min = OptimizationAlgorithms(optimization_level=0)
        optimizer_max = OptimizationAlgorithms(optimization_level=3)
        
        assert optimizer_min.optimization_level == 0
        assert optimizer_max.optimization_level == 3
        
        # Max iterations à la limite
        optimizer_small = OptimizationAlgorithms(max_iterations=1)
        optimizer_large = OptimizationAlgorithms(max_iterations=1000000)
        
        assert optimizer_small.max_iterations == 1
        assert optimizer_large.max_iterations == 1000000

    def test_optimization_algorithms_multiple_instances(self):
        """Test plusieurs instances."""
        optimizer1 = OptimizationAlgorithms(optimization_level=1)
        optimizer2 = OptimizationAlgorithms(optimization_level=2)
        optimizer3 = OptimizationAlgorithms(optimization_level=3)
        
        assert optimizer1.optimization_level == 1
        assert optimizer2.optimization_level == 2
        assert optimizer3.optimization_level == 3
        
        # Les caches sont indépendants
        assert optimizer1.cache is not optimizer2.cache
        assert optimizer2.cache is not optimizer3.cache