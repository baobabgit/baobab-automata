"""
Module algorithms - Algorithmes pour les automates.

Ce module contient les algorithmes de conversion, d'optimisation
et de reconnaissance pour les différents types d'automates.
"""

from .dependency_analysis import (
    DependencyAnalyzer,
    ComponentDependency,
    DevelopmentPhase,
    ComponentStatus,
    DependencyAnalysisError,
)

__all__ = [
    "DependencyAnalyzer",
    "ComponentDependency",
    "DevelopmentPhase",
    "ComponentStatus",
    "DependencyAnalysisError",
]
