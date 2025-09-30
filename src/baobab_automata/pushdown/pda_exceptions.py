"""
Exceptions personnalisées pour les automates à pile non-déterministes (PDA).

Ce module définit la hiérarchie d'exceptions spécifiques aux PDA,
permettant une gestion d'erreurs robuste et informative.
"""

from typing import Any, Optional


class PDAError(Exception):
    """Exception de base pour tous les problèmes liés aux PDA.

    Cette classe sert de classe parente pour toutes les exceptions
    spécifiques aux automates à pile non-déterministes.
    """

    def __init__(self, message: str, details: Optional[Any] = None) -> None:
        """Initialise l'exception avec un message et des détails optionnels.

        :param message: Message d'erreur descriptif
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Retourne la représentation textuelle de l'exception.

        :return: Message d'erreur avec détails si disponibles
        """
        if self.details is not None:
            return f"{self.message} (Détails: {self.details})"
        return self.message


class InvalidPDAError(PDAError):
    """Exception levée quand un PDA est invalide.

    Cette exception est levée lors de la validation d'un PDA
    qui ne respecte pas les contraintes de cohérence.
    """

    def __init__(self, message: str, validation_errors: Optional[list] = None) -> None:
        """Initialise l'exception avec les erreurs de validation.

        :param message: Message d'erreur principal
        :param validation_errors: Liste des erreurs de validation détectées
        """
        super().__init__(message, validation_errors)
        self.validation_errors = validation_errors or []


class InvalidStateError(PDAError):
    """Exception levée quand un état n'existe pas ou est invalide.

    Cette exception est levée quand une opération tente d'utiliser
    un état qui n'appartient pas à l'automate.
    """

    def __init__(self, state: str, message: Optional[str] = None) -> None:
        """Initialise l'exception avec l'état invalide.

        :param state: État invalide
        :param message: Message d'erreur personnalisé
        """
        if message is None:
            message = f"État invalide: '{state}'"
        super().__init__(message, state)
        self.state = state


class InvalidTransitionError(PDAError):
    """Exception levée quand une transition est invalide.

    Cette exception est levée quand une transition ne respecte pas
    les contraintes de l'automate (états inexistants, symboles invalides, etc.).
    """

    def __init__(self, transition: tuple, message: Optional[str] = None) -> None:
        """Initialise l'exception avec la transition invalide.

        :param transition: Transition invalide (état, symbole_entrée, symbole_pile)
        :param message: Message d'erreur personnalisé
        """
        if message is None:
            message = f"Transition invalide: {transition}"
        super().__init__(message, transition)
        self.transition = transition


class PDASimulationError(PDAError):
    """Exception levée lors d'erreurs de simulation.

    Cette exception est levée quand une erreur survient pendant
    la simulation de reconnaissance d'un mot.
    """

    def __init__(
        self,
        message: str,
        word: Optional[str] = None,
        configuration: Optional[Any] = None,
    ) -> None:
        """Initialise l'exception avec les détails de la simulation.

        :param message: Message d'erreur descriptif
        :param word: Mot en cours de simulation
        :param configuration: Configuration au moment de l'erreur
        """
        super().__init__(message, {"word": word, "configuration": configuration})
        self.word = word
        self.configuration = configuration


class PDAStackError(PDAError):
    """Exception levée lors d'erreurs de gestion de pile.

    Cette exception est levée quand une erreur survient lors
    de la manipulation de la pile (lecture, écriture, etc.).
    """

    def __init__(self, message: str, stack_state: Optional[str] = None) -> None:
        """Initialise l'exception avec l'état de la pile.

        :param message: Message d'erreur descriptif
        :param stack_state: État de la pile au moment de l'erreur
        """
        super().__init__(message, stack_state)
        self.stack_state = stack_state


class PDAValidationError(PDAError):
    """Exception levée lors d'erreurs de validation.

    Cette exception est levée quand la validation d'un PDA
    échoue pour des raisons spécifiques.
    """

    def __init__(self, message: str, validation_step: Optional[str] = None) -> None:
        """Initialise l'exception avec l'étape de validation.

        :param message: Message d'erreur descriptif
        :param validation_step: Étape de validation qui a échoué
        """
        super().__init__(message, validation_step)
        self.validation_step = validation_step


class PDAOperationError(PDAError):
    """Exception levée lors d'erreurs d'opérations sur les langages.

    Cette exception est levée quand une opération sur les langages
    (union, concaténation, étoile) échoue.
    """

    def __init__(self, operation: str, message: Optional[str] = None) -> None:
        """Initialise l'exception avec l'opération qui a échoué.

        :param operation: Nom de l'opération qui a échoué
        :param message: Message d'erreur personnalisé
        """
        if message is None:
            message = f"Erreur lors de l'opération '{operation}'"
        super().__init__(message, operation)
        self.operation = operation
