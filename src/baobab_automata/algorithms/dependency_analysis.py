"""
Module d'analyse des dépendances pour la phase 2 du projet Baobab Automata.

Ce module fournit des outils pour analyser les dépendances entre les composants
de la phase 2 et optimiser l'ordre de développement.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
import time
from collections import defaultdict, deque


class ComponentStatus(Enum):
    """Statuts possibles d'un composant."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass
class ComponentDependency:
    """Représente une dépendance entre deux composants."""

    source: str
    target: str
    dependency_type: str
    priority: int = 1
    description: str = ""

    def __post_init__(self):
        """Validation après initialisation."""
        if not self.source or not self.target:
            raise ValueError("Source et target ne peuvent pas être vides")
        if self.source == self.target:
            raise ValueError("Un composant ne peut pas dépendre de lui-même")


@dataclass
class DevelopmentPhase:
    """Représente une phase de développement."""

    name: str
    components: List[str] = None
    can_parallelize: bool = False
    estimated_duration: int = 0
    dependencies: List[str] = None

    def __post_init__(self):
        """Initialisation des valeurs par défaut."""
        if self.components is None:
            self.components = []
        if self.dependencies is None:
            self.dependencies = []


class DependencyAnalysisError(Exception):
    """Exception levée lors d'erreurs dans l'analyse des dépendances."""


class DependencyAnalyzer:
    """Analyseur de dépendances pour optimiser le développement."""

    def __init__(self):
        """Initialise l'analyseur de dépendances."""
        self.components: Dict[str, Dict[str, Any]] = {}
        self.dependencies: List[ComponentDependency] = []
        self.phases: List[DevelopmentPhase] = []
        self.component_status: Dict[str, ComponentStatus] = {}

        self._initialize_components()
        self._initialize_dependencies()
        self._initialize_phases()

    def _initialize_components(self) -> None:
        """Initialise les composants de la phase 2 avec leurs métadonnées."""
        try:
            self.components = {
                "DFA": {
                    "name": "Deterministic Finite Automaton",
                    "priority": 1,
                    "estimated_duration": 3,
                    "dependencies": [],
                    "dependents": [
                        "NFA",
                        "ε-NFA",
                        "RegexParser",
                        "ConversionAlgorithms",
                        "OptimizationAlgorithms",
                        "LanguageOperations",
                    ],
                    "performance_targets": {
                        "execution_time": 10,  # ms
                        "memory_usage": 1,  # MB
                        "max_states": 100,
                    },
                    "test_coverage_target": 95,
                },
                "NFA": {
                    "name": "Non-deterministic Finite Automaton",
                    "priority": 2,
                    "estimated_duration": 3,
                    "dependencies": ["DFA"],
                    "dependents": [
                        "ε-NFA",
                        "RegexParser",
                        "ConversionAlgorithms",
                        "OptimizationAlgorithms",
                        "LanguageOperations",
                    ],
                    "performance_targets": {
                        "execution_time": 20,  # ms
                        "memory_usage": 2,  # MB
                        "max_states": 100,
                    },
                    "test_coverage_target": 95,
                },
                "ε-NFA": {
                    "name": "NFA with epsilon transitions",
                    "priority": 3,
                    "estimated_duration": 3,
                    "dependencies": ["NFA", "DFA"],
                    "dependents": [
                        "RegexParser",
                        "ConversionAlgorithms",
                        "OptimizationAlgorithms",
                        "LanguageOperations",
                    ],
                    "performance_targets": {
                        "execution_time": 100,  # ms
                        "memory_usage": 3,  # MB
                        "max_states": 100,
                    },
                    "test_coverage_target": 95,
                },
                "RegexParser": {
                    "name": "Regular Expression Parser",
                    "priority": 4,
                    "estimated_duration": 4,
                    "dependencies": ["DFA", "NFA", "ε-NFA"],
                    "dependents": ["ConversionAlgorithms"],
                    "performance_targets": {
                        "execution_time": 10,  # ms
                        "memory_usage": 1,  # MB
                        "max_expression_length": 1000,
                    },
                    "test_coverage_target": 95,
                },
                "ConversionAlgorithms": {
                    "name": "Conversion Algorithms",
                    "priority": 5,
                    "estimated_duration": 4,
                    "dependencies": ["DFA", "NFA", "ε-NFA", "RegexParser"],
                    "dependents": [],
                    "performance_targets": {
                        "execution_time": 500,  # ms
                        "memory_usage": 10,  # MB
                        "max_states": 20,
                    },
                    "test_coverage_target": 95,
                },
                "OptimizationAlgorithms": {
                    "name": "Optimization Algorithms",
                    "priority": 6,
                    "estimated_duration": 3,
                    "dependencies": ["DFA", "NFA", "ε-NFA"],
                    "dependents": [],
                    "performance_targets": {
                        "execution_time": 100,  # ms
                        "memory_usage": 5,  # MB
                        "max_states": 1000,
                    },
                    "test_coverage_target": 95,
                },
                "LanguageOperations": {
                    "name": "Language Operations",
                    "priority": 7,
                    "estimated_duration": 3,
                    "dependencies": ["DFA", "NFA", "ε-NFA"],
                    "dependents": [],
                    "performance_targets": {
                        "execution_time": 50,  # ms
                        "memory_usage": 10,  # MB
                        "max_states": 1000,
                    },
                    "test_coverage_target": 95,
                },
            }
        except Exception as e:
            raise DependencyAnalysisError(
                f"Erreur lors de l'initialisation des composants: {e}"
            ) from e

    def _initialize_dependencies(self) -> None:
        """Initialise les dépendances entre composants."""
        try:
            self.dependencies = [
                # Dépendances DFA
                ComponentDependency(
                    "NFA", "DFA", "interface", 1, "NFA utilise DFA pour les conversions"
                ),
                ComponentDependency(
                    "ε-NFA",
                    "DFA",
                    "interface",
                    1,
                    "ε-NFA utilise DFA pour les conversions",
                ),
                ComponentDependency(
                    "RegexParser",
                    "DFA",
                    "implementation",
                    1,
                    "RegexParser construit des DFA",
                ),
                ComponentDependency(
                    "ConversionAlgorithms",
                    "DFA",
                    "implementation",
                    1,
                    "ConversionAlgorithms convertit vers/depuis DFA",
                ),
                ComponentDependency(
                    "OptimizationAlgorithms",
                    "DFA",
                    "implementation",
                    1,
                    "OptimizationAlgorithms optimise les DFA",
                ),
                ComponentDependency(
                    "LanguageOperations",
                    "DFA",
                    "implementation",
                    1,
                    "LanguageOperations opère sur les DFA",
                ),
                # Dépendances NFA
                ComponentDependency("ε-NFA", "NFA", "interface", 1, "ε-NFA étend NFA"),
                ComponentDependency(
                    "ConversionAlgorithms",
                    "NFA",
                    "implementation",
                    1,
                    "ConversionAlgorithms convertit vers/depuis NFA",
                ),
                ComponentDependency(
                    "OptimizationAlgorithms",
                    "NFA",
                    "implementation",
                    1,
                    "OptimizationAlgorithms optimise les NFA",
                ),
                ComponentDependency(
                    "LanguageOperations",
                    "NFA",
                    "implementation",
                    1,
                    "LanguageOperations opère sur les NFA",
                ),
                # Dépendances ε-NFA
                ComponentDependency(
                    "RegexParser",
                    "ε-NFA",
                    "implementation",
                    1,
                    "RegexParser utilise ε-NFA",
                ),
                ComponentDependency(
                    "ConversionAlgorithms",
                    "ε-NFA",
                    "implementation",
                    1,
                    "ConversionAlgorithms convertit vers/depuis ε-NFA",
                ),
                ComponentDependency(
                    "OptimizationAlgorithms",
                    "ε-NFA",
                    "implementation",
                    1,
                    "OptimizationAlgorithms optimise les ε-NFA",
                ),
                ComponentDependency(
                    "LanguageOperations",
                    "ε-NFA",
                    "implementation",
                    1,
                    "LanguageOperations opère sur les ε-NFA",
                ),
                # Dépendances RegexParser
                ComponentDependency(
                    "ConversionAlgorithms",
                    "RegexParser",
                    "implementation",
                    1,
                    "ConversionAlgorithms utilise RegexParser",
                ),
            ]

            # Initialiser les statuts des composants
            for component in self.components:
                self.component_status[component] = ComponentStatus.NOT_STARTED

        except Exception as e:
            raise DependencyAnalysisError(
                f"Erreur lors de l'initialisation des dépendances: {e}"
            ) from e

    def _initialize_phases(self) -> None:
        """Initialise les phases de développement."""
        try:
            self.phases = [
                DevelopmentPhase(
                    name="Phase 2A: Classes de Base",
                    components=["DFA", "NFA", "ε-NFA"],
                    can_parallelize=False,
                    estimated_duration=6,
                    dependencies=[],
                ),
                DevelopmentPhase(
                    name="Phase 2B: Parser et Conversion",
                    components=["RegexParser", "ConversionAlgorithms"],
                    can_parallelize=True,
                    estimated_duration=4,
                    dependencies=["Phase 2A"],
                ),
                DevelopmentPhase(
                    name="Phase 2C: Optimisation et Opérations",
                    components=["OptimizationAlgorithms", "LanguageOperations"],
                    can_parallelize=True,
                    estimated_duration=3,
                    dependencies=["Phase 2A"],
                ),
            ]
        except Exception as e:
            raise DependencyAnalysisError(
                f"Erreur lors de l'initialisation des phases: {e}"
            ) from e

    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analyse les dépendances et retourne un rapport complet."""
        start_time = time.time()

        try:
            # Construire le graphe des dépendances
            dependency_graph = self._build_dependency_graph()

            # Calculer le chemin critique
            critical_path = self._calculate_critical_path(dependency_graph)

            # Identifier les opportunités de parallélisation
            parallel_opportunities = self._identify_parallel_opportunities(
                dependency_graph
            )

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
                "total_dependencies": len(self.dependencies),
            }
        except Exception as e:
            raise DependencyAnalysisError(
                f"Erreur lors de l'analyse des dépendances: {e}"
            ) from e

    def get_optimal_development_order(self) -> List[DevelopmentPhase]:
        """Retourne l'ordre optimal de développement des phases."""
        if not self.phases:
            raise DependencyAnalysisError("Aucune phase définie")

        try:
            # Trier les phases par priorité et dépendances
            sorted_phases = sorted(
                self.phases,
                key=lambda p: (
                    len(p.dependencies),  # Moins de dépendances en premier
                    p.estimated_duration,  # Durée plus courte en premier
                ),
            )
            return sorted_phases
        except Exception as e:
            raise DependencyAnalysisError(
                f"Erreur lors du calcul de l'ordre optimal: {e}"
            ) from e

    def get_parallel_components(self) -> Dict[str, List[str]]:
        """Identifie les composants qui peuvent être développés en parallèle."""
        if not self.phases:
            raise DependencyAnalysisError("Aucune phase définie")

        try:
            parallel_components = {}
            for phase in self.phases:
                if phase.can_parallelize:
                    parallel_components[phase.name] = phase.components
            return parallel_components
        except Exception as e:
            raise DependencyAnalysisError(
                f"Erreur lors de l'identification des composants parallèles: {e}"
            ) from e

    def get_component_dependencies(self, component: str) -> List[ComponentDependency]:
        """Retourne les dépendances d'un composant."""
        if component not in self.components:
            raise DependencyAnalysisError(f"Composant '{component}' non trouvé")

        return [dep for dep in self.dependencies if dep.source == component]

    def get_component_dependents(self, component: str) -> List[ComponentDependency]:
        """Retourne les composants qui dépendent du composant donné."""
        if component not in self.components:
            raise DependencyAnalysisError(f"Composant '{component}' non trouvé")

        return [dep for dep in self.dependencies if dep.target == component]

    def update_component_status(self, component: str, status: ComponentStatus) -> None:
        """Met à jour le statut d'un composant."""
        if component not in self.components:
            raise DependencyAnalysisError(f"Composant '{component}' non trouvé")

        self.component_status[component] = status

    def get_development_roadmap(self) -> Dict[str, Any]:
        """Génère une feuille de route complète de développement."""
        try:
            analysis = self.analyze_dependencies()
            optimal_order = self.get_optimal_development_order()
            parallel_components = self.get_parallel_components()
            recommendations = self._generate_recommendations()
            timeline = self._generate_timeline()

            return {
                "analysis": analysis,
                "optimal_order": optimal_order,
                "parallel_components": parallel_components,
                "recommendations": recommendations,
                "timeline": timeline,
            }
        except Exception as e:
            raise DependencyAnalysisError(
                f"Erreur lors de la génération de la feuille de route: {e}"
            ) from e

    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Construit le graphe des dépendances."""
        graph = defaultdict(list)
        for dep in self.dependencies:
            graph[dep.source].append(dep.target)
        return dict(graph)

    def _calculate_critical_path(self, graph: Dict[str, List[str]]) -> List[str]:
        """Calcule le chemin critique de développement."""
        # Tri topologique simple
        in_degree = defaultdict(int)
        for node in self.components:
            in_degree[node] = 0

        for dep in self.dependencies:
            in_degree[dep.target] += 1

        queue = deque([node for node in self.components if in_degree[node] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result

    def _identify_parallel_opportunities(
        self, graph: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """Identifie les opportunités de développement parallèle."""
        opportunities = {}
        levels = self._calculate_dependency_levels(graph)

        for level, components in levels.items():
            if len(components) > 1:
                opportunities[f"Level {level}"] = components

        return opportunities

    def _calculate_dependency_levels(
        self, graph: Dict[str, List[str]]
    ) -> Dict[int, List[str]]:
        """Calcule les niveaux de dépendance."""
        levels = defaultdict(list)
        visited = set()

        def dfs(node, level):
            if node in visited:
                return
            visited.add(node)
            levels[level].append(node)

            for neighbor in graph.get(node, []):
                dfs(neighbor, level + 1)

        # Commencer par les nœuds sans dépendances
        for node in self.components:
            if not any(dep.target == node for dep in self.dependencies):
                dfs(node, 0)

        return dict(levels)

    def _analyze_risks(self, graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyse les risques de développement."""
        risks = {
            "high_dependency_components": [],
            "circular_dependencies": [],
            "performance_risks": [],
            "complexity_risks": [],
        }

        # Identifier les composants avec beaucoup de dépendances
        for component, deps in graph.items():
            if len(deps) > 3:
                risks["high_dependency_components"].append(component)

        # Détecter les dépendances circulaires
        risks["circular_dependencies"] = self._detect_circular_dependencies(graph)

        # Analyser les risques de performance
        for component, metadata in self.components.items():
            perf_targets = metadata.get("performance_targets", {})
            if perf_targets.get("execution_time", 0) > 100:
                risks["performance_risks"].append(component)

        return risks

    def _detect_circular_dependencies(
        self, graph: Dict[str, List[str]]
    ) -> List[List[str]]:
        """Détecte les dépendances circulaires."""
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node, path):
            if node in rec_stack:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            if node in visited:
                return

            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                dfs(neighbor, path.copy())

            rec_stack.remove(node)

        for node in self.components:
            if node not in visited:
                dfs(node, [])

        return cycles

    def _calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calcule les métriques de performance."""
        total_duration = sum(phase.estimated_duration for phase in self.phases)
        parallel_phases = sum(1 for phase in self.phases if phase.can_parallelize)
        sequential_phases = len(self.phases) - parallel_phases
        efficiency_gain = self._calculate_efficiency_gain()
        resource_utilization = self._calculate_resource_utilization()

        return {
            "total_estimated_duration": total_duration,
            "parallel_phases": parallel_phases,
            "sequential_phases": sequential_phases,
            "efficiency_gain": efficiency_gain,
            "resource_utilization": resource_utilization,
        }

    def _calculate_efficiency_gain(self) -> float:
        """Calcule le gain d'efficacité du développement parallèle."""
        total_sequential = sum(phase.estimated_duration for phase in self.phases)
        parallel_phases = [p for p in self.phases if p.can_parallelize]

        if not parallel_phases:
            return 0.0

        max_parallel_duration = max(
            phase.estimated_duration for phase in parallel_phases
        )
        sequential_phases = [p for p in self.phases if not p.can_parallelize]
        sequential_duration = sum(
            phase.estimated_duration for phase in sequential_phases
        )

        parallel_duration = sequential_duration + max_parallel_duration
        efficiency_gain = (
            (total_sequential - parallel_duration) / total_sequential
        ) * 100

        return max(0.0, efficiency_gain)

    def _calculate_resource_utilization(self) -> Dict[str, float]:
        """Calcule l'utilisation des ressources."""
        total_phases = len(self.phases)
        parallel_phases = sum(1 for phase in self.phases if phase.can_parallelize)
        sequential_phases = total_phases - parallel_phases

        parallel_utilization = (
            (parallel_phases / total_phases) * 100 if total_phases > 0 else 0
        )
        sequential_utilization = (
            (sequential_phases / total_phases) * 100 if total_phases > 0 else 0
        )

        return {
            "parallel_utilization": parallel_utilization,
            "sequential_utilization": sequential_utilization,
        }

    def _generate_recommendations(self) -> List[str]:
        """Génère des recommandations de développement."""
        recommendations = []

        # Recommandations basées sur les dépendances
        high_dep_components = [
            comp
            for comp, deps in self.components.items()
            if len(deps.get("dependencies", [])) > 2
        ]
        if high_dep_components:
            recommendations.append(
                f"Prioriser le développement des composants à haute dépendance: {', '.join(high_dep_components)}"
            )

        # Recommandations de parallélisation
        parallel_phases = [phase for phase in self.phases if phase.can_parallelize]
        if parallel_phases:
            recommendations.append(
                f"Développer en parallèle les phases: {', '.join(phase.name for phase in parallel_phases)}"
            )

        # Recommandations de test
        recommendations.append(
            "Maintenir une couverture de tests >= 95% pour tous les composants"
        )
        recommendations.append(
            "Implémenter des tests d'intégration pour valider les dépendances"
        )

        return recommendations

    def _generate_timeline(self) -> Dict[str, Any]:
        """Génère une timeline de développement."""
        timeline = {
            "total_duration": sum(phase.estimated_duration for phase in self.phases),
            "phases": [],
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
                "can_parallelize": phase.can_parallelize,
            }
            timeline["phases"].append(phase_info)

            current_week += phase.estimated_duration

        return timeline
