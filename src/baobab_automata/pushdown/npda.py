"""
Automates à pile non-déterministes (NPDA) avec capacités parallèles.

Ce module implémente les automates à pile non-déterministes avec des
capacités avancées pour la simulation parallèle et l'optimisation des calculs.
"""

import heapq
import time
from typing import Any, Dict, List, Optional, Set, Tuple

from .abstract_pushdown_automaton import AbstractPushdownAutomaton
from .npda_configuration import NPDAConfiguration
from .npda_exceptions import (
    InvalidNPDAError,
    NPDAMemoryError,
    NPDAError,
    NPDATimeoutError,
)


class NPDA(AbstractPushdownAutomaton):
    """Automate à pile non-déterministe avec capacités avancées pour la simulation parallèle.

    Cette classe implémente un automate à pile non-déterministe avec des
    capacités spécialisées pour la simulation parallèle, la gestion des
    branches de calcul et l'optimisation des performances.
    """

    def __init__(
        self,
        states: Set[str],
        input_alphabet: Set[str],
        stack_alphabet: Set[str],
        transitions: Dict[Tuple[str, str, str], Set[Tuple[str, str]]],
        initial_state: str,
        initial_stack_symbol: str,
        final_states: Set[str],
        name: Optional[str] = None,
        max_parallel_branches: int = 1000,
    ) -> None:
        """Initialise un automate à pile non-déterministe.

        :param states: Ensemble des états
        :param input_alphabet: Alphabet d'entrée
        :param stack_alphabet: Alphabet de pile
        :param transitions: Fonction de transition non-déterministe
        :param initial_state: État initial
        :param initial_stack_symbol: Symbole initial de pile
        :param final_states: États finaux
        :param name: Nom optionnel de l'automate
        :param max_parallel_branches: Nombre maximum de branches parallèles
        :raises InvalidNPDAError: Si l'automate n'est pas valide
        """
        self._states = states
        self._input_alphabet = input_alphabet
        self._stack_alphabet = stack_alphabet
        self._transitions = transitions
        self._initial_state = initial_state
        self._initial_stack_symbol = initial_stack_symbol
        self._final_states = final_states
        self._name = name
        self._max_parallel_branches = max_parallel_branches

        # Configuration des capacités parallèles
        self._timeout = 10.0
        self._memory_limit = 100 * 1024 * 1024  # 100MB

        # Cache pour les optimisations
        self._epsilon_closure_cache: Dict[Tuple[str, str], Set[NPDAConfiguration]] = {}
        self._transition_cache: Dict[Tuple[str, str, str], Set[Tuple[str, str]]] = {}
        self._recognition_cache: Dict[str, bool] = {}

        # Statistiques de performance
        self._performance_stats = {
            "total_computations": 0,
            "parallel_branches_created": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "timeout_count": 0,
            "memory_limit_count": 0,
        }

        # Validation de l'automate
        if not self.validate():
            raise InvalidNPDAError("L'automate NPDA n'est pas valide")

    @property
    def states(self) -> Set[str]:
        """Retourne l'ensemble des états de l'automate.

        :return: Ensemble des états
        """
        return self._states

    @property
    def input_alphabet(self) -> Set[str]:
        """Retourne l'alphabet d'entrée de l'automate.

        :return: Alphabet d'entrée
        """
        return self._input_alphabet

    @property
    def stack_alphabet(self) -> Set[str]:
        """Retourne l'alphabet de pile de l'automate.

        :return: Alphabet de pile
        """
        return self._stack_alphabet

    @property
    def initial_state(self) -> str:
        """Retourne l'état initial de l'automate.

        :return: État initial
        """
        return self._initial_state

    @property
    def initial_stack_symbol(self) -> str:
        """Retourne le symbole initial de pile.

        :return: Symbole initial de pile
        """
        return self._initial_stack_symbol

    @property
    def final_states(self) -> Set[str]:
        """Retourne l'ensemble des états finaux.

        :return: États finaux
        """
        return self._final_states

    @property
    def name(self) -> Optional[str]:
        """Retourne le nom de l'automate.

        :return: Nom de l'automate ou None
        """
        return self._name

    @property
    def max_parallel_branches(self) -> int:
        """Retourne le nombre maximum de branches parallèles.

        :return: Nombre maximum de branches parallèles
        """
        return self._max_parallel_branches

    def configure_parallel_execution(
        self,
        max_branches: int = 1000,
        timeout: float = 10.0,
        memory_limit: int = 100 * 1024 * 1024,  # 100MB
    ) -> None:
        """Configure les paramètres d'exécution parallèle.

        :param max_branches: Nombre maximum de branches parallèles
        :param timeout: Timeout en secondes
        :param memory_limit: Limite de mémoire en octets
        :raises NPDAError: Si la configuration est invalide
        """
        if max_branches <= 0:
            raise NPDAError("Le nombre maximum de branches doit être positif")
        if timeout <= 0:
            raise NPDAError("Le timeout doit être positif")
        if memory_limit <= 0:
            raise NPDAError("La limite de mémoire doit être positive")

        self._max_parallel_branches = max_branches
        self._timeout = timeout
        self._memory_limit = memory_limit

    def accepts(self, word: str) -> bool:
        """Vérifie si un mot est accepté par l'automate.

        :param word: Mot à tester
        :return: True si le mot est accepté, False sinon
        :raises NPDAError: En cas d'erreur de traitement
        :raises NPDATimeoutError: Si le calcul dépasse le timeout
        :raises NPDAMemoryError: Si le calcul dépasse la limite mémoire
        """
        if not isinstance(word, str):
            raise NPDAError("Le mot doit être une chaîne de caractères")

        # Vérification du cache
        if word in self._recognition_cache:
            self._performance_stats["cache_hits"] += 1
            return self._recognition_cache[word]

        self._performance_stats["cache_misses"] += 1
        self._performance_stats["total_computations"] += 1

        try:
            result = self._simulate_word_parallel(word)
            self._recognition_cache[word] = result
            return result
        except NPDATimeoutError:
            self._performance_stats["timeout_count"] += 1
            raise
        except NPDAMemoryError:
            self._performance_stats["memory_limit_count"] += 1
            raise

    def get_transitions(
        self, state: str, input_symbol: str, stack_symbol: str
    ) -> Set[Tuple[str, str]]:
        """Récupère toutes les transitions possibles depuis un état donné.

        :param state: État source
        :param input_symbol: Symbole d'entrée (peut être ε)
        :param stack_symbol: Symbole de pile
        :return: Ensemble des transitions possibles
        :raises NPDAError: Si l'état n'existe pas
        """
        if state not in self._states:
            raise NPDAError(f"L'état '{state}' n'existe pas")

        # Vérification du cache
        cache_key = (state, input_symbol, stack_symbol)
        if cache_key in self._transition_cache:
            return self._transition_cache[cache_key]

        transitions = self._transitions.get(cache_key, set())
        self._transition_cache[cache_key] = transitions
        return transitions

    def is_final_state(self, state: str) -> bool:
        """Vérifie si un état est final.

        :param state: État à vérifier
        :return: True si l'état est final, False sinon
        """
        return state in self._final_states

    def get_reachable_states(self, from_state: str) -> Set[str]:
        """Récupère tous les états accessibles depuis un état donné.

        :param from_state: État de départ
        :return: Ensemble des états accessibles
        :raises NPDAError: Si l'état de départ n'existe pas
        """
        if from_state not in self._states:
            raise NPDAError(f"L'état '{from_state}' n'existe pas")

        visited = set()
        queue = [from_state]

        while queue:
            current_state = queue.pop(0)
            if current_state in visited:
                continue

            visited.add(current_state)

            # Parcourir toutes les transitions possibles
            for (
                state,
                input_symbol,
                stack_symbol,
            ), transitions in self._transitions.items():
                if state == current_state:
                    for next_state, _ in transitions:
                        if next_state not in visited:
                            queue.append(next_state)

        return visited

    def validate(self) -> bool:
        """Valide la cohérence de l'automate.

        :return: True si l'automate est valide, False sinon
        :raises InvalidNPDAError: Si l'automate n'est pas valide
        """
        try:
            # Vérification des états
            if not self._states:
                raise InvalidNPDAError("L'ensemble des états ne peut pas être vide")

            if self._initial_state not in self._states:
                raise InvalidNPDAError(
                    "L'état initial doit appartenir à l'ensemble des états"
                )

            if not self._final_states.issubset(self._states):
                raise InvalidNPDAError(
                    "Les états finaux doivent appartenir à l'ensemble des états"
                )

            # Vérification des alphabets
            if not self._input_alphabet:
                raise InvalidNPDAError("L'alphabet d'entrée ne peut pas être vide")

            if not self._stack_alphabet:
                raise InvalidNPDAError("L'alphabet de pile ne peut pas être vide")

            if self._initial_stack_symbol not in self._stack_alphabet:
                raise InvalidNPDAError(
                    "Le symbole initial de pile doit appartenir à l'alphabet de pile"
                )

            # Vérification des transitions
            for (
                state,
                input_symbol,
                stack_symbol,
            ), transitions in self._transitions.items():
                if state not in self._states:
                    raise InvalidNPDAError(
                        f"L'état '{state}' dans les transitions n'existe pas"
                    )

                if input_symbol != "" and input_symbol not in self._input_alphabet:
                    raise InvalidNPDAError(
                        f"Le symbole d'entrée '{input_symbol}' n'est pas dans l'alphabet d'entrée"
                    )

                if stack_symbol not in self._stack_alphabet:
                    raise InvalidNPDAError(
                        f"Le symbole de pile '{stack_symbol}' n'est pas dans l'alphabet de pile"
                    )

                for next_state, stack_symbols in transitions:
                    if next_state not in self._states:
                        raise InvalidNPDAError(
                            f"L'état de destination '{next_state}' n'existe pas"
                        )

                    for symbol in stack_symbols:
                        if symbol not in self._stack_alphabet:
                            raise InvalidNPDAError(
                                f"Le symbole de pile '{symbol}' n'est pas dans l'alphabet de pile"
                            )

            return True

        except InvalidNPDAError:
            return False

    def _simulate_word_parallel(self, word: str) -> bool:
        """Simule la reconnaissance d'un mot de manière parallèle.

        :param word: Mot à simuler
        :return: True si le mot est accepté, False sinon
        :raises NPDATimeoutError: Si le calcul dépasse le timeout
        :raises NPDAMemoryError: Si le calcul dépasse la limite mémoire
        """
        start_time = time.time()
        initial_config = NPDAConfiguration(
            state=self._initial_state,
            remaining_input=word,
            stack=self._initial_stack_symbol,
            priority=0,
            branch_id=0,
            depth=0,
        )

        # File de priorité pour gérer les configurations
        config_queue = [(-initial_config.priority, initial_config)]
        visited_configs = set()
        branch_counter = 0

        while config_queue:
            # Vérification du timeout
            if time.time() - start_time > self._timeout:
                raise NPDATimeoutError(
                    f"Timeout de calcul dépassé ({self._timeout}s)", self._timeout, word
                )

            # Vérification de la mémoire
            if len(config_queue) > self._max_parallel_branches:
                raise NPDAMemoryError(
                    f"Limite de branches parallèles dépassée ({self._max_parallel_branches})",
                    self._max_parallel_branches,
                    len(config_queue),
                )

            # Récupération de la configuration avec la plus haute priorité
            _, current_config = heapq.heappop(config_queue)

            # Vérification si la configuration a déjà été visitée
            config_key = (
                current_config.state,
                current_config.remaining_input,
                current_config.stack,
            )
            if config_key in visited_configs:
                continue

            visited_configs.add(config_key)

            # Vérification si la configuration est acceptante
            if current_config.is_accepting and self.is_final_state(
                current_config.state
            ):
                return True

            # Génération des nouvelles configurations
            new_configs = self._generate_next_configurations(
                current_config, branch_counter
            )
            branch_counter += len(new_configs)
            self._performance_stats["parallel_branches_created"] += len(new_configs)

            # Ajout des nouvelles configurations à la file de priorité
            for config in new_configs:
                heapq.heappush(config_queue, (-config.priority, config))

        return False

    def _generate_next_configurations(
        self, config: NPDAConfiguration, branch_counter: int
    ) -> List[NPDAConfiguration]:
        """Génère les configurations suivantes à partir d'une configuration donnée.

        :param config: Configuration actuelle
        :param branch_counter: Compteur de branches
        :return: Liste des nouvelles configurations
        """
        new_configs = []

        # Traitement des transitions epsilon
        epsilon_configs = self._epsilon_closure_parallel(config.state, config.stack_top)
        for epsilon_config in epsilon_configs:
            new_config = NPDAConfiguration(
                state=epsilon_config.state,
                remaining_input=config.remaining_input,
                stack=epsilon_config.stack,
                priority=config.priority + 1,
                branch_id=branch_counter + len(new_configs),
                depth=config.depth + 1,
                parent_id=config.branch_id,
            )
            new_configs.append(new_config)

        # Traitement des transitions avec symbole d'entrée
        if config.remaining_input:
            input_symbol = config.remaining_input[0]
            transitions = self.get_transitions(
                config.state, input_symbol, config.stack_top
            )

            for next_state, stack_symbols in transitions:
                new_config = config.change_state(next_state)
                new_config = new_config.consume_input(1)

                # Gestion de la pile
                if stack_symbols:
                    new_config = new_config.push_symbols(stack_symbols)
                else:
                    new_config = new_config.pop_symbol()

                new_config = new_config.with_branch_id(
                    branch_counter + len(new_configs)
                )
                new_configs.append(new_config)

        return new_configs

    def _epsilon_closure_parallel(
        self, state: str, stack_symbol: str
    ) -> Set[NPDAConfiguration]:
        """Calcule la fermeture epsilon parallèle pour un état et un symbole de pile.

        :param state: État de départ
        :param stack_symbol: Symbole de pile
        :return: Ensemble des configurations accessibles par transitions epsilon
        """
        cache_key = (state, stack_symbol)
        if cache_key in self._epsilon_closure_cache:
            return self._epsilon_closure_cache[cache_key]

        closure = set()
        visited = set()
        queue = [(state, stack_symbol)]

        while queue:
            current_state, current_stack = queue.pop(0)
            if (current_state, current_stack) in visited:
                continue

            visited.add((current_state, current_stack))

            # Recherche des transitions epsilon
            transitions = self.get_transitions(current_state, "", current_stack)
            for next_state, stack_symbols in transitions:
                if stack_symbols:
                    new_stack = (
                        stack_symbols + current_stack[1:]
                        if current_stack
                        else stack_symbols
                    )
                else:
                    new_stack = current_stack[1:] if current_stack else ""

                closure.add(
                    NPDAConfiguration(
                        state=next_state,
                        remaining_input="",
                        stack=new_stack,
                        priority=0,
                        branch_id=0,
                        depth=0,
                    )
                )

                if (next_state, new_stack) not in visited:
                    queue.append((next_state, new_stack))

        self._epsilon_closure_cache[cache_key] = closure
        return closure

    def get_performance_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques de performance.

        :return: Dictionnaire avec les statistiques de performance
        """
        return self._performance_stats.copy()

    def analyze_complexity(self) -> Dict[str, Any]:
        """Analyse la complexité de l'automate.

        :return: Dictionnaire avec les métriques de complexité
        """
        # Calcul des métriques de base
        num_states = len(self._states)
        num_transitions = sum(
            len(transitions) for transitions in self._transitions.values()
        )
        num_epsilon_transitions = sum(
            1 for (_, input_symbol, _) in self._transitions.keys() if input_symbol == ""
        )

        # Calcul de la profondeur maximale de pile théorique
        max_stack_depth = self._calculate_max_stack_depth()

        # Calcul de la complexité temporelle moyenne
        avg_time_complexity = self._calculate_avg_time_complexity()

        # Calcul de la complexité spatiale
        space_complexity = self._calculate_space_complexity()

        return {
            "num_states": num_states,
            "num_transitions": num_transitions,
            "num_epsilon_transitions": num_epsilon_transitions,
            "max_parallel_branches": self._max_parallel_branches,
            "max_stack_depth": max_stack_depth,
            "avg_time_complexity": avg_time_complexity,
            "space_complexity": space_complexity,
            "deterministic_ratio": self._calculate_deterministic_ratio(),
            "epsilon_ratio": num_epsilon_transitions / max(num_transitions, 1),
            "branching_factor": self._calculate_branching_factor(),
        }

    def _calculate_max_stack_depth(self) -> int:
        """Calcule la profondeur maximale de pile théorique.

        :return: Profondeur maximale de pile
        """
        max_depth = 0
        for (_, _, stack_symbol), transitions in self._transitions.items():
            for _, stack_symbols in transitions:
                if stack_symbols:
                    # Estimation basée sur la longueur des chaînes de symboles
                    depth = len(stack_symbols)
                    max_depth = max(max_depth, depth)
        return max_depth

    def _calculate_avg_time_complexity(self) -> float:
        """Calcule la complexité temporelle moyenne.

        :return: Complexité temporelle moyenne
        """
        # Estimation basée sur le nombre de transitions et de branches
        num_transitions = sum(
            len(transitions) for transitions in self._transitions.values()
        )
        branching_factor = self._calculate_branching_factor()

        # Complexité approximative O(n * b^d) où n = transitions, b = facteur de branchement, d = profondeur
        return num_transitions * (branching_factor**2)

    def _calculate_space_complexity(self) -> int:
        """Calcule la complexité spatiale.

        :return: Complexité spatiale en nombre de configurations
        """
        # Estimation basée sur le nombre d'états et de branches parallèles
        return len(self._states) * self._max_parallel_branches

    def _calculate_deterministic_ratio(self) -> float:
        """Calcule le ratio de déterminisme de l'automate.

        :return: Ratio de déterminisme (0.0 = complètement non-déterministe, 1.0 = déterministe)
        """
        deterministic_transitions = 0
        total_transitions = 0

        for transitions in self._transitions.values():
            total_transitions += 1
            if len(transitions) <= 1:
                deterministic_transitions += 1

        return deterministic_transitions / max(total_transitions, 1)

    def _calculate_branching_factor(self) -> float:
        """Calcule le facteur de branchement moyen.

        :return: Facteur de branchement moyen
        """
        if not self._transitions:
            return 0.0

        total_branches = sum(
            len(transitions) for transitions in self._transitions.values()
        )
        return total_branches / len(self._transitions)

    def optimize_parallel_execution(self) -> "NPDA":
        """Optimise l'exécution parallèle de l'automate.

        :return: NPDA optimisé
        :raises NPDAError: Si l'optimisation échoue
        """
        try:
            # Création d'une copie de l'automate
            optimized_npda = NPDA(
                states=self._states,
                input_alphabet=self._input_alphabet,
                stack_alphabet=self._stack_alphabet,
                transitions=self._transitions.copy(),
                initial_state=self._initial_state,
                initial_stack_symbol=self._initial_stack_symbol,
                final_states=self._final_states,
                name=f"Optimized_{self._name or 'NPDA'}",
                max_parallel_branches=self._max_parallel_branches,
            )

            # Optimisations appliquées
            optimized_npda._optimize_epsilon_transitions()
            optimized_npda._optimize_redundant_transitions()
            optimized_npda._optimize_parallel_branches()

            return optimized_npda

        except Exception as e:
            raise NPDAError(f"Erreur lors de l'optimisation : {e}")

    def _optimize_epsilon_transitions(self) -> None:
        """Optimise les transitions epsilon.

        Cette méthode élimine les transitions epsilon redondantes
        et optimise les fermetures epsilon.
        """
        # Mise à jour du cache des fermetures epsilon
        self._epsilon_closure_cache.clear()

        # Optimisation des transitions epsilon en cascade
        for state in self._states:
            for stack_symbol in self._stack_alphabet:
                self._epsilon_closure_parallel(state, stack_symbol)

    def _optimize_redundant_transitions(self) -> None:
        """Optimise les transitions redondantes.

        Cette méthode élimine les transitions redondantes
        et optimise la structure des transitions.
        """
        # Élimination des transitions redondantes
        optimized_transitions = {}

        for (
            state,
            input_symbol,
            stack_symbol,
        ), transitions in self._transitions.items():
            if transitions:
                # Élimination des transitions dupliquées
                unique_transitions = set(transitions)
                optimized_transitions[(state, input_symbol, stack_symbol)] = (
                    unique_transitions
                )

        self._transitions = optimized_transitions

    def _optimize_parallel_branches(self) -> None:
        """Optimise la gestion des branches parallèles.

        Cette méthode ajuste les paramètres de gestion
        des branches parallèles pour de meilleures performances.
        """
        # Ajustement du nombre maximum de branches parallèles
        complexity = self.analyze_complexity()
        branching_factor = complexity["branching_factor"]

        if branching_factor > 2.0:
            # Réduction du nombre de branches pour les automates très non-déterministes
            self._max_parallel_branches = min(self._max_parallel_branches, 500)
        elif branching_factor < 1.5:
            # Augmentation du nombre de branches pour les automates peu non-déterministes
            self._max_parallel_branches = min(self._max_parallel_branches * 2, 2000)

    def is_deterministic(self) -> bool:
        """Vérifie si l'automate est déterministe.

        :return: True si l'automate est déterministe, False sinon
        """
        for transitions in self._transitions.values():
            if len(transitions) > 1:
                return False
        return True

    def get_epsilon_transitions(self) -> Set[Tuple[str, str, str]]:
        """Récupère toutes les transitions epsilon de l'automate.

        :return: Ensemble des transitions epsilon
        """
        epsilon_transitions = set()
        for state, input_symbol, stack_symbol in self._transitions.keys():
            if input_symbol == "":
                epsilon_transitions.add((state, input_symbol, stack_symbol))
        return epsilon_transitions

    def get_transition_count(self) -> int:
        """Récupère le nombre total de transitions.

        :return: Nombre total de transitions
        """
        return sum(len(transitions) for transitions in self._transitions.values())

    def get_state_count(self) -> int:
        """Récupère le nombre d'états.

        :return: Nombre d'états
        """
        return len(self._states)

    def get_alphabet_sizes(self) -> Dict[str, int]:
        """Récupère les tailles des alphabets.

        :return: Dictionnaire avec les tailles des alphabets
        """
        return {
            "input_alphabet": len(self._input_alphabet),
            "stack_alphabet": len(self._stack_alphabet),
        }

    def clear_cache(self) -> None:
        """Vide tous les caches de l'automate.

        Cette méthode permet de libérer la mémoire utilisée par les caches
        et de réinitialiser les statistiques de performance.
        """
        self._epsilon_closure_cache.clear()
        self._transition_cache.clear()
        self._recognition_cache.clear()
        self._performance_stats = {
            "total_computations": 0,
            "parallel_branches_created": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "timeout_count": 0,
            "memory_limit_count": 0,
        }

    def union(self, other: "NPDA") -> "NPDA":
        """Crée l'union de deux NPDA.

        :param other: Autre NPDA
        :return: NPDA reconnaissant l'union des langages
        :raises NPDAError: Si les NPDA ne sont pas compatibles
        """
        if not isinstance(other, NPDA):
            raise NPDAError("L'autre automate doit être un NPDA")

        # Vérification de la compatibilité des alphabets
        if self._input_alphabet != other._input_alphabet:
            raise NPDAError("Les alphabets d'entrée doivent être identiques")

        if self._stack_alphabet != other._stack_alphabet:
            raise NPDAError("Les alphabets de pile doivent être identiques")

        # Création d'un nouvel état initial
        new_initial_state = "q_union_start"

        # Union des états avec préfixes pour éviter les conflits
        new_states = {new_initial_state}
        new_states.update(f"L1_{state}" for state in self._states)
        new_states.update(f"L2_{state}" for state in other._states)

        # Union des états finaux
        new_final_states = set()
        new_final_states.update(f"L1_{state}" for state in self._final_states)
        new_final_states.update(f"L2_{state}" for state in other._final_states)

        # Construction des nouvelles transitions
        new_transitions = {}

        # Transition initiale vers les deux automates
        new_transitions[(new_initial_state, "", self._initial_stack_symbol)] = {
            (f"L1_{self._initial_state}", self._initial_stack_symbol),
            (f"L2_{other._initial_state}", other._initial_stack_symbol),
        }

        # Transitions du premier automate
        for (
            state,
            input_symbol,
            stack_symbol,
        ), transitions in self._transitions.items():
            new_key = (f"L1_{state}", input_symbol, stack_symbol)
            new_transitions[new_key] = {
                (f"L1_{next_state}", stack_symbols)
                for next_state, stack_symbols in transitions
            }

        # Transitions du second automate
        for (
            state,
            input_symbol,
            stack_symbol,
        ), transitions in other._transitions.items():
            new_key = (f"L2_{state}", input_symbol, stack_symbol)
            new_transitions[new_key] = {
                (f"L2_{next_state}", stack_symbols)
                for next_state, stack_symbols in transitions
            }

        return NPDA(
            states=new_states,
            input_alphabet=self._input_alphabet,
            stack_alphabet=self._stack_alphabet,
            transitions=new_transitions,
            initial_state=new_initial_state,
            initial_stack_symbol=self._initial_stack_symbol,
            final_states=new_final_states,
            name=f"Union({self._name or 'NPDA1'}, {other._name or 'NPDA2'})",
            max_parallel_branches=max(
                self._max_parallel_branches, other._max_parallel_branches
            ),
        )

    def concatenation(self, other: "NPDA") -> "NPDA":
        """Crée la concaténation de deux NPDA.

        :param other: Autre NPDA
        :return: NPDA reconnaissant la concaténation des langages
        :raises NPDAError: Si les NPDA ne sont pas compatibles
        """
        if not isinstance(other, NPDA):
            raise NPDAError("L'autre automate doit être un NPDA")

        # Vérification de la compatibilité des alphabets
        if self._input_alphabet != other._input_alphabet:
            raise NPDAError("Les alphabets d'entrée doivent être identiques")

        if self._stack_alphabet != other._stack_alphabet:
            raise NPDAError("Les alphabets de pile doivent être identiques")

        # Création d'un nouvel état initial
        new_initial_state = "q_concat_start"

        # Union des états avec préfixes pour éviter les conflits
        new_states = {new_initial_state}
        new_states.update(f"L1_{state}" for state in self._states)
        new_states.update(f"L2_{state}" for state in other._states)

        # États finaux du second automate
        new_final_states = {f"L2_{state}" for state in other._final_states}

        # Construction des nouvelles transitions
        new_transitions = {}

        # Transition initiale vers le premier automate
        new_transitions[(new_initial_state, "", self._initial_stack_symbol)] = {
            (f"L1_{self._initial_state}", self._initial_stack_symbol)
        }

        # Transitions du premier automate
        for (
            state,
            input_symbol,
            stack_symbol,
        ), transitions in self._transitions.items():
            new_key = (f"L1_{state}", input_symbol, stack_symbol)
            new_transitions[new_key] = set()

            for next_state, stack_symbols in transitions:
                if next_state in self._final_states:
                    # Transition vers le second automate
                    new_transitions[new_key].add(
                        (f"L2_{other._initial_state}", stack_symbols)
                    )
                else:
                    # Transition normale dans le premier automate
                    new_transitions[new_key].add((f"L1_{next_state}", stack_symbols))

        # Transitions du second automate
        for (
            state,
            input_symbol,
            stack_symbol,
        ), transitions in other._transitions.items():
            new_key = (f"L2_{state}", input_symbol, stack_symbol)
            new_transitions[new_key] = {
                (f"L2_{next_state}", stack_symbols)
                for next_state, stack_symbols in transitions
            }

        return NPDA(
            states=new_states,
            input_alphabet=self._input_alphabet,
            stack_alphabet=self._stack_alphabet,
            transitions=new_transitions,
            initial_state=new_initial_state,
            initial_stack_symbol=self._initial_stack_symbol,
            final_states=new_final_states,
            name=f"Concat({self._name or 'NPDA1'}, {other._name or 'NPDA2'})",
            max_parallel_branches=max(
                self._max_parallel_branches, other._max_parallel_branches
            ),
        )

    def kleene_star(self) -> "NPDA":
        """Crée l'étoile de Kleene d'un NPDA.

        :return: NPDA reconnaissant l'étoile de Kleene du langage
        :raises NPDAError: Si l'opération échoue
        """
        # Création d'un nouvel état initial et final
        new_initial_state = "q_star_start"
        new_final_state = "q_star_final"

        # Union des états
        new_states = {new_initial_state, new_final_state}
        new_states.update(f"L_{state}" for state in self._states)

        # États finaux
        new_final_states = {new_final_state}

        # Construction des nouvelles transitions
        new_transitions = {}

        # Transition initiale vers l'automate original
        new_transitions[(new_initial_state, "", self._initial_stack_symbol)] = {
            (f"L_{self._initial_state}", self._initial_stack_symbol)
        }

        # Transition initiale vers l'état final (mot vide)
        new_transitions[(new_initial_state, "", self._initial_stack_symbol)].add(
            (new_final_state, self._initial_stack_symbol)
        )

        # Transitions de l'automate original
        for (
            state,
            input_symbol,
            stack_symbol,
        ), transitions in self._transitions.items():
            new_key = (f"L_{state}", input_symbol, stack_symbol)
            new_transitions[new_key] = set()

            for next_state, stack_symbols in transitions:
                if next_state in self._final_states:
                    # Transition vers l'état final
                    new_transitions[new_key].add((new_final_state, stack_symbols))
                    # Transition vers l'état initial (boucle)
                    new_transitions[new_key].add(
                        (f"L_{self._initial_state}", stack_symbols)
                    )
                else:
                    # Transition normale
                    new_transitions[new_key].add((f"L_{next_state}", stack_symbols))

        # Transition de l'état final vers l'état initial (boucle)
        new_transitions[(new_final_state, "", self._initial_stack_symbol)] = {
            (f"L_{self._initial_state}", self._initial_stack_symbol)
        }

        return NPDA(
            states=new_states,
            input_alphabet=self._input_alphabet,
            stack_alphabet=self._stack_alphabet,
            transitions=new_transitions,
            initial_state=new_initial_state,
            initial_stack_symbol=self._initial_stack_symbol,
            final_states=new_final_states,
            name=f"Kleene({self._name or 'NPDA'})",
            max_parallel_branches=self._max_parallel_branches,
        )

    @classmethod
    def from_pda(cls, pda: "PDA") -> "NPDA":
        """Convertit un PDA en NPDA.

        :param pda: PDA à convertir
        :return: NPDA équivalent
        :raises NPDAError: Si la conversion échoue
        """
        try:
            # Import local pour éviter les dépendances circulaires
            from .pda import PDA

            if not isinstance(pda, PDA):
                raise NPDAError("L'automate doit être un PDA")

            # Conversion des transitions
            npda_transitions = {}
            for (
                state,
                input_symbol,
                stack_symbol,
            ), transitions in pda._transitions.items():
                npda_transitions[(state, input_symbol, stack_symbol)] = set(transitions)

            return cls(
                states=pda._states,
                input_alphabet=pda._input_alphabet,
                stack_alphabet=pda._stack_alphabet,
                transitions=npda_transitions,
                initial_state=pda._initial_state,
                initial_stack_symbol=pda._initial_stack_symbol,
                final_states=pda._final_states,
                name=f"NPDA_from_{pda._name or 'PDA'}",
                max_parallel_branches=1000,
            )
        except Exception as e:
            raise NPDAError(f"Erreur lors de la conversion PDA → NPDA : {e}")

    def to_pda(self) -> "PDA":
        """Convertit le NPDA en PDA.

        :return: PDA équivalent
        :raises NPDAError: Si la conversion échoue
        """
        try:
            # Import local pour éviter les dépendances circulaires
            from .pda import PDA

            # Conversion des transitions
            pda_transitions = {}
            for (
                state,
                input_symbol,
                stack_symbol,
            ), transitions in self._transitions.items():
                pda_transitions[(state, input_symbol, stack_symbol)] = transitions

            return PDA(
                states=self._states,
                input_alphabet=self._input_alphabet,
                stack_alphabet=self._stack_alphabet,
                transitions=pda_transitions,
                initial_state=self._initial_state,
                initial_stack_symbol=self._initial_stack_symbol,
                final_states=self._final_states,
                name=f"PDA_from_{self._name or 'NPDA'}",
            )
        except Exception as e:
            raise NPDAError(f"Erreur lors de la conversion NPDA → PDA : {e}")

    @classmethod
    def from_dpda(cls, dpda: "DPDA") -> "NPDA":
        """Convertit un DPDA en NPDA.

        :param dpda: DPDA à convertir
        :return: NPDA équivalent
        :raises NPDAError: Si la conversion échoue
        """
        try:
            # Import local pour éviter les dépendances circulaires
            from .dpda import DPDA

            if not isinstance(dpda, DPDA):
                raise NPDAError("L'automate doit être un DPDA")

            # Conversion des transitions
            npda_transitions = {}
            for (state, input_symbol, stack_symbol), (
                next_state,
                stack_symbols,
            ) in dpda._transitions.items():
                npda_transitions[(state, input_symbol, stack_symbol)] = {
                    (next_state, stack_symbols)
                }

            return cls(
                states=dpda._states,
                input_alphabet=dpda._input_alphabet,
                stack_alphabet=dpda._stack_alphabet,
                transitions=npda_transitions,
                initial_state=dpda._initial_state,
                initial_stack_symbol=dpda._initial_stack_symbol,
                final_states=dpda._final_states,
                name=f"NPDA_from_{dpda._name or 'DPDA'}",
                max_parallel_branches=1000,
            )
        except Exception as e:
            raise NPDAError(f"Erreur lors de la conversion DPDA → NPDA : {e}")

    def to_dpda(self) -> "DPDA":
        """Convertit le NPDA en DPDA si possible.

        :return: DPDA équivalent
        :raises NPDAError: Si la conversion échoue ou si le NPDA n'est pas déterministe
        """
        try:
            # Import local pour éviter les dépendances circulaires
            from .dpda import DPDA

            # Vérification du déterminisme
            for (
                state,
                input_symbol,
                stack_symbol,
            ), transitions in self._transitions.items():
                if len(transitions) > 1:
                    raise NPDAError(
                        "Le NPDA n'est pas déterministe, conversion impossible"
                    )

            # Conversion des transitions
            dpda_transitions = {}
            for (
                state,
                input_symbol,
                stack_symbol,
            ), transitions in self._transitions.items():
                if transitions:
                    next_state, stack_symbols = next(iter(transitions))
                    dpda_transitions[(state, input_symbol, stack_symbol)] = (
                        next_state,
                        stack_symbols,
                    )

            return DPDA(
                states=self._states,
                input_alphabet=self._input_alphabet,
                stack_alphabet=self._stack_alphabet,
                transitions=dpda_transitions,
                initial_state=self._initial_state,
                initial_stack_symbol=self._initial_stack_symbol,
                final_states=self._final_states,
                name=f"DPDA_from_{self._name or 'NPDA'}",
            )
        except Exception as e:
            raise NPDAError(f"Erreur lors de la conversion NPDA → DPDA : {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'automate en dictionnaire.

        :return: Représentation dictionnaire de l'automate
        """
        return {
            "type": "NPDA",
            "states": list(self._states),
            "input_alphabet": list(self._input_alphabet),
            "stack_alphabet": list(self._stack_alphabet),
            "transitions": {
                f"{state},{input_symbol},{stack_symbol}": [
                    [next_state, stack_symbols]
                    for next_state, stack_symbols in transitions
                ]
                for (
                    state,
                    input_symbol,
                    stack_symbol,
                ), transitions in self._transitions.items()
            },
            "initial_state": self._initial_state,
            "initial_stack_symbol": self._initial_stack_symbol,
            "final_states": list(self._final_states),
            "name": self._name,
            "max_parallel_branches": self._max_parallel_branches,
            "timeout": self._timeout,
            "memory_limit": self._memory_limit,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NPDA":
        """Crée un automate à partir d'un dictionnaire.

        :param data: Données de l'automate
        :return: Instance de NPDA
        :raises InvalidNPDAError: Si les données sont invalides
        """
        try:
            # Reconstruction des transitions
            transitions = {}
            for key, transitions_list in data["transitions"].items():
                state, input_symbol, stack_symbol = key.split(",")
                transitions[(state, input_symbol, stack_symbol)] = {
                    (next_state, stack_symbols)
                    for next_state, stack_symbols in transitions_list
                }

            return cls(
                states=set(data["states"]),
                input_alphabet=set(data["input_alphabet"]),
                stack_alphabet=set(data["stack_alphabet"]),
                transitions=transitions,
                initial_state=data["initial_state"],
                initial_stack_symbol=data["initial_stack_symbol"],
                final_states=set(data["final_states"]),
                name=data.get("name"),
                max_parallel_branches=data.get("max_parallel_branches", 1000),
            )
        except (KeyError, ValueError) as e:
            raise InvalidNPDAError(f"Données de NPDA invalides : {e}")

    def __str__(self) -> str:
        """Retourne la représentation textuelle de l'automate.

        :return: Représentation textuelle
        """
        return (
            f"NPDA(name='{self._name}', "
            f"states={len(self._states)}, "
            f"input_alphabet={len(self._input_alphabet)}, "
            f"stack_alphabet={len(self._stack_alphabet)}, "
            f"max_parallel_branches={self._max_parallel_branches})"
        )

    def __repr__(self) -> str:
        """Retourne la représentation technique de l'automate.

        :return: Représentation technique pour le débogage
        """
        return (
            f"NPDA(states={self._states}, "
            f"input_alphabet={self._input_alphabet}, "
            f"stack_alphabet={self._stack_alphabet}, "
            f"transitions=..., "
            f"initial_state='{self._initial_state}', "
            f"initial_stack_symbol='{self._initial_stack_symbol}', "
            f"final_states={self._final_states}, "
            f"max_parallel_branches={self._max_parallel_branches})"
        )
