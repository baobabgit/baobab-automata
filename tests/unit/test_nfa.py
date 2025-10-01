"""Tests unitaires pour la classe NFA."""

import pytest
from baobab_automata.finite.nfa import NFA
from baobab_automata.finite.nfa_exceptions import (
    InvalidNFAError,
    InvalidTransitionError,
    NFAError,
)


@pytest.mark.unit
class TestNFA:
    """Tests pour la classe NFA."""

    def test_nfa_creation(self):
        """Test la création d'un NFA valide."""
        nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "b"): {"q2"},
                ("q1", "a"): {"q1", "q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        assert len(nfa.states) == 3
        assert nfa.initial_state == "q0"
        assert len(nfa.final_states) == 1
        assert "q2" in nfa.final_states
        assert nfa.alphabet == {"a", "b"}

    def test_nfa_creation_with_empty_transitions(self):
        """Test la création d'un NFA sans transitions."""
        nfa = NFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )

        assert len(nfa.states) == 1
        assert nfa.initial_state == "q0"
        assert "q0" in nfa.final_states
        assert len(nfa.alphabet) == 1

    def test_nfa_creation_invalid_initial_state(self):
        """Test la création d'un NFA avec un état initial invalide."""
        with pytest.raises(InvalidNFAError):
            NFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={},
                initial_state="q2",  # État initial pas dans les états
                final_states={"q1"},
            )

    def test_nfa_creation_invalid_final_states(self):
        """Test la création d'un NFA avec des états finaux invalides."""
        with pytest.raises(InvalidNFAError):
            NFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={},
                initial_state="q0",
                final_states={"q2"},  # État final pas dans les états
            )

    def test_nfa_creation_invalid_transitions(self):
        """Test la création d'un NFA avec des transitions invalides."""
        with pytest.raises(InvalidTransitionError):
            NFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={
                    ("q0", "a"): {"q2"},  # État de destination pas dans les états
                },
                initial_state="q0",
                final_states={"q1"},
            )

    def test_nfa_creation_invalid_transition_symbol(self):
        """Test la création d'un NFA avec un symbole de transition invalide."""
        with pytest.raises(InvalidTransitionError):
            NFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={
                    ("q0", "b"): {"q1"},  # Symbole pas dans l'alphabet
                },
                initial_state="q0",
                final_states={"q1"},
            )

    def test_nfa_creation_invalid_transition_state(self):
        """Test la création d'un NFA avec un état de transition invalide."""
        with pytest.raises(InvalidTransitionError):
            NFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={
                    ("q2", "a"): {"q1"},  # État source pas dans les états
                },
                initial_state="q0",
                final_states={"q1"},
            )

    def test_nfa_accepts_word(self):
        """Test l'acceptation d'un mot par un NFA."""
        nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "b"): {"q2"},
                ("q1", "a"): {"q1", "q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        assert nfa.accepts("a") is True
        assert nfa.accepts("b") is True
        assert nfa.accepts("aa") is True
        assert nfa.accepts("ab") is False
        assert nfa.accepts("") is False

    def test_nfa_accepts_word_with_multiple_paths(self):
        """Test l'acceptation d'un mot avec plusieurs chemins possibles."""
        nfa = NFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1", "q2"},
                ("q1", "b"): {"q3"},
                ("q2", "b"): {"q3"},
            },
            initial_state="q0",
            final_states={"q3"},
        )

        assert nfa.accepts("ab") is True

    def test_nfa_accepts_word_with_no_path(self):
        """Test l'acceptation d'un mot sans chemin valide."""
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )

        assert nfa.accepts("b") is False
        assert nfa.accepts("aa") is False

    def test_nfa_accepts_empty_word(self):
        """Test l'acceptation du mot vide."""
        # NFA acceptant le mot vide
        nfa = NFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )

        assert nfa.accepts("") is True
        assert nfa.accepts("a") is False

    def test_nfa_get_transition(self):
        """Test la récupération des transitions."""
        nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "b"): {"q2"},
                ("q1", "a"): {"q1", "q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        assert nfa.get_transition("q0", "a") == {"q1"}
        assert nfa.get_transition("q0", "b") == {"q2"}
        assert nfa.get_transition("q1", "a") == {"q1", "q2"}
        assert nfa.get_transition("q0", "c") is None
        assert nfa.get_transition("q3", "a") is None

    def test_nfa_is_final_state(self):
        """Test la vérification des états finaux."""
        nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q1", "q2"},
        )

        assert nfa.is_final_state("q1") is True
        assert nfa.is_final_state("q2") is True
        assert nfa.is_final_state("q0") is False
        assert nfa.is_final_state("q3") is False

    def test_nfa_get_reachable_states(self):
        """Test la récupération des états accessibles."""
        nfa = NFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "b"): {"q2"},
                ("q1", "a"): {"q3"},
            },
            initial_state="q0",
            final_states={"q3"},
        )

        reachable = nfa.get_reachable_states()
        assert "q0" in reachable
        assert "q1" in reachable
        assert "q2" in reachable
        assert "q3" in reachable

    def test_nfa_get_reachable_states_with_unreachable(self):
        """Test la récupération des états accessibles avec des états inaccessibles."""
        nfa = NFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q2", "a"): {"q3"},  # q2 et q3 ne sont pas accessibles depuis q0
            },
            initial_state="q0",
            final_states={"q1"},
        )

        reachable = nfa.get_reachable_states()
        assert "q0" in reachable
        assert "q1" in reachable
        assert "q2" not in reachable
        assert "q3" not in reachable

    def test_nfa_validate(self):
        """Test la validation d'un NFA."""
        # NFA valide
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )
        assert nfa.validate() is True

        # NFA invalide (état initial pas dans les états)
        nfa._initial_state = "q2"
        assert nfa.validate() is False

    def test_nfa_to_dict(self):
        """Test la conversion en dictionnaire."""
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        result = nfa.to_dict()
        assert "states" in result
        assert "alphabet" in result
        assert "transitions" in result
        assert "initial_state" in result
        assert "final_states" in result
        assert result["initial_state"] == "q0"

    def test_nfa_from_dict(self):
        """Test la création depuis un dictionnaire."""
        data = {
            "states": {"q0", "q1"},
            "alphabet": {"a"},
            "transitions": {("q0", "a"): {"q1"}},
            "initial_state": "q0",
            "final_states": {"q1"},
        }

        nfa = NFA.from_dict(data)
        assert nfa.states == {"q0", "q1"}
        assert nfa.alphabet == {"a"}
        assert nfa.initial_state == "q0"
        assert nfa.final_states == {"q1"}

    def test_nfa_string_representation(self):
        """Test la représentation string d'un NFA."""
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        str_repr = str(nfa)
        assert "NFA" in str_repr
        assert "q0" in str_repr
        assert "q1" in str_repr

    def test_nfa_remove_unreachable_states(self):
        """Test la suppression des états inaccessibles."""
        nfa = NFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q2", "a"): {"q3"},  # q2 et q3 ne sont pas accessibles
            },
            initial_state="q0",
            final_states={"q1"},
        )

        nfa.remove_unreachable_states()
        assert "q0" in nfa.states
        assert "q1" in nfa.states
        assert "q2" not in nfa.states
        assert "q3" not in nfa.states

    def test_nfa_to_dfa(self):
        """Test la conversion en DFA."""
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        dfa = nfa.to_dfa()
        assert dfa.states is not None
        assert dfa.alphabet == {"a"}
        assert dfa.initial_state is not None

    def test_nfa_union(self):
        """Test l'union de deux NFA."""
        nfa1 = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        nfa2 = NFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): {"q3"}},
            initial_state="q2",
            final_states={"q3"},
        )

        union = nfa1.union(nfa2)
        assert isinstance(union, NFA)

    def test_nfa_intersection(self):
        """Test l'intersection de deux NFA."""
        nfa1 = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        nfa2 = NFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): {"q3"}},
            initial_state="q2",
            final_states={"q3"},
        )

        intersection = nfa1.intersection(nfa2)
        assert isinstance(intersection, NFA)

    def test_nfa_concatenation(self):
        """Test la concaténation de deux NFA."""
        nfa1 = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        nfa2 = NFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): {"q3"}},
            initial_state="q2",
            final_states={"q3"},
        )

        concatenation = nfa1.concatenation(nfa2)
        assert isinstance(concatenation, NFA)

    def test_nfa_kleene_star(self):
        """Test l'étoile de Kleene d'un NFA."""
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        kleene = nfa.kleene_star()
        assert isinstance(kleene, NFA)

    def test_nfa_complement(self):
        """Test le complément d'un NFA."""
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        complement = nfa.complement()
        assert isinstance(complement, NFA)

    def test_nfa_minimize(self):
        """Test la minimisation d'un NFA."""
        nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "a"): {"q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        minimized = nfa.minimize()
        assert isinstance(minimized, NFA)

    def test_nfa_edge_cases(self):
        """Test des cas limites pour les NFA."""
        # NFA avec un seul état
        single_state_nfa = NFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )

        assert single_state_nfa.accepts("") is True
        assert single_state_nfa.accepts("a") is False

        # NFA avec transitions multiples
        multi_transition_nfa = NFA(
            states={"q0", "q1", "q2"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1", "q2"},
            },
            initial_state="q0",
            final_states={"q1", "q2"},
        )

        assert multi_transition_nfa.accepts("a") is True

    def test_nfa_immutability(self):
        """Test que les propriétés sont en lecture seule."""
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        # Les propriétés ne peuvent pas être modifiées directement
        with pytest.raises(AttributeError):
            nfa.states = {"q2"}
        with pytest.raises(AttributeError):
            nfa.alphabet = {"b"}
        with pytest.raises(AttributeError):
            nfa.initial_state = "q2"
        with pytest.raises(AttributeError):
            nfa.final_states = {"q2"}

    def test_nfa_copy_behavior(self):
        """Test que les copies sont indépendantes."""
        nfa = NFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        states_copy = nfa.states
        alphabet_copy = nfa.alphabet
        final_states_copy = nfa.final_states

        # Modifier les copies ne doit pas affecter l'original
        states_copy.add("q2")
        alphabet_copy.add("b")
        final_states_copy.add("q2")

        assert "q2" not in nfa.states
        assert "b" not in nfa.alphabet
        assert "q2" not in nfa.final_states