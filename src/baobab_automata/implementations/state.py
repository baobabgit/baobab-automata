"""
Implémentation concrète de l'interface IState.

Ce module contient la classe State qui implémente l'interface IState
avec une approche immuable utilisant dataclass.
"""

from dataclasses import dataclass, field
from typing import Any, Dict
import copy
from types import MappingProxyType

from ..interfaces.state import IState, StateType


@dataclass(frozen=True)
class State(IState):
    """
    Implémentation concrète d'un état d'automate.

    Cette classe implémente l'interface IState en utilisant un dataclass
    immuable. L'immutabilité garantit que les états ne peuvent pas être
    modifiés après leur création, évitant ainsi les effets de bord.

    :param identifier: Identifiant unique de l'état
    :type identifier: str
    :param state_type: Type de l'état
    :type state_type: StateType
    :param metadata: Métadonnées associées à l'état
    :type metadata: Dict[str, Any]
    """

    _identifier: str
    _state_type: StateType
    _metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Créer une copie profonde des métadonnées pour l'immutabilité."""
        if self._metadata is None:
            object.__setattr__(self, "_metadata", {})
        else:
            object.__setattr__(self, "_metadata", copy.deepcopy(self._metadata))

    @property
    def identifier(self) -> str:
        """Identifiant unique de l'état."""
        return self._identifier

    @property
    def state_type(self) -> StateType:
        """Type de l'état."""
        return self._state_type

    @property
    def metadata(self) -> Dict[str, Any]:
        """Métadonnées associées à l'état."""
        return MappingProxyType(self._metadata)

    def is_initial(self) -> bool:
        """
        Vérifie si l'état est initial.

        :return: True si l'état est initial, False sinon
        :rtype: bool
        """
        return self._state_type == StateType.INITIAL

    def is_final(self) -> bool:
        """
        Vérifie si l'état est final.

        :return: True si l'état est final, False sinon
        :rtype: bool
        """
        return self._state_type == StateType.FINAL

    def is_accepting(self) -> bool:
        """
        Vérifie si l'état est acceptant.

        Un état acceptant peut être soit final, soit intermédiaire selon
        le type d'automate.

        :return: True si l'état est acceptant, False sinon
        :rtype: bool
        """
        return self._state_type in {StateType.FINAL, StateType.ACCEPTING}

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Ajoute une métadonnée à l'état.

        Note: Cette méthode ne peut pas être implémentée avec @dataclass(frozen=True).
        Une implémentation alternative sera nécessaire pour les cas où la
        modification des métadonnées est requise.

        :param key: Clé de la métadonnée
        :type key: str
        :param value: Valeur de la métadonnée
        :type value: Any
        :raises NotImplementedError: Car l'état est immuable
        """
        raise NotImplementedError(
            "Cannot modify frozen dataclass. Use StateBuilder for mutable states."
        )

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
        return self._metadata.get(key, default)

    def __eq__(self, other: object) -> bool:
        """
        Comparaison d'égalité entre états.

        Deux états sont considérés égaux s'ils ont le même identifiant et le même type.

        :param other: Autre objet à comparer
        :type other: object
        :return: True si les états sont égaux, False sinon
        :rtype: bool
        """
        if not isinstance(other, State):
            return False
        return (
            self._identifier == other._identifier
            and self._state_type == other._state_type
        )

    def __hash__(self) -> int:
        """
        Hash de l'état pour utilisation dans des sets.

        :return: Valeur de hachage de l'état
        :rtype: int
        """
        return hash((self._identifier, self._state_type))

    def __str__(self) -> str:
        """
        Représentation string de l'état.

        :return: Représentation string de l'état
        :rtype: str
        """
        return f"State({self._identifier})"

    def __repr__(self) -> str:
        """
        Représentation détaillée de l'état.

        :return: Représentation détaillée de l'état
        :rtype: str
        """
        return f"State(identifier='{self._identifier}', type={self._state_type})"
