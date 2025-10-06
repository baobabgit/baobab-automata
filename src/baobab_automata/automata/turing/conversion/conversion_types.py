"""
Types de base pour les algorithmes de conversion des machines de Turing.

Ce module définit les énumérations et classes de base utilisées par
les algorithmes de conversion entre différents types de machines de Turing.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Type


class ConversionType(Enum):
    """Types de conversions supportées."""

    NTM_TO_DTM = "ntm_to_dtm"
    MULTITAPE_TO_SINGLE = "multitape_to_single"
    DTM_TO_TM = "dtm_to_tm"
    TM_TO_DTM = "tm_to_dtm"
    STATE_REDUCTION = "state_reduction"
    SYMBOL_MINIMIZATION = "symbol_minimization"


@dataclass(frozen=True)
class ConversionResult:
    """Résultat d'une conversion."""

    converted_machine: Any
    conversion_type: ConversionType
    equivalence_verified: bool = False
    optimization_applied: bool = False
    conversion_stats: Dict[str, Any] = None

    def __post_init__(self):
        """Initialise les statistiques si elles ne sont pas fournies."""
        if self.conversion_stats is None:
            object.__setattr__(self, "conversion_stats", {})


class IConversionAlgorithm(ABC):
    """Interface abstraite pour les algorithmes de conversion."""

    @abstractmethod
    def convert(
        self, source_machine: Any, target_type: Type, **kwargs
    ) -> ConversionResult:
        """Convertit une machine source vers un type cible.

        :param source_machine: Machine source à convertir
        :param target_type: Type cible de la conversion
        :param kwargs: Paramètres additionnels pour la conversion
        :return: Résultat de la conversion
        :raises ConversionError: Si la conversion échoue
        """
        pass

    @abstractmethod
    def verify_equivalence(
        self,
        source_machine: Any,
        converted_machine: Any,
        test_cases: List[str],
    ) -> bool:
        """Vérifie l'équivalence entre deux machines.

        :param source_machine: Machine source
        :param converted_machine: Machine convertie
        :param test_cases: Cas de test pour la vérification
        :return: True si les machines sont équivalentes
        """
        pass

    @abstractmethod
    def optimize_conversion(
        self, conversion_result: ConversionResult
    ) -> ConversionResult:
        """Optimise le résultat d'une conversion.

        :param conversion_result: Résultat de conversion à optimiser
        :return: Résultat optimisé
        """
        pass

    @abstractmethod
    def get_conversion_complexity(self, source_machine: Any) -> Dict[str, Any]:
        """Analyse la complexité d'une conversion.

        :param source_machine: Machine source
        :return: Analyse de complexité
        """
        pass
