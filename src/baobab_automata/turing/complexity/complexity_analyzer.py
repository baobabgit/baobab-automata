"""Analyseur de complexité pour les machines de Turing."""

import time
import threading
from typing import Any, Dict, List

try:
    import psutil
except ImportError:
    psutil = None

from .interfaces import IComplexityAnalyzer
from .types import (
    ComplexityClass,
    DecidabilityStatus,
)
from .exceptions import (
    ComplexityAnalysisError,
    InvalidComplexityAnalyzerError,
)


class ComplexityAnalyzer(IComplexityAnalyzer):
    """Analyseur de complexité pour les machines de Turing."""

    def __init__(
        self,
        enable_profiling: bool = True,
        enable_memory_monitoring: bool = True,
        max_analysis_time: int = 60,
        sample_size: int = 100,
    ) -> None:
        """Initialise l'analyseur de complexité.

        :param enable_profiling: Active le profilage détaillé
        :param enable_memory_monitoring: Active le monitoring mémoire
        :param max_analysis_time: Temps maximum d'analyse (secondes)
        :param sample_size: Taille d'échantillon pour les tests
        :raises InvalidComplexityAnalyzerError: Si la configuration est
            invalide
        """
        self._enable_profiling = enable_profiling
        self._enable_memory_monitoring = enable_memory_monitoring
        self._max_analysis_time = max_analysis_time
        self._sample_size = sample_size

        # Cache des analyses
        self._analysis_cache = {}
        self._complexity_cache = {}

        # Statistiques d'analyse
        self._analysis_stats = {
            "total_analyses": 0,
            "successful_analyses": 0,
            "failed_analyses": 0,
            "cache_hits": 0,
            "average_analysis_time": 0.0,
        }

        # Monitoring des ressources
        self._memory_monitor = None
        self._cpu_monitor = None
        self._current_memory_usage = 0
        self._current_cpu_usage = 0

        if enable_memory_monitoring and psutil:
            self._start_resource_monitoring()

        # Validation de la configuration
        if max_analysis_time <= 0:
            raise InvalidComplexityAnalyzerError(
                "Max analysis time must be positive"
            )
        if sample_size <= 0:
            raise InvalidComplexityAnalyzerError(
                "Sample size must be positive"
            )

    def _start_resource_monitoring(self) -> None:
        """Démarre le monitoring des ressources."""
        if not psutil:
            return

        self._memory_monitor = threading.Thread(
            target=self._monitor_memory, daemon=True
        )
        self._cpu_monitor = threading.Thread(
            target=self._monitor_cpu, daemon=True
        )

        self._memory_monitor.start()
        self._cpu_monitor.start()

    def analyze_time_complexity(
        self, machine: Any, test_cases: List[str]
    ) -> Dict[str, Any]:
        """Analyse la complexité temporelle d'une machine.

        :param machine: Machine à analyser
        :param test_cases: Cas de test pour l'analyse
        :return: Analyse de complexité temporelle
        :raises ComplexityAnalysisError: Si l'analyse échoue
        """
        start_time = time.time()

        try:
            # Vérification du cache
            cache_key = self._get_cache_key(machine, "time_complexity")
            if cache_key in self._analysis_cache:
                self._analysis_stats["cache_hits"] += 1
                return self._analysis_cache[cache_key]

            # Génération de cas de test si nécessaire
            if not test_cases:
                test_cases = self._generate_test_cases(
                    machine, self._sample_size
                )

            # Analyse des performances
            performance_data = self._collect_performance_data(
                machine, test_cases
            )

            # Classification de la complexité
            complexity_class = self._classify_time_complexity(performance_data)

            # Calcul des métriques
            metrics = self._calculate_time_metrics(
                performance_data, complexity_class
            )

            # Construction du résultat
            result = {
                "machine_type": type(machine).__name__,
                "complexity_class": complexity_class.value,
                "time_metrics": metrics,
                "performance_data": performance_data,
                "test_cases_analyzed": len(test_cases),
                "analysis_time": time.time() - start_time,
                "confidence_level": self._calculate_confidence_level(
                    performance_data
                ),
            }

            # Cache du résultat
            self._analysis_cache[cache_key] = result
            self._analysis_stats["total_analyses"] += 1
            self._analysis_stats["successful_analyses"] += 1

            return result

        except Exception as e:
            self._analysis_stats["failed_analyses"] += 1
            raise ComplexityAnalysisError(
                f"Time complexity analysis failed: {e}"
            ) from e

    def analyze_space_complexity(
        self, machine: Any, test_cases: List[str]
    ) -> Dict[str, Any]:
        """Analyse la complexité spatiale d'une machine.

        :param machine: Machine à analyser
        :param test_cases: Cas de test pour l'analyse
        :return: Analyse de complexité spatiale
        :raises ComplexityAnalysisError: Si l'analyse échoue
        """
        start_time = time.time()

        try:
            # Vérification du cache
            cache_key = self._get_cache_key(machine, "space_complexity")
            if cache_key in self._analysis_cache:
                self._analysis_stats["cache_hits"] += 1
                return self._analysis_cache[cache_key]

            # Génération de cas de test si nécessaire
            if not test_cases:
                test_cases = self._generate_test_cases(
                    machine, self._sample_size
                )

            # Analyse de l'usage mémoire
            memory_data = self._collect_memory_data(machine, test_cases)

            # Classification de la complexité spatiale
            space_complexity_class = self._classify_space_complexity(
                memory_data
            )

            # Calcul des métriques
            metrics = self._calculate_space_metrics(
                memory_data, space_complexity_class
            )

            # Construction du résultat
            result = {
                "machine_type": type(machine).__name__,
                "space_complexity_class": space_complexity_class.value,
                "space_metrics": metrics,
                "memory_data": memory_data,
                "test_cases_analyzed": len(test_cases),
                "analysis_time": time.time() - start_time,
                "confidence_level": self._calculate_confidence_level(
                    memory_data
                ),
            }

            # Cache du résultat
            self._analysis_cache[cache_key] = result
            self._analysis_stats["total_analyses"] += 1
            self._analysis_stats["successful_analyses"] += 1

            return result

        except Exception as e:
            self._analysis_stats["failed_analyses"] += 1
            raise ComplexityAnalysisError(
                f"Space complexity analysis failed: {e}"
            ) from e

    def classify_problem(self, machine: Any) -> ComplexityClass:
        """Classe un problème selon sa complexité.

        :param machine: Machine à classifier
        :return: Classe de complexité
        :raises ComplexityAnalysisError: Si la classification échoue
        """
        try:
            # Analyse temporelle
            time_analysis = self.analyze_time_complexity(machine, [])
            time_class = ComplexityClass(time_analysis["complexity_class"])

            # Analyse spatiale
            space_analysis = self.analyze_space_complexity(machine, [])
            space_class = ComplexityClass(
                space_analysis["space_complexity_class"]
            )

            # Classification finale basée sur les deux analyses
            final_class = self._determine_final_complexity_class(
                time_class, space_class
            )

            # Cache du résultat
            cache_key = self._get_cache_key(machine, "problem_classification")
            self._complexity_cache[cache_key] = final_class

            return final_class

        except Exception as e:
            raise ComplexityAnalysisError(
                f"Problem classification failed: {e}"
            ) from e

    def determine_decidability(self, machine: Any) -> DecidabilityStatus:
        """Détermine la décidabilité d'un problème.

        :param machine: Machine à analyser
        :return: Statut de décidabilité
        :raises ComplexityAnalysisError: Si l'analyse échoue
        """
        try:
            # Test de décidabilité avec cas limites
            decidability_tests = self._run_decidability_tests(machine)

            # Analyse des résultats
            if decidability_tests["always_halts"]:
                return DecidabilityStatus.DECIDABLE
            if decidability_tests["sometimes_halts"]:
                return DecidabilityStatus.SEMI_DECIDABLE
            if decidability_tests["never_halts"]:
                return DecidabilityStatus.UNDECIDABLE
            return DecidabilityStatus.UNKNOWN

        except Exception as e:
            raise ComplexityAnalysisError(
                f"Decidability determination failed: {e}"
            ) from e

    def compare_complexity(
        self, machine1: Any, machine2: Any
    ) -> Dict[str, Any]:
        """Compare la complexité de deux machines.

        :param machine1: Première machine
        :param machine2: Deuxième machine
        :return: Comparaison de complexité
        :raises ComplexityAnalysisError: Si la comparaison échoue
        """
        try:
            # Analyse des deux machines
            analysis1 = self._analyze_machine_complete(machine1)
            analysis2 = self._analyze_machine_complete(machine2)

            # Comparaison des métriques
            comparison = {
                "machine1": {
                    "type": type(machine1).__name__,
                    "complexity_class": analysis1["complexity_class"],
                    "time_metrics": analysis1["time_metrics"],
                    "space_metrics": analysis1["space_metrics"],
                },
                "machine2": {
                    "type": type(machine2).__name__,
                    "complexity_class": analysis2["complexity_class"],
                    "time_metrics": analysis2["time_metrics"],
                    "space_metrics": analysis2["space_metrics"],
                },
                "comparison": {
                    "time_comparison": self._compare_time_complexity(
                        analysis1, analysis2
                    ),
                    "space_comparison": self._compare_space_complexity(
                        analysis1, analysis2
                    ),
                    "overall_comparison": self._compare_overall_complexity(
                        analysis1, analysis2
                    ),
                },
            }

            return comparison

        except Exception as e:
            raise ComplexityAnalysisError(
                f"Complexity comparison failed: {e}"
            ) from e

    def _collect_performance_data(
        self, machine: Any, test_cases: List[str]
    ) -> Dict[str, Any]:
        """Collecte les données de performance."""
        performance_data = {
            "execution_times": [],
            "input_lengths": [],
            "step_counts": [],
            "timeout_count": 0,
            "error_count": 0,
        }

        for test_case in test_cases:
            try:
                start_time = time.time()

                # Simulation avec limitation de temps
                if hasattr(machine, "simulate"):
                    _, trace = machine.simulate(test_case, max_steps=10000)
                elif hasattr(machine, "simulate_deterministic"):
                    _, trace = machine.simulate_deterministic(
                        test_case, max_steps=10000
                    )
                elif hasattr(machine, "simulate_non_deterministic"):
                    _, trace = machine.simulate_non_deterministic(
                        test_case, max_steps=10000
                    )
                elif hasattr(machine, "simulate_multi_tape"):
                    default_inputs = [test_case] * machine.tape_count
                    _, trace = machine.simulate_multi_tape(
                        default_inputs, max_steps=10000
                    )
                else:
                    continue

                execution_time = time.time() - start_time

                performance_data["execution_times"].append(execution_time)
                performance_data["input_lengths"].append(len(test_case))
                performance_data["step_counts"].append(len(trace))

                # Vérification du timeout
                if len(trace) >= 10000:
                    performance_data["timeout_count"] += 1

            except Exception:
                performance_data["error_count"] += 1

        return performance_data

    def _collect_memory_data(
        self, machine: Any, test_cases: List[str]
    ) -> Dict[str, Any]:
        """Collecte les données d'usage mémoire."""
        memory_data = {
            "memory_usage": [],
            "tape_lengths": [],
            "state_counts": [],
            "peak_memory": 0,
            "average_memory": 0,
        }

        if not psutil:
            # Fallback sans psutil
            for test_case in test_cases:
                memory_data["memory_usage"].append(
                    len(test_case) * 100
                )  # Estimation
                memory_data["tape_lengths"].append(len(test_case))
                memory_data["state_counts"].append(10)  # Estimation
            memory_data["peak_memory"] = (
                max(memory_data["memory_usage"])
                if memory_data["memory_usage"]
                else 0
            )
            memory_data["average_memory"] = (
                sum(memory_data["memory_usage"])
                / len(memory_data["memory_usage"])
                if memory_data["memory_usage"]
                else 0
            )
            return memory_data

        for test_case in test_cases:
            try:
                # Monitoring mémoire avant simulation
                memory_before = psutil.Process().memory_info().rss

                # Simulation
                if hasattr(machine, "simulate"):
                    _, trace = machine.simulate(test_case, max_steps=10000)
                elif hasattr(machine, "simulate_deterministic"):
                    _, trace = machine.simulate_deterministic(
                        test_case, max_steps=10000
                    )
                elif hasattr(machine, "simulate_non_deterministic"):
                    _, trace = machine.simulate_non_deterministic(
                        test_case, max_steps=10000
                    )
                elif hasattr(machine, "simulate_multi_tape"):
                    default_inputs = [test_case] * machine.tape_count
                    _, trace = machine.simulate_multi_tape(
                        default_inputs, max_steps=10000
                    )
                else:
                    continue

                # Monitoring mémoire après simulation
                memory_after = psutil.Process().memory_info().rss
                memory_used = memory_after - memory_before

                memory_data["memory_usage"].append(memory_used)
                memory_data["tape_lengths"].append(len(test_case))
                memory_data["state_counts"].append(len(trace))

                # Mise à jour du pic mémoire
                memory_data["peak_memory"] = max(
                    memory_data["peak_memory"], memory_used
                )

            except Exception:
                continue

        # Calcul de la moyenne
        if memory_data["memory_usage"]:
            memory_data["average_memory"] = sum(
                memory_data["memory_usage"]
            ) / len(memory_data["memory_usage"])

        return memory_data

    def _classify_time_complexity(
        self, performance_data: Dict[str, Any]
    ) -> ComplexityClass:
        """Classe la complexité temporelle."""
        execution_times = performance_data["execution_times"]
        input_lengths = performance_data["input_lengths"]

        if not execution_times or not input_lengths:
            return ComplexityClass.UNKNOWN

        # Analyse de la croissance
        growth_rate = self._calculate_growth_rate(
            execution_times, input_lengths
        )

        # Classification basée sur le taux de croissance
        if growth_rate <= 1.2:
            return ComplexityClass.P
        elif growth_rate <= 2.0:
            return ComplexityClass.NP
        elif growth_rate <= 3.0:
            return ComplexityClass.PSPACE
        elif growth_rate <= 4.0:
            return ComplexityClass.EXPTIME
        else:
            return ComplexityClass.EXPSPACE

    def _classify_space_complexity(
        self, memory_data: Dict[str, Any]
    ) -> ComplexityClass:
        """Classe la complexité spatiale."""
        memory_usage = memory_data["memory_usage"]
        tape_lengths = memory_data["tape_lengths"]

        if not memory_usage or not tape_lengths:
            return ComplexityClass.UNKNOWN

        # Analyse de la croissance de l'usage mémoire
        space_growth_rate = self._calculate_space_growth_rate(
            memory_usage, tape_lengths
        )

        # Classification basée sur le taux de croissance spatiale
        if space_growth_rate <= 1.1:
            return ComplexityClass.P
        elif space_growth_rate <= 2.0:
            return ComplexityClass.PSPACE
        elif space_growth_rate <= 3.0:
            return ComplexityClass.EXPSPACE
        else:
            return ComplexityClass.EXPSPACE

    def _determine_final_complexity_class(
        self, time_class: ComplexityClass, space_class: ComplexityClass
    ) -> ComplexityClass:
        """Détermine la classe de complexité finale."""
        # Hiérarchie des classes de complexité
        complexity_hierarchy = {
            ComplexityClass.P: 1,
            ComplexityClass.NP: 2,
            ComplexityClass.PSPACE: 3,
            ComplexityClass.EXPTIME: 4,
            ComplexityClass.EXPSPACE: 5,
            ComplexityClass.RECURSIVE: 6,
            ComplexityClass.RECURSIVELY_ENUMERABLE: 7,
            ComplexityClass.UNDECIDABLE: 8,
        }

        # Prendre la classe la plus complexe
        time_level = complexity_hierarchy.get(time_class, 0)
        space_level = complexity_hierarchy.get(space_class, 0)

        max_level = max(time_level, space_level)

        # Retourner la classe correspondante
        for complexity_class, level in complexity_hierarchy.items():
            if level == max_level:
                return complexity_class

        return ComplexityClass.UNKNOWN

    def _run_decidability_tests(self, machine: Any) -> Dict[str, bool]:
        """Exécute les tests de décidabilité."""
        tests = {
            "always_halts": True,
            "sometimes_halts": False,
            "never_halts": False,
        }

        # Cas de test pour la décidabilité
        test_cases = self._generate_decidability_test_cases(machine)

        halt_count = 0
        total_tests = len(test_cases)

        for test_case in test_cases:
            try:
                # Simulation avec limite de temps
                start_time = time.time()

                if hasattr(machine, "simulate"):
                    _, trace = machine.simulate(test_case, max_steps=1000)
                elif hasattr(machine, "simulate_deterministic"):
                    _, trace = machine.simulate_deterministic(
                        test_case, max_steps=1000
                    )
                elif hasattr(machine, "simulate_non_deterministic"):
                    _, trace = machine.simulate_non_deterministic(
                        test_case, max_steps=1000
                    )
                elif hasattr(machine, "simulate_multi_tape"):
                    default_inputs = [test_case] * machine.tape_count
                    _, trace = machine.simulate_multi_tape(
                        default_inputs, max_steps=1000
                    )
                else:
                    continue

                execution_time = time.time() - start_time

                # Vérification si la machine s'arrête
                if len(trace) < 1000 and execution_time < 1.0:
                    halt_count += 1
                else:
                    tests["always_halts"] = False

            except Exception:
                tests["always_halts"] = False

        # Détermination du statut
        halt_ratio = halt_count / total_tests if total_tests > 0 else 0

        if halt_ratio == 1.0:
            tests["always_halts"] = True
        elif halt_ratio > 0:
            tests["sometimes_halts"] = True
        else:
            tests["never_halts"] = True

        return tests

    def _generate_decidability_test_cases(self, machine: Any) -> List[str]:
        """Génère des cas de test pour la décidabilité."""
        test_cases = []

        # Cas de test basiques
        alphabet = (
            list(machine.alphabet)
            if hasattr(machine, "alphabet")
            else ["a", "b"]
        )

        # Chaînes courtes
        for length in range(1, 6):
            test_cases.extend(
                self._generate_strings_of_length(alphabet, length)
            )

        # Cas limites
        test_cases.append("")  # Chaîne vide
        test_cases.append(alphabet[0] * 10)  # Chaîne longue

        return test_cases[:20]  # Limiter à 20 cas de test

    def _generate_strings_of_length(
        self, alphabet: List[str], length: int
    ) -> List[str]:
        """Génère toutes les chaînes d'un alphabet donné de longueur donnée."""
        if length == 0:
            return [""]

        result = []
        for char in alphabet:
            for suffix in self._generate_strings_of_length(
                alphabet, length - 1
            ):
                result.append(char + suffix)

        return result

    def _analyze_machine_complete(self, machine: Any) -> Dict[str, Any]:
        """Analyse complète d'une machine."""
        time_analysis = self.analyze_time_complexity(machine, [])
        space_analysis = self.analyze_space_complexity(machine, [])

        return {
            "complexity_class": time_analysis["complexity_class"],
            "time_metrics": time_analysis["time_metrics"],
            "space_metrics": space_analysis["space_metrics"],
        }

    def _compare_time_complexity(
        self, analysis1: Dict[str, Any], analysis2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare la complexité temporelle."""
        time1 = analysis1["time_metrics"].get("average_execution_time", 0)
        time2 = analysis2["time_metrics"].get("average_execution_time", 0)

        if time1 < time2:
            faster_machine = "machine1"
            speedup_factor = time2 / time1 if time1 > 0 else float("inf")
        elif time2 < time1:
            faster_machine = "machine2"
            speedup_factor = time1 / time2 if time2 > 0 else float("inf")
        else:
            faster_machine = "equal"
            speedup_factor = 1.0

        return {
            "faster_machine": faster_machine,
            "speedup_factor": speedup_factor,
            "time1": time1,
            "time2": time2,
        }

    def _compare_space_complexity(
        self, analysis1: Dict[str, Any], analysis2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare la complexité spatiale."""
        space1 = analysis1["space_metrics"].get("average_memory", 0)
        space2 = analysis2["space_metrics"].get("average_memory", 0)

        if space1 < space2:
            more_efficient_machine = "machine1"
            efficiency_factor = space2 / space1 if space1 > 0 else float("inf")
        elif space2 < space1:
            more_efficient_machine = "machine2"
            efficiency_factor = space1 / space2 if space2 > 0 else float("inf")
        else:
            more_efficient_machine = "equal"
            efficiency_factor = 1.0

        return {
            "more_efficient_machine": more_efficient_machine,
            "efficiency_factor": efficiency_factor,
            "space1": space1,
            "space2": space2,
        }

    def _compare_overall_complexity(
        self, analysis1: Dict[str, Any], analysis2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare la complexité globale."""
        class1 = ComplexityClass(analysis1["complexity_class"])
        class2 = ComplexityClass(analysis2["complexity_class"])

        complexity_hierarchy = {
            ComplexityClass.P: 1,
            ComplexityClass.NP: 2,
            ComplexityClass.PSPACE: 3,
            ComplexityClass.EXPTIME: 4,
            ComplexityClass.EXPSPACE: 5,
            ComplexityClass.RECURSIVE: 6,
            ComplexityClass.RECURSIVELY_ENUMERABLE: 7,
            ComplexityClass.UNDECIDABLE: 8,
        }

        level1 = complexity_hierarchy.get(class1, 0)
        level2 = complexity_hierarchy.get(class2, 0)

        if level1 < level2:
            simpler_machine = "machine1"
        elif level2 < level1:
            simpler_machine = "machine2"
        else:
            simpler_machine = "equal"

        return {
            "simpler_machine": simpler_machine,
            "class1": class1.value,
            "class2": class2.value,
        }

    def _calculate_growth_rate(
        self, times: List[float], lengths: List[int]
    ) -> float:
        """Calcule le taux de croissance."""
        if len(times) < 2:
            return 1.0

        # Calcul de la pente moyenne
        slopes = []
        for i in range(1, len(times)):
            if lengths[i] != lengths[i - 1]:
                slope = (times[i] - times[i - 1]) / (
                    lengths[i] - lengths[i - 1]
                )
                slopes.append(slope)

        if not slopes:
            return 1.0

        return sum(slopes) / len(slopes)

    def _calculate_space_growth_rate(
        self, memory_usage: List[int], tape_lengths: List[int]
    ) -> float:
        """Calcule le taux de croissance spatiale."""
        if len(memory_usage) < 2:
            return 1.0

        # Calcul de la pente moyenne
        slopes = []
        for i in range(1, len(memory_usage)):
            if tape_lengths[i] != tape_lengths[i - 1]:
                slope = (memory_usage[i] - memory_usage[i - 1]) / (
                    tape_lengths[i] - tape_lengths[i - 1]
                )
                slopes.append(slope)

        if not slopes:
            return 1.0

        return sum(slopes) / len(slopes)

    def _calculate_time_metrics(
        self,
        performance_data: Dict[str, Any],
        _complexity_class: ComplexityClass,
    ) -> Dict[str, Any]:
        """Calcule les métriques temporelles."""
        execution_times = performance_data["execution_times"]

        if not execution_times:
            return {
                "average_execution_time": 0.0,
                "worst_case_time": 0.0,
                "best_case_time": 0.0,
                "total_execution_time": 0.0,
            }

        return {
            "average_execution_time": sum(execution_times)
            / len(execution_times),
            "worst_case_time": max(execution_times),
            "best_case_time": min(execution_times),
            "total_execution_time": sum(execution_times),
        }

    def _calculate_space_metrics(
        self, memory_data: Dict[str, Any], _complexity_class: ComplexityClass
    ) -> Dict[str, Any]:
        """Calcule les métriques spatiales."""
        memory_usage = memory_data["memory_usage"]

        if not memory_usage:
            return {"average_memory": 0, "peak_memory": 0, "total_memory": 0}

        return {
            "average_memory": sum(memory_usage) / len(memory_usage),
            "peak_memory": max(memory_usage),
            "total_memory": sum(memory_usage),
        }

    def _calculate_confidence_level(self, data: Dict[str, Any]) -> float:
        """Calcule le niveau de confiance de l'analyse."""
        error_count = data.get("error_count", 0)
        timeout_count = data.get("timeout_count", 0)
        total_tests = (
            len(data.get("execution_times", [])) + error_count + timeout_count
        )

        if total_tests == 0:
            return 0.0

        success_rate = (
            total_tests - error_count - timeout_count
        ) / total_tests
        return min(success_rate, 1.0)

    def _generate_test_cases(
        self, machine: Any, sample_size: int
    ) -> List[str]:
        """Génère des cas de test pour l'analyse."""
        test_cases = []

        # Alphabet de la machine
        alphabet = (
            list(machine.alphabet)
            if hasattr(machine, "alphabet")
            else ["a", "b"]
        )

        # Génération de chaînes de différentes longueurs
        for length in range(1, min(sample_size // 10 + 1, 20)):
            test_cases.extend(
                self._generate_strings_of_length(alphabet, length)
            )

        # Limiter la taille
        return test_cases[:sample_size]

    def _get_cache_key(self, machine: Any, analysis_type: str) -> str:
        """Génère une clé de cache pour une machine et un type d'analyse."""
        machine_type = type(machine).__name__
        machine_id = id(machine)
        return f"{machine_type}_{machine_id}_{analysis_type}"

    def _monitor_memory(self) -> None:
        """Monitore l'usage mémoire en temps réel."""
        if not psutil:
            return

        while True:
            try:
                memory_info = psutil.Process().memory_info()
                self._current_memory_usage = memory_info.rss

                time.sleep(0.1)  # Monitoring toutes les 100ms
            except Exception:
                break

    def _monitor_cpu(self) -> None:
        """Monitore l'usage CPU en temps réel."""
        if not psutil:
            return

        while True:
            try:
                cpu_percent = psutil.cpu_percent()
                self._current_cpu_usage = cpu_percent

                time.sleep(0.1)  # Monitoring toutes les 100ms
            except Exception:
                break

    def get_resource_usage(self) -> Dict[str, Any]:
        """Retourne l'usage actuel des ressources."""
        return {
            "memory_usage": getattr(self, "_current_memory_usage", 0),
            "cpu_usage": getattr(self, "_current_cpu_usage", 0),
            "analysis_stats": self._analysis_stats.copy(),
        }
