"""
Tests unitaires pour l'implémentation Transition.

Ce module teste l'implémentation concrète Transition de l'interface ITransition.
"""

import pytest

from baobab_automata.implementations.transition import Transition
from baobab_automata.implementations.state import State
from baobab_automata.interfaces.state import StateType
from baobab_automata.interfaces.transition import TransitionType


class TestTransitionImplementation:
    """Tests pour l'implémentation Transition."""

    def test_transition_creation_all_types(self):
        """Test de création de transitions de tous les types."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)

        transitions = [
            Transition(source, target, "a", TransitionType.SYMBOL),
            Transition(source, target, None, TransitionType.EPSILON),
            Transition(source, target, "A", TransitionType.STACK_PUSH),
            Transition(source, target, "A", TransitionType.STACK_POP),
            Transition(source, target, "A", TransitionType.STACK_READ),
            Transition(source, target, "a", TransitionType.TAPE_READ),
            Transition(source, target, "b", TransitionType.TAPE_WRITE),
            Transition(source, target, "L", TransitionType.TAPE_MOVE),
        ]

        for transition in transitions:
            assert isinstance(transition, Transition)
            assert transition.source_state == source
            assert transition.target_state == target

    def test_transition_with_conditions_and_actions(self):
        """Test de création de transition avec conditions et actions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        conditions = {"stack_top": "A", "tape_symbol": "a"}
        actions = {"stack_push": "B", "tape_write": "b"}

        transition = Transition(
            source, target, "a", TransitionType.SYMBOL, conditions, actions
        )

        assert transition.conditions == conditions
        assert transition.actions == actions

    def test_transition_default_conditions_and_actions(self):
        """Test de création de transition avec conditions et actions par défaut."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)

        transition = Transition(source, target, "a", TransitionType.SYMBOL)

        assert transition.conditions == {}
        assert transition.actions == {}

    def test_is_applicable_symbol_transition(self):
        """Test de is_applicable pour une transition symbolique."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)

        # Symbole correct
        assert transition.is_applicable("a", {}) is True

        # Symbole incorrect
        assert transition.is_applicable("b", {}) is False

        # Symbole None
        assert transition.is_applicable(None, {}) is False

    def test_is_applicable_epsilon_transition(self):
        """Test de is_applicable pour une transition epsilon."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        transition = Transition(source, target, None, TransitionType.EPSILON)

        # Transition epsilon applicable avec n'importe quel symbole
        assert transition.is_applicable("a", {}) is True
        assert transition.is_applicable("b", {}) is True
        assert transition.is_applicable(None, {}) is True

    def test_is_applicable_with_conditions(self):
        """Test de is_applicable avec des conditions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        conditions = {"stack_top": "A", "tape_symbol": "a"}
        transition = Transition(
            source, target, "a", TransitionType.SYMBOL, conditions
        )

        # Contexte satisfaisant toutes les conditions
        context1 = {"stack_top": "A", "tape_symbol": "a"}
        assert transition.is_applicable("a", context1) is True

        # Contexte ne satisfaisant pas toutes les conditions
        context2 = {"stack_top": "B", "tape_symbol": "a"}
        assert transition.is_applicable("a", context2) is False

        # Contexte manquant une condition
        context3 = {"stack_top": "A"}
        assert transition.is_applicable("a", context3) is False

        # Contexte avec conditions supplémentaires
        context4 = {"stack_top": "A", "tape_symbol": "a", "extra": "value"}
        assert transition.is_applicable("a", context4) is True

    def test_is_applicable_empty_conditions(self):
        """Test de is_applicable avec des conditions vides."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        transition = Transition(source, target, "a", TransitionType.SYMBOL, {})

        # Transition applicable avec le bon symbole
        assert transition.is_applicable("a", {}) is True
        assert transition.is_applicable("a", {"any": "context"}) is True

    def test_execute_with_actions(self):
        """Test de execute avec des actions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        actions = {"stack_push": "A", "tape_write": "b", "counter": 1}
        transition = Transition(
            source, target, "a", TransitionType.SYMBOL, {}, actions
        )

        context = {"current_state": source, "existing": "value"}
        new_context = transition.execute(context)

        # Vérifier que le contexte original n'est pas modifié
        assert context == {"current_state": source, "existing": "value"}

        # Vérifier que le nouveau contexte contient les actions
        expected_context = {
            "current_state": source,
            "existing": "value",
            "stack_push": "A",
            "tape_write": "b",
            "counter": 1,
        }
        assert new_context == expected_context

    def test_execute_empty_actions(self):
        """Test de execute avec des actions vides."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)

        context = {"current_state": source, "existing": "value"}
        new_context = transition.execute(context)

        # Le contexte doit être une copie identique
        assert new_context == context
        assert new_context is not context  # Vérifier que c'est une copie

    def test_execute_overwrite_existing_values(self):
        """Test de execute qui écrase des valeurs existantes."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        actions = {"counter": 2, "status": "updated"}
        transition = Transition(
            source, target, "a", TransitionType.SYMBOL, {}, actions
        )

        context = {"counter": 1, "status": "original", "other": "value"}
        new_context = transition.execute(context)

        # Vérifier que les valeurs sont écrasées
        assert new_context["counter"] == 2
        assert new_context["status"] == "updated"
        assert new_context["other"] == "value"

    def test_equality(self):
        """Test de l'égalité entre transitions."""
        source1 = State("q0", StateType.INITIAL)
        target1 = State("q1", StateType.FINAL)
        source2 = State("q0", StateType.INITIAL)
        target2 = State("q1", StateType.FINAL)
        source3 = State("q2", StateType.INITIAL)

        transition1 = Transition(source1, target1, "a", TransitionType.SYMBOL)
        transition2 = Transition(source2, target2, "a", TransitionType.SYMBOL)
        transition3 = Transition(source3, target1, "a", TransitionType.SYMBOL)
        transition4 = Transition(source1, target1, "b", TransitionType.SYMBOL)
        transition5 = Transition(source1, target1, "a", TransitionType.EPSILON)

        # Transitions identiques
        assert transition1 == transition2

        # États source différents
        assert transition1 != transition3

        # Symboles différents
        assert transition1 != transition4

        # Types différents
        assert transition1 != transition5

        # Comparaison avec autre type
        assert transition1 != "not_a_transition"
        assert transition1 != 42

    def test_hash(self):
        """Test du hachage des transitions."""
        source1 = State("q0", StateType.INITIAL)
        target1 = State("q1", StateType.FINAL)
        source2 = State("q0", StateType.INITIAL)
        target2 = State("q1", StateType.FINAL)

        transition1 = Transition(source1, target1, "a", TransitionType.SYMBOL)
        transition2 = Transition(source2, target2, "a", TransitionType.SYMBOL)

        # Transitions identiques = même hash
        assert hash(transition1) == hash(transition2)

        # Hash stable
        assert hash(transition1) == hash(transition1)

    def test_transition_in_sets(self):
        """Test d'utilisation des transitions dans des sets."""
        source1 = State("q0", StateType.INITIAL)
        target1 = State("q1", StateType.FINAL)
        source2 = State("q0", StateType.INITIAL)
        target2 = State("q1", StateType.FINAL)
        source3 = State("q2", StateType.INITIAL)

        transition1 = Transition(source1, target1, "a", TransitionType.SYMBOL)
        transition2 = Transition(source2, target2, "a", TransitionType.SYMBOL)
        transition3 = Transition(source3, target1, "a", TransitionType.SYMBOL)

        transition_set = {transition1, transition2, transition3}

        # Les transitions identiques ne doivent apparaître qu'une fois
        assert len(transition_set) == 2
        assert transition1 in transition_set
        assert transition2 in transition_set
        assert transition3 in transition_set

    def test_string_representation(self):
        """Test de la représentation string des transitions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)

        # Transition avec symbole
        transition1 = Transition(source, target, "a", TransitionType.SYMBOL)
        assert str(transition1) == "State(q0) --a--> State(q1)"

        # Transition epsilon
        transition2 = Transition(source, target, None, TransitionType.EPSILON)
        assert str(transition2) == "State(q0) --ε--> State(q1)"

        # Transition avec symbole complexe
        transition3 = Transition(source, target, "ε", TransitionType.SYMBOL)
        assert str(transition3) == "State(q0) --ε--> State(q1)"

    def test_transition_immutability(self):
        """Test de l'immutabilité des transitions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)

        # Vérifier que la transition est hashable
        assert hash(transition) is not None

        # Vérifier que les attributs ne peuvent pas être modifiés
        with pytest.raises(AttributeError):
            transition.symbol = "b"

        with pytest.raises(AttributeError):
            transition.transition_type = TransitionType.EPSILON

        with pytest.raises(AttributeError):
            transition.conditions = {"new": "condition"}

        with pytest.raises(AttributeError):
            transition.actions = {"new": "action"}

    def test_transition_conditions_immutability(self):
        """Test de l'immutabilité des conditions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        conditions = {"key": "value"}
        transition = Transition(
            source, target, "a", TransitionType.SYMBOL, conditions
        )

        # Les conditions ne doivent pas pouvoir être modifiées
        with pytest.raises(TypeError):
            transition.conditions["new_key"] = "new_value"

    def test_transition_actions_immutability(self):
        """Test de l'immutabilité des actions."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        actions = {"key": "value"}
        transition = Transition(
            source, target, "a", TransitionType.SYMBOL, {}, actions
        )

        # Les actions ne doivent pas pouvoir être modifiées
        with pytest.raises(TypeError):
            transition.actions["new_key"] = "new_value"
