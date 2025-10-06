"""Tests unitaires pour la classe OperationStats."""

import pytest
import time
from baobab_automata.automata.finite.operation_stats import OperationStats


@pytest.mark.unit
class TestOperationStats:
    """Tests pour la classe OperationStats."""

    def test_initialization(self):
        """Test l'initialisation des statistiques."""
        stats = OperationStats()
        assert len(stats._operations) == 0
        assert stats._start_time is None

    def test_add_operation(self):
        """Test l'ajout d'une opération."""
        stats = OperationStats()
        stats.add_operation("union", 0.5, 10, 20, 1024)
        
        assert len(stats._operations) == 1
        op = stats._operations[0]
        assert op["operation"] == "union"
        assert op["time"] == 0.5
        assert op["states"] == 10
        assert op["transitions"] == 20
        assert op["memory"] == 1024
        assert "timestamp" in op

    def test_add_operation_without_memory(self):
        """Test l'ajout d'une opération sans mémoire."""
        stats = OperationStats()
        stats.add_operation("intersection", 0.3, 5, 15)
        
        assert len(stats._operations) == 1
        op = stats._operations[0]
        assert op["memory"] == 0

    def test_start_timing(self):
        """Test le démarrage du chronométrage."""
        stats = OperationStats()
        stats.start_timing()
        
        assert stats._start_time is not None
        assert isinstance(stats._start_time, float)

    def test_stop_timing(self):
        """Test l'arrêt du chronométrage."""
        stats = OperationStats()
        stats.start_timing()
        
        # Attendre un peu pour avoir un temps > 0
        time.sleep(0.01)
        
        stats.stop_timing("union", 10, 20, 1024)
        
        assert len(stats._operations) == 1
        op = stats._operations[0]
        assert op["operation"] == "union"
        assert op["time"] > 0
        assert op["states"] == 10
        assert op["transitions"] == 20
        assert op["memory"] == 1024
        assert stats._start_time is None

    def test_stop_timing_without_start(self):
        """Test l'arrêt du chronométrage sans démarrage."""
        stats = OperationStats()
        
        with pytest.raises(ValueError, match="start_timing\\(\\) must be called before stop_timing\\(\\)"):
            stats.stop_timing("union", 10, 20)

    def test_get_stats_empty(self):
        """Test les statistiques avec aucune opération."""
        stats = OperationStats()
        result = stats.get_stats()
        
        expected = {
            "total_operations": 0,
            "average_time": 0.0,
            "total_time": 0.0,
            "average_states": 0.0,
            "average_transitions": 0.0,
            "operations_by_type": {},
        }
        assert result == expected

    def test_get_stats_single_operation(self):
        """Test les statistiques avec une seule opération."""
        stats = OperationStats()
        stats.add_operation("union", 0.5, 10, 20, 1024)
        
        result = stats.get_stats()
        
        assert result["total_operations"] == 1
        assert result["average_time"] == 0.5
        assert result["total_time"] == 0.5
        assert result["average_states"] == 10.0
        assert result["average_transitions"] == 20.0
        assert "union" in result["operations_by_type"]
        
        union_stats = result["operations_by_type"]["union"]
        assert union_stats["count"] == 1
        assert union_stats["total_time"] == 0.5
        assert union_stats["average_time"] == 0.5
        assert union_stats["total_states"] == 10
        assert union_stats["average_states"] == 10.0
        assert union_stats["total_transitions"] == 20
        assert union_stats["average_transitions"] == 20.0

    def test_get_stats_multiple_operations(self):
        """Test les statistiques avec plusieurs opérations."""
        stats = OperationStats()
        stats.add_operation("union", 0.5, 10, 20)
        stats.add_operation("intersection", 0.3, 5, 15)
        stats.add_operation("union", 0.7, 15, 25)
        
        result = stats.get_stats()
        
        assert result["total_operations"] == 3
        assert result["average_time"] == 0.5  # (0.5 + 0.3 + 0.7) / 3
        assert result["total_time"] == 1.5
        assert result["average_states"] == 10.0  # (10 + 5 + 15) / 3
        assert result["average_transitions"] == 20.0  # (20 + 15 + 25) / 3
        
        # Vérifier les statistiques par type
        assert "union" in result["operations_by_type"]
        assert "intersection" in result["operations_by_type"]
        
        union_stats = result["operations_by_type"]["union"]
        assert union_stats["count"] == 2
        assert union_stats["total_time"] == 1.2
        assert union_stats["average_time"] == 0.6
        
        intersection_stats = result["operations_by_type"]["intersection"]
        assert intersection_stats["count"] == 1
        assert intersection_stats["total_time"] == 0.3
        assert intersection_stats["average_time"] == 0.3

    def test_get_operation_history(self):
        """Test la récupération de l'historique des opérations."""
        stats = OperationStats()
        stats.add_operation("union", 0.5, 10, 20)
        stats.add_operation("intersection", 0.3, 5, 15)
        
        history = stats.get_operation_history()
        
        assert len(history) == 2
        assert history[0]["operation"] == "union"
        assert history[1]["operation"] == "intersection"
        
        # Vérifier que c'est une copie
        history.append({"test": "data"})
        assert len(stats.get_operation_history()) == 2

    def test_get_operations_by_type(self):
        """Test la récupération des opérations par type."""
        stats = OperationStats()
        stats.add_operation("union", 0.5, 10, 20)
        stats.add_operation("intersection", 0.3, 5, 15)
        stats.add_operation("union", 0.7, 15, 25)
        
        union_ops = stats.get_operations_by_type("union")
        intersection_ops = stats.get_operations_by_type("intersection")
        empty_ops = stats.get_operations_by_type("nonexistent")
        
        assert len(union_ops) == 2
        assert len(intersection_ops) == 1
        assert len(empty_ops) == 0
        
        assert union_ops[0]["operation"] == "union"
        assert union_ops[1]["operation"] == "union"
        assert intersection_ops[0]["operation"] == "intersection"

    def test_reset(self):
        """Test la remise à zéro des statistiques."""
        stats = OperationStats()
        stats.add_operation("union", 0.5, 10, 20)
        stats.start_timing()
        
        stats.reset()
        
        assert len(stats._operations) == 0
        assert stats._start_time is None

    def test_export_to_dict(self):
        """Test l'export vers un dictionnaire."""
        stats = OperationStats()
        stats.add_operation("union", 0.5, 10, 20, 1024)
        
        exported = stats.export_to_dict()
        
        assert "stats" in exported
        assert "history" in exported
        assert len(exported["history"]) == 1
        assert exported["stats"]["total_operations"] == 1

    def test_import_from_dict(self):
        """Test l'import depuis un dictionnaire."""
        stats = OperationStats()
        
        data = {
            "history": [
                {
                    "operation": "union",
                    "time": 0.5,
                    "states": 10,
                    "transitions": 20,
                    "memory": 1024,
                    "timestamp": time.time()
                }
            ]
        }
        
        stats.import_from_dict(data)
        
        assert len(stats._operations) == 1
        op = stats._operations[0]
        assert op["operation"] == "union"
        assert op["time"] == 0.5
        assert op["states"] == 10
        assert op["transitions"] == 20
        assert op["memory"] == 1024

    def test_import_from_dict_invalid_format(self):
        """Test l'import avec un format invalide."""
        stats = OperationStats()
        
        # Données sans clé 'history'
        with pytest.raises(ValueError, match="Invalid data format: missing 'history' key"):
            stats.import_from_dict({"invalid": "data"})
        
        # Données avec opération incomplète
        with pytest.raises(ValueError, match="Invalid operation data: missing required keys"):
            stats.import_from_dict({
                "history": [{"operation": "union"}]  # Manque time, states, transitions
            })

    def test_import_from_dict_with_missing_memory(self):
        """Test l'import avec mémoire manquante (utilise 0 par défaut)."""
        stats = OperationStats()
        
        data = {
            "history": [
                {
                    "operation": "union",
                    "time": 0.5,
                    "states": 10,
                    "transitions": 20,
                    "timestamp": time.time()
                    # Pas de clé 'memory'
                }
            ]
        }
        
        stats.import_from_dict(data)
        
        assert len(stats._operations) == 1
        op = stats._operations[0]
        assert op["memory"] == 0

    def test_timing_accuracy(self):
        """Test la précision du chronométrage."""
        stats = OperationStats()
        
        # Test avec un délai connu
        stats.start_timing()
        time.sleep(0.1)  # 100ms
        stats.stop_timing("test", 1, 1)
        
        op = stats._operations[0]
        assert 0.09 <= op["time"] <= 0.11  # Tolérance de 10ms

    def test_multiple_timing_sessions(self):
        """Test plusieurs sessions de chronométrage."""
        stats = OperationStats()
        
        # Première session
        stats.start_timing()
        time.sleep(0.01)
        stats.stop_timing("op1", 1, 1)
        
        # Deuxième session
        stats.start_timing()
        time.sleep(0.01)
        stats.stop_timing("op2", 2, 2)
        
        assert len(stats._operations) == 2
        assert stats._operations[0]["operation"] == "op1"
        assert stats._operations[1]["operation"] == "op2"
        assert stats._start_time is None

    def test_edge_cases(self):
        """Test des cas limites."""
        stats = OperationStats()
        
        # Opération avec temps zéro
        stats.add_operation("zero_time", 0.0, 0, 0)
        
        # Opération avec valeurs négatives
        stats.add_operation("negative", -0.1, -1, -1)
        
        result = stats.get_stats()
        assert result["total_operations"] == 2
        assert result["average_time"] == -0.05
        assert result["average_states"] == -0.5
        assert result["average_transitions"] == -0.5

    def test_operation_immutability(self):
        """Test que les opérations ajoutées ne peuvent pas être modifiées."""
        stats = OperationStats()
        stats.add_operation("union", 0.5, 10, 20)
        
        # Modifier la liste retournée ne doit pas affecter les statistiques
        history = stats.get_operation_history()
        history.append({"test": "data"})
        
        assert len(stats.get_operation_history()) == 1