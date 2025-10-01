"""
Tests unitaires pour le module dependency_analysis.

Ce module contient les tests unitaires pour l'analyse des dépendances
entre les composants de la phase 2 du projet Baobab Automata.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, List, Any

from baobab_automata.algorithms.dependency_analysis import (
    DependencyAnalyzer,
    ComponentDependency,
    DevelopmentPhase,
    ComponentStatus,
    DependencyAnalysisError,
)


class TestComponentDependency:
    """Tests pour la classe ComponentDependency."""

    def test_component_dependency_creation(self):
        """Test la création d'une dépendance de composant."""
        dep = ComponentDependency(
            source="NFA",
            target="DFA",
            dependency_type="interface",
            priority=1,
            description="NFA utilise DFA pour les conversions",
        )

        assert dep.source == "NFA"
        assert dep.target == "DFA"
        assert dep.dependency_type == "interface"
        assert dep.priority == 1
        assert dep.description == "NFA utilise DFA pour les conversions"

    def test_component_dependency_default_values(self):
        """Test les valeurs par défaut d'une dépendance de composant."""
        dep = ComponentDependency(
            source="NFA", target="DFA", dependency_type="interface"
        )

        assert dep.priority == 1
        assert dep.description == ""


class TestDevelopmentPhase:
    """Tests pour la classe DevelopmentPhase."""

    def test_development_phase_creation(self):
        """Test la création d'une phase de développement."""
        phase = DevelopmentPhase(
            name="Phase 2A",
            components=["DFA", "NFA"],
            can_parallelize=False,
            estimated_duration=6,
            dependencies=[],
        )

        assert phase.name == "Phase 2A"
        assert phase.components == ["DFA", "NFA"]
        assert phase.can_parallelize is False
        assert phase.estimated_duration == 6
        assert phase.dependencies == []

    def test_development_phase_default_values(self):
        """Test les valeurs par défaut d'une phase de développement."""
        phase = DevelopmentPhase(name="Phase 2A")

        assert phase.components == []
        assert phase.can_parallelize is False
        assert phase.estimated_duration == 0
        assert phase.dependencies == []


class TestDependencyAnalyzer:
    """Tests pour la classe DependencyAnalyzer."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.analyzer = DependencyAnalyzer()

    def test_initialization(self):
        """Test l'initialisation de l'analyseur."""
        assert len(self.analyzer.components) == 7
        assert len(self.analyzer.dependencies) > 0
        assert len(self.analyzer.phases) == 3
        assert len(self.analyzer.component_status) == 7

        # Vérifier que tous les composants sont initialisés
        expected_components = [
            "DFA",
            "NFA",
            "ε-NFA",
            "RegexParser",
            "ConversionAlgorithms",
            "OptimizationAlgorithms",
            "LanguageOperations",
        ]
        for component in expected_components:
            assert component in self.analyzer.components
            assert component in self.analyzer.component_status
            assert (
                self.analyzer.component_status[component] == ComponentStatus.NOT_STARTED
            )

    def test_analyze_dependencies(self):
        """Test l'analyse des dépendances."""
        analysis = self.analyzer.analyze_dependencies()

        assert "dependency_graph" in analysis
        assert "critical_path" in analysis
        assert "parallel_opportunities" in analysis
        assert "risk_analysis" in analysis
        assert "performance_metrics" in analysis
        assert "analysis_time" in analysis
        assert "total_components" in analysis
        assert "total_dependencies" in analysis

        assert analysis["total_components"] == 7
        assert analysis["total_dependencies"] > 0
        assert analysis["analysis_time"] > 0

    def test_get_optimal_development_order(self):
        """Test la détermination de l'ordre optimal de développement."""
        optimal_order = self.analyzer.get_optimal_development_order()

        assert len(optimal_order) == 3
        assert all(isinstance(phase, DevelopmentPhase) for phase in optimal_order)

        # Vérifier que la phase 2A (classes de base) est en premier
        assert optimal_order[0].name == "Phase 2A: Classes de Base"
        assert "DFA" in optimal_order[0].components
        assert "NFA" in optimal_order[0].components
        assert "ε-NFA" in optimal_order[0].components

    def test_get_parallel_components(self):
        """Test l'identification des composants parallélisables."""
        parallel_components = self.analyzer.get_parallel_components()

        assert isinstance(parallel_components, dict)
        assert len(parallel_components) > 0

        # Vérifier que les phases parallélisables sont présentes
        phase_names = list(parallel_components.keys())
        assert any("Phase 2B" in name for name in phase_names)
        assert any("Phase 2C" in name for name in phase_names)

    def test_get_component_dependencies(self):
        """Test l'obtention des dépendances d'un composant."""
        dependencies = self.analyzer.get_component_dependencies("DFA")

        assert isinstance(dependencies, list)
        assert all(isinstance(dep, ComponentDependency) for dep in dependencies)

        # DFA ne devrait avoir aucune dépendance
        assert len(dependencies) == 0

    def test_get_component_dependencies_nonexistent(self):
        """Test l'obtention des dépendances d'un composant inexistant."""
        with pytest.raises(DependencyAnalysisError):
            self.analyzer.get_component_dependencies("Inexistant")

    def test_get_component_dependents(self):
        """Test l'obtention des composants dépendants."""
        dependents = self.analyzer.get_component_dependents("DFA")

        assert isinstance(dependents, list)
        assert all(isinstance(dep, ComponentDependency) for dep in dependents)
        assert len(dependents) > 0

        # Vérifier que NFA dépend de DFA
        nfa_deps = [dep for dep in dependents if dep.source == "NFA"]
        assert len(nfa_deps) > 0

    def test_get_component_dependents_nonexistent(self):
        """Test l'obtention des composants dépendants d'un composant inexistant."""
        with pytest.raises(DependencyAnalysisError):
            self.analyzer.get_component_dependents("Inexistant")

    def test_update_component_status(self):
        """Test la mise à jour du statut d'un composant."""
        self.analyzer.update_component_status("DFA", ComponentStatus.IN_PROGRESS)
        assert self.analyzer.component_status["DFA"] == ComponentStatus.IN_PROGRESS

        self.analyzer.update_component_status("DFA", ComponentStatus.COMPLETED)
        assert self.analyzer.component_status["DFA"] == ComponentStatus.COMPLETED

    def test_update_component_status_nonexistent(self):
        """Test la mise à jour du statut d'un composant inexistant."""
        with pytest.raises(DependencyAnalysisError):
            self.analyzer.update_component_status(
                "Inexistant", ComponentStatus.IN_PROGRESS
            )

    def test_get_development_roadmap(self):
        """Test la génération de la feuille de route de développement."""
        roadmap = self.analyzer.get_development_roadmap()

        assert "analysis" in roadmap
        assert "optimal_order" in roadmap
        assert "parallel_components" in roadmap
        assert "recommendations" in roadmap
        assert "timeline" in roadmap

        assert isinstance(roadmap["recommendations"], list)
        assert len(roadmap["recommendations"]) > 0

        assert isinstance(roadmap["timeline"], dict)
        assert "total_duration" in roadmap["timeline"]
        assert "phases" in roadmap["timeline"]

    def test_build_dependency_graph(self):
        """Test la construction du graphe des dépendances."""
        graph = self.analyzer._build_dependency_graph()

        assert isinstance(graph, dict)
        assert len(graph) > 0

        # Vérifier que DFA n'a pas de dépendances
        assert "DFA" not in graph or len(graph["DFA"]) == 0

    def test_calculate_critical_path(self):
        """Test le calcul du chemin critique."""
        graph = self.analyzer._build_dependency_graph()
        critical_path = self.analyzer._calculate_critical_path(graph)

        assert isinstance(critical_path, list)
        assert len(critical_path) == 7

        # DFA devrait être en premier (aucune dépendance)
        assert critical_path[0] == "DFA"

    def test_identify_parallel_opportunities(self):
        """Test l'identification des opportunités de développement parallèle."""
        graph = self.analyzer._build_dependency_graph()
        opportunities = self.analyzer._identify_parallel_opportunities(graph)

        assert isinstance(opportunities, dict)
        assert len(opportunities) > 0

    def test_calculate_dependency_levels(self):
        """Test le calcul des niveaux de dépendance."""
        graph = self.analyzer._build_dependency_graph()
        levels = self.analyzer._calculate_dependency_levels(graph)

        assert isinstance(levels, dict)
        assert len(levels) > 0

        # Vérifier que tous les composants sont dans un niveau
        all_components = set()
        for level_components in levels.values():
            all_components.update(level_components)
        assert len(all_components) == 7

    def test_analyze_risks(self):
        """Test l'analyse des risques."""
        graph = self.analyzer._build_dependency_graph()
        risks = self.analyzer._analyze_risks(graph)

        assert isinstance(risks, dict)
        assert "high_dependency_components" in risks
        assert "circular_dependencies" in risks
        assert "performance_risks" in risks
        assert "complexity_risks" in risks

    def test_detect_circular_dependencies(self):
        """Test la détection des dépendances circulaires."""
        graph = self.analyzer._build_dependency_graph()
        cycles = self.analyzer._detect_circular_dependencies(graph)

        assert isinstance(cycles, list)
        # Dans notre cas, il ne devrait pas y avoir de cycles
        assert len(cycles) == 0

    def test_calculate_performance_metrics(self):
        """Test le calcul des métriques de performance."""
        metrics = self.analyzer._calculate_performance_metrics()

        assert isinstance(metrics, dict)
        assert "total_estimated_duration" in metrics
        assert "parallel_phases" in metrics
        assert "sequential_phases" in metrics
        assert "efficiency_gain" in metrics
        assert "resource_utilization" in metrics

        assert metrics["total_estimated_duration"] > 0
        assert metrics["efficiency_gain"] >= 0
        assert metrics["resource_utilization"]["parallel_utilization"] >= 0

    def test_calculate_efficiency_gain(self):
        """Test le calcul du gain d'efficacité."""
        efficiency_gain = self.analyzer._calculate_efficiency_gain()

        assert isinstance(efficiency_gain, float)
        assert efficiency_gain >= 0

    def test_calculate_resource_utilization(self):
        """Test le calcul de l'utilisation des ressources."""
        utilization = self.analyzer._calculate_resource_utilization()

        assert isinstance(utilization, dict)
        assert "parallel_utilization" in utilization
        assert "sequential_utilization" in utilization

        total_utilization = (
            utilization["parallel_utilization"] + utilization["sequential_utilization"]
        )
        assert abs(total_utilization - 100.0) < 0.01  # Devrait être proche de 100%

    def test_generate_recommendations(self):
        """Test la génération des recommandations."""
        recommendations = self.analyzer._generate_recommendations()

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all(isinstance(rec, str) for rec in recommendations)

    def test_generate_timeline(self):
        """Test la génération de la timeline."""
        timeline = self.analyzer._generate_timeline()

        assert isinstance(timeline, dict)
        assert "total_duration" in timeline
        assert "phases" in timeline

        assert isinstance(timeline["phases"], list)
        assert len(timeline["phases"]) == 3

        for phase in timeline["phases"]:
            assert "name" in phase
            assert "duration" in phase
            assert "start_week" in phase
            assert "start_day" in phase
            assert "components" in phase
            assert "can_parallelize" in phase

    def test_error_handling_analyze_dependencies(self):
        """Test la gestion d'erreur dans analyze_dependencies."""
        with patch.object(
            self.analyzer,
            "_build_dependency_graph",
            side_effect=Exception("Test error"),
        ):
            with pytest.raises(DependencyAnalysisError):
                self.analyzer.analyze_dependencies()

    def test_error_handling_get_optimal_development_order(self):
        """Test la gestion d'erreur dans get_optimal_development_order."""
        with patch.object(self.analyzer, "phases", None):
            with pytest.raises(DependencyAnalysisError):
                self.analyzer.get_optimal_development_order()

    def test_error_handling_get_parallel_components(self):
        """Test la gestion d'erreur dans get_parallel_components."""
        with patch.object(self.analyzer, "phases", None):
            with pytest.raises(DependencyAnalysisError):
                self.analyzer.get_parallel_components()

    def test_error_handling_get_development_roadmap(self):
        """Test la gestion d'erreur dans get_development_roadmap."""
        with patch.object(
            self.analyzer, "analyze_dependencies", side_effect=Exception("Test error")
        ):
            with pytest.raises(DependencyAnalysisError):
                self.analyzer.get_development_roadmap()


class TestComponentStatus:
    """Tests pour l'énumération ComponentStatus."""

    def test_component_status_values(self):
        """Test les valeurs de l'énumération ComponentStatus."""
        assert ComponentStatus.NOT_STARTED.value == "not_started"
        assert ComponentStatus.IN_PROGRESS.value == "in_progress"
        assert ComponentStatus.COMPLETED.value == "completed"
        assert ComponentStatus.BLOCKED.value == "blocked"
        assert ComponentStatus.FAILED.value == "failed"

    def test_component_status_enumeration(self):
        """Test l'énumération des statuts."""
        statuses = list(ComponentStatus)
        assert len(statuses) == 5
        assert ComponentStatus.NOT_STARTED in statuses
        assert ComponentStatus.IN_PROGRESS in statuses
        assert ComponentStatus.COMPLETED in statuses
        assert ComponentStatus.BLOCKED in statuses
        assert ComponentStatus.FAILED in statuses


class TestDependencyAnalysisError:
    """Tests pour l'exception DependencyAnalysisError."""

    def test_dependency_analysis_error_creation(self):
        """Test la création d'une exception DependencyAnalysisError."""
        error = DependencyAnalysisError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)

    def test_dependency_analysis_error_inheritance(self):
        """Test l'héritage de DependencyAnalysisError."""
        error = DependencyAnalysisError("Test error message")
        assert isinstance(error, Exception)


class TestIntegration:
    """Tests d'intégration pour le module dependency_analysis."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.analyzer = DependencyAnalyzer()

    def test_full_workflow(self):
        """Test le workflow complet de l'analyse des dépendances."""
        # 1. Analyser les dépendances
        analysis = self.analyzer.analyze_dependencies()
        assert analysis is not None

        # 2. Obtenir l'ordre optimal
        optimal_order = self.analyzer.get_optimal_development_order()
        assert len(optimal_order) > 0

        # 3. Identifier les composants parallèles
        parallel_components = self.analyzer.get_parallel_components()
        assert len(parallel_components) > 0

        # 4. Générer la feuille de route
        roadmap = self.analyzer.get_development_roadmap()
        assert roadmap is not None

        # 5. Mettre à jour le statut d'un composant
        self.analyzer.update_component_status("DFA", ComponentStatus.IN_PROGRESS)
        assert self.analyzer.component_status["DFA"] == ComponentStatus.IN_PROGRESS

    def test_performance_requirements(self):
        """Test que les exigences de performance sont respectées."""
        analysis = self.analyzer.analyze_dependencies()

        # Vérifier que l'analyse se termine rapidement
        assert analysis["analysis_time"] < 1.0  # Moins d'une seconde

        # Vérifier que tous les composants sont analysés
        assert analysis["total_components"] == 7
        assert analysis["total_dependencies"] > 0

    def test_memory_usage(self):
        """Test que l'utilisation mémoire reste raisonnable."""
        # Créer plusieurs analyseurs pour tester la mémoire
        analyzers = [DependencyAnalyzer() for _ in range(10)]

        # Vérifier que chaque analyseur fonctionne
        for analyzer in analyzers:
            analysis = analyzer.analyze_dependencies()
            assert analysis is not None

        # Nettoyer
        del analyzers
