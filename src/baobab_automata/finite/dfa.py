"""
Implémentation d'un automate fini déterministe (DFA).

Ce module contient la classe DFA qui implémente l'interface IAutomaton
pour les automates finis déterministes.
"""

from typing import Any, Dict, List, Optional, Set

from ..interfaces.automaton import IAutomaton, AutomatonType
from ..interfaces.state import IState
from ..interfaces.transition import ITransition


class DFA(IAutomaton):
    """
    Implémentation d'un automate fini déterministe (DFA).
    
    Un DFA est un automate fini où pour chaque état et chaque symbole,
    il existe exactement une transition possible.
    
    :param states: Ensemble des états de l'automate
    :type states: Set[IState]
    :param initial_states: Ensemble des états initiaux
    :type initial_states: Set[IState]
    :param final_states: Ensemble des états finaux
    :type final_states: Set[IState]
    :param alphabet: Alphabet de l'automate
    :type alphabet: Set[str]
    :param transitions: Ensemble des transitions
    :type transitions: Set[ITransition]
    """
    
    def __init__(
        self,
        states: Set[IState],
        initial_states: Set[IState],
        final_states: Set[IState],
        alphabet: Set[str],
        transitions: Set[ITransition]
    ):
        """Initialise un DFA."""
        self._states = states.copy()
        self._initial_states = initial_states.copy()
        self._final_states = final_states.copy()
        self._alphabet = alphabet.copy()
        self._transitions = transitions.copy()
    
    @property
    def automaton_type(self) -> AutomatonType:
        """Type de l'automate."""
        return AutomatonType.DFA
    
    @property
    def states(self) -> Set[IState]:
        """Ensemble des états de l'automate."""
        return self._states.copy()
    
    @property
    def initial_states(self) -> Set[IState]:
        """Ensemble des états initiaux."""
        return self._initial_states.copy()
    
    @property
    def final_states(self) -> Set[IState]:
        """Ensemble des états finaux."""
        return self._final_states.copy()
    
    @property
    def alphabet(self) -> Set[str]:
        """Alphabet de l'automate."""
        return self._alphabet.copy()
    
    @property
    def transitions(self) -> Set[ITransition]:
        """Ensemble des transitions de l'automate."""
        return self._transitions.copy()
    
    def add_state(self, state: IState) -> None:
        """Ajoute un état à l'automate."""
        self._states.add(state)
    
    def remove_state(self, state: IState) -> None:
        """Supprime un état de l'automate."""
        if state in self._states:
            self._states.remove(state)
            self._initial_states.discard(state)
            self._final_states.discard(state)
            # Supprimer les transitions associées
            self._transitions = {
                t for t in self._transitions
                if t.source_state != state and t.target_state != state
            }
    
    def add_transition(self, transition: ITransition) -> None:
        """Ajoute une transition à l'automate."""
        self._transitions.add(transition)
    
    def remove_transition(self, transition: ITransition) -> None:
        """Supprime une transition de l'automate."""
        self._transitions.discard(transition)
    
    def get_transitions_from(self, state: IState) -> Set[ITransition]:
        """Récupère les transitions partant d'un état."""
        return {
            t for t in self._transitions
            if t.source_state == state
        }
    
    def get_transitions_to(self, state: IState) -> Set[ITransition]:
        """Récupère les transitions arrivant à un état."""
        return {
            t for t in self._transitions
            if t.target_state == state
        }
    
    def get_transitions(
        self, source: IState, symbol: Optional[str]
    ) -> Set[ITransition]:
        """Récupère les transitions pour un état et un symbole donnés."""
        return {
            t for t in self._transitions
            if t.source_state == source and t.symbol == symbol
        }
    
    def is_valid(self) -> bool:
        """Vérifie si l'automate est valide."""
        errors = self.validate()
        return len(errors) == 0
    
    def validate(self) -> List[str]:
        """Valide l'automate et retourne la liste des erreurs."""
        errors = []
        
        # Vérifier qu'il y a au moins un état initial
        if not self._initial_states:
            errors.append("DFA must have at least one initial state")
        
        # Vérifier que tous les états initiaux sont dans l'ensemble des états
        for state in self._initial_states:
            if state not in self._states:
                errors.append(f"Initial state {state} is not in states set")
        
        # Vérifier que tous les états finaux sont dans l'ensemble des états
        for state in self._final_states:
            if state not in self._states:
                errors.append(f"Final state {state} is not in states set")
        
        # Vérifier que toutes les transitions utilisent des états valides
        for transition in self._transitions:
            if transition.source_state not in self._states:
                errors.append(f"Transition source state {transition.source_state} is not in states set")
            if transition.target_state not in self._states:
                errors.append(f"Transition target state {transition.target_state} is not in states set")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Sérialise l'automate en dictionnaire."""
        return {
            "automaton_type": self.automaton_type.value,
            "states": [
                {
                    "identifier": state.identifier,
                    "state_type": state.state_type.value,
                    "metadata": dict(state.metadata)
                }
                for state in self._states
            ],
            "initial_states": [state.identifier for state in self._initial_states],
            "final_states": [state.identifier for state in self._final_states],
            "alphabet": list(self._alphabet),
            "transitions": [
                {
                    "source_state": transition.source_state.identifier,
                    "target_state": transition.target_state.identifier,
                    "symbol": transition.symbol,
                    "transition_type": transition.transition_type.value,
                    "conditions": dict(transition.conditions),
                    "actions": dict(transition.actions)
                }
                for transition in self._transitions
            ]
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Désérialise l'automate depuis un dictionnaire."""
        # Cette méthode sera implémentée plus tard
        raise NotImplementedError("from_dict not yet implemented")
    
    def __str__(self) -> str:
        """Représentation string de l'automate."""
        return f"DFA(states={len(self._states)}, transitions={len(self._transitions)})"
    
    def __repr__(self) -> str:
        """Représentation détaillée de l'automate."""
        return (
            f"DFA(states={self._states}, initial_states={self._initial_states}, "
            f"final_states={self._final_states}, alphabet={self._alphabet}, "
            f"transitions={self._transitions})"
        )