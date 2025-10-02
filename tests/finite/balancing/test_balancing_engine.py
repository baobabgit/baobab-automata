"""
Tests unitaires pour BalancingEngine.

Ce module teste le moteur de balancing des automates finis.
"""

import pytest
from unittest.mock import Mock, patch

from src.baobab_automata.finite.balancing.balancing_engine import BalancingEngine
from src.baobab_automata.finite.balancing.balancing_exceptions import (
    BalancingError,
    InvalidBalancingStrategyError,
)
from src.baobab_automata.finite.balancing.balancing_metrics import BalancingMetrics
from src.baobab_automata.finite.balancing.balancing_result import BalancingResult
from src.baobab_automata.finite.balancing.balancing_strategy import IBalancingStrategy
from src.baobab_automata.finite.dfa import DFA


class TestBalancingEngine:
    """Tests unitaires pour BalancingEngine."""
    
    def setup_method(self):
        """Configure les tests."""
        self.engine = BalancingEngine()
        self.mock_strategy = Mock(spec=IBalancingStrategy)
        self.mock_strategy.name = "TestStrategy"
        self.mock_strategy.description = "Test strategy"
        
        # Création d'un automate de test
        self.test_automaton = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={"q0": {"a": "q1", "b": "q0"}, "q1": {"a": "q1", "b": "q0"}},
            initial_state="q0",
            final_states={"q1"}
        )
    
    def test_init_valid_parameters(self):
        """Test l'initialisation avec des paramètres valides."""
        engine = BalancingEngine(default_timeout=30.0, max_cache_size=50)
        
        assert engine._default_timeout == 30.0
        assert engine._max_cache_size == 50
        assert len(engine._strategies) == 0
        assert len(engine._cache) == 0
        assert len(engine._metrics_cache) == 0
    
    def test_init_invalid_timeout(self):
        """Test l'initialisation avec un timeout invalide."""
        with pytest.raises(BalancingError, match="Timeout par défaut invalide"):
            BalancingEngine(default_timeout=0.0)
    
    def test_init_invalid_cache_size(self):
        """Test l'initialisation avec une taille de cache invalide."""
        with pytest.raises(BalancingError, match="Taille maximale du cache invalide"):
            BalancingEngine(max_cache_size=0)
    
    def test_register_strategy_valid(self):
        """Test l'enregistrement d'une stratégie valide."""
        self.engine.register_strategy("test", self.mock_strategy)
        
        assert "test" in self.engine._strategies
        assert self.engine._strategies["test"] == self.mock_strategy
    
    def test_register_strategy_invalid_name(self):
        """Test l'enregistrement avec un nom invalide."""
        with pytest.raises(BalancingError, match="Nom de stratégie invalide"):
            self.engine.register_strategy("", self.mock_strategy)
        
        with pytest.raises(BalancingError, match="Nom de stratégie invalide"):
            self.engine.register_strategy(None, self.mock_strategy)
    
    def test_register_strategy_invalid_strategy(self):
        """Test l'enregistrement avec une stratégie invalide."""
        with pytest.raises(BalancingError, match="Stratégie invalide"):
            self.engine.register_strategy("test", "invalid")
    
    def test_register_strategy_duplicate(self):
        """Test l'enregistrement d'une stratégie déjà existante."""
        self.engine.register_strategy("test", self.mock_strategy)
        
        with pytest.raises(BalancingError, match="Stratégie déjà enregistrée"):
            self.engine.register_strategy("test", self.mock_strategy)
    
    def test_unregister_strategy_valid(self):
        """Test le désenregistrement d'une stratégie valide."""
        self.engine.register_strategy("test", self.mock_strategy)
        self.engine.unregister_strategy("test")
        
        assert "test" not in self.engine._strategies
    
    def test_unregister_strategy_invalid(self):
        """Test le désenregistrement d'une stratégie inexistante."""
        with pytest.raises(BalancingError, match="Stratégie non enregistrée"):
            self.engine.unregister_strategy("nonexistent")
    
    def test_get_strategy_valid(self):
        """Test la récupération d'une stratégie valide."""
        self.engine.register_strategy("test", self.mock_strategy)
        strategy = self.engine.get_strategy("test")
        
        assert strategy == self.mock_strategy
    
    def test_get_strategy_invalid(self):
        """Test la récupération d'une stratégie inexistante."""
        with pytest.raises(BalancingError, match="Stratégie non enregistrée"):
            self.engine.get_strategy("nonexistent")
    
    def test_list_strategies(self):
        """Test la liste des stratégies."""
        assert self.engine.list_strategies() == []
        
        self.engine.register_strategy("test1", self.mock_strategy)
        self.engine.register_strategy("test2", self.mock_strategy)
        
        strategies = self.engine.list_strategies()
        assert "test1" in strategies
        assert "test2" in strategies
        assert len(strategies) == 2
    
    def test_balance_valid_strategy(self):
        """Test le balancing avec une stratégie valide."""
        # Configuration du mock
        mock_result = Mock(spec=BalancingResult)
        self.mock_strategy.can_balance.return_value = True
        self.mock_strategy.balance.return_value = mock_result
        
        self.engine.register_strategy("test", self.mock_strategy)
        result = self.engine.balance(self.test_automaton, "test")
        
        assert result == mock_result
        self.mock_strategy.can_balance.assert_called_once_with(self.test_automaton)
        self.mock_strategy.balance.assert_called_once_with(self.test_automaton)
    
    def test_balance_invalid_strategy(self):
        """Test le balancing avec une stratégie invalide."""
        with pytest.raises(InvalidBalancingStrategyError, match="Stratégie non enregistrée"):
            self.engine.balance(self.test_automaton, "nonexistent")
    
    def test_balance_strategy_cannot_balance(self):
        """Test le balancing avec une stratégie qui ne peut pas équilibrer."""
        self.mock_strategy.can_balance.return_value = False
        
        self.engine.register_strategy("test", self.mock_strategy)
        
        with pytest.raises(InvalidBalancingStrategyError, match="ne peut pas être appliquée"):
            self.engine.balance(self.test_automaton, "test")
    
    def test_balance_strategy_error(self):
        """Test le balancing avec une erreur de stratégie."""
        self.mock_strategy.can_balance.return_value = True
        self.mock_strategy.balance.side_effect = Exception("Strategy error")
        
        self.engine.register_strategy("test", self.mock_strategy)
        
        with pytest.raises(BalancingError, match="Erreur lors de l'application"):
            self.engine.balance(self.test_automaton, "test")
    
    def test_balance_caching(self):
        """Test la mise en cache des résultats."""
        mock_result = Mock(spec=BalancingResult)
        self.mock_strategy.can_balance.return_value = True
        self.mock_strategy.balance.return_value = mock_result
        
        self.engine.register_strategy("test", self.mock_strategy)
        
        # Premier appel
        result1 = self.engine.balance(self.test_automaton, "test")
        
        # Deuxième appel (doit utiliser le cache)
        result2 = self.engine.balance(self.test_automaton, "test")
        
        assert result1 == result2
        assert result1 == mock_result
        # La stratégie ne doit être appelée qu'une fois
        self.mock_strategy.balance.assert_called_once()
    
    def test_auto_balance_no_strategies(self):
        """Test l'auto-balancing sans stratégies."""
        with pytest.raises(BalancingError, match="Aucune stratégie de balancing appropriée trouvée"):
            self.engine.auto_balance(self.test_automaton)
    
    def test_auto_balance_with_strategies(self):
        """Test l'auto-balancing avec des stratégies."""
        # Configuration des mocks
        mock_result = Mock(spec=BalancingResult)
        self.mock_strategy.can_balance.return_value = True
        self.mock_strategy.get_priority.return_value = 0.8
        self.mock_strategy.balance.return_value = mock_result
        
        self.engine.register_strategy("test", self.mock_strategy)
        result = self.engine.auto_balance(self.test_automaton)
        
        assert result == mock_result
        self.mock_strategy.get_priority.assert_called_once_with(self.test_automaton)
        self.mock_strategy.balance.assert_called_once_with(self.test_automaton)
    
    def test_get_metrics(self):
        """Test le calcul des métriques."""
        with patch('src.baobab_automata.finite.balancing.balancing_engine.BalancingMetrics') as mock_metrics_class:
            mock_metrics = Mock(spec=BalancingMetrics)
            mock_metrics_class.from_automaton.return_value = mock_metrics
            
            result = self.engine.get_metrics(self.test_automaton)
            
            assert result == mock_metrics
            mock_metrics_class.from_automaton.assert_called_once_with(self.test_automaton)
    
    def test_get_metrics_caching(self):
        """Test la mise en cache des métriques."""
        with patch('src.baobab_automata.finite.balancing.balancing_engine.BalancingMetrics') as mock_metrics_class:
            mock_metrics = Mock(spec=BalancingMetrics)
            mock_metrics_class.from_automaton.return_value = mock_metrics
            
            # Premier appel
            result1 = self.engine.get_metrics(self.test_automaton)
            
            # Deuxième appel (doit utiliser le cache)
            result2 = self.engine.get_metrics(self.test_automaton)
            
            assert result1 == result2
            assert result1 == mock_metrics
            # Les métriques ne doivent être calculées qu'une fois
            mock_metrics_class.from_automaton.assert_called_once()
    
    def test_is_balanced_with_strategy(self):
        """Test la vérification d'équilibrage avec une stratégie spécifique."""
        self.mock_strategy.is_balanced.return_value = True
        
        self.engine.register_strategy("test", self.mock_strategy)
        result = self.engine.is_balanced(self.test_automaton, "test")
        
        assert result is True
        self.mock_strategy.is_balanced.assert_called_once_with(self.test_automaton)
    
    def test_is_balanced_without_strategy(self):
        """Test la vérification d'équilibrage sans stratégie spécifique."""
        self.mock_strategy.can_balance.return_value = True
        self.mock_strategy.is_balanced.return_value = True
        
        self.engine.register_strategy("test", self.mock_strategy)
        result = self.engine.is_balanced(self.test_automaton)
        
        assert result is True
        self.mock_strategy.can_balance.assert_called_once_with(self.test_automaton)
        self.mock_strategy.is_balanced.assert_called_once_with(self.test_automaton)
    
    def test_is_balanced_no_balanced_strategy(self):
        """Test la vérification d'équilibrage sans stratégie équilibrée."""
        self.mock_strategy.can_balance.return_value = True
        self.mock_strategy.is_balanced.return_value = False
        
        self.engine.register_strategy("test", self.mock_strategy)
        result = self.engine.is_balanced(self.test_automaton)
        
        assert result is False
    
    def test_clear_cache(self):
        """Test la suppression du cache."""
        # Ajout d'éléments au cache
        self.engine._cache["key1"] = Mock()
        self.engine._metrics_cache["key2"] = Mock()
        self.engine._cache_access_count["key1"] = 5
        
        self.engine.clear_cache()
        
        assert len(self.engine._cache) == 0
        assert len(self.engine._metrics_cache) == 0
        assert len(self.engine._cache_access_count) == 0
    
    def test_get_cache_stats(self):
        """Test l'obtention des statistiques du cache."""
        # Ajout d'éléments au cache
        self.engine._cache["key1"] = Mock()
        self.engine._metrics_cache["key2"] = Mock()
        self.engine._cache_access_count["key1"] = 5
        
        stats = self.engine.get_cache_stats()
        
        assert stats["cache_size"] == 1
        assert stats["metrics_cache_size"] == 1
        assert stats["max_cache_size"] == 100
        assert "cache_hit_rate" in stats
        assert "most_accessed" in stats
    
    def test_cache_eviction(self):
        """Test l'éviction du cache."""
        engine = BalancingEngine(max_cache_size=2)
        
        # Ajout de plus d'éléments que la taille maximale
        engine._cache["key1"] = Mock()
        engine._cache["key2"] = Mock()
        engine._cache["key3"] = Mock()
        
        # L'éviction doit avoir eu lieu
        assert len(engine._cache) <= 2
    
    def test_generate_cache_key(self):
        """Test la génération de clés de cache."""
        key1 = self.engine._generate_cache_key(self.test_automaton, "test")
        key2 = self.engine._generate_cache_key(self.test_automaton, "test")
        key3 = self.engine._generate_cache_key(self.test_automaton, "other")
        
        assert key1 == key2  # Même automate, même suffixe
        assert key1 != key3  # Même automate, suffixe différent
        assert isinstance(key1, str)
        assert "test" in key1