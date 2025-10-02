"""Exceptions personnalisées pour l'analyse de complexité."""


class ComplexityAnalysisError(Exception):
    """Exception de base pour les erreurs d'analyse de complexité."""

    pass


class InvalidComplexityAnalyzerError(ComplexityAnalysisError):
    """Exception pour analyseur de complexité invalide."""

    pass


class ComplexityAnalysisTimeoutError(ComplexityAnalysisError):
    """Exception pour timeout d'analyse."""

    pass


class ResourceMonitoringError(ComplexityAnalysisError):
    """Exception pour erreur de monitoring des ressources."""

    pass
