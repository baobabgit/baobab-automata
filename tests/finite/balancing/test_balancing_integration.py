"""
Tests d'intégration pour les stratégies de balancing.

Ce module teste l'intégration entre les différents composants
de balancing des automates finis.
"""

import pytest
from unittest.mock import Mock, patch

from src.baobab_automata.finite.balancing.balancing_engine import BalancingEngine
from src.baobab_automata.finite.balancing.balancing_exceptions import (
    BalancingError,
    InvalidBalancingStrategyError,
)
from src.baobab_automata.finite.balancing.memory_balancing_strategy import (
    MemoryBalancingStrategy,
)
from src.baobab_automata.finite.balancing.performance_balancing_strategy import (
    PerformanceBalancingStrategy,
)
from src.baobab_automata.finite.balancing.structural_balancing_strategy import (
    StructuralBalancingStrategy,
)
from src.baobab_automata.finite.dfa import DFA


class TestBalancingIntegration:
    """Tests d'intégration pour les stratégies de balancing."""
    
    def setup_method(self):
        """Configure les tests."""
        self.engine = BalancingEngine()
        
        # Enregistrement des stratégies
        self.structural_strategy = StructuralBalancingStrategy()
        self.performance_strategy = PerformanceBalancingStrategy()
        self.memory_strategy = MemoryBalancingStrategy()
        
        self.engine.register_strategy("structural", self.structural_strategy)
        self.engine.register_strategy("performance", self.performance_strategy)
        self.engine.register_strategy("memory", self.memory_strategy)
        
        # Automate de test
        self.test_automaton = DFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a", "b", "c"},
            transitions={
                "q0": {"a": "q1", "b": "q2"},
                "q1": {"a": "q2", "b": "q3", "c": "q1"},
                "q2": {"a": "q3", "b": "q0"},
                "q3": {"a": "q0", "b": "q1", "c": "q2"}
            },
            initial_state="q0",
            final_states={"q3"}
        )
    
    def test_engine_with_all_strategies(self):
        """Test le moteur avec toutes les stratégies enregistrées."""
        strategies = self.engine.list_strategies()
        
        assert "structural" in strategies
        assert "performance" in strategies
        assert "memory" in strategies
        assert len(strategies) == 3
    
    def test_structural_balancing_integration(self):
        """Test l'intégration de la stratégie structurelle."""
        with patch.object(self.structural_strategy, 'balance') as mock_balance:
            mock_result = Mock()
            mock_balance.return_value = mock_result
            
            result = self.engine.balance(self.test_automaton, "structural")
            
            assert result == mock_result
            mock_balance.assert_called_once_with(self.test_automaton)
    
    def test_performance_balancing_integration(self):
        """Test l'intégration de la stratégie de performance."""
        with patch.object(self.performance_strategy, 'balance') as mock_balance:
            mock_result = Mock()
            mock_balance.return_value = mock_result
            
            result = self.engine.balance(self.test_automaton, "performance")
            
            assert result == mock_result
            mock_balance.assert_called_once_with(self.test_automaton)
    
    def test_memory_balancing_integration(self):
        """Test l'intégration de la stratégie mémoire."""
        with patch.object(self.memory_strategy, 'balance') as mock_balance:
            mock_result = Mock()
            mock_balance.return_value = mock_result
            
            result = self.engine.balance(self.test_automaton, "memory")
            
            assert result == mock_result
            mock_balance.assert_called_once_with(self.test_automaton)
    
    def test_auto_balance_strategy_selection(self):
        """Test la sélection automatique de stratégie."""
        # Configuration des priorités
        with patch.object(self.structural_strategy, 'can_balance', return_value=True):
            with patch.object(self.structural_strategy, 'get_priority', return_value=0.8):
                with patch.object(self.structural_strategy, 'balance') as mock_balance:
                    mock_result = Mock()
                    mock_balance.return_value = mock_result
                    
                    result = self.engine.auto_balance(self.test_automaton)
                    
                    assert result == mock_result
                    mock_balance.assert_called_once_with(self.test_automaton)
    
    def test_auto_balance_no_suitable_strategy(self):
        """Test l'auto-balancing sans stratégie appropriée."""
        # Configuration pour qu'aucune stratégie ne puisse équilibrer
        with patch.object(self.structural_strategy, 'can_balance', return_value=False):
            with patch.object(self.performance_strategy, 'can_balance', return_value=False):
                with patch.object(self.memory_strategy, 'can_balance', return_value=False):
                    with pytest.raises(BalancingError, match="Aucune stratégie de balancing appropriée trouvée"):
                        self.engine.auto_balance(self.test_automaton)
    
    def test_strategy_cannot_balance_error(self):
        """Test l'erreur quand une stratégie ne peut pas équilibrer."""
        with patch.object(self.structural_strategy, 'can_balance', return_value=False):
            with pytest.raises(InvalidBalancingStrategyError, match="ne peut pas être appliquée"):
                self.engine.balance(self.test_automaton, "structural")
    
    def test_strategy_balance_error(self):
        """Test l'erreur lors du balancing."""
        with patch.object(self.structural_strategy, 'can_balance', return_value=True):
            with patch.object(self.structural_strategy, 'balance', side_effect=Exception("Balance error")):
                with pytest.raises(BalancingError, match="Erreur lors de l'application"):
                    self.engine.balance(self.test_automaton, "structural")
    
    def test_cache_functionality(self):
        """Test la fonctionnalité de cache."""
        with patch.object(self.structural_strategy, 'can_balance', return_value=True):
            with patch.object(self.structural_strategy, 'balance') as mock_balance:
                mock_result = Mock()
                mock_balance.return_value = mock_result
                
                # Premier appel
                result1 = self.engine.balance(self.test_automaton, "structural")
                
                # Deuxième appel (doit utiliser le cache)
                result2 = self.engine.balance(self.test_automaton, "structural")
                
                assert result1 == result2
                assert result1 == mock_result
                # La stratégie ne doit être appelée qu'une fois
                mock_balance.assert_called_once()
    
    def test_metrics_caching(self):
        """Test la mise en cache des métriques."""
        with patch('src.baobab_automata.finite.balancing.balancing_engine.BalancingMetrics') as mock_metrics_class:
            mock_metrics = Mock()
            mock_metrics_class.from_automaton.return_value = mock_metrics
            
            # Premier appel
            result1 = self.engine.get_metrics(self.test_automaton)
            
            # Deuxième appel (doit utiliser le cache)
            result2 = self.engine.get_metrics(self.test_automaton)
            
            assert result1 == result2
            assert result1 == mock_metrics
            # Les métriques ne doivent être calculées qu'une fois
            mock_metrics_class.from_automaton.assert_called_once()
    
    def test_is_balanced_with_specific_strategy(self):
        """Test la vérification d'équilibrage avec une stratégie spécifique."""
        with patch.object(self.structural_strategy, 'is_balanced', return_value=True):
            result = self.engine.is_balanced(self.test_automaton, "structural")
            
            assert result is True
            self.structural_strategy.is_balanced.assert_called_once_with(self.test_automaton)
    
    def test_is_balanced_auto_detection(self):
        """Test la détection automatique d'équilibrage."""
        with patch.object(self.structural_strategy, 'can_balance', return_value=True):
            with patch.object(self.structural_strategy, 'is_balanced', return_value=True):
                result = self.engine.is_balanced(self.test_automaton)
                
                assert result is True
                self.structural_strategy.can_balance.assert_called_once_with(self.test_automaton)
                self.structural_strategy.is_balanced.assert_called_once_with(self.test_automaton)
    
    def test_is_balanced_no_balanced_strategy(self):
        """Test la vérification d'équilibrage sans stratégie équilibrée."""
        with patch.object(self.structural_strategy, 'can_balance', return_value=True):
            with patch.object(self.structural_strategy, 'is_balanced', return_value=False):
                with patch.object(self.performance_strategy, 'can_balance', return_value=True):
                    with patch.object(self.performance_strategy, 'is_balanced', return_value=False):
                        with patch.object(self.memory_strategy, 'can_balance', return_value=True):
                            with patch.object(self.memory_strategy, 'is_balanced', return_value=False):
                                result = self.engine.is_balanced(self.test_automaton)
                                
                                assert result is False
    
    def test_cache_management(self):
        """Test la gestion du cache."""
        # Ajout d'éléments au cache
        self.engine._cache["key1"] = Mock()
        self.engine._metrics_cache["key2"] = Mock()
        
        # Vérification des statistiques
        stats = self.engine.get_cache_stats()
        assert stats["cache_size"] == 1
        assert stats["metrics_cache_size"] == 1
        
        # Suppression du cache
        self.engine.clear_cache()
        
        # Vérification que le cache est vide
        stats_after = self.engine.get_cache_stats()
        assert stats_after["cache_size"] == 0
        assert stats_after["metrics_cache_size"] == 0
    
    def test_strategy_unregistration(self):
        """Test le désenregistrement d'une stratégie."""
        # Vérification que la stratégie est enregistrée
        assert "structural" in self.engine.list_strategies()
        
        # Désenregistrement
        self.engine.unregister_strategy("structural")
        
        # Vérification que la stratégie n'est plus enregistrée
        assert "structural" not in self.engine.list_strategies()
        
        # Tentative d'utilisation de la stratégie désenregistrée
        with pytest.raises(InvalidBalancingStrategyError, match="Stratégie non enregistrée"):
            self.engine.balance(self.test_automaton, "structural")
    
    def test_multiple_strategies_priority(self):
        """Test la priorité entre plusieurs stratégies."""
        # Configuration des priorités
        with patch.object(self.structural_strategy, 'can_balance', return_value=True):
            with patch.object(self.structural_strategy, 'get_priority', return_value=0.6):
                with patch.object(self.performance_strategy, 'can_balance', return_value=True):
                    with patch.object(self.performance_strategy, 'get_priority', return_value=0.8):
                        with patch.object(self.performance_strategy, 'balance') as mock_balance:
                            mock_result = Mock()
                            mock_balance.return_value = mock_result
                            
                            result = self.engine.auto_balance(self.test_automaton)
                            
                            # La stratégie de performance doit être sélectionnée (priorité plus élevée)
                            assert result == mock_result
                            mock_balance.assert_called_once_with(self.test_automaton)
    
    def test_strategy_error_handling(self):
        """Test la gestion des erreurs de stratégie."""
        with patch.object(self.structural_strategy, 'can_balance', return_value=True):
            with patch.object(self.structural_strategy, 'balance', side_effect=ValueError("Test error")):
                with pytest.raises(BalancingError, match="Erreur lors de l'application"):
                    self.engine.balance(self.test_automaton, "structural")
    
    def test_engine_with_no_strategies(self):
        """Test le moteur sans stratégies enregistrées."""
        empty_engine = BalancingEngine()
        
        # Tentative d'auto-balancing sans stratégies
        with pytest.raises(BalancingError, match="Aucune stratégie de balancing appropriée trouvée"):
            empty_engine.auto_balance(self.test_automaton)
        
        # Tentative d'utilisation d'une stratégie inexistante
        with pytest.raises(InvalidBalancingStrategyError, match="Stratégie non enregistrée"):
            empty_engine.balance(self.test_automaton, "nonexistent")
    
    def test_strategy_interface_compliance(self):
        """Test la conformité des stratégies à l'interface."""
        # Vérification que toutes les stratégies implémentent l'interface
        assert hasattr(self.structural_strategy, 'name')
        assert hasattr(self.structural_strategy, 'description')
        assert hasattr(self.structural_strategy, 'balance')
        assert hasattr(self.structural_strategy, 'get_metrics')
        assert hasattr(self.structural_strategy, 'is_balanced')
        assert hasattr(self.structural_strategy, 'can_balance')
        
        assert hasattr(self.performance_strategy, 'name')
        assert hasattr(self.performance_strategy, 'description')
        assert hasattr(self.performance_strategy, 'balance')
        assert hasattr(self.performance_strategy, 'get_metrics')
        assert hasattr(self.performance_strategy, 'is_balanced')
        assert hasattr(self.performance_strategy, 'can_balance')
        
        assert hasattr(self.memory_strategy, 'name')
        assert hasattr(self.memory_strategy, 'description')
        assert hasattr(self.memory_strategy, 'balance')
        assert hasattr(self.memory_strategy, 'get_metrics')
        assert hasattr(self.memory_strategy, 'is_balanced')
        assert hasattr(self.memory_strategy, 'can_balance')