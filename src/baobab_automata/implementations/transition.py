"""
Implémentation concrète de l'interface ITransition.

Ce module contient la classe Transition qui implémente l'interface ITransition
avec une approche immuable utilisant dataclass.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import copy
from types import MappingProxyType

from ..interfaces.state import IState
from ..interfaces.transition import ITransition, TransitionType


@dataclass(frozen=True)
class Transition(ITransition):
    """
    Implémentation concrète d'une transition d'automate.

    Cette classe implémente l'interface ITransition en utilisant un dataclass
    immuable. L'immutabilité garantit que les transitions ne peuvent pas être
    modifiées après leur création, évitant ainsi les effets de bord.

    :param source_state: État source de la transition
    :type source_state: IState
    :param target_state: État cible de la transition
    :type target_state: IState
    :param symbol: Symbole de la transition (None pour epsilon)
    :type symbol: Optional[str]
    :param transition_type: Type de la transition
    :type transition_type: TransitionType
    :param conditions: Conditions d'application de la transition
    :type conditions: Dict[str, Any]
    :param actions: Actions à exécuter lors de la transition
    :type actions: Dict[str, Any]
    """

    _source_state: IState
    _target_state: IState
    _symbol: Optional[str]
    _transition_type: TransitionType
    _conditions: Dict[str, Any] = field(default_factory=dict)
    _actions: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Créer des copies profondes des conditions et actions pour l'immutabilité."""
        if self._conditions is None:
            object.__setattr__(self, "_conditions", {})
        else:
            object.__setattr__(self, "_conditions", copy.deepcopy(self._conditions))

        if self._actions is None:
            object.__setattr__(self, "_actions", {})
        else:
            object.__setattr__(self, "_actions", copy.deepcopy(self._actions))

    @property
    def source_state(self) -> IState:
        """État source de la transition."""
        return self._source_state

    @property
    def target_state(self) -> IState:
        """État cible de la transition."""
        return self._target_state

    @property
    def symbol(self) -> Optional[str]:
        """Symbole de la transition."""
        return self._symbol

    @property
    def transition_type(self) -> TransitionType:
        """Type de la transition."""
        return self._transition_type

    @property
    def conditions(self) -> Dict[str, Any]:
        """Conditions de la transition."""
        return MappingProxyType(self._conditions)

    @property
    def actions(self) -> Dict[str, Any]:
        """Actions de la transition."""
        return MappingProxyType(self._actions)

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
        # Vérification du symbole
        if self._symbol is not None:
            # Transition symbolique : le symbole doit correspondre
            if self._symbol != symbol:
                return False
        else:
            # Transition epsilon : le symbole doit être None
            if symbol is not None:
                return False

        # Vérification des conditions
        for condition_key, condition_value in self._conditions.items():
            if context.get(condition_key) != condition_value:
                return False

        return True

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute la transition et retourne le nouveau contexte.

        :param context: Contexte d'exécution actuel
        :type context: Dict[str, Any]
        :return: Nouveau contexte après exécution de la transition
        :rtype: Dict[str, Any]
        """
        new_context = context.copy()

        # Exécution des actions
        for action_key, action_value in self._actions.items():
            new_context[action_key] = action_value

        return new_context

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
        if not isinstance(other, Transition):
            return False
        return (
            self._source_state == other._source_state
            and self._target_state == other._target_state
            and self._symbol == other._symbol
            and self._transition_type == other._transition_type
        )

    def __hash__(self) -> int:
        """
        Hash de la transition.

        :return: Valeur de hachage de la transition
        :rtype: int
        """
        return hash(
            (
                self._source_state,
                self._target_state,
                self._symbol,
                self._transition_type,
            )
        )

    def __str__(self) -> str:
        """
        Représentation string de la transition.

        :return: Représentation string de la transition
        :rtype: str
        """
        symbol_str = self._symbol if self._symbol is not None else "ε"
        return f"{self._source_state} --{symbol_str}--> {self._target_state}"
