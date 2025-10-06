"""Exceptions pour le parser d'expressions régulières."""

class RegexError(Exception):
    """Erreur générale d'expression régulière."""
    def __init__(self, message: str, regex: str = None):
        super().__init__(message)
        self.regex = regex

class RegexParseError(RegexError):
    """Erreur de parsing d'expression régulière."""
    def __init__(self, message: str, regex: str = None):
        super().__init__(message, regex)

class RegexSyntaxError(RegexError):
    """Erreur de syntaxe d'expression régulière."""
    def __init__(self, message: str, position: int = None, regex: str = None):
        super().__init__(message, regex)
        self.position = position

class RegexConversionError(RegexError):
    """Erreur de conversion d'expression régulière."""
    def __init__(self, message: str, regex: str = None, conversion_step: str = None):
        super().__init__(message, regex)
        self.conversion_step = conversion_step