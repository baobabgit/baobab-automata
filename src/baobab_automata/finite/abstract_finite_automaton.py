"""
Interface abstraite pour les automates finis.

Ce module définit l'interface AbstractFiniteAutomaton qui sert de base
pour tous les types d'automates finis (DFA, NFA, ε-NFA).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Set


class AbstractFiniteAutomaton(ABC):
    """
    Interface abstraite pour tous les automates finis.

    Cette interface définit le contrat commun pour tous les types
    d'automates finis (DFA, NFA, ε-NFA) dans la bibliothèque.
    """

    @property
    @abstractmethod
    def states(self) -> Set[str]:
        """
        Ensemble des états de l'automate.

        :return: Ensemble des identifiants des états
        :rtype: Set[str]
        """
        pass

    @property
    @abstractmethod
    def alphabet(self) -> Set[str]:
        """
        Alphabet de l'automate.

        :return: Ensemble des symboles de l'alphabet
        :rtype: Set[str]
        """
        pass

    @property
    @abstractmethod
    def initial_state(self) -> str:
        """
        État initial de l'automate.

        :return: Identifiant de l'état initial
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def final_states(self) -> Set[str]:
        """
        Ensemble des états finaux.

        :return: Ensemble des identifiants des états finaux
        :rtype: Set[str]
        """
        pass

    @abstractmethod
    def accepts(self, word: str) -> bool:
        """
        Vérifie si l'automate accepte un mot donné.

        :param word: Mot à tester
        :type word: str
        :return: True si le mot est accepté, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_transition(self, state: str, symbol: str) -> Optional[str]:
        """
        Récupère l'état de destination pour une transition donnée.

        :param state: État source
        :type state: str
        :param symbol: Symbole de la transition
        :type symbol: str
        :return: État de destination ou None si la transition n'existe pas
        :rtype: Optional[str]
        """
        pass

    @abstractmethod
    def is_final_state(self, state: str) -> bool:
        """
        Vérifie si un état est final.

        :param state: Identifiant de l'état
        :type state: str
        :return: True si l'état est final, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_reachable_states(self) -> Set[str]:
        """
        Récupère tous les états accessibles depuis l'état initial.

        :return: Ensemble des états accessibles
        :rtype: Set[str]
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """
        Valide la cohérence de l'automate.

        :return: True si l'automate est valide, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Sérialise l'automate en dictionnaire.

        :return: Dictionnaire représentant l'automate
        :rtype: Dict[str, Any]
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AbstractFiniteAutomaton":
        """
        Crée un automate depuis un dictionnaire.

        :param data: Dictionnaire représentant l'automate
        :type data: Dict[str, Any]
        :return: Instance de l'automate
        :rtype: AbstractFiniteAutomaton
        """
        pass
