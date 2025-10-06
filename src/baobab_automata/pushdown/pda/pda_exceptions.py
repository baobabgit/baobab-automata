"""Exceptions pour les automates à pile non-déterministes."""

class PDAError(Exception):
    """Erreur générale de PDA."""
    def __init__(self, message: str):
        super().__init__(message)

class InvalidStateError(PDAError):
    """Erreur d'état invalide."""
    def __init__(self, state):
        super().__init__(f"État invalide: '{state}'")

class InvalidTransitionError(PDAError):
    """Erreur de transition invalide."""
    def __init__(self, transition, message=None):
        if message:
            super().__init__(message)
        else:
            super().__init__(f"Transition invalide: {transition}")

class PDAValidationError(PDAError):
    """Erreur de validation de PDA."""
    def __init__(self, message: str, field: str = None):
        super().__init__(message)
        self.field = field

class PDASimulationError(PDAError):
    """Erreur de simulation de PDA."""
    def __init__(self, message: str, word: str = None, configuration=None):
        super().__init__(message)
        self.word = word
        self.configuration = configuration

class PDAStackError(PDAError):
    """Erreur de pile de PDA."""
    pass

class PDAOperationError(PDAError):
    """Erreur d'opération de PDA."""
    def __init__(self, operation):
        super().__init__(f"Erreur lors de l'opération '{operation}'")

class InvalidPDAError(PDAError):
    """Erreur de PDA invalide."""
    pass