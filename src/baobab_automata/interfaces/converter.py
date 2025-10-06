"""
Interface abstraite pour les conversions d'automates.

Ce module définit l'interface IConverter pour la conversion entre différents
types d'automates.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .automaton import IAutomaton, AutomatonType


class IConverter(ABC):
    """
    Interface abstraite pour les conversions d'automates.

    Cette interface définit le contrat que doivent respecter tous les
    mécanismes de conversion entre différents types d'automates.

    La conversion permet de transformer un automate d'un type vers un autre
    type compatible, en préservant les propriétés du langage reconnu.
    """

    @abstractmethod
    def can_convert(
        self, source_type: AutomatonType, target_type: AutomatonType
    ) -> bool:
        """
        Vérifie si la conversion est possible.

        :param source_type: Type d'automate source
        :type source_type: AutomatonType
        :param target_type: Type d'automate cible
        :type target_type: AutomatonType
        :return: True si la conversion est possible, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def convert(self, automaton: IAutomaton, target_type: AutomatonType) -> IAutomaton:
        """
        Convertit un automate vers un autre type.

        :param automaton: Automate à convertir
        :type automaton: IAutomaton
        :param target_type: Type d'automate cible
        :type target_type: AutomatonType
        :return: Automate converti
        :rtype: IAutomaton
        :raises ConversionError: Si la conversion échoue
        """
        pass

    @abstractmethod
    def get_conversion_options(self, source_type: AutomatonType) -> List[AutomatonType]:
        """
        Retourne les types d'automates vers lesquels on peut convertir.

        :param source_type: Type d'automate source
        :type source_type: AutomatonType
        :return: Liste des types d'automates compatibles
        :rtype: List[AutomatonType]
        """
        pass

    @abstractmethod
    def get_conversion_info(
        self, source_type: AutomatonType, target_type: AutomatonType
    ) -> Dict[str, Any]:
        """
        Retourne des informations sur la conversion.

        :param source_type: Type d'automate source
        :type source_type: AutomatonType
        :param target_type: Type d'automate cible
        :type target_type: AutomatonType
        :return: Dictionnaire d'informations sur la conversion
        :rtype: Dict[str, Any]
        :raises ConversionError: Si la conversion n'est pas possible
        """
        pass
