"""Interface abstraite pour l'analyse de complexité."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .types import ComplexityClass, DecidabilityStatus


class IComplexityAnalyzer(ABC):
    """Interface abstraite pour l'analyse de complexité."""

    @abstractmethod
    def analyze_time_complexity(
        self, machine: Any, test_cases: List[str]
    ) -> Dict[str, Any]:
        """Analyse la complexité temporelle d'une machine.

        :param machine: Machine à analyser
        :param test_cases: Cas de test pour l'analyse
        :return: Analyse de complexité temporelle
        :raises ComplexityAnalysisError: Si l'analyse échoue
        """
        pass

    @abstractmethod
    def analyze_space_complexity(
        self, machine: Any, test_cases: List[str]
    ) -> Dict[str, Any]:
        """Analyse la complexité spatiale d'une machine.

        :param machine: Machine à analyser
        :param test_cases: Cas de test pour l'analyse
        :return: Analyse de complexité spatiale
        :raises ComplexityAnalysisError: Si l'analyse échoue
        """
        pass

    @abstractmethod
    def classify_problem(self, machine: Any) -> ComplexityClass:
        """Classe un problème selon sa complexité.

        :param machine: Machine à classifier
        :return: Classe de complexité
        :raises ComplexityAnalysisError: Si la classification échoue
        """
        pass

    @abstractmethod
    def determine_decidability(self, machine: Any) -> DecidabilityStatus:
        """Détermine la décidabilité d'un problème.

        :param machine: Machine à analyser
        :return: Statut de décidabilité
        :raises ComplexityAnalysisError: Si l'analyse échoue
        """
        pass

    @abstractmethod
    def compare_complexity(
        self, machine1: Any, machine2: Any
    ) -> Dict[str, Any]:
        """Compare la complexité de deux machines.

        :param machine1: Première machine
        :param machine2: Deuxième machine
        :return: Comparaison de complexité
        :raises ComplexityAnalysisError: Si la comparaison échoue
        """
        pass
