"""
Tests unitaires pour l'interface IRecognizer.

Ce module teste l'interface IRecognizer.
"""

import pytest

from baobab_automata.core.interfaces.recognizer import IRecognizer


class TestIRecognizerInterface:
    """Tests pour l'interface IRecognizer."""

    def test_interface_has_required_methods(self):
        """Test que l'interface IRecognizer a toutes les méthodes requises."""
        required_methods = [
            "recognize",
            "recognize_with_trace",
            "get_accepting_paths",
            "is_deterministic",
            "get_language_properties",
        ]

        for method_name in required_methods:
            assert hasattr(
                IRecognizer, method_name
            ), f"Method {method_name} missing from IRecognizer"

    def test_interface_methods_are_abstract(self):
        """Test que les méthodes de l'interface sont abstraites."""
        # Vérifier que l'interface ne peut pas être instanciée directement
        with pytest.raises(TypeError):
            IRecognizer()
