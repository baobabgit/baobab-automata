"""
Interface abstraite pour la reconnaissance de mots.

Ce module définit l'interface IRecognizer pour la reconnaissance de mots
par un automate.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from .state import IState


class IRecognizer(ABC):
    """
    Interface abstraite pour la reconnaissance de mots.

    Cette interface définit le contrat que doivent respecter tous les
    mécanismes de reconnaissance de mots, indépendamment du type d'automate
    utilisé.

    La reconnaissance consiste à déterminer si un mot donné appartient au
    langage reconnu par l'automate.
    """

    @abstractmethod
    def recognize(
        self, word: str, context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Reconnaît si un mot appartient au langage de l'automate.

        :param word: Mot à reconnaître
        :type word: str
        :param context: Contexte d'exécution optionnel
        :type context: Optional[Dict[str, Any]]
        :return: True si le mot est reconnu, False sinon
        :rtype: bool
        :raises RecognitionError: Si une erreur survient lors de la reconnaissance
        """
        pass

    @abstractmethod
    def recognize_with_trace(
        self, word: str, context: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Reconnaît un mot et retourne la trace d'exécution.

        :param word: Mot à reconnaître
        :type word: str
        :param context: Contexte d'exécution optionnel
        :type context: Optional[Dict[str, Any]]
        :return: Tuple (reconnu, trace) où trace est la liste des étapes
        :rtype: Tuple[bool, List[Dict[str, Any]]]
        :raises RecognitionError: Si une erreur survient lors de la reconnaissance
        """
        pass

    @abstractmethod
    def get_accepting_paths(
        self, word: str, context: Optional[Dict[str, Any]] = None
    ) -> List[List[IState]]:
        """
        Retourne tous les chemins acceptants pour un mot.

        :param word: Mot à analyser
        :type word: str
        :param context: Contexte d'exécution optionnel
        :type context: Optional[Dict[str, Any]]
        :return: Liste des chemins acceptants (chaque chemin est une liste d'états)
        :rtype: List[List[IState]]
        :raises RecognitionError: Si une erreur survient lors de l'analyse
        """
        pass

    @abstractmethod
    def is_deterministic(self) -> bool:
        """
        Vérifie si l'automate est déterministe.

        :return: True si l'automate est déterministe, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def get_language_properties(self) -> Dict[str, Any]:
        """
        Retourne les propriétés du langage reconnu.

        :return: Dictionnaire des propriétés du langage
        :rtype: Dict[str, Any]
        """
        pass
