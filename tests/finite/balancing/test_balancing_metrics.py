"""
Tests unitaires pour BalancingMetrics.

Ce module teste les métriques de balancing des automates finis.
"""

import pytest

from src.baobab_automata.finite.balancing.balancing_metrics import BalancingMetrics
from src.baobab_automata.finite.dfa import DFA


class TestBalancingMetrics:
    """Tests unitaires pour BalancingMetrics."""
    
    def setup_method(self):
        """Configure les tests."""
        self.test_automaton = DFA(
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
    
    def test_init_valid_parameters(self):
        """Test l'initialisation avec des paramètres valides."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=6,
            average_transitions_per_state=2.0,
            max_transitions_per_state=2,
            min_transitions_per_state=2,
            transition_variance=0.0,
            balance_score=1.0
        )
        
        assert metrics.state_count == 3
        assert metrics.transition_count == 6
        assert metrics.average_transitions_per_state == 2.0
        assert metrics.max_transitions_per_state == 2
        assert metrics.min_transitions_per_state == 2
        assert metrics.transition_variance == 0.0
        assert metrics.balance_score == 1.0
    
    def test_init_invalid_state_count(self):
        """Test l'initialisation avec un nombre d'états invalide."""
        with pytest.raises(ValueError, match="Nombre d'états invalide"):
            BalancingMetrics(
                state_count=-1,
                transition_count=6,
                average_transitions_per_state=2.0,
                max_transitions_per_state=2,
                min_transitions_per_state=2,
                transition_variance=0.0,
                balance_score=1.0
            )
    
    def test_init_invalid_transition_count(self):
        """Test l'initialisation avec un nombre de transitions invalide."""
        with pytest.raises(ValueError, match="Nombre de transitions invalide"):
            BalancingMetrics(
                state_count=3,
                transition_count=-1,
                average_transitions_per_state=2.0,
                max_transitions_per_state=2,
                min_transitions_per_state=2,
                transition_variance=0.0,
                balance_score=1.0
            )
    
    def test_init_invalid_max_min_transitions(self):
        """Test l'initialisation avec max < min transitions."""
        with pytest.raises(ValueError, match="Max transitions.*<.*Min transitions"):
            BalancingMetrics(
                state_count=3,
                transition_count=6,
                average_transitions_per_state=2.0,
                max_transitions_per_state=1,
                min_transitions_per_state=2,
                transition_variance=0.0,
                balance_score=1.0
            )
    
    def test_init_invalid_balance_score(self):
        """Test l'initialisation avec un score d'équilibrage invalide."""
        with pytest.raises(ValueError, match="Score d'équilibrage invalide"):
            BalancingMetrics(
                state_count=3,
                transition_count=6,
                average_transitions_per_state=2.0,
                max_transitions_per_state=2,
                min_transitions_per_state=2,
                transition_variance=0.0,
                balance_score=1.5
            )
    
    def test_transition_balance_ratio_perfect_balance(self):
        """Test le ratio d'équilibrage des transitions parfait."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=6,
            average_transitions_per_state=2.0,
            max_transitions_per_state=2,
            min_transitions_per_state=2,
            transition_variance=0.0,
            balance_score=1.0
        )
        
        assert metrics.transition_balance_ratio == 1.0
    
    def test_transition_balance_ratio_unbalanced(self):
        """Test le ratio d'équilibrage des transitions déséquilibré."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=6,
            average_transitions_per_state=2.0,
            max_transitions_per_state=4,
            min_transitions_per_state=1,
            transition_variance=1.0,
            balance_score=0.5
        )
        
        assert metrics.transition_balance_ratio == 0.25  # 1/4
    
    def test_transition_balance_ratio_zero_max(self):
        """Test le ratio d'équilibrage avec max transitions = 0."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=0,
            average_transitions_per_state=0.0,
            max_transitions_per_state=0,
            min_transitions_per_state=0,
            transition_variance=0.0,
            balance_score=1.0
        )
        
        assert metrics.transition_balance_ratio == 1.0
    
    def test_state_utilization_empty_frequency(self):
        """Test l'utilisation des états avec fréquence vide."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=6,
            average_transitions_per_state=2.0,
            max_transitions_per_state=2,
            min_transitions_per_state=2,
            transition_variance=0.0,
            balance_score=1.0,
            state_access_frequency={}
        )
        
        assert metrics.state_utilization == 0.0
    
    def test_state_utilization_equal_frequency(self):
        """Test l'utilisation des états avec fréquences égales."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=6,
            average_transitions_per_state=2.0,
            max_transitions_per_state=2,
            min_transitions_per_state=2,
            transition_variance=0.0,
            balance_score=1.0,
            state_access_frequency={"q0": 0.33, "q1": 0.33, "q2": 0.34}
        )
        
        # Avec des fréquences égales, l'utilisation doit être élevée
        assert metrics.state_utilization > 0.8
    
    def test_state_utilization_zero_total_frequency(self):
        """Test l'utilisation des états avec fréquence totale = 0."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=6,
            average_transitions_per_state=2.0,
            max_transitions_per_state=2,
            min_transitions_per_state=2,
            transition_variance=0.0,
            balance_score=1.0,
            state_access_frequency={"q0": 0.0, "q1": 0.0, "q2": 0.0}
        )
        
        assert metrics.state_utilization == 0.0
    
    def test_is_well_balanced_true(self):
        """Test la vérification d'équilibrage bien équilibré."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=6,
            average_transitions_per_state=2.0,
            max_transitions_per_state=2,
            min_transitions_per_state=2,
            transition_variance=0.0,
            balance_score=0.8,
            state_access_frequency={"q0": 0.33, "q1": 0.33, "q2": 0.34}
        )
        
        assert metrics.is_well_balanced is True
    
    def test_is_well_balanced_false(self):
        """Test la vérification d'équilibrage mal équilibré."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=6,
            average_transitions_per_state=2.0,
            max_transitions_per_state=4,
            min_transitions_per_state=1,
            transition_variance=1.0,
            balance_score=0.5,
            state_access_frequency={"q0": 0.1, "q1": 0.1, "q2": 0.8}
        )
        
        assert metrics.is_well_balanced is False
    
    def test_complexity_score_simple(self):
        """Test le score de complexité pour un automate simple."""
        metrics = BalancingMetrics(
            state_count=2,
            transition_count=4,
            average_transitions_per_state=2.0,
            max_transitions_per_state=2,
            min_transitions_per_state=2,
            transition_variance=0.0,
            balance_score=1.0
        )
        
        assert metrics.complexity_score < 0.5  # Simple
    
    def test_complexity_score_complex(self):
        """Test le score de complexité pour un automate complexe."""
        metrics = BalancingMetrics(
            state_count=100,
            transition_count=500,
            average_transitions_per_state=5.0,
            max_transitions_per_state=10,
            min_transitions_per_state=1,
            transition_variance=10.0,
            balance_score=0.3
        )
        
        assert metrics.complexity_score > 0.5  # Complexe
    
    def test_to_dict(self):
        """Test la sérialisation en dictionnaire."""
        metrics = BalancingMetrics(
            state_count=3,
            transition_count=6,
            average_transitions_per_state=2.0,
            max_transitions_per_state=2,
            min_transitions_per_state=2,
            transition_variance=0.0,
            balance_score=1.0,
            state_access_frequency={"q0": 0.33, "q1": 0.33, "q2": 0.34},
            transition_usage_frequency={"q0:a": 0.5, "q1:b": 0.5},
            memory_usage=1024,
            recognition_complexity=0.3
        )
        
        result = metrics.to_dict()
        
        assert result["state_count"] == 3
        assert result["transition_count"] == 6
        assert result["average_transitions_per_state"] == 2.0
        assert result["max_transitions_per_state"] == 2
        assert result["min_transitions_per_state"] == 2
        assert result["transition_variance"] == 0.0
        assert result["balance_score"] == 1.0
        assert result["state_access_frequency"] == {"q0": 0.33, "q1": 0.33, "q2": 0.34}
        assert result["transition_usage_frequency"] == {"q0:a": 0.5, "q1:b": 0.5}
        assert result["memory_usage"] == 1024
        assert result["recognition_complexity"] == 0.3
        assert "transition_balance_ratio" in result
        assert "state_utilization" in result
        assert "is_well_balanced" in result
        assert "complexity_score" in result
    
    def test_from_automaton_empty_automaton(self):
        """Test le calcul des métriques pour un automate vide."""
        empty_automaton = DFA(
            states=set(),
            alphabet=set(),
            transitions={},
            initial_state="",
            final_states=set()
        )
        
        metrics = BalancingMetrics.from_automaton(empty_automaton)
        
        assert metrics.state_count == 0
        assert metrics.transition_count == 0
        assert metrics.average_transitions_per_state == 0.0
        assert metrics.max_transitions_per_state == 0
        assert metrics.min_transitions_per_state == 0
        assert metrics.transition_variance == 0.0
        assert metrics.balance_score == 1.0
    
    def test_from_automaton_single_state(self):
        """Test le calcul des métriques pour un automate à un état."""
        single_state_automaton = DFA(
            states={"q0"},
            alphabet={"a"},
            transitions={"q0": {"a": "q0"}},
            initial_state="q0",
            final_states={"q0"}
        )
        
        metrics = BalancingMetrics.from_automaton(single_state_automaton)
        
        assert metrics.state_count == 1
        assert metrics.transition_count == 1
        assert metrics.average_transitions_per_state == 1.0
        assert metrics.max_transitions_per_state == 1
        assert metrics.min_transitions_per_state == 1
        assert metrics.transition_variance == 0.0
        assert metrics.balance_score == 1.0
    
    def test_from_automaton_multiple_states(self):
        """Test le calcul des métriques pour un automate à plusieurs états."""
        metrics = BalancingMetrics.from_automaton(self.test_automaton)
        
        assert metrics.state_count == 3
        assert metrics.transition_count == 6
        assert metrics.average_transitions_per_state == 2.0
        assert metrics.max_transitions_per_state == 2
        assert metrics.min_transitions_per_state == 2
        assert metrics.transition_variance == 0.0
        assert metrics.balance_score == 1.0
    
    def test_from_automaton_unbalanced(self):
        """Test le calcul des métriques pour un automate déséquilibré."""
        unbalanced_automaton = DFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                "q0": {"a": "q1"},  # 1 transition
                "q1": {"a": "q2", "b": "q1"},  # 2 transitions
                "q2": {"a": "q2", "b": "q0", "c": "q1"}  # 3 transitions
            },
            initial_state="q0",
            final_states={"q2"}
        )
        
        metrics = BalancingMetrics.from_automaton(unbalanced_automaton)
        
        assert metrics.state_count == 3
        assert metrics.transition_count == 6
        assert metrics.max_transitions_per_state == 3
        assert metrics.min_transitions_per_state == 1
        assert metrics.transition_variance > 0.0
        assert metrics.balance_score < 1.0
    
    def test_calculate_balance_score_perfect(self):
        """Test le calcul du score d'équilibrage parfait."""
        score = BalancingMetrics._calculate_balance_score(2.0, 2, 2, 0.0)
        assert score == 1.0
    
    def test_calculate_balance_score_unbalanced(self):
        """Test le calcul du score d'équilibrage déséquilibré."""
        score = BalancingMetrics._calculate_balance_score(2.0, 4, 1, 1.0)
        assert score < 1.0
        assert score > 0.0
    
    def test_calculate_balance_score_zero_max(self):
        """Test le calcul du score d'équilibrage avec max = 0."""
        score = BalancingMetrics._calculate_balance_score(0.0, 0, 0, 0.0)
        assert score == 1.0