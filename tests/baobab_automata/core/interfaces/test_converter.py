"""
Tests unitaires pour l'interface IConverter.

Ce module teste l'interface IConverter.
"""

import pytest

from baobab_automata.core.interfaces.converter import IConverter


class TestIConverterInterface:
    """Tests pour l'interface IConverter."""

    def test_interface_has_required_methods(self):
        """Test que l'interface IConverter a toutes les méthodes requises."""
        required_methods = [
            "can_convert",
            "convert",
            "get_conversion_options",
            "get_conversion_info",
        ]

        for method_name in required_methods:
            assert hasattr(
                IConverter, method_name
            ), f"Method {method_name} missing from IConverter"

    def test_interface_methods_are_abstract(self):
        """Test que les méthodes de l'interface sont abstraites."""
        # Vérifier que l'interface ne peut pas être instanciée directement
        with pytest.raises(TypeError):
            IConverter()
