"""
Interface abstraite pour les états d'automate.

Ce module définit l'interface IState et l'énumération StateType pour représenter
les états dans un automate.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict


class StateType(Enum):
    """
    Types d'états possibles dans un automate.

    Cette énumération définit les différents types d'états que peut avoir
    un automate selon sa nature et son rôle dans la reconnaissance.
    """

    INITIAL = "initial"
    """État initial de l'automate."""

    FINAL = "final"
    """État final de l'automate."""

    INTERMEDIATE = "intermediate"
    """État intermédiaire de l'automate."""

    ACCEPTING = "accepting"
    """État acceptant (peut être final ou intermédiaire)."""

    REJECTING = "rejecting"
    """État rejetant (pour certains types d'automates)."""


class IState(ABC):
    """
    Interface abstraite pour les états d'un automate.

    Cette interface définit le contrat que doivent respecter tous les états
    d'un automate, indépendamment de leur implémentation concrète.

    Un état est caractérisé par :
    - Un identifiant unique
    - Un type d'état
    - Des métadonnées optionnelles
    - Des méthodes de vérification de propriétés
    """

    @property
    @abstractmethod
    def identifier(self) -> str:
        """
        Identifiant unique de l'état.

        :return: Identifiant unique de l'état
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def state_type(self) -> StateType:
        """
        Type de l'état.

        :return: Type de l'état selon l'énumération StateType
        :rtype: StateType
        """
        pass

    @property
    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        """
        Métadonnées associées à l'état.

        :return: Dictionnaire des métadonnées de l'état
        :rtype: Dict[str, Any]
        """
        pass

    @abstractmethod
    def is_initial(self) -> bool:
        """
        Vérifie si l'état est initial.

        :return: True si l'état est initial, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_final(self) -> bool:
        """
        Vérifie si l'état est final.

        :return: True si l'état est final, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_accepting(self) -> bool:
        """
        Vérifie si l'état est acceptant.

        Un état acceptant peut être soit final, soit intermédiaire selon
        le type d'automate.

        :return: True si l'état est acceptant, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def add_metadata(self, key: str, value: Any) -> None:
        """
        Ajoute une métadonnée à l'état.

        :param key: Clé de la métadonnée
        :type key: str
        :param value: Valeur de la métadonnée
        :type value: Any
        :raises NotImplementedError: Si l'état est immuable
        """
        pass

    @abstractmethod
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Récupère une métadonnée de l'état.

        :param key: Clé de la métadonnée à récupérer
        :type key: str
        :param default: Valeur par défaut si la clé n'existe pas
        :type default: Any, optional
        :return: Valeur de la métadonnée ou valeur par défaut
        :rtype: Any
        """
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Comparaison d'égalité entre états.

        Deux états sont considérés égaux s'ils ont le même identifiant.

        :param other: Autre objet à comparer
        :type other: object
        :return: True si les états sont égaux, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def __hash__(self) -> int:
        """
        Hash de l'état pour utilisation dans des sets.

        :return: Valeur de hachage de l'état
        :rtype: int
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Représentation string de l'état.

        :return: Représentation string de l'état
        :rtype: str
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Représentation détaillée de l'état.

        :return: Représentation détaillée de l'état
        :rtype: str
        """
        pass
