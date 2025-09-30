
"""
Module d'analyse des dépendances pour les composants de la phase 2.

Ce module fournit des outils pour analyser les dépendances entre les composants
de la phase 2 du projet Baobab Automata, déterminer l'ordre optimal de développement
et identifier les composants qui peuvent être développés en parallèle.

Classes:
DependencyAnalyzer: Analyseur principal des dépendances entre composants.
ComponentDependency: Représentation d'une dépendance entre composants.
DevelopmentPhase: Représentation d'une phase de développement.
ComponentStatus: Statut d'un composant dans le cycle de développement.

Exemples:
>>> analyzer = DependencyAnalyzer()
>>> dependencies = analyzer.analyze_dependencies()
>>> optimal_order = analyzer.get_optimal_development_order()
>>> parallel_components = analyzer.get_parallel_components()
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict, deque

from baobab_automata.exceptions.base import BaobabAutomataError


class ComponentStatus(Enum):
    """Statut d'un composant dans le cycle de développement."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


    @dataclass
    class ComponentDependency:
        """
        Représentation d'une dépendance entre composants.

        Attributes:
        source: Composant source de la dépendance.
        target: Composant cible de la dépendance.
        dependency_type: Type de dépendance (interface, implementation, etc.).
        priority: Priorité de la dépendance (1 = critique, 5 = optionnelle).
        description: Description de la dépendance.
        """

        source: str
        target: str
        dependency_type: str
        priority: int = 1
        description: str = ""


        @dataclass
        class DevelopmentPhase:
            """
            Représentation d'une phase de développement.

            Attributes:
            name: Nom de la phase.
            components: Liste des composants de cette phase.
            can_parallelize: Indique si les composants peuvent être développés en parallèle.
            estimated_duration: Durée estimée en jours.
            dependencies: Dépendances de cette phase.
            """

            name: str
            components: List[str] = field(default_factory=list)
            can_parallelize: bool = False
            estimated_duration: int = 0
            dependencies: List[str] = field(default_factory=list)


            class DependencyAnalysisError(BaobabAutomataError):
                """Exception levée lors d'erreurs dans l'analyse des dépendances."""
                pass


                class DependencyAnalyzer:
                    """
                    Analyseur des dépendances entre composants de la phase 2.

                    Cette classe fournit des méthodes pour analyser les dépendances entre
                    les composants de la phase 2, déterminer l'ordre optimal de développement
                    et identifier les composants qui peuvent être développés en parallèle.

                    Attributes:
                    components: Dictionnaire des composants et leurs métadonnées.
                    dependencies: Liste des dépendances entre composants.
                    phases: Liste des phases de développement.
                    component_status: Statut actuel de chaque composant.
                    """

                    def __init__(self):
                        """Initialise l'analyseur de dépendances."""
                        self.components: Dict[str, Dict[str, Any]] = {}
                        self.dependencies: List[ComponentDependency] = []
                        self.phases: List[DevelopmentPhase] = []
                        self.component_status: Dict[str, ComponentStatus] = {}

                        self._initialize_components()
                        self._initialize_dependencies()
                        self._initialize_phases()
                        self._initialize_status()

                        def _initialize_components(self) -> None:
                            """
                            Initialise les composants de la phase 2 avec leurs métadonnées.

                            Raises:
                            DependencyAnalysisError: Si l'initialisation échoue.
                            """
                            try:
                                self.components = {
                                "DFA": {
                                "name": "Deterministic Finite Automaton",
                                "priority": 1,
                                "estimated_duration": 3,
                                "dependencies": [],
                                "dependents": ["NFA", "ε-NFA", "RegexParser",
                                "ConversionAlgorithms",
                                "OptimizationAlgorithms", "LanguageOperations"],
                                "performance_targets": {
                                "execution_time": 100, # ms
                                "memory_usage": 1, # MB
                                "max_states": 100
                                },
                                "test_coverage_target": 95
                                },
                                "NFA": {
                                "name": "Non-deterministic Finite Automaton",
                                "priority": 2,
                                "estimated_duration": 3,
                                "dependencies": ["DFA"],
                                "dependents": ["ε-NFA", "ConversionAlgorithms",
                                "OptimizationAlgorithms",
                                "LanguageOperations"],
                                "performance_targets": {
                                "execution_time": 50, # ms
                                "memory_usage": 2, # MB
                                "max_states": 100
                                },
                                "test_coverage_target": 95
                                },
                                "ε-NFA": {
                                "name": "NFA with epsilon transitions",
                                "priority": 3,
                                "estimated_duration": 3,
                                "dependencies": ["NFA", "DFA"],
                                "dependents": ["RegexParser", "ConversionAlgorithms",
                                "OptimizationAlgorithms",
                                "LanguageOperations"],
                                "performance_targets": {
                                "execution_time": 100, # ms
                                "memory_usage": 3, # MB
                                "max_states": 100
                                },
                                "test_coverage_target": 95
                                },
                                "RegexParser": {
                                "name": "Regular Expression Parser",
                                "priority": 4,
                                "estimated_duration": 4,
                                "dependencies": ["DFA", "NFA", "ε-NFA"],
                                "dependents": ["ConversionAlgorithms"],
                                "performance_targets": {
                                "execution_time": 10, # ms
                                "memory_usage": 1, # MB
                                "max_expression_length": 1000
                                },
                                "test_coverage_target": 95
                                },
                                "ConversionAlgorithms": {
                                "name": "Conversion Algorithms",
                                "priority": 5,
                                "estimated_duration": 4,
                                "dependencies": ["DFA", "NFA", "ε-NFA", "RegexParser"],
                                "dependents": [],
                                "performance_targets": {
                                "execution_time": 500, # ms
                                "memory_usage": 10, # MB
                                "max_states": 20
                                },
                                "test_coverage_target": 95
                                },
                                "OptimizationAlgorithms": {
                                "name": "Optimization Algorithms",
                                "priority": 6,
                                "estimated_duration": 3,
                                "dependencies": ["DFA", "NFA", "ε-NFA"],
                                "dependents": [],
                                "performance_targets": {
                                "execution_time": 100, # ms
                                "memory_usage": 5, # MB
                                "max_states": 1000
                                },
                                "test_coverage_target": 95
                                },
                                "LanguageOperations": {
                                "name": "Language Operations",
                                "priority": 7,
                                "estimated_duration": 3,
                                "dependencies": ["DFA", "NFA", "ε-NFA"],
                                "dependents": [],
                                "performance_targets": {
                                "execution_time": 50, # ms
                                "memory_usage": 10, # MB
                                "max_states": 1000
                                },
                                "test_coverage_target": 95
                                }
                                }
                                except Exception as e:
                                    raise DependencyAnalysisError(f"Erreur lors de l'initialisation des
                                    composants: {e}")

                                    def _initialize_dependencies(self) -> None:
                                        """
                                        Initialise les dépendances entre composants.

                                        Raises:
                                        DependencyAnalysisError: Si l'initialisation échoue.
                                        """
                                        try:
                                            self.dependencies = [
                                            # Dépendances DFA
                                            ComponentDependency("NFA", "DFA", "interface", 1, "NFA utilise DFA pour
                                            les conversions"),
                                            ComponentDependency("ε-NFA", "DFA", "interface", 1, "ε-NFA utilise DFA
                                            pour les conversions"),
                                            ComponentDependency("RegexParser", "DFA", "implementation", 1,
                                            "RegexParser construit des DFA"),
                                            ComponentDependency("ConversionAlgorithms", "DFA", "implementation", 1,
                                            "ConversionAlgorithms convertit vers/depuis DFA"),
                                            ComponentDependency("OptimizationAlgorithms", "DFA", "implementation",
                                            1, "OptimizationAlgorithms optimise les DFA"),
                                            ComponentDependency("LanguageOperations", "DFA", "implementation", 1,
                                            "LanguageOperations opère sur les DFA"),

                                            # Dépendances NFA
                                            ComponentDependency("ε-NFA", "NFA", "interface", 1, "ε-NFA étend NFA"),
                                            ComponentDependency("ConversionAlgorithms", "NFA", "implementation", 1,
                                            "ConversionAlgorithms convertit vers/depuis NFA"),
                                            ComponentDependency("OptimizationAlgorithms", "NFA", "implementation",
                                            1, "OptimizationAlgorithms optimise les NFA"),
                                            ComponentDependency("LanguageOperations", "NFA", "implementation", 1,
                                            "LanguageOperations opère sur les NFA"),

                                            # Dépendances ε-NFA
                                            ComponentDependency("RegexParser", "ε-NFA", "implementation", 1,
                                            "RegexParser construit des ε-NFA"),
                                            ComponentDependency("ConversionAlgorithms", "ε-NFA", "implementation",
                                            1, "ConversionAlgorithms convertit vers/depuis ε-NFA"),
                                            ComponentDependency("OptimizationAlgorithms", "ε-NFA",
                                            "implementation", 1, "OptimizationAlgorithms optimise les ε-NFA"),
                                            ComponentDependency("LanguageOperations", "ε-NFA", "implementation", 1,
                                            "LanguageOperations opère sur les ε-NFA"),

                                            # Dépendances RegexParser
                                            ComponentDependency("ConversionAlgorithms", "RegexParser", "interface",
                                            1, "ConversionAlgorithms utilise RegexParser"),
                                            ]
                                            except Exception as e:
                                                raise DependencyAnalysisError(f"Erreur lors de l'initialisation des
                                                dépendances: {e}")

                                                def _initialize_phases(self) -> None:
                                                    """
                                                    Initialise les phases de développement.

                                                    Raises:
                                                    DependencyAnalysisError: Si l'initialisation échoue.
                                                    """
                                                    try:
                                                        self.phases = [
                                                        DevelopmentPhase(
                                                        name="Phase 2A: Classes de Base",
                                                        components=["DFA", "NFA", "ε-NFA"],
                                                        can_parallelize=False,
                                                        estimated_duration=9,
                                                        dependencies=[]
                                                        ),
                                                        DevelopmentPhase(
                                                        name="Phase 2B: Parser et Conversions",
                                                        components=["RegexParser", "ConversionAlgorithms"],
                                                        can_parallelize=True,
                                                        estimated_duration=4,
                                                        dependencies=["Phase 2A"]
                                                        ),
                                                        DevelopmentPhase(
                                                        name="Phase 2C: Optimisations et Opérations",
                                                        components=["OptimizationAlgorithms", "LanguageOperations"],
                                                        can_parallelize=True,
                                                        estimated_duration=3,
                                                        dependencies=["Phase 2A"]
                                                        )
                                                        ]
                                                        except Exception as e:
                                                            raise DependencyAnalysisError(f"Erreur lors de l'initialisation des phases:
                                                            {e}")

                                                            def _initialize_status(self) -> None:
                                                                """
                                                                Initialise le statut des composants.

                                                                Raises:
                                                                DependencyAnalysisError: Si l'initialisation échoue.
                                                                """
                                                                try:
                                                                    for component in self.components:
                                                                        self.component_status[component] = ComponentStatus.NOT_STARTED
                                                                        except Exception as e:
                                                                            raise DependencyAnalysisError(f"Erreur lors de l'initialisation du statut:
                                                                            {e}")

                                                                            def analyze_dependencies(self) -> Dict[str, Any]:
                                                                                """
                                                                                Analyse les dépendances entre tous les composants.

                                                                                Returns:
                                                                                Dictionnaire contenant l'analyse des dépendances avec:
                                                                                - dependency_graph: Graphe des dépendances
                                                                                - critical_path: Chemin critique de développement
                                                                                - parallel_opportunities: Opportunités de développement parallèle
                                                                                - risk_analysis: Analyse des risques

                                                                                Raises:
                                                                                DependencyAnalysisError: Si l'analyse échoue.
                                                                                """
                                                                                try:
                                                                                    start_time = time.time()

                                                                                    # Construire le graphe des dépendances
                                                                                    dependency_graph = self._build_dependency_graph()

                                                                                    # Calculer le chemin critique
                                                                                    critical_path = self._calculate_critical_path(dependency_graph)

                                                                                    # Identifier les opportunités de développement parallèle
                                                                                    parallel_opportunities = self._identify_parallel_opportunities(dependency_graph)

                                                                                    # Analyser les risques
                                                                                    risk_analysis = self._analyze_risks(dependency_graph)

                                                                                    # Calculer les métriques de performance
                                                                                    performance_metrics = self._calculate_performance_metrics()

                                                                                    analysis_time = time.time() - start_time

                                                                                    return {
                                                                                    "dependency_graph": dependency_graph,
                                                                                    "critical_path": critical_path,
                                                                                    "parallel_opportunities": parallel_opportunities,
                                                                                    "risk_analysis": risk_analysis,
                                                                                    "performance_metrics": performance_metrics,
                                                                                    "analysis_time": analysis_time,
                                                                                    "total_components": len(self.components),
                                                                                    "total_dependencies": len(self.dependencies)
                                                                                    }
                                                                                    except Exception as e:
                                                                                        raise DependencyAnalysisError(f"Erreur lors de l'analyse des dépendances:
                                                                                        {e}")

                                                                                        def _build_dependency_graph(self) -> Dict[str, List[str]]:
                                                                                            """
                                                                                            Construit le graphe des dépendances.

                                                                                            Returns:
                                                                                            Dictionnaire représentant le graphe des dépendances.
                                                                                            """
                                                                                            graph = defaultdict(list)

                                                                                            for dependency in self.dependencies:
                                                                                                graph[dependency.target].append(dependency.source)

                                                                                                return dict(graph)

                                                                                                def _calculate_critical_path(self, dependency_graph: Dict[str, List[str]]) ->
                                                                                                List[str]:
                                                                                                """
                                                                                                Calcule le chemin critique de développement.

                                                                                                Args:
                                                                                                dependency_graph: Graphe des dépendances.

                                                                                                Returns:
                                                                                                Liste des composants dans l'ordre du chemin critique.
                                                                                                """
                                                                                                # Utiliser l'algorithme de tri topologique
                                                                                                in_degree = defaultdict(int)
                                                                                                for component in self.components:
                                                                                                    in_degree[component] = 0

                                                                                                    for dependency in self.dependencies:
                                                                                                        in_degree[dependency.source] += 1

                                                                                                        queue = deque([comp for comp in self.components if in_degree[comp] == 0])
                                                                                                        critical_path = []

                                                                                                        while queue:
                                                                                                            current = queue.popleft()
                                                                                                            critical_path.append(current)

                                                                                                            # Mettre à jour les degrés d'entrée
                                                                                                            for dependency in self.dependencies:
                                                                                                                if dependency.target == current:
                                                                                                                    in_degree[dependency.source] -= 1
                                                                                                                    if in_degree[dependency.source] == 0:
                                                                                                                        queue.append(dependency.source)

                                                                                                                        return critical_path

                                                                                                                        def _identify_parallel_opportunities(self, dependency_graph: Dict[str, List[str]])
                                                                                                                        -> Dict[str, List[str]]:
                                                                                                                        """
                                                                                                                        Identifie les opportunités de développement parallèle.

                                                                                                                        Args:
                                                                                                                        dependency_graph: Graphe des dépendances.

                                                                                                                        Returns:
                                                                                                                        Dictionnaire des composants qui peuvent être développés en parallèle.
                                                                                                                        """
                                                                                                                        parallel_opportunities = defaultdict(list)

                                                                                                                        # Grouper les composants par niveau de dépendance
                                                                                                                        levels = self._calculate_dependency_levels(dependency_graph)

                                                                                                                        for level, components in levels.items():
                                                                                                                            if len(components) > 1:
                                                                                                                                parallel_opportunities[f"Level {level}"] = components

                                                                                                                                return dict(parallel_opportunities)

                                                                                                                                def _calculate_dependency_levels(self, dependency_graph: Dict[str, List[str]]) ->
                                                                                                                                Dict[int, List[str]]:
                                                                                                                                """
                                                                                                                                Calcule les niveaux de dépendance des composants.

                                                                                                                                Args:
                                                                                                                                dependency_graph: Graphe des dépendances.

                                                                                                                                Returns:
                                                                                                                                Dictionnaire des niveaux de dépendance.
                                                                                                                                """
                                                                                                                                levels = defaultdict(list)
                                                                                                                                visited = set()

                                                                                                                                def dfs(component: str, level: int = 0) -> int:
                                                                                                                                    if component in visited:
                                                                                                                                        return level

                                                                                                                                        visited.add(component)
                                                                                                                                        max_level = level

                                                                                                                                        for dependency in dependency_graph.get(component, []):
                                                                                                                                            dep_level = dfs(dependency, level + 1)
                                                                                                                                            max_level = max(max_level, dep_level)

                                                                                                                                            levels[max_level].append(component)
                                                                                                                                            return max_level

                                                                                                                                            for component in self.components:
                                                                                                                                                if component not in visited:
                                                                                                                                                    dfs(component)

                                                                                                                                                    return dict(levels)

                                                                                                                                                    def _analyze_risks(self, dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
                                                                                                                                                        """
                                                                                                                                                        Analyse les risques de développement.

                                                                                                                                                        Args:
                                                                                                                                                        dependency_graph: Graphe des dépendances.

                                                                                                                                                        Returns:
                                                                                                                                                        Dictionnaire contenant l'analyse des risques.
                                                                                                                                                        """
                                                                                                                                                        risks = {
                                                                                                                                                        "high_dependency_components": [],
                                                                                                                                                        "circular_dependencies": [],
                                                                                                                                                        "performance_risks": [],
                                                                                                                                                        "complexity_risks": []
                                                                                                                                                        }

                                                                                                                                                        # Identifier les composants avec beaucoup de dépendances
                                                                                                                                                        for component, deps in dependency_graph.items():
                                                                                                                                                            if len(deps) > 3:
                                                                                                                                                                risks["high_dependency_components"].append({
                                                                                                                                                                "component": component,
                                                                                                                                                                "dependency_count": len(deps),
                                                                                                                                                                "dependencies": deps
                                                                                                                                                                })

                                                                                                                                                                # Vérifier les dépendances circulaires
                                                                                                                                                                risks["circular_dependencies"] = self._detect_circular_dependencies(dependency_graph)

                                                                                                                                                                # Analyser les risques de performance
                                                                                                                                                                for component, metadata in self.components.items():
                                                                                                                                                                    perf_targets = metadata.get("performance_targets", {})
                                                                                                                                                                    if perf_targets.get("execution_time", 0) > 200:
                                                                                                                                                                        risks["performance_risks"].append({
                                                                                                                                                                        "component": component,
                                                                                                                                                                        "risk": "High execution time target",
                                                                                                                                                                        "target": perf_targets["execution_time"]
                                                                                                                                                                        })

                                                                                                                                                                        return risks

                                                                                                                                                                        def _detect_circular_dependencies(self, dependency_graph: Dict[str, List[str]]) ->
                                                                                                                                                                        List[List[str]]:
                                                                                                                                                                        """
                                                                                                                                                                        Détecte les dépendances circulaires.

                                                                                                                                                                        Args:
                                                                                                                                                                        dependency_graph: Graphe des dépendances.

                                                                                                                                                                        Returns:
                                                                                                                                                                        Liste des cycles détectés.
                                                                                                                                                                        """
                                                                                                                                                                        cycles = []
                                                                                                                                                                        visited = set()
                                                                                                                                                                        rec_stack = set()

                                                                                                                                                                        def dfs(component: str, path: List[str]) -> None:
                                                                                                                                                                            if component in rec_stack:
                                                                                                                                                                                # Cycle détecté
                                                                                                                                                                                cycle_start = path.index(component)
                                                                                                                                                                                cycles.append(path[cycle_start:] + [component])
                                                                                                                                                                                return

                                                                                                                                                                                if component in visited:
                                                                                                                                                                                    return

                                                                                                                                                                                    visited.add(component)
                                                                                                                                                                                    rec_stack.add(component)
                                                                                                                                                                                    path.append(component)

                                                                                                                                                                                    for dependency in dependency_graph.get(component, []):
                                                                                                                                                                                        dfs(dependency, path.copy())

                                                                                                                                                                                        rec_stack.remove(component)
                                                                                                                                                                                        path.pop()

                                                                                                                                                                                        for component in self.components:
                                                                                                                                                                                            if component not in visited:
                                                                                                                                                                                                dfs(component, [])

                                                                                                                                                                                                return cycles

                                                                                                                                                                                                def _calculate_performance_metrics(self) -> Dict[str, Any]:
                                                                                                                                                                                                    """
                                                                                                                                                                                                    Calcule les métriques de performance du projet.

                                                                                                                                                                                                    Returns:
                                                                                                                                                                                                    Dictionnaire contenant les métriques de performance.
                                                                                                                                                                                                    """
                                                                                                                                                                                                    total_duration = sum(phase.estimated_duration for phase in self.phases)
                                                                                                                                                                                                    parallel_phases = sum(1 for phase in self.phases if phase.can_parallelize)

                                                                                                                                                                                                    return {
                                                                                                                                                                                                    "total_estimated_duration": total_duration,
                                                                                                                                                                                                    "parallel_phases": parallel_phases,
                                                                                                                                                                                                    "sequential_phases": len(self.phases) - parallel_phases,
                                                                                                                                                                                                    "efficiency_gain": self._calculate_efficiency_gain(),
                                                                                                                                                                                                    "resource_utilization": self._calculate_resource_utilization()
                                                                                                                                                                                                    }

                                                                                                                                                                                                    def _calculate_efficiency_gain(self) -> float:
                                                                                                                                                                                                        """
                                                                                                                                                                                                        Calcule le gain d'efficacité du développement parallèle.

                                                                                                                                                                                                        Returns:
                                                                                                                                                                                                        Gain d'efficacité en pourcentage.
                                                                                                                                                                                                        """
                                                                                                                                                                                                        sequential_duration = sum(comp["estimated_duration"] for comp in
                                                                                                                                                                                                        self.components.values())
                                                                                                                                                                                                        parallel_duration = sum(phase.estimated_duration for phase in self.phases)

                                                                                                                                                                                                        if sequential_duration == 0:
                                                                                                                                                                                                            return 0.0

                                                                                                                                                                                                            return ((sequential_duration - parallel_duration) / sequential_duration) * 100

                                                                                                                                                                                                            def _calculate_resource_utilization(self) -> Dict[str, float]:
                                                                                                                                                                                                                """
                                                                                                                                                                                                                Calcule l'utilisation des ressources.

                                                                                                                                                                                                                Returns:
                                                                                                                                                                                                                Dictionnaire contenant les métriques d'utilisation des ressources.
                                                                                                                                                                                                                """
                                                                                                                                                                                                                total_components = len(self.components)
                                                                                                                                                                                                                parallel_components = sum(
                                                                                                                                                                                                                len(phase.components) for phase in self.phases if phase.can_parallelize
                                                                                                                                                                                                                )

                                                                                                                                                                                                                return {
                                                                                                                                                                                                                "parallel_utilization": (parallel_components / total_components) * 100,
                                                                                                                                                                                                                "sequential_utilization": ((total_components - parallel_components) /
                                                                                                                                                                                                                total_components) * 100
                                                                                                                                                                                                                }

                                                                                                                                                                                                                def get_optimal_development_order(self) -> List[DevelopmentPhase]:
                                                                                                                                                                                                                    """
                                                                                                                                                                                                                    Détermine l'ordre optimal de développement.

                                                                                                                                                                                                                    Returns:
                                                                                                                                                                                                                    Liste des phases de développement dans l'ordre optimal.

                                                                                                                                                                                                                    Raises:
                                                                                                                                                                                                                    DependencyAnalysisError: Si la détermination échoue.
                                                                                                                                                                                                                    """
                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                        # Trier les phases par priorité et dépendances
                                                                                                                                                                                                                        sorted_phases = sorted(
                                                                                                                                                                                                                        self.phases,
                                                                                                                                                                                                                        key=lambda phase: (
                                                                                                                                                                                                                        len(phase.dependencies), # Moins de dépendances en premier
                                                                                                                                                                                                                        phase.estimated_duration # Durée plus courte en premier
                                                                                                                                                                                                                        )
                                                                                                                                                                                                                        )

                                                                                                                                                                                                                        return sorted_phases
                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                            raise DependencyAnalysisError(f"Erreur lors de la détermination de l'ordre
                                                                                                                                                                                                                            optimal: {e}")

                                                                                                                                                                                                                            def get_parallel_components(self) -> Dict[str, List[str]]:
                                                                                                                                                                                                                                """
                                                                                                                                                                                                                                Identifie les composants qui peuvent être développés en parallèle.

                                                                                                                                                                                                                                Returns:
                                                                                                                                                                                                                                Dictionnaire des composants parallélisables par phase.

                                                                                                                                                                                                                                Raises:
                                                                                                                                                                                                                                DependencyAnalysisError: Si l'identification échoue.
                                                                                                                                                                                                                                """
                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                    parallel_components = {}

                                                                                                                                                                                                                                    for phase in self.phases:
                                                                                                                                                                                                                                        if phase.can_parallelize:
                                                                                                                                                                                                                                            parallel_components[phase.name] = phase.components

                                                                                                                                                                                                                                            return parallel_components
                                                                                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                                                                                raise DependencyAnalysisError(f"Erreur lors de l'identification des
                                                                                                                                                                                                                                                composants parallèles: {e}")

                                                                                                                                                                                                                                                def get_component_dependencies(self, component: str) -> List[ComponentDependency]:
                                                                                                                                                                                                                                                    """
                                                                                                                                                                                                                                                    Obtient les dépendances d'un composant spécifique.

                                                                                                                                                                                                                                                    Args:
                                                                                                                                                                                                                                                    component: Nom du composant.

                                                                                                                                                                                                                                                    Returns:
                                                                                                                                                                                                                                                    Liste des dépendances du composant.

                                                                                                                                                                                                                                                    Raises:
                                                                                                                                                                                                                                                    DependencyAnalysisError: Si le composant n'existe pas.
                                                                                                                                                                                                                                                    """
                                                                                                                                                                                                                                                    if component not in self.components:
                                                                                                                                                                                                                                                        raise DependencyAnalysisError(f"Composant '{component}' non trouvé")

                                                                                                                                                                                                                                                        return [
                                                                                                                                                                                                                                                        dep for dep in self.dependencies
                                                                                                                                                                                                                                                        if dep.source == component
                                                                                                                                                                                                                                                        ]

                                                                                                                                                                                                                                                        def get_component_dependents(self, component: str) -> List[ComponentDependency]:
                                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                                            Obtient les composants qui dépendent d'un composant spécifique.

                                                                                                                                                                                                                                                            Args:
                                                                                                                                                                                                                                                            component: Nom du composant.

                                                                                                                                                                                                                                                            Returns:
                                                                                                                                                                                                                                                            Liste des composants dépendants.

                                                                                                                                                                                                                                                            Raises:
                                                                                                                                                                                                                                                            DependencyAnalysisError: Si le composant n'existe pas.
                                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                                            if component not in self.components:
                                                                                                                                                                                                                                                                raise DependencyAnalysisError(f"Composant '{component}' non trouvé")

                                                                                                                                                                                                                                                                return [
                                                                                                                                                                                                                                                                dep for dep in self.dependencies
                                                                                                                                                                                                                                                                if dep.target == component
                                                                                                                                                                                                                                                                ]

                                                                                                                                                                                                                                                                def update_component_status(self, component: str, status: ComponentStatus) -> None:
                                                                                                                                                                                                                                                                    """
                                                                                                                                                                                                                                                                    Met à jour le statut d'un composant.

                                                                                                                                                                                                                                                                    Args:
                                                                                                                                                                                                                                                                    component: Nom du composant.
                                                                                                                                                                                                                                                                    status: Nouveau statut du composant.

                                                                                                                                                                                                                                                                    Raises:
                                                                                                                                                                                                                                                                    DependencyAnalysisError: Si le composant n'existe pas.
                                                                                                                                                                                                                                                                    """
                                                                                                                                                                                                                                                                    if component not in self.components:
                                                                                                                                                                                                                                                                        raise DependencyAnalysisError(f"Composant '{component}' non trouvé")

                                                                                                                                                                                                                                                                        self.component_status[component] = status

                                                                                                                                                                                                                                                                        def get_development_roadmap(self) -> Dict[str, Any]:
                                                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                                                            Génère une feuille de route de développement complète.

                                                                                                                                                                                                                                                                            Returns:
                                                                                                                                                                                                                                                                            Dictionnaire contenant la feuille de route de développement.

                                                                                                                                                                                                                                                                            Raises:
                                                                                                                                                                                                                                                                            DependencyAnalysisError: Si la génération échoue.
                                                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                analysis = self.analyze_dependencies()
                                                                                                                                                                                                                                                                                optimal_order = self.get_optimal_development_order()
                                                                                                                                                                                                                                                                                parallel_components = self.get_parallel_components()

                                                                                                                                                                                                                                                                                return {
                                                                                                                                                                                                                                                                                "analysis": analysis,
                                                                                                                                                                                                                                                                                "optimal_order": optimal_order,
                                                                                                                                                                                                                                                                                "parallel_components": parallel_components,
                                                                                                                                                                                                                                                                                "recommendations": self._generate_recommendations(),
                                                                                                                                                                                                                                                                                "timeline": self._generate_timeline()
                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                                                                                                                    raise DependencyAnalysisError(f"Erreur lors de la génération de la feuille
                                                                                                                                                                                                                                                                                    de route: {e}")

                                                                                                                                                                                                                                                                                    def _generate_recommendations(self) -> List[str]:
                                                                                                                                                                                                                                                                                        """
                                                                                                                                                                                                                                                                                        Génère des recommandations pour le développement.

                                                                                                                                                                                                                                                                                        Returns:
                                                                                                                                                                                                                                                                                        Liste des recommandations.
                                                                                                                                                                                                                                                                                        """
                                                                                                                                                                                                                                                                                        recommendations = [
                                                                                                                                                                                                                                                                                        "Commencer par le développement séquentiel des classes de base (DFA, NFA,
                                                                                                                                                                                                                                                                                        ε-NFA)",
                                                                                                                                                                                                                                                                                        "Développer RegexParser et ConversionAlgorithms en parallèle après les
                                                                                                                                                                                                                                                                                        classes de base",
                                                                                                                                                                                                                                                                                        "Développer OptimizationAlgorithms et LanguageOperations en parallèle",
                                                                                                                                                                                                                                                                                        "Implémenter les tests unitaires en même temps que le code",
                                                                                                                                                                                                                                                                                        "Surveiller les performances et respecter les objectifs définis",
                                                                                                                                                                                                                                                                                        "Maintenir une couverture de tests >= 95%",
                                                                                                                                                                                                                                                                                        "Documenter le code au fur et à mesure du développement"
                                                                                                                                                                                                                                                                                        ]

                                                                                                                                                                                                                                                                                        return recommendations

                                                                                                                                                                                                                                                                                        def _generate_timeline(self) -> Dict[str, Any]:
                                                                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                                                                            Génère une timeline de développement.

                                                                                                                                                                                                                                                                                            Returns:
                                                                                                                                                                                                                                                                                            Dictionnaire contenant la timeline.
                                                                                                                                                                                                                                                                                            """
                                                                                                                                                                                                                                                                                            timeline = {
                                                                                                                                                                                                                                                                                            "total_duration": sum(phase.estimated_duration for phase in self.phases),
                                                                                                                                                                                                                                                                                            "phases": []
                                                                                                                                                                                                                                                                                            }

                                                                                                                                                                                                                                                                                            current_week = 1
                                                                                                                                                                                                                                                                                            current_day = 1

                                                                                                                                                                                                                                                                                            for phase in self.phases:
                                                                                                                                                                                                                                                                                                phase_info = {
                                                                                                                                                                                                                                                                                                "name": phase.name,
                                                                                                                                                                                                                                                                                                "duration": phase.estimated_duration,
                                                                                                                                                                                                                                                                                                "start_week": current_week,
                                                                                                                                                                                                                                                                                                "start_day": current_day,
                                                                                                                                                                                                                                                                                                "components": phase.components,
                                                                                                                                                                                                                                                                                                "can_parallelize": phase.can_parallelize
                                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                                                                timeline["phases"].append(phase_info)

                                                                                                                                                                                                                                                                                                # Mettre à jour la position pour la phase suivante
                                                                                                                                                                                                                                                                                                if phase.can_parallelize:
                                                                                                                                                                                                                                                                                                    current_day += phase.estimated_duration
                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                    current_day += phase.estimated_duration

                                                                                                                                                                                                                                                                                                    if current_day > 7:
                                                                                                                                                                                                                                                                                                        current_week += 1
                                                                                                                                                                                                                                                                                                        current_day = current_day % 7

                                                                                                                                                                                                                                                                                                        return timeline
