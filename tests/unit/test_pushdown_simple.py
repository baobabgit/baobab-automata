"""Tests simples pour les modules pushdown."""

import pytest
from baobab_automata.pushdown.dpda import DPDA
from baobab_automata.pushdown.npda import NPDA
from baobab_automata.pushdown.pda import PDA
from baobab_automata.pushdown.dpda.dpda_exceptions import InvalidDPDAError
from baobab_automata.pushdown.npda.npda_exceptions import InvalidNPDAError
from baobab_automata.pushdown.pda.pda_exceptions import InvalidPDAError


@pytest.mark.unit
class TestPushdownSimple:
    """Tests simples pour les modules pushdown."""

    def test_dpda_creation_basic(self):
        """Test la création basique d'un DPDA."""
        dpda = DPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q1", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        assert len(dpda.states) == 2
        assert dpda.initial_state == "q0"
        assert len(dpda.final_states) == 1
        assert "q1" in dpda.final_states
        assert dpda.input_alphabet == {"a"}
        assert dpda.stack_alphabet == {"Z"}

    def test_dpda_creation_with_name(self):
        """Test la création d'un DPDA avec nom."""
        dpda = DPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q1", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
            name="test_dpda",
        )
        
        assert dpda.name == "test_dpda"

    def test_dpda_creation_invalid_state(self):
        """Test la création d'un DPDA avec état invalide."""
        with pytest.raises(InvalidDPDAError):
            DPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q0", "a", "Z"): ("q1", "Z")},
                initial_state="q1",  # q1 n'est pas dans states
                initial_stack_symbol="Z",
                final_states=set(),
            )

    def test_dpda_creation_invalid_final_state(self):
        """Test la création d'un DPDA avec état final invalide."""
        with pytest.raises(InvalidDPDAError):
            DPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q0", "a", "Z"): ("q0", "Z")},
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states={"q1"},  # q1 n'est pas dans states
            )

    def test_dpda_creation_invalid_transition_state(self):
        """Test la création d'un DPDA avec transition invalide."""
        with pytest.raises(InvalidDPDAError):
            DPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q1", "a", "Z"): ("q0", "Z")},  # q1 n'est pas dans states
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states=set(),
            )

    def test_dpda_creation_invalid_initial_stack_symbol(self):
        """Test la création d'un DPDA avec symbole de pile initial invalide."""
        with pytest.raises(InvalidDPDAError):
            DPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q0", "a", "Z"): ("q0", "Z")},
                initial_state="q0",
                initial_stack_symbol="A",  # A n'est pas dans stack_alphabet
                final_states=set(),
            )

    def test_dpda_properties(self):
        """Test les propriétés du DPDA."""
        dpda = DPDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z", "A"},
            transitions={("q0", "a", "Z"): ("q1", "AZ")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        assert dpda.states == {"q0", "q1"}
        assert dpda.input_alphabet == {"a", "b"}
        assert dpda.stack_alphabet == {"Z", "A"}
        assert dpda.initial_state == "q0"
        assert dpda.initial_stack_symbol == "Z"
        assert dpda.final_states == {"q1"}

    def test_dpda_string_representation(self):
        """Test la représentation string."""
        dpda = DPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q1", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        str_repr = str(dpda)
        assert "DPDA" in str_repr

    def test_dpda_repr(self):
        """Test la représentation repr."""
        dpda = DPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q1", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        repr_str = repr(dpda)
        assert "DPDA" in repr_str

    def test_npda_creation_basic(self):
        """Test la création basique d'un NPDA."""
        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        assert len(npda.states) == 2
        assert npda.initial_state == "q0"
        assert len(npda.final_states) == 1
        assert "q1" in npda.final_states
        assert npda.input_alphabet == {"a"}
        assert npda.stack_alphabet == {"Z"}

    def test_npda_creation_with_name(self):
        """Test la création d'un NPDA avec nom."""
        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
            name="test_npda",
        )
        
        assert npda.name == "test_npda"

    def test_npda_creation_invalid_state(self):
        """Test la création d'un NPDA avec état invalide."""
        with pytest.raises(InvalidNPDAError):
            NPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q0", "a", "Z"): {("q1", "Z")}},
                initial_state="q1",  # q1 n'est pas dans states
                initial_stack_symbol="Z",
                final_states=set(),
            )

    def test_npda_creation_invalid_final_state(self):
        """Test la création d'un NPDA avec état final invalide."""
        with pytest.raises(InvalidNPDAError):
            NPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q0", "a", "Z"): {("q0", "Z")}},
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states={"q1"},  # q1 n'est pas dans states
            )

    def test_npda_creation_invalid_transition_state(self):
        """Test la création d'un NPDA avec transition invalide."""
        with pytest.raises(InvalidNPDAError):
            NPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q1", "a", "Z"): {("q0", "Z")}},  # q1 n'est pas dans states
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states=set(),
            )

    def test_npda_creation_invalid_initial_stack_symbol(self):
        """Test la création d'un NPDA avec symbole de pile initial invalide."""
        with pytest.raises(InvalidNPDAError):
            NPDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q0", "a", "Z"): {("q0", "Z")}},
                initial_state="q0",
                initial_stack_symbol="A",  # A n'est pas dans stack_alphabet
                final_states=set(),
            )

    def test_npda_properties(self):
        """Test les propriétés du NPDA."""
        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z", "A"},
            transitions={("q0", "a", "Z"): {("q1", "AZ")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        assert npda.states == {"q0", "q1"}
        assert npda.input_alphabet == {"a", "b"}
        assert npda.stack_alphabet == {"Z", "A"}
        assert npda.initial_state == "q0"
        assert npda.initial_stack_symbol == "Z"
        assert npda.final_states == {"q1"}

    def test_npda_string_representation(self):
        """Test la représentation string."""
        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        str_repr = str(npda)
        assert "NPDA" in str_repr

    def test_npda_repr(self):
        """Test la représentation repr."""
        npda = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        repr_str = repr(npda)
        assert "NPDA" in repr_str

    def test_pda_creation_basic(self):
        """Test la création basique d'un PDA."""
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        assert len(pda.states) == 2
        assert pda.initial_state == "q0"
        assert len(pda.final_states) == 1
        assert "q1" in pda.final_states
        assert pda.input_alphabet == {"a"}
        assert pda.stack_alphabet == {"Z"}

    def test_pda_creation_with_name(self):
        """Test la création d'un PDA avec nom."""
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
            name="test_pda",
        )
        
        assert pda.name == "test_pda"

    def test_pda_creation_invalid_state(self):
        """Test la création d'un PDA avec état invalide."""
        with pytest.raises(InvalidPDAError):
            PDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q0", "a", "Z"): {("q1", "Z")}},
                initial_state="q1",  # q1 n'est pas dans states
                initial_stack_symbol="Z",
                final_states=set(),
            )

    def test_pda_creation_invalid_final_state(self):
        """Test la création d'un PDA avec état final invalide."""
        with pytest.raises(InvalidPDAError):
            PDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q0", "a", "Z"): {("q0", "Z")}},
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states={"q1"},  # q1 n'est pas dans states
            )

    def test_pda_creation_invalid_transition_state(self):
        """Test la création d'un PDA avec transition invalide."""
        with pytest.raises(InvalidPDAError):
            PDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q1", "a", "Z"): {("q0", "Z")}},  # q1 n'est pas dans states
                initial_state="q0",
                initial_stack_symbol="Z",
                final_states=set(),
            )

    def test_pda_creation_invalid_initial_stack_symbol(self):
        """Test la création d'un PDA avec symbole de pile initial invalide."""
        with pytest.raises(InvalidPDAError):
            PDA(
                states={"q0"},
                input_alphabet={"a"},
                stack_alphabet={"Z"},
                transitions={("q0", "a", "Z"): {("q0", "Z")}},
                initial_state="q0",
                initial_stack_symbol="A",  # A n'est pas dans stack_alphabet
                final_states=set(),
            )

    def test_pda_properties(self):
        """Test les propriétés du PDA."""
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a", "b"},
            stack_alphabet={"Z", "A"},
            transitions={("q0", "a", "Z"): {("q1", "AZ")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        assert pda.states == {"q0", "q1"}
        assert pda.input_alphabet == {"a", "b"}
        assert pda.stack_alphabet == {"Z", "A"}
        assert pda.initial_state == "q0"
        assert pda.initial_stack_symbol == "Z"
        assert pda.final_states == {"q1"}

    def test_pda_string_representation(self):
        """Test la représentation string."""
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        str_repr = str(pda)
        assert "PDA" in str_repr

    def test_pda_repr(self):
        """Test la représentation repr."""
        pda = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        repr_str = repr(pda)
        assert "PDA" in repr_str

    def test_dpda_edge_cases(self):
        """Test les cas limites d'un DPDA."""
        # DPDA avec un seul état
        dpda_single = DPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q0", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q0"},
        )
        
        assert len(dpda_single.states) == 1
        assert dpda_single.initial_state == "q0"
        assert "q0" in dpda_single.final_states
        
        # DPDA sans états finaux
        dpda_no_final = DPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q0", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states=set(),
        )
        
        assert len(dpda_no_final.final_states) == 0

    def test_npda_edge_cases(self):
        """Test les cas limites d'un NPDA."""
        # NPDA avec un seul état
        npda_single = NPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q0", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q0"},
        )
        
        assert len(npda_single.states) == 1
        assert npda_single.initial_state == "q0"
        assert "q0" in npda_single.final_states
        
        # NPDA sans états finaux
        npda_no_final = NPDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q0", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states=set(),
        )
        
        assert len(npda_no_final.final_states) == 0

    def test_pda_edge_cases(self):
        """Test les cas limites d'un PDA."""
        # PDA avec un seul état
        pda_single = PDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q0", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q0"},
        )
        
        assert len(pda_single.states) == 1
        assert pda_single.initial_state == "q0"
        assert "q0" in pda_single.final_states
        
        # PDA sans états finaux
        pda_no_final = PDA(
            states={"q0"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q0", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states=set(),
        )
        
        assert len(pda_no_final.final_states) == 0

    def test_dpda_multiple_instances(self):
        """Test plusieurs instances de DPDA."""
        dpda1 = DPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): ("q1", "Z")},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        dpda2 = DPDA(
            states={"q0", "q2"},
            input_alphabet={"b"},
            stack_alphabet={"A"},
            transitions={("q0", "b", "A"): ("q2", "A")},
            initial_state="q0",
            initial_stack_symbol="A",
            final_states={"q2"},
        )
        
        assert dpda1 != dpda2
        assert dpda1.states != dpda2.states
        assert dpda1.input_alphabet != dpda2.input_alphabet
        assert dpda1.stack_alphabet != dpda2.stack_alphabet

    def test_npda_multiple_instances(self):
        """Test plusieurs instances de NPDA."""
        npda1 = NPDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        npda2 = NPDA(
            states={"q0", "q2"},
            input_alphabet={"b"},
            stack_alphabet={"A"},
            transitions={("q0", "b", "A"): {("q2", "A")}},
            initial_state="q0",
            initial_stack_symbol="A",
            final_states={"q2"},
        )
        
        assert npda1 != npda2
        assert npda1.states != npda2.states
        assert npda1.input_alphabet != npda2.input_alphabet
        assert npda1.stack_alphabet != npda2.stack_alphabet

    def test_pda_multiple_instances(self):
        """Test plusieurs instances de PDA."""
        pda1 = PDA(
            states={"q0", "q1"},
            input_alphabet={"a"},
            stack_alphabet={"Z"},
            transitions={("q0", "a", "Z"): {("q1", "Z")}},
            initial_state="q0",
            initial_stack_symbol="Z",
            final_states={"q1"},
        )
        
        pda2 = PDA(
            states={"q0", "q2"},
            input_alphabet={"b"},
            stack_alphabet={"A"},
            transitions={("q0", "b", "A"): {("q2", "A")}},
            initial_state="q0",
            initial_stack_symbol="A",
            final_states={"q2"},
        )
        
        assert pda1 != pda2
        assert pda1.states != pda2.states
        assert pda1.input_alphabet != pda2.input_alphabet
        assert pda1.stack_alphabet != pda2.stack_alphabet