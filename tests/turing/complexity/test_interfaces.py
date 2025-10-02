"""Tests unitaires pour les interfaces d'analyse de complexité."""

import unittest
from abc import ABC
from unittest.mock import Mock

from baobab_automata.turing.complexity.interfaces import IComplexityAnalyzer
from baobab_automata.turing.complexity.types import (
    ComplexityClass,
    DecidabilityStatus,
)


class TestComplexityAnalyzer(unittest.TestCase):
    """Implémentation concrète pour tester l'interface."""

    def analyze_time_complexity(self, machine, test_cases):
        """Implémentation de test."""
        return {"complexity_class": "P", "time_metrics": {}}

    def analyze_space_complexity(self, machine, test_cases):
        """Implémentation de test."""
        return {"space_complexity_class": "P", "space_metrics": {}}

    def classify_problem(self, machine):
        """Implémentation de test."""
        return ComplexityClass.P

    def determine_decidability(self, machine):
        """Implémentation de test."""
        return DecidabilityStatus.DECIDABLE

    def compare_complexity(self, machine1, machine2):
        """Implémentation de test."""
        return {"comparison": "equal"}


class TestIComplexityAnalyzer(unittest.TestCase):
    """Tests pour l'interface IComplexityAnalyzer."""

    def test_interface_is_abstract(self):
        """Test que l'interface est abstraite."""
        self.assertTrue(issubclass(IComplexityAnalyzer, ABC))

    def test_interface_methods_exist(self):
        """Test que toutes les méthodes de l'interface existent."""
        required_methods = [
            "analyze_time_complexity",
            "analyze_space_complexity",
            "classify_problem",
            "determine_decidability",
            "compare_complexity",
        ]

        for method_name in required_methods:
            self.assertTrue(hasattr(IComplexityAnalyzer, method_name))

    def test_concrete_implementation(self):
        """Test d'une implémentation concrète de l'interface."""
        analyzer = TestComplexityAnalyzer()

        # Test que l'implémentation peut être utilisée
        machine = Mock()
        test_cases = ["a", "b"]

        # Test des méthodes
        time_result = analyzer.analyze_time_complexity(machine, test_cases)
        self.assertIsInstance(time_result, dict)

        space_result = analyzer.analyze_space_complexity(machine, test_cases)
        self.assertIsInstance(space_result, dict)

        complexity_class = analyzer.classify_problem(machine)
        self.assertIsInstance(complexity_class, ComplexityClass)

        decidability_status = analyzer.determine_decidability(machine)
        self.assertIsInstance(decidability_status, DecidabilityStatus)

        comparison = analyzer.compare_complexity(machine, machine)
        self.assertIsInstance(comparison, dict)

    def test_interface_cannot_be_instantiated_directly(self):
        """Test que l'interface ne peut pas être instanciée directement."""
        with self.assertRaises(TypeError):
            IComplexityAnalyzer()

    def test_method_signatures(self):
        """Test des signatures des méthodes de l'interface."""
        # Test analyze_time_complexity
        method = IComplexityAnalyzer.analyze_time_complexity
        self.assertIsNotNone(method)

        # Test analyze_space_complexity
        method = IComplexityAnalyzer.analyze_space_complexity
        self.assertIsNotNone(method)

        # Test classify_problem
        method = IComplexityAnalyzer.classify_problem
        self.assertIsNotNone(method)

        # Test determine_decidability
        method = IComplexityAnalyzer.determine_decidability
        self.assertIsNotNone(method)

        # Test compare_complexity
        method = IComplexityAnalyzer.compare_complexity
        self.assertIsNotNone(method)


if __name__ == "__main__":
    unittest.main()
