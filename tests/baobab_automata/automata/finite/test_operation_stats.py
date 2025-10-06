"""
Tests unitaires pour la classe OperationStats.

Ce module contient tous les tests unitaires pour valider le bon fonctionnement
de la classe OperationStats selon les spécifications détaillées.
"""

import time
import unittest

from baobab_automata.automata.finite.operation_stats import OperationStats


class TestOperationStats(unittest.TestCase):
    """Tests unitaires pour la classe OperationStats."""

    def setUp(self):
        """Configuration des tests."""
        self.stats = OperationStats()

    def test_initialization(self):
        """Test de l'initialisation."""
        self.assertEqual(len(self.stats._operations), 0)
        self.assertIsNone(self.stats._start_time)

    def test_add_operation(self):
        """Test d'ajout d'une opération."""
        self.stats.add_operation("union", 0.1, 10, 20, 1024)

        self.assertEqual(len(self.stats._operations), 1)
        operation = self.stats._operations[0]
        self.assertEqual(operation["operation"], "union")
        self.assertEqual(operation["time"], 0.1)
        self.assertEqual(operation["states"], 10)
        self.assertEqual(operation["transitions"], 20)
        self.assertEqual(operation["memory"], 1024)
        self.assertIn("timestamp", operation)

    def test_add_operation_without_memory(self):
        """Test d'ajout d'une opération sans mémoire."""
        self.stats.add_operation("intersection", 0.2, 15, 30)

        self.assertEqual(len(self.stats._operations), 1)
        operation = self.stats._operations[0]
        self.assertEqual(operation["memory"], 0)

    def test_start_timing(self):
        """Test de démarrage du chronométrage."""
        self.stats.start_timing()
        self.assertIsNotNone(self.stats._start_time)
        self.assertGreaterEqual(self.stats._start_time, 0)

    def test_stop_timing_success(self):
        """Test d'arrêt du chronométrage avec succès."""
        self.stats.start_timing()
        time.sleep(0.01)  # Petit délai pour avoir un temps > 0
        self.stats.stop_timing("complement", 5, 10, 512)

        self.assertEqual(len(self.stats._operations), 1)
        operation = self.stats._operations[0]
        self.assertEqual(operation["operation"], "complement")
        self.assertGreater(operation["time"], 0)
        self.assertEqual(operation["states"], 5)
        self.assertEqual(operation["transitions"], 10)
        self.assertEqual(operation["memory"], 512)
        self.assertIsNone(self.stats._start_time)

    def test_stop_timing_without_start(self):
        """Test d'arrêt du chronométrage sans démarrage."""
        with self.assertRaises(ValueError):
            self.stats.stop_timing("union", 10, 20)

    def test_get_stats_empty(self):
        """Test de récupération des statistiques avec aucune opération."""
        stats = self.stats.get_stats()

        expected = {
            "total_operations": 0,
            "average_time": 0.0,
            "total_time": 0.0,
            "average_states": 0.0,
            "average_transitions": 0.0,
            "operations_by_type": {},
        }
        self.assertEqual(stats, expected)

    def test_get_stats_with_operations(self):
        """Test de récupération des statistiques avec des opérations."""
        # Ajouter plusieurs opérations
        self.stats.add_operation("union", 0.1, 10, 20, 1000)
        self.stats.add_operation("union", 0.2, 15, 30, 1500)
        self.stats.add_operation("intersection", 0.3, 20, 40, 2000)

        stats = self.stats.get_stats()

        self.assertEqual(stats["total_operations"], 3)
        self.assertAlmostEqual(stats["average_time"], 0.2, places=1)
        self.assertAlmostEqual(stats["total_time"], 0.6, places=1)
        self.assertAlmostEqual(stats["average_states"], 15.0, places=1)
        self.assertAlmostEqual(stats["average_transitions"], 30.0, places=1)

        # Vérifier les statistiques par type
        self.assertIn("union", stats["operations_by_type"])
        self.assertIn("intersection", stats["operations_by_type"])

        union_stats = stats["operations_by_type"]["union"]
        self.assertEqual(union_stats["count"], 2)
        self.assertAlmostEqual(union_stats["average_time"], 0.15, places=2)
        self.assertEqual(union_stats["total_states"], 25)
        self.assertEqual(union_stats["average_states"], 12.5)

    def test_get_operation_history(self):
        """Test de récupération de l'historique des opérations."""
        self.stats.add_operation("union", 0.1, 10, 20)
        self.stats.add_operation("intersection", 0.2, 15, 30)

        history = self.stats.get_operation_history()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["operation"], "union")
        self.assertEqual(history[1]["operation"], "intersection")

        # Vérifier que c'est une copie
        self.assertIsNot(history, self.stats._operations)

    def test_get_operations_by_type(self):
        """Test de récupération des opérations par type."""
        self.stats.add_operation("union", 0.1, 10, 20)
        self.stats.add_operation("intersection", 0.2, 15, 30)
        self.stats.add_operation("union", 0.3, 20, 40)

        union_ops = self.stats.get_operations_by_type("union")
        intersection_ops = self.stats.get_operations_by_type("intersection")
        complement_ops = self.stats.get_operations_by_type("complement")

        self.assertEqual(len(union_ops), 2)
        self.assertEqual(len(intersection_ops), 1)
        self.assertEqual(len(complement_ops), 0)

        self.assertEqual(union_ops[0]["operation"], "union")
        self.assertEqual(union_ops[1]["operation"], "union")
        self.assertEqual(intersection_ops[0]["operation"], "intersection")

    def test_reset(self):
        """Test de remise à zéro des statistiques."""
        self.stats.add_operation("union", 0.1, 10, 20)
        self.stats.start_timing()

        self.stats.reset()

        self.assertEqual(len(self.stats._operations), 0)
        self.assertIsNone(self.stats._start_time)

    def test_export_to_dict(self):
        """Test d'export vers dictionnaire."""
        self.stats.add_operation("union", 0.1, 10, 20, 1000)

        exported = self.stats.export_to_dict()

        self.assertIn("stats", exported)
        self.assertIn("history", exported)
        self.assertEqual(len(exported["history"]), 1)
        self.assertEqual(exported["history"][0]["operation"], "union")

    def test_import_from_dict_valid(self):
        """Test d'import depuis dictionnaire valide."""
        data = {
            "history": [
                {
                    "operation": "union",
                    "time": 0.1,
                    "states": 10,
                    "transitions": 20,
                    "memory": 1000,
                },
                {
                    "operation": "intersection",
                    "time": 0.2,
                    "states": 15,
                    "transitions": 30,
                    "memory": 1500,
                },
            ]
        }

        self.stats.import_from_dict(data)

        self.assertEqual(len(self.stats._operations), 2)
        self.assertEqual(self.stats._operations[0]["operation"], "union")
        self.assertEqual(self.stats._operations[1]["operation"], "intersection")

    def test_import_from_dict_invalid_missing_history(self):
        """Test d'import depuis dictionnaire invalide (manque history)."""
        data = {"stats": {}}

        with self.assertRaises(ValueError):
            self.stats.import_from_dict(data)

    def test_import_from_dict_invalid_missing_keys(self):
        """Test d'import depuis dictionnaire invalide (manque des clés)."""
        data = {
            "history": [
                {"operation": "union", "time": 0.1}  # Manque states, transitions
            ]
        }

        with self.assertRaises(ValueError):
            self.stats.import_from_dict(data)

    def test_import_from_dict_resets_existing(self):
        """Test que l'import remplace les données existantes."""
        # Ajouter des données existantes
        self.stats.add_operation("old", 0.1, 10, 20)

        # Importer de nouvelles données
        data = {
            "history": [
                {
                    "operation": "new",
                    "time": 0.2,
                    "states": 15,
                    "transitions": 30,
                    "memory": 0,
                }
            ]
        }
        self.stats.import_from_dict(data)

        # Vérifier que les anciennes données sont remplacées
        self.assertEqual(len(self.stats._operations), 1)
        self.assertEqual(self.stats._operations[0]["operation"], "new")

    def test_timing_accuracy(self):
        """Test de la précision du chronométrage."""
        self.stats.start_timing()
        time.sleep(0.1)  # 100ms
        self.stats.stop_timing("test", 1, 1)

        operation = self.stats._operations[0]
        # Vérifier que le temps est proche de 0.1 secondes (tolérance de 50ms)
        self.assertGreaterEqual(operation["time"], 0.05)
        self.assertLessEqual(operation["time"], 0.15)


if __name__ == "__main__":
    unittest.main()
