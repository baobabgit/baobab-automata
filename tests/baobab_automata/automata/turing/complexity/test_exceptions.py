"""Tests unitaires pour les exceptions d'analyse de complexité."""

import unittest

from baobab_automata.algorithms.turing.exceptions import (
    ComplexityAnalysisError,
    InvalidComplexityAnalyzerError,
    ComplexityAnalysisTimeoutError,
    ResourceMonitoringError,
)


class TestComplexityAnalysisError(unittest.TestCase):
    """Tests pour l'exception de base ComplexityAnalysisError."""

    def test_complexity_analysis_error_creation(self):
        """Test de création d'une exception ComplexityAnalysisError."""
        error = ComplexityAnalysisError("Test error message")

        self.assertEqual(str(error), "Test error message")
        self.assertIsInstance(error, Exception)

    def test_complexity_analysis_error_inheritance(self):
        """Test de l'héritage de ComplexityAnalysisError."""
        error = ComplexityAnalysisError("Test")

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, ComplexityAnalysisError)


class TestInvalidComplexityAnalyzerError(unittest.TestCase):
    """Tests pour l'exception InvalidComplexityAnalyzerError."""

    def test_invalid_complexity_analyzer_error_creation(self):
        """Test de création d'une exception InvalidComplexityAnalyzerError."""
        error = InvalidComplexityAnalyzerError("Invalid configuration")

        self.assertEqual(str(error), "Invalid configuration")
        self.assertIsInstance(error, ComplexityAnalysisError)

    def test_invalid_complexity_analyzer_error_inheritance(self):
        """Test de l'héritage de InvalidComplexityAnalyzerError."""
        error = InvalidComplexityAnalyzerError("Test")

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, ComplexityAnalysisError)
        self.assertIsInstance(error, InvalidComplexityAnalyzerError)


class TestComplexityAnalysisTimeoutError(unittest.TestCase):
    """Tests pour l'exception ComplexityAnalysisTimeoutError."""

    def test_complexity_analysis_timeout_error_creation(self):
        """Test de création d'une exception ComplexityAnalysisTimeoutError."""
        error = ComplexityAnalysisTimeoutError("Analysis timeout")

        self.assertEqual(str(error), "Analysis timeout")
        self.assertIsInstance(error, ComplexityAnalysisError)

    def test_complexity_analysis_timeout_error_inheritance(self):
        """Test de l'héritage de ComplexityAnalysisTimeoutError."""
        error = ComplexityAnalysisTimeoutError("Test")

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, ComplexityAnalysisError)
        self.assertIsInstance(error, ComplexityAnalysisTimeoutError)


class TestResourceMonitoringError(unittest.TestCase):
    """Tests pour l'exception ResourceMonitoringError."""

    def test_resource_monitoring_error_creation(self):
        """Test de création d'une exception ResourceMonitoringError."""
        error = ResourceMonitoringError("Memory monitoring failed")

        self.assertEqual(str(error), "Memory monitoring failed")
        self.assertIsInstance(error, ComplexityAnalysisError)

    def test_resource_monitoring_error_inheritance(self):
        """Test de l'héritage de ResourceMonitoringError."""
        error = ResourceMonitoringError("Test")

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, ComplexityAnalysisError)
        self.assertIsInstance(error, ResourceMonitoringError)


class TestExceptionHierarchy(unittest.TestCase):
    """Tests pour la hiérarchie des exceptions."""

    def test_exception_hierarchy(self):
        """Test de la hiérarchie complète des exceptions."""
        # Test de la base
        base_error = ComplexityAnalysisError("Base error")
        self.assertIsInstance(base_error, Exception)

        # Test des exceptions spécialisées
        invalid_error = InvalidComplexityAnalyzerError("Invalid error")
        self.assertIsInstance(invalid_error, ComplexityAnalysisError)
        self.assertIsInstance(invalid_error, Exception)

        timeout_error = ComplexityAnalysisTimeoutError("Timeout error")
        self.assertIsInstance(timeout_error, ComplexityAnalysisError)
        self.assertIsInstance(timeout_error, Exception)

        resource_error = ResourceMonitoringError("Resource error")
        self.assertIsInstance(resource_error, ComplexityAnalysisError)
        self.assertIsInstance(resource_error, Exception)

    def test_exception_catching(self):
        """Test de capture des exceptions."""

        def raise_base_error():
            raise ComplexityAnalysisError("Base error")

        def raise_invalid_error():
            raise InvalidComplexityAnalyzerError("Invalid error")

        def raise_timeout_error():
            raise ComplexityAnalysisTimeoutError("Timeout error")

        def raise_resource_error():
            raise ResourceMonitoringError("Resource error")

        # Test de capture de la base
        with self.assertRaises(ComplexityAnalysisError):
            raise_base_error()

        # Test de capture des spécialisées
        with self.assertRaises(ComplexityAnalysisError):
            raise_invalid_error()

        with self.assertRaises(ComplexityAnalysisError):
            raise_timeout_error()

        with self.assertRaises(ComplexityAnalysisError):
            raise_resource_error()


if __name__ == "__main__":
    unittest.main()
