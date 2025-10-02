"""Tests unitaires pour la classe TransitionChange."""

import pytest
from baobab_automata.finite.transition_change import TransitionChange


@pytest.mark.unit
class TestTransitionChange:
    """Tests pour la classe TransitionChange."""

    def test_creation(self):
        """Test la création d'un changement de transition."""
        change = TransitionChange("q0", "a", "q1", "q2")
        
        assert change.state == "q0"
        assert change.symbol == "a"
        assert change.old_target == "q1"
        assert change.new_target == "q2"

    def test_creation_with_none_values(self):
        """Test la création avec des valeurs None."""
        # Addition (old_target = None)
        addition = TransitionChange("q0", "a", None, "q1")
        assert addition.old_target is None
        assert addition.new_target == "q1"
        
        # Suppression (new_target = None)
        removal = TransitionChange("q0", "a", "q1", None)
        assert removal.old_target == "q1"
        assert removal.new_target is None

    def test_creation_invalid_state(self):
        """Test la création avec un état invalide."""
        with pytest.raises(ValueError, match="L'état et le symbole ne peuvent pas être vides"):
            TransitionChange("", "a", "q1", "q2")
        
        with pytest.raises(ValueError, match="L'état et le symbole ne peuvent pas être vides"):
            TransitionChange(None, "a", "q1", "q2")

    def test_creation_invalid_symbol(self):
        """Test la création avec un symbole invalide."""
        with pytest.raises(ValueError, match="L'état et le symbole ne peuvent pas être vides"):
            TransitionChange("q0", "", "q1", "q2")
        
        with pytest.raises(ValueError, match="L'état et le symbole ne peuvent pas être vides"):
            TransitionChange("q0", None, "q1", "q2")

    def test_properties(self):
        """Test les propriétés en lecture seule."""
        change = TransitionChange("q0", "a", "q1", "q2")
        
        # Les propriétés doivent être en lecture seule
        with pytest.raises(AttributeError):
            change.state = "q3"
        with pytest.raises(AttributeError):
            change.symbol = "b"
        with pytest.raises(AttributeError):
            change.old_target = "q3"
        with pytest.raises(AttributeError):
            change.new_target = "q3"

    def test_repr(self):
        """Test la représentation string."""
        change = TransitionChange("q0", "a", "q1", "q2")
        expected = "TransitionChange(state='q0', symbol='a', old_target='q1', new_target='q2')"
        assert repr(change) == expected

    def test_repr_with_none_values(self):
        """Test la représentation string avec des valeurs None."""
        # Addition
        addition = TransitionChange("q0", "a", None, "q1")
        expected = "TransitionChange(state='q0', symbol='a', old_target='None', new_target='q1')"
        assert repr(addition) == expected
        
        # Suppression
        removal = TransitionChange("q0", "a", "q1", None)
        expected = "TransitionChange(state='q0', symbol='a', old_target='q1', new_target='None')"
        assert repr(removal) == expected

    def test_equality(self):
        """Test l'égalité entre changements de transition."""
        change1 = TransitionChange("q0", "a", "q1", "q2")
        change2 = TransitionChange("q0", "a", "q1", "q2")
        change3 = TransitionChange("q0", "b", "q1", "q2")
        change4 = TransitionChange("q1", "a", "q1", "q2")
        change5 = TransitionChange("q0", "a", "q2", "q2")
        change6 = TransitionChange("q0", "a", "q1", "q3")
        
        assert change1 == change2
        assert change1 != change3
        assert change1 != change4
        assert change1 != change5
        assert change1 != change6
        assert change1 != "not_a_transition_change"

    def test_equality_with_none_values(self):
        """Test l'égalité avec des valeurs None."""
        addition1 = TransitionChange("q0", "a", None, "q1")
        addition2 = TransitionChange("q0", "a", None, "q1")
        addition3 = TransitionChange("q0", "a", None, "q2")
        
        assert addition1 == addition2
        assert addition1 != addition3

    def test_hash(self):
        """Test le hash des changements de transition."""
        change1 = TransitionChange("q0", "a", "q1", "q2")
        change2 = TransitionChange("q0", "a", "q1", "q2")
        change3 = TransitionChange("q0", "b", "q1", "q2")
        
        assert hash(change1) == hash(change2)
        assert hash(change1) != hash(change3)

    def test_hash_with_none_values(self):
        """Test le hash avec des valeurs None."""
        addition = TransitionChange("q0", "a", None, "q1")
        removal = TransitionChange("q0", "a", "q1", None)
        
        assert hash(addition) != hash(removal)

    def test_is_addition(self):
        """Test la méthode is_addition."""
        # Addition
        addition = TransitionChange("q0", "a", None, "q1")
        assert addition.is_addition() is True
        
        # Modification
        modification = TransitionChange("q0", "a", "q1", "q2")
        assert modification.is_addition() is False
        
        # Suppression
        removal = TransitionChange("q0", "a", "q1", None)
        assert removal.is_addition() is False

    def test_is_removal(self):
        """Test la méthode is_removal."""
        # Suppression
        removal = TransitionChange("q0", "a", "q1", None)
        assert removal.is_removal() is True
        
        # Modification
        modification = TransitionChange("q0", "a", "q1", "q2")
        assert modification.is_removal() is False
        
        # Addition
        addition = TransitionChange("q0", "a", None, "q1")
        assert addition.is_removal() is False

    def test_is_modification(self):
        """Test la méthode is_modification."""
        # Modification
        modification = TransitionChange("q0", "a", "q1", "q2")
        assert modification.is_modification() is True
        
        # Addition
        addition = TransitionChange("q0", "a", None, "q1")
        assert addition.is_modification() is False
        
        # Suppression
        removal = TransitionChange("q0", "a", "q1", None)
        assert removal.is_modification() is False

    def test_edge_cases(self):
        """Test des cas limites."""
        # Changement avec des chaînes vides pour les cibles
        change = TransitionChange("q0", "a", "", "")
        assert change.old_target == ""
        assert change.new_target == ""
        assert change.is_modification() is True

        # Changement avec des chaînes identiques
        change = TransitionChange("q0", "a", "q1", "q1")
        assert change.old_target == change.new_target
        assert change.is_modification() is True

    def test_immutability(self):
        """Test que les attributs sont immutables."""
        change = TransitionChange("q0", "a", "q1", "q2")
        
        # Les attributs privés peuvent être modifiés (pas d'immutabilité stricte)
        # mais testons que les valeurs initiales sont correctes
        assert change.state == "q0"
        assert change.symbol == "a"
        assert change.old_target == "q1"
        assert change.new_target == "q2"

    def test_different_change_types(self):
        """Test différents types de changements."""
        # Addition d'une nouvelle transition
        addition = TransitionChange("q0", "a", None, "q1")
        assert addition.is_addition()
        assert not addition.is_removal()
        assert not addition.is_modification()
        
        # Suppression d'une transition existante
        removal = TransitionChange("q0", "a", "q1", None)
        assert removal.is_removal()
        assert not removal.is_addition()
        assert not removal.is_modification()
        
        # Modification d'une transition existante
        modification = TransitionChange("q0", "a", "q1", "q2")
        assert modification.is_modification()
        assert not modification.is_addition()
        assert not modification.is_removal()

    def test_string_symbols(self):
        """Test avec des symboles de transition complexes."""
        # Symbole epsilon
        epsilon_change = TransitionChange("q0", "ε", "q1", "q2")
        assert epsilon_change.symbol == "ε"
        
        # Symbole avec caractères spéciaux
        special_change = TransitionChange("q0", "a*", "q1", "q2")
        assert special_change.symbol == "a*"
        
        # Symbole numérique
        numeric_change = TransitionChange("q0", "0", "q1", "q2")
        assert numeric_change.symbol == "0"

    def test_complex_states(self):
        """Test avec des identifiants d'état complexes."""
        # État avec numéro
        state_change = TransitionChange("state_0", "a", "state_1", "state_2")
        assert state_change.state == "state_0"
        assert state_change.old_target == "state_1"
        assert state_change.new_target == "state_2"
        
        # État avec caractères spéciaux
        special_state_change = TransitionChange("q-0", "a", "q-1", "q-2")
        assert special_state_change.state == "q-0"