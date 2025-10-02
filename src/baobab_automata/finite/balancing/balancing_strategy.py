"""
Interface pour les stratégies de balancing des automates finis.

Ce module définit l'interface abstraite que toutes les stratégies
de balancing doivent implémenter.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .balancing_metrics import BalancingMetrics
    from .balancing_result import BalancingResult
    from ..abstract_finite_automaton import AbstractFiniteAutomaton


class IBalancingStrategy(ABC):
    """
    Interface pour les stratégies de balancing des automates finis.
    
    Cette interface définit le contrat que toutes les stratégies
    de balancing doivent respecter pour être utilisées avec le
    moteur de balancing.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nom de la stratégie de balancing.
        
        :return: Nom unique de la stratégie
        :rtype: str
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """
        Description de la stratégie de balancing.
        
        :return: Description détaillée de la stratégie
        :rtype: str
        """
        pass
    
    @abstractmethod
    def balance(self, automaton: "AbstractFiniteAutomaton") -> "BalancingResult":
        """
        Applique la stratégie de balancing à un automate.
        
        :param automaton: Automate à équilibrer
        :type automaton: AbstractFiniteAutomaton
        :return: Résultat de l'opération de balancing
        :rtype: BalancingResult
        :raises BalancingError: Si l'opération de balancing échoue
        """
        pass
    
    @abstractmethod
    def get_metrics(self, automaton: "AbstractFiniteAutomaton") -> "BalancingMetrics":
        """
        Calcule les métriques de balancing pour un automate.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Métriques de balancing
        :rtype: BalancingMetrics
        """
        pass
    
    @abstractmethod
    def is_balanced(self, automaton: "AbstractFiniteAutomaton") -> bool:
        """
        Vérifie si un automate est équilibré selon cette stratégie.
        
        :param automaton: Automate à vérifier
        :type automaton: AbstractFiniteAutomaton
        :return: True si l'automate est équilibré, False sinon
        :rtype: bool
        """
        pass
    
    @abstractmethod
    def can_balance(self, automaton: "AbstractFiniteAutomaton") -> bool:
        """
        Vérifie si cette stratégie peut être appliquée à un automate.
        
        :param automaton: Automate à vérifier
        :type automaton: AbstractFiniteAutomaton
        :return: True si la stratégie peut être appliquée, False sinon
        :rtype: bool
        """
        pass
    
    def get_priority(self, automaton: "AbstractFiniteAutomaton") -> float:
        """
        Calcule la priorité de cette stratégie pour un automate donné.
        
        :param automaton: Automate à analyser
        :type automaton: AbstractFiniteAutomaton
        :return: Priorité de la stratégie (0.0 à 1.0)
        :rtype: float
        """
        if not self.can_balance(automaton):
            return 0.0
        
        metrics = self.get_metrics(automaton)
        
        # Priorité basée sur le besoin d'équilibrage
        if metrics.is_well_balanced:
            return 0.1  # Faible priorité si déjà équilibré
        
        # Priorité basée sur le score d'équilibrage
        return 1.0 - metrics.balance_score
    
    def __str__(self) -> str:
        """
        Représentation textuelle de la stratégie.
        
        :return: Nom et description de la stratégie
        :rtype: str
        """
        return f"{self.name}: {self.description}"
    
    def __repr__(self) -> str:
        """
        Représentation technique de la stratégie.
        
        :return: Représentation technique
        :rtype: str
        """
        return f"{self.__class__.__name__}(name='{self.name}')"