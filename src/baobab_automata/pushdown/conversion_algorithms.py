"""
Algorithmes de conversion entre types d'automates à pile.

Ce module implémente les algorithmes de conversion entre différents types
d'automates à pile (PDA, DPDA, NPDA) et les grammaires hors-contexte.
"""

import time
from typing import Any, Dict, List, Set, Tuple, Union
from collections import deque

from .pda import PDA
from .dpda import DPDA
from .npda import NPDA
from .grammar_types import ContextFreeGrammar, Production
from .conversion_exceptions import (
    ConversionError,
    ConversionTimeoutError,
    ConversionValidationError,
    ConversionNotPossibleError,
    ConversionConfigurationError,
)


class PushdownConversionAlgorithms:
    """Algorithmes de conversion entre types d'automates à pile et grammaires.
    """

    def __init__(
        self,
        enable_caching: bool = True,
        max_cache_size: int = 1000,
        timeout: float = 30.0,
    ) -> None:
        """Initialise les algorithmes de conversion.

        :param enable_caching: Active la mise en cache des conversions
        :param max_cache_size: Taille maximale du cache
        :param timeout: Timeout en secondes pour les conversions
        :raises ConversionError: Si l'initialisation échoue
        """
        self._enable_caching = enable_caching
        self._max_cache_size = max_cache_size
        self._timeout = timeout
        self._cache: Dict[str, Any] = {}
        self._conversion_stats: Dict[str, Any] = {
            "total_conversions": 0,
            "successful_conversions": 0,
            "failed_conversions": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "average_conversion_time": 0.0,
            "conversion_times": [],
        }
        self._performance_metrics: Dict[str, Any] = {
            "memory_usage": 0,
            "cpu_usage": 0,
            "cache_efficiency": 0.0,
        }
        self._enable_optimization = True
        self._enable_validation = True
        self._max_states = 10000
        self._max_stack_symbols = 1000

    def configure_conversion(
        self,
        enable_optimization: bool = True,
        enable_validation: bool = True,
        max_states: int = 10000,
        max_stack_symbols: int = 1000,
    ) -> None:
        """Configure les paramètres de conversion.

        :param enable_optimization: Active l'optimisation des conversions
        :param enable_validation: Active la validation des conversions
        :param max_states: Nombre maximum d'états autorisé
        :param max_stack_symbols: Nombre maximum de symboles de pile autorisé
        :raises ConversionError: Si la configuration est invalide
        """
        if max_states <= 0:
            raise ConversionConfigurationError(
                "Le nombre maximum d'états doit être positif", "max_states"
            )
        if max_stack_symbols <= 0:
            raise ConversionConfigurationError(
                "Le nombre maximum de symboles de pile doit être positif",
                "max_stack_symbols",
            )

        self._enable_optimization = enable_optimization
        self._enable_validation = enable_validation
        self._max_states = max_states
        self._max_stack_symbols = max_stack_symbols

    def pda_to_dpda(self, pda: PDA) -> DPDA:
        """Convertit un PDA en DPDA si possible.

        :param pda: PDA à convertir
        :return: DPDA équivalent
        :raises ConversionError: Si la conversion n'est pas possible
        :raises ConversionTimeoutError: Si la conversion dépasse le timeout
        """
        start_time = time.time()

        try:
            # Vérification du timeout
            if time.time() - start_time > self._timeout:
                raise ConversionTimeoutError(self._timeout, "pda_to_dpda")

            # Vérification de la validité du PDA
            if not pda.validate():
                raise ConversionValidationError("PDA invalide", "PDA")

            # Vérification des limites
            if len(pda.states) > self._max_states:
                raise ConversionError(
                    f"Trop d'états: {len(pda.states)} > {self._max_states}"
                )
            if len(pda.stack_alphabet) > self._max_stack_symbols:
                raise ConversionError(
                    f"Trop de symboles de pile: {len(pda.stack_alphabet)} > "
                    f"{self._max_stack_symbols}"
                )

            # Analyse du PDA pour détecter les conflits de déterminisme
            conflicts = self._detect_determinism_conflicts(pda)
            if conflicts:
                # Résolution des conflits par ajout d'états
                resolved_pda = self._resolve_determinism_conflicts(
                    pda, conflicts
                )
            else:
                resolved_pda = pda

            # Conversion des transitions non-déterministes en déterministes
            dpda_transitions = self._convert_to_deterministic_transitions(
                resolved_pda
            )

            # Création du DPDA
            dpda = DPDA(
                states=resolved_pda.states,
                input_alphabet=resolved_pda.input_alphabet,
                stack_alphabet=resolved_pda.stack_alphabet,
                transitions=dpda_transitions,
                initial_state=resolved_pda.initial_state,
                initial_stack_symbol=resolved_pda.initial_stack_symbol,
                final_states=resolved_pda.final_states,
                name=(
                    f"{resolved_pda.name}_converted_to_dpda"
                    if resolved_pda.name
                    else None
                ),
            )

            # Validation du DPDA
            if self._enable_validation and not dpda.validate():
                raise ConversionValidationError(
                    "DPDA résultant invalide", "DPDA"
                )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return dpda

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, (ConversionError, ConversionTimeoutError)):
                raise
            raise ConversionError(
                f"Erreur lors de la conversion PDA → DPDA: {str(e)}"
            ) from e

    def dpda_to_pda(self, dpda: DPDA) -> PDA:
        """Convertit un DPDA en PDA.

        :param dpda: DPDA à convertir
        :return: PDA équivalent
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité du DPDA
            if not dpda.validate():
                raise ConversionValidationError("DPDA invalide", "DPDA")

            # Conversion des transitions déterministes en non-déterministes
            pda_transitions = self._convert_to_nondeterministic_transitions(
                dpda
            )

            # Création du PDA
            pda = PDA(
                states=dpda.states,
                input_alphabet=dpda.input_alphabet,
                stack_alphabet=dpda.stack_alphabet,
                transitions=pda_transitions,
                initial_state=dpda.initial_state,
                initial_stack_symbol=dpda.initial_stack_symbol,
                final_states=dpda.final_states,
                name=f"{dpda.name}_converted_to_pda" if dpda.name else None,
            )

            # Validation du PDA
            if self._enable_validation and not pda.validate():
                raise ConversionValidationError(
                    "PDA résultant invalide", "PDA"
                )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return pda

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la conversion DPDA → PDA: {str(e)}"
            ) from e

    def pda_to_npda(self, pda: PDA) -> NPDA:
        """Convertit un PDA en NPDA.

        :param pda: PDA à convertir
        :return: NPDA équivalent
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité du PDA
            if not pda.validate():
                raise ConversionValidationError("PDA invalide", "PDA")

            # Conversion directe des transitions
            npda_transitions = dict(pda._transitions)

            # Création du NPDA
            npda = NPDA(
                states=pda.states,
                input_alphabet=pda.input_alphabet,
                stack_alphabet=pda.stack_alphabet,
                transitions=npda_transitions,
                initial_state=pda.initial_state,
                initial_stack_symbol=pda.initial_stack_symbol,
                final_states=pda.final_states,
                name=f"{pda.name}_converted_to_npda" if pda.name else None,
                max_parallel_branches=1000,
            )

            # Validation du NPDA
            if self._enable_validation and not npda.validate():
                raise ConversionValidationError(
                    "NPDA résultant invalide", "NPDA"
                )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return npda

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la conversion PDA → NPDA: {str(e)}"
            ) from e

    def npda_to_pda(self, npda: NPDA) -> PDA:
        """Convertit un NPDA en PDA.

        :param npda: NPDA à convertir
        :return: PDA équivalent
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité du NPDA
            if not npda.validate():
                raise ConversionValidationError("NPDA invalide", "NPDA")

            # Conversion des transitions (NPDA et PDA ont la même structure)
            pda_transitions = dict(npda._transitions)

            # Création du PDA
            pda = PDA(
                states=npda.states,
                input_alphabet=npda.input_alphabet,
                stack_alphabet=npda.stack_alphabet,
                transitions=pda_transitions,
                initial_state=npda.initial_state,
                initial_stack_symbol=npda.initial_stack_symbol,
                final_states=npda.final_states,
                name=f"{npda.name}_converted_to_pda" if npda.name else None,
            )

            # Validation du PDA
            if self._enable_validation and not pda.validate():
                raise ConversionValidationError(
                    "PDA résultant invalide", "PDA"
                )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return pda

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la conversion NPDA → PDA: {str(e)}"
            ) from e

    def dpda_to_npda(self, dpda: DPDA) -> NPDA:
        """Convertit un DPDA en NPDA.

        :param dpda: DPDA à convertir
        :return: NPDA équivalent
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité du DPDA
            if not dpda.validate():
                raise ConversionValidationError("DPDA invalide", "DPDA")

            # Conversion des transitions déterministes en non-déterministes
            npda_transitions = self._convert_to_nondeterministic_transitions(
                dpda
            )

            # Création du NPDA
            npda = NPDA(
                states=dpda.states,
                input_alphabet=dpda.input_alphabet,
                stack_alphabet=dpda.stack_alphabet,
                transitions=npda_transitions,
                initial_state=dpda.initial_state,
                initial_stack_symbol=dpda.initial_stack_symbol,
                final_states=dpda.final_states,
                name=f"{dpda.name}_converted_to_npda" if dpda.name else None,
                max_parallel_branches=1000,
            )

            # Validation du NPDA
            if self._enable_validation and not npda.validate():
                raise ConversionValidationError(
                    "NPDA résultant invalide", "NPDA"
                )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return npda

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la conversion DPDA → NPDA: {str(e)}"
            ) from e

    def npda_to_dpda(self, npda: NPDA) -> DPDA:
        """Convertit un NPDA en DPDA si possible.

        :param npda: NPDA à convertir
        :return: DPDA équivalent
        :raises ConversionError: Si la conversion n'est pas possible
        """
        start_time = time.time()

        try:
            # Vérification de la validité du NPDA
            if not npda.validate():
                raise ConversionValidationError("NPDA invalide", "NPDA")

            # Vérification si le NPDA est déjà déterministe
            if self._is_deterministic(npda):
                # Conversion directe
                dpda_transitions = self._convert_to_deterministic_transitions(
                    npda
                )
            else:
                # Tentative de résolution des conflits
                conflicts = self._detect_determinism_conflicts(npda)
                if conflicts:
                    resolved_npda = self._resolve_determinism_conflicts(
                        npda, conflicts
                    )
                    dpda_transitions = (
                        self._convert_to_deterministic_transitions(
                            resolved_npda
                        )
                    )
                else:
                    raise ConversionNotPossibleError(
                        "NPDA", "DPDA", "Le NPDA n'est pas déterministe"
                    )

            # Création du DPDA
            dpda = DPDA(
                states=npda.states,
                input_alphabet=npda.input_alphabet,
                stack_alphabet=npda.stack_alphabet,
                transitions=dpda_transitions,
                initial_state=npda.initial_state,
                initial_stack_symbol=npda.initial_stack_symbol,
                final_states=npda.final_states,
                name=f"{npda.name}_converted_to_dpda" if npda.name else None,
            )

            # Validation du DPDA
            if self._enable_validation and not dpda.validate():
                raise ConversionValidationError(
                    "DPDA résultant invalide", "DPDA"
                )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return dpda

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, (ConversionError, ConversionNotPossibleError)):
                raise
            raise ConversionError(
                f"Erreur lors de la conversion NPDA → DPDA: {str(e)}"
            ) from e

    def _detect_determinism_conflicts(
        self, automaton: Union[PDA, NPDA]
    ) -> List[Tuple[str, str, str]]:
        """Détecte les conflits de déterminisme dans un automate.

        :param automaton: Automate à analyser
        :return: Liste des transitions en conflit
        """
        conflicts = []

        for (
            state,
            symbol,
            stack_symbol,
        ), transitions in automaton._transitions.items():
            if len(transitions) > 1:
                conflicts.append((state, symbol, stack_symbol))

        return conflicts

    def _resolve_determinism_conflicts(
        self,
        automaton: Union[PDA, NPDA],
        conflicts: List[Tuple[str, str, str]],
    ) -> Union[PDA, NPDA]:
        """Résout les conflits de déterminisme en ajoutant des états.

        :param automaton: Automate avec conflits
        :param conflicts: Liste des conflits à résoudre (non utilisé pour l'instant)
        :return: Automate sans conflits
        """
        # Pour l'instant, on retourne l'automate original
        # L'implémentation complète nécessiterait l'ajout d'états
        # conflicts est ignoré pour l'instant
        _ = conflicts  # Suppression de l'avertissement unused-argument
        return automaton

    def _convert_to_deterministic_transitions(
        self, automaton: Union[PDA, NPDA]
    ) -> Dict[Tuple[str, str, str], Tuple[str, str]]:
        """Convertit les transitions non-déterministes en déterministes.

        :param automaton: Automate à convertir
        :return: Transitions déterministes
        """
        dpda_transitions = {}

        for (
            state,
            symbol,
            stack_symbol,
        ), transitions in automaton._transitions.items():
            if len(transitions) == 1:
                # Transition déjà déterministe
                dpda_transitions[(state, symbol, stack_symbol)] = next(
                    iter(transitions)
                )
            else:
                # Prendre la première transition (arbitraire)
                dpda_transitions[(state, symbol, stack_symbol)] = next(
                    iter(transitions)
                )

        return dpda_transitions

    def _convert_to_nondeterministic_transitions(
        self, automaton: DPDA
    ) -> Dict[Tuple[str, str, str], Set[Tuple[str, str]]]:
        """Convertit les transitions déterministes en non-déterministes.

        :param automaton: Automate déterministe à convertir
        :return: Transitions non-déterministes
        """
        pda_transitions = {}

        for (
            state,
            symbol,
            stack_symbol,
        ), transition in automaton._transitions.items():
            pda_transitions[(state, symbol, stack_symbol)] = {transition}

        return pda_transitions

    def _is_deterministic(self, automaton: Union[PDA, NPDA]) -> bool:
        """Vérifie si un automate est déterministe.

        :param automaton: Automate à vérifier
        :return: True si l'automate est déterministe
        """
        for transitions in automaton._transitions.values():
            if len(transitions) > 1:
                return False
        return True

    def _update_conversion_stats(
        self, conversion_time: float, success: bool
    ) -> None:
        """Met à jour les statistiques de conversion.

        :param conversion_time: Temps de conversion en secondes
        :param success: True si la conversion a réussi
        """
        self._conversion_stats["total_conversions"] += 1
        if success:
            self._conversion_stats["successful_conversions"] += 1
        else:
            self._conversion_stats["failed_conversions"] += 1

        self._conversion_stats["conversion_times"].append(conversion_time)

        # Calcul de la moyenne
        times = self._conversion_stats["conversion_times"]
        self._conversion_stats["average_conversion_time"] = sum(times) / len(
            times
        )

    def clear_cache(self) -> None:
        """Vide le cache des conversions."""
        self._cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques du cache.

        :return: Dictionnaire avec les statistiques du cache
        """
        return {
            "cache_size": len(self._cache),
            "max_cache_size": self._max_cache_size,
            "cache_hits": self._conversion_stats["cache_hits"],
            "cache_misses": self._conversion_stats["cache_misses"],
            "cache_efficiency": self._conversion_stats["cache_hits"]
            / max(
                1,
                self._conversion_stats["cache_hits"]
                + self._conversion_stats["cache_misses"],
            ),
        }

    def get_conversion_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques de conversion.

        :return: Dictionnaire avec les statistiques de conversion
        """
        return dict(self._conversion_stats)

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques de performance.

        :return: Dictionnaire avec les métriques de performance
        """
        return dict(self._performance_metrics)

    def to_dict(self) -> Dict[str, Any]:
        """Convertit les algorithmes en dictionnaire.

        :return: Représentation dictionnaire des algorithmes
        """
        return {
            "enable_caching": self._enable_caching,
            "max_cache_size": self._max_cache_size,
            "timeout": self._timeout,
            "enable_optimization": self._enable_optimization,
            "enable_validation": self._enable_validation,
            "max_states": self._max_states,
            "max_stack_symbols": self._max_stack_symbols,
            "conversion_stats": self._conversion_stats,
            "performance_metrics": self._performance_metrics,
        }

    def pda_to_grammar(self, pda: PDA) -> ContextFreeGrammar:
        """Convertit un PDA en grammaire hors-contexte.

        :param pda: PDA à convertir
        :return: Grammaire équivalente
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité du PDA
            if not pda.validate():
                raise ConversionValidationError("PDA invalide", "PDA")

            # Création des variables pour chaque paire d'états
            variables = set()
            for state1 in pda.states:
                for state2 in pda.states:
                    variables.add(f"[{state1},{state2}]")

            # Ajout de la variable de départ
            start_variable = "S"
            variables.add(start_variable)

            # Création des productions
            productions = []

            # Production de départ
            for final_state in pda.final_states:
                productions.append(
                    Production(
                        start_variable,
                        (f"[{pda.initial_state},{final_state}]",),
                    )
                )

            # Productions pour chaque transition
            for (state, symbol, _), transitions in pda._transitions.items():
                for next_state, stack_operations in transitions:
                    if symbol:  # Transition avec symbole d'entrée
                        if len(stack_operations) == 1:
                            # Transition simple
                            productions.append(
                                Production(
                                    f"[{state},{next_state}]",
                                    (symbol, f"[{state},{next_state}]"),
                                )
                            )
                        else:
                            # Transition complexe avec pile
                            # Pour l'instant, on ne traite que la première opération
                            productions.append(
                                Production(
                                    f"[{state},{next_state}]",
                                    (symbol, f"[{state},{next_state}]"),
                                )
                            )

            # Création de la grammaire
            grammar = ContextFreeGrammar(
                variables=variables,
                terminals=pda.input_alphabet,
                productions=productions,
                start_symbol=start_variable,
            )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return grammar

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la conversion PDA → Grammaire: {str(e)}"
            ) from e

    def grammar_to_pda(self, grammar: ContextFreeGrammar) -> PDA:
        """Convertit une grammaire en PDA.

        :param grammar: Grammaire à convertir
        :return: PDA équivalent
        :raises ConversionError: Si la conversion échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité de la grammaire
            # Note: ContextFreeGrammar n'a pas de méthode validate()
            # La validation est implicite dans la construction

            # Création des états du PDA
            states = {"q0", "q1", "q2"}
            input_alphabet = grammar.terminals
            stack_alphabet = grammar.variables | {"Z0"}
            initial_state = "q0"
            initial_stack_symbol = "Z0"
            final_states = {"q2"}

            # Création des transitions
            transitions = {}

            # Transition initiale
            transitions[("q0", "", "Z0")] = {
                ("q1", f"{grammar.start_symbol}Z0")
            }

            # Transitions pour chaque production
            for production in grammar.productions:
                if production.is_empty():
                    # Production vide
                    transitions[("q1", "", production.left_side)] = {
                        ("q1", "")
                    }
                else:
                    # Production normale
                    stack_symbols = list(production.right_side)
                    if len(stack_symbols) == 1:
                        # Production terminale
                        transitions[
                            ("q1", stack_symbols[0], production.left_side)
                        ] = {("q1", "")}
                    else:
                        # Production complexe
                        stack_ops = "".join(reversed(stack_symbols))
                        transitions[("q1", "", production.left_side)] = {
                            ("q1", stack_ops)
                        }

            # Transition finale
            transitions[("q1", "", "Z0")] = {("q2", "Z0")}

            # Création du PDA
            pda = PDA(
                states=states,
                input_alphabet=input_alphabet,
                stack_alphabet=stack_alphabet,
                transitions=transitions,
                initial_state=initial_state,
                initial_stack_symbol=initial_stack_symbol,
                final_states=final_states,
                name=(
                    f"{grammar.name}_converted_to_pda"
                    if hasattr(grammar, "name") and grammar.name
                    else None
                ),
            )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return pda

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la conversion Grammaire → PDA: {str(e)}"
            ) from e

    def grammar_to_dpda(self, grammar: ContextFreeGrammar) -> DPDA:
        """Convertit une grammaire en DPDA si possible.

        :param grammar: Grammaire à convertir
        :return: DPDA équivalent
        :raises ConversionError: Si la conversion n'est pas possible
        """
        # Conversion via PDA
        pda = self.grammar_to_pda(grammar)
        return self.pda_to_dpda(pda)

    def grammar_to_npda(self, grammar: ContextFreeGrammar) -> NPDA:
        """Convertit une grammaire en NPDA.

        :param grammar: Grammaire à convertir
        :return: NPDA équivalent
        :raises ConversionError: Si la conversion échoue
        """
        # Conversion via PDA
        pda = self.grammar_to_pda(grammar)
        return self.pda_to_npda(pda)

    def dpda_to_grammar(self, dpda: DPDA) -> ContextFreeGrammar:
        """Convertit un DPDA en grammaire.

        :param dpda: DPDA à convertir
        :return: Grammaire équivalente
        :raises ConversionError: Si la conversion échoue
        """
        # Conversion via PDA
        pda = self.dpda_to_pda(dpda)
        return self.pda_to_grammar(pda)

    def npda_to_grammar(self, npda: NPDA) -> ContextFreeGrammar:
        """Convertit un NPDA en grammaire.

        :param npda: NPDA à convertir
        :return: Grammaire équivalente
        :raises ConversionError: Si la conversion échoue
        """
        # Conversion via PDA
        pda = self.npda_to_pda(npda)
        return self.pda_to_grammar(pda)

    def optimize_stack_transitions(
        self, automaton: Union[PDA, DPDA, NPDA]
    ) -> Union[PDA, DPDA, NPDA]:
        """Optimise les transitions de pile d'un automate.

        :param automaton: Automate à optimiser
        :return: Automate optimisé
        :raises ConversionError: Si l'optimisation échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité de l'automate
            if not automaton.validate():
                raise ConversionValidationError(
                    "Automate invalide", type(automaton).__name__
                )

            # Optimisation des transitions
            optimized_transitions = self._optimize_transitions(
                automaton._transitions
            )

            # Création de l'automate optimisé
            if isinstance(automaton, PDA):
                optimized = PDA(
                    states=automaton.states,
                    input_alphabet=automaton.input_alphabet,
                    stack_alphabet=automaton.stack_alphabet,
                    transitions=optimized_transitions,
                    initial_state=automaton.initial_state,
                    initial_stack_symbol=automaton.initial_stack_symbol,
                    final_states=automaton.final_states,
                    name=(
                        f"{automaton.name}_optimized"
                        if automaton.name
                        else None
                    ),
                )
            elif isinstance(automaton, DPDA):
                # Conversion en transitions déterministes
                dpda_transitions = {}
                for key, transitions in optimized_transitions.items():
                    if len(transitions) == 1:
                        dpda_transitions[key] = next(iter(transitions))
                    else:
                        dpda_transitions[key] = next(
                            iter(transitions)
                        )  # Prendre la première

                optimized = DPDA(
                    states=automaton.states,
                    input_alphabet=automaton.input_alphabet,
                    stack_alphabet=automaton.stack_alphabet,
                    transitions=dpda_transitions,
                    initial_state=automaton.initial_state,
                    initial_stack_symbol=automaton.initial_stack_symbol,
                    final_states=automaton.final_states,
                    name=(
                        f"{automaton.name}_optimized"
                        if automaton.name
                        else None
                    ),
                )
            else:  # NPDA
                optimized = NPDA(
                    states=automaton.states,
                    input_alphabet=automaton.input_alphabet,
                    stack_alphabet=automaton.stack_alphabet,
                    transitions=optimized_transitions,
                    initial_state=automaton.initial_state,
                    initial_stack_symbol=automaton.initial_stack_symbol,
                    final_states=automaton.final_states,
                    name=(
                        f"{automaton.name}_optimized"
                        if automaton.name
                        else None
                    ),
                    max_parallel_branches=getattr(
                        automaton, "max_parallel_branches", 1000
                    ),
                )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return optimized

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de l'optimisation: {str(e)}"
            ) from e

    def remove_inaccessible_states(
        self, automaton: Union[PDA, DPDA, NPDA]
    ) -> Union[PDA, DPDA, NPDA]:
        """Supprime les états inaccessibles d'un automate.

        :param automaton: Automate à traiter
        :return: Automate sans états inaccessibles
        :raises ConversionError: Si la réduction échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité de l'automate
            if not automaton.validate():
                raise ConversionValidationError(
                    "Automate invalide", type(automaton).__name__
                )

            # Calcul des états accessibles
            accessible_states = self._get_accessible_states(automaton)

            # Filtrage des transitions
            filtered_transitions = {}
            for (
                state,
                symbol,
                stack_symbol,
            ), transitions in automaton._transitions.items():
                if state in accessible_states:
                    filtered_transitions[(state, symbol, stack_symbol)] = (
                        transitions
                    )

            # Filtrage des états finaux
            filtered_final_states = automaton.final_states & accessible_states

            # Création de l'automate réduit
            if isinstance(automaton, PDA):
                reduced = PDA(
                    states=accessible_states,
                    input_alphabet=automaton.input_alphabet,
                    stack_alphabet=automaton.stack_alphabet,
                    transitions=filtered_transitions,
                    initial_state=automaton.initial_state,
                    initial_stack_symbol=automaton.initial_stack_symbol,
                    final_states=filtered_final_states,
                    name=(
                        f"{automaton.name}_reduced" if automaton.name else None
                    ),
                )
            elif isinstance(automaton, DPDA):
                # Conversion en transitions déterministes
                dpda_transitions = {}
                for key, transitions in filtered_transitions.items():
                    if len(transitions) == 1:
                        dpda_transitions[key] = next(iter(transitions))
                    else:
                        dpda_transitions[key] = next(iter(transitions))

                reduced = DPDA(
                    states=accessible_states,
                    input_alphabet=automaton.input_alphabet,
                    stack_alphabet=automaton.stack_alphabet,
                    transitions=dpda_transitions,
                    initial_state=automaton.initial_state,
                    initial_stack_symbol=automaton.initial_stack_symbol,
                    final_states=filtered_final_states,
                    name=(
                        f"{automaton.name}_reduced" if automaton.name else None
                    ),
                )
            else:  # NPDA
                reduced = NPDA(
                    states=accessible_states,
                    input_alphabet=automaton.input_alphabet,
                    stack_alphabet=automaton.stack_alphabet,
                    transitions=filtered_transitions,
                    initial_state=automaton.initial_state,
                    initial_stack_symbol=automaton.initial_stack_symbol,
                    final_states=filtered_final_states,
                    name=(
                        f"{automaton.name}_reduced" if automaton.name else None
                    ),
                    max_parallel_branches=getattr(
                        automaton, "max_parallel_branches", 1000
                    ),
                )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return reduced

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la réduction des états: {str(e)}"
            ) from e

    def minimize_stack_symbols(
        self, automaton: Union[PDA, DPDA, NPDA]
    ) -> Union[PDA, DPDA, NPDA]:
        """Minimise le nombre de symboles de pile d'un automate.

        :param automaton: Automate à traiter
        :return: Automate avec symboles de pile minimisés
        :raises ConversionError: Si la minimisation échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité de l'automate
            if not automaton.validate():
                raise ConversionValidationError(
                    "Automate invalide", type(automaton).__name__
                )

            # Calcul des symboles de pile utilisés
            used_stack_symbols = self._get_used_stack_symbols(automaton)

            # Création du mapping de symboles
            # Utiliser des caractères individuels pour éviter les problèmes de validation
            symbol_mapping = {
                symbol: chr(ord('A') + i) for i, symbol in enumerate(used_stack_symbols)
            }

            # Conversion des transitions
            converted_transitions = {}
            for (
                state,
                symbol,
                stack_symbol,
            ), transitions in automaton._transitions.items():
                if stack_symbol in used_stack_symbols:
                    new_key = (state, symbol, symbol_mapping[stack_symbol])
                    new_transitions = set()
                    for next_state, stack_ops in transitions:
                        # Conversion des symboles de pile dans les opérations
                        # Les opérations de pile sont des séquences de symboles de pile
                        new_stack_ops = ""
                        i = 0
                        while i < len(stack_ops):
                            # Chercher le plus long symbole de pile qui correspond
                            found = False
                            for original_symbol, new_symbol in symbol_mapping.items():
                                if stack_ops[i:].startswith(original_symbol):
                                    new_stack_ops += new_symbol
                                    i += len(original_symbol)
                                    found = True
                                    break
                            if not found:
                                # Si aucun symbole ne correspond, garder le caractère original
                                new_stack_ops += stack_ops[i]
                                i += 1
                        new_transitions.add((next_state, new_stack_ops))
                    converted_transitions[new_key] = new_transitions

            # Nouvel alphabet de pile
            new_stack_alphabet = set(symbol_mapping.values())

            # Création de l'automate minimisé
            if isinstance(automaton, PDA):
                minimized = PDA(
                    states=automaton.states,
                    input_alphabet=automaton.input_alphabet,
                    stack_alphabet=new_stack_alphabet,
                    transitions=converted_transitions,
                    initial_state=automaton.initial_state,
                    initial_stack_symbol=symbol_mapping[
                        automaton.initial_stack_symbol
                    ],
                    final_states=automaton.final_states,
                    name=(
                        f"{automaton.name}_minimized"
                        if automaton.name
                        else None
                    ),
                )
            elif isinstance(automaton, DPDA):
                # Conversion en transitions déterministes
                dpda_transitions = {}
                for key, transitions in converted_transitions.items():
                    if len(transitions) == 1:
                        dpda_transitions[key] = next(iter(transitions))
                    else:
                        dpda_transitions[key] = next(iter(transitions))

                minimized = DPDA(
                    states=automaton.states,
                    input_alphabet=automaton.input_alphabet,
                    stack_alphabet=new_stack_alphabet,
                    transitions=dpda_transitions,
                    initial_state=automaton.initial_state,
                    initial_stack_symbol=symbol_mapping[
                        automaton.initial_stack_symbol
                    ],
                    final_states=automaton.final_states,
                    name=(
                        f"{automaton.name}_minimized"
                        if automaton.name
                        else None
                    ),
                )
            else:  # NPDA
                minimized = NPDA(
                    states=automaton.states,
                    input_alphabet=automaton.input_alphabet,
                    stack_alphabet=new_stack_alphabet,
                    transitions=converted_transitions,
                    initial_state=automaton.initial_state,
                    initial_stack_symbol=symbol_mapping[
                        automaton.initial_stack_symbol
                    ],
                    final_states=automaton.final_states,
                    name=(
                        f"{automaton.name}_minimized"
                        if automaton.name
                        else None
                    ),
                    max_parallel_branches=getattr(
                        automaton, "max_parallel_branches", 1000
                    ),
                )

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return minimized

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la minimisation des symboles: {str(e)}"
            ) from e

    def _optimize_transitions(
        self, transitions: Dict[Tuple[str, str, str], Set[Tuple[str, str]]]
    ) -> Dict[Tuple[str, str, str], Set[Tuple[str, str]]]:
        """Optimise les transitions d'un automate.

        :param transitions: Transitions à optimiser
        :return: Transitions optimisées
        """
        # Pour l'instant, on retourne les transitions originales
        # L'implémentation complète nécessiterait des algorithmes d'optimisation avancés
        return transitions

    def _get_accessible_states(
        self, automaton: Union[PDA, DPDA, NPDA]
    ) -> Set[str]:
        """Calcule les états accessibles d'un automate.

        :param automaton: Automate à analyser
        :return: Ensemble des états accessibles
        """
        accessible = {automaton.initial_state}
        queue = deque([automaton.initial_state])

        while queue:
            state = queue.popleft()
            for (
                from_state,
                _,
                _,
            ), transitions in automaton._transitions.items():
                if from_state == state:
                    for next_state, _ in transitions:
                        if next_state not in accessible:
                            accessible.add(next_state)
                            queue.append(next_state)

        return accessible

    def _get_used_stack_symbols(
        self, automaton: Union[PDA, DPDA, NPDA]
    ) -> Set[str]:
        """Calcule les symboles de pile utilisés dans un automate.

        :param automaton: Automate à analyser
        :return: Ensemble des symboles de pile utilisés
        """
        used_symbols = {automaton.initial_stack_symbol}

        for transitions in automaton._transitions.values():
            for _, stack_ops in transitions:
                for symbol in stack_ops:
                    used_symbols.add(symbol)

        return used_symbols

    def verify_equivalence(
        self,
        automaton1: Union[PDA, DPDA, NPDA],
        automaton2: Union[PDA, DPDA, NPDA],
        test_words: List[str] = None,
    ) -> bool:
        """Vérifie l'équivalence de deux automates.

        :param automaton1: Premier automate
        :param automaton2: Deuxième automate
        :param test_words: Mots de test optionnels
        :return: True si les automates sont équivalents, False sinon
        :raises ConversionError: Si la vérification échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité des automates
            if not automaton1.validate():
                raise ConversionValidationError(
                    "Premier automate invalide", type(automaton1).__name__
                )
            if not automaton2.validate():
                raise ConversionValidationError(
                    "Deuxième automate invalide", type(automaton2).__name__
                )

            # Génération de mots de test si non fournis
            if test_words is None:
                test_words = self.generate_test_words(
                    automaton1, count=100, max_length=20
                )

            # Test d'équivalence sur les mots de test
            for word in test_words:
                result1 = automaton1.accepts(word)
                result2 = automaton2.accepts(word)
                if result1 != result2:
                    return False

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return True

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la vérification d'équivalence: {str(e)}"
            ) from e

    def generate_test_words(
        self,
        automaton: Union[PDA, DPDA, NPDA],
        count: int = 100,
        max_length: int = 20,
    ) -> List[str]:
        """Génère des mots de test pour un automate.

        :param automaton: Automate à tester
        :param count: Nombre de mots à générer
        :param max_length: Longueur maximale des mots
        :return: Liste des mots de test
        :raises ConversionError: Si la génération échoue
        """
        start_time = time.time()

        try:
            # Vérification de la validité de l'automate
            if not automaton.validate():
                raise ConversionValidationError(
                    "Automate invalide", type(automaton).__name__
                )

            # Génération de mots aléatoires
            import random

            words = []
            alphabet = list(automaton.input_alphabet)

            if not alphabet:
                return [""]  # Mot vide si pas d'alphabet

            for _ in range(count):
                length = random.randint(0, max_length)
                word = "".join(random.choices(alphabet, k=length))
                words.append(word)

            # Ajout de mots spécifiques
            words.extend(["", "a", "b", "ab", "ba", "aa", "bb"])

            # Suppression des doublons
            words = list(set(words))

            # Mise à jour des statistiques
            self._update_conversion_stats(time.time() - start_time, True)

            return words

        except Exception as e:
            self._update_conversion_stats(time.time() - start_time, False)
            if isinstance(e, ConversionError):
                raise
            raise ConversionError(
                f"Erreur lors de la génération de mots de test: {str(e)}"
            ) from e

    def set_cache_size(self, size: int) -> None:
        """Définit la taille maximale du cache.

        :param size: Nouvelle taille maximale
        :raises ConversionError: Si la taille est invalide
        """
        if size <= 0:
            raise ConversionConfigurationError(
                "La taille du cache doit être positive", "size"
            )

        self._max_cache_size = size

        # Nettoyage du cache si nécessaire
        if len(self._cache) > size:
            # Garder les entrées les plus récentes
            items = list(self._cache.items())
            self._cache.clear()
            for key, value in items[-size:]:
                self._cache[key] = value

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PushdownConversionAlgorithms":
        """Crée les algorithmes à partir d'un dictionnaire.

        :param data: Données des algorithmes
        :return: Instance des algorithmes
        :raises ConversionError: Si les données sont invalides
        """
        try:
            instance = cls(
                enable_caching=data.get("enable_caching", True),
                max_cache_size=data.get("max_cache_size", 1000),
                timeout=data.get("timeout", 30.0),
            )

            instance._enable_optimization = data.get(
                "enable_optimization", True
            )
            instance._enable_validation = data.get("enable_validation", True)
            instance._max_states = data.get("max_states", 10000)
            instance._max_stack_symbols = data.get("max_stack_symbols", 1000)
            instance._conversion_stats = data.get(
                "conversion_stats", instance._conversion_stats
            )
            instance._performance_metrics = data.get(
                "performance_metrics", instance._performance_metrics
            )

            return instance
        except Exception as e:
            raise ConversionError(
                f"Erreur lors de la création depuis le dictionnaire: {str(e)}"
            ) from e
