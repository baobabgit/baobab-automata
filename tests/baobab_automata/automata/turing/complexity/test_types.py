"""Tests unitaires pour les types d'analyse de complexité."""

import unittest
from dataclasses import FrozenInstanceError

from baobab_automata.algorithms.turing.types import (
    ComplexityClass,
    DecidabilityStatus,
    ComplexityMetrics,
    AnalysisResult,
)


class TestComplexityClass(unittest.TestCase):
    """Tests pour l'énumération ComplexityClass."""

    def test_complexity_class_values(self):
        """Test des valeurs de l'énumération."""
        self.assertEqual(ComplexityClass.P.value, "polynomial_time")
        self.assertEqual(
            ComplexityClass.NP.value, "nondeterministic_polynomial_time"
        )
        self.assertEqual(ComplexityClass.PSPACE.value, "polynomial_space")
        self.assertEqual(ComplexityClass.EXPTIME.value, "exponential_time")
        self.assertEqual(ComplexityClass.EXPSPACE.value, "exponential_space")
        self.assertEqual(ComplexityClass.RECURSIVE.value, "recursive")
        self.assertEqual(
            ComplexityClass.RECURSIVELY_ENUMERABLE.value,
            "recursively_enumerable",
        )
        self.assertEqual(ComplexityClass.UNDECIDABLE.value, "undecidable")
        self.assertEqual(ComplexityClass.UNKNOWN.value, "unknown")

    def test_complexity_class_enumeration(self):
        """Test de l'énumération complète."""
        expected_values = {
            "polynomial_time",
            "nondeterministic_polynomial_time",
            "polynomial_space",
            "exponential_time",
            "exponential_space",
            "recursive",
            "recursively_enumerable",
            "undecidable",
            "unknown",
        }

        actual_values = {cls.value for cls in ComplexityClass}
        self.assertEqual(actual_values, expected_values)


class TestDecidabilityStatus(unittest.TestCase):
    """Tests pour l'énumération DecidabilityStatus."""

    def test_decidability_status_values(self):
        """Test des valeurs de l'énumération."""
        self.assertEqual(DecidabilityStatus.DECIDABLE.value, "decidable")
        self.assertEqual(
            DecidabilityStatus.SEMI_DECIDABLE.value, "semi_decidable"
        )
        self.assertEqual(DecidabilityStatus.UNDECIDABLE.value, "undecidable")
        self.assertEqual(DecidabilityStatus.UNKNOWN.value, "unknown")

    def test_decidability_status_enumeration(self):
        """Test de l'énumération complète."""
        expected_values = {
            "decidable",
            "semi_decidable",
            "undecidable",
            "unknown",
        }

        actual_values = {status.value for status in DecidabilityStatus}
        self.assertEqual(actual_values, expected_values)


class TestComplexityMetrics(unittest.TestCase):
    """Tests pour la classe ComplexityMetrics."""

    def test_complexity_metrics_creation(self):
        """Test de création d'une instance ComplexityMetrics."""
        metrics = ComplexityMetrics(
            time_complexity="O(n)",
            space_complexity="O(1)",
            complexity_class=ComplexityClass.P,
            decidability_status=DecidabilityStatus.DECIDABLE,
            worst_case_time=1.0,
            worst_case_space=100,
            average_case_time=0.5,
            average_case_space=50,
        )

        self.assertEqual(metrics.time_complexity, "O(n)")
        self.assertEqual(metrics.space_complexity, "O(1)")
        self.assertEqual(metrics.complexity_class, ComplexityClass.P)
        self.assertEqual(
            metrics.decidability_status, DecidabilityStatus.DECIDABLE
        )
        self.assertEqual(metrics.worst_case_time, 1.0)
        self.assertEqual(metrics.worst_case_space, 100)
        self.assertEqual(metrics.average_case_time, 0.5)
        self.assertEqual(metrics.average_case_space, 50)

    def test_complexity_metrics_optional_fields(self):
        """Test de création avec champs optionnels."""
        metrics = ComplexityMetrics(
            time_complexity="O(n²)",
            space_complexity="O(n)",
            complexity_class=ComplexityClass.NP,
            decidability_status=DecidabilityStatus.UNKNOWN,
        )

        self.assertEqual(metrics.time_complexity, "O(n²)")
        self.assertEqual(metrics.space_complexity, "O(n)")
        self.assertEqual(metrics.complexity_class, ComplexityClass.NP)
        self.assertEqual(
            metrics.decidability_status, DecidabilityStatus.UNKNOWN
        )
        self.assertIsNone(metrics.worst_case_time)
        self.assertIsNone(metrics.worst_case_space)
        self.assertIsNone(metrics.average_case_time)
        self.assertIsNone(metrics.average_case_space)

    def test_complexity_metrics_immutability(self):
        """Test de l'immutabilité de ComplexityMetrics."""
        metrics = ComplexityMetrics(
            time_complexity="O(n)",
            space_complexity="O(1)",
            complexity_class=ComplexityClass.P,
            decidability_status=DecidabilityStatus.DECIDABLE,
        )

        # Test de modification (devrait lever une exception)
        with self.assertRaises(FrozenInstanceError):
            metrics.time_complexity = "O(n²)"


class TestAnalysisResult(unittest.TestCase):
    """Tests pour la classe AnalysisResult."""

    def test_analysis_result_creation(self):
        """Test de création d'une instance AnalysisResult."""
        metrics = ComplexityMetrics(
            time_complexity="O(n)",
            space_complexity="O(1)",
            complexity_class=ComplexityClass.P,
            decidability_status=DecidabilityStatus.DECIDABLE,
        )

        result = AnalysisResult(
            machine_type="DTM",
            complexity_metrics=metrics,
            analysis_time=1.5,
            test_cases_analyzed=10,
            confidence_level=0.95,
            recommendations=["Optimize transitions", "Reduce states"],
        )

        self.assertEqual(result.machine_type, "DTM")
        self.assertEqual(result.complexity_metrics, metrics)
        self.assertEqual(result.analysis_time, 1.5)
        self.assertEqual(result.test_cases_analyzed, 10)
        self.assertEqual(result.confidence_level, 0.95)
        self.assertEqual(
            result.recommendations, ["Optimize transitions", "Reduce states"]
        )

    def test_analysis_result_empty_recommendations(self):
        """Test de création avec recommandations vides."""
        metrics = ComplexityMetrics(
            time_complexity="O(n)",
            space_complexity="O(1)",
            complexity_class=ComplexityClass.P,
            decidability_status=DecidabilityStatus.DECIDABLE,
        )

        result = AnalysisResult(
            machine_type="NTM",
            complexity_metrics=metrics,
            analysis_time=2.0,
            test_cases_analyzed=5,
            confidence_level=0.8,
            recommendations=[],
        )

        self.assertEqual(result.machine_type, "NTM")
        self.assertEqual(result.recommendations, [])

    def test_analysis_result_immutability(self):
        """Test de l'immutabilité de AnalysisResult."""
        metrics = ComplexityMetrics(
            time_complexity="O(n)",
            space_complexity="O(1)",
            complexity_class=ComplexityClass.P,
            decidability_status=DecidabilityStatus.DECIDABLE,
        )

        result = AnalysisResult(
            machine_type="DTM",
            complexity_metrics=metrics,
            analysis_time=1.0,
            test_cases_analyzed=5,
            confidence_level=0.9,
            recommendations=[],
        )

        # Test de modification (devrait lever une exception)
        with self.assertRaises(FrozenInstanceError):
            result.machine_type = "NTM"


if __name__ == "__main__":
    unittest.main()
