"""
Machine de Turing déterministe.

Ce module implémente la classe DTM qui représente une machine de Turing
déterministe avec des optimisations spécifiques pour améliorer les
performances.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
import time
from collections import defaultdict

from ..tm import TM
from .dtm_configuration import DTMConfiguration
from ...interfaces.deterministic_turing_machine import (
    IDeterministicTuringMachine,
)
from ...interfaces.turing_machine import TapeDirection
from ...exceptions.dtm_exceptions import (
    InvalidDTMError,
    DTMSimulationError,
    DTMOptimizationError,
    DTMCacheError,
)
from ...exceptions.tm_exceptions import InvalidStateError


class DTM(TM, IDeterministicTuringMachine):
    """Machine de Turing déterministe avec optimisations spécifiques.

    Cette classe étend la classe TM de base avec des contraintes de
    déterminisme et des optimisations de performance pour les machines de
    Turing déterministes.

    :param states: Ensemble des états de la machine
    :param alphabet: Alphabet d'entrée
    :param tape_alphabet: Alphabet de la bande (incluant le symbole blanc)
    :param transitions: Fonction de transition déterministe
    :param initial_state: État initial
    :param accept_states: États d'acceptation
    :param reject_states: États de rejet
    :param blank_symbol: Symbole blanc (par défaut "B")
    :param name: Nom optionnel de la machine
    :param enable_optimizations: Active les optimisations (par défaut True)
    :raises InvalidDTMError: Si la machine n'est pas valide ou déterministe
    """

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        tape_alphabet: Set[str],
        transitions: Dict[Tuple[str, str], Tuple[str, str, TapeDirection]],
        initial_state: str,
        accept_states: Set[str],
        reject_states: Set[str],
        blank_symbol: str = "B",
        name: Optional[str] = None,
        enable_optimizations: bool = True,
    ) -> None:
        """Initialise une machine de Turing déterministe.

        :param states: Ensemble des états
        :param alphabet: Alphabet d'entrée
        :param tape_alphabet: Alphabet de la bande
        :param transitions: Fonction de transition déterministe
        :param initial_state: État initial
        :param accept_states: États d'acceptation
        :param reject_states: États de rejet
        :param blank_symbol: Symbole blanc
        :param name: Nom optionnel de la machine
        :param enable_optimizations: Active les optimisations
        :raises InvalidDTMError: Si la machine n'est pas valide ou déterministe
        """
        # Optimisations (doit être défini avant l'appel au parent)
        self._enable_optimizations = enable_optimizations
        self._transition_cache = {}
        self._state_cache = {}

        # Appel du constructeur parent
        super().__init__(
            states,
            alphabet,
            tape_alphabet,
            transitions,
            initial_state,
            accept_states,
            reject_states,
            blank_symbol,
            name,
        )

        # Validation du déterminisme
        determinism_errors = self.validate_determinism()
        if determinism_errors:
            error_msg = (
                f"Machine is not deterministic: "
                f"{'; '.join(determinism_errors)}"
            )
            raise InvalidDTMError(error_msg)

        if enable_optimizations:
            self._build_optimization_caches()

    def validate_determinism(self) -> List[str]:
        """Valide le déterminisme de la machine.

        :return: Liste des erreurs de déterminisme
        """
        errors = []
        transition_counts = defaultdict(int)

        # Compter les transitions pour chaque (état, symbole)
        for (state, symbol), _ in self._transitions.items():
            transition_counts[(state, symbol)] += 1

        # Vérifier qu'il n'y a qu'une seule transition par (état, symbole)
        for (state, symbol), count in transition_counts.items():
            if count > 1:
                error_msg = (
                    f"Multiple transitions from state '{state}' "
                    f"on symbol '{symbol}'"
                )
                errors.append(error_msg)

        # Vérifier que tous les états ont des transitions définies pour tous
        # les symboles
        for state in self._states:
            if (
                state not in self._accept_states
                and state not in self._reject_states
            ):
                for symbol in self._tape_alphabet:
                    if (state, symbol) not in self._transitions:
                        error_msg = (
                            f"No transition defined from state '{state}' "
                            f"on symbol '{symbol}'"
                        )
                        errors.append(error_msg)

        return errors

    def _build_optimization_caches(self) -> None:
        """Construit les caches d'optimisation."""
        try:
            # Cache des transitions par état
            self._state_transitions = defaultdict(dict)
            for (state, symbol), (
                new_state,
                write_symbol,
                direction,
            ) in self._transitions.items():
                self._state_transitions[state][symbol] = (
                    new_state,
                    write_symbol,
                    direction,
                )

            # Cache des états d'arrêt
            self._halting_states = self._accept_states | self._reject_states

            # Cache des symboles fréquents
            self._symbol_frequency = defaultdict(int)
            for (_, symbol), _ in self._transitions.items():
                self._symbol_frequency[symbol] += 1

        except Exception as e:
            raise DTMCacheError(
                f"Failed to build optimization caches: {e}"
            ) from e

    def get_next_configuration(
        self, current_state: str, tape_symbol: str
    ) -> Optional[Tuple[str, str, TapeDirection]]:
        """Récupère la prochaine configuration de manière déterministe.

        :param current_state: État actuel
        :param tape_symbol: Symbole lu sur la bande
        :return: Transition (nouvel_état, symbole_écrit, direction) ou None
        :raises InvalidStateError: Si l'état n'existe pas
        """
        if current_state not in self._states:
            raise InvalidStateError(f"State '{current_state}' not in states")

        # Utilisation du cache si disponible
        if self._enable_optimizations and hasattr(self, "_state_transitions"):
            return self._state_transitions[current_state].get(tape_symbol)

        # Fallback vers la méthode parent
        return self.step(current_state, tape_symbol)

    def simulate_deterministic(
        self, input_string: str, max_steps: int = 10000
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Simule l'exécution déterministe de la machine.

        :param input_string: Chaîne d'entrée
        :param max_steps: Nombre maximum d'étapes
        :return: Tuple (accepté, trace_d_exécution)
        :raises DTMSimulationError: En cas d'erreur de simulation
        """
        try:
            trace = []
            tape = input_string
            head_position = 0
            current_state = self._initial_state
            step_count = 0

            # Configuration initiale
            config = DTMConfiguration(
                current_state, tape, head_position, step_count
            )
            trace.append(self._config_to_dict(config))

            # Simulation optimisée
            while step_count < max_steps:
                # Vérification rapide des états d'arrêt
                if (
                    hasattr(self, "_halting_states")
                    and current_state in self._halting_states
                ):
                    is_accepting = current_state in self._accept_states
                    config = DTMConfiguration(
                        current_state,
                        tape,
                        head_position,
                        step_count,
                        is_accepting=is_accepting,
                        is_rejecting=not is_accepting,
                    )
                    trace.append(self._config_to_dict(config))
                    return is_accepting, trace

                # Lecture du symbole actuel
                current_symbol = self._get_tape_symbol(tape, head_position)

                # Recherche optimisée de la transition
                transition = self.get_next_configuration(
                    current_state, current_symbol
                )
                if transition is None:
                    # Pas de transition définie - rejet
                    config = DTMConfiguration(
                        current_state,
                        tape,
                        head_position,
                        step_count,
                        is_rejecting=True,
                    )
                    trace.append(self._config_to_dict(config))
                    return False, trace

                # Application de la transition
                new_state, write_symbol, direction = transition
                tape = self._write_to_tape(tape, head_position, write_symbol)
                head_position = self._move_head(head_position, direction)
                current_state = new_state
                step_count += 1

                # Enregistrement de la configuration
                config = DTMConfiguration(
                    current_state, tape, head_position, step_count
                )
                trace.append(self._config_to_dict(config))

            # Timeout - considéré comme rejet
            config = DTMConfiguration(
                current_state,
                tape,
                head_position,
                step_count,
                is_rejecting=True,
            )
            trace.append(self._config_to_dict(config))
            return False, trace

        except Exception as e:
            raise DTMSimulationError(
                f"Deterministic simulation error: {e}"
            ) from e

    def _config_to_dict(self, config: DTMConfiguration) -> Dict[str, Any]:
        """Convertit une configuration DTM en dictionnaire pour la trace.

        :param config: Configuration à convertir
        :return: Dictionnaire représentant la configuration
        """
        return {
            "state": config.state,
            "tape": config.tape,
            "head_position": config.head_position,
            "step_count": config.step_count,
            "current_symbol": self._get_tape_symbol(
                config.tape, config.head_position
            ),
            "is_accepting": config.is_accepting,
            "is_rejecting": config.is_rejecting,
        }

    def validate(self) -> List[str]:
        """Valide la cohérence de la machine déterministe.

        :return: Liste des erreurs de validation
        """
        errors = super().validate()

        # Validation spécifique au déterminisme
        determinism_errors = self.validate_determinism()
        errors.extend(determinism_errors)

        # Validation des optimisations
        if self._enable_optimizations:
            optimization_errors = self._validate_optimizations()
            errors.extend(optimization_errors)

        return errors

    def _validate_optimizations(self) -> List[str]:
        """Valide les optimisations."""
        errors = []

        # Vérifier la cohérence du cache
        if hasattr(self, "_state_transitions"):
            for state, transitions in self._state_transitions.items():
                if state not in self._states:
                    errors.append(f"Cache references unknown state '{state}'")
                for symbol, _ in transitions.items():
                    if symbol not in self._tape_alphabet:
                        errors.append(
                            f"Cache references unknown symbol '{symbol}'"
                        )

        return errors

    @property
    def is_deterministic(self) -> bool:
        """Vérifie si la machine est déterministe.

        :return: True si la machine est déterministe
        """
        return len(self.validate_determinism()) == 0

    @property
    def optimization_enabled(self) -> bool:
        """Indique si les optimisations sont activées.

        :return: True si les optimisations sont activées
        """
        return self._enable_optimizations

    @property
    def cache_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache.

        :return: Dictionnaire contenant les statistiques du cache
        """
        if not self._enable_optimizations:
            return {"enabled": False}

        return {
            "enabled": True,
            "state_transitions_cache_size": len(
                getattr(self, "_state_transitions", {})
            ),
            "halting_states_cache_size": len(
                getattr(self, "_halting_states", set())
            ),
            "symbol_frequency_cache_size": len(
                getattr(self, "_symbol_frequency", {})
            ),
        }

    def optimize_transitions(self) -> "DTM":
        """Optimise les transitions pour améliorer les performances.

        :return: Nouvelle DTM optimisée
        :raises DTMOptimizationError: Si l'optimisation échoue
        """
        try:
            # Création d'une nouvelle DTM avec transitions optimisées
            optimized_transitions = self._optimize_transition_table()

            return DTM(
                states=self._states,
                alphabet=self._alphabet,
                tape_alphabet=self._tape_alphabet,
                transitions=optimized_transitions,
                initial_state=self._initial_state,
                accept_states=self._accept_states,
                reject_states=self._reject_states,
                blank_symbol=self._blank_symbol,
                name=f"{self._name}_optimized",
                enable_optimizations=True,
            )
        except (KeyError, ValueError, TypeError) as e:
            raise DTMOptimizationError(f"Failed to optimize DTM: {e}") from e

    def _optimize_transition_table(
        self,
    ) -> Dict[Tuple[str, str], Tuple[str, str, TapeDirection]]:
        """Optimise la table de transitions.

        :return: Table de transitions optimisée
        """
        optimized = {}

        # Réorganisation des transitions par fréquence d'usage
        transition_frequency = defaultdict(int)
        for (state, symbol), _ in self._transitions.items():
            transition_frequency[(state, symbol)] += 1

        # Tri par fréquence décroissante
        sorted_transitions = sorted(
            self._transitions.items(),
            key=lambda x: transition_frequency[x[0]],
            reverse=True,
        )

        # Reconstruction de la table optimisée
        for (state, symbol), (
            new_state,
            write_symbol,
            direction,
        ) in sorted_transitions:
            optimized[(state, symbol)] = (new_state, write_symbol, direction)

        return optimized

    def analyze_performance(
        self, test_cases: List[str], max_steps: int = 10000
    ) -> Dict[str, Any]:
        """Analyse les performances de la machine.

        :param test_cases: Cas de test pour l'analyse
        :param max_steps: Nombre maximum d'étapes par test
        :return: Statistiques de performance
        """
        results = {
            "total_tests": len(test_cases),
            "successful_simulations": 0,
            "failed_simulations": 0,
            "average_execution_time": 0.0,
            "average_steps": 0,
            "max_execution_time": 0.0,
            "min_execution_time": float("inf"),
            "timeout_count": 0,
        }

        total_time = 0.0
        total_steps = 0

        for test_case in test_cases:
            start_time = time.time()
            try:
                _, trace = self.simulate_deterministic(test_case, max_steps)
                execution_time = time.time() - start_time

                results["successful_simulations"] += 1
                total_time += execution_time
                total_steps += len(trace)

                results["max_execution_time"] = max(
                    results["max_execution_time"], execution_time
                )
                results["min_execution_time"] = min(
                    results["min_execution_time"], execution_time
                )

                if len(trace) >= max_steps:
                    results["timeout_count"] += 1

            except (DTMSimulationError, ValueError, TypeError):
                results["failed_simulations"] += 1

        if results["successful_simulations"] > 0:
            results["average_execution_time"] = (
                total_time / results["successful_simulations"]
            )
            results["average_steps"] = (
                total_steps / results["successful_simulations"]
            )

        if results["min_execution_time"] == float("inf"):
            results["min_execution_time"] = 0.0

        return results

    def to_dict(self) -> Dict[str, Any]:
        """Convertit la machine en dictionnaire avec optimisations.

        :return: Représentation dictionnaire de la machine
        """
        base_dict = super().to_dict()
        base_dict.update(
            {
                "type": "DTM",
                "is_deterministic": self.is_deterministic,
                "optimization_enabled": self._enable_optimizations,
                "cache_stats": self.cache_stats,
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DTM":
        """Crée une machine à partir d'un dictionnaire.

        :param data: Données de la machine
        :return: Instance de DTM
        :raises InvalidDTMError: Si les données sont invalides
        """
        try:
            # Reconstruction des transitions
            transitions = {}
            for key, value in data["transitions"].items():
                state, symbol = key.split(",", 1)
                new_state, write_symbol, direction_str = value
                direction = TapeDirection(direction_str)
                transitions[(state, symbol)] = (
                    new_state,
                    write_symbol,
                    direction,
                )

            return cls(
                states=set(data["states"]),
                alphabet=set(data["alphabet"]),
                tape_alphabet=set(data["tape_alphabet"]),
                transitions=transitions,
                initial_state=data["initial_state"],
                accept_states=set(data["accept_states"]),
                reject_states=set(data["reject_states"]),
                blank_symbol=data["blank_symbol"],
                name=data.get("name"),
                enable_optimizations=data.get("optimization_enabled", True),
            )
        except (KeyError, ValueError, TypeError) as e:
            raise InvalidDTMError(f"Invalid DTM data: {e}") from e

    def __str__(self) -> str:
        """Représentation textuelle de la machine.

        :return: Représentation textuelle
        """
        deterministic_str = (
            " (Deterministic)"
            if self.is_deterministic
            else " (Non-deterministic)"
        )
        optimized_str = " (Optimized)" if self._enable_optimizations else ""
        return (
            f"DTM({self._name}){deterministic_str}{optimized_str} - "
            f"States: {len(self._states)}, "
            f"Transitions: {len(self._transitions)}"
        )

    def __repr__(self) -> str:
        """Représentation technique de la machine.

        :return: Représentation technique
        """
        return (
            f"DTM(name='{self._name}', deterministic={self.is_deterministic}, "
            f"optimized={self._enable_optimizations}, "
            f"states={len(self._states)}, "
            f"transitions={len(self._transitions)})"
        )

    def get_detailed_info(self) -> Dict[str, Any]:
        """Retourne des informations détaillées sur la machine.

        :return: Dictionnaire contenant les informations détaillées
        """
        return {
            "name": self._name,
            "type": "DTM",
            "states_count": len(self._states),
            "alphabet_size": len(self._alphabet),
            "tape_alphabet_size": len(self._tape_alphabet),
            "transitions_count": len(self._transitions),
            "accept_states_count": len(self._accept_states),
            "reject_states_count": len(self._reject_states),
            "is_deterministic": self.is_deterministic,
            "optimization_enabled": self._enable_optimizations,
            "cache_stats": self.cache_stats,
        }
