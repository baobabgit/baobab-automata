"""
Classe pour représenter les changements de transitions.

Ce module définit la classe TransitionChange qui représente un changement
de transition dans un automate, utilisé pour les optimisations incrémentales.
"""

from typing import Any


class TransitionChange:
    """
    Représente un changement de transition dans un automate.

    Cette classe est utilisée pour représenter les modifications
    apportées aux transitions d'un automate lors des optimisations
    incrémentales.

    :param state: État source de la transition
    :type state: str
    :param symbol: Symbole de la transition
    :type symbol: str
    :param old_target: Ancien état de destination
    :type old_target: str
    :param new_target: Nouvel état de destination
    :type new_target: str
    """

    def __init__(
        self, state: str, symbol: str, old_target: str, new_target: str
    ) -> None:
        """
        Initialise un changement de transition.

        :param state: État source de la transition
        :type state: str
        :param symbol: Symbole de la transition
        :type symbol: str
        :param old_target: Ancien état de destination
        :type old_target: str
        :param new_target: Nouvel état de destination
        :type new_target: str
        :raises ValueError: Si les paramètres sont invalides
        """
        if not state or not symbol:
            raise ValueError("L'état et le symbole ne peuvent pas être vides")

        self._state = state
        self._symbol = symbol
        self._old_target = old_target
        self._new_target = new_target

    @property
    def state(self) -> str:
        """
        État source de la transition.

        :return: Identifiant de l'état source
        :rtype: str
        """
        return self._state

    @property
    def symbol(self) -> str:
        """
        Symbole de la transition.

        :return: Symbole de la transition
        :rtype: str
        """
        return self._symbol

    @property
    def old_target(self) -> str:
        """
        Ancien état de destination.

        :return: Identifiant de l'ancien état de destination
        :rtype: str
        """
        return self._old_target

    @property
    def new_target(self) -> str:
        """
        Nouvel état de destination.

        :return: Identifiant du nouvel état de destination
        :rtype: str
        """
        return self._new_target

    def __repr__(self) -> str:
        """
        Représentation string du changement de transition.

        :return: Représentation string
        :rtype: str
        """
        return f"TransitionChange(state='{self._state}', symbol='{self._symbol}', old_target='{self._old_target}', new_target='{self._new_target}')"

    def __eq__(self, other: Any) -> bool:
        """
        Vérifie l'égalité avec un autre objet.

        :param other: Autre objet à comparer
        :type other: Any
        :return: True si les objets sont égaux
        :rtype: bool
        """
        if not isinstance(other, TransitionChange):
            return False

        return (
            self._state == other._state
            and self._symbol == other._symbol
            and self._old_target == other._old_target
            and self._new_target == other._new_target
        )

    def __hash__(self) -> int:
        """
        Calcule le hash du changement de transition.

        :return: Hash du changement de transition
        :rtype: int
        """
        return hash((self._state, self._symbol, self._old_target, self._new_target))

    def is_addition(self) -> bool:
        """
        Vérifie si c'est une addition de transition.

        :return: True si c'est une addition (old_target est None)
        :rtype: bool
        """
        return self._old_target is None

    def is_removal(self) -> bool:
        """
        Vérifie si c'est une suppression de transition.

        :return: True si c'est une suppression (new_target est None)
        :rtype: bool
        """
        return self._new_target is None

    def is_modification(self) -> bool:
        """
        Vérifie si c'est une modification de transition.

        :return: True si c'est une modification (ni addition ni suppression)
        :rtype: bool
        """
        return not self.is_addition() and not self.is_removal()
