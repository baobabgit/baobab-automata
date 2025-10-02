"""
Tests pour les types de base de conversion.
"""

import pytest
from src.baobab_automata.turing.conversion.conversion_types import (
    ConversionType,
    ConversionResult,
    IConversionAlgorithm,
)


class TestConversionType:
    """Tests pour l'énumération ConversionType."""

    def test_conversion_type_values(self):
        """Teste les valeurs de l'énumération ConversionType."""
        assert ConversionType.NTM_TO_DTM.value == "ntm_to_dtm"
        assert (
            ConversionType.MULTITAPE_TO_SINGLE.value == "multitape_to_single"
        )
        assert ConversionType.DTM_TO_TM.value == "dtm_to_tm"
        assert ConversionType.TM_TO_DTM.value == "tm_to_dtm"
        assert ConversionType.STATE_REDUCTION.value == "state_reduction"
        assert (
            ConversionType.SYMBOL_MINIMIZATION.value == "symbol_minimization"
        )

    def test_conversion_type_count(self):
        """Teste le nombre de types de conversion."""
        assert len(ConversionType) == 6


class TestConversionResult:
    """Tests pour la classe ConversionResult."""

    def test_conversion_result_creation(self):
        """Teste la création d'un ConversionResult."""
        machine = object()
        result = ConversionResult(
            converted_machine=machine,
            conversion_type=ConversionType.NTM_TO_DTM,
        )

        assert result.converted_machine is machine
        assert result.conversion_type == ConversionType.NTM_TO_DTM
        assert result.equivalence_verified is False
        assert result.optimization_applied is False
        assert result.conversion_stats == {}

    def test_conversion_result_with_stats(self):
        """Teste la création d'un ConversionResult avec des statistiques."""
        machine = object()
        stats = {"test": "value"}
        result = ConversionResult(
            converted_machine=machine,
            conversion_type=ConversionType.NTM_TO_DTM,
            equivalence_verified=True,
            optimization_applied=True,
            conversion_stats=stats,
        )

        assert result.converted_machine is machine
        assert result.conversion_type == ConversionType.NTM_TO_DTM
        assert result.equivalence_verified is True
        assert result.optimization_applied is True
        assert result.conversion_stats == stats

    def test_conversion_result_immutable(self):
        """Teste que ConversionResult est immutable."""
        machine = object()
        result = ConversionResult(
            converted_machine=machine,
            conversion_type=ConversionType.NTM_TO_DTM,
        )

        # Teste que les attributs ne peuvent pas être modifiés
        with pytest.raises(AttributeError):
            result.converted_machine = object()

        with pytest.raises(AttributeError):
            result.conversion_type = ConversionType.DTM_TO_TM


class TestIConversionAlgorithm:
    """Tests pour l'interface IConversionAlgorithm."""

    def test_interface_abstract(self):
        """Teste que l'interface est abstraite."""
        with pytest.raises(TypeError):
            IConversionAlgorithm()

    def test_interface_methods(self):
        """Teste que l'interface définit les méthodes requises."""
        # Vérifie que les méthodes abstraites sont définies
        assert hasattr(IConversionAlgorithm, "convert")
        assert hasattr(IConversionAlgorithm, "verify_equivalence")
        assert hasattr(IConversionAlgorithm, "optimize_conversion")
        assert hasattr(IConversionAlgorithm, "get_conversion_complexity")

        # Vérifie que les méthodes sont abstraites
        assert getattr(
            IConversionAlgorithm.convert, "__isabstractmethod__", False
        )
        assert getattr(
            IConversionAlgorithm.verify_equivalence,
            "__isabstractmethod__",
            False,
        )
        assert getattr(
            IConversionAlgorithm.optimize_conversion,
            "__isabstractmethod__",
            False,
        )
        assert getattr(
            IConversionAlgorithm.get_conversion_complexity,
            "__isabstractmethod__",
            False,
        )
