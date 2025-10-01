"""Tests unitaires pour la classe EpsilonNFA."""

import pytest
from baobab_automata.finite.epsilon_nfa import EpsilonNFA
from baobab_automata.finite.epsilon_nfa_exceptions import (
    InvalidEpsilonNFAError,
    InvalidEpsilonTransitionError,
)


@pytest.mark.unit
class TestEpsilonNFA:
    """Tests pour la classe EpsilonNFA."""

    def test_epsilon_nfa_creation(self):
        """Test la création d'un EpsilonNFA valide."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "ε"): {"q2"},
                ("q1", "b"): {"q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        assert len(epsilon_nfa.states) == 3
        assert epsilon_nfa.initial_state == "q0"
        assert len(epsilon_nfa.final_states) == 1
        assert "q2" in epsilon_nfa.final_states
        assert epsilon_nfa.alphabet == {"a", "b"}
        assert epsilon_nfa.epsilon_symbol == "ε"

    def test_epsilon_nfa_creation_with_custom_epsilon(self):
        """Test la création d'un EpsilonNFA avec un symbole epsilon personnalisé."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "epsilon"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
            epsilon_symbol="epsilon",
        )

        assert epsilon_nfa.epsilon_symbol == "epsilon"

    def test_epsilon_nfa_creation_with_empty_transitions(self):
        """Test la création d'un EpsilonNFA sans transitions."""
        epsilon_nfa = EpsilonNFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )

        assert len(epsilon_nfa.states) == 1
        assert epsilon_nfa.initial_state == "q0"
        assert "q0" in epsilon_nfa.final_states
        assert len(epsilon_nfa.alphabet) == 1

    def test_epsilon_nfa_creation_invalid_initial_state(self):
        """Test la création d'un EpsilonNFA avec un état initial invalide."""
        with pytest.raises(InvalidEpsilonNFAError):
            EpsilonNFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={},
                initial_state="q2",  # État initial pas dans les états
                final_states={"q1"},
            )

    def test_epsilon_nfa_creation_invalid_final_states(self):
        """Test la création d'un EpsilonNFA avec des états finaux invalides."""
        with pytest.raises(InvalidEpsilonNFAError):
            EpsilonNFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={},
                initial_state="q0",
                final_states={"q2"},  # État final pas dans les états
            )

    def test_epsilon_nfa_creation_invalid_transitions(self):
        """Test la création d'un EpsilonNFA avec des transitions invalides."""
        with pytest.raises(InvalidEpsilonTransitionError):
            EpsilonNFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={
                    ("q0", "a"): {"q2"},  # État de destination pas dans les états
                },
                initial_state="q0",
                final_states={"q1"},
            )

    def test_epsilon_nfa_creation_invalid_transition_symbol(self):
        """Test la création d'un EpsilonNFA avec un symbole de transition invalide."""
        with pytest.raises(InvalidEpsilonTransitionError):
            EpsilonNFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={
                    ("q0", "b"): {"q1"},  # Symbole pas dans l'alphabet
                },
                initial_state="q0",
                final_states={"q1"},
            )

    def test_epsilon_nfa_creation_invalid_transition_state(self):
        """Test la création d'un EpsilonNFA avec un état de transition invalide."""
        with pytest.raises(InvalidEpsilonTransitionError):
            EpsilonNFA(
                states={"q0", "q1"},
                alphabet={"a"},
                transitions={
                    ("q2", "a"): {"q1"},  # État source pas dans les états
                },
                initial_state="q0",
                final_states={"q1"},
            )

    def test_epsilon_nfa_accepts_word(self):
        """Test l'acceptation d'un mot par un EpsilonNFA."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "ε"): {"q2"},
                ("q1", "b"): {"q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        assert epsilon_nfa.accepts("a") is True  # q0 -> q1 (via a)
        assert epsilon_nfa.accepts("ab") is True  # q0 -> q1 -> q2
        assert epsilon_nfa.accepts("") is True  # q0 -> q2 (via epsilon)
        assert epsilon_nfa.accepts("b") is False

    def test_epsilon_nfa_accepts_word_with_epsilon_closure(self):
        """Test l'acceptation d'un mot avec fermeture epsilon."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a"},
            transitions={
                ("q0", "ε"): {"q1", "q2"},
                ("q1", "a"): {"q3"},
                ("q2", "a"): {"q3"},
            },
            initial_state="q0",
            final_states={"q3"},
        )

        assert epsilon_nfa.accepts("a") is True  # q0 -> {q1,q2} -> q3

    def test_epsilon_nfa_accepts_word_with_no_path(self):
        """Test l'acceptation d'un mot sans chemin valide."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )

        assert epsilon_nfa.accepts("b") is False
        assert epsilon_nfa.accepts("aa") is False

    def test_epsilon_nfa_accepts_empty_word(self):
        """Test l'acceptation du mot vide."""
        # EpsilonNFA acceptant le mot vide
        epsilon_nfa = EpsilonNFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )

        assert epsilon_nfa.accepts("") is True
        assert epsilon_nfa.accepts("a") is False

    def test_epsilon_nfa_accepts_empty_word_with_epsilon(self):
        """Test l'acceptation du mot vide avec transitions epsilon."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={
                ("q0", "ε"): {"q1"},
            },
            initial_state="q0",
            final_states={"q1"},
        )

        assert epsilon_nfa.accepts("") is True  # q0 -> q1 via epsilon
        assert epsilon_nfa.accepts("a") is False

    def test_epsilon_nfa_get_transition(self):
        """Test la récupération des transitions."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "ε"): {"q2"},
                ("q1", "b"): {"q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        assert epsilon_nfa.get_transition("q0", "a") == {"q1"}
        assert epsilon_nfa.get_transition("q0", "ε") == {"q2"}
        assert epsilon_nfa.get_transition("q1", "b") == {"q2"}
        assert epsilon_nfa.get_transition("q0", "c") is None
        assert epsilon_nfa.get_transition("q3", "a") is None

    def test_epsilon_nfa_is_final_state(self):
        """Test la vérification des états finaux."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q1", "q2"},
        )

        assert epsilon_nfa.is_final_state("q1") is True
        assert epsilon_nfa.is_final_state("q2") is True
        assert epsilon_nfa.is_final_state("q0") is False
        assert epsilon_nfa.is_final_state("q3") is False

    def test_epsilon_nfa_get_reachable_states(self):
        """Test la récupération des états accessibles."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q0", "ε"): {"q2"},
                ("q1", "b"): {"q3"},
            },
            initial_state="q0",
            final_states={"q3"},
        )

        reachable = epsilon_nfa.get_reachable_states()
        assert "q0" in reachable
        assert "q1" in reachable
        assert "q2" in reachable
        assert "q3" in reachable

    def test_epsilon_nfa_get_reachable_states_with_unreachable(self):
        """Test la récupération des états accessibles avec des états inaccessibles."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q2", "a"): {"q3"},  # q2 et q3 ne sont pas accessibles depuis q0
            },
            initial_state="q0",
            final_states={"q1"},
        )

        reachable = epsilon_nfa.get_reachable_states()
        assert "q0" in reachable
        assert "q1" in reachable
        assert "q2" not in reachable
        assert "q3" not in reachable

    def test_epsilon_nfa_validate(self):
        """Test la validation d'un EpsilonNFA."""
        # EpsilonNFA valide
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )
        assert epsilon_nfa.validate() is True

        # EpsilonNFA invalide (état initial pas dans les états)
        epsilon_nfa._initial_state = "q2"
        assert epsilon_nfa.validate() is False

    def test_epsilon_nfa_to_dict(self):
        """Test la conversion en dictionnaire."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        result = epsilon_nfa.to_dict()
        assert "states" in result
        assert "alphabet" in result
        assert "transitions" in result
        assert "initial_state" in result
        assert "final_states" in result
        assert "epsilon_symbol" in result
        assert result["initial_state"] == "q0"
        assert result["epsilon_symbol"] == "ε"

    def test_epsilon_nfa_from_dict(self):
        """Test la création depuis un dictionnaire."""
        data = {
            "states": {"q0", "q1"},
            "alphabet": {"a"},
            "transitions": {("q0", "a"): {"q1"}},
            "initial_state": "q0",
            "final_states": {"q1"},
            "epsilon_symbol": "ε",
        }

        epsilon_nfa = EpsilonNFA.from_dict(data)
        assert epsilon_nfa.states == {"q0", "q1"}
        assert epsilon_nfa.alphabet == {"a"}
        assert epsilon_nfa.initial_state == "q0"
        assert epsilon_nfa.final_states == {"q1"}
        assert epsilon_nfa.epsilon_symbol == "ε"

    def test_epsilon_nfa_string_representation(self):
        """Test la représentation string d'un EpsilonNFA."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        str_repr = str(epsilon_nfa)
        assert "EpsilonNFA" in str_repr
        assert "q0" in str_repr
        assert "q1" in str_repr

    def test_epsilon_nfa_remove_unreachable_states(self):
        """Test la suppression des états inaccessibles."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q2", "a"): {"q3"},  # q2 et q3 ne sont pas accessibles
            },
            initial_state="q0",
            final_states={"q1"},
        )

        epsilon_nfa.remove_unreachable_states()
        assert "q0" in epsilon_nfa.states
        assert "q1" in epsilon_nfa.states
        assert "q2" not in epsilon_nfa.states
        assert "q3" not in epsilon_nfa.states

    def test_epsilon_nfa_to_nfa(self):
        """Test la conversion en NFA."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        nfa = epsilon_nfa.to_nfa()
        assert nfa.states is not None
        assert nfa.alphabet == {"a"}
        assert nfa.initial_state is not None

    def test_epsilon_nfa_to_dfa(self):
        """Test la conversion en DFA."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        dfa = epsilon_nfa.to_dfa()
        assert dfa.states is not None
        assert dfa.alphabet == {"a"}
        assert dfa.initial_state is not None

    def test_epsilon_nfa_union(self):
        """Test l'union de deux EpsilonNFA."""
        epsilon_nfa1 = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        epsilon_nfa2 = EpsilonNFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): {"q3"}},
            initial_state="q2",
            final_states={"q3"},
        )

        union = epsilon_nfa1.union(epsilon_nfa2)
        assert isinstance(union, EpsilonNFA)

    def test_epsilon_nfa_intersection(self):
        """Test l'intersection de deux EpsilonNFA."""
        epsilon_nfa1 = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        epsilon_nfa2 = EpsilonNFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): {"q3"}},
            initial_state="q2",
            final_states={"q3"},
        )

        intersection = epsilon_nfa1.intersection(epsilon_nfa2)
        assert isinstance(intersection, EpsilonNFA)

    def test_epsilon_nfa_concatenation(self):
        """Test la concaténation de deux EpsilonNFA."""
        epsilon_nfa1 = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        epsilon_nfa2 = EpsilonNFA(
            states={"q2", "q3"},
            alphabet={"a"},
            transitions={("q2", "a"): {"q3"}},
            initial_state="q2",
            final_states={"q3"},
        )

        concatenation = epsilon_nfa1.concatenation(epsilon_nfa2)
        assert isinstance(concatenation, EpsilonNFA)

    def test_epsilon_nfa_kleene_star(self):
        """Test l'étoile de Kleene d'un EpsilonNFA."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        kleene = epsilon_nfa.kleene_star()
        assert isinstance(kleene, EpsilonNFA)

    def test_epsilon_nfa_complement(self):
        """Test le complément d'un EpsilonNFA."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        complement = epsilon_nfa.complement()
        assert isinstance(complement, EpsilonNFA)

    def test_epsilon_nfa_minimize(self):
        """Test la minimisation d'un EpsilonNFA."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a"},
            transitions={
                ("q0", "a"): {"q1"},
                ("q1", "a"): {"q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        minimized = epsilon_nfa.minimize()
        assert isinstance(minimized, EpsilonNFA)

    def test_epsilon_nfa_edge_cases(self):
        """Test des cas limites pour les EpsilonNFA."""
        # EpsilonNFA avec un seul état
        single_state_epsilon_nfa = EpsilonNFA(
            states={"q0"},
            alphabet={"a"},
            transitions={},
            initial_state="q0",
            final_states={"q0"},
        )

        assert single_state_epsilon_nfa.accepts("") is True
        assert single_state_epsilon_nfa.accepts("a") is False

        # EpsilonNFA avec transitions epsilon multiples
        multi_epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a"},
            transitions={
                ("q0", "ε"): {"q1", "q2"},
            },
            initial_state="q0",
            final_states={"q1", "q2"},
        )

        assert multi_epsilon_nfa.accepts("") is True

    def test_epsilon_nfa_immutability(self):
        """Test que les propriétés sont en lecture seule."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        # Les propriétés ne peuvent pas être modifiées directement
        with pytest.raises(AttributeError):
            epsilon_nfa.states = {"q2"}
        with pytest.raises(AttributeError):
            epsilon_nfa.alphabet = {"b"}
        with pytest.raises(AttributeError):
            epsilon_nfa.initial_state = "q2"
        with pytest.raises(AttributeError):
            epsilon_nfa.final_states = {"q2"}

    def test_epsilon_nfa_copy_behavior(self):
        """Test que les copies sont indépendantes."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1"},
            alphabet={"a"},
            transitions={("q0", "a"): {"q1"}},
            initial_state="q0",
            final_states={"q1"},
        )

        states_copy = epsilon_nfa.states
        alphabet_copy = epsilon_nfa.alphabet
        final_states_copy = epsilon_nfa.final_states

        # Modifier les copies ne doit pas affecter l'original
        states_copy.add("q2")
        alphabet_copy.add("b")
        final_states_copy.add("q2")

        assert "q2" not in epsilon_nfa.states
        assert "b" not in epsilon_nfa.alphabet
        assert "q2" not in epsilon_nfa.final_states

    def test_epsilon_nfa_epsilon_closure_caching(self):
        """Test la mise en cache des fermetures epsilon."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2"},
            alphabet={"a"},
            transitions={
                ("q0", "ε"): {"q1"},
                ("q1", "ε"): {"q2"},
            },
            initial_state="q0",
            final_states={"q2"},
        )

        # La première fois, le cache est vide
        assert len(epsilon_nfa._epsilon_closure_cache) == 0

        # Après avoir calculé une fermeture epsilon, elle est mise en cache
        epsilon_nfa._get_epsilon_closure({"q0"})
        assert len(epsilon_nfa._epsilon_closure_cache) > 0

    def test_epsilon_nfa_complex_epsilon_transitions(self):
        """Test des transitions epsilon complexes."""
        epsilon_nfa = EpsilonNFA(
            states={"q0", "q1", "q2", "q3", "q4"},
            alphabet={"a", "b"},
            transitions={
                ("q0", "ε"): {"q1", "q2"},
                ("q1", "a"): {"q3"},
                ("q2", "b"): {"q4"},
                ("q3", "ε"): {"q4"},
            },
            initial_state="q0",
            final_states={"q4"},
        )

        assert epsilon_nfa.accepts("a") is True  # q0 -> {q1,q2} -> q3 -> q4
        assert epsilon_nfa.accepts("b") is True  # q0 -> {q1,q2} -> q4
        assert epsilon_nfa.accepts("ab") is False