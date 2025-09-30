"""
Exceptions spécifiques pour le parser d'expressions régulières.

Ce module définit les exceptions utilisées par le parser d'expressions régulières
et les opérations de conversion entre automates et expressions régulières.
"""

from ..exceptions.base import BaobabAutomataError


class RegexError(BaobabAutomataError):
    """
    Exception de base pour les erreurs de regex.

    Cette exception sert de point d'entrée pour toutes les erreurs liées
    aux expressions régulières dans la bibliothèque.

    :param message: Message d'erreur descriptif
    :type message: str
    :param position: Position dans l'expression où l'erreur s'est produite
    :type position: int, optional
    :param regex: Expression régulière qui a causé l'erreur
    :type regex: str, optional
    """

    def __init__(
        self,
        message: str,
        position: int = None,
        regex: str = None,
    ) -> None:
        """
        Initialise l'exception de regex.

        :param message: Message d'erreur descriptif
        :param position: Position dans l'expression où l'erreur s'est produite
        :param regex: Expression régulière qui a causé l'erreur
        """
        details = {}
        if position is not None:
            details["position"] = position
        if regex:
            details["regex"] = regex

        super().__init__(message, details)
        self.position = position
        self.regex = regex


class RegexSyntaxError(RegexError):
    """
    Exception levée quand une erreur de syntaxe est détectée dans une expression régulière.

    Cette exception est levée lors de la validation syntaxique d'une expression
    régulière qui ne respecte pas la grammaire définie.

    :param message: Message d'erreur descriptif
    :type message: str
    :param position: Position dans l'expression où l'erreur s'est produite
    :type position: int, optional
    :param regex: Expression régulière qui a causé l'erreur
    :type regex: str, optional
    :param expected: Caractère ou token attendu
    :type expected: str, optional
    :param found: Caractère ou token trouvé
    :type found: str, optional
    """

    def __init__(
        self,
        message: str,
        position: int = None,
        regex: str = None,
        expected: str = None,
        found: str = None,
    ) -> None:
        """
        Initialise l'exception de syntaxe regex.

        :param message: Message d'erreur descriptif
        :param position: Position dans l'expression où l'erreur s'est produite
        :param regex: Expression régulière qui a causé l'erreur
        :param expected: Caractère ou token attendu
        :param found: Caractère ou token trouvé
        """
        details = {}
        if position is not None:
            details["position"] = position
        if regex:
            details["regex"] = regex
        if expected:
            details["expected"] = expected
        if found:
            details["found"] = found

        super().__init__(message, position, regex)
        self.expected = expected
        self.found = found


class RegexParseError(RegexError):
    """
    Exception levée quand le parsing d'une expression régulière échoue.

    Cette exception est levée lors d'erreurs dans le processus de parsing
    d'une expression régulière (ex: parenthèses non équilibrées, opérateurs mal placés).

    :param message: Message d'erreur descriptif
    :type message: str
    :param position: Position dans l'expression où l'erreur s'est produite
    :type position: int, optional
    :param regex: Expression régulière qui a causé l'erreur
    :type regex: str, optional
    :param parse_step: Étape de parsing où l'erreur s'est produite
    :type parse_step: str, optional
    """

    def __init__(
        self,
        message: str,
        position: int = None,
        regex: str = None,
        parse_step: str = None,
    ) -> None:
        """
        Initialise l'exception de parsing regex.

        :param message: Message d'erreur descriptif
        :param position: Position dans l'expression où l'erreur s'est produite
        :param regex: Expression régulière qui a causé l'erreur
        :param parse_step: Étape de parsing où l'erreur s'est produite
        """
        details = {}
        if position is not None:
            details["position"] = position
        if regex:
            details["regex"] = regex
        if parse_step:
            details["parse_step"] = parse_step

        super().__init__(message, position, regex)
        self.parse_step = parse_step


class RegexConversionError(RegexError):
    """
    Exception levée quand la conversion entre automate et expression régulière échoue.

    Cette exception est levée lors d'erreurs dans les conversions bidirectionnelles
    entre automates et expressions régulières.

    :param message: Message d'erreur descriptif
    :type message: str
    :param automaton_type: Type d'automate concerné
    :type automaton_type: str, optional
    :param conversion_direction: Direction de la conversion (automate→regex ou regex→automate)
    :type conversion_direction: str, optional
    :param conversion_step: Étape de conversion où l'erreur s'est produite
    :type conversion_step: str, optional
    """

    def __init__(
        self,
        message: str,
        automaton_type: str = None,
        conversion_direction: str = None,
        conversion_step: str = None,
    ) -> None:
        """
        Initialise l'exception de conversion regex.

        :param message: Message d'erreur descriptif
        :param automaton_type: Type d'automate concerné
        :param conversion_direction: Direction de la conversion
        :param conversion_step: Étape de conversion où l'erreur s'est produite
        """
        details = {}
        if automaton_type:
            details["automaton_type"] = automaton_type
        if conversion_direction:
            details["conversion_direction"] = conversion_direction
        if conversion_step:
            details["conversion_step"] = conversion_step

        super().__init__(message)
        self.automaton_type = automaton_type
        self.conversion_direction = conversion_direction
        self.conversion_step = conversion_step