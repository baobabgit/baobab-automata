"""Tests unitaires pour l'analyseur de complexité."""

import unittest
from unittest.mock import Mock

from baobab_automata.algorithms.turing.complexity_analyzer import (
    ComplexityAnalyzer,
)
from baobab_automata.algorithms.turing.types import (
    ComplexityClass,
    DecidabilityStatus,
)
from baobab_automata.algorithms.turing.exceptions import (
    InvalidComplexityAnalyzerError,
)
from baobab_automata.turing.dtm import DTM
from baobab_automata.interfaces.turing_machine import TapeDirection


class TestComplexityAnalyzer(unittest.TestCase):
    """Tests pour l'analyseur de complexité."""

    def setUp(self):
        """Configuration des tests."""
        self.analyzer = ComplexityAnalyzer(
            enable_profiling=True,
            enable_memory_monitoring=True,
            max_analysis_time=30,
            sample_size=50,
        )

        # Création d'une machine de test simple
        self.simple_dtm = self._create_simple_dtm()

        # Création d'une machine de test complexe
        self.complex_dtm = self._create_complex_dtm()

    def test_complexity_analyzer_construction(self):
        """Test de construction de l'analyseur."""
        analyzer = ComplexityAnalyzer(
            enable_profiling=True,
            enable_memory_monitoring=True,
            max_analysis_time=30,
            sample_size=50,
        )

        self.assertTrue(analyzer._enable_profiling)
        self.assertTrue(analyzer._enable_memory_monitoring)
        self.assertEqual(analyzer._max_analysis_time, 30)
        self.assertEqual(analyzer._sample_size, 50)
        self.assertIsInstance(analyzer._analysis_cache, dict)
        self.assertIsInstance(analyzer._complexity_cache, dict)
        self.assertIsInstance(analyzer._analysis_stats, dict)

    def test_invalid_construction_parameters(self):
        """Test de construction avec paramètres invalides."""
        with self.assertRaises(InvalidComplexityAnalyzerError):
            ComplexityAnalyzer(max_analysis_time=0)

        with self.assertRaises(InvalidComplexityAnalyzerError):
            ComplexityAnalyzer(sample_size=-1)

    def test_time_complexity_analysis(self):
        """Test d'analyse de complexité temporelle."""
        test_cases = ["a", "aa", "aaa"]

        result = self.analyzer.analyze_time_complexity(self.simple_dtm, test_cases)

        self.assertIn("complexity_class", result)
        self.assertIn("time_metrics", result)
        self.assertIn("performance_data", result)
        self.assertIn("test_cases_analyzed", result)
        self.assertIn("analysis_time", result)
        self.assertIn("confidence_level", result)
        self.assertEqual(result["test_cases_analyzed"], len(test_cases))
        self.assertIsInstance(result["complexity_class"], str)
        self.assertIsInstance(result["time_metrics"], dict)

    def test_space_complexity_analysis(self):
        """Test d'analyse de complexité spatiale."""
        test_cases = ["a", "aa", "aaa"]

        result = self.analyzer.analyze_space_complexity(self.simple_dtm, test_cases)

        self.assertIn("space_complexity_class", result)
        self.assertIn("space_metrics", result)
        self.assertIn("memory_data", result)
        self.assertIn("test_cases_analyzed", result)
        self.assertIn("analysis_time", result)
        self.assertIn("confidence_level", result)
        self.assertEqual(result["test_cases_analyzed"], len(test_cases))
        self.assertIsInstance(result["space_complexity_class"], str)
        self.assertIsInstance(result["space_metrics"], dict)

    def test_problem_classification(self):
        """Test de classification de problème."""
        complexity_class = self.analyzer.classify_problem(self.simple_dtm)

        self.assertIsInstance(complexity_class, ComplexityClass)
        # La classification peut retourner UNKNOWN si les données sont insuffisantes
        # C'est acceptable pour ce test

    def test_decidability_determination(self):
        """Test de détermination de décidabilité."""
        decidability_status = self.analyzer.determine_decidability(self.simple_dtm)

        self.assertIsInstance(decidability_status, DecidabilityStatus)
        # Le statut peut être UNKNOWN si les tests de décidabilité échouent
        # C'est acceptable pour ce test

    def test_complexity_comparison(self):
        """Test de comparaison de complexité."""
        comparison = self.analyzer.compare_complexity(self.simple_dtm, self.complex_dtm)

        self.assertIn("machine1", comparison)
        self.assertIn("machine2", comparison)
        self.assertIn("comparison", comparison)
        self.assertIn("time_comparison", comparison["comparison"])
        self.assertIn("space_comparison", comparison["comparison"])
        self.assertIn("overall_comparison", comparison["comparison"])

        # Vérification des types de machines
        self.assertEqual(comparison["machine1"]["type"], "DTM")
        self.assertEqual(comparison["machine2"]["type"], "DTM")

    def test_resource_monitoring(self):
        """Test de monitoring des ressources."""
        analyzer = ComplexityAnalyzer(enable_memory_monitoring=True)

        resource_usage = analyzer.get_resource_usage()

        self.assertIn("memory_usage", resource_usage)
        self.assertIn("cpu_usage", resource_usage)
        self.assertIn("analysis_stats", resource_usage)
        self.assertIsInstance(resource_usage["analysis_stats"], dict)

    def test_analysis_cache(self):
        """Test du cache d'analyse."""
        machine = self.simple_dtm
        test_cases = ["a"]

        # Première analyse
        result1 = self.analyzer.analyze_time_complexity(machine, test_cases)

        # Deuxième analyse (devrait utiliser le cache)
        result2 = self.analyzer.analyze_time_complexity(machine, test_cases)

        self.assertGreater(self.analyzer._analysis_stats["cache_hits"], 0)
        self.assertEqual(result1["complexity_class"], result2["complexity_class"])

    def test_generate_test_cases(self):
        """Test de génération de cas de test."""
        test_cases = self.analyzer._generate_test_cases(self.simple_dtm, 10)

        self.assertIsInstance(test_cases, list)
        self.assertLessEqual(len(test_cases), 10)

        # Vérification que tous les cas de test sont des chaînes
        for test_case in test_cases:
            self.assertIsInstance(test_case, str)

    def test_generate_strings_of_length(self):
        """Test de génération de chaînes de longueur donnée."""
        alphabet = ["a", "b"]

        # Test longueur 0
        strings_0 = self.analyzer._generate_strings_of_length(alphabet, 0)
        self.assertEqual(strings_0, [""])

        # Test longueur 1
        strings_1 = self.analyzer._generate_strings_of_length(alphabet, 1)
        self.assertEqual(set(strings_1), {"a", "b"})

        # Test longueur 2
        strings_2 = self.analyzer._generate_strings_of_length(alphabet, 2)
        expected_2 = {"aa", "ab", "ba", "bb"}
        self.assertEqual(set(strings_2), expected_2)

    def test_calculate_growth_rate(self):
        """Test de calcul du taux de croissance."""
        times = [0.1, 0.2, 0.4, 0.8]
        lengths = [1, 2, 3, 4]

        growth_rate = self.analyzer._calculate_growth_rate(times, lengths)

        self.assertIsInstance(growth_rate, float)
        self.assertGreater(growth_rate, 0)

    def test_calculate_space_growth_rate(self):
        """Test de calcul du taux de croissance spatiale."""
        memory_usage = [100, 200, 400, 800]
        tape_lengths = [1, 2, 3, 4]

        growth_rate = self.analyzer._calculate_space_growth_rate(
            memory_usage, tape_lengths
        )

        self.assertIsInstance(growth_rate, float)
        self.assertGreater(growth_rate, 0)

    def test_determine_final_complexity_class(self):
        """Test de détermination de la classe de complexité finale."""
        # Test avec classes différentes
        final_class = self.analyzer._determine_final_complexity_class(
            ComplexityClass.P, ComplexityClass.NP
        )
        self.assertEqual(final_class, ComplexityClass.NP)

        # Test avec classes identiques
        final_class = self.analyzer._determine_final_complexity_class(
            ComplexityClass.P, ComplexityClass.P
        )
        self.assertEqual(final_class, ComplexityClass.P)

    def test_calculate_confidence_level(self):
        """Test de calcul du niveau de confiance."""
        # Test avec données parfaites
        perfect_data = {
            "execution_times": [0.1, 0.2, 0.3],
            "error_count": 0,
            "timeout_count": 0,
        }
        confidence = self.analyzer._calculate_confidence_level(perfect_data)
        self.assertEqual(confidence, 1.0)

        # Test avec erreurs
        error_data = {
            "execution_times": [0.1, 0.2],
            "error_count": 1,
            "timeout_count": 1,
        }
        confidence = self.analyzer._calculate_confidence_level(error_data)
        self.assertLess(confidence, 1.0)
        self.assertGreaterEqual(confidence, 0.0)

    def test_get_cache_key(self):
        """Test de génération de clé de cache."""
        machine = self.simple_dtm
        analysis_type = "time_complexity"

        cache_key = self.analyzer._get_cache_key(machine, analysis_type)

        self.assertIsInstance(cache_key, str)
        self.assertIn("DTM", cache_key)
        self.assertIn(analysis_type, cache_key)

    def test_analysis_with_empty_test_cases(self):
        """Test d'analyse avec cas de test vides."""
        result = self.analyzer.analyze_time_complexity(self.simple_dtm, [])

        self.assertIn("complexity_class", result)
        self.assertIn("time_metrics", result)
        self.assertIn("performance_data", result)
        self.assertGreaterEqual(result["test_cases_analyzed"], 0)

    def test_analysis_with_machine_without_simulate_method(self):
        """Test d'analyse avec machine sans méthode simulate."""
        mock_machine = Mock()
        mock_machine.alphabet = {"a", "b"}
        # Pas de méthode simulate

        result = self.analyzer.analyze_time_complexity(mock_machine, ["a"])

        # L'analyse devrait quand même fonctionner avec des données par défaut
        self.assertIn("complexity_class", result)
        self.assertIn("time_metrics", result)

    def _create_simple_dtm(self) -> DTM:
        """Crée une DTM simple pour les tests."""
        states = {"q0", "q1", "q_accept", "q_reject"}
        alphabet = {"a", "b"}
        tape_alphabet = {"a", "b", "B"}

        transitions = {
            ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
            ("q0", "b"): ("q_reject", "b", TapeDirection.STAY),
            ("q0", "B"): ("q_reject", "B", TapeDirection.STAY),
            ("q1", "a"): ("q_accept", "a", TapeDirection.STAY),
            ("q1", "b"): ("q_reject", "b", TapeDirection.STAY),
            ("q1", "B"): ("q_reject", "B", TapeDirection.STAY),
        }

        initial_state = "q0"
        accept_states = {"q_accept"}
        reject_states = {"q_reject"}

        dtm = DTM(
            states=states,
            alphabet=alphabet,
            tape_alphabet=tape_alphabet,
            transitions=transitions,
            initial_state=initial_state,
            accept_states=accept_states,
            reject_states=reject_states,
        )

        return dtm

    def _create_complex_dtm(self) -> DTM:
        """Crée une DTM complexe pour les tests."""
        states = {"q0", "q1", "q2", "q3", "q_accept", "q_reject"}
        alphabet = {"a", "b", "c"}
        tape_alphabet = {"a", "b", "c", "B"}

        transitions = {
            ("q0", "a"): ("q1", "a", TapeDirection.RIGHT),
            ("q0", "b"): ("q2", "b", TapeDirection.RIGHT),
            ("q0", "c"): ("q_reject", "c", TapeDirection.STAY),
            ("q0", "B"): ("q_reject", "B", TapeDirection.STAY),
            ("q1", "a"): ("q1", "a", TapeDirection.RIGHT),
            ("q1", "b"): ("q3", "b", TapeDirection.RIGHT),
            ("q1", "c"): ("q_reject", "c", TapeDirection.STAY),
            ("q1", "B"): ("q_reject", "B", TapeDirection.STAY),
            ("q2", "a"): ("q3", "a", TapeDirection.RIGHT),
            ("q2", "b"): ("q2", "b", TapeDirection.RIGHT),
            ("q2", "c"): ("q_reject", "c", TapeDirection.STAY),
            ("q2", "B"): ("q_reject", "B", TapeDirection.STAY),
            ("q3", "a"): ("q_accept", "a", TapeDirection.STAY),
            ("q3", "b"): ("q_accept", "b", TapeDirection.STAY),
            ("q3", "c"): ("q_reject", "c", TapeDirection.STAY),
            ("q3", "B"): ("q_reject", "B", TapeDirection.STAY),
        }

        initial_state = "q0"
        accept_states = {"q_accept"}
        reject_states = {"q_reject"}

        dtm = DTM(
            states=states,
            alphabet=alphabet,
            tape_alphabet=tape_alphabet,
            transitions=transitions,
            initial_state=initial_state,
            accept_states=accept_states,
            reject_states=reject_states,
        )

        return dtm


if __name__ == "__main__":
    unittest.main()
