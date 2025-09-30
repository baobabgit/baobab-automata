"""
Tests unitaires pour l'interface ITransition et l'énumération TransitionType.

Ce module teste l'interface ITransition et l'énumération TransitionType.
"""

import pytest

from baobab_automata.interfaces.transition import ITransition, TransitionType
from baobab_automata.implementations.transition import Transition
from baobab_automata.implementations.state import State
from baobab_automata.interfaces.state import StateType


class TestTransitionType:
    """Tests pour l'énumération TransitionType."""

    def test_transition_type_values(self):
        """Test que tous les types de transitions sont définis."""
        assert TransitionType.SYMBOL.value == "symbol"
        assert TransitionType.EPSILON.value == "epsilon"
        assert TransitionType.STACK_PUSH.value == "stack_push"
        assert TransitionType.STACK_POP.value == "stack_pop"
        assert TransitionType.STACK_READ.value == "stack_read"
        assert TransitionType.TAPE_READ.value == "tape_read"
        assert TransitionType.TAPE_WRITE.value == "tape_write"
        assert TransitionType.TAPE_MOVE.value == "tape_move"

    def test_transition_type_enumeration(self):
        """Test que l'énumération contient tous les types attendus."""
        expected_types = {
            "symbol",
            "epsilon",
            "stack_push",
            "stack_pop",
            "stack_read",
            "tape_read",
            "tape_write",
            "tape_move",
        }
        actual_types = {
            transition_type.value for transition_type in TransitionType
        }
        assert actual_types == expected_types


class TestITransitionInterface:
    """Tests pour l'interface ITransition."""

    def test_interface_has_required_methods(self):
        """Test que l'interface ITransition a toutes les méthodes requises."""
        required_methods = [
            "source_state",
            "target_state",
            "symbol",
            "transition_type",
            "conditions",
            "actions",
            "is_applicable",
            "execute",
            "__eq__",
            "__hash__",
            "__str__",
        ]

        for method_name in required_methods:
            assert hasattr(
                ITransition, method_name
            ), f"Method {method_name} missing from ITransition"

    def test_interface_methods_are_abstract(self):
        """Test que les méthodes de l'interface sont abstraites."""
        # Vérifier que l'interface ne peut pas être instanciée directement
        with pytest.raises(TypeError):
            ITransition()


class TestTransitionImplementation:
    """Tests pour l'implémentation Transition de ITransition."""

    def test_transition_implements_interface(self):
        """Test que Transition implémente l'interface ITransition."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)
        assert isinstance(transition, ITransition)

    def test_transition_initialization(self):
        """Test de l'initialisation d'une transition."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        conditions = {"stack_top": "A"}
        actions = {"stack_push": "B"}

        transition = Transition(
            source, target, "a", TransitionType.SYMBOL, conditions, actions
        )

        assert transition.source_state == source
        assert transition.target_state == target
        assert transition.symbol == "a"
        assert transition.transition_type == TransitionType.SYMBOL
        assert transition.conditions == conditions
        assert transition.actions == actions

    def test_transition_initialization_default_values(self):
        """Test de l'initialisation avec valeurs par défaut."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)

        transition = Transition(source, target, None, TransitionType.EPSILON)

        assert transition.source_state == source
        assert transition.target_state == target
        assert transition.symbol is None
        assert transition.transition_type == TransitionType.EPSILON
        assert transition.conditions == {}
        assert transition.actions == {}

    def test_is_applicable_with_symbol(self):
        """Test de is_applicable avec un symbole."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)

        # Transition applicable avec le bon symbole
        assert transition.is_applicable("a", {}) is True

        # Transition non applicable avec un mauvais symbole
        assert transition.is_applicable("b", {}) is False

        # Transition non applicable avec None
        assert transition.is_applicable(None, {}) is False

    def test_is_applicable_epsilon(self):
        """Test de is_applicable avec une transition epsilon."""
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

    def test_execute(self):
        """Test de la méthode execute."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        actions = {"stack_push": "A", "tape_write": "b"}
        transition = Transition(
            source, target, "a", TransitionType.SYMBOL, {}, actions
        )

        context = {"current_state": source}
        new_context = transition.execute(context)

        # Vérifier que le contexte original n'est pas modifié
        assert context == {"current_state": source}

        # Vérifier que le nouveau contexte contient les actions
        expected_context = {
            "current_state": source,
            "stack_push": "A",
            "tape_write": "b",
        }
        assert new_context == expected_context

    def test_execute_empty_actions(self):
        """Test de execute avec des actions vides."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)

        context = {"current_state": source}
        new_context = transition.execute(context)

        # Le contexte doit être une copie identique
        assert new_context == context
        assert new_context is not context  # Vérifier que c'est une copie

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

        assert transition1 == transition2
        assert transition1 != transition3
        assert transition1 != "not_a_transition"

    def test_hash(self):
        """Test du hachage des transitions."""
        source1 = State("q0", StateType.INITIAL)
        target1 = State("q1", StateType.FINAL)
        source2 = State("q0", StateType.INITIAL)
        target2 = State("q1", StateType.FINAL)

        transition1 = Transition(source1, target1, "a", TransitionType.SYMBOL)
        transition2 = Transition(source2, target2, "a", TransitionType.SYMBOL)

        assert hash(transition1) == hash(transition2)

    def test_str_representation(self):
        """Test de la représentation string."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)

        # Transition avec symbole
        transition1 = Transition(source, target, "a", TransitionType.SYMBOL)
        assert str(transition1) == "State(q0) --a--> State(q1)"

        # Transition epsilon
        transition2 = Transition(source, target, None, TransitionType.EPSILON)
        assert str(transition2) == "State(q0) --ε--> State(q1)"

    def test_transition_immutability(self):
        """Test que la transition est immuable."""
        source = State("q0", StateType.INITIAL)
        target = State("q1", StateType.FINAL)
        transition = Transition(source, target, "a", TransitionType.SYMBOL)

        # Vérifier que la transition est hashable (nécessaire pour l'immutabilité)
        transition_set = {transition}
        assert transition in transition_set

        # Vérifier que la transition ne peut pas être modifiée
        with pytest.raises(AttributeError):
            transition.symbol = "b"
