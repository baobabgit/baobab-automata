"""
Tests unitaires pour BalancingResult.

Ce module teste les résultats de balancing des automates finis.
"""

import pytest
from unittest.mock import Mock

from src.baobab_automata.finite.balancing.balancing_metrics import BalancingMetrics
from src.baobab_automata.finite.balancing.balancing_result import BalancingResult
from src.baobab_automata.finite.dfa import DFA


class TestBalancingResult:
    """Tests unitaires pour BalancingResult."""
    
    def setup_method(self):
        """Configure les tests."""
        self.test_automaton = DFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={"q0": {"a": "q1", "b": "q0"}, "q1": {"a": "q1", "b": "q0"}},
            initial_state="q0",
            final_states={"q1"}
        )
        
        self.mock_metrics = Mock(spec=BalancingMetrics)
        self.mock_metrics.balance_score = 0.8
    
    def test_init_valid_parameters(self):
        """Test l'initialisation avec des paramètres valides."""
        result = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=0.2,
            execution_time=1.5,
            memory_usage=1024,
            strategy_name="TestStrategy"
        )
        
        assert result.original_automaton == self.test_automaton
        assert result.balanced_automaton == self.test_automaton
        assert result.metrics_before == self.mock_metrics
        assert result.metrics_after == self.mock_metrics
        assert result.improvement_ratio == 0.2
        assert result.execution_time == 1.5
        assert result.memory_usage == 1024
        assert result.strategy_name == "TestStrategy"
    
    def test_init_invalid_improvement_ratio_negative(self):
        """Test l'initialisation avec un ratio d'amélioration négatif."""
        with pytest.raises(ValueError, match="Ratio d'amélioration invalide"):
            BalancingResult(
                original_automaton=self.test_automaton,
                balanced_automaton=self.test_automaton,
                metrics_before=self.mock_metrics,
                metrics_after=self.mock_metrics,
                improvement_ratio=-0.1,
                execution_time=1.5,
                memory_usage=1024,
                strategy_name="TestStrategy"
            )
    
    def test_init_invalid_improvement_ratio_too_high(self):
        """Test l'initialisation avec un ratio d'amélioration trop élevé."""
        with pytest.raises(ValueError, match="Ratio d'amélioration invalide"):
            BalancingResult(
                original_automaton=self.test_automaton,
                balanced_automaton=self.test_automaton,
                metrics_before=self.mock_metrics,
                metrics_after=self.mock_metrics,
                improvement_ratio=1.5,
                execution_time=1.5,
                memory_usage=1024,
                strategy_name="TestStrategy"
            )
    
    def test_init_invalid_execution_time(self):
        """Test l'initialisation avec un temps d'exécution négatif."""
        with pytest.raises(ValueError, match="Temps d'exécution invalide"):
            BalancingResult(
                original_automaton=self.test_automaton,
                balanced_automaton=self.test_automaton,
                metrics_before=self.mock_metrics,
                metrics_after=self.mock_metrics,
                improvement_ratio=0.2,
                execution_time=-1.0,
                memory_usage=1024,
                strategy_name="TestStrategy"
            )
    
    def test_init_invalid_memory_usage(self):
        """Test l'initialisation avec une utilisation mémoire négative."""
        with pytest.raises(ValueError, match="Utilisation mémoire invalide"):
            BalancingResult(
                original_automaton=self.test_automaton,
                balanced_automaton=self.test_automaton,
                metrics_before=self.mock_metrics,
                metrics_after=self.mock_metrics,
                improvement_ratio=0.2,
                execution_time=1.5,
                memory_usage=-100,
                strategy_name="TestStrategy"
            )
    
    def test_is_improvement_true(self):
        """Test la vérification d'amélioration avec amélioration."""
        result = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=0.2,
            execution_time=1.5,
            memory_usage=1024,
            strategy_name="TestStrategy"
        )
        
        assert result.is_improvement is True
    
    def test_is_improvement_false(self):
        """Test la vérification d'amélioration sans amélioration."""
        result = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=0.0,
            execution_time=1.5,
            memory_usage=1024,
            strategy_name="TestStrategy"
        )
        
        assert result.is_improvement is False
    
    def test_performance_gain(self):
        """Test le calcul du gain de performance."""
        result = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=0.25,
            execution_time=1.5,
            memory_usage=1024,
            strategy_name="TestStrategy"
        )
        
        assert result.performance_gain == 25.0
    
    def test_performance_gain_zero(self):
        """Test le calcul du gain de performance avec ratio = 0."""
        result = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=0.0,
            execution_time=1.5,
            memory_usage=1024,
            strategy_name="TestStrategy"
        )
        
        assert result.performance_gain == 0.0
    
    def test_performance_gain_maximum(self):
        """Test le calcul du gain de performance avec ratio = 1."""
        result = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=1.0,
            execution_time=1.5,
            memory_usage=1024,
            strategy_name="TestStrategy"
        )
        
        assert result.performance_gain == 100.0
    
    def test_to_dict(self):
        """Test la sérialisation en dictionnaire."""
        result = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=0.3,
            execution_time=2.5,
            memory_usage=2048,
            strategy_name="TestStrategy"
        )
        
        # Mock des méthodes to_dict des métriques
        self.mock_metrics.to_dict.return_value = {"balance_score": 0.8}
        
        # Mock des méthodes to_dict des automates
        with pytest.Mock() as mock_automaton_dict:
            mock_automaton_dict.to_dict.return_value = {"states": ["q0", "q1"]}
            
            # Remplacement temporaire des méthodes to_dict
            original_to_dict = self.test_automaton.to_dict
            self.test_automaton.to_dict = mock_automaton_dict.to_dict
            
            try:
                result_dict = result.to_dict()
                
                assert "original_automaton" in result_dict
                assert "balanced_automaton" in result_dict
                assert "metrics_before" in result_dict
                assert "metrics_after" in result_dict
                assert result_dict["improvement_ratio"] == 0.3
                assert result_dict["execution_time"] == 2.5
                assert result_dict["memory_usage"] == 2048
                assert result_dict["strategy_name"] == "TestStrategy"
                assert result_dict["is_improvement"] is True
                assert result_dict["performance_gain"] == 30.0
                
            finally:
                # Restauration de la méthode originale
                self.test_automaton.to_dict = original_to_dict
    
    def test_frozen_dataclass(self):
        """Test que BalancingResult est immutable."""
        result = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=0.2,
            execution_time=1.5,
            memory_usage=1024,
            strategy_name="TestStrategy"
        )
        
        # Vérification que l'objet est immutable
        with pytest.raises(AttributeError):
            result.improvement_ratio = 0.5
        
        with pytest.raises(AttributeError):
            result.execution_time = 3.0
        
        with pytest.raises(AttributeError):
            result.strategy_name = "NewStrategy"
    
    def test_edge_cases(self):
        """Test des cas limites."""
        # Ratio d'amélioration = 0
        result_zero = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=0.0,
            execution_time=0.0,
            memory_usage=0,
            strategy_name="TestStrategy"
        )
        
        assert result_zero.is_improvement is False
        assert result_zero.performance_gain == 0.0
        
        # Ratio d'amélioration = 1
        result_max = BalancingResult(
            original_automaton=self.test_automaton,
            balanced_automaton=self.test_automaton,
            metrics_before=self.mock_metrics,
            metrics_after=self.mock_metrics,
            improvement_ratio=1.0,
            execution_time=0.001,
            memory_usage=1,
            strategy_name="TestStrategy"
        )
        
        assert result_max.is_improvement is True
        assert result_max.performance_gain == 100.0