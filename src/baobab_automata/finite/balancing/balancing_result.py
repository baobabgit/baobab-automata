"""
Types de résultats pour les stratégies de balancing.

Ce module définit les types de données utilisés pour représenter
les résultats des opérations de balancing des automates finis.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .balancing_metrics import BalancingMetrics
    from ..abstract_finite_automaton import AbstractFiniteAutomaton


@dataclass(frozen=True)
class BalancingResult:
    """
    Résultat d'une opération de balancing.
    
    Cette classe encapsule tous les résultats d'une opération de balancing,
    incluant l'automate original, l'automate équilibré, les métriques
    avant et après, et les statistiques de performance.
    
    :param original_automaton: Automate original avant balancing
    :type original_automaton: AbstractFiniteAutomaton
    :param balanced_automaton: Automate équilibré après balancing
    :type balanced_automaton: AbstractFiniteAutomaton
    :param metrics_before: Métriques avant balancing
    :type metrics_before: BalancingMetrics
    :param metrics_after: Métriques après balancing
    :type metrics_after: BalancingMetrics
    :param improvement_ratio: Ratio d'amélioration (0.0 à 1.0)
    :type improvement_ratio: float
    :param execution_time: Temps d'exécution en secondes
    :type execution_time: float
    :param memory_usage: Utilisation mémoire en octets
    :type memory_usage: int
    :param strategy_name: Nom de la stratégie utilisée
    :type strategy_name: str
    """
    
    original_automaton: "AbstractFiniteAutomaton"
    balanced_automaton: "AbstractFiniteAutomaton"
    metrics_before: "BalancingMetrics"
    metrics_after: "BalancingMetrics"
    improvement_ratio: float
    execution_time: float
    memory_usage: int
    strategy_name: str
    
    def __post_init__(self) -> None:
        """
        Valide les données du résultat après initialisation.
        
        :raises ValueError: Si les données sont invalides
        """
        if not 0.0 <= self.improvement_ratio <= 1.0:
            raise ValueError(
                f"Ratio d'amélioration invalide: {self.improvement_ratio}"
            )
        
        if self.execution_time < 0.0:
            raise ValueError(
                f"Temps d'exécution invalide: {self.execution_time}"
            )
        
        if self.memory_usage < 0:
            raise ValueError(
                f"Utilisation mémoire invalide: {self.memory_usage}"
            )
    
    @property
    def is_improvement(self) -> bool:
        """
        Indique si le balancing a amélioré les performances.
        
        :return: True si amélioration, False sinon
        :rtype: bool
        """
        return self.improvement_ratio > 0.0
    
    @property
    def performance_gain(self) -> float:
        """
        Calcule le gain de performance en pourcentage.
        
        :return: Gain de performance en pourcentage
        :rtype: float
        """
        return self.improvement_ratio * 100.0
    
    def to_dict(self) -> dict:
        """
        Sérialise le résultat en dictionnaire.
        
        :return: Dictionnaire représentant le résultat
        :rtype: dict
        """
        return {
            "original_automaton": self.original_automaton.to_dict(),
            "balanced_automaton": self.balanced_automaton.to_dict(),
            "metrics_before": self.metrics_before.to_dict(),
            "metrics_after": self.metrics_after.to_dict(),
            "improvement_ratio": self.improvement_ratio,
            "execution_time": self.execution_time,
            "memory_usage": self.memory_usage,
            "strategy_name": self.strategy_name,
            "is_improvement": self.is_improvement,
            "performance_gain": self.performance_gain,
        }