"""
Machine de Turing non-déterministe.

Ce module implémente la classe NTM qui représente une machine de Turing
non-déterministe avec simulation parallèle optimisée.
"""

import time
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Set, Tuple

from ..tm import TM
from .ntm_configuration import NTMConfiguration
from ...interfaces.non_deterministic_turing_machine import (
    INonDeterministicTuringMachine,
    NTMTransition,
)
from ...interfaces.turing_machine import TapeDirection
from ...exceptions.ntm_exceptions import (
    InvalidNTMError,
    NTMOptimizationError,
)
from ...exceptions.tm_exceptions import InvalidStateError


class NTM(TM, INonDeterministicTuringMachine):
    """Machine de Turing non-déterministe avec simulation parallèle optimisée.

    Cette classe étend la classe TM de base avec des capacités
    non-déterministes,
    incluant la gestion des transitions multiples avec poids probabilistes,
    la simulation parallèle avec BFS, et l'analyse des arbres de calcul.

    :param states: Ensemble des états de la machine
    :param alphabet: Alphabet d'entrée
    :param tape_alphabet: Alphabet de la bande (incluant le symbole blanc)
    :param transitions: Fonction de transition non-déterministe
    :param initial_state: État initial
    :param accept_states: États d'acceptation
    :param reject_states: États de rejet
    :param blank_symbol: Symbole blanc (par défaut "B")
    :param name: Nom optionnel de la machine
    :param enable_parallel_simulation: Active la simulation parallèle
    :param max_branches: Nombre maximum de branches simultanées
    :raises InvalidNTMError: Si la machine n'est pas valide
    """

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        tape_alphabet: Set[str],
        transitions: Dict[
            Tuple[str, str], List[Tuple[str, str, TapeDirection, float]]
        ],
        initial_state: str,
        accept_states: Set[str],
        reject_states: Set[str],
        blank_symbol: str = "B",
        name: Optional[str] = None,
        enable_parallel_simulation: bool = True,
        max_branches: int = 1000,
    ) -> None:
        """Initialise une machine de Turing non-déterministe.

        :param states: Ensemble des états
        :param alphabet: Alphabet d'entrée
        :param tape_alphabet: Alphabet de la bande
        :param transitions: Fonction de transition non-déterministe
        :param initial_state: État initial
        :param accept_states: États d'acceptation
        :param reject_states: États de rejet
        :param blank_symbol: Symbole blanc
        :param name: Nom optionnel de la machine
        :param enable_parallel_simulation: Active la simulation parallèle
        :param max_branches: Nombre maximum de branches simultanées
        :raises InvalidNTMError: Si la machine n'est pas valide
        """
        # Conversion des transitions non-déterministes
        self._ntm_transitions = transitions
        self._enable_parallel_simulation = enable_parallel_simulation
        self._max_branches = max_branches

        # Construction des transitions déterministes pour compatibilité
        self._build_deterministic_transitions()

        # Appel du constructeur parent avec transitions déterministes
        # construites
        super().__init__(
            states,
            alphabet,
            tape_alphabet,
            self._transitions,  # Transitions déterministes construites
            initial_state,
            accept_states,
            reject_states,
            blank_symbol,
            name,
        )

        # Validation du non-déterminisme
        non_determinism_errors = self.validate_non_determinism()
        if non_determinism_errors:
            raise InvalidNTMError(
                f"Machine non-determinism validation failed: "
                f"{'; '.join(non_determinism_errors)}"
            )

        # Optimisations
        self._branch_cache = {}
        self._computation_tree_cache = {}

        if enable_parallel_simulation:
            self._build_parallel_caches()

    def _build_deterministic_transitions(self) -> None:
        """Construit les transitions déterministes pour compatibilité."""
        deterministic_transitions = {}
        for (state, symbol), transitions_list in self._ntm_transitions.items():
            if transitions_list:
                # Prendre la première transition comme transition déterministe
                new_state, write_symbol, direction, _ = transitions_list[0]
                deterministic_transitions[(state, symbol)] = (
                    new_state,
                    write_symbol,
                    direction,
                )

        # Mise à jour des transitions parent
        self._transitions = deterministic_transitions

    def validate_non_determinism(self) -> List[str]:
        """Valide la cohérence non-déterministe de la machine.

        :return: Liste des erreurs de validation
        """
        errors = []

        # Note: On permet les NTM déterministes mais on les marque comme
        # telles. La vérification du non-déterminisme se fait via la
        # propriété is_non_deterministic

        # Vérifier la cohérence des transitions
        for (state, symbol), transitions_list in self._ntm_transitions.items():
            if state not in self._states:
                errors.append(f"Transition references unknown state '{state}'")
            if symbol not in self._tape_alphabet:
                errors.append(
                    f"Transition references unknown tape symbol '{symbol}'"
                )

            for transition in transitions_list:
                new_state, write_symbol, direction, weight = transition
                if new_state not in self._states:
                    errors.append(
                        f"Transition references unknown target state "
                        f"'{new_state}'"
                    )
                if write_symbol not in self._tape_alphabet:
                    errors.append(
                        f"Transition writes unknown symbol '{write_symbol}'"
                    )
                if not isinstance(direction, TapeDirection):
                    errors.append(f"Invalid tape direction '{direction}'")
                if weight <= 0:
                    errors.append(
                        f"Invalid transition weight '{weight}' - "
                        f"must be positive"
                    )

        return errors

    def simulate_non_deterministic(
        self,
        input_string: str,
        max_steps: int = 10000,
        max_branches: int = 1000,
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Simule l'exécution non-déterministe de la machine.

        :param input_string: Chaîne d'entrée
        :param max_steps: Nombre maximum d'étapes par branche
        :param max_branches: Nombre maximum de branches simultanées
        :return: Tuple (accepté, trace_d_exécution)
        :raises NTMSimulationError: En cas d'erreur de simulation
        """
        start_time = time.time()
        trace = []

        # File de configurations à explorer (BFS)
        config_queue = deque()
        initial_config = NTMConfiguration(
            state=self._initial_state,
            tape=input_string,
            head_position=0,
            step_count=0,
            branch_id=0,
            weight=1.0,
        )
        config_queue.append(initial_config)

        # Cache des configurations visitées pour éviter les boucles
        visited_configs = set()

        # Statistiques de simulation
        total_branches_explored = 0
        accepting_branches = []

        while config_queue and total_branches_explored < max_branches:
            current_config = config_queue.popleft()
            total_branches_explored += 1

            # Vérification des états d'arrêt
            if current_config.state in self._accept_states:
                accepting_branches.append(current_config)
                trace.append(self._config_to_dict(current_config))
                continue

            if current_config.state in self._reject_states:
                trace.append(self._config_to_dict(current_config))
                continue

            # Limitation du nombre d'étapes
            if current_config.step_count >= max_steps:
                trace.append(self._config_to_dict(current_config))
                continue

            # Lecture du symbole actuel
            current_symbol = self._get_tape_symbol(
                current_config.tape, current_config.head_position
            )

            # Récupération de toutes les transitions possibles
            transitions = self.get_all_transitions(
                current_config.state, current_symbol
            )

            if not transitions:
                # Pas de transition définie - rejet
                reject_config = NTMConfiguration(
                    state=current_config.state,
                    tape=current_config.tape,
                    head_position=current_config.head_position,
                    step_count=current_config.step_count,
                    branch_id=current_config.branch_id,
                    is_rejecting=True,
                    weight=current_config.weight,
                )
                trace.append(self._config_to_dict(reject_config))
                continue

            # Exploration de toutes les branches
            for i, transition in enumerate(transitions):
                new_state, write_symbol, direction, transition_weight = (
                    transition.new_state,
                    transition.write_symbol,
                    transition.direction,
                    transition.weight,
                )

                # Nouvelle configuration
                new_tape = self._write_to_tape(
                    current_config.tape,
                    current_config.head_position,
                    write_symbol,
                )
                new_head_position = self._move_head(
                    current_config.head_position, direction
                )
                new_weight = current_config.weight * transition_weight

                new_config = NTMConfiguration(
                    state=new_state,
                    tape=new_tape,
                    head_position=new_head_position,
                    step_count=current_config.step_count + 1,
                    branch_id=current_config.branch_id * 10 + i,
                    weight=new_weight,
                )

                # Éviter les boucles infinies
                config_key = new_config.get_configuration_key()
                if config_key not in visited_configs:
                    visited_configs.add(config_key)
                    config_queue.append(new_config)
                    trace.append(self._config_to_dict(new_config))

        # Détermination du résultat
        is_accepted = len(accepting_branches) > 0

        # Ajout des statistiques à la trace
        execution_time = time.time() - start_time
        trace.append(
            {
                "type": "simulation_summary",
                "accepted": is_accepted,
                "total_branches_explored": total_branches_explored,
                "accepting_branches_count": len(accepting_branches),
                "execution_time": execution_time,
                "max_branches_reached": total_branches_explored
                >= max_branches,
            }
        )

        return is_accepted, trace

    def get_all_transitions(
        self, current_state: str, tape_symbol: str
    ) -> List[NTMTransition]:
        """Récupère toutes les transitions possibles pour un état et symbole.

        :param current_state: État actuel
        :param tape_symbol: Symbole lu sur la bande
        :return: Liste des transitions possibles
        :raises InvalidStateError: Si l'état n'existe pas
        """
        if current_state not in self._states:
            raise InvalidStateError(f"State '{current_state}' not in states")

        transition_key = (current_state, tape_symbol)
        transitions_list = self._ntm_transitions.get(transition_key, [])

        return [
            NTMTransition(new_state, write_symbol, direction, weight)
            for new_state, write_symbol, direction, weight in transitions_list
        ]

    def get_transition_probability(
        self,
        current_state: str,
        tape_symbol: str,
        target_state: str,
        write_symbol: str,
        direction: TapeDirection,
    ) -> float:
        """Calcule la probabilité d'une transition spécifique.

        :param current_state: État actuel
        :param tape_symbol: Symbole lu
        :param target_state: État cible
        :param write_symbol: Symbole à écrire
        :param direction: Direction de déplacement
        :return: Probabilité de la transition
        """
        transitions = self.get_all_transitions(current_state, tape_symbol)
        if not transitions:
            return 0.0

        # Recherche de la transition spécifique
        for transition in transitions:
            if (
                transition.new_state == target_state
                and transition.write_symbol == write_symbol
                and transition.direction == direction
            ):
                return transition.weight

        return 0.0

    def analyze_computation_tree(
        self, input_string: str, max_depth: int = 100
    ) -> Dict[str, Any]:
        """Analyse l'arbre de calcul pour une entrée donnée.

        :param input_string: Chaîne d'entrée
        :param max_depth: Profondeur maximale de l'arbre
        :return: Analyse détaillée de l'arbre de calcul
        """
        if input_string in self._computation_tree_cache:
            return self._computation_tree_cache[input_string]

        tree_analysis = {
            "input": input_string,
            "total_nodes": 0,
            "accepting_paths": 0,
            "rejecting_paths": 0,
            "infinite_paths": 0,
            "max_depth_reached": 0,
            "branching_factor": 0.0,
            "average_path_length": 0.0,
            "computation_complexity": "unknown",
        }

        # Construction de l'arbre avec DFS limité
        visited_nodes = set()
        accepting_paths = []
        rejecting_paths = []
        infinite_paths = []

        def explore_tree(
            config: NTMConfiguration, depth: int, path_weight: float
        ):
            if depth > max_depth:
                infinite_paths.append((config, depth, path_weight))
                return

            node_key = config.get_configuration_key()
            if node_key in visited_nodes:
                infinite_paths.append((config, depth, path_weight))
                return

            visited_nodes.add(node_key)
            tree_analysis["total_nodes"] += 1
            tree_analysis["max_depth_reached"] = max(
                tree_analysis["max_depth_reached"], depth
            )

            # Vérification des états d'arrêt
            if config.state in self._accept_states:
                accepting_paths.append((config, depth, path_weight))
                return

            if config.state in self._reject_states:
                rejecting_paths.append((config, depth, path_weight))
                return

            # Exploration des transitions
            current_symbol = self._get_tape_symbol(
                config.tape, config.head_position
            )
            transitions = self.get_all_transitions(
                config.state, current_symbol
            )

            if not transitions:
                rejecting_paths.append((config, depth, path_weight))
                return

            # Exploration de chaque branche
            for transition in transitions:
                new_state, write_symbol, direction, weight = (
                    transition.new_state,
                    transition.write_symbol,
                    transition.direction,
                    transition.weight,
                )
                new_tape = self._write_to_tape(
                    config.tape, config.head_position, write_symbol
                )
                new_head_position = self._move_head(
                    config.head_position, direction
                )

                new_config = NTMConfiguration(
                    state=new_state,
                    tape=new_tape,
                    head_position=new_head_position,
                    step_count=config.step_count + 1,
                    branch_id=config.branch_id,
                    weight=path_weight * weight,
                )

                explore_tree(new_config, depth + 1, path_weight * weight)

        # Démarrage de l'exploration
        initial_config = NTMConfiguration(
            state=self._initial_state,
            tape=input_string,
            head_position=0,
            step_count=0,
            branch_id=0,
            weight=1.0,
        )

        explore_tree(initial_config, 0, 1.0)

        # Calcul des statistiques
        tree_analysis["accepting_paths"] = len(accepting_paths)
        tree_analysis["rejecting_paths"] = len(rejecting_paths)
        tree_analysis["infinite_paths"] = len(infinite_paths)

        if tree_analysis["total_nodes"] > 0:
            # Calculer le facteur de branchement moyen
            total_branches = 0
            branch_count = 0
            for transitions_list in self._ntm_transitions.values():
                if len(transitions_list) > 1:
                    total_branches += len(transitions_list)
                    branch_count += 1
            tree_analysis["branching_factor"] = (
                total_branches / branch_count if branch_count > 0 else 0
            )
            total_path_length = sum(
                depth for _, depth, _ in accepting_paths + rejecting_paths
            )
            total_paths = len(accepting_paths) + len(rejecting_paths)
            if total_paths > 0:
                tree_analysis["average_path_length"] = (
                    total_path_length / total_paths
                )

        # Classification de la complexité
        if tree_analysis["infinite_paths"] > 0:
            tree_analysis["computation_complexity"] = "infinite"
        elif tree_analysis["accepting_paths"] > 0:
            tree_analysis["computation_complexity"] = "accepting"
        else:
            tree_analysis["computation_complexity"] = "rejecting"

        # Cache du résultat
        self._computation_tree_cache[input_string] = tree_analysis
        return tree_analysis

    def _build_parallel_caches(self) -> None:
        """Construit les caches pour l'optimisation parallèle."""
        # Cache des transitions par état pour accès rapide
        self._state_transitions_cache = defaultdict(dict)
        for (state, symbol), transitions_list in self._ntm_transitions.items():
            self._state_transitions_cache[state][symbol] = transitions_list

        # Cache des états d'arrêt
        self._halting_states_cache = self._accept_states | self._reject_states

        # Cache des poids de transition
        self._transition_weights_cache = {}
        for (state, symbol), transitions_list in self._ntm_transitions.items():
            total_weight = sum(weight for _, _, _, weight in transitions_list)
            self._transition_weights_cache[(state, symbol)] = total_weight

    def optimize_parallel_computation(self) -> "NTM":
        """Optimise les calculs parallèles.

        :return: Nouvelle NTM optimisée
        :raises NTMOptimizationError: Si l'optimisation échoue
        """
        try:
            # Réorganisation des transitions par poids décroissant
            optimized_transitions = {}
            for (
                state,
                symbol,
            ), transitions_list in self._ntm_transitions.items():
                # Tri par poids décroissant pour explorer les branches les
                # plus probables en premier
                sorted_transitions = sorted(
                    transitions_list, key=lambda x: x[3], reverse=True
                )
                optimized_transitions[(state, symbol)] = sorted_transitions

            return NTM(
                states=self._states,
                alphabet=self._alphabet,
                tape_alphabet=self._tape_alphabet,
                transitions=optimized_transitions,
                initial_state=self._initial_state,
                accept_states=self._accept_states,
                reject_states=self._reject_states,
                blank_symbol=self._blank_symbol,
                name=f"{self._name}_optimized",
                enable_parallel_simulation=True,
                max_branches=self._max_branches,
            )
        except Exception as e:
            raise NTMOptimizationError(f"Failed to optimize NTM: {e}") from e

    def _config_to_dict(self, config: NTMConfiguration) -> Dict[str, Any]:
        """Convertit une configuration en dictionnaire.

        :param config: Configuration à convertir
        :return: Dictionnaire représentant la configuration
        """
        return {
            "state": config.state,
            "tape": config.tape,
            "head_position": config.head_position,
            "step_count": config.step_count,
            "branch_id": config.branch_id,
            "is_accepting": config.is_accepting,
            "is_rejecting": config.is_rejecting,
            "weight": config.weight,
        }

    def _get_tape_symbol(self, tape: str, position: int) -> str:
        """Récupère le symbole à une position donnée sur la bande.

        :param tape: Contenu de la bande
        :param position: Position sur la bande
        :return: Symbole à la position donnée
        """
        if 0 <= position < len(tape):
            return tape[position]
        return self._blank_symbol

    def _write_to_tape(self, tape: str, position: int, symbol: str) -> str:
        """Écrit un symbole à une position donnée sur la bande.

        :param tape: Contenu actuel de la bande
        :param position: Position où écrire
        :param symbol: Symbole à écrire
        :return: Nouveau contenu de la bande
        """
        if position < 0:
            # Extension vers la gauche
            return symbol + tape
        elif position >= len(tape):
            # Extension vers la droite
            return tape + symbol
        else:
            # Modification à l'intérieur
            return tape[:position] + symbol + tape[position + 1:]

    def _move_head(self, position: int, direction: TapeDirection) -> int:
        """Déplace la tête selon la direction spécifiée.

        :param position: Position actuelle de la tête
        :param direction: Direction de déplacement
        :return: Nouvelle position de la tête
        """
        if direction == TapeDirection.LEFT:
            return position - 1
        if direction == TapeDirection.RIGHT:
            return position + 1
        # STAY
        return position

    @property
    def is_non_deterministic(self) -> bool:
        """Vérifie si la machine est non-déterministe."""
        # Vérifier s'il y a au moins une transition avec plusieurs choix
        for transitions_list in self._ntm_transitions.values():
            if len(transitions_list) > 1:
                return True
        return False

    @property
    def parallel_simulation_enabled(self) -> bool:
        """Indique si la simulation parallèle est activée."""
        return self._enable_parallel_simulation

    @property
    def max_branches_limit(self) -> int:
        """Retourne la limite de branches simultanées."""
        return self._max_branches

    @property
    def cache_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache."""
        if not self._enable_parallel_simulation:
            return {"enabled": False}

        return {
            "enabled": True,
            "state_transitions_cache_size": len(self._state_transitions_cache),
            "halting_states_cache_size": len(self._halting_states_cache),
            "transition_weights_cache_size": len(
                self._transition_weights_cache
            ),
            "computation_tree_cache_size": len(self._computation_tree_cache),
        }

    def validate(self) -> List[str]:
        """Valide la cohérence de la machine non-déterministe.

        :return: Liste des erreurs de validation
        """
        errors = super().validate()

        # Validation spécifique au non-déterminisme
        non_determinism_errors = self.validate_non_determinism()
        errors.extend(non_determinism_errors)

        # Validation des optimisations
        if self._enable_parallel_simulation:
            optimization_errors = self._validate_parallel_optimizations()
            errors.extend(optimization_errors)

        return errors

    def _validate_parallel_optimizations(self) -> List[str]:
        """Valide les optimisations parallèles."""
        errors = []

        # Vérifier la cohérence du cache
        if hasattr(self, "_state_transitions_cache"):
            for (
                state,
                transitions_dict,
            ) in self._state_transitions_cache.items():
                if state not in self._states:
                    errors.append(f"Cache references unknown state '{state}'")
                for symbol in transitions_dict.keys():
                    if symbol not in self._tape_alphabet:
                        errors.append(
                            f"Cache references unknown symbol '{symbol}'"
                        )

        return errors
