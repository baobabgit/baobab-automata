"""
Interface abstraite pour les automates à pile.

Ce module définit l'interface commune pour tous les types d'automates à pile,
fournissant un contrat uniforme pour les opérations de base.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Set, Tuple


class AbstractPushdownAutomaton(ABC):
    """Interface abstraite pour les automates à pile.

    Cette classe définit le contrat commun pour tous les types d'automates à pile
    (PDA, DPDA, NPDA), garantissant une interface uniforme et cohérente.
    """

    @property
    @abstractmethod
    def states(self) -> Set[str]:
        """Retourne l'ensemble des états de l'automate.

        :return: Ensemble des états
        """
        pass

    @property
    @abstractmethod
    def input_alphabet(self) -> Set[str]:
        """Retourne l'alphabet d'entrée de l'automate.

        :return: Alphabet d'entrée
        """
        pass

    @property
    @abstractmethod
    def stack_alphabet(self) -> Set[str]:
        """Retourne l'alphabet de pile de l'automate.

        :return: Alphabet de pile
        """
        pass

    @property
    @abstractmethod
    def initial_state(self) -> str:
        """Retourne l'état initial de l'automate.

        :return: État initial
        """
        pass

    @property
    @abstractmethod
    def initial_stack_symbol(self) -> str:
        """Retourne le symbole initial de pile.

        :return: Symbole initial de pile
        """
        pass

    @property
    @abstractmethod
    def final_states(self) -> Set[str]:
        """Retourne l'ensemble des états finaux.

        :return: États finaux
        """
        pass

    @abstractmethod
    def accepts(self, word: str) -> bool:
        """Vérifie si un mot est accepté par l'automate.

        :param word: Mot à tester
        :return: True si le mot est accepté, False sinon
        """
        pass

    @abstractmethod
    def get_transitions(
        self, state: str, input_symbol: str, stack_symbol: str
    ) -> Set[Tuple[str, str]]:
        """Récupère les transitions possibles depuis un état donné.

        :param state: État source
        :param input_symbol: Symbole d'entrée (peut être ε)
        :param stack_symbol: Symbole de pile
        :return: Ensemble des transitions possibles (état_destination, symboles_pile)
        """
        pass

    @abstractmethod
    def is_final_state(self, state: str) -> bool:
        """Vérifie si un état est final.

        :param state: État à vérifier
        :return: True si l'état est final, False sinon
        """
        pass

    @abstractmethod
    def get_reachable_states(self, from_state: str) -> Set[str]:
        """Récupère tous les états accessibles depuis un état donné.

        :param from_state: État de départ
        :return: Ensemble des états accessibles
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Valide la cohérence de l'automate.

        :return: True si l'automate est valide, False sinon
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'automate en dictionnaire.

        :return: Représentation dictionnaire de l'automate
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AbstractPushdownAutomaton":
        """Crée un automate à partir d'un dictionnaire.

        :param data: Données de l'automate
        :return: Instance de l'automate
        """
        pass

    def __str__(self) -> str:
        """Retourne la représentation textuelle de l'automate.

        :return: Représentation textuelle
        """
        return (
            f"{self.__class__.__name__}("
            f"states={len(self.states)}, "
            f"input_alphabet={self.input_alphabet}, "
            f"stack_alphabet={self.stack_alphabet}, "
            f"initial_state='{self.initial_state}', "
            f"final_states={self.final_states})"
        )

    def __repr__(self) -> str:
        """Retourne la représentation technique de l'automate.

        :return: Représentation technique pour le débogage
        """
        return (
            f"{self.__class__.__name__}("
            f"states={self.states}, "
            f"input_alphabet={self.input_alphabet}, "
            f"stack_alphabet={self.stack_alphabet}, "
            f"transitions=..., "
            f"initial_state='{self.initial_state}', "
            f"initial_stack_symbol='{self.initial_stack_symbol}', "
            f"final_states={self.final_states})"
        )
