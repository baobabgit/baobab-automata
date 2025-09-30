"""
Exceptions de base pour Baobab Automata.

Ce module définit la hiérarchie des exceptions utilisées dans la bibliothèque.
"""


class BaobabAutomataError(Exception):
    """
    Exception de base pour toutes les erreurs de Baobab Automata.

    Cette classe sert de point d'entrée pour toutes les exceptions personnalisées
    de la bibliothèque, permettant une gestion centralisée des erreurs.

    :param message: Message d'erreur descriptif
    :type message: str
    :param details: Détails supplémentaires sur l'erreur
    :type details: dict, optional
    """

    def __init__(self, message: str, details: dict = None) -> None:
        """
        Initialise l'exception avec un message et des détails optionnels.

        :param message: Message d'erreur descriptif
        :param details: Détails supplémentaires sur l'erreur
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur formaté
        :rtype: str
        """
        if self.details:
            return f"{self.message} (Détails: {self.details})"
        return self.message


class InvalidAutomatonError(BaobabAutomataError):
    """
    Exception levée quand un automate est invalide.

    Cette exception est levée lors de la validation d'un automate qui ne respecte
    pas les contraintes de son type (ex: automate déterministe avec transitions
    non-déterministes).

    :param message: Message d'erreur descriptif
    :type message: str
    :param automaton_type: Type d'automate concerné
    :type automaton_type: str, optional
    :param validation_errors: Liste des erreurs de validation
    :type validation_errors: list, optional
    """

    def __init__(
        self,
        message: str,
        automaton_type: str = None,
        validation_errors: list = None,
    ) -> None:
        """
        Initialise l'exception d'automate invalide.

        :param message: Message d'erreur descriptif
        :param automaton_type: Type d'automate concerné
        :param validation_errors: Liste des erreurs de validation
        """
        details = {}
        if automaton_type:
            details["automaton_type"] = automaton_type
        if validation_errors:
            details["validation_errors"] = validation_errors

        super().__init__(message, details)
        self.automaton_type = automaton_type
        self.validation_errors = validation_errors or []


class InvalidStateError(BaobabAutomataError):
    """
    Exception levée quand un état est invalide.

    Cette exception est levée lors de la validation d'un état qui ne respecte
    pas les contraintes (ex: état sans identifiant, type d'état invalide).

    :param message: Message d'erreur descriptif
    :type message: str
    :param state_identifier: Identifiant de l'état concerné
    :type state_identifier: str, optional
    :param state_type: Type d'état concerné
    :type state_type: str, optional
    """

    def __init__(
        self,
        message: str,
        state_identifier: str = None,
        state_type: str = None,
    ) -> None:
        """
        Initialise l'exception d'état invalide.

        :param message: Message d'erreur descriptif
        :param state_identifier: Identifiant de l'état concerné
        :param state_type: Type d'état concerné
        """
        details = {}
        if state_identifier:
            details["state_identifier"] = state_identifier
        if state_type:
            details["state_type"] = state_type

        super().__init__(message, details)
        self.state_identifier = state_identifier
        self.state_type = state_type


class InvalidTransitionError(BaobabAutomataError):
    """
    Exception levée quand une transition est invalide.

    Cette exception est levée lors de la validation d'une transition qui ne
    respecte pas les contraintes (ex: transition sans état source/cible,
    symbole invalide).

    :param message: Message d'erreur descriptif
    :type message: str
    :param source_state: État source de la transition
    :type source_state: str, optional
    :param target_state: État cible de la transition
    :type target_state: str, optional
    :param symbol: Symbole de la transition
    :type symbol: str, optional
    """

    def __init__(
        self,
        message: str,
        source_state: str = None,
        target_state: str = None,
        symbol: str = None,
    ) -> None:
        """
        Initialise l'exception de transition invalide.

        :param message: Message d'erreur descriptif
        :param source_state: État source de la transition
        :param target_state: État cible de la transition
        :param symbol: Symbole de la transition
        """
        details = {}
        if source_state:
            details["source_state"] = source_state
        if target_state:
            details["target_state"] = target_state
        if symbol:
            details["symbol"] = symbol

        super().__init__(message, details)
        self.source_state = source_state
        self.target_state = target_state
        self.symbol = symbol


class ConversionError(BaobabAutomataError):
    """
    Exception levée quand une conversion d'automate échoue.

    Cette exception est levée lors de tentatives de conversion entre différents
    types d'automates qui ne sont pas compatibles ou qui échouent.

    :param message: Message d'erreur descriptif
    :type message: str
    :param source_type: Type d'automate source
    :type source_type: str, optional
    :param target_type: Type d'automate cible
    :type target_type: str, optional
    :param conversion_step: Étape de conversion où l'erreur s'est produite
    :type conversion_step: str, optional
    """

    def __init__(
        self,
        message: str,
        source_type: str = None,
        target_type: str = None,
        conversion_step: str = None,
    ) -> None:
        """
        Initialise l'exception de conversion.

        :param message: Message d'erreur descriptif
        :param source_type: Type d'automate source
        :param target_type: Type d'automate cible
        :param conversion_step: Étape de conversion où l'erreur s'est produite
        """
        details = {}
        if source_type:
            details["source_type"] = source_type
        if target_type:
            details["target_type"] = target_type
        if conversion_step:
            details["conversion_step"] = conversion_step

        super().__init__(message, details)
        self.source_type = source_type
        self.target_type = target_type
        self.conversion_step = conversion_step


class RecognitionError(BaobabAutomataError):
    """
    Exception levée quand la reconnaissance d'un mot échoue.

    Cette exception est levée lors d'erreurs dans le processus de reconnaissance
    d'un mot par un automate (ex: automate non initialisé, contexte invalide).

    :param message: Message d'erreur descriptif
    :type message: str
    :param word: Mot qui a causé l'erreur
    :type word: str, optional
    :param automaton_type: Type d'automate utilisé
    :type automaton_type: str, optional
    :param recognition_step: Étape de reconnaissance où l'erreur s'est produite
    :type recognition_step: str, optional
    """

    def __init__(
        self,
        message: str,
        word: str = None,
        automaton_type: str = None,
        recognition_step: str = None,
    ) -> None:
        """
        Initialise l'exception de reconnaissance.

        :param message: Message d'erreur descriptif
        :param word: Mot qui a causé l'erreur
        :param automaton_type: Type d'automate utilisé
        :param recognition_step: Étape de reconnaissance où l'erreur s'est produite
        """
        details = {}
        if word:
            details["word"] = word
        if automaton_type:
            details["automaton_type"] = automaton_type
        if recognition_step:
            details["recognition_step"] = recognition_step

        super().__init__(message, details)
        self.word = word
        self.automaton_type = automaton_type
        self.recognition_step = recognition_step
