"""
Interface abstraite pour les automates.

Ce module définit l'interface IAutomaton et l'énumération AutomatonType pour
représenter les différents types d'automates.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from .state import IState
from .transition import ITransition


class AutomatonType(Enum):
    """
    Types d'automates supportés par la bibliothèque.

    Cette énumération définit tous les types d'automates que peut gérer
    la bibliothèque Baobab Automata.
    """

    # Automates finis
    DFA = "dfa"
    """Automate fini déterministe."""

    NFA = "nfa"
    """Automate fini non-déterministe."""

    EPSILON_NFA = "epsilon_nfa"
    """Automate fini non-déterministe avec transitions epsilon."""

    # Automates à pile
    PDA = "pda"
    """Automate à pile (Pushdown Automaton)."""

    DPDA = "dpda"
    """Automate à pile déterministe."""

    NPDA = "npda"
    """Automate à pile non-déterministe."""

    # Machines de Turing
    TM = "tm"
    """Machine de Turing."""

    DTM = "dtm"
    """Machine de Turing déterministe."""

    NTM = "ntm"
    """Machine de Turing non-déterministe."""

    MULTI_TAPE_TM = "multi_tape_tm"
    """Machine de Turing multi-bandes."""


class IAutomaton(ABC):
    """
    Interface abstraite pour tous les types d'automates.

    Cette interface définit le contrat que doivent respecter tous les
    automates de la bibliothèque, indépendamment de leur type et de leur
    implémentation concrète.

    Un automate est caractérisé par :
    - Un type d'automate
    - Un ensemble d'états
    - Des états initiaux et finaux
    - Un alphabet de symboles
    - Un ensemble de transitions
    """

    @property
    @abstractmethod
    def automaton_type(self) -> AutomatonType:
        """
        Type de l'automate.

        :return: Type de l'automate selon l'énumération AutomatonType
        :rtype: AutomatonType
        """
        pass

    @property
    @abstractmethod
    def states(self) -> Set[IState]:
        """
        Ensemble des états de l'automate.

        :return: Ensemble de tous les états de l'automate
        :rtype: Set[IState]
        """
        pass

    @property
    @abstractmethod
    def initial_states(self) -> Set[IState]:
        """
        Ensemble des états initiaux.

        :return: Ensemble des états initiaux de l'automate
        :rtype: Set[IState]
        """
        pass

    @property
    @abstractmethod
    def final_states(self) -> Set[IState]:
        """
        Ensemble des états finaux.

        :return: Ensemble des états finaux de l'automate
        :rtype: Set[IState]
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
    def transitions(self) -> Set[ITransition]:
        """
        Ensemble des transitions de l'automate.

        :return: Ensemble de toutes les transitions de l'automate
        :rtype: Set[ITransition]
        """
        pass

    @abstractmethod
    def add_state(self, state: IState) -> None:
        """
        Ajoute un état à l'automate.

        :param state: État à ajouter
        :type state: IState
        :raises InvalidStateError: Si l'état est invalide
        """
        pass

    @abstractmethod
    def remove_state(self, state: IState) -> None:
        """
        Supprime un état de l'automate.

        :param state: État à supprimer
        :type state: IState
        :raises InvalidStateError: Si l'état n'existe pas
        """
        pass

    @abstractmethod
    def add_transition(self, transition: ITransition) -> None:
        """
        Ajoute une transition à l'automate.

        :param transition: Transition à ajouter
        :type transition: ITransition
        :raises InvalidTransitionError: Si la transition est invalide
        """
        pass

    @abstractmethod
    def remove_transition(self, transition: ITransition) -> None:
        """
        Supprime une transition de l'automate.

        :param transition: Transition à supprimer
        :type transition: ITransition
        :raises InvalidTransitionError: Si la transition n'existe pas
        """
        pass

    @abstractmethod
    def get_transitions_from(self, state: IState) -> Set[ITransition]:
        """
        Récupère les transitions partant d'un état.

        :param state: État source
        :type state: IState
        :return: Ensemble des transitions partant de l'état
        :rtype: Set[ITransition]
        :raises InvalidStateError: Si l'état n'existe pas
        """
        pass

    @abstractmethod
    def get_transitions_to(self, state: IState) -> Set[ITransition]:
        """
        Récupère les transitions arrivant à un état.

        :param state: État cible
        :type state: IState
        :return: Ensemble des transitions arrivant à l'état
        :rtype: Set[ITransition]
        :raises InvalidStateError: Si l'état n'existe pas
        """
        pass

    @abstractmethod
    def get_transitions(
        self, source: IState, symbol: Optional[str]
    ) -> Set[ITransition]:
        """
        Récupère les transitions pour un état et un symbole donnés.

        :param source: État source
        :type source: IState
        :param symbol: Symbole de la transition (None pour epsilon)
        :type symbol: Optional[str]
        :return: Ensemble des transitions correspondantes
        :rtype: Set[ITransition]
        :raises InvalidStateError: Si l'état n'existe pas
        """
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Vérifie si l'automate est valide.

        :return: True si l'automate est valide, False sinon
        :rtype: bool
        """
        pass

    @abstractmethod
    def validate(self) -> List[str]:
        """
        Valide l'automate et retourne la liste des erreurs.

        :return: Liste des erreurs de validation (vide si valide)
        :rtype: List[str]
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

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Désérialise l'automate depuis un dictionnaire.

        :param data: Dictionnaire représentant l'automate
        :type data: Dict[str, Any]
        :raises InvalidAutomatonError: Si les données sont invalides
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Représentation string de l'automate.

        :return: Représentation string de l'automate
        :rtype: str
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Représentation détaillée de l'automate.

        :return: Représentation détaillée de l'automate
        :rtype: str
        """
        pass
