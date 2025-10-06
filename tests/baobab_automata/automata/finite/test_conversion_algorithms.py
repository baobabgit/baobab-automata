"""
Tests unitaires pour la classe ConversionAlgorithms.

Ce module contient tous les tests pour les algorithmes de conversion
entre différents types d'automates finis.
"""

import pytest
from unittest.mock import Mock, patch

from baobab_automata.algorithms.finite.conversion_algorithms import (
    ConversionAlgorithms,
    ConversionError,
    ConversionMemoryError,
    ConversionStats,
    ConversionTimeoutError,
    ConversionValidationError,
)
from baobab_automata.finite.dfa import DFA
from baobab_automata.finite.epsilon_nfa import EpsilonNFA
from baobab_automata.finite.nfa import NFA


class TestConversionStats:
    """Tests pour la classe ConversionStats."""

    def test_init(self):
        """Test l'initialisation de ConversionStats."""
        stats = ConversionStats()
        assert stats._conversions == {}
        assert stats._total_conversions == 0
        assert stats._total_time == 0.0

    def test_add_conversion(self):
        """Test l'ajout d'une conversion."""
        stats = ConversionStats()
        stats.add_conversion("NFA", "DFA", 0.5)

        assert stats._total_conversions == 1
        assert stats._total_time == 0.5
        assert ("NFA", "DFA") in stats._conversions
        assert stats._conversions[("NFA", "DFA")] == [0.5]

    def test_add_multiple_conversions(self):
        """Test l'ajout de plusieurs conversions."""
        stats = ConversionStats()
        stats.add_conversion("NFA", "DFA", 0.5)
        stats.add_conversion("NFA", "DFA", 0.3)
        stats.add_conversion("ε-NFA", "NFA", 0.2)

        assert stats._total_conversions == 3
        assert stats._total_time == 1.0
        assert len(stats._conversions[("NFA", "DFA")]) == 2
        assert len(stats._conversions[("ε-NFA", "NFA")]) == 1

    def test_get_stats(self):
        """Test la récupération des statistiques."""
        stats = ConversionStats()
        stats.add_conversion("NFA", "DFA", 0.5)
        stats.add_conversion("NFA", "DFA", 0.3)

        result = stats.get_stats()

        assert result["total_conversions"] == 2
        assert result["total_time"] == 0.8
        assert result["average_time"] == 0.4
        assert "conversions_by_type" in result
        assert "NFA_to_DFA" in result["conversions_by_type"]

        nfa_to_dfa_stats = result["conversions_by_type"]["NFA_to_DFA"]
        assert nfa_to_dfa_stats["count"] == 2
        assert nfa_to_dfa_stats["total_time"] == 0.8
        assert nfa_to_dfa_stats["average_time"] == 0.4
        assert nfa_to_dfa_stats["min_time"] == 0.3
        assert nfa_to_dfa_stats["max_time"] == 0.5

    def test_reset(self):
        """Test la remise à zéro des statistiques."""
        stats = ConversionStats()
        stats.add_conversion("NFA", "DFA", 0.5)
        stats.reset()

        assert stats._conversions == {}
        assert stats._total_conversions == 0
        assert stats._total_time == 0.0


class TestConversionAlgorithms:
    """Tests pour la classe ConversionAlgorithms."""

    def test_init_default(self):
        """Test l'initialisation par défaut."""
        converter = ConversionAlgorithms()

        assert converter._optimization_enabled is True
        assert converter._max_states == 1000
        assert converter._cache == {}
        assert converter._cache_hits == 0
        assert converter._cache_misses == 0

    def test_init_custom(self):
        """Test l'initialisation avec paramètres personnalisés."""
        converter = ConversionAlgorithms(optimization_enabled=False, max_states=500)

        assert converter._optimization_enabled is False
        assert converter._max_states == 500

    def test_properties(self):
        """Test des propriétés."""
        converter = ConversionAlgorithms()

        assert converter.optimization_enabled is True
        assert converter.max_states == 1000
        assert converter.cache_size == 0

    def test_clear_cache(self):
        """Test du vidage du cache."""
        converter = ConversionAlgorithms()
        converter._cache["test"] = "value"
        converter._cache_hits = 5
        converter._cache_misses = 3

        converter.clear_cache()

        assert converter._cache == {}
        assert converter._cache_hits == 0
        assert converter._cache_misses == 0

    def test_get_cache_stats(self):
        """Test des statistiques du cache."""
        converter = ConversionAlgorithms()
        converter._cache_hits = 3
        converter._cache_misses = 2

        stats = converter.get_cache_stats()

        assert stats["cache_size"] == 0
        assert stats["cache_hits"] == 3
        assert stats["cache_misses"] == 2
        assert stats["hit_rate"] == 0.6
        assert stats["total_requests"] == 5

    def test_set_cache_size(self):
        """Test de la configuration de la taille du cache."""
        converter = ConversionAlgorithms()
        converter._cache = {"key1": "value1", "key2": "value2", "key3": "value3"}

        converter.set_cache_size(2)

        assert len(converter._cache) == 2

    def test_set_cache_size_negative(self):
        """Test de la configuration d'une taille de cache négative."""
        converter = ConversionAlgorithms()

        with pytest.raises(ValueError, match="Cache size must be non-negative"):
            converter.set_cache_size(-1)

    def test_validate_automaton_valid(self):
        """Test de la validation d'un automate valide."""
        converter = ConversionAlgorithms()
        automaton = Mock()
        automaton.validate.return_value = True
        automaton.states = {"q0", "q1"}

        # Ne doit pas lever d'exception
        converter._validate_automaton(automaton)

    def test_validate_automaton_invalid(self):
        """Test de la validation d'un automate invalide."""
        converter = ConversionAlgorithms()
        automaton = Mock()
        automaton.validate.return_value = False

        with pytest.raises(ConversionValidationError):
            converter._validate_automaton(automaton)

    def test_validate_automaton_too_many_states(self):
        """Test de la validation d'un automate avec trop d'états."""
        converter = ConversionAlgorithms(max_states=2)
        automaton = Mock()
        automaton.validate.return_value = True
        automaton.states = {"q0", "q1", "q2", "q3"}

        with pytest.raises(ConversionMemoryError):
            converter._validate_automaton(automaton)

    def test_validate_conversion_equivalent(self):
        """Test de la validation d'une conversion équivalente."""
        converter = ConversionAlgorithms()

        # Créer des automates mock qui acceptent les mêmes mots
        original = Mock()
        converted = Mock()

        # Configurer les automates pour accepter les mêmes mots
        def mock_accepts(word):
            return word in ["a", "b", "ab"]

        original.accepts = mock_accepts
        converted.accepts = mock_accepts
        original.alphabet = {"a", "b"}
        converted.alphabet = {"a", "b"}

        assert converter.validate_conversion(original, converted) is True

    def test_validate_conversion_different(self):
        """Test de la validation d'une conversion non équivalente."""
        converter = ConversionAlgorithms()

        # Créer des automates mock qui acceptent des mots différents
        original = Mock()
        converted = Mock()

        original.accepts = lambda word: word == "a"
        converted.accepts = lambda word: word == "b"
        original.alphabet = {"a", "b"}
        converted.alphabet = {"a", "b"}

        assert converter.validate_conversion(original, converted) is False

    def test_optimize_automaton_dfa(self):
        """Test de l'optimisation d'un DFA."""
        converter = ConversionAlgorithms()

        # Créer un DFA mock
        dfa = Mock(spec=DFA)
        optimized_dfa = Mock(spec=DFA)
        dfa.remove_unreachable_states.return_value = optimized_dfa

        result = converter.optimize_automaton(dfa)

        assert result == optimized_dfa
        dfa.remove_unreachable_states.assert_called_once()

    def test_optimize_automaton_other(self):
        """Test de l'optimisation d'autres types d'automates."""
        converter = ConversionAlgorithms()

        # Créer un NFA mock
        nfa = Mock(spec=NFA)

        result = converter.optimize_automaton(nfa)

        # Pour l'instant, doit retourner l'automate tel quel
        assert result == nfa

    def test_optimize_automaton_disabled(self):
        """Test de l'optimisation désactivée."""
        converter = ConversionAlgorithms(optimization_enabled=False)

        automaton = Mock()

        result = converter.optimize_automaton(automaton)

        assert result == automaton


class TestNFAtoDFAConversion:
    """Tests pour les conversions NFA → DFA."""

    def test_nfa_to_dfa_simple(self):
        """Test de conversion NFA → DFA simple."""
        # Créer un NFA simple
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        dfa = ConversionAlgorithms.nfa_to_dfa(nfa)

        assert isinstance(dfa, DFA)
        assert dfa.initial_state in dfa.states
        assert len(dfa.final_states) > 0

    def test_nfa_to_dfa_optimized(self):
        """Test de conversion NFA → DFA optimisée."""
        converter = ConversionAlgorithms()

        # Créer un NFA simple
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        dfa = converter.nfa_to_dfa_optimized(nfa)

        assert isinstance(dfa, DFA)
        assert converter._cache_hits == 0  # Premier appel, pas de cache hit
        assert converter._cache_misses == 1

    def test_nfa_to_dfa_cached(self):
        """Test de conversion NFA → DFA avec cache."""
        converter = ConversionAlgorithms()

        # Créer un NFA simple
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        # Premier appel
        dfa1 = converter.nfa_to_dfa_optimized(nfa)

        # Deuxième appel (doit utiliser le cache)
        dfa2 = converter.nfa_to_dfa_optimized(nfa)

        assert dfa1 == dfa2
        assert converter._cache_hits == 1
        assert converter._cache_misses == 1


class TestEpsilonNFAtoNFAConversion:
    """Tests pour les conversions ε-NFA → NFA."""

    def test_epsilon_nfa_to_nfa_simple(self):
        """Test de conversion ε-NFA → NFA simple."""
        # Créer un ε-NFA simple
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        nfa = ConversionAlgorithms.epsilon_nfa_to_nfa(epsilon_nfa)

        assert isinstance(nfa, NFA)
        assert nfa.initial_state == "q0"
        assert "q1" in nfa.final_states

    def test_epsilon_nfa_to_nfa_optimized(self):
        """Test de conversion ε-NFA → NFA optimisée."""
        converter = ConversionAlgorithms()

        # Créer un ε-NFA simple
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        nfa = converter.epsilon_nfa_to_nfa_optimized(epsilon_nfa)

        assert isinstance(nfa, NFA)
        assert converter._cache_hits == 0
        assert converter._cache_misses == 1


class TestEpsilonNFAtoDFAConversion:
    """Tests pour les conversions ε-NFA → DFA."""

    def test_epsilon_nfa_to_dfa_direct(self):
        """Test de conversion ε-NFA → DFA directe."""
        # Créer un ε-NFA simple
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        dfa = ConversionAlgorithms.epsilon_nfa_to_dfa(epsilon_nfa)

        assert isinstance(dfa, DFA)
        assert dfa.initial_state in dfa.states
        assert len(dfa.final_states) > 0

    def test_epsilon_nfa_to_dfa_via_nfa(self):
        """Test de conversion ε-NFA → DFA via NFA."""
        converter = ConversionAlgorithms()

        # Créer un ε-NFA simple
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        dfa = converter.epsilon_nfa_to_dfa_via_nfa(epsilon_nfa)

        assert isinstance(dfa, DFA)
        assert converter._cache_hits == 0
        assert converter._cache_misses == 1


class TestRegexToAutomatonConversion:
    """Tests pour les conversions Expression Régulière → Automate."""

    def test_regex_to_automaton_empty(self):
        """Test de conversion d'une expression vide."""
        automaton = ConversionAlgorithms.regex_to_automaton("")

        assert isinstance(automaton, EpsilonNFA)
        assert automaton.initial_state == "q0"
        assert "q0" in automaton.final_states

    def test_regex_to_automaton_single_symbol(self):
        """Test de conversion d'un symbole simple."""
        automaton = ConversionAlgorithms.regex_to_automaton("a")

        assert isinstance(automaton, EpsilonNFA)
        assert automaton.alphabet == {"a"}
        assert automaton.initial_state == "q0"
        assert "q1" in automaton.final_states

    def test_regex_to_automaton_kleene_star(self):
        """Test de conversion de l'étoile de Kleene."""
        automaton = ConversionAlgorithms.regex_to_automaton("a*")

        assert isinstance(automaton, EpsilonNFA)
        assert automaton.alphabet == {"a"}
        assert "q3" in automaton.final_states

    def test_regex_to_automaton_optimized(self):
        """Test de conversion optimisée."""
        converter = ConversionAlgorithms()

        automaton = converter.regex_to_automaton_optimized("a", "dfa")

        assert isinstance(automaton, DFA)
        assert converter._cache_hits == 0
        assert converter._cache_misses == 1


class TestAutomatonToRegexConversion:
    """Tests pour les conversions Automate → Expression Régulière."""

    def test_automaton_to_regex_dfa(self):
        """Test de conversion DFA → Expression Régulière."""
        # Créer un DFA simple
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        regex = ConversionAlgorithms.automaton_to_regex(dfa)

        assert isinstance(regex, str)
        assert len(regex) > 0

    def test_automaton_to_regex_nfa(self):
        """Test de conversion NFA → Expression Régulière."""
        # Créer un NFA simple
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        regex = ConversionAlgorithms.automaton_to_regex(nfa)

        assert isinstance(regex, str)
        assert len(regex) > 0

    def test_automaton_to_regex_optimized(self):
        """Test de conversion optimisée."""
        converter = ConversionAlgorithms()

        # Créer un DFA simple
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): "q1"},
            initial_state="q0",
            final_states={"q1"},
        )

        regex = converter.automaton_to_regex_optimized(dfa)

        assert isinstance(regex, str)
        assert len(regex) > 0


class TestErrorHandling:
    """Tests pour la gestion d'erreurs."""

    def test_conversion_error(self):
        """Test de ConversionError."""
        error = ConversionError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_conversion_timeout_error(self):
        """Test de ConversionTimeoutError."""
        error = ConversionTimeoutError("Timeout")
        assert str(error) == "Timeout"
        assert isinstance(error, ConversionError)

    def test_conversion_memory_error(self):
        """Test de ConversionMemoryError."""
        error = ConversionMemoryError("Memory error")
        assert str(error) == "Memory error"
        assert isinstance(error, ConversionError)

    def test_conversion_validation_error(self):
        """Test de ConversionValidationError."""
        error = ConversionValidationError("Validation error")
        assert str(error) == "Validation error"
        assert isinstance(error, ConversionError)
