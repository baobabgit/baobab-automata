"""
Tests unitaires pour les algorithmes spécialisés.

Ce module teste les algorithmes spécialisés pour les grammaires hors-contexte
et les automates à pile, incluant CYK, Earley, et les algorithmes de normalisation.
"""

import pytest

from baobab_automata.pushdown.specialized_algorithms import (
    SpecializedAlgorithms,
    ParseTree,
    AlgorithmStats,
)
from baobab_automata.pushdown.specialized_exceptions import (
    AlgorithmError,
    AlgorithmTimeoutError,
    AlgorithmMemoryError,
    CYKError,
    EarleyError,
    LeftRecursionError,
    EmptyProductionError,
    NormalizationError,
)
from baobab_automata.pushdown.grammar_types import (
    ContextFreeGrammar,
    Production,
)


class TestSpecializedAlgorithms:
    """Tests pour la classe SpecializedAlgorithms."""

    @pytest.fixture
    def algorithms(self):
        """Fixture pour créer une instance d'algorithmes spécialisés."""
        return SpecializedAlgorithms(enable_caching=True, max_cache_size=100)

    @pytest.fixture
    def chomsky_grammar(self):
        """Grammaire en forme normale de Chomsky pour les tests CYK."""
        return ContextFreeGrammar(
            variables={"S", "A", "B"},
            terminals={"a", "b"},
            productions={
                Production("S", ("A", "B")),
                Production("A", ("a",)),
                Production("B", ("b",)),
            },
            start_symbol="S",
        )

    @pytest.fixture
    def general_grammar(self):
        """Grammaire générale pour les tests Earley."""
        return ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a", "b"},
            productions={
                Production("S", ("a", "A")),
                Production("A", ("b",)),
                Production("A", ("A", "b")),
            },
            start_symbol="S",
        )

    @pytest.fixture
    def left_recursive_grammar(self):
        """Grammaire avec récursivité gauche."""
        return ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a", "b"},
            productions={Production("S", ("S", "a")), Production("S", ("b",))},
            start_symbol="S",
        )

    @pytest.fixture
    def empty_production_grammar(self):
        """Grammaire avec productions vides."""
        return ContextFreeGrammar(
            variables={"S", "A"},
            terminals={"a"},
            productions={
                Production("S", ("A",)),
                Production("A", ("a",)),
                Production("A", ()),
            },
            start_symbol="S",
        )

    def test_init_default(self):
        """Test de l'initialisation par défaut."""
        algorithms = SpecializedAlgorithms()
        assert algorithms.enable_caching is True
        assert algorithms.max_cache_size == 1000
        assert algorithms.timeout == 60.0

    def test_init_custom(self):
        """Test de l'initialisation avec paramètres personnalisés."""
        algorithms = SpecializedAlgorithms(
            enable_caching=False, max_cache_size=500, timeout=30.0
        )
        assert algorithms.enable_caching is False
        assert algorithms.max_cache_size == 500
        assert algorithms.timeout == 30.0

    def test_init_invalid_cache_size(self):
        """Test de l'initialisation avec taille de cache invalide."""
        with pytest.raises(
            AlgorithmError, match="La taille du cache doit être positive"
        ):
            SpecializedAlgorithms(max_cache_size=0)

    def test_init_invalid_timeout(self):
        """Test de l'initialisation avec timeout invalide."""
        with pytest.raises(
            AlgorithmError, match="Le timeout doit être positif"
        ):
            SpecializedAlgorithms(timeout=0)

    def test_configure_algorithm(self, algorithms):
        """Test de la configuration d'un algorithme."""
        algorithms.configure_algorithm("CYK", {"optimize": False})
        assert algorithms._algorithm_config["CYK"]["optimize"] is False

    def test_configure_algorithm_invalid_type(self, algorithms):
        """Test de la configuration d'un algorithme invalide."""
        with pytest.raises(AlgorithmError, match="Type d'algorithme inconnu"):
            algorithms.configure_algorithm("Invalid", {})

    def test_configure_algorithm_invalid_key(self, algorithms):
        """Test de la configuration avec clé invalide."""
        with pytest.raises(AlgorithmError, match="Clé de paramètre invalide"):
            algorithms.configure_algorithm("CYK", {123: "value"})

    def test_cyk_parse_success(self, algorithms, chomsky_grammar):
        """Test de parsing CYK réussi."""
        result = algorithms.cyk_parse(chomsky_grammar, "ab")
        assert result is True

    def test_cyk_parse_failure(self, algorithms, chomsky_grammar):
        """Test de parsing CYK échoué."""
        result = algorithms.cyk_parse(chomsky_grammar, "ba")
        assert result is False

    def test_cyk_parse_empty_word(self, algorithms, chomsky_grammar):
        """Test de parsing CYK avec mot vide."""
        result = algorithms.cyk_parse(chomsky_grammar, "")
        assert result is False

    def test_cyk_parse_not_chomsky(self, algorithms, general_grammar):
        """Test de parsing CYK avec grammaire non-Chomsky."""
        with pytest.raises(
            CYKError,
            match="La grammaire doit être en forme normale de Chomsky",
        ):
            algorithms.cyk_parse(general_grammar, "ab")

    def test_cyk_parse_with_tree_success(self, algorithms, chomsky_grammar):
        """Test de parsing CYK avec arbre de dérivation réussi."""
        tree = algorithms.cyk_parse_with_tree(chomsky_grammar, "ab")
        assert tree is not None
        assert tree.symbol == "S"
        assert len(tree.children) == 2

    def test_cyk_parse_with_tree_failure(self, algorithms, chomsky_grammar):
        """Test de parsing CYK avec arbre de dérivation échoué."""
        tree = algorithms.cyk_parse_with_tree(chomsky_grammar, "ba")
        assert tree is None

    def test_cyk_parse_optimized(self, algorithms, chomsky_grammar):
        """Test de parsing CYK optimisé."""
        result = algorithms.cyk_parse_optimized(chomsky_grammar, "ab")
        assert result is True

    def test_earley_parse_success(self, algorithms, general_grammar):
        """Test de parsing Earley réussi."""
        result = algorithms.earley_parse(general_grammar, "ab")
        assert result is True

    def test_earley_parse_failure(self, algorithms, general_grammar):
        """Test de parsing Earley échoué."""
        result = algorithms.earley_parse(general_grammar, "ba")
        assert result is False

    def test_earley_parse_empty_word(self, algorithms, general_grammar):
        """Test de parsing Earley avec mot vide."""
        result = algorithms.earley_parse(general_grammar, "")
        assert result is False

    def test_earley_parse_with_tree_success(self, algorithms, general_grammar):
        """Test de parsing Earley avec arbre de dérivation réussi."""
        tree = algorithms.earley_parse_with_tree(general_grammar, "ab")
        assert tree is not None
        assert tree.symbol == "S"

    def test_earley_parse_with_tree_failure(self, algorithms, general_grammar):
        """Test de parsing Earley avec arbre de dérivation échoué."""
        tree = algorithms.earley_parse_with_tree(general_grammar, "ba")
        assert tree is None

    def test_earley_parse_optimized(self, algorithms, general_grammar):
        """Test de parsing Earley optimisé."""
        result = algorithms.earley_parse_optimized(general_grammar, "ab")
        assert result is True

    def test_detect_left_recursion(self, algorithms, left_recursive_grammar):
        """Test de détection de récursivité gauche."""
        left_recursion = algorithms.detect_left_recursion(
            left_recursive_grammar
        )
        assert "S" in left_recursion
        assert "S a" in left_recursion["S"]

    def test_detect_left_recursion_none(self, algorithms, chomsky_grammar):
        """Test de détection de récursivité gauche (aucune)."""
        left_recursion = algorithms.detect_left_recursion(chomsky_grammar)
        assert not left_recursion

    def test_eliminate_left_recursion(
        self, algorithms, left_recursive_grammar
    ):
        """Test d'élimination de récursivité gauche."""
        new_grammar = algorithms.eliminate_left_recursion(
            left_recursive_grammar
        )

        # Vérifier qu'il n'y a plus de récursivité gauche
        left_recursion = algorithms.detect_left_recursion(new_grammar)
        assert not left_recursion

        # Vérifier que la grammaire a plus de variables
        assert len(new_grammar.variables) > len(
            left_recursive_grammar.variables
        )

    def test_eliminate_indirect_left_recursion(
        self, algorithms, left_recursive_grammar
    ):
        """Test d'élimination de récursivité gauche indirecte."""
        new_grammar = algorithms.eliminate_indirect_left_recursion(
            left_recursive_grammar
        )
        assert isinstance(new_grammar, ContextFreeGrammar)

    def test_detect_empty_productions(
        self, algorithms, empty_production_grammar
    ):
        """Test de détection de productions vides."""
        nullable = algorithms.detect_empty_productions(
            empty_production_grammar
        )
        assert "A" in nullable
        assert "S" in nullable

    def test_detect_empty_productions_none(self, algorithms, chomsky_grammar):
        """Test de détection de productions vides (aucune)."""
        nullable = algorithms.detect_empty_productions(chomsky_grammar)
        assert not nullable

    def test_eliminate_empty_productions(
        self, algorithms, empty_production_grammar
    ):
        """Test d'élimination de productions vides."""
        new_grammar = algorithms.eliminate_empty_productions(
            empty_production_grammar
        )

        # Vérifier qu'il n'y a plus de productions vides
        nullable = algorithms.detect_empty_productions(new_grammar)
        assert not nullable

    def test_to_chomsky_normal_form(self, algorithms, general_grammar):
        """Test de conversion en forme normale de Chomsky."""
        chomsky_grammar = algorithms.to_chomsky_normal_form(general_grammar)
        assert isinstance(chomsky_grammar, ContextFreeGrammar)

        # Vérifier que la grammaire est en forme normale de Chomsky
        assert algorithms._is_chomsky_normal_form(chomsky_grammar)

    def test_to_greibach_normal_form(self, algorithms, general_grammar):
        """Test de conversion en forme normale de Greibach."""
        greibach_grammar = algorithms.to_greibach_normal_form(general_grammar)
        assert isinstance(greibach_grammar, ContextFreeGrammar)

    def test_detect_ambiguity(self, algorithms, general_grammar):
        """Test de détection d'ambiguïté."""
        is_ambiguous = algorithms.detect_ambiguity(general_grammar)
        assert isinstance(is_ambiguous, bool)

    def test_analyze_recursion(self, algorithms, left_recursive_grammar):
        """Test d'analyse de récursivité."""
        analysis = algorithms.analyze_recursion(left_recursive_grammar)
        assert "left_recursion" in analysis
        assert "has_left_recursion" in analysis
        assert "recursive_variables" in analysis
        assert analysis["has_left_recursion"] is True

    def test_analyze_symbols(self, algorithms, chomsky_grammar):
        """Test d'analyse des symboles."""
        analysis = algorithms.analyze_symbols(chomsky_grammar)
        assert "variables" in analysis
        assert "terminals" in analysis
        assert "productions" in analysis
        assert "productions_by_variable" in analysis
        assert analysis["variables"] == 3
        assert analysis["terminals"] == 2
        assert analysis["productions"] == 3

    def test_clear_cache(self, algorithms, chomsky_grammar):
        """Test de vidage du cache."""
        # Utiliser le cache
        algorithms.cyk_parse(chomsky_grammar, "ab")
        assert len(algorithms._cache) > 0

        # Vider le cache
        algorithms.clear_cache()
        assert len(algorithms._cache) == 0
        assert algorithms._cache_stats["hits"] == 0
        assert algorithms._cache_stats["misses"] == 0

    def test_get_cache_stats(self, algorithms, chomsky_grammar):
        """Test de récupération des statistiques du cache."""
        # Utiliser le cache
        algorithms.cyk_parse(chomsky_grammar, "ab")
        algorithms.cyk_parse(chomsky_grammar, "ab")  # Hit

        stats = algorithms.get_cache_stats()
        assert "hits" in stats
        assert "misses" in stats
        assert "hit_rate" in stats
        assert "size" in stats
        assert "max_size" in stats
        assert stats["hits"] >= 1
        assert stats["misses"] >= 1

    def test_get_performance_stats(self, algorithms, chomsky_grammar):
        """Test de récupération des statistiques de performance."""
        # Exécuter quelques algorithmes
        algorithms.cyk_parse(chomsky_grammar, "ab")
        algorithms.earley_parse(chomsky_grammar, "ab")

        stats = algorithms.get_performance_stats()
        assert "CYK" in stats
        assert "Earley" in stats

        for algo_type, algo_stats in stats.items():
            assert "count" in algo_stats
            assert "total_time" in algo_stats
            assert "average_time" in algo_stats
            assert "cache_hit_rate" in algo_stats

    def test_to_dict(self, algorithms):
        """Test de sérialisation en dictionnaire."""
        data = algorithms.to_dict()
        assert "enable_caching" in data
        assert "max_cache_size" in data
        assert "timeout" in data
        assert "algorithm_config" in data
        assert "cache_stats" in data

    def test_from_dict(self):
        """Test de désérialisation depuis un dictionnaire."""
        data = {
            "enable_caching": False,
            "max_cache_size": 500,
            "timeout": 30.0,
            "algorithm_config": {"CYK": {"optimize": False}},
        }

        algorithms = SpecializedAlgorithms.from_dict(data)
        assert algorithms.enable_caching is False
        assert algorithms.max_cache_size == 500
        assert algorithms.timeout == 30.0
        assert algorithms._algorithm_config["CYK"]["optimize"] is False

    def test_from_dict_invalid(self):
        """Test de désérialisation avec données invalides."""
        with pytest.raises(
            AlgorithmError, match="Les données doivent être un dictionnaire"
        ):
            SpecializedAlgorithms.from_dict("not a dict")

    def test_caching_behavior(self, algorithms, chomsky_grammar):
        """Test du comportement du cache."""
        # Premier appel - miss
        result1 = algorithms.cyk_parse(chomsky_grammar, "ab")
        assert result1 is True

        # Deuxième appel - hit
        result2 = algorithms.cyk_parse(chomsky_grammar, "ab")
        assert result2 is True

        # Vérifier les statistiques du cache
        stats = algorithms.get_cache_stats()
        assert stats["hits"] >= 1
        assert stats["misses"] >= 1

    def test_cache_size_limit(self, algorithms, chomsky_grammar):
        """Test de la limite de taille du cache."""
        # Créer un cache avec une petite taille
        small_algorithms = SpecializedAlgorithms(max_cache_size=2)

        # Remplir le cache
        small_algorithms.cyk_parse(chomsky_grammar, "ab")
        small_algorithms.cyk_parse(chomsky_grammar, "ba")
        small_algorithms.cyk_parse(chomsky_grammar, "aa")

        # Le cache ne devrait pas dépasser la limite
        assert len(small_algorithms._cache) <= 2

    def test_error_handling_cyk(self, algorithms):
        """Test de gestion d'erreurs pour CYK."""
        with pytest.raises(CYKError):
            algorithms.cyk_parse(None, "ab")

    def test_error_handling_earley(self, algorithms):
        """Test de gestion d'erreurs pour Earley."""
        with pytest.raises(EarleyError):
            algorithms.earley_parse(None, "ab")

    def test_error_handling_left_recursion(self, algorithms):
        """Test de gestion d'erreurs pour la récursivité gauche."""
        with pytest.raises(LeftRecursionError):
            algorithms.detect_left_recursion(None)

    def test_error_handling_empty_productions(self, algorithms):
        """Test de gestion d'erreurs pour les productions vides."""
        with pytest.raises(EmptyProductionError):
            algorithms.detect_empty_productions(None)

    def test_error_handling_normalization(self, algorithms):
        """Test de gestion d'erreurs pour la normalisation."""
        with pytest.raises(NormalizationError):
            algorithms.to_chomsky_normal_form(None)


class TestParseTree:
    """Tests pour la classe ParseTree."""

    def test_parse_tree_creation(self):
        """Test de création d'un arbre de dérivation."""
        tree = ParseTree("S", [], 0, 2)
        assert tree.symbol == "S"
        assert tree.children == []
        assert tree.start_pos == 0
        assert tree.end_pos == 2

    def test_parse_tree_with_children(self):
        """Test de création d'un arbre avec enfants."""
        child1 = ParseTree("A", [], 0, 1)
        child2 = ParseTree("B", [], 1, 2)
        tree = ParseTree("S", [child1, child2], 0, 2)

        assert tree.symbol == "S"
        assert len(tree.children) == 2
        assert tree.children[0] == child1
        assert tree.children[1] == child2

    def test_parse_tree_str(self):
        """Test de représentation string d'un arbre."""
        child1 = ParseTree("A", [], 0, 1)
        child2 = ParseTree("B", [], 1, 2)
        tree = ParseTree("S", [child1, child2], 0, 2)

        expected = "(S A B)"
        assert str(tree) == expected

    def test_parse_tree_str_leaf(self):
        """Test de représentation string d'une feuille."""
        tree = ParseTree("a", [], 0, 1)
        assert str(tree) == "a"


class TestAlgorithmStats:
    """Tests pour la classe AlgorithmStats."""

    def test_algorithm_stats_creation(self):
        """Test de création de statistiques d'algorithme."""
        stats = AlgorithmStats(
            algorithm_type="CYK",
            execution_time=0.1,
            memory_used=1024,
            cache_hits=5,
            cache_misses=2,
            iterations=10,
        )

        assert stats.algorithm_type == "CYK"
        assert stats.execution_time == 0.1
        assert stats.memory_used == 1024
        assert stats.cache_hits == 5
        assert stats.cache_misses == 2
        assert stats.iterations == 10

    def test_cache_hit_rate(self):
        """Test du calcul du taux de réussite du cache."""
        stats = AlgorithmStats(
            algorithm_type="CYK",
            execution_time=0.1,
            memory_used=1024,
            cache_hits=3,
            cache_misses=2,
        )

        expected_rate = 3 / (3 + 2)  # 0.6
        assert stats.cache_hit_rate == expected_rate

    def test_cache_hit_rate_zero(self):
        """Test du taux de réussite du cache avec zéro hits."""
        stats = AlgorithmStats(
            algorithm_type="CYK",
            execution_time=0.1,
            memory_used=1024,
            cache_hits=0,
            cache_misses=0,
        )

        assert stats.cache_hit_rate == 0.0


class TestSpecializedExceptions:
    """Tests pour les exceptions spécialisées."""

    def test_algorithm_error(self):
        """Test de l'exception AlgorithmError."""
        error = AlgorithmError("Test error", "CYK", {"key": "value"})
        assert str(error) == "AlgorithmError (CYK): Test error"
        assert error.message == "Test error"
        assert error.algorithm_type == "CYK"
        assert error.details == {"key": "value"}

    def test_algorithm_timeout_error(self):
        """Test de l'exception AlgorithmTimeoutError."""
        error = AlgorithmTimeoutError("Timeout", 60.0, "CYK")
        assert "timeout: 60.0s" in str(error)
        assert error.timeout_duration == 60.0

    def test_algorithm_memory_error(self):
        """Test de l'exception AlgorithmMemoryError."""
        error = AlgorithmMemoryError("Memory", 1024, "CYK")
        assert "limit: 1024 bytes" in str(error)
        assert error.memory_limit == 1024

    def test_left_recursion_error(self):
        """Test de l'exception LeftRecursionError."""
        error = LeftRecursionError("Left recursion", "S")
        assert "variable 'S'" in str(error)
        assert error.variable == "S"

    def test_empty_production_error(self):
        """Test de l'exception EmptyProductionError."""
        error = EmptyProductionError("Empty production", "A")
        assert "variable 'A'" in str(error)
        assert error.variable == "A"
