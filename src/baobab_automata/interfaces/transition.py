"""
Interface abstraite pour les transitions d'automate.

Ce module définit l'interface ITransition et l'énumération TransitionType pour
représenter les transitions dans un automate.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional

from .state import IState


class TransitionType(Enum):
    """
    Types de transitions possibles dans un automate.

    Cette énumération définit les différents types de transitions selon
    le type d'automate et les opérations qu'elles effectuent.
    """

    SYMBOL = "symbol"
    """Transition symbolique classique (lecture d'un symbole)."""

    EPSILON = "epsilon"
    """Transition epsilon (sans lecture de symbole)."""

    STACK_PUSH = "stack_push"
    """Transition de pile : empile un symbole."""

    STACK_POP = "stack_pop"
    """Transition de pile : dépile un symbole."""

    STACK_READ = "stack_read"
    """Transition de pile : lit le sommet de la pile."""

    TAPE_READ = "tape_read"
    """Transition de bande : lit le symbole sous la tête."""

    TAPE_WRITE = "tape_write"
    """Transition de bande : écrit un symbole sur la bande."""

    TAPE_MOVE = "tape_move"
    """Transition de bande : déplace la tête de lecture."""


class ITransition(ABC):
    """
    Interface abstraite pour les transitions d'un automate.

    Cette interface définit le contrat que doivent respecter toutes les
    transitions d'un automate, indépendamment de leur implémentation concrète.

    Une transition est caractérisée par :
    - Un état source
    - Un état cible
    - Un symbole (optionnel pour les transitions epsilon)
    - Un type de transition
    - Des conditions d'application
    - Des actions à exécuter
    """

    @property
    @abstractmethod
    def source_state(self) -> IState:
        """
        État source de la transition.

        :return: État d'où part la transition
        :rtype: IState
        """
        pass

    @property
    @abstractmethod
    def target_state(self) -> IState:
        """
        État cible de la transition.

        :return: État vers lequel va la transition
        :rtype: IState
        """
        pass

    @property
    @abstractmethod
    def symbol(self) -> Optional[str]:
        """
        Symbole de la transition.

        :return: Symbole de la transition (None pour epsilon)
        :rtype: Optional[str]
        """
        pass

    @property
    @abstractmethod
    def transition_type(self) -> TransitionType:
        """
        Type de la transition.

        :return: Type de la transition selon l'énumération TransitionType
        :rtype: TransitionType
        """
        pass

    @property
    @abstractmethod
    def conditions(self) -> Dict[str, Any]:
        """
        Conditions de la transition.

        :return: Dictionnaire des conditions d'application de la transition
        :rtype: Dict[str, Any]
        """
        pass

    @property
    @abstractmethod
    def actions(self) -> Dict[str, Any]:
        """
        Actions de la transition.

        :return: Dictionnaire des actions à exécuter lors de la transition
        :rtype: Dict[str, Any]
        """
        pass

    @abstractmethod
    def is_applicable(self, symbol: Optional[str], context: Dict[str, Any]) -> bool:
        """
        Vérifie si la transition est applicable.

        :param symbol: Symbole à lire (None pour epsilon)
        :type symbol: Optional[str]
        :param context: Contexte d'exécution de l'automate
        :type context: Dict[str, Any]
        :return: True si la transition est applicable, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute la transition et retourne le nouveau contexte.

        :param context: Contexte d'exécution actuel
        :type context: Dict[str, Any]
        :return: Nouveau contexte après exécution de la transition
        :rtype: Dict[str, Any]
        """
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Comparaison d'égalité entre transitions.

        Deux transitions sont considérées égales si elles ont les mêmes
        états source et cible, le même symbole et le même type.

        :param other: Autre objet à comparer
        :type other: object
        :return: True si les transitions sont égales, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def __hash__(self) -> int:
        """
        Hash de la transition.

        :return: Valeur de hachage de la transition
        :rtype: int
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Représentation string de la transition.

        :return: Représentation string de la transition
        :rtype: str
        """
        pass
