"""Tests pour les configurations pushdown."""

import pytest
from baobab_automata.pushdown.dpda.dpda_configuration import DPDAConfiguration
from baobab_automata.pushdown.npda.npda_configuration import NPDAConfiguration
from baobab_automata.pushdown.pda.pda_configuration import PDAConfiguration


@pytest.mark.unit
class TestPushdownConfigurations:
    """Tests pour les configurations pushdown."""

    def test_dpda_configuration_creation(self):
        """Test la création d'une DPDAConfiguration."""
        config = DPDAConfiguration("q0", "ab", "Z")
        assert config.state == "q0"
        assert config.remaining_input == "ab"
        assert config.stack == "Z"
        # Vérifier les propriétés calculées
        assert config.stack_top == "Z"
        assert len(config.stack) == 1
        assert len(config.stack) > 0

    def test_dpda_configuration_creation_with_none_values(self):
        """Test la création d'une DPDAConfiguration avec des valeurs None."""
        with pytest.raises(ValueError, match="L'état doit être une chaîne non vide"):
            DPDAConfiguration(None, None, None)

    def test_dpda_configuration_repr(self):
        """Test la représentation d'une DPDAConfiguration."""
        config = DPDAConfiguration("q0", "ab", "Z")
        repr_str = repr(config)
        assert "DPDAConfiguration" in repr_str
        assert "q0" in repr_str
        assert "ab" in repr_str
        assert "Z" in repr_str

    def test_dpda_configuration_equality(self):
        """Test l'égalité de deux DPDAConfiguration."""
        config1 = DPDAConfiguration("q0", "ab", "Z")
        config2 = DPDAConfiguration("q0", "ab", "Z")
        config3 = DPDAConfiguration("q1", "ab", "Z")
        
        assert config1 == config2
        assert config1 != config3

    def test_dpda_configuration_hash(self):
        """Test le hash d'une DPDAConfiguration."""
        config1 = DPDAConfiguration("q0", "ab", "Z")
        config2 = DPDAConfiguration("q0", "ab", "Z")
        config3 = DPDAConfiguration("q1", "ab", "Z")
        
        assert hash(config1) == hash(config2)
        assert hash(config1) != hash(config3)

    def test_dpda_configuration_string_representation(self):
        """Test la représentation string d'une DPDAConfiguration."""
        config = DPDAConfiguration("q0", "ab", "Z")
        str_repr = str(config)
        assert "q0" in str_repr
        assert "ab" in str_repr
        assert "Z" in str_repr

    def test_npda_configuration_creation(self):
        """Test la création d'une NPDAConfiguration."""
        config = NPDAConfiguration("q0", "ab", "Z")
        assert config.state == "q0"
        assert config.remaining_input == "ab"
        assert config.stack == "Z"
        # Vérifier les propriétés calculées
        assert config.stack_top == "Z"
        assert len(config.stack) == 1
        assert len(config.stack) > 0

    def test_npda_configuration_creation_with_none_values(self):
        """Test la création d'une NPDAConfiguration avec des valeurs None."""
        with pytest.raises(ValueError, match="L'état ne peut pas être vide"):
            NPDAConfiguration(None, None, None)

    def test_npda_configuration_repr(self):
        """Test la représentation d'une NPDAConfiguration."""
        config = NPDAConfiguration("q0", "ab", "Z")
        repr_str = repr(config)
        assert "NPDAConfiguration" in repr_str
        assert "q0" in repr_str
        assert "ab" in repr_str
        assert "Z" in repr_str

    def test_npda_configuration_equality(self):
        """Test l'égalité de deux NPDAConfiguration."""
        config1 = NPDAConfiguration("q0", "ab", "Z")
        config2 = NPDAConfiguration("q0", "ab", "Z")
        config3 = NPDAConfiguration("q1", "ab", "Z")
        
        assert config1 == config2
        assert config1 != config3

    def test_npda_configuration_hash(self):
        """Test le hash d'une NPDAConfiguration."""
        config1 = NPDAConfiguration("q0", "ab", "Z")
        config2 = NPDAConfiguration("q0", "ab", "Z")
        config3 = NPDAConfiguration("q1", "ab", "Z")
        
        assert hash(config1) == hash(config2)
        assert hash(config1) != hash(config3)

    def test_npda_configuration_string_representation(self):
        """Test la représentation string d'une NPDAConfiguration."""
        config = NPDAConfiguration("q0", "ab", "Z")
        str_repr = str(config)
        assert "q0" in str_repr
        assert "ab" in str_repr
        assert "Z" in str_repr

    def test_pda_configuration_creation(self):
        """Test la création d'une PDAConfiguration."""
        config = PDAConfiguration("q0", "ab", "Z")
        assert config.state == "q0"
        assert config.remaining_input == "ab"
        assert config.stack == "Z"
        # Vérifier les propriétés calculées
        assert config.stack_top == "Z"
        assert len(config.stack) == 1
        assert len(config.stack) > 0

    def test_pda_configuration_creation_with_none_values(self):
        """Test la création d'une PDAConfiguration avec des valeurs None."""
        with pytest.raises(ValueError, match="L'état doit être une chaîne non vide"):
            PDAConfiguration(None, None, None)

    def test_pda_configuration_repr(self):
        """Test la représentation d'une PDAConfiguration."""
        config = PDAConfiguration("q0", "ab", "Z")
        repr_str = repr(config)
        assert "PDAConfiguration" in repr_str
        assert "q0" in repr_str
        assert "ab" in repr_str
        assert "Z" in repr_str

    def test_pda_configuration_equality(self):
        """Test l'égalité de deux PDAConfiguration."""
        config1 = PDAConfiguration("q0", "ab", "Z")
        config2 = PDAConfiguration("q0", "ab", "Z")
        config3 = PDAConfiguration("q1", "ab", "Z")
        
        assert config1 == config2
        assert config1 != config3

    def test_pda_configuration_hash(self):
        """Test le hash d'une PDAConfiguration."""
        config1 = PDAConfiguration("q0", "ab", "Z")
        config2 = PDAConfiguration("q0", "ab", "Z")
        config3 = PDAConfiguration("q1", "ab", "Z")
        
        assert hash(config1) == hash(config2)
        assert hash(config1) != hash(config3)

    def test_pda_configuration_string_representation(self):
        """Test la représentation string d'une PDAConfiguration."""
        config = PDAConfiguration("q0", "ab", "Z")
        str_repr = str(config)
        assert "q0" in str_repr
        assert "ab" in str_repr
        assert "Z" in str_repr

    def test_configuration_immutability(self):
        """Test l'immutabilité des configurations."""
        config = DPDAConfiguration("q0", "ab", "Z")
        with pytest.raises(AttributeError):
            config.state = "q1"
        with pytest.raises(AttributeError):
            config.remaining_input = "cd"
        with pytest.raises(AttributeError):
            config.stack = "Y"

    def test_configuration_copy(self):
        """Test la copie des configurations."""
        import copy
        config = DPDAConfiguration("q0", "ab", "Z")
        copied_config = copy.copy(config)
        assert copied_config == config
        assert copied_config is not config

    def test_configuration_deep_copy(self):
        """Test la copie profonde des configurations."""
        import copy
        config = DPDAConfiguration("q0", "ab", "Z")
        deep_copied_config = copy.deepcopy(config)
        assert deep_copied_config == config
        assert deep_copied_config is not config

    def test_configuration_serialization(self):
        """Test la sérialisation des configurations."""
        import pickle
        config = DPDAConfiguration("q0", "ab", "Z")
        serialized = pickle.dumps(config)
        deserialized = pickle.loads(serialized)
        assert deserialized == config

    def test_configuration_edge_cases(self):
        """Test les cas limites des configurations."""
        # Configuration avec pile vide
        config1 = DPDAConfiguration("q0", "", "")
        assert config1.state == "q0"
        assert config1.remaining_input == ""
        assert config1.stack == ""
        assert config1.is_empty_stack is True
        assert config1.is_accepting is True

        # Configuration avec des caractères spéciaux
        config2 = DPDAConfiguration("q0_$#@", "ab_αβγ", "Z_ε")
        assert config2.state == "q0_$#@"
        assert config2.remaining_input == "ab_αβγ"
        assert config2.stack == "Z_ε"

        # Configuration avec des nombres
        config3 = DPDAConfiguration("q0", "12", "34")
        assert config3.state == "q0"
        assert config3.remaining_input == "12"
        assert config3.stack == "34"

    def test_configuration_comparison_operators(self):
        """Test les opérateurs de comparaison des configurations."""
        config1 = DPDAConfiguration("q0", "ab", "Z")
        config2 = DPDAConfiguration("q1", "ab", "Z")
        
        # Les configurations n'ont pas d'ordre défini
        with pytest.raises(TypeError):
            assert config1 < config2
        with pytest.raises(TypeError):
            assert config1 > config2
        with pytest.raises(TypeError):
            assert config1 <= config2
        with pytest.raises(TypeError):
            assert config1 >= config2

    def test_configuration_boolean_conversion(self):
        """Test la conversion booléenne des configurations."""
        config = DPDAConfiguration("q0", "ab", "Z")
        assert bool(config) is True
        
        # Configuration avec pile vide
        config_empty = DPDAConfiguration("q0", "", "")
        assert bool(config_empty) is True

    def test_configuration_arithmetic_operations(self):
        """Test les opérations arithmétiques sur les configurations."""
        config = DPDAConfiguration("q0", "ab", "Z")
        with pytest.raises(TypeError):
            _ = config + "1"
        with pytest.raises(TypeError):
            _ = config - 1
        with pytest.raises(TypeError):
            _ = config * 2
        with pytest.raises(TypeError):
            _ = config / 2