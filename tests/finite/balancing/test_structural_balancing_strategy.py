"""
Tests unitaires pour StructuralBalancingStrategy.

Ce module teste la stratégie de balancing structurel des automates finis.
"""

import pytest
from unittest.mock import Mock, patch

from src.baobab_automata.finite.balancing.balancing_exceptions import (
    BalancingError,
    BalancingTimeoutError,
)
from src.baobab_automata.finite.balancing.balancing_metrics import BalancingMetrics
from src.baobab_automata.finite.balancing.balancing_result import BalancingResult
from src.baobab_automata.finite.balancing.structural_balancing_strategy import (
    StructuralBalancingStrategy,
)
from src.baobab_automata.finite.dfa import DFA
from src.baobab_automata.finite.epsilon_nfa import EpsilonNFA
from src.baobab_automata.finite.nfa import NFA


class TestStructuralBalancingStrategy:
    """Tests unitaires pour StructuralBalancingStrategy."""
    
    def setup_method(self):
        """Configure les tests."""
        self.strategy = StructuralBalancingStrategy()
        
        self.test_dfa = DFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                "q0": {"a": "q1", "b": "q0"},
                "q1": {"a": "q2", "b": "q1"},
                "q2": {"a": "q2", "b": "q0"}
            },
            initial_state="q0",
            final_states={"q2"}
        )
        
        self.test_nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a", "b"},
            transitions={
                "q0": {"a": {"q1"}, "b": {"q0"}},
                "q1": {"a": {"q1"}, "b": {"q0"}}
            },
            initial_state="q0",
            final_states={"q1"}
        )
        
        self.test_epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                "q0": {"a": {"q1"}, "ε": {"q2"}},
                "q1": {"b": {"q2"}},
                "q2": {"a": {"q2"}}
            },
            initial_state="q0",
            final_states={"q2"}
        )
    
    def test_init_valid_parameters(self):
        """Test l'initialisation avec des paramètres valides."""
        strategy = StructuralBalancingStrategy(
            max_iterations=50,
            timeout_seconds=15.0,
            balance_threshold=0.7
        )
        
        assert strategy._max_iterations == 50
        assert strategy._timeout_seconds == 15.0
        assert strategy._balance_threshold == 0.7
    
    def test_init_invalid_max_iterations(self):
        """Test l'initialisation avec un nombre d'itérations invalide."""
        with pytest.raises(BalancingError, match="Nombre d'itérations invalide"):
            StructuralBalancingStrategy(max_iterations=0)
    
    def test_init_invalid_timeout(self):
        """Test l'initialisation avec un timeout invalide."""
        with pytest.raises(BalancingError, match="Timeout invalide"):
            StructuralBalancingStrategy(timeout_seconds=0.0)
    
    def test_init_invalid_balance_threshold(self):
        """Test l'initialisation avec un seuil d'équilibrage invalide."""
        with pytest.raises(BalancingError, match="Seuil d'équilibrage invalide"):
            StructuralBalancingStrategy(balance_threshold=1.5)
    
    def test_name(self):
        """Test le nom de la stratégie."""
        assert self.strategy.name == "StructuralBalancing"
    
    def test_description(self):
        """Test la description de la stratégie."""
        description = self.strategy.description
        assert isinstance(description, str)
        assert len(description) > 0
        assert "structure" in description.lower()
    
    def test_can_balance_dfa(self):
        """Test la capacité de balancing pour un DFA."""
        assert self.strategy.can_balance(self.test_dfa) is True
    
    def test_can_balance_nfa(self):
        """Test la capacité de balancing pour un NFA."""
        assert self.strategy.can_balance(self.test_nfa) is True
    
    def test_can_balance_epsilon_nfa(self):
        """Test la capacité de balancing pour un ε-NFA."""
        assert self.strategy.can_balance(self.test_epsilon_nfa) is True
    
    def test_can_balance_invalid_automaton(self):
        """Test la capacité de balancing pour un automate invalide."""
        invalid_automaton = Mock()
        invalid_automaton.validate.return_value = False
        
        assert self.strategy.can_balance(invalid_automaton) is False
    
    def test_can_balance_single_state(self):
        """Test la capacité de balancing pour un automate à un état."""
        single_state_dfa = DFA(
            states={"q0"},
            alphabet={"a"},
            transitions={"q0": {"a": "q0"}},
            initial_state="q0",
            final_states={"q0"}
        )
        
        assert self.strategy.can_balance(single_state_dfa) is False
    
    def test_get_metrics(self):
        """Test le calcul des métriques."""
        with patch('src.baobab_automata.finite.balancing.structural_balancing_strategy.BalancingMetrics') as mock_metrics_class:
            mock_metrics = Mock(spec=BalancingMetrics)
            mock_metrics_class.from_automaton.return_value = mock_metrics
            
            result = self.strategy.get_metrics(self.test_dfa)
            
            assert result == mock_metrics
            mock_metrics_class.from_automaton.assert_called_once_with(self.test_dfa)
    
    def test_is_balanced_true(self):
        """Test la vérification d'équilibrage pour un automate équilibré."""
        with patch('src.baobab_automata.finite.balancing.structural_balancing_strategy.BalancingMetrics') as mock_metrics_class:
            mock_metrics = Mock(spec=BalancingMetrics)
            mock_metrics.is_well_balanced = True
            mock_metrics.balance_score = 0.9
            mock_metrics_class.from_automaton.return_value = mock_metrics
            
            result = self.strategy.is_balanced(self.test_dfa)
            
            assert result is True
    
    def test_is_balanced_false(self):
        """Test la vérification d'équilibrage pour un automate déséquilibré."""
        with patch('src.baobab_automata.finite.balancing.structural_balancing_strategy.BalancingMetrics') as mock_metrics_class:
            mock_metrics = Mock(spec=BalancingMetrics)
            mock_metrics.is_well_balanced = False
            mock_metrics.balance_score = 0.5
            mock_metrics_class.from_automaton.return_value = mock_metrics
            
            result = self.strategy.is_balanced(self.test_dfa)
            
            assert result is False
    
    def test_balance_already_balanced(self):
        """Test le balancing d'un automate déjà équilibré."""
        with patch('src.baobab_automata.finite.balancing.structural_balancing_strategy.BalancingMetrics') as mock_metrics_class:
            mock_metrics = Mock(spec=BalancingMetrics)
            mock_metrics.is_well_balanced = True
            mock_metrics_class.from_automaton.return_value = mock_metrics
            
            result = self.strategy.balance(self.test_dfa)
            
            assert isinstance(result, BalancingResult)
            assert result.original_automaton == self.test_dfa
            assert result.balanced_automaton == self.test_dfa
            assert result.improvement_ratio == 0.0
            assert result.strategy_name == "StructuralBalancing"
    
    def test_balance_with_improvement(self):
        """Test le balancing avec amélioration."""
        with patch('src.baobab_automata.finite.balancing.structural_balancing_strategy.BalancingMetrics') as mock_metrics_class:
            # Métriques avant (déséquilibré)
            mock_metrics_before = Mock(spec=BalancingMetrics)
            mock_metrics_before.is_well_balanced = False
            mock_metrics_before.balance_score = 0.5
            
            # Métriques après (équilibré)
            mock_metrics_after = Mock(spec=BalancingMetrics)
            mock_metrics_after.is_well_balanced = True
            mock_metrics_after.balance_score = 0.8
            
            mock_metrics_class.from_automaton.side_effect = [mock_metrics_before, mock_metrics_after]
            
            # Mock de l'automate équilibré
            with patch.object(self.strategy, '_apply_structural_balancing', return_value=self.test_dfa):
                result = self.strategy.balance(self.test_dfa)
                
                assert isinstance(result, BalancingResult)
                assert result.original_automaton == self.test_dfa
                assert result.balanced_automaton == self.test_dfa
                assert result.strategy_name == "StructuralBalancing"
    
    def test_balance_strategy_error(self):
        """Test le balancing avec une erreur de stratégie."""
        with patch('src.baobab_automata.finite.balancing.structural_balancing_strategy.BalancingMetrics') as mock_metrics_class:
            mock_metrics = Mock(spec=BalancingMetrics)
            mock_metrics.is_well_balanced = False
            mock_metrics_class.from_automaton.return_value = mock_metrics
            
            with patch.object(self.strategy, '_apply_structural_balancing', side_effect=Exception("Strategy error")):
                with pytest.raises(BalancingError, match="Erreur lors du balancing structurel"):
                    self.strategy.balance(self.test_dfa)
    
    def test_balance_timeout_error(self):
        """Test le balancing avec timeout."""
        with patch('src.baobab_automata.finite.balancing.structural_balancing_strategy.BalancingMetrics') as mock_metrics_class:
            mock_metrics = Mock(spec=BalancingMetrics)
            mock_metrics.is_well_balanced = False
            mock_metrics_class.from_automaton.return_value = mock_metrics
            
            # Mock du timeout
            with patch('src.baobab_automata.finite.balancing.structural_balancing_strategy.time.time') as mock_time:
                mock_time.side_effect = [0, 0, 100]  # Timeout après 100 secondes
                
                with patch.object(self.strategy, '_apply_structural_balancing', side_effect=Exception("Timeout")):
                    with pytest.raises(BalancingTimeoutError):
                        self.strategy.balance(self.test_dfa)
    
    def test_analyze_transitions_per_state(self):
        """Test l'analyse des transitions par état."""
        result = self.strategy._analyze_transitions_per_state(self.test_dfa)
        
        assert isinstance(result, dict)
        assert "q0" in result
        assert "q1" in result
        assert "q2" in result
        assert result["q0"] == 2  # a->q1, b->q0
        assert result["q1"] == 2  # a->q2, b->q1
        assert result["q2"] == 2  # a->q2, b->q0
    
    def test_identify_unbalanced_states(self):
        """Test l'identification des états déséquilibrés."""
        transitions_per_state = {
            "q0": 1,  # Peu de transitions
            "q1": 2,  # Moyen
            "q2": 5   # Beaucoup de transitions
        }
        
        unbalanced_states = self.strategy._identify_unbalanced_states(transitions_per_state)
        
        assert "q0" in unbalanced_states  # Trop peu
        assert "q2" in unbalanced_states  # Trop beaucoup
        assert "q1" not in unbalanced_states  # Équilibré
    
    def test_identify_unbalanced_states_empty(self):
        """Test l'identification des états déséquilibrés avec dictionnaire vide."""
        unbalanced_states = self.strategy._identify_unbalanced_states({})
        
        assert unbalanced_states == []
    
    def test_calculate_improvement_ratio(self):
        """Test le calcul du ratio d'amélioration."""
        metrics_before = Mock(spec=BalancingMetrics)
        metrics_before.balance_score = 0.5
        
        metrics_after = Mock(spec=BalancingMetrics)
        metrics_after.balance_score = 0.8
        
        ratio = self.strategy._calculate_improvement_ratio(metrics_before, metrics_after)
        
        expected_ratio = (0.8 - 0.5) / 0.5  # 0.6
        assert ratio == expected_ratio
    
    def test_calculate_improvement_ratio_zero_before(self):
        """Test le calcul du ratio d'amélioration avec score avant = 0."""
        metrics_before = Mock(spec=BalancingMetrics)
        metrics_before.balance_score = 0.0
        
        metrics_after = Mock(spec=BalancingMetrics)
        metrics_after.balance_score = 0.8
        
        ratio = self.strategy._calculate_improvement_ratio(metrics_before, metrics_after)
        
        assert ratio == 0.0
    
    def test_calculate_improvement_ratio_negative(self):
        """Test le calcul du ratio d'amélioration négatif."""
        metrics_before = Mock(spec=BalancingMetrics)
        metrics_before.balance_score = 0.8
        
        metrics_after = Mock(spec=BalancingMetrics)
        metrics_after.balance_score = 0.5
        
        ratio = self.strategy._calculate_improvement_ratio(metrics_before, metrics_after)
        
        assert ratio == 0.0  # Clampé à 0
    
    def test_calculate_improvement_ratio_excessive(self):
        """Test le calcul du ratio d'amélioration excessif."""
        metrics_before = Mock(spec=BalancingMetrics)
        metrics_before.balance_score = 0.1
        
        metrics_after = Mock(spec=BalancingMetrics)
        metrics_after.balance_score = 0.5
        
        ratio = self.strategy._calculate_improvement_ratio(metrics_before, metrics_after)
        
        assert ratio == 1.0  # Clampé à 1
    
    def test_get_memory_usage(self):
        """Test l'obtention de l'utilisation mémoire."""
        usage = self.strategy._get_memory_usage()
        
        assert isinstance(usage, int)
        assert usage >= 0
    
    def test_apply_structural_balancing(self):
        """Test l'application du balancing structurel."""
        with patch.object(self.strategy, '_optimize_state_distribution', return_value=self.test_dfa):
            with patch.object(self.strategy, '_optimize_transition_distribution', return_value=self.test_dfa):
                with patch.object(self.strategy, '_reorganize_states', return_value=self.test_dfa):
                    result = self.strategy._apply_structural_balancing(self.test_dfa)
                    
                    assert result == self.test_dfa
    
    def test_optimize_state_distribution(self):
        """Test l'optimisation de la distribution des états."""
        with patch.object(self.strategy, '_analyze_transitions_per_state', return_value={"q0": 1, "q1": 3}):
            with patch.object(self.strategy, '_identify_unbalanced_states', return_value=["q1"]):
                with patch.object(self.strategy, '_rebalance_states', return_value=self.test_dfa):
                    result = self.strategy._optimize_state_distribution(self.test_dfa)
                    
                    assert result == self.test_dfa
    
    def test_optimize_transition_distribution(self):
        """Test l'optimisation de la distribution des transitions."""
        with patch.object(self.strategy, '_find_redundant_transitions', return_value=[]):
            with patch.object(self.strategy, '_merge_redundant_transitions', return_value=self.test_dfa):
                result = self.strategy._optimize_transition_distribution(self.test_dfa)
                
                assert result == self.test_dfa
    
    def test_reorganize_states(self):
        """Test la réorganisation des états."""
        with patch.object(self.strategy, '_analyze_state_frequency', return_value={"q0": 0.5, "q1": 0.5}):
            with patch.object(self.strategy, '_reorganize_by_frequency', return_value=self.test_dfa):
                result = self.strategy._reorganize_states(self.test_dfa)
                
                assert result == self.test_dfa