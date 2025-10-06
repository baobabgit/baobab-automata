"""
Tests unitaires pour les algorithmes d'optimisation.

Ce module contient les tests unitaires pour la classe OptimizationAlgorithms
et les classes de support associées.
"""

import pytest
from typing import Dict, Set, Tuple

from baobab_automata.finite.dfa import DFA
from baobab_automata.finite.nfa import NFA
from baobab_automata.finite.epsilon_nfa import EpsilonNFA
from baobab_automata.algorithms.finite.optimization_algorithms import (
    OptimizationAlgorithms,
    OptimizationStats,
)
from baobab_automata.finite.optimization.optimization_exceptions import (
    OptimizationError,
    OptimizationMemoryError,
    OptimizationTimeoutError,
    OptimizationValidationError,
)
from baobab_automata.finite.optimization.transition_change import TransitionChange


class TestOptimizationAlgorithms:
    """Tests pour la classe OptimizationAlgorithms."""

    def test_init_valid(self):
        """Test l'initialisation avec des paramètres valides."""
        optimizer = OptimizationAlgorithms(optimization_level=2, max_iterations=1000)

        assert optimizer.optimization_level == 2
        assert optimizer.max_iterations == 1000
        assert len(optimizer.cache) == 0

    def test_init_invalid_optimization_level(self):
        """Test l'initialisation avec un niveau d'optimisation invalide."""
        with pytest.raises(OptimizationError):
            OptimizationAlgorithms(optimization_level=5)

        with pytest.raises(OptimizationError):
            OptimizationAlgorithms(optimization_level=-1)

    def test_minimize_dfa_simple(self):
        """Test la minimisation d'un DFA simple."""
        # Créer un DFA simple
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q2",
            ("q1", "a"): "q1",
            ("q1", "b"): "q1",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
        }
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Minimiser le DFA
        minimal_dfa = optimizer.minimize_dfa(dfa)

        # Vérifier que le DFA minimal est valide
        assert isinstance(minimal_dfa, DFA)
        assert minimal_dfa.validate()

        # Vérifier que les langages sont équivalents
        test_words = ["", "a", "b", "aa", "bb", "ab", "ba"]
        for word in test_words:
            assert dfa.accepts(word) == minimal_dfa.accepts(word)

    def test_minimize_dfa_already_minimal(self):
        """Test la minimisation d'un DFA déjà minimal."""
        # Créer un DFA minimal
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1", ("q1", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Minimiser le DFA
        minimal_dfa = optimizer.minimize_dfa(dfa)

        # Vérifier que le DFA reste minimal
        assert len(minimal_dfa.states) == len(dfa.states)
        assert minimal_dfa.states == dfa.states

    def test_minimize_dfa_invalid_type(self):
        """Test la minimisation avec un type d'automate invalide."""
        optimizer = OptimizationAlgorithms()

        with pytest.raises(OptimizationError):
            optimizer.minimize_dfa("not_a_dfa")

    def test_minimize_dfa_optimized(self):
        """Test la minimisation optimisée d'un DFA."""
        # Créer un DFA avec des états inaccessibles
        states = {"q0", "q1", "q2", "q3"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q2",
            ("q1", "a"): "q1",
            ("q1", "b"): "q1",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
            # q3 est inaccessible
        }
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Minimiser le DFA de manière optimisée
        minimal_dfa = optimizer.minimize_dfa_optimized(dfa)

        # Vérifier que le DFA minimal est valide
        assert isinstance(minimal_dfa, DFA)
        assert minimal_dfa.validate()

        # Vérifier que les langages sont équivalents
        test_words = ["", "a", "b", "aa", "bb", "ab", "ba"]
        for word in test_words:
            assert dfa.accepts(word) == minimal_dfa.accepts(word)

    def test_minimize_dfa_incremental(self):
        """Test la minimisation incrémentale d'un DFA."""
        # Créer un DFA simple
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q2",
            ("q1", "a"): "q1",
            ("q1", "b"): "q1",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
        }
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Créer des changements de transitions
        changes = [TransitionChange("q0", "a", "q1", "q1")]

        # Minimiser le DFA de manière incrémentale
        minimal_dfa = optimizer.minimize_dfa_incremental(dfa, changes)

        # Vérifier que le DFA minimal est valide
        assert isinstance(minimal_dfa, DFA)
        assert minimal_dfa.validate()

    def test_minimize_nfa_simple(self):
        """Test la minimisation d'un NFA simple."""
        # Créer un NFA simple
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): {"q1", "q2"},
            ("q1", "a"): {"q1"},
            ("q2", "b"): {"q2"},
        }
        initial_state = "q0"
        final_states = {"q1"}

        nfa = NFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Minimiser le NFA (retourne un DFA)
        minimal_dfa = optimizer.minimize_nfa(nfa)

        # Vérifier que le DFA minimal est valide
        assert isinstance(minimal_dfa, DFA)
        assert minimal_dfa.validate()

    def test_minimize_nfa_heuristic(self):
        """Test la minimisation heuristique d'un NFA."""
        # Créer un NFA simple
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): {"q1", "q2"},
            ("q1", "a"): {"q1"},
            ("q2", "b"): {"q2"},
        }
        initial_state = "q0"
        final_states = {"q1"}

        nfa = NFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Minimiser le NFA avec heuristiques
        minimal_nfa = optimizer.minimize_nfa_heuristic(nfa)

        # Vérifier que le NFA minimal est valide
        assert isinstance(minimal_nfa, NFA)
        assert minimal_nfa.validate()

    def test_minimize_nfa_approximate(self):
        """Test la minimisation approximative d'un NFA."""
        # Créer un NFA simple
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): {"q1", "q2"},
            ("q1", "a"): {"q1"},
            ("q2", "b"): {"q2"},
        }
        initial_state = "q0"
        final_states = {"q1"}

        nfa = NFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Minimiser le NFA de manière approximative
        minimal_nfa = optimizer.minimize_nfa_approximate(nfa, tolerance=0.1)

        # Vérifier que le NFA minimal est valide
        assert isinstance(minimal_nfa, NFA)
        assert minimal_nfa.validate()

    def test_minimize_nfa_approximate_invalid_tolerance(self):
        """Test la minimisation approximative avec une tolérance invalide."""
        nfa = NFA({"q0"}, {"a"}, {}, "q0", set())
        optimizer = OptimizationAlgorithms()

        with pytest.raises(OptimizationError):
            optimizer.minimize_nfa_approximate(nfa, tolerance=1.5)

        with pytest.raises(OptimizationError):
            optimizer.minimize_nfa_approximate(nfa, tolerance=-0.1)

    def test_remove_unreachable_states_dfa(self):
        """Test l'élimination des états inaccessibles d'un DFA."""
        # Créer un DFA avec des états inaccessibles
        states = {"q0", "q1", "q2", "q3"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q2",
            ("q1", "a"): "q1",
            ("q1", "b"): "q1",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
            # q3 est inaccessible
        }
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Éliminer les états inaccessibles
        clean_dfa = optimizer.remove_unreachable_states(dfa)

        # Vérifier que q3 a été supprimé
        assert "q3" not in clean_dfa.states
        assert len(clean_dfa.states) == 3

        # Vérifier que les langages sont équivalents
        test_words = ["", "a", "b", "aa", "bb", "ab", "ba"]
        for word in test_words:
            assert dfa.accepts(word) == clean_dfa.accepts(word)

    def test_remove_unreachable_states_nfa(self):
        """Test l'élimination des états inaccessibles d'un NFA."""
        # Créer un NFA avec des états inaccessibles
        states = {"q0", "q1", "q2", "q3"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): {"q1", "q2"},
            ("q1", "a"): {"q1"},
            ("q2", "b"): {"q2"},
            # q3 est inaccessible
        }
        initial_state = "q0"
        final_states = {"q1"}

        nfa = NFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Éliminer les états inaccessibles
        clean_nfa = optimizer.remove_unreachable_states(nfa)

        # Vérifier que q3 a été supprimé
        assert "q3" not in clean_nfa.states
        assert len(clean_nfa.states) == 3

    def test_remove_coaccessible_states_dfa(self):
        """Test l'élimination des états non-cœurs d'un DFA."""
        # Créer un DFA avec des états non-cœurs
        states = {"q0", "q1", "q2", "q3"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q2",
            ("q1", "a"): "q1",
            ("q1", "b"): "q1",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
            ("q3", "a"): "q3",
            ("q3", "b"): "q3",
        }
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Éliminer les états non-cœurs
        clean_dfa = optimizer.remove_coaccessible_states(dfa)

        # Vérifier que q3 a été supprimé (non-cœur)
        assert "q3" not in clean_dfa.states
        # q2 est aussi supprimé car il n'est pas coaccessible
        assert "q2" not in clean_dfa.states
        assert len(clean_dfa.states) == 2

    def test_merge_identical_transitions_dfa(self):
        """Test la fusion des transitions identiques d'un DFA."""
        # Créer un DFA simple
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q2",
            ("q1", "a"): "q1",
            ("q1", "b"): "q1",
            ("q2", "a"): "q2",
            ("q2", "b"): "q2",
        }
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Fusionner les transitions identiques
        merged_dfa = optimizer.merge_identical_transitions(dfa)

        # Pour un DFA, les transitions sont déjà uniques
        assert merged_dfa.states == dfa.states
        # Vérifier que les transitions sont identiques (via _transitions)
        assert merged_dfa._transitions == dfa._transitions

    def test_merge_identical_transitions_nfa(self):
        """Test la fusion des transitions identiques d'un NFA."""
        # Créer un NFA avec des transitions identiques
        states = {"q0", "q1", "q2"}
        alphabet = {"a", "b"}
        transitions = {
            ("q0", "a"): {"q1", "q2"},
            ("q0", "b"): {"q1"},
            ("q1", "a"): {"q1"},
            ("q1", "b"): {"q1"},
            ("q2", "a"): {"q2"},
            ("q2", "b"): {"q2"},
        }
        initial_state = "q0"
        final_states = {"q1"}

        nfa = NFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Fusionner les transitions identiques
        merged_nfa = optimizer.merge_identical_transitions(nfa)

        # Vérifier que le NFA est valide
        assert isinstance(merged_nfa, NFA)
        assert merged_nfa.validate()

    def test_optimize_data_structures(self):
        """Test l'optimisation des structures de données."""
        # Créer un DFA simple
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Optimiser les structures de données
        optimized_dfa = optimizer.optimize_data_structures(dfa)

        # Vérifier que l'automate est valide
        assert isinstance(optimized_dfa, DFA)
        assert optimized_dfa.validate()

    def test_optimize_performance(self):
        """Test l'optimisation des performances."""
        # Créer un DFA simple
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Optimiser les performances
        optimized_dfa = optimizer.optimize_performance(dfa)

        # Vérifier que l'automate est valide
        assert isinstance(optimized_dfa, DFA)
        assert optimized_dfa.validate()

    def test_optimize_memory(self):
        """Test l'optimisation de la mémoire."""
        # Créer un DFA simple
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Optimiser la mémoire
        optimized_dfa = optimizer.optimize_memory(dfa)

        # Vérifier que l'automate est valide
        assert isinstance(optimized_dfa, DFA)
        assert optimized_dfa.validate()

    def test_optimize_for_conversion(self):
        """Test l'optimisation pour conversion."""
        # Créer un DFA simple
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Optimiser pour conversion
        optimized_dfa = optimizer.optimize_for_conversion(dfa, "NFA")

        # Vérifier que l'automate est valide
        assert isinstance(optimized_dfa, DFA)
        assert optimized_dfa.validate()

    def test_reduce_epsilon_transitions(self):
        """Test la réduction des transitions epsilon."""
        # Créer un ε-NFA simple
        states = {"q0", "q1", "q2"}
        alphabet = {"a"}
        transitions = {("q0", "ε"): {"q1"}, ("q1", "a"): {"q2"}}
        initial_state = "q0"
        final_states = {"q2"}

        epsilon_nfa = EpsilonNFA(
            states, alphabet, transitions, initial_state, final_states
        )
        optimizer = OptimizationAlgorithms()

        # Réduire les transitions epsilon
        optimized_epsilon_nfa = optimizer.reduce_epsilon_transitions(epsilon_nfa)

        # Vérifier que l'automate est valide
        assert isinstance(optimized_epsilon_nfa, EpsilonNFA)
        assert optimized_epsilon_nfa.validate()

    def test_reduce_epsilon_transitions_invalid_type(self):
        """Test la réduction des transitions epsilon avec un type invalide."""
        optimizer = OptimizationAlgorithms()

        with pytest.raises(OptimizationError):
            optimizer.reduce_epsilon_transitions("not_an_epsilon_nfa")

    def test_validate_optimization(self):
        """Test la validation d'optimisation."""
        # Créer un DFA simple
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Valider l'optimisation
        is_valid = optimizer.validate_optimization(dfa, dfa)
        assert is_valid

    def test_get_optimization_stats(self):
        """Test la récupération des statistiques d'optimisation."""
        # Créer un DFA simple
        states = {"q0", "q1"}
        alphabet = {"a"}
        transitions = {("q0", "a"): "q1"}
        initial_state = "q0"
        final_states = {"q1"}

        dfa = DFA(states, alphabet, transitions, initial_state, final_states)
        optimizer = OptimizationAlgorithms()

        # Récupérer les statistiques
        stats = optimizer.get_optimization_stats(dfa, dfa)

        # Vérifier les statistiques
        assert "original_states" in stats
        assert "optimized_states" in stats
        assert "state_reduction" in stats
        assert "state_reduction_percent" in stats
        assert "optimization_stats" in stats

    def test_clear_cache(self):
        """Test le vidage du cache."""
        optimizer = OptimizationAlgorithms()

        # Ajouter quelque chose au cache
        optimizer._cache["test"] = "value"
        assert len(optimizer.cache) == 1

        # Vider le cache
        optimizer.clear_cache()
        assert len(optimizer.cache) == 0

    def test_get_cache_stats(self):
        """Test la récupération des statistiques du cache."""
        optimizer = OptimizationAlgorithms()

        # Ajouter quelque chose au cache
        optimizer._cache["test"] = "value"

        # Récupérer les statistiques du cache
        cache_stats = optimizer.get_cache_stats()

        # Vérifier les statistiques
        assert cache_stats["cache_size"] == 1
        assert "test" in cache_stats["cache_keys"]

    def test_set_cache_size(self):
        """Test la définition de la taille du cache."""
        optimizer = OptimizationAlgorithms()

        # Définir une taille de cache valide
        optimizer.set_cache_size(100)

        # Vérifier qu'aucune exception n'est levée
        assert True

    def test_set_cache_size_invalid(self):
        """Test la définition d'une taille de cache invalide."""
        optimizer = OptimizationAlgorithms()

        # Définir une taille de cache invalide
        with pytest.raises(OptimizationError):
            optimizer.set_cache_size(-1)


class TestOptimizationStats:
    """Tests pour la classe OptimizationStats."""

    def test_init(self):
        """Test l'initialisation des statistiques."""
        stats = OptimizationStats()

        # Vérifier que les statistiques sont vides
        assert len(stats._optimizations) == 0

    def test_add_optimization(self):
        """Test l'ajout d'une optimisation."""
        stats = OptimizationStats()

        # Ajouter une optimisation
        stats.add_optimization("test_optimization", 1.0, 50.0)

        # Vérifier que l'optimisation a été ajoutée
        assert len(stats._optimizations) == 1
        assert stats._optimizations[0]["type"] == "test_optimization"
        assert stats._optimizations[0]["time"] == 1.0
        assert stats._optimizations[0]["improvement"] == 50.0

    def test_get_stats_empty(self):
        """Test la récupération des statistiques quand elles sont vides."""
        stats = OptimizationStats()

        # Récupérer les statistiques
        stats_dict = stats.get_stats()

        # Vérifier les statistiques
        assert stats_dict["total_optimizations"] == 0

    def test_get_stats_with_data(self):
        """Test la récupération des statistiques avec des données."""
        stats = OptimizationStats()

        # Ajouter plusieurs optimisations
        stats.add_optimization("test1", 1.0, 50.0)
        stats.add_optimization("test2", 2.0, 75.0)
        stats.add_optimization("test1", 1.5, 60.0)

        # Récupérer les statistiques
        stats_dict = stats.get_stats()

        # Vérifier les statistiques
        assert stats_dict["total_optimizations"] == 3
        assert stats_dict["total_time"] == 4.5
        assert stats_dict["average_time"] == 1.5
        assert stats_dict["average_improvement"] == 61.666666666666664

        # Vérifier les statistiques par type
        by_type = stats_dict["optimizations_by_type"]
        assert "test1" in by_type
        assert "test2" in by_type
        assert by_type["test1"]["count"] == 2
        assert by_type["test2"]["count"] == 1

    def test_reset(self):
        """Test la remise à zéro des statistiques."""
        stats = OptimizationStats()

        # Ajouter des optimisations
        stats.add_optimization("test", 1.0, 50.0)
        assert len(stats._optimizations) == 1

        # Remettre à zéro
        stats.reset()
        assert len(stats._optimizations) == 0


class TestTransitionChange:
    """Tests pour la classe TransitionChange."""

    def test_init_valid(self):
        """Test l'initialisation avec des paramètres valides."""
        change = TransitionChange("q0", "a", "q1", "q2")

        assert change.state == "q0"
        assert change.symbol == "a"
        assert change.old_target == "q1"
        assert change.new_target == "q2"

    def test_init_invalid_state(self):
        """Test l'initialisation avec un état invalide."""
        with pytest.raises(ValueError):
            TransitionChange("", "a", "q1", "q2")

    def test_init_invalid_symbol(self):
        """Test l'initialisation avec un symbole invalide."""
        with pytest.raises(ValueError):
            TransitionChange("q0", "", "q1", "q2")

    def test_repr(self):
        """Test la représentation string."""
        change = TransitionChange("q0", "a", "q1", "q2")
        repr_str = repr(change)

        assert "TransitionChange" in repr_str
        assert "q0" in repr_str
        assert "a" in repr_str
        assert "q1" in repr_str
        assert "q2" in repr_str

    def test_eq(self):
        """Test l'égalité entre deux changements."""
        change1 = TransitionChange("q0", "a", "q1", "q2")
        change2 = TransitionChange("q0", "a", "q1", "q2")
        change3 = TransitionChange("q0", "b", "q1", "q2")

        assert change1 == change2
        assert change1 != change3
        assert change1 != "not_a_transition_change"

    def test_hash(self):
        """Test le calcul du hash."""
        change1 = TransitionChange("q0", "a", "q1", "q2")
        change2 = TransitionChange("q0", "a", "q1", "q2")
        change3 = TransitionChange("q0", "b", "q1", "q2")

        assert hash(change1) == hash(change2)
        assert hash(change1) != hash(change3)

    def test_is_addition(self):
        """Test la détection d'une addition."""
        change = TransitionChange("q0", "a", None, "q1")
        assert change.is_addition()

        change = TransitionChange("q0", "a", "q1", "q2")
        assert not change.is_addition()

    def test_is_removal(self):
        """Test la détection d'une suppression."""
        change = TransitionChange("q0", "a", "q1", None)
        assert change.is_removal()

        change = TransitionChange("q0", "a", "q1", "q2")
        assert not change.is_removal()

    def test_is_modification(self):
        """Test la détection d'une modification."""
        change = TransitionChange("q0", "a", "q1", "q2")
        assert change.is_modification()

        change = TransitionChange("q0", "a", None, "q1")
        assert not change.is_modification()

        change = TransitionChange("q0", "a", "q1", None)
        assert not change.is_modification()


class TestOptimizationExceptions:
    """Tests pour les exceptions d'optimisation."""

    def test_optimization_error(self):
        """Test l'exception OptimizationError."""
        error = OptimizationError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"

    def test_optimization_timeout_error(self):
        """Test l'exception OptimizationTimeoutError."""
        error = OptimizationTimeoutError("Timeout error", 5.0)
        assert str(error) == "Timeout error"
        assert error.timeout_duration == 5.0

    def test_optimization_memory_error(self):
        """Test l'exception OptimizationMemoryError."""
        error = OptimizationMemoryError("Memory error", 1024)
        assert str(error) == "Memory error"
        assert error.memory_required == 1024

    def test_optimization_validation_error(self):
        """Test l'exception OptimizationValidationError."""
        error = OptimizationValidationError("Validation error", "Details")
        assert str(error) == "Validation error"
        assert error.validation_details == "Details"
